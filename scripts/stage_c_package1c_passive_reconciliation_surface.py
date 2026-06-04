#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping


SUMMARY_ARTIFACT_NAME = "summary.json"
STAGE_C_ROW_FACT_ARTIFACT_NAME = "stage_c_row_fact_metadata_artifact.json"
STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME = "stage_c_family_a_scorer_evidence_artifact.json"
STAGE_C_GOVERNANCE_GUARDRAILS_ARTIFACT_NAME = "stage_c_governance_guardrails_artifact.json"
STAGE_C_RUNTIME_CONTRACT_SUMMARY_ARTIFACT_NAME = "stage_c_runtime_contract_summary_artifact.json"
STAGE_C_PACKAGE1C_RECONCILIATION_REPORT_NAME = "stage_c_package1c_passive_reconciliation_report.json"


class PassiveReconciliationError(RuntimeError):
    """Raised when the Package 1C passive reconciliation surface cannot proceed."""


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PassiveReconciliationError(f"required artifact missing: {path}") from exc
    except Exception as exc:
        raise PassiveReconciliationError(f"invalid JSON artifact {path}: {exc}") from exc


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
        raise PassiveReconciliationError(f"{field_name} must be a list")
    out: list[dict[str, Any]] = []
    for idx, record in enumerate(records):
        if not isinstance(record, dict):
            raise PassiveReconciliationError(f"{field_name}[{idx}] must be an object")
        out.append(record)
    return out


def _require_side_records(family_a_artifact: Mapping[str, Any], side: str) -> list[dict[str, Any]]:
    sides = family_a_artifact.get("sides")
    if not isinstance(sides, Mapping):
        raise PassiveReconciliationError("family_a_scorer_evidence.sides must be an object")
    side_payload = sides.get(side)
    if not isinstance(side_payload, Mapping):
        raise PassiveReconciliationError(f"family_a_scorer_evidence missing side '{side}'")
    return _as_records(side_payload, "records")


def _sorted_row_ids(row_ids: list[str]) -> list[str]:
    return sorted(str(row_id) for row_id in row_ids)


def _legacy_metric_value(summary: Mapping[str, Any], path: tuple[str, ...]) -> Any:
    cursor: Any = summary
    for key in path:
        if not isinstance(cursor, Mapping) or key not in cursor:
            return None
        cursor = cursor[key]
    return cursor


def _float_equal(left: Any, right: Any, tolerance: float = 1e-12) -> bool:
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return abs(float(left) - float(right)) <= tolerance
    return left == right


def _surface_record(
    *,
    surface_id: str,
    authoritative_source: Mapping[str, Any],
    legacy_source: Mapping[str, Any],
    ownership_authority: Mapping[str, str],
    reconciliation_status: str,
    reason_code: str,
    reason: str,
) -> dict[str, Any]:
    return {
        "surface_id": surface_id,
        "authoritative_source": dict(authoritative_source),
        "legacy_source": dict(legacy_source),
        "ownership_authority": dict(ownership_authority),
        "reconciliation_status": reconciliation_status,
        "reason_code": reason_code,
        "reason": reason,
    }


