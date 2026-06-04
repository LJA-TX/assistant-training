#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Mapping


STAGE_C_ROW_FACT_ARTIFACT_NAME = "stage_c_row_fact_metadata_artifact.json"
STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME = "stage_c_family_a_scorer_evidence_artifact.json"
STAGE_C_GOVERNANCE_GUARDRAILS_ARTIFACT_NAME = "stage_c_governance_guardrails_artifact.json"
STAGE_C_RUNTIME_CONTRACT_SUMMARY_ARTIFACT_NAME = "stage_c_runtime_contract_summary_artifact.json"

STAGE_C_PACKAGE1B_GOVERNANCE_REPORT_NAME = "stage_c_package1b_passive_governance_report.json"


class PassiveGovernanceConsumerError(RuntimeError):
    """Raised when the Package 1B passive governance consumer cannot proceed."""


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PassiveGovernanceConsumerError(f"required artifact missing: {path}") from exc
    except Exception as exc:
        raise PassiveGovernanceConsumerError(f"invalid JSON artifact {path}: {exc}") from exc


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
        raise PassiveGovernanceConsumerError(f"{field_name} must be a list")
    out: list[dict[str, Any]] = []
    for idx, record in enumerate(records):
        if not isinstance(record, dict):
            raise PassiveGovernanceConsumerError(f"{field_name}[{idx}] must be an object")
        out.append(record)
    return out


def _require_side_records(family_a_artifact: Mapping[str, Any], side: str) -> list[dict[str, Any]]:
    sides = family_a_artifact.get("sides")
    if not isinstance(sides, Mapping):
        raise PassiveGovernanceConsumerError("family_a_scorer_evidence.sides must be an object")
    side_payload = sides.get(side)
    if not isinstance(side_payload, Mapping):
        raise PassiveGovernanceConsumerError(f"family_a_scorer_evidence missing side '{side}'")
    return _as_records(side_payload, "records")


def _family_a_tool_expected_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [record for record in records if _as_bool(record.get("tool_expected_eligibility")) is True]


def _family_a_non_exact_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [record for record in records if _as_bool(record.get("non_exact_tool_expected")) is True]


def _sorted_counter(counter: Counter[str]) -> dict[str, int]:
    return {key: int(counter[key]) for key in sorted(counter)}


def _value_entry(
    *,
    value: Any,
    origin_artifact: str,
    owning_authority: str,
    consumption_path: str,
) -> dict[str, Any]:
    return {
        "value": value,
        "origin_artifact": origin_artifact,
        "owning_authority": owning_authority,
        "consumption_path": consumption_path,
    }


def _anchor_declared(record: Mapping[str, Any]) -> bool:
    membership = record.get("membership_markers")
    if not isinstance(membership, Mapping):
        return False
    anchor_eligible = _as_bool(membership.get("family_b2_anchor_eligible"))
    no_anchor_member = _as_bool(membership.get("family_b2_no_anchor_member"))
    anchor_category = _as_nonempty_str(membership.get("family_b2_anchor_category"))
    return bool(anchor_eligible is True or no_anchor_member is not None or anchor_category is not None)


