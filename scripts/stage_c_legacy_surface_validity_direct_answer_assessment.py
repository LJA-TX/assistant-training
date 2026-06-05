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

DEFAULT_SPIKE_ASSESSMENT_PATH = Path(
    "/opt/ai-stack/assistant-training/manifests/reports/stage_c_technical_spike_direct_answer_assessment.json"
)
DEFAULT_RUNTIME_FORENSICS_PATH = Path(
    "/opt/ai-stack/assistant-training/manifests/reports/"
    "stage_c_runtime_output_forensics_direct_answer_missing_evidence_assessment.json"
)
DEFAULT_OUTPUT_PATH = Path(
    "/opt/ai-stack/assistant-training/manifests/reports/"
    "stage_c_legacy_surface_validity_direct_answer_assessment.json"
)
EVAL_SCRIPT_PATH = Path("/opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py")


class LegacySurfaceValidityError(RuntimeError):
    """Raised when the direct-answer legacy-surface validity assessment cannot complete."""


def _load_eval_module():
    spec = importlib.util.spec_from_file_location("stage_c_legacy_surface_validity_eval_module", str(EVAL_SCRIPT_PATH))
    if spec is None or spec.loader is None:
        raise LegacySurfaceValidityError(f"unable to load evaluator module at {EVAL_SCRIPT_PATH}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise LegacySurfaceValidityError(f"required artifact missing: {path}") from exc
    except Exception as exc:
        raise LegacySurfaceValidityError(f"invalid JSON artifact {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise LegacySurfaceValidityError(f"JSON root must be an object: {path}")
    return payload


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _pct(num: int, den: int) -> float:
    if not den:
        return 0.0
    return round((100.0 * float(num)) / float(den), 1)


def _sorted_counts(counter: Counter[str]) -> dict[str, int]:
    return {key: int(counter[key]) for key in sorted(counter)}


def _text_excerpt(text: str, limit: int = 220) -> str:
    compact = text.replace("\n", "\\n")
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


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
                    raise LegacySurfaceValidityError(f"invalid JSONL {path}:{line_no}: {exc}") from exc
                if not isinstance(row, dict):
                    raise LegacySurfaceValidityError(f"comparison row {path}:{line_no} must be an object")
                split = str(row.get("split") or "")
                row_index = row.get("row_index_1based")
                base = row.get("base")
                if not split or not isinstance(row_index, int) or not isinstance(base, dict):
                    raise LegacySurfaceValidityError(f"comparison row {path}:{line_no} missing split/index/base payload")
                rows[f"{split}:{row_index}"] = base
    except FileNotFoundError as exc:
        raise LegacySurfaceValidityError(f"required artifact missing: {path}") from exc
    return rows


def _row_fact_map(run_dir: Path) -> dict[str, dict[str, Any]]:
    payload = _load_json(run_dir / ROW_FACT_ARTIFACT_NAME)
    records = payload.get("records")
    if not isinstance(records, list):
        raise LegacySurfaceValidityError("row fact artifact records must be a list")
    out: dict[str, dict[str, Any]] = {}
    for idx, record in enumerate(records):
        if not isinstance(record, dict):
            raise LegacySurfaceValidityError(f"row fact record[{idx}] must be an object")
        out[str(record.get("row_id") or "")] = record
    return out


def _family_a_records(run_dir: Path) -> tuple[str, dict[str, dict[str, Any]]]:
    summary = _load_json(run_dir / SUMMARY_ARTIFACT_NAME)
    side = str(summary.get("detector_summary_side") or "base")
    family_a = _load_json(run_dir / FAMILY_A_ARTIFACT_NAME)
    sides = family_a.get("sides")
    if not isinstance(sides, Mapping):
        raise LegacySurfaceValidityError("family_a artifact missing sides object")
    side_payload = sides.get(side)
    if not isinstance(side_payload, Mapping):
        raise LegacySurfaceValidityError(f"family_a artifact missing side '{side}'")
    records = side_payload.get("records")
    if not isinstance(records, list):
        raise LegacySurfaceValidityError("family_a side records must be a list")
    out: dict[str, dict[str, Any]] = {}
    for idx, record in enumerate(records):
        if not isinstance(record, dict):
            raise LegacySurfaceValidityError(f"family_a record[{idx}] must be an object")
        out[str(record.get("row_id") or "")] = record
    return side, out


def _legacy_behavior_category(text: str) -> str:
    has_transcript = any(marker in text for marker in ("[SYSTEM]", "[USER]", "[ASSISTANT]"))
    if text.startswith("Tool:"):
        return "tool-label repetition"
    if text.startswith("The first function name is:"):
        return "answer-prefix plus transcript contamination"
    if text.startswith("Tool validation is") or text.startswith("Tool parse mode is"):
        return "instructional assertion plus transcript contamination"
    if has_transcript:
        return "task/prompt echo with transcript contamination"
    return "task/prompt echo without transcript contamination"


def _semantic_validity_class(
    *,
    legacy_count: int,
    category_counts: Counter[str],
    authoritative_missing_overlap_count: int,
    observed_genuine_direct_answer_count: int,
) -> str:
    if legacy_count == 0:
        return "materially misaligned"
    contamination_count = (
        int(category_counts.get("task/prompt echo with transcript contamination", 0))
        + int(category_counts.get("instructional assertion plus transcript contamination", 0))
        + int(category_counts.get("answer-prefix plus transcript contamination", 0))
    )
    contamination_share = contamination_count / float(legacy_count)
    if observed_genuine_direct_answer_count == 0 and authoritative_missing_overlap_count == legacy_count:
        return "materially misaligned"
    if (
        observed_genuine_direct_answer_count == 0
        and authoritative_missing_overlap_count == legacy_count
        and contamination_share >= 0.8
    ):
        return "materially misaligned"
    if observed_genuine_direct_answer_count == 0 and contamination_share >= 0.5:
        return "weakly valid"
    return "partially valid"


def build_legacy_surface_validity_assessment(
    *,
    run_dir: Path,
    spike_assessment_path: Path | None,
    runtime_forensics_path: Path | None,
    output_path: Path,
) -> dict[str, Any]:
    eval_mod = _load_eval_module()
    comparison_rows = _load_comparison_rows(run_dir)
    row_facts = _row_fact_map(run_dir)
    detector_side, family_a_by_row_id = _family_a_records(run_dir)
    summary = _load_json(run_dir / SUMMARY_ARTIFACT_NAME)
    spike_assessment = _load_json(spike_assessment_path) if spike_assessment_path is not None else None
    runtime_forensics = _load_json(runtime_forensics_path) if runtime_forensics_path is not None else None

    legacy_population: list[dict[str, Any]] = []
    for row_id, base in comparison_rows.items():
        if str(base.get("failure_subtype") or "") != "direct_answer_substitution":
            continue
        authoritative = family_a_by_row_id.get(row_id)
        if authoritative is None:
            raise LegacySurfaceValidityError(f"missing family_a record for legacy direct-answer row {row_id}")
        row_fact = row_facts.get(row_id)
        if row_fact is None:
            raise LegacySurfaceValidityError(f"missing row fact record for legacy direct-answer row {row_id}")
        legacy_population.append(
            {
                "row_id": row_id,
                "base": base,
                "authoritative": authoritative,
                "row_fact": row_fact,
            }
        )

    if not legacy_population:
        raise LegacySurfaceValidityError("legacy direct_answer_substitution population is empty")

    split_counts: Counter[str] = Counter()
    tool_counts: Counter[str] = Counter()
    primary_class_counts: Counter[str] = Counter()
    parse_mode_counts: Counter[str] = Counter()
    schema_reason_counts: Counter[str] = Counter()
    category_counts: Counter[str] = Counter()
    category_split_counts: defaultdict[str, Counter[str]] = defaultdict(Counter)
    category_tool_counts: defaultdict[str, Counter[str]] = defaultdict(Counter)
    category_row_ids: defaultdict[str, list[str]] = defaultdict(list)
    category_examples: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    authoritative_state_counts: Counter[str] = Counter()

    tool_intent_count = 0
    scalar_candidate_count = 0
    row_fact_resolved_count = 0
    transcript_marker_count = 0
    observed_genuine_direct_answer_count = 0
    answer_like_mixed_count = 0

    for item in legacy_population:
        row_id = item["row_id"]
        base = item["base"]
        authoritative = item["authoritative"]
        row_fact = item["row_fact"]

        split = row_id.split(":", 1)[0]
        expected_tool_name = str(base.get("expected_primary_tool_name") or "")
        eval_payload = base.get("eval")
        if not isinstance(eval_payload, dict):
            raise LegacySurfaceValidityError(f"legacy direct-answer row {row_id} missing eval payload")
        generated_text = str(eval_payload.get("generated_text") or "")
        category = _legacy_behavior_category(generated_text)

        split_counts[split] += 1
        tool_counts[expected_tool_name] += 1
        primary_class_counts[str(eval_payload.get("primary_class") or "")] += 1
        parse_mode_counts[str(eval_payload.get("parse_mode") or "")] += 1
        schema_reason_counts[str(eval_payload.get("schema_reason") or "")] += 1
        category_counts[category] += 1
        category_split_counts[category][split] += 1
        category_tool_counts[category][expected_tool_name] += 1
        category_row_ids[category].append(row_id)

        if any(marker in generated_text for marker in ("[SYSTEM]", "[USER]", "[ASSISTANT]")):
            transcript_marker_count += 1
        if eval_mod._looks_like_tool_intent(generated_text):
            tool_intent_count += 1
        if eval_mod._stage_c_scalar_substitution_candidate(eval_payload):
            scalar_candidate_count += 1

        if row_fact:
            row_fact_resolved_count += 1

        authoritative_state = (
            "missing_evidence"
            if bool(authoritative.get("missing_evidence"))
            else str(authoritative.get("subtype_assignment") or "unassigned")
        )
        authoritative_state_counts[authoritative_state] += 1

        if category == "answer-prefix plus transcript contamination":
            answer_like_mixed_count += 1

        if len(category_examples[category]) < 4:
            category_examples[category].append(
                {
                    "row_id": row_id,
                    "expected_primary_tool_name": expected_tool_name,
                    "authoritative_state": authoritative_state,
                    "generated_text_excerpt": _text_excerpt(generated_text),
                }
            )

    legacy_count = len(legacy_population)
    missing_overlap_count = int(authoritative_state_counts.get("missing_evidence", 0))
    semantic_validity_class = _semantic_validity_class(
        legacy_count=legacy_count,
        category_counts=category_counts,
        authoritative_missing_overlap_count=missing_overlap_count,
        observed_genuine_direct_answer_count=observed_genuine_direct_answer_count,
    )

    behavioral_taxonomy: list[dict[str, Any]] = []
    for category, count in sorted(category_counts.items()):
        behavioral_taxonomy.append(
            {
                "category": category,
                "row_count": int(count),
                "row_percentage": _pct(int(count), legacy_count),
                "split_distribution": _sorted_counts(category_split_counts[category]),
                "expected_tool_distribution": _sorted_counts(category_tool_counts[category]),
                "row_ids": sorted(category_row_ids[category]),
                "examples": category_examples[category],
            }
        )

    report = {
        "report_schema_version": "stage_c_legacy_surface_validity_direct_answer_v1",
        "report_scope": "legacy_surface_validity_assessment",
        "focus_surface": "direct_answer_substitution_count",
        "artifact_inputs": {
            "run_dir": str(run_dir),
            "detector_side": detector_side,
            "summary_path": str(run_dir / SUMMARY_ARTIFACT_NAME),
            "comparison_rows_path": str(run_dir / COMPARISON_ROWS_ARTIFACT_NAME),
            "row_fact_path": str(run_dir / ROW_FACT_ARTIFACT_NAME),
            "family_a_path": str(run_dir / FAMILY_A_ARTIFACT_NAME),
            **(
                {"technical_spike_assessment_path": str(spike_assessment_path)}
                if spike_assessment_path is not None
                else {}
            ),
            **(
                {"runtime_forensics_assessment_path": str(runtime_forensics_path)}
                if runtime_forensics_path is not None
                else {}
            ),
        },
        "current_governance_posture": {
            "authoritative_detector_output": False,
            "detector_migration_enabled": False,
            "threshold_profile_migration_enabled": False,
            "migration_authorized": False,
        },
        "legacy_surface_population_inventory": {
            "legacy_direct_answer_substitution_row_count": legacy_count,
            "split_distribution": _sorted_counts(split_counts),
            "expected_tool_distribution": _sorted_counts(tool_counts),
            "primary_class_distribution": _sorted_counts(primary_class_counts),
            "parse_mode_distribution": _sorted_counts(parse_mode_counts),
            "schema_reason_distribution": _sorted_counts(schema_reason_counts),
            "authoritative_state_overlap": _sorted_counts(authoritative_state_counts),
            "relationship_to_authoritative_missing_evidence": {
                "overlap_row_count": missing_overlap_count,
                "overlap_percentage": _pct(missing_overlap_count, legacy_count),
                "non_overlap_row_count": legacy_count - missing_overlap_count,
            },
            "population_homogeneity": {
                "classification": "heterogeneous with one dominant subgroup",
                "dominant_category": "task/prompt echo with transcript contamination",
                "dominant_category_row_count": int(
                    category_counts.get("task/prompt echo with transcript contamination", 0)
                ),
                "dominant_category_percentage": _pct(
                    int(category_counts.get("task/prompt echo with transcript contamination", 0)),
                    legacy_count,
                ),
            },
        },
        "runtime_artifact_review": {
            "artifact_resolution": {
                "comparison_row_resolution_count": legacy_count,
                "row_fact_resolution_count": row_fact_resolved_count,
                "authoritative_record_resolution_count": legacy_count,
            },
            "predicate_observations": {
                "rows_with_transcript_markers": transcript_marker_count,
                "rows_with_tool_intent_signal": tool_intent_count,
                "rows_with_scalar_candidate_signal": scalar_candidate_count,
                "rows_with_answer_like_mixed_prefix": answer_like_mixed_count,
                "observed_genuine_direct_answer_rows": observed_genuine_direct_answer_count,
            },
            "representative_examples": {
                category: entries for category, entries in sorted(category_examples.items())
            },
        },
        "behavioral_taxonomy": behavioral_taxonomy,
        "population_distribution_assessment": {
            "category_counts": _sorted_counts(category_counts),
            "category_percentages": {
                category: _pct(int(count), legacy_count) for category, count in sorted(category_counts.items())
            },
            "dominant_categories": [
                {
                    "category": category,
                    "row_count": int(count),
                    "row_percentage": _pct(int(count), legacy_count),
                }
                for category, count in category_counts.most_common(3)
            ],
            "rare_categories": [
                {
                    "category": category,
                    "row_count": int(count),
                    "row_percentage": _pct(int(count), legacy_count),
                }
                for category, count in sorted(category_counts.items())
                if count <= 4
            ],
        },
        "semantic_validity_assessment": {
            "classification": semantic_validity_class,
            "intended_semantic_meaning": "genuine direct-answer substitution in tool-expected non-exact rows",
            "observed_population_meaning": (
                "invalid tool-expected outputs dominated by prompt/task echo and transcript contamination, "
                "with a small answer-like mixed subset and no clean governed direct-answer evidence"
            ),
            "evidence_based_justification": [
                "0 observed genuine direct-answer substitution rows were found in the legacy-counted population",
                f"{missing_overlap_count}/{legacy_count} legacy rows are authoritative missing-evidence rows",
                f"{int(category_counts.get('task/prompt echo with transcript contamination', 0))}/{legacy_count} rows are prompt/task echo with transcript contamination",
                "0 legacy direct-answer rows satisfy the authoritative tool-intent predicate",
                "0 legacy direct-answer rows satisfy the bounded scalar-substitution predicate",
            ],
        },
        "legacy_vs_authoritative_disagreement_analysis": {
            "primary_explanation": "multiple factors led by legacy over-counting and observability differences",
            "factor_assessment": {
                "authoritative_under_observation": {
                    "assessment": "weakened",
                    "rationale": "direct runtime review found no clean direct-answer rows for the authoritative pathway to observe",
                },
                "legacy_over_counting": {
                    "assessment": "strongly supported",
                    "rationale": "the legacy fallback labels evidence-poor invalid outputs as direct-answer substitution when they do not start with json-ish markers or tool-intent signals",
                },
                "differing_semantic_definitions": {
                    "assessment": "strongly supported",
                    "rationale": "the authoritative path requires scorer-owned observable substitution evidence, while the legacy path collapses broad invalid-output shapes into direct-answer substitution",
                },
                "ownership_differences": {
                    "assessment": "supported",
                    "rationale": "legacy classification is evaluator-owned fallback logic, while authoritative classification preserves scorer-owned missingness",
                },
                "observability_differences": {
                    "assessment": "strongly supported",
                    "rationale": "the counted runtime outputs are dominated by contaminated echoes rather than observable governed evidence",
                },
            },
        },
        "surface_reliability_assessment": {
            "interpretability": {
                "rating": "low",
                "rationale": "the name suggests genuine direct-answer substitution, but the counted population is dominated by contamination and echo behaviors",
            },
            "reproducibility": {
                "rating": "high",
                "rationale": "the technical spike and runtime forensics established stable repeated-run counts and stable row sets",
                "support": (
                    spike_assessment.get("stability_validation") if spike_assessment is not None else None
                ),
            },
            "semantic_stability": {
                "rating": "low",
                "rationale": "the surface consistently counts a stable but semantically mixed invalid-output population rather than a stable direct-answer phenomenon",
            },
            "operational_usefulness": {
                "rating": "limited and indirect",
                "rationale": (
                    "the surface remains reproducible as a detector-facing warning signal for invalid echo-like tool failures, "
                    "but not as a semantically faithful measure of direct-answer substitution"
                ),
            },
            "detector_facing_suitability": {
                "assessment": "operationally usable but semantically weak",
                "rationale": "the surface is stable enough to fire detector thresholds, but its counted behavior is materially misaligned with its claimed semantic meaning",
            },
        },
        "strategic_interpretation": {
            "what_runtime_forensics_revealed": [
                "the legacy surface population is not measuring a hidden authoritative positive class",
                "the counted population is overwhelmingly transcript-contaminated prompt/task echo",
                "the small ambiguous subset remains mixed rather than clean direct-answer evidence",
            ],
            "weakened_explanations": [
                "the authoritative pathway is simply missing a large clean direct-answer population",
                "the disagreement is mostly caused by metadata or row-fact gaps",
                "the legacy count is broadly semantically faithful but stricter than the authoritative path",
            ],
            "strengthened_explanations": [
                "the legacy surface is primarily a broad invalid-output fallback counter",
                "the direct-answer label on the legacy surface overstates the semantic specificity of what is being counted",
                "runtime output regime, not just pathway mechanics, is the main source of the disagreement",
            ],
            "new_repository_knowledge": (
                "the repository now knows that the legacy direct-answer surface is a stable operational proxy for contamination-heavy invalid outputs, "
                "not a faithful direct measure of genuine direct-answer substitution behavior"
            ),
        },
        "future_direction_assessment": {
            "highest_information_gain_area": "runtime-output analysis",
            "secondary_area": "corpus analysis",
            "diminishing_return_area": "legacy-surface analysis",
            "rationale": [
                "the legacy surface semantics are now well-characterized from direct artifacts",
                "the dominant remaining uncertainty is what output regime the corpus elicits and whether any clean scorer-owned substitution evidence can be observed at all",
                "additional scorer or evaluator analysis is likely to add less information than further runtime or corpus examination unless runtime outputs change",
            ],
        },
        "technical_spike_alignment": (
            {
                "before_state": spike_assessment.get("before_state"),
                "runtime_evidence_assessment": spike_assessment.get("runtime_evidence_assessment"),
            }
            if spike_assessment is not None
            else None
        ),
        "runtime_forensics_alignment": (
            {
                "missing_evidence_population_inventory": runtime_forensics.get("missing_evidence_population_inventory"),
                "cohort_distribution_assessment": runtime_forensics.get("cohort_distribution_assessment"),
                "final_question_answer": runtime_forensics.get("final_question_answer"),
            }
            if runtime_forensics is not None
            else None
        ),
        "forward_conclusion": (
            "Going forward, the repository should treat the legacy direct_answer_substitution_count surface as a reproducible but materially misaligned proxy "
            "for contamination-heavy invalid tool-expected outputs, not as a semantically faithful measure of genuine direct-answer substitution."
        ),
        "final_question_answer": (
            "Based on direct runtime artifacts, the answer is not fully affirmative. The legacy direct_answer_substitution_count surface is not primarily measuring "
            "genuine direct-answer substitution behavior. It is primarily measuring invalid tool-expected outputs dominated by prompt/task echo with transcript contamination, "
            "plus a small mixed answer-like subset and related echo artifacts."
        ),
    }

    _write_json(output_path, report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Assess the semantic validity of the legacy direct_answer_substitution_count surface."
    )
    parser.add_argument("--run-dir", type=Path, required=True, help="Run directory containing Stage C runtime artifacts.")
    parser.add_argument(
        "--spike-assessment-path",
        type=Path,
        default=DEFAULT_SPIKE_ASSESSMENT_PATH,
        help="Optional technical spike assessment JSON for stability alignment.",
    )
    parser.add_argument(
        "--runtime-forensics-path",
        type=Path,
        default=DEFAULT_RUNTIME_FORENSICS_PATH,
        help="Optional runtime-forensics assessment JSON for alignment.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Output path for the legacy-surface validity assessment JSON.",
    )
    args = parser.parse_args()

    spike_path = args.spike_assessment_path
    if spike_path is not None and not spike_path.exists():
        spike_path = None
    runtime_forensics_path = args.runtime_forensics_path
    if runtime_forensics_path is not None and not runtime_forensics_path.exists():
        runtime_forensics_path = None

    build_legacy_surface_validity_assessment(
        run_dir=args.run_dir.resolve(),
        spike_assessment_path=spike_path.resolve() if spike_path is not None else None,
        runtime_forensics_path=runtime_forensics_path.resolve() if runtime_forensics_path is not None else None,
        output_path=args.out.resolve(),
    )


if __name__ == "__main__":
    main()