def _build_read_file_exact_valid_surface(
    *,
    run_dir: Path,
    row_fact_records: list[dict[str, Any]],
    family_a_by_id: dict[str, dict[str, Any]],
    summary: Mapping[str, Any],
) -> dict[str, Any]:
    read_file_row_ids = _sorted_row_ids(
        [
            str(record.get("row_id"))
            for record in row_fact_records
            if _as_bool((record.get("membership_markers") or {}).get("family_b1_read_file_eligible")) is True
        ]
    )
    missing_family_a_row_ids = _sorted_row_ids([row_id for row_id in read_file_row_ids if row_id not in family_a_by_id])

    exact_valid_count = sum(
        1
        for row_id in read_file_row_ids
        if _as_bool((family_a_by_id.get(row_id) or {}).get("exact_valid")) is True
    )
    authoritative_rows = len(read_file_row_ids)
    authoritative_rate = float(exact_valid_count) / float(authoritative_rows) if authoritative_rows else None

    legacy_rows = _legacy_metric_value(summary, ("failure_profile", "read_file_exact_valid", "rows"))
    legacy_count = _legacy_metric_value(summary, ("failure_profile", "read_file_exact_valid", "count"))
    legacy_rate = _legacy_metric_value(summary, ("failure_profile", "read_file_exact_valid", "rate"))

    authoritative_source = {
        "artifact_paths": [
            str(run_dir / STAGE_C_ROW_FACT_ARTIFACT_NAME),
            str(run_dir / STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME),
        ],
        "consumption_paths": [
            "records[].membership_markers.family_b1_read_file_eligible == true",
            "sides.base.records[].exact_valid joined by row_id",
        ],
        "source_state": "available" if not missing_family_a_row_ids else "requires_future_migration",
        "value": {
            "rows": authoritative_rows,
            "count": exact_valid_count,
            "rate": authoritative_rate,
            "row_ids": read_file_row_ids,
            "missing_family_a_row_ids": missing_family_a_row_ids,
        },
    }
    legacy_source = {
        "artifact_path": str(run_dir / SUMMARY_ARTIFACT_NAME),
        "consumption_path": "failure_profile.read_file_exact_valid",
        "value": {
            "rows": legacy_rows,
            "count": legacy_count,
            "rate": legacy_rate,
        },
    }

    if missing_family_a_row_ids:
        return _surface_record(
            surface_id="read_file_exact_valid_rate",
            authoritative_source=authoritative_source,
            legacy_source=legacy_source,
            ownership_authority={
                "authoritative": "dataset metadata + scorer consumed by evaluator",
                "legacy": "legacy evaluator failure_profile",
            },
            reconciliation_status="requires_future_migration",
            reason_code="read_file_rows_missing_family_a_records",
            reason="Authoritative read-file eligibility rows are missing scorer evidence rows, so the direct rate comparison is incomplete.",
        )

    if (
        authoritative_rows == legacy_rows
        and exact_valid_count == legacy_count
        and _float_equal(authoritative_rate, legacy_rate)
    ):
        return _surface_record(
            surface_id="read_file_exact_valid_rate",
            authoritative_source=authoritative_source,
            legacy_source=legacy_source,
            ownership_authority={
                "authoritative": "dataset metadata + scorer consumed by evaluator",
                "legacy": "legacy evaluator failure_profile",
            },
            reconciliation_status="aligned",
            reason_code="direct_stage_c_rate_matches_legacy_rate",
            reason="Authoritative read-file eligibility and exact-valid scorer facts reconcile exactly with the legacy read-file exact-valid surface.",
        )

    return _surface_record(
        surface_id="read_file_exact_valid_rate",
        authoritative_source=authoritative_source,
        legacy_source=legacy_source,
        ownership_authority={
            "authoritative": "dataset metadata + scorer consumed by evaluator",
            "legacy": "legacy evaluator failure_profile",
        },
        reconciliation_status="requires_future_migration",
        reason_code="direct_stage_c_rate_differs_from_legacy_rate",
        reason="Authoritative read-file exact-valid facts are directly consumable, but the current legacy surface does not reconcile exactly in this run.",
    )