def _build_passive_governance_report(
    *,
    run_dir: Path,
    side: str,
    row_fact_artifact: Mapping[str, Any],
    family_a_artifact: Mapping[str, Any],
    guardrail_artifact: Mapping[str, Any],
    runtime_summary_artifact: Mapping[str, Any],
) -> dict[str, Any]:
    row_fact_records = _as_records(row_fact_artifact, "records")
    family_a_records = _require_side_records(family_a_artifact, side)

    row_fact_by_id = {
        str(record.get("row_id")): record
        for record in row_fact_records
    }
    row_ids = sorted(row_fact_by_id.keys())
    family_a_by_id = {
        str(record.get("row_id")): record
        for record in family_a_records
    }
    family_a_row_ids = sorted(family_a_by_id.keys())

    tool_expected_row_ids = sorted(
        str(record.get("row_id"))
        for record in row_fact_records
        if _as_bool((record.get("membership_markers") or {}).get("family_a_tool_expected_eligible")) is True
    )
    family_a_tool_expected = _family_a_tool_expected_records(family_a_records)
    family_a_non_exact = _family_a_non_exact_records(family_a_records)

    rows_with_missing_evidence = sorted(
        str(record.get("row_id"))
        for record in family_a_tool_expected
        if _as_bool(record.get("missing_evidence")) is True
    )
    missing_evidence_reason_counts = Counter(
        str(reason)
        for record in family_a_tool_expected
        if _as_bool(record.get("missing_evidence")) is True
        for reason in record.get("missing_evidence_reasons", [])
        if isinstance(reason, str) and reason.strip()
    )

    declared_symbol_membership_rows = []
    rows_with_missing_symbol_owner = []
    declared_anchor_rows = []
    rows_with_missing_anchor_assignment_owner = []
    rows_with_missing_anchor_taxonomy_owner = []
    rows_with_ownership_conflicts = []

    for record in row_fact_records:
        row_id = str(record.get("row_id"))
        membership = record.get("membership_markers") if isinstance(record.get("membership_markers"), Mapping) else {}
        ownership = record.get("ownership_markers") if isinstance(record.get("ownership_markers"), Mapping) else {}

        if membership.get("family_b1_symbol_name_member") is not None:
            declared_symbol_membership_rows.append(row_id)
            if _as_nonempty_str(ownership.get("symbol_name_membership_owner")) is None:
                rows_with_missing_symbol_owner.append(row_id)

        if _anchor_declared(record):
            declared_anchor_rows.append(row_id)
            if _as_nonempty_str(ownership.get("anchor_assignment_owner")) is None:
                rows_with_missing_anchor_assignment_owner.append(row_id)

            anchor_category = _as_nonempty_str(membership.get("family_b2_anchor_category"))
            if anchor_category is not None and _as_nonempty_str(ownership.get("anchor_taxonomy_owner")) is None:
                rows_with_missing_anchor_taxonomy_owner.append(row_id)

        if _as_bool(ownership.get("conflicting_ownership_markers")) is True:
            rows_with_ownership_conflicts.append(row_id)

    tool_expected_without_family_a = sorted(set(tool_expected_row_ids) - set(family_a_row_ids))
    family_a_without_row_fact = sorted(set(family_a_row_ids) - set(row_ids))
    guardrail_status = dict(sorted((guardrail_artifact.get("guardrail_status") or {}).items()))
    legacy_surface_policy = dict(sorted((runtime_summary_artifact.get("legacy_surface_policy") or {}).items()))

    reported_values = {
        "row_fact_record_count": _value_entry(
            value=int(row_fact_artifact.get("row_fact_count", len(row_fact_records))),
            origin_artifact=STAGE_C_ROW_FACT_ARTIFACT_NAME,
            owning_authority="evaluator emitted artifact summary",
            consumption_path="row_fact_count",
        ),
        "unique_row_id_count": _value_entry(
            value=len(set(row_ids)),
            origin_artifact=STAGE_C_ROW_FACT_ARTIFACT_NAME,
            owning_authority="dataset metadata row identity as emitted by evaluator",
            consumption_path="records[].row_id -> unique count",
        ),
        "family_a_tool_expected_population_count": _value_entry(
            value=len(tool_expected_row_ids),
            origin_artifact=STAGE_C_ROW_FACT_ARTIFACT_NAME,
            owning_authority="dataset metadata",
            consumption_path="records[].membership_markers.family_a_tool_expected_eligible == true",
        ),
        "family_a_exact_valid_tool_expected_count": _value_entry(
            value=sum(1 for record in family_a_tool_expected if _as_bool(record.get("exact_valid")) is True),
            origin_artifact=STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME,
            owning_authority="scorer",
            consumption_path=f"sides.{side}.records[] filtered by tool_expected_eligibility and exact_valid",
        ),
        "family_a_non_exact_tool_expected_count": _value_entry(
            value=len(family_a_non_exact),
            origin_artifact=STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME,
            owning_authority="scorer",
            consumption_path=f"sides.{side}.records[].non_exact_tool_expected == true",
        ),
        "family_a_subtype_assigned_count": _value_entry(
            value=sum(1 for record in family_a_non_exact if record.get("subtype_assignment") is not None),
            origin_artifact=STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME,
            owning_authority="scorer",
            consumption_path=f"sides.{side}.records[] non_exact rows with non-null subtype_assignment",
        ),
        "family_a_missing_evidence_count": _value_entry(
            value=len(rows_with_missing_evidence),
            origin_artifact=STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME,
            owning_authority="scorer",
            consumption_path=f"sides.{side}.records[] tool-expected rows with missing_evidence == true",
        ),
        "family_a_missing_evidence_reason_counts": _value_entry(
            value=_sorted_counter(missing_evidence_reason_counts),
            origin_artifact=STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME,
            owning_authority="scorer",
            consumption_path=f"sides.{side}.records[].missing_evidence_reasons aggregated over missing_evidence rows",
        ),
        "declared_symbol_membership_row_count": _value_entry(
            value=len(declared_symbol_membership_rows),
            origin_artifact=STAGE_C_ROW_FACT_ARTIFACT_NAME,
            owning_authority="dataset metadata",
            consumption_path="records[].membership_markers.family_b1_symbol_name_member != null",
        ),
        "declared_symbol_membership_rows_missing_owner_count": _value_entry(
            value=len(rows_with_missing_symbol_owner),
            origin_artifact=STAGE_C_ROW_FACT_ARTIFACT_NAME,
            owning_authority="dataset metadata",
            consumption_path=(
                "records[] where family_b1_symbol_name_member is declared and "
                "ownership_markers.symbol_name_membership_owner is null"
            ),
        ),
        "declared_anchor_row_count": _value_entry(
            value=len(declared_anchor_rows),
            origin_artifact=STAGE_C_ROW_FACT_ARTIFACT_NAME,
            owning_authority="dataset metadata",
            consumption_path="records[] with declared family_b2 anchor membership or category markers",
        ),
        "declared_anchor_rows_missing_assignment_owner_count": _value_entry(
            value=len(rows_with_missing_anchor_assignment_owner),
            origin_artifact=STAGE_C_ROW_FACT_ARTIFACT_NAME,
            owning_authority="dataset metadata",
            consumption_path=(
                "records[] with declared family_b2 anchor markers and "
                "ownership_markers.anchor_assignment_owner is null"
            ),
        ),
        "declared_anchor_rows_missing_taxonomy_owner_count": _value_entry(
            value=len(rows_with_missing_anchor_taxonomy_owner),
            origin_artifact=STAGE_C_ROW_FACT_ARTIFACT_NAME,
            owning_authority="dataset metadata",
            consumption_path=(
                "records[] with declared family_b2 anchor category and "
                "ownership_markers.anchor_taxonomy_owner is null"
            ),
        ),
        "ownership_conflict_row_count": _value_entry(
            value=len(rows_with_ownership_conflicts),
            origin_artifact=STAGE_C_ROW_FACT_ARTIFACT_NAME,
            owning_authority="dataset metadata",
            consumption_path="records[].ownership_markers.conflicting_ownership_markers == true",
        ),
        "guardrail_status": _value_entry(
            value=guardrail_status,
            origin_artifact=STAGE_C_GOVERNANCE_GUARDRAILS_ARTIFACT_NAME,
            owning_authority="evaluator governance guardrail surface",
            consumption_path="guardrail_status",
        ),
        "legacy_surface_policy": _value_entry(
            value=legacy_surface_policy,
            origin_artifact=STAGE_C_RUNTIME_CONTRACT_SUMMARY_ARTIFACT_NAME,
            owning_authority="evaluator runtime contract summary",
            consumption_path="legacy_surface_policy",
        ),
    }

    integrity_checks = {
        "row_id_uniqueness_preserved": len(set(row_ids)) == len(row_fact_records),
        "row_fact_count_matches_runtime_summary": int(row_fact_artifact.get("row_fact_count", 0))
        == int(runtime_summary_artifact.get("row_fact_count", -1)),
        "family_a_side_record_count_matches_runtime_summary": len(family_a_records)
        == int((runtime_summary_artifact.get("family_a_side_record_counts") or {}).get(side, -1)),
        "tool_expected_row_ids_have_family_a_records": not tool_expected_without_family_a,
        "family_a_row_ids_resolve_to_row_facts": not family_a_without_row_fact,
        "guardrails_clear": not any(bool(value) for value in guardrail_status.values()),
    }

    return {
        "consumer_scope": "stage_c_package1b_family_a_passive_governance_consumer",
        "governance_question": (
            "For the authoritative Family A tool-expected population, how much scorer evidence is directly "
            "consumable for governed subtype analysis, how much remains explicit missing evidence, and are any "
            "declared governed ownership markers absent or conflicting?"
        ),
        "selection_rationale": [
            "Family A tool-expected eligibility is already emitted in authoritative row-fact metadata.",
            "Family A subtype assignment and missing-evidence state are already emitted in authoritative scorer evidence.",
            "The question is governance-relevant and can be answered from Stage C artifacts only.",
            "No detector migration, threshold migration, or historical metric replacement is required.",
        ],
        "consumer_boundaries": {
            "reads_stage_c_artifacts_only": True,
            "modifies_detector_inputs": False,
            "modifies_threshold_inputs": False,
            "modifies_legacy_summary": False,
            "modifies_historical_metrics": False,
        },
        "input_artifacts": {
            "run_dir": str(run_dir),
            "row_fact_metadata": {
                "path": str(run_dir / STAGE_C_ROW_FACT_ARTIFACT_NAME),
                "record_count": len(row_fact_records),
            },
            "family_a_scorer_evidence": {
                "path": str(run_dir / STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME),
                "side": side,
                "record_count": len(family_a_records),
            },
            "governance_guardrails": {
                "path": str(run_dir / STAGE_C_GOVERNANCE_GUARDRAILS_ARTIFACT_NAME),
            },
            "runtime_contract_summary": {
                "path": str(run_dir / STAGE_C_RUNTIME_CONTRACT_SUMMARY_ARTIFACT_NAME),
            },
        },
        "reported_values": reported_values,
        "supporting_row_sets": {
            "tool_expected_row_ids_without_family_a_record": tool_expected_without_family_a,
            "family_a_record_row_ids_without_row_fact": family_a_without_row_fact,
            "rows_with_missing_evidence": rows_with_missing_evidence,
            "rows_with_missing_symbol_membership_owner": sorted(rows_with_missing_symbol_owner),
            "rows_with_missing_anchor_assignment_owner": sorted(rows_with_missing_anchor_assignment_owner),
            "rows_with_missing_anchor_taxonomy_owner": sorted(rows_with_missing_anchor_taxonomy_owner),
            "rows_with_ownership_conflicts": sorted(rows_with_ownership_conflicts),
        },
        "integrity_checks": integrity_checks,
    }


