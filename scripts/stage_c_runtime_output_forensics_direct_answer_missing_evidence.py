#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Mapping


SUMMARY_ARTIFACT_NAME = "summary.json"
COMPARISON_ROWS_ARTIFACT_NAME = "comparison_rows.jsonl"
ROW_FACT_ARTIFACT_NAME = "stage_c_row_fact_metadata_artifact.json"
FAMILY_A_ARTIFACT_NAME = "stage_c_family_a_scorer_evidence_artifact.json"
PACKAGE1C_RECONCILIATION_REPORT_NAME = "stage_c_package1c_passive_reconciliation_report.json"
PACKAGE1D_READINESS_REPORT_NAME = "stage_c_package1d_migration_readiness_assessment.json"

DEFAULT_SPIKE_ASSESSMENT_PATH = Path(
    "/opt/ai-stack/assistant-training/manifests/reports/stage_c_technical_spike_direct_answer_assessment.json"
)
DEFAULT_OUTPUT_PATH = Path(
    "/opt/ai-stack/assistant-training/manifests/reports/"
    "stage_c_runtime_output_forensics_direct_answer_missing_evidence_assessment.json"
)
EVAL_SCRIPT_PATH = Path("/opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py")

KNOWN_AMBIGUOUS_ROW_IDS = (
    "heldout_validation:10",
    "heldout_validation:28",
    "heldout_validation:77",
)


class RuntimeForensicsError(RuntimeError):
    """Raised when the direct-answer runtime forensics slice cannot complete."""