def _build_symbol_name_surface(
    *,
    run_dir: Path,
    row_fact_records: list[dict[str, Any]],
    family_a_by_id: dict[str, dict[str, Any]],
    summary: Mapping[str, Any],
) -> dict[str, Any]:
    declared_symbol_row_ids = _sorted_row_ids(
        [
            str(record.get("row_id"))
            for record in row_fact_records
            if (record.get("membership_markers") or {}).get("family_b1_symbol_name_member") is True
        ]
    )
    missing_owner_row_ids = _sorted_row_ids(
        [
            str(record.get("row_id"))
            for record in row_fact_records
            if (record.get("membership_markers") or {}).get("family_b1_symbol_name_member") is True
            and _as_nonempty_str((record.get("ownership_markers") or {}).get("symbol_name_membership_owner")) is None
        ]
    )
    missing_family_a_row_ids = _sorted_row_ids([row_id for row_id in declared_symbol_row_ids if row_id not in family_a_by_id])
    exact_valid_count = sum(
        1
        for row_id in declared_symbol_row_ids
        if _as_bool((family_a_by_id.get(row_id) or {}).get("exact_valid")) is True
    )
    authoritative_rows = len(declared_symbol_row_ids)
    authoritative_rate = float(exact_valid_count) / float(authoritative_rows) if authoritative_rows else None

    legacy_rows = _legacy_metric_value(summary, ("failure_profile", "read_file_symbol_name_exact_valid", "rows"))
    legacy_count = _legacy_metric_value(summary, ("failure_profile", "read_file_symbol_name_exact_valid", "count"))
    legacy_rate = _legacy_metric_value(summary, ("failure_profile", "read_file_symbol_name_exact_valid", "rate"))

    authoritative_source = {
        "artifact_paths": [
            str(run_dir / STAGE_C_ROW_FACT_ARTIFACT_NAME),
            str(run_dir / STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME),
        ],
        "consumption_paths": [
            "records[].membership_markers.family_b1_symbol_name_member == true",
            "records[].ownership_markers.symbol_name_membership_owner",
            "sides.base.records[].exact_valid joined by row_id",
        ],
        "source_state": "available" if authoritative_rows > 0 and not missing_family_a_row_ids else "unavailable",
        "value": {
            "rows": authoritative_rows,
            "count": exact_valid_count,
            "rate": authoritative_rate,
            "declared_symbol_membership_row_ids": declared_symbol_row_ids,
            "missing_owner_row_ids": missing_owner_row_ids,
            "missing_family_a_row_ids": missing_family_a_row_ids,
        },
    }
    legacy_source = {
        "artifact_path": str(run_dir / SUMMARY_ARTIFACT_NAME),
        "consumption_path": "failure_profile.read_file_symbol_name_exact_valid",
        "value": {
            "rows": legacy_rows,
            "count": legacy_count,
            "rate": legacy_rate,
        },
    }

    if authoritative_rows == 0:
        return _surface_record(
            surface_id="read_file_symbol_name_exact_valid_rate",
            authoritative_source=authoritative_source,
            legacy_source=legacy_source,
            ownership_authority={
                "authoritative": "dataset metadata + scorer consumed by evaluator",
                "legacy": "legacy evaluator failure_profile",
            },
            reconciliation_status="requires_future_migration",
            reason_code="authoritative_declared_symbol_membership_unavailable",
            reason="Authoritative declared symbol-name membership rows are absent in the current run, while the legacy symbol-name surface remains populated.",
        )

    if missing_owner_row_ids or missing_family_a_row_ids:
        return _surface_record(
            surface_id="read_file_symbol_name_exact_valid_rate",
            authoritative_source=authoritative_source,
            legacy_source=legacy_source,
            ownership_authority={
                "authoritative": "dataset metadata + scorer consumed by evaluator",
                "legacy": "legacy evaluator failure_profile",
            },
            reconciliation_status="requires_future_migration",
            reason_code="authoritative_symbol_membership_incomplete",
            reason="Authoritative symbol-name governed rows exist but ownership or scorer linkage remains incomplete.",
        )

    if (
        authoritative_rows == legacy_rows
        and exact_valid_count == legacy_count
        and _float_equal(authoritative_rate, legacy_rate)
    ):
        return _surface_record(
            surface_id="read_file_symbol_name_exact_valid_rate",
            authoritative_source=authoritative_source,
            legacy_source=legacy_source,
            ownership_authority={
                "authoritative": "dataset metadata + scorer consumed by evaluator",
                "legacy": "legacy evaluator failure_profile",
            },
            reconciliation_status="aligned",
            reason_code="direct_stage_c_symbol_rate_matches_legacy_rate",
            reason="Authoritative declared symbol-name membership and scorer exact-valid facts reconcile exactly with the legacy symbol-name surface.",
        )

    return _surface_record(
        surface_id="read_file_symbol_name_exact_valid_rate",
        authoritative_source=authoritative_source,
        legacy_source=legacy_source,
        ownership_authority={
            "authoritative": "dataset metadata + scorer consumed by evaluator",
            "legacy": "legacy evaluator failure_profile",
        },
        reconciliation_status="requires_future_migration",
        reason_code="authoritative_symbol_surface_differs_from_legacy_surface",
        reason="Authoritative declared symbol-name surface is available, but it does not reconcile exactly with the legacy symbol-name surface in this run.",
    )