def run_stage_c_package1b_passive_governance_consumer(
    *,
    run_dir: Path,
    side: str = "base",
    output_path: Path | None = None,
) -> dict[str, Any]:
    run_dir = run_dir.resolve()
    row_fact_artifact = _load_json(run_dir / STAGE_C_ROW_FACT_ARTIFACT_NAME)
    family_a_artifact = _load_json(run_dir / STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME)
    guardrail_artifact = _load_json(run_dir / STAGE_C_GOVERNANCE_GUARDRAILS_ARTIFACT_NAME)
    runtime_summary_artifact = _load_json(run_dir / STAGE_C_RUNTIME_CONTRACT_SUMMARY_ARTIFACT_NAME)

    report = _build_passive_governance_report(
        run_dir=run_dir,
        side=side,
        row_fact_artifact=row_fact_artifact,
        family_a_artifact=family_a_artifact,
        guardrail_artifact=guardrail_artifact,
        runtime_summary_artifact=runtime_summary_artifact,
    )

    resolved_output_path = (output_path or (run_dir / STAGE_C_PACKAGE1B_GOVERNANCE_REPORT_NAME)).resolve()
    _write_json(resolved_output_path, report)

    return {
        "report_path": str(resolved_output_path),
        "consumer_scope": report["consumer_scope"],
        "analyzed_side": side,
        "row_fact_record_count": report["reported_values"]["row_fact_record_count"]["value"],
        "family_a_tool_expected_population_count": report["reported_values"][
            "family_a_tool_expected_population_count"
        ]["value"],
        "family_a_missing_evidence_count": report["reported_values"]["family_a_missing_evidence_count"]["value"],
        "ownership_conflict_row_count": report["reported_values"]["ownership_conflict_row_count"]["value"],
        "guardrails_clear": report["integrity_checks"]["guardrails_clear"],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Passive governance consumer over Stage C Package 1/1A artifacts.")
    parser.add_argument("--run-dir", required=True, help="Directory containing emitted Stage C artifacts")
    parser.add_argument("--side", default="base", help="Family A side to analyze (default: base)")
    parser.add_argument("--output-path", default=None, help="Optional output path for the governance report")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = run_stage_c_package1b_passive_governance_consumer(
        run_dir=Path(args.run_dir),
        side=str(args.side),
        output_path=Path(args.output_path).resolve() if args.output_path else None,
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
