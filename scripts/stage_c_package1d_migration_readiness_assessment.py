#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping


STAGE_C_ROW_FACT_ARTIFACT_NAME = "stage_c_row_fact_metadata_artifact.json"
STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME = "stage_c_family_a_scorer_evidence_artifact.json"
STAGE_C_GOVERNANCE_GUARDRAILS_ARTIFACT_NAME = "stage_c_governance_guardrails_artifact.json"
STAGE_C_RUNTIME_CONTRACT_SUMMARY_ARTIFACT_NAME = "stage_c_runtime_contract_summary_artifact.json"
STAGE_C_PACKAGE1C_RECONCILIATION_REPORT_NAME = "stage_c_package1c_passive_reconciliation_report.json"
STAGE_C_PACKAGE1D_READINESS_REPORT_NAME = "stage_c_package1d_migration_readiness_assessment.json"


class MigrationReadinessAssessmentError(RuntimeError):
    """Raised when the Package 1D migration-readiness assessment cannot proceed."""


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise MigrationReadinessAssessmentError(f"required artifact missing: {path}") from exc
    except Exception as exc:
        raise MigrationReadinessAssessmentError(f"invalid JSON artifact {path}: {exc}") from exc


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _as_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    return None


def _as_nonempty_str(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _as_records(payload: Mapping[str, Any], field_name: str) -> list[dict[str, Any]]:
    records = payload.get(field_name)
    if not isinstance(records, list):
        raise MigrationReadinessAssessmentError(f"{field_name} must be a list")
    out: list[dict[str, Any]] = []
    for idx, record in enumerate(records):
        if not isinstance(record, dict):
            raise MigrationReadinessAssessmentError(f"{field_name}[{idx}] must be an object")
        out.append(record)
    return out


def _require_side_records(family_a_artifact: Mapping[str, Any], side: str) -> list[dict[str, Any]]:
    sides = family_a_artifact.get("sides")
    if not isinstance(sides, Mapping):
        raise MigrationReadinessAssessmentError("family_a_scorer_evidence.sides must be an object")
    side_payload = sides.get(side)
    if not isinstance(side_payload, Mapping):
        raise MigrationReadinessAssessmentError(f"family_a_scorer_evidence missing side '{side}'")
    return _as_records(side_payload, "records")


def _legacy_policy_preserved(runtime_summary_artifact: Mapping[str, Any]) -> bool:
    policy = dict(sorted((runtime_summary_artifact.get("legacy_surface_policy") or {}).items()))
    return policy == {
        "comparability_policy": "unchanged",
        "comparison_rows_jsonl": "preserved",
        "detector_metrics": "unchanged",
        "summary_json": "preserved",
        "threshold_behavior": "unchanged",
    }


def _guardrails_clear(guardrails_artifact: Mapping[str, Any]) -> bool:
    status = guardrails_artifact.get("guardrail_status")
    if not isinstance(status, Mapping):
        return False
    return not any(bool(value) for value in status.values())


def _taxonomy() -> dict[str, Any]:
    return {
        "migration-ready": {
            "definition": (
                "The authoritative Stage C surface and the legacy surface reconcile directly in the current run, "
                "guardrails remain clear, and no current authoritative blocker is visible in emitted evidence."
            ),
            "derived_from_package_1c": "refines reconciliation_status=aligned into a readiness judgment",
        },
        "migration-blocked": {
            "definition": (
                "The surface is conceptually comparable, but current authoritative evidence contains an explicit blocker "
                "that prevents safe migration readiness."
            ),
            "derived_from_package_1c": "refines reconciliation_status=requires_future_migration when authoritative blockers are explicit",
        },
        "not-comparable": {
            "definition": (
                "Current authoritative and legacy surfaces are explicitly non-equivalent under existing authority and "
                "must not be treated as migration-ready replacements."
            ),
            "derived_from_package_1c": "carries forward reconciliation_status=not_comparable",
        },
        "insufficient-evidence": {
            "definition": (
                "The current artifact set does not provide enough authoritative evidence to classify the surface as "
                "migration-ready or migration-blocked."
            ),
            "derived_from_package_1c": "refines reconciliation_status=requires_future_migration or unavailable when evidence is incomplete rather than blocked",
        },
    }


def _row_id_uniqueness(row_fact_artifact: Mapping[str, Any]) -> bool:
    row_fact_records = _as_records(row_fact_artifact, "records")
    row_ids = [str(record.get("row_id")) for record in row_fact_records]
    return len(set(row_ids)) == len(row_ids)


def _family_a_rows_resolve(row_fact_artifact: Mapping[str, Any], family_a_records: list[dict[str, Any]]) -> bool:
    row_ids = {str(record.get("row_id")) for record in _as_records(row_fact_artifact, "records")}
    return all(str(record.get("row_id")) in row_ids for record in family_a_records)


def _assessment_record(
    *,
    surface_id: str,
    readiness_state: str,
    reasoning: str,
    blocking_conditions: list[dict[str, Any]],
    reconciliation_record: Mapping[str, Any],
    authoritative_support: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "surface_id": surface_id,
        "readiness_state": readiness_state,
        "reasoning": reasoning,
        "blocking_conditions": list(blocking_conditions),
        "reconciliation_record": dict(reconciliation_record),
        "authoritative_support": dict(authoritative_support),
    }


def _authoritative_support_for_surface(
    *,
    surface_id: str,
    row_fact_artifact: Mapping[str, Any],
    family_a_records: list[dict[str, Any]],
) -> dict[str, Any]:
    row_fact_records = _as_records(row_fact_artifact, "records")
    family_a_by_id = {
        str(record.get("row_id")): record
        for record in family_a_records
    }

    if surface_id == "read_file_exact_valid_rate":
        read_file_row_ids = sorted(
            str(record.get("row_id"))
            for record in row_fact_records
            if _as_bool((record.get("membership_markers") or {}).get("family_b1_read_file_eligible")) is True
        )
        missing_family_a_row_ids = sorted(
            row_id for row_id in read_file_row_ids if row_id not in family_a_by_id
        )
        return {
            "read_file_row_ids": read_file_row_ids,
            "missing_family_a_row_ids": missing_family_a_row_ids,
            "exact_valid_count": sum(
                1
                for row_id in read_file_row_ids
                if _as_bool((family_a_by_id.get(row_id) or {}).get("exact_valid")) is True
            ),
        }

    if surface_id == "read_file_symbol_name_exact_valid_rate":
        declared_symbol_row_ids = sorted(
            str(record.get("row_id"))
            for record in row_fact_records
            if (record.get("membership_markers") or {}).get("family_b1_symbol_name_member") is True
        )
        missing_owner_row_ids = sorted(
            str(record.get("row_id"))
            for record in row_fact_records
            if (record.get("membership_markers") or {}).get("family_b1_symbol_name_member") is True
            and _as_nonempty_str((record.get("ownership_markers") or {}).get("symbol_name_membership_owner")) is None
        )
        missing_family_a_row_ids = sorted(
            row_id for row_id in declared_symbol_row_ids if row_id not in family_a_by_id
        )
        return {
            "declared_symbol_membership_row_ids": declared_symbol_row_ids,
            "missing_owner_row_ids": missing_owner_row_ids,
            "missing_family_a_row_ids": missing_family_a_row_ids,
        }

    if surface_id == "direct_answer_substitution_count":
        non_exact_records = [
            record for record in family_a_records if _as_bool(record.get("non_exact_tool_expected")) is True
        ]
        missing_evidence_row_ids = sorted(
            str(record.get("row_id"))
            for record in non_exact_records
            if _as_bool(record.get("missing_evidence")) is True
        )
        direct_answer_row_ids = sorted(
            str(record.get("row_id"))
            for record in non_exact_records
            if _as_nonempty_str(record.get("subtype_assignment")) == "direct-answer substitution"
        )
        return {
            "non_exact_tool_expected_row_count": len(non_exact_records),
            "direct_answer_row_ids": direct_answer_row_ids,
            "missing_evidence_row_ids": missing_evidence_row_ids,
        }

    if surface_id == "no_anchor_exact_valid_share":
        declared_anchor_row_ids = sorted(
            str(record.get("row_id"))
            for record in row_fact_records
            if _as_bool((record.get("membership_markers") or {}).get("family_b2_anchor_eligible")) is True
        )
        declared_no_anchor_row_ids = sorted(
            str(record.get("row_id"))
            for record in row_fact_records
            if _as_bool((record.get("membership_markers") or {}).get("family_b2_no_anchor_member")) is True
        )
        return {
            "declared_anchor_row_ids": declared_anchor_row_ids,
            "declared_no_anchor_row_ids": declared_no_anchor_row_ids,
        }

    return {}


def _assess_surface(
    *,
    surface: Mapping[str, Any],
    row_fact_artifact: Mapping[str, Any],
    family_a_records: list[dict[str, Any]],
    guardrails_clear: bool,
    legacy_policy_preserved: bool,
) -> dict[str, Any]:
    surface_id = str(surface.get("surface_id"))
    reconciliation_status = _as_nonempty_str(surface.get("reconciliation_status")) or "unknown"
    reason_code = _as_nonempty_str(surface.get("reason_code")) or "unknown_reason"
    reason = _as_nonempty_str(surface.get("reason")) or "No reconciliation reason provided."

    authoritative_support = _authoritative_support_for_surface(
        surface_id=surface_id,
        row_fact_artifact=row_fact_artifact,
        family_a_records=family_a_records,
    )

    blocking_conditions: list[dict[str, Any]] = []

    if not guardrails_clear:
        blocking_conditions.append(
            {
                "condition_code": "guardrails_not_clear",
                "condition_type": "governance_blocker",
                "evidence": "Stage C guardrail artifact reports active inference/substitution/reconstruction or legacy-surface modification flags.",
            }
        )
    if not legacy_policy_preserved:
        blocking_conditions.append(
            {
                "condition_code": "legacy_surface_policy_not_preserved",
                "condition_type": "policy_blocker",
                "evidence": "Runtime contract summary no longer reports preserved summary, comparison rows, detector metrics, threshold behavior, and comparability policy.",
            }
        )

    if reconciliation_status == "not_comparable":
        blocking_conditions.append(
            {
                "condition_code": reason_code,
                "condition_type": "semantic_non_equivalence",
                "evidence": reason,
            }
        )
        return _assessment_record(
            surface_id=surface_id,
            readiness_state="not-comparable",
            reasoning="Package 1C already established explicit semantic non-equivalence for this surface.",
            blocking_conditions=blocking_conditions,
            reconciliation_record=surface,
            authoritative_support=authoritative_support,
        )

    if reconciliation_status == "aligned":
        if blocking_conditions:
            return _assessment_record(
                surface_id=surface_id,
                readiness_state="migration-blocked",
                reasoning="The surface reconciles directly, but guardrail or legacy-policy blockers still prevent migration-ready status.",
                blocking_conditions=blocking_conditions,
                reconciliation_record=surface,
                authoritative_support=authoritative_support,
            )

        return _assessment_record(
            surface_id=surface_id,
            readiness_state="migration-ready",
            reasoning="The authoritative and legacy surfaces reconcile directly, and no active guardrail or policy blocker is visible in the current artifacts.",
            blocking_conditions=[],
            reconciliation_record=surface,
            authoritative_support=authoritative_support,
        )

    if reconciliation_status in {"requires_future_migration", "unavailable"}:
        if reason_code == "authoritative_family_a_subtype_surface_incomplete":
            blocking_conditions.append(
                {
                    "condition_code": reason_code,
                    "condition_type": "authoritative_evidence_blocker",
                    "evidence": {
                        "missing_evidence_row_ids": authoritative_support.get("missing_evidence_row_ids", []),
                        "reason": reason,
                    },
                }
            )
            return _assessment_record(
                surface_id=surface_id,
                readiness_state="migration-blocked",
                reasoning="Current authoritative scorer evidence explicitly preserves missing subtype evidence, so migration readiness is blocked rather than merely unknown.",
                blocking_conditions=blocking_conditions,
                reconciliation_record=surface,
                authoritative_support=authoritative_support,
            )

        if reason_code in {
            "read_file_rows_missing_family_a_records",
            "authoritative_symbol_membership_incomplete",
            "direct_stage_c_rate_differs_from_legacy_rate",
            "authoritative_direct_answer_count_differs_from_legacy_count",
            "authoritative_symbol_surface_differs_from_legacy_surface",
        }:
            blocking_conditions.append(
                {
                    "condition_code": reason_code,
                    "condition_type": "migration_blocker",
                    "evidence": reason,
                }
            )
            return _assessment_record(
                surface_id=surface_id,
                readiness_state="migration-blocked",
                reasoning="The surface is conceptually comparable, but Package 1C exposes an explicit blocker preventing migration-ready status.",
                blocking_conditions=blocking_conditions,
                reconciliation_record=surface,
                authoritative_support=authoritative_support,
            )

        if reason_code in {
            "authoritative_declared_symbol_membership_unavailable",
        }:
            blocking_conditions.append(
                {
                    "condition_code": reason_code,
                    "condition_type": "insufficient_authoritative_evidence",
                    "evidence": {
                        "declared_symbol_membership_row_ids": authoritative_support.get("declared_symbol_membership_row_ids", []),
                        "reason": reason,
                    },
                }
            )
            return _assessment_record(
                surface_id=surface_id,
                readiness_state="insufficient-evidence",
                reasoning="Current authoritative artifacts do not yet expose enough governed evidence to classify the surface as ready or explicitly blocked.",
                blocking_conditions=blocking_conditions,
                reconciliation_record=surface,
                authoritative_support=authoritative_support,
            )

        blocking_conditions.append(
            {
                "condition_code": reason_code,
                "condition_type": "insufficient_evidence",
                "evidence": reason,
            }
        )
        return _assessment_record(
            surface_id=surface_id,
            readiness_state="insufficient-evidence",
            reasoning="Package 1C indicates future migration is required, but the current artifact set does not provide enough evidence to classify the surface more strongly.",
            blocking_conditions=blocking_conditions,
            reconciliation_record=surface,
            authoritative_support=authoritative_support,
        )

    blocking_conditions.append(
        {
            "condition_code": "unknown_reconciliation_status",
            "condition_type": "insufficient_evidence",
            "evidence": reconciliation_status,
        }
    )
    return _assessment_record(
        surface_id=surface_id,
        readiness_state="insufficient-evidence",
        reasoning="The reconciliation record does not expose a recognized status for readiness assessment.",
        blocking_conditions=blocking_conditions,
        reconciliation_record=surface,
        authoritative_support=authoritative_support,
    )


def _build_readiness_report(
    *,
    run_dir: Path,
    side: str,
    row_fact_artifact: Mapping[str, Any],
    family_a_artifact: Mapping[str, Any],
    guardrails_artifact: Mapping[str, Any],
    runtime_summary_artifact: Mapping[str, Any],
    reconciliation_report: Mapping[str, Any],
) -> dict[str, Any]:
    family_a_records = _require_side_records(family_a_artifact, side)
    reconciled_surfaces = _as_records(reconciliation_report, "reconciled_surfaces")
    guardrails_clear = _guardrails_clear(guardrails_artifact)
    legacy_policy_preserved = _legacy_policy_preserved(runtime_summary_artifact)

    assessments = [
        _assess_surface(
            surface=surface,
            row_fact_artifact=row_fact_artifact,
            family_a_records=family_a_records,
            guardrails_clear=guardrails_clear,
            legacy_policy_preserved=legacy_policy_preserved,
        )
        for surface in reconciled_surfaces
    ]

    readiness_counts: dict[str, int] = {}
    for assessment in assessments:
        state = str(assessment.get("readiness_state"))
        readiness_counts[state] = readiness_counts.get(state, 0) + 1

    return {
        "assessment_scope": "stage_c_package1d_migration_readiness_assessment",
        "assessment_question": (
            "For the active compatibility-bearing legacy surfaces, which surfaces are migration-ready, which remain "
            "blocked by explicit authoritative evidence, which are not comparable, and which lack enough evidence "
            "for a readiness determination?"
        ),
        "readiness_taxonomy": _taxonomy(),
        "assessment_boundaries": {
            "reads_stage_c_authoritative_artifacts": True,
            "reads_package1c_reconciliation_artifact": True,
            "reads_detector_outputs_directly": False,
            "reads_threshold_outputs_directly": False,
            "performs_reconstruction": False,
            "performs_detector_projection": False,
            "performs_threshold_projection": False,
            "creates_replacement_metrics": False,
            "authorizes_migration": False,
        },
        "input_artifacts": {
            "row_fact_metadata": str(run_dir / STAGE_C_ROW_FACT_ARTIFACT_NAME),
            "family_a_scorer_evidence": str(run_dir / STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME),
            "governance_guardrails": str(run_dir / STAGE_C_GOVERNANCE_GUARDRAILS_ARTIFACT_NAME),
            "runtime_contract_summary": str(run_dir / STAGE_C_RUNTIME_CONTRACT_SUMMARY_ARTIFACT_NAME),
            "package1c_reconciliation_report": str(run_dir / STAGE_C_PACKAGE1C_RECONCILIATION_REPORT_NAME),
        },
        "guardrail_status": dict(sorted((guardrails_artifact.get("guardrail_status") or {}).items())),
        "legacy_surface_policy": dict(sorted((runtime_summary_artifact.get("legacy_surface_policy") or {}).items())),
        "compatibility_surface_assessments": assessments,
        "readiness_counts": dict(sorted(readiness_counts.items())),
        "integrity_checks": {
            "row_id_uniqueness_preserved": _row_id_uniqueness(row_fact_artifact),
            "family_a_rows_resolve_to_row_facts": _family_a_rows_resolve(row_fact_artifact, family_a_records),
            "guardrails_clear": guardrails_clear,
            "legacy_surface_policy_preserved": legacy_policy_preserved,
            "package1c_surface_count_matches": len(reconciled_surfaces) == 4,
        },
    }


def run_stage_c_package1d_migration_readiness_assessment(
    *,
    run_dir: Path,
    side: str = "base",
    output_path: Path | None = None,
) -> dict[str, Any]:
    run_dir = run_dir.resolve()
    row_fact_artifact = _load_json(run_dir / STAGE_C_ROW_FACT_ARTIFACT_NAME)
    family_a_artifact = _load_json(run_dir / STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME)
    guardrails_artifact = _load_json(run_dir / STAGE_C_GOVERNANCE_GUARDRAILS_ARTIFACT_NAME)
    runtime_summary_artifact = _load_json(run_dir / STAGE_C_RUNTIME_CONTRACT_SUMMARY_ARTIFACT_NAME)
    reconciliation_report = _load_json(run_dir / STAGE_C_PACKAGE1C_RECONCILIATION_REPORT_NAME)

    report = _build_readiness_report(
        run_dir=run_dir,
        side=side,
        row_fact_artifact=row_fact_artifact,
        family_a_artifact=family_a_artifact,
        guardrails_artifact=guardrails_artifact,
        runtime_summary_artifact=runtime_summary_artifact,
        reconciliation_report=reconciliation_report,
    )

    resolved_output_path = (output_path or (run_dir / STAGE_C_PACKAGE1D_READINESS_REPORT_NAME)).resolve()
    _write_json(resolved_output_path, report)

    return {
        "report_path": str(resolved_output_path),
        "assessment_scope": report["assessment_scope"],
        "analyzed_side": side,
        "surface_count": len(report["compatibility_surface_assessments"]),
        "readiness_counts": report["readiness_counts"],
        "guardrails_clear": report["integrity_checks"]["guardrails_clear"],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Migration-readiness assessment over Stage C authoritative artifacts and Package 1C reconciliation output.")
    parser.add_argument("--run-dir", required=True, help="Directory containing Stage C authoritative artifacts and the Package 1C reconciliation artifact")
    parser.add_argument("--side", default="base", help="Family A side to analyze (default: base)")
    parser.add_argument("--output-path", default=None, help="Optional output path for the readiness assessment artifact")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = run_stage_c_package1d_migration_readiness_assessment(
        run_dir=Path(args.run_dir),
        side=str(args.side),
        output_path=Path(args.output_path).resolve() if args.output_path else None,
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