def _build_no_anchor_surface(
    *,
    run_dir: Path,
    row_fact_records: list[dict[str, Any]],
    summary: Mapping[str, Any],
) -> dict[str, Any]:
    declared_anchor_row_ids = _sorted_row_ids(
        [
            str(record.get("row_id"))
            for record in row_fact_records
            if _as_bool((record.get("membership_markers") or {}).get("family_b2_anchor_eligible")) is True
        ]
    )
    declared_no_anchor_row_ids = _sorted_row_ids(
        [
            str(record.get("row_id"))
            for record in row_fact_records
            if _as_bool((record.get("membership_markers") or {}).get("family_b2_no_anchor_member")) is True
        ]
    )

    legacy_value = _legacy_metric_value(summary, ("failure_profile", "anchor_exact_share", "no_anchor_phrase"))

    authoritative_source = {
        "artifact_paths": [str(run_dir / STAGE_C_ROW_FACT_ARTIFACT_NAME)],
        "consumption_paths": [
            "records[].membership_markers.family_b2_anchor_eligible == true",
            "records[].membership_markers.family_b2_no_anchor_member == true",
        ],
        "source_state": "unavailable",
        "value": {
            "declared_anchor_row_count": len(declared_anchor_row_ids),
            "declared_no_anchor_row_count": len(declared_no_anchor_row_ids),
            "declared_anchor_row_ids": declared_anchor_row_ids,
            "declared_no_anchor_row_ids": declared_no_anchor_row_ids,
        },
    }
    legacy_source = {
        "artifact_path": str(run_dir / SUMMARY_ARTIFACT_NAME),
        "consumption_path": "failure_profile.anchor_exact_share.no_anchor_phrase",
        "value": legacy_value,
    }

    return _surface_record(
        surface_id="no_anchor_exact_valid_share",
        authoritative_source=authoritative_source,
        legacy_source=legacy_source,
        ownership_authority={
            "authoritative": "dataset metadata ownership of B2 anchor markers consumed by evaluator",
            "legacy": "legacy evaluator failure_profile",
        },
        reconciliation_status="not_comparable",
        reason_code="legacy_no_anchor_share_semantic_mismatch",
        reason="The legacy no-anchor share is a historical share-of-successes surface and is not a comparable authoritative Stage C governed metric in the current artifact set.",
    )


def _build_direct_answer_surface(
    *,
    run_dir: Path,
    family_a_records: list[dict[str, Any]],
    summary: Mapping[str, Any],
) -> dict[str, Any]:
    non_exact_tool_expected_rows = [
        record
        for record in family_a_records
        if _as_bool(record.get("non_exact_tool_expected")) is True
    ]
    direct_answer_row_ids = _sorted_row_ids(
        [
            str(record.get("row_id"))
            for record in non_exact_tool_expected_rows
            if _as_nonempty_str(record.get("subtype_assignment")) == "direct-answer substitution"
        ]
    )
    missing_evidence_row_ids = _sorted_row_ids(
        [
            str(record.get("row_id"))
            for record in non_exact_tool_expected_rows
            if _as_bool(record.get("missing_evidence")) is True
        ]
    )

    legacy_value = _legacy_metric_value(
        summary,
        ("failure_profile", "failure_categories_non_exact_tool_rows", "direct_answer_substitution"),
    )

    authoritative_source = {
        "artifact_paths": [str(run_dir / STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME)],
        "consumption_paths": [
            "sides.base.records[].subtype_assignment == 'direct-answer substitution'",
            "sides.base.records[].missing_evidence == true",
        ],
        "source_state": "available" if not missing_evidence_row_ids else "requires_future_migration",
        "value": {
            "direct_answer_substitution_count": len(direct_answer_row_ids),
            "direct_answer_row_ids": direct_answer_row_ids,
            "non_exact_tool_expected_row_count": len(non_exact_tool_expected_rows),
            "missing_evidence_row_ids": missing_evidence_row_ids,
        },
    }
    legacy_source = {
        "artifact_path": str(run_dir / SUMMARY_ARTIFACT_NAME),
        "consumption_path": "failure_profile.failure_categories_non_exact_tool_rows.direct_answer_substitution",
        "value": legacy_value,
    }

    if missing_evidence_row_ids:
        return _surface_record(
            surface_id="direct_answer_substitution_count",
            authoritative_source=authoritative_source,
            legacy_source=legacy_source,
            ownership_authority={
                "authoritative": "scorer consumed by evaluator",
                "legacy": "legacy evaluator failure_profile",
            },
            reconciliation_status="requires_future_migration",
            reason_code="authoritative_family_a_subtype_surface_incomplete",
            reason="Authoritative Family A subtype evidence still contains explicit missing-evidence rows, so direct-answer count alignment cannot yet be treated as migration-ready.",
        )

    if len(direct_answer_row_ids) == legacy_value:
        return _surface_record(
            surface_id="direct_answer_substitution_count",
            authoritative_source=authoritative_source,
            legacy_source=legacy_source,
            ownership_authority={
                "authoritative": "scorer consumed by evaluator",
                "legacy": "legacy evaluator failure_profile",
            },
            reconciliation_status="aligned",
            reason_code="direct_stage_c_subtype_count_matches_legacy_count",
            reason="Authoritative direct-answer subtype rows reconcile exactly with the legacy direct-answer count surface.",
        )

    return _surface_record(
        surface_id="direct_answer_substitution_count",
        authoritative_source=authoritative_source,
        legacy_source=legacy_source,
        ownership_authority={
            "authoritative": "scorer consumed by evaluator",
            "legacy": "legacy evaluator failure_profile",
        },
        reconciliation_status="requires_future_migration",
        reason_code="authoritative_direct_answer_count_differs_from_legacy_count",
        reason="Authoritative direct-answer subtype rows are directly consumable, but the current legacy direct-answer count does not reconcile exactly in this run.",
    )


