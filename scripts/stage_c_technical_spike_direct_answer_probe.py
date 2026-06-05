#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Mapping


PACKAGE5B_SCRIPT_PATH = Path(
    "/opt/ai-stack/assistant-training/scripts/stage_c_package5b_direct_answer_blocker_persistence.py"
)
FAMILY_A_ARTIFACT_NAME = "stage_c_family_a_scorer_evidence_artifact.json"
SUMMARY_ARTIFACT_NAME = "summary.json"

AMBIGUOUS_ROW_IDS = (
    "heldout_validation:10",
    "heldout_validation:28",
    "heldout_validation:77",
)


class DirectAnswerSpikeAssessmentError(RuntimeError):
    """Raised when the technical spike assessment cannot complete."""


def _load_package5b_module():
    spec = importlib.util.spec_from_file_location(
        "stage_c_package5b_direct_answer_blocker_persistence",
        str(PACKAGE5B_SCRIPT_PATH),
    )
    if spec is None or spec.loader is None:
        raise DirectAnswerSpikeAssessmentError("unable to load Package 5B persistence module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise DirectAnswerSpikeAssessmentError(f"missing required JSON artifact: {path}") from exc
    except Exception as exc:
        raise DirectAnswerSpikeAssessmentError(f"invalid JSON artifact {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise DirectAnswerSpikeAssessmentError(f"JSON root must be an object: {path}")
    return payload


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _row_status_map(run_dir: Path) -> dict[str, dict[str, Any]]:
    summary = _load_json(run_dir / SUMMARY_ARTIFACT_NAME)
    detector_side = str(summary.get("detector_summary_side") or "base")
    family_a_artifact = _load_json(run_dir / FAMILY_A_ARTIFACT_NAME)
    sides = family_a_artifact.get("sides")
    if not isinstance(sides, Mapping):
        raise DirectAnswerSpikeAssessmentError("family_a_scorer_evidence.sides must be an object")
    side_payload = sides.get(detector_side)
    if not isinstance(side_payload, Mapping):
        raise DirectAnswerSpikeAssessmentError(f"family_a_scorer_evidence missing side '{detector_side}'")
    records = side_payload.get("records")
    if not isinstance(records, list):
        raise DirectAnswerSpikeAssessmentError("family_a_scorer_evidence side records must be a list")

    status_map: dict[str, dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, Mapping):
            raise DirectAnswerSpikeAssessmentError("family_a_scorer_evidence record must be an object")
        row_id = str(record.get("row_id") or "")
        status_map[row_id] = {
            "row_id": row_id,
            "primary_outcome": record.get("primary_outcome"),
            "subtype_assignment": record.get("subtype_assignment"),
            "missing_evidence": bool(record.get("missing_evidence")),
            "missing_evidence_reasons": list(record.get("missing_evidence_reasons") or []),
            "non_exact_tool_expected": bool(record.get("non_exact_tool_expected")),
            "exact_valid": bool(record.get("exact_valid")),
        }
    return status_map


def _surface_snapshot(bundle: Mapping[str, Any]) -> dict[str, Any]:
    blocker = bundle["blocker_inventory"]
    subtype_counts = blocker.get("subtype_counts") if isinstance(blocker.get("subtype_counts"), Mapping) else {}
    focus_reconciliation = blocker["focus_surface_reconciliation"]
    focus_readiness = blocker["focus_surface_readiness"]
    return {
        "direct_answer_substitution_count": blocker.get("direct_answer_substitution_count"),
        "scalar_substitution_count": int(subtype_counts.get("scalar substitution", 0)),
        "missing_evidence_count": blocker.get("missing_evidence_count"),
        "reconciliation_state": focus_reconciliation.get("reconciliation_status"),
        "readiness_state": focus_readiness.get("readiness_state"),
        "subtype_counts": dict(sorted(subtype_counts.items())),
        "missing_evidence_reason_counts": blocker.get("missing_evidence_reason_counts"),
        "direct_answer_row_ids": blocker.get("direct_answer_row_ids"),
        "missing_evidence_row_ids": blocker.get("missing_evidence_row_ids"),
    }


def _cohort_audit(
    *,
    cohort_label: str,
    row_ids: list[str],
    before_status: Mapping[str, dict[str, Any]],
    after_status: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    unchanged: list[str] = []
    changed: list[dict[str, Any]] = []
    missing_rows: list[str] = []

    for row_id in row_ids:
        before = before_status.get(row_id)
        after = after_status.get(row_id)
        if before is None or after is None:
            missing_rows.append(row_id)
            continue
        if before == after:
            unchanged.append(row_id)
            continue
        changed.append(
            {
                "row_id": row_id,
                "before": before,
                "after": after,
            }
        )

    return {
        "cohort_label": cohort_label,
        "row_count": len(row_ids),
        "unchanged_count": len(unchanged),
        "changed_count": len(changed),
        "missing_row_count": len(missing_rows),
        "unchanged_row_ids": sorted(unchanged),
        "changed_rows": changed,
        "missing_row_ids": sorted(missing_rows),
        "all_rows_preserved": not changed and not missing_rows,
    }


def _downstream_independence(
    *,
    before_bundle: Mapping[str, Any],
    after_bundle: Mapping[str, Any],
) -> dict[str, Any]:
    before_guardrails = before_bundle.get("guardrail_results") or {}
    after_guardrails = after_bundle.get("guardrail_results") or {}
    return {
        "legacy_direct_answer_count_unchanged": (
            before_bundle["legacy_surface_snapshot"]["failure_profile_direct_answer_substitution_count"]
            == after_bundle["legacy_surface_snapshot"]["failure_profile_direct_answer_substitution_count"]
        ),
        "legacy_failure_category_distribution_unchanged": (
            before_bundle["legacy_surface_snapshot"]["failure_profile_failure_categories_non_exact_tool_rows"]
            == after_bundle["legacy_surface_snapshot"]["failure_profile_failure_categories_non_exact_tool_rows"]
        ),
        "legacy_surface_policy_unchanged": (
            before_guardrails.get("runtime_legacy_surface_policy")
            == after_guardrails.get("runtime_legacy_surface_policy")
        ),
        "guardrails_clear": bool(after_guardrails.get("guardrails_clear")),
        "migration_posture_unchanged": (
            after_bundle["blocker_inventory"]["focus_surface_reconciliation"]["reconciliation_status"]
            == "requires_future_migration"
            and after_bundle["blocker_inventory"]["focus_surface_readiness"]["readiness_state"]
            == "migration-blocked"
        ),
    }


def _stability_validation(
    *,
    before_bundle: Mapping[str, Any],
    after_bundle_a: Mapping[str, Any],
    after_bundle_b: Mapping[str, Any],
) -> dict[str, Any]:
    keys = (
        "row_id_digest",
        "tool_expected_row_id_digest",
        "non_exact_row_id_digest",
    )
    row_identity_stable = all(
        after_bundle_a["row_identity_snapshot"][key] == after_bundle_b["row_identity_snapshot"][key]
        for key in keys
    )
    evidence_stable = (
        after_bundle_a["normalized_digests"]["blocker_inventory_digest"]
        == after_bundle_b["normalized_digests"]["blocker_inventory_digest"]
        and after_bundle_a["normalized_digests"]["focus_reconciliation_digest"]
        == after_bundle_b["normalized_digests"]["focus_reconciliation_digest"]
        and after_bundle_a["normalized_digests"]["focus_readiness_digest"]
        == after_bundle_b["normalized_digests"]["focus_readiness_digest"]
    )
    before_after_generation_stable = (
        before_bundle["raw_artifact_hashes"]["comparison_rows_jsonl"]
        == after_bundle_a["raw_artifact_hashes"]["comparison_rows_jsonl"]
        == after_bundle_b["raw_artifact_hashes"]["comparison_rows_jsonl"]
    )
    return {
        "after_run_reproducible": row_identity_stable and evidence_stable,
        "row_identity_stable": row_identity_stable,
        "evidence_stable": evidence_stable,
        "comparison_rows_stable_across_before_after": before_after_generation_stable,
        "after_run_a_row_identity_snapshot": after_bundle_a["row_identity_snapshot"],
        "after_run_b_row_identity_snapshot": after_bundle_b["row_identity_snapshot"],
        "after_run_a_blocker_inventory_digest": after_bundle_a["normalized_digests"]["blocker_inventory_digest"],
        "after_run_b_blocker_inventory_digest": after_bundle_b["normalized_digests"]["blocker_inventory_digest"],
    }


def build_spike_assessment(
    *,
    before_run_dir: Path,
    after_run_dir_a: Path,
    after_run_dir_b: Path,
    before_bundle_path: Path,
    after_bundle_a_path: Path,
    after_bundle_b_path: Path,
    assessment_output_path: Path,
) -> dict[str, Any]:
    package5b = _load_package5b_module()

    package5b.build_blocker_bundle(
        run_dir=before_run_dir,
        bundle_label="before",
        output_path=before_bundle_path,
    )
    before_bundle = _load_json(before_bundle_path)

    package5b.build_blocker_bundle(
        run_dir=after_run_dir_a,
        bundle_label="after_run_a",
        output_path=after_bundle_a_path,
    )
    after_bundle_a = _load_json(after_bundle_a_path)

    package5b.build_blocker_bundle(
        run_dir=after_run_dir_b,
        bundle_label="after_run_b",
        output_path=after_bundle_b_path,
    )
    after_bundle_b = _load_json(after_bundle_b_path)

    before_status = _row_status_map(before_run_dir)
    after_status_a = _row_status_map(after_run_dir_a)
    after_status_b = _row_status_map(after_run_dir_b)

    before_missing = set(before_bundle["blocker_inventory"]["missing_evidence_row_ids"])
    ambiguous = set(AMBIGUOUS_ROW_IDS)
    if not ambiguous.issubset(before_missing):
        raise DirectAnswerSpikeAssessmentError("baseline missing-evidence cohort does not contain all expected ambiguous rows")
    structurally_incapable = sorted(before_missing - ambiguous)

    before_snapshot = _surface_snapshot(before_bundle)
    after_snapshot_a = _surface_snapshot(after_bundle_a)
    after_snapshot_b = _surface_snapshot(after_bundle_b)

    runtime_evidence_assessment = {
        "new_direct_answer_evidence_appeared": (
            after_snapshot_a["direct_answer_substitution_count"] != before_snapshot["direct_answer_substitution_count"]
        ),
        "new_scalar_evidence_appeared": (
            after_snapshot_a["scalar_substitution_count"] != before_snapshot["scalar_substitution_count"]
        ),
        "new_authoritative_evidence_appeared": (
            after_snapshot_a["direct_answer_substitution_count"] != before_snapshot["direct_answer_substitution_count"]
            or after_snapshot_a["scalar_substitution_count"] != before_snapshot["scalar_substitution_count"]
            or after_snapshot_a["missing_evidence_count"] != before_snapshot["missing_evidence_count"]
        ),
        "direct_answer_substitution_delta": (
            after_snapshot_a["direct_answer_substitution_count"] - before_snapshot["direct_answer_substitution_count"]
        ),
        "scalar_substitution_delta": (
            after_snapshot_a["scalar_substitution_count"] - before_snapshot["scalar_substitution_count"]
        ),
        "missing_evidence_delta": after_snapshot_a["missing_evidence_count"] - before_snapshot["missing_evidence_count"],
        "before_direct_answer_row_ids": before_snapshot["direct_answer_row_ids"],
        "after_direct_answer_row_ids": after_snapshot_a["direct_answer_row_ids"],
    }

    assessment = {
        "report_schema_version": "stage_c_technical_spike_direct_answer_probe_v1",
        "report_scope": "stage_c_technical_spike_direct_answer_scorer_pathway_evidence_emission_probe",
        "focus_surface": "direct_answer_substitution_count",
        "before_bundle_path": str(before_bundle_path),
        "after_run_a_bundle_path": str(after_bundle_a_path),
        "after_run_b_bundle_path": str(after_bundle_b_path),
        "before_state": before_snapshot,
        "after_state_run_a": after_snapshot_a,
        "after_state_run_b": after_snapshot_b,
        "preservation_audit": {
            "structurally_incapable_row_count": len(structurally_incapable),
            "ambiguous_row_count": len(AMBIGUOUS_ROW_IDS),
            "structurally_incapable_row_ids": structurally_incapable,
            "ambiguous_row_ids": list(AMBIGUOUS_ROW_IDS),
            "after_run_a": {
                "structurally_incapable": _cohort_audit(
                    cohort_label="structurally_incapable",
                    row_ids=structurally_incapable,
                    before_status=before_status,
                    after_status=after_status_a,
                ),
                "ambiguous": _cohort_audit(
                    cohort_label="ambiguous",
                    row_ids=list(AMBIGUOUS_ROW_IDS),
                    before_status=before_status,
                    after_status=after_status_a,
                ),
            },
            "after_run_b": {
                "structurally_incapable": _cohort_audit(
                    cohort_label="structurally_incapable",
                    row_ids=structurally_incapable,
                    before_status=before_status,
                    after_status=after_status_b,
                ),
                "ambiguous": _cohort_audit(
                    cohort_label="ambiguous",
                    row_ids=list(AMBIGUOUS_ROW_IDS),
                    before_status=before_status,
                    after_status=after_status_b,
                ),
            },
        },
        "stability_validation": _stability_validation(
            before_bundle=before_bundle,
            after_bundle_a=after_bundle_a,
            after_bundle_b=after_bundle_b,
        ),
        "downstream_independence_review": {
            "after_run_a": _downstream_independence(before_bundle=before_bundle, after_bundle=after_bundle_a),
            "after_run_b": _downstream_independence(before_bundle=before_bundle, after_bundle=after_bundle_b),
        },
        "runtime_evidence_assessment": runtime_evidence_assessment,
    }
    _write_json(assessment_output_path, assessment)
    return assessment


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before-run-dir", required=True)
    parser.add_argument("--after-run-dir-a", required=True)
    parser.add_argument("--after-run-dir-b", required=True)
    parser.add_argument("--before-bundle-out", required=True)
    parser.add_argument("--after-bundle-a-out", required=True)
    parser.add_argument("--after-bundle-b-out", required=True)
    parser.add_argument("--assessment-out", required=True)
    args = parser.parse_args()

    build_spike_assessment(
        before_run_dir=Path(args.before_run_dir).resolve(),
        after_run_dir_a=Path(args.after_run_dir_a).resolve(),
        after_run_dir_b=Path(args.after_run_dir_b).resolve(),
        before_bundle_path=Path(args.before_bundle_out).resolve(),
        after_bundle_a_path=Path(args.after_bundle_a_out).resolve(),
        after_bundle_b_path=Path(args.after_bundle_b_out).resolve(),
        assessment_output_path=Path(args.assessment_out).resolve(),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