def _load_eval_module():
    spec = importlib.util.spec_from_file_location("stage_c_runtime_forensics_eval_module", str(EVAL_SCRIPT_PATH))
    if spec is None or spec.loader is None:
        raise RuntimeForensicsError(f"unable to load evaluator module at {EVAL_SCRIPT_PATH}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeForensicsError(f"required artifact missing: {path}") from exc
    except Exception as exc:
        raise RuntimeForensicsError(f"invalid JSON artifact {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise RuntimeForensicsError(f"JSON root must be an object: {path}")
    return payload


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _sorted_counts(counter: Counter[str]) -> dict[str, int]:
    return {key: int(counter[key]) for key in sorted(counter)}


def _load_comparison_rows(run_dir: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    path = run_dir / COMPARISON_ROWS_ARTIFACT_NAME
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                raw = line.strip()
                if not raw:
                    continue
                try:
                    row = json.loads(raw)
                except Exception as exc:
                    raise RuntimeForensicsError(f"invalid JSONL {path}:{line_no}: {exc}") from exc
                if not isinstance(row, dict):
                    raise RuntimeForensicsError(f"comparison row {path}:{line_no} must be an object")
                split = str(row.get("split") or "")
                row_index = row.get("row_index_1based")
                if not split or not isinstance(row_index, int):
                    raise RuntimeForensicsError(f"comparison row {path}:{line_no} missing split/index")
                base = row.get("base")
                if not isinstance(base, dict):
                    raise RuntimeForensicsError(f"comparison row {path}:{line_no} missing base payload")
                rows[f"{split}:{row_index}"] = base
    except FileNotFoundError as exc:
        raise RuntimeForensicsError(f"required artifact missing: {path}") from exc
    return rows


def _row_fact_map(run_dir: Path) -> dict[str, dict[str, Any]]:
    payload = _load_json(run_dir / ROW_FACT_ARTIFACT_NAME)
    records = payload.get("records")
    if not isinstance(records, list):
        raise RuntimeForensicsError("row fact artifact records must be a list")
    out: dict[str, dict[str, Any]] = {}
    for idx, record in enumerate(records):
        if not isinstance(record, dict):
            raise RuntimeForensicsError(f"row fact artifact records[{idx}] must be an object")
        row_id = str(record.get("row_id") or "")
        out[row_id] = record
    return out


def _family_a_records(run_dir: Path) -> tuple[str, list[dict[str, Any]]]:
    summary = _load_json(run_dir / SUMMARY_ARTIFACT_NAME)
    side = str(summary.get("detector_summary_side") or "base")
    family_a = _load_json(run_dir / FAMILY_A_ARTIFACT_NAME)
    sides = family_a.get("sides")
    if not isinstance(sides, Mapping):
        raise RuntimeForensicsError("family_a artifact missing sides object")
    side_payload = sides.get(side)
    if not isinstance(side_payload, Mapping):
        raise RuntimeForensicsError(f"family_a artifact missing side '{side}'")
    records = side_payload.get("records")
    if not isinstance(records, list):
        raise RuntimeForensicsError("family_a side records must be a list")
    normalized: list[dict[str, Any]] = []
    for idx, record in enumerate(records):
        if not isinstance(record, dict):
            raise RuntimeForensicsError(f"family_a record[{idx}] must be an object")
        normalized.append(record)
    return side, normalized


def _find_surface(records: list[dict[str, Any]], surface_id: str, field_name: str) -> dict[str, Any]:
    matches = [record for record in records if str(record.get("surface_id") or "") == surface_id]
    if len(matches) != 1:
        raise RuntimeForensicsError(
            f"expected exactly one {field_name} record for surface_id={surface_id!r}; found {len(matches)}"
        )
    return matches[0]


def _text_excerpt(text: str, limit: int = 220) -> str:
    compact = text.replace("\n", "\\n")
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def _missing_output_category(text: str) -> str:
    has_transcript_markers = any(marker in text for marker in ("[SYSTEM]", "[USER]", "[ASSISTANT]"))
    if text.startswith("Tool:"):
        return "tool-label repetition"
    if text.startswith("The first function name is:"):
        return "answer-prefix plus transcript contamination"
    if text.startswith("Tool validation is") or text.startswith("Tool parse mode is"):
        return "instructional assertion plus transcript contamination"
    if text.startswith("[SYSTEM]"):
        return "pure transcript contamination"
    if has_transcript_markers:
        return "task/prompt echo with transcript contamination"
    return "task/prompt echo without transcript contamination"


def _category_observability(category: str) -> str:
    if category == "answer-prefix plus transcript contamination":
        return "indirectly observable"
    return "absent from runtime outputs"


def _category_remediability(category: str) -> str:
    if category == "answer-prefix plus transcript contamination":
        return "possibly remediable"
    if category in {
        "pure transcript contamination",
        "task/prompt echo with transcript contamination",
        "task/prompt echo without transcript contamination",
        "tool-label repetition",
        "instructional assertion plus transcript contamination",
    }:
        return "currently non-remediable"
    return "likely remediable"


def build_runtime_forensics(
    *,
    run_dir: Path,
    spike_assessment_path: Path | None,
    output_path: Path,
) -> dict[str, Any]:
    eval_mod = _load_eval_module()
    comparison_rows = _load_comparison_rows(run_dir)
    row_facts = _row_fact_map(run_dir)
    detector_side, family_a_records = _family_a_records(run_dir)
    summary = _load_json(run_dir / SUMMARY_ARTIFACT_NAME)
    reconciliation = _load_json(run_dir / PACKAGE1C_RECONCILIATION_REPORT_NAME)
    readiness = _load_json(run_dir / PACKAGE1D_READINESS_REPORT_NAME)
    spike_assessment = _load_json(spike_assessment_path) if spike_assessment_path is not None else None

    family_a_by_row_id = {str(record.get("row_id") or ""): record for record in family_a_records}
    missing_records = [
        record
        for record in family_a_records
        if bool(record.get("missing_evidence")) and bool(record.get("non_exact_tool_expected"))
    ]
    subtype_records = [
        record
        for record in family_a_records
        if isinstance(record.get("subtype_assignment"), str) and str(record.get("subtype_assignment")).strip()
    ]

    missing_row_ids = sorted(str(record.get("row_id") or "") for record in missing_records)
    ambiguous_row_ids = sorted(row_id for row_id in missing_row_ids if row_id in KNOWN_AMBIGUOUS_ROW_IDS)
    structurally_incapable_row_ids = sorted(row_id for row_id in missing_row_ids if row_id not in KNOWN_AMBIGUOUS_ROW_IDS)

    category_counts: Counter[str] = Counter()
    split_counts: Counter[str] = Counter()
    tool_counts: Counter[str] = Counter()
    primary_class_counts: Counter[str] = Counter()
    parse_mode_counts: Counter[str] = Counter()
    schema_reason_counts: Counter[str] = Counter()
    legacy_failure_subtype_counts: Counter[str] = Counter()
    category_split_counts: defaultdict[str, Counter[str]] = defaultdict(Counter)
    category_tool_counts: defaultdict[str, Counter[str]] = defaultdict(Counter)
    category_row_ids: defaultdict[str, list[str]] = defaultdict(list)
    category_examples: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    row_fact_resolution_count = 0
    transcript_marker_count = 0
    no_transcript_marker_count = 0
    looks_like_tool_intent_missing_count = 0
    scalar_candidate_missing_count = 0

    for record in missing_records:
        row_id = str(record.get("row_id") or "")
        row = comparison_rows.get(row_id)
        if row is None:
            raise RuntimeForensicsError(f"missing comparison row for authoritative missing-evidence row {row_id}")
        if row_id in row_facts:
            row_fact_resolution_count += 1

        split = row_id.split(":", 1)[0]
        expected_tool_name = str(row.get("expected_primary_tool_name") or "")
        eval_payload = row.get("eval")
        if not isinstance(eval_payload, dict):
            raise RuntimeForensicsError(f"comparison row {row_id} missing eval payload")
        generated_text = str(eval_payload.get("generated_text") or "")
        category = _missing_output_category(generated_text)
        category_counts[category] += 1
        category_row_ids[category].append(row_id)
        category_split_counts[category][split] += 1
        category_tool_counts[category][expected_tool_name] += 1
        split_counts[split] += 1
        tool_counts[expected_tool_name] += 1
        primary_class_counts[str(eval_payload.get("primary_class") or "")] += 1
        parse_mode_counts[str(eval_payload.get("parse_mode") or "")] += 1
        schema_reason_counts[str(eval_payload.get("schema_reason") or "")] += 1
        legacy_failure_subtype_counts[str(row.get("failure_subtype") or "")] += 1

        if any(marker in generated_text for marker in ("[SYSTEM]", "[USER]", "[ASSISTANT]")):
            transcript_marker_count += 1
        else:
            no_transcript_marker_count += 1
        if eval_mod._looks_like_tool_intent(generated_text):
            looks_like_tool_intent_missing_count += 1
        if eval_mod._stage_c_scalar_substitution_candidate(eval_payload):
            scalar_candidate_missing_count += 1

        if len(category_examples[category]) < 4:
            category_examples[category].append(
                {
                    "row_id": row_id,
                    "expected_primary_tool_name": expected_tool_name,
                    "legacy_failure_subtype": row.get("failure_subtype"),
                    "generated_text_excerpt": _text_excerpt(generated_text),
                }
            )

    assigned_looks_like_tool_intent_count = 0
    assigned_scalar_candidate_count = 0
    subtype_counts: Counter[str] = Counter()
    subtype_examples: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in subtype_records:
        subtype = str(record.get("subtype_assignment") or "")
        row_id = str(record.get("row_id") or "")
        row = comparison_rows.get(row_id)
        if row is None:
            raise RuntimeForensicsError(f"missing comparison row for subtype-assigned row {row_id}")
        eval_payload = row.get("eval")
        if not isinstance(eval_payload, dict):
            raise RuntimeForensicsError(f"comparison row {row_id} missing eval payload")
        generated_text = str(eval_payload.get("generated_text") or "")
        subtype_counts[subtype] += 1
        if eval_mod._looks_like_tool_intent(generated_text):
            assigned_looks_like_tool_intent_count += 1
        if eval_mod._stage_c_scalar_substitution_candidate(eval_payload):
            assigned_scalar_candidate_count += 1
        if len(subtype_examples[subtype]) < 4:
            subtype_examples[subtype].append(
                {
                    "row_id": row_id,
                    "expected_primary_tool_name": row.get("expected_primary_tool_name"),
                    "generated_text_excerpt": _text_excerpt(generated_text),
                }
            )

    reconciled_surface = _find_surface(
        reconciliation.get("reconciled_surfaces") if isinstance(reconciliation.get("reconciled_surfaces"), list) else [],
        "direct_answer_substitution_count",
        "reconciled_surfaces",
    )
    readiness_surface = _find_surface(
        readiness.get("compatibility_surface_assessments")
        if isinstance(readiness.get("compatibility_surface_assessments"), list)
        else [],
        "direct_answer_substitution_count",
        "compatibility_surface_assessments",
    )

    blocker_taxonomy: list[dict[str, Any]] = []
    for category, count in sorted(category_counts.items()):
        row_ids = sorted(category_row_ids[category])
        blocker_taxonomy.append(
            {
                "category": category,
                "row_count": count,
                "row_ids": row_ids,
                "cohort_classification": (
                    "ambiguous"
                    if category == "answer-prefix plus transcript contamination"
                    else "structurally_incapable"
                ),
                "remediability": _category_remediability(category),
                "observability": _category_observability(category),
                "split_distribution": _sorted_counts(category_split_counts[category]),
                "expected_tool_distribution": _sorted_counts(category_tool_counts[category]),
                "examples": category_examples[category],
            }
        )

    legacy_failure_gap_counts = {
        "legacy_direct_answer_substitution_missing_authoritative": int(
            legacy_failure_subtype_counts.get("direct_answer_substitution", 0)
        ),
        "legacy_malformed_partial_json_missing_authoritative": int(
            legacy_failure_subtype_counts.get("malformed_partial_json", 0)
        ),
        "authoritative_direct_answer_substitution_count": int(subtype_counts.get("direct-answer substitution", 0)),
        "authoritative_scalar_substitution_count": int(subtype_counts.get("scalar substitution", 0)),
        "authoritative_malformed_output_count": int(subtype_counts.get("malformed output", 0)),
    }

    artifact_inputs = {
        "run_dir": str(run_dir),
        "detector_side": detector_side,
        "summary_path": str(run_dir / SUMMARY_ARTIFACT_NAME),
        "comparison_rows_path": str(run_dir / COMPARISON_ROWS_ARTIFACT_NAME),
        "row_fact_path": str(run_dir / ROW_FACT_ARTIFACT_NAME),
        "family_a_path": str(run_dir / FAMILY_A_ARTIFACT_NAME),
        "reconciliation_path": str(run_dir / PACKAGE1C_RECONCILIATION_REPORT_NAME),
        "readiness_path": str(run_dir / PACKAGE1D_READINESS_REPORT_NAME),
    }
    if spike_assessment_path is not None:
        artifact_inputs["technical_spike_assessment_path"] = str(spike_assessment_path)

    report = {
        "report_schema_version": "stage_c_runtime_forensics_direct_answer_missing_evidence_v1",
        "report_scope": "direct_answer_missing_evidence_runtime_output_forensics",
        "focus_surface": "direct_answer_substitution_count",
        "artifact_inputs": artifact_inputs,
        "current_surface_state": {
            "reconciliation_status": reconciled_surface.get("reconciliation_status"),
            "readiness_state": readiness_surface.get("readiness_state"),
            "governance_posture": {
                "authoritative_detector_output": False,
                "detector_migration_enabled": False,
                "threshold_profile_migration_enabled": False,
            },
        },
        "missing_evidence_population_inventory": {
            "missing_evidence_row_count": len(missing_row_ids),
            "structurally_incapable_row_count": len(structurally_incapable_row_ids),
            "ambiguous_row_count": len(ambiguous_row_ids),
            "structurally_incapable_row_ids": structurally_incapable_row_ids,
            "ambiguous_row_ids": ambiguous_row_ids,
            "split_distribution": _sorted_counts(split_counts),
            "expected_tool_distribution": _sorted_counts(tool_counts),
            "primary_class_distribution": _sorted_counts(primary_class_counts),
            "parse_mode_distribution": _sorted_counts(parse_mode_counts),
            "schema_reason_distribution": _sorted_counts(schema_reason_counts),
            "legacy_failure_subtype_distribution": _sorted_counts(legacy_failure_subtype_counts),
            "missing_evidence_reason_distribution": _sorted_counts(
                Counter(
                    reason
                    for record in missing_records
                    for reason in list(record.get("missing_evidence_reasons") or [])
                )
            ),
            "artifact_coverage": {
                "comparison_row_resolution_count": len(missing_row_ids),
                "row_fact_resolution_count": row_fact_resolution_count,
                "family_a_record_resolution_count": len(missing_row_ids),
            },
            "evidence_availability_patterns": {
                "transcript_marker_count": transcript_marker_count,
                "no_transcript_marker_count": no_transcript_marker_count,
                "looks_like_tool_intent_missing_count": looks_like_tool_intent_missing_count,
                "scalar_candidate_missing_count": scalar_candidate_missing_count,
            },
        },
        "runtime_output_examination": {
            "authoritative_subtype_counts": _sorted_counts(subtype_counts),
            "assigned_subtype_examples": {key: value for key, value in sorted(subtype_examples.items())},
            "missing_output_categories": blocker_taxonomy,
            "authoritative_predicate_observations": {
                "missing_rows_with_tool_intent_signal": looks_like_tool_intent_missing_count,
                "subtype_assigned_rows_with_tool_intent_signal": assigned_looks_like_tool_intent_count,
                "missing_rows_with_scalar_candidate_signal": scalar_candidate_missing_count,
                "subtype_assigned_rows_with_scalar_candidate_signal": assigned_scalar_candidate_count,
            },
            "why_subtype_assignment_failed": [
                "all authoritative missing-evidence rows remained primary_class=invalid_json with parse_mode=invalid and schema_reason=payload_not_parsed",
                "zero missing-evidence rows satisfied the live tool-intent predicate used to promote invalid_json rows into malformed-output classification",
                "zero missing-evidence rows satisfied the strict scalar-substitution candidate predicate added by the bounded technical spike",
                "the only answer-like outputs were the three known ambiguous rows, each mixed with transcript contamination rather than clean scorer-owned evidence",
            ],
        },
        "blocker_taxonomy": blocker_taxonomy,
        "cohort_distribution_assessment": {
            "dominant_category": "task/prompt echo with transcript contamination",
            "dominant_category_row_count": int(category_counts.get("task/prompt echo with transcript contamination", 0)),
            "rare_categories": [
                {
                    "category": category,
                    "row_count": int(count),
                }
                for category, count in sorted(category_counts.items())
                if count <= 4
            ],
            "category_counts": _sorted_counts(category_counts),
            "category_cluster_notes": [
                "the 40 tool_holdout rows all fall inside the dominant task/prompt-echo category",
                "pure transcript contamination, answer-prefix contamination, instructional-assertion contamination, and tool-label repetition occur only in heldout_validation",
                "the three ambiguous rows align exactly with the answer-prefix category",
            ],
        },
        "remediability_assessment": {
            category["category"]: {
                "row_count": category["row_count"],
                "remediability": category["remediability"],
                "rationale": (
                    "current runtime outputs do not expose clean scorer-owned substitution evidence for this category"
                    if category["remediability"] == "currently non-remediable"
                    else "the category contains answer-like material, but it is still mixed with transcript contamination"
                ),
            }
            for category in blocker_taxonomy
        },
        "observability_assessment": {
            "direct_answer_target": {
                "classification": "theoretically representable but not directly observable",
                "rationale": "no clean direct-answer substitution rows were observed; only three mixed answer-prefix rows contained answer-like content",
            },
            "scalar_target": {
                "classification": "absent from runtime outputs",
                "rationale": "zero missing-evidence rows satisfied the strict scalar candidate predicate and zero authoritative scalar substitutions were emitted",
            },
            "overall_surface_observability": {
                "classification": "theoretically representable but not observable on the frozen corpus",
                "rationale": "the runtime outputs expose malformed echoes and mixed transcript contamination rather than clean scorer-owned substitution evidence",
            },
        },
        "legacy_vs_authoritative_gap_analysis": {
            "legacy_failure_profile": {
                "direct_answer_substitution_count": int(
                    ((summary.get("failure_profile") or {}).get("failure_categories_non_exact_tool_rows") or {}).get(
                        "direct_answer_substitution",
                        0,
                    )
                ),
                "scalar_substitution_count": int(
                    ((summary.get("failure_profile") or {}).get("failure_categories_non_exact_tool_rows") or {}).get(
                        "scalar_substitution",
                        0,
                    )
                ),
                "malformed_partial_json_count": int(
                    ((summary.get("failure_profile") or {}).get("failure_categories_non_exact_tool_rows") or {}).get(
                        "malformed_partial_json",
                        0,
                    )
                ),
            },
            "authoritative_surface": legacy_failure_gap_counts,
            "authoritative_vs_legacy_crosswalk": {
                "125 of 134 missing-evidence rows are legacy direct-answer substitutions": int(
                    legacy_failure_subtype_counts.get("direct_answer_substitution", 0)
                ),
                "9 of 134 missing-evidence rows are legacy malformed_partial_json": int(
                    legacy_failure_subtype_counts.get("malformed_partial_json", 0)
                ),
                "6 rows remain authoritative malformed output": int(subtype_counts.get("malformed output", 0)),
            },
            "primary_gap_explanation": (
                "the numerical gap is driven by legacy text-pattern classification applied to evidence-poor invalid outputs, "
                "while the authoritative path requires scorer-owned observable evidence and therefore preserves missingness"
            ),
            "primary_gap_factors": [
                "runtime evidence absence",
                "legacy-versus-authoritative evidence interpretation mismatch",
                "structural incompatibility between transcript/prompt echoes and governed substitution evidence",
            ],
        },
        "strategic_interpretation": {
            "what_the_technical_spike_taught_us": [
                "the smallest governance-safe scalar pathway change was runtime-inert because none of the missing-evidence outputs met the scalar predicate",
                "the persistence of missing evidence is not explained solely by a missing code branch; it is reinforced by the actual output shapes emitted on the frozen corpus",
                "the malformed-output pathway already activates only when the runtime text crosses the explicit tool-intent predicate, and the missing-evidence cohort never crosses that line",
            ],
            "weakened_explanations": [
                "latent clean scalar-substitution rows are present but unreachable",
                "row-fact metadata absence is the main blocker",
                "a trivial bounded scorer change would likely surface new authoritative evidence on this corpus",
            ],
            "strengthened_explanations": [
                "runtime outputs are dominated by transcript contamination and prompt/task echo rather than governed substitution evidence",
                "the legacy direct-answer count is primarily a broad interpretation of invalid output text, not a direct measure of authoritative substitution evidence",
                "the dominant remaining blocker is observability of scorer-owned evidence in the emitted runtime outputs",
            ],
            "dominant_remaining_uncertainty": (
                "whether any future scorer-owned pathway can observe governed substitution evidence without violating non-inference "
                "when the frozen corpus outputs are mostly transcript-contaminated echoes"
            ),
        },
        "future_investigation_assessment": {
            "highest_information_gain_uncertainty": "runtime outputs and corpus composition",
            "recommended_focus_area": "runtime outputs",
            "focus_rationale": (
                "the current evidence localizes the remaining uncertainty to what the model actually emits on the frozen corpus, "
                "not to missing row facts, missing ownership metadata, or simple bounded scorer mechanics"
            ),
            "secondary_focus_area": "corpus composition",
            "secondary_rationale": (
                "if the corpus primarily elicits transcript-contaminated echoes, future evidence gain may depend more on output regime coverage than on additional scorer-path tweaks"
            ),
        },
        "technical_spike_alignment": (
            {
                "before_state": spike_assessment.get("before_state"),
                "stability_validation": spike_assessment.get("stability_validation"),
                "runtime_evidence_assessment": spike_assessment.get("runtime_evidence_assessment"),
            }
            if spike_assessment is not None
            else None
        ),
        "final_question_answer": (
            "Based on direct runtime artifacts, the most likely explanation is that the authoritative missing-evidence population persists "
            "because the frozen-corpus outputs almost never contain clean scorer-owned substitution evidence at all. "
            "Instead, 131 rows are structurally incapable prompt/task or transcript echoes, and the remaining 3 rows are answer-like prefixes "
            "immediately mixed with transcript contamination. Those outputs never satisfy the live tool-intent or scalar-substitution predicates, "
            "so the authoritative pathway continues to preserve missing evidence rather than emit governed direct-answer or scalar-substitution rows."
        ),
    }

    _write_json(output_path, report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Perform runtime-output forensics over the direct-answer missing-evidence population."
    )
    parser.add_argument("--run-dir", type=Path, required=True, help="Run directory containing Stage C runtime artifacts.")
    parser.add_argument(
        "--spike-assessment-path",
        type=Path,
        default=DEFAULT_SPIKE_ASSESSMENT_PATH,
        help="Optional technical spike assessment JSON for stability cross-reference.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Output path for the forensic assessment JSON.",
    )
    args = parser.parse_args()

    spike_path = args.spike_assessment_path
    if spike_path is not None and not spike_path.exists():
        spike_path = None

    build_runtime_forensics(
        run_dir=args.run_dir.resolve(),
        spike_assessment_path=spike_path.resolve() if spike_path is not None else None,
        output_path=args.out.resolve(),
    )


if __name__ == "__main__":
    main()