def _build_reconciliation_report(
    *,
    run_dir: Path,
    side: str,
    row_fact_artifact: Mapping[str, Any],
    family_a_artifact: Mapping[str, Any],
    guardrail_artifact: Mapping[str, Any],
    runtime_summary_artifact: Mapping[str, Any],
    summary: Mapping[str, Any],
) -> dict[str, Any]:
    row_fact_records = _as_records(row_fact_artifact, "records")
    family_a_records = _require_side_records(family_a_artifact, side)
    family_a_by_id = {
        str(record.get("row_id")): record
        for record in family_a_records
    }
    row_ids = [str(record.get("row_id")) for record in row_fact_records]

    surfaces = [
        _build_read_file_exact_valid_surface(
            run_dir=run_dir,
            row_fact_records=row_fact_records,
            family_a_by_id=family_a_by_id,
            summary=summary,
        ),
        _build_symbol_name_surface(
            run_dir=run_dir,
            row_fact_records=row_fact_records,
            family_a_by_id=family_a_by_id,
            summary=summary,
        ),
        _build_no_anchor_surface(
            run_dir=run_dir,
            row_fact_records=row_fact_records,
            summary=summary,
        ),
        _build_direct_answer_surface(
            run_dir=run_dir,
            family_a_records=family_a_records,
            summary=summary,
        ),
    ]

    guardrail_status = dict(sorted((guardrail_artifact.get("guardrail_status") or {}).items()))
    legacy_surface_policy = dict(sorted((runtime_summary_artifact.get("legacy_surface_policy") or {}).items()))
    row_id_uniqueness_preserved = len(set(row_ids)) == len(row_fact_records)
    family_a_rows_resolve = all(str(record.get("row_id")) in set(row_ids) for record in family_a_records)

    return {
        "consumer_scope": "stage_c_package1c_passive_reconciliation_surface",
        "reconciliation_question": (
            "For the active legacy compatibility-bearing surfaces, which legacy outputs already reconcile directly "
            "with authoritative Stage C facts, and which remain unavailable or non-comparable without migration?"
        ),
        "selection_rationale": [
            "The four active compatibility-bearing legacy surfaces are already explicitly defined in the live threshold profile.",
            "These surfaces provide the narrowest useful authoritative-to-legacy reconciliation slice without detector or threshold migration.",
            "The surface is governance-relevant because it exposes which legacy metrics already have direct authoritative backing and which still depend on blocked semantics or incomplete subtype coverage.",
        ],
        "consumer_boundaries": {
            "reads_authoritative_stage_c_artifacts_only_for_authoritative_side": True,
            "reads_legacy_summary_only_for_legacy_side": True,
            "modifies_detector_inputs": False,
            "modifies_threshold_inputs": False,
            "modifies_legacy_summary": False,
            "creates_authoritative_replacement_metrics": False,
            "performs_detector_projection": False,
            "performs_threshold_projection": False,
        },
        "input_artifacts": {
            "legacy_summary": str(run_dir / SUMMARY_ARTIFACT_NAME),
            "row_fact_metadata": str(run_dir / STAGE_C_ROW_FACT_ARTIFACT_NAME),
            "family_a_scorer_evidence": str(run_dir / STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME),
            "governance_guardrails": str(run_dir / STAGE_C_GOVERNANCE_GUARDRAILS_ARTIFACT_NAME),
            "runtime_contract_summary": str(run_dir / STAGE_C_RUNTIME_CONTRACT_SUMMARY_ARTIFACT_NAME),
        },
        "legacy_surface_policy": legacy_surface_policy,
        "guardrail_status": guardrail_status,
        "reconciled_surfaces": surfaces,
        "integrity_checks": {
            "row_id_uniqueness_preserved": row_id_uniqueness_preserved,
            "family_a_rows_resolve_to_row_facts": family_a_rows_resolve,
            "guardrails_clear": not any(bool(value) for value in guardrail_status.values()),
            "legacy_surface_policy_preserved": legacy_surface_policy
            == {
                "comparability_policy": "unchanged",
                "comparison_rows_jsonl": "preserved",
                "detector_metrics": "unchanged",
                "summary_json": "preserved",
                "threshold_behavior": "unchanged",
            },
        },
    }


def run_stage_c_package1c_passive_reconciliation_surface(
    *,
    run_dir: Path,
    side: str = "base",
    output_path: Path | None = None,
) -> dict[str, Any]:
    run_dir = run_dir.resolve()
    summary = _load_json(run_dir / SUMMARY_ARTIFACT_NAME)
    row_fact_artifact = _load_json(run_dir / STAGE_C_ROW_FACT_ARTIFACT_NAME)
    family_a_artifact = _load_json(run_dir / STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME)
    guardrail_artifact = _load_json(run_dir / STAGE_C_GOVERNANCE_GUARDRAILS_ARTIFACT_NAME)
    runtime_summary_artifact = _load_json(run_dir / STAGE_C_RUNTIME_CONTRACT_SUMMARY_ARTIFACT_NAME)

    report = _build_reconciliation_report(
        run_dir=run_dir,
        side=side,
        row_fact_artifact=row_fact_artifact,
        family_a_artifact=family_a_artifact,
        guardrail_artifact=guardrail_artifact,
        runtime_summary_artifact=runtime_summary_artifact,
        summary=summary,
    )

    resolved_output_path = (output_path or (run_dir / STAGE_C_PACKAGE1C_RECONCILIATION_REPORT_NAME)).resolve()
    _write_json(resolved_output_path, report)

    status_counts: dict[str, int] = {}
    for row in report["reconciled_surfaces"]:
        status = str(row.get("reconciliation_status"))
        status_counts[status] = status_counts.get(status, 0) + 1

    return {
        "report_path": str(resolved_output_path),
        "consumer_scope": report["consumer_scope"],
        "analyzed_side": side,
        "surface_count": len(report["reconciled_surfaces"]),
        "status_counts": dict(sorted(status_counts.items())),
        "guardrails_clear": report["integrity_checks"]["guardrails_clear"],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Passive reconciliation surface over authoritative Stage C artifacts and legacy summary outputs.")
    parser.add_argument("--run-dir", required=True, help="Directory containing legacy summary and emitted Stage C artifacts")
    parser.add_argument("--side", default="base", help="Family A side to analyze (default: base)")
    parser.add_argument("--output-path", default=None, help="Optional output path for the reconciliation report")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = run_stage_c_package1c_passive_reconciliation_surface(
        run_dir=Path(args.run_dir),
        side=str(args.side),
        output_path=Path(args.output_path).resolve() if args.output_path else None,
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
