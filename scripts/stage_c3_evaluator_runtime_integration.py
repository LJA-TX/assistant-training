#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping


class RuntimeIntegrationError(RuntimeError):
    """Raised when runtime integration cannot complete."""


@dataclass(frozen=True)
class FixtureDocument:
    path: Path
    payload: dict[str, Any]


def _load_module(module_path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, str(module_path))
    if spec is None or spec.loader is None:
        raise RuntimeIntegrationError(f"unable to load module at {module_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_foundations():
    scripts_dir = Path(__file__).resolve().parent
    c1 = _load_module(scripts_dir / "stage_c1_evaluator_foundation.py", "stage_c1_evaluator_foundation")
    c2 = _load_module(
        scripts_dir / "stage_c2_family_state_reconciliation_foundation.py",
        "stage_c2_family_state_reconciliation_foundation",
    )
    return c1, c2


def _canonical_fixture_hash(payload: Mapping[str, Any]) -> str:
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _as_nonempty_str(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _load_fixture_documents(fixtures_root: Path) -> list[FixtureDocument]:
    docs: list[FixtureDocument] = []
    for path in sorted(fixtures_root.rglob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise RuntimeIntegrationError(f"fixture root must be object: {path}")
        docs.append(FixtureDocument(path=path, payload=payload))
    return docs


def _family_scope(payload: Mapping[str, Any]) -> str:
    return _as_nonempty_str(payload.get("family")) or "Unspecified family scope"


def _concept_scope(payload: Mapping[str, Any]) -> str:
    return _as_nonempty_str(payload.get("governed_concept")) or str(payload.get("source_definition_id") or "unknown")


def _subslice_scope(payload: Mapping[str, Any]) -> str | None:
    return _as_nonempty_str(payload.get("intended_subtype")) or _as_nonempty_str(payload.get("intended_subslice_or_state"))


def _build_row_fact_records(c1, fixtures: list[FixtureDocument]) -> list[dict[str, Any]]:
    now_utc = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    records: list[dict[str, Any]] = []

    for doc in fixtures:
        fixture = doc.payload
        ownership = fixture.get("ownership_expectations")
        ownership_map = ownership if isinstance(ownership, Mapping) else {}
        expected_state = fixture.get("expected_state")
        expected_state_map = expected_state if isinstance(expected_state, Mapping) else {}

        payload = {
            "row_id": str(fixture.get("fixture_id") or doc.path.stem),
            "split_id": "all_splits",
            "excluded": False,
            "expected_tool_name": None,
            "membership_markers": {
                # Baseline integration intentionally avoids inferring family-specific row membership.
                "family_a_tool_expected_eligible": False,
                "family_b1_read_file_eligible": False,
                "family_b1_symbol_name_member": None,
                "family_b2_anchor_eligible": False,
                "family_b2_no_anchor_member": None,
                "family_b2_anchor_category": None,
            },
            "ownership_markers": {
                "symbol_name_membership_owner": _as_nonempty_str(ownership_map.get("membership_owner")),
                "anchor_assignment_owner": _as_nonempty_str(ownership_map.get("anchor_assignment_owner")),
                "anchor_taxonomy_owner": _as_nonempty_str(
                    ownership_map.get("anchor_taxonomy_owner") or ownership_map.get("taxonomy_owner")
                ),
                "conflicting_ownership_markers": False,
                "ownership_conflict_reasons": [],
            },
            "provenance": {
                "row_source": "stage_b_wp8_fixture_corpus",
                "dataset_id": "stage_b_wp8_validation_fixtures",
                "dataset_version": "contract-baseline",
                "extraction_timestamp_utc": now_utc,
                "evidence_digest": _canonical_fixture_hash(fixture),
            },
            "denominator_provenance": {
                "eligible_population_source": "stage_b_fixture_inventory_population",
                "non_exact_population_source": "stage_b_fixture_inventory_population",
                "read_file_population_source": None,
                "symbol_name_population_source": None,
                "anchor_population_source": None,
                "no_anchor_population_source": None,
            },
            "evidence": {
                "fixture_path": str(doc.path),
                "source_definition_id": fixture.get("source_definition_id"),
                "required_inputs_keys": sorted((fixture.get("required_inputs") or {}).keys()),
                "ownership_expectations": dict(ownership_map),
                "expected_state": dict(expected_state_map),
                "guardrail_flags": {
                    "inference_used": False,
                    "substitution_used": False,
                    "reconstruction_used": False,
                },
            },
        }
        records.append(c1.build_row_fact_record(payload).to_dict())

    return records


def _build_state_axis_records(c2, fixtures: list[FixtureDocument]) -> list[dict[str, Any]]:
    state_records: list[dict[str, Any]] = []
    for doc in fixtures:
        fixture = doc.payload
        expected_state = fixture.get("expected_state")
        if not isinstance(expected_state, Mapping):
            continue

        completeness = c2.CompletenessState(expected_state["completeness"])
        current_run = c2.CurrentRunComputabilityState(expected_state["current_run_computability"])
        comparability = c2.ComparabilityState(expected_state["comparability"])
        noncomputability_reasons = tuple(str(x) for x in expected_state.get("noncomputability_reasons", []))
        comparison_block_reasons = tuple(str(x) for x in expected_state.get("comparison_block_reasons", []))

        concept_id = str(fixture.get("fixture_id") or fixture.get("source_definition_id") or doc.path.stem)
        record = c2.ConceptStateRecord(
            concept_id=concept_id,
            completeness=completeness,
            current_run_computability=current_run,
            comparability=comparability,
            noncomputability_reasons=noncomputability_reasons,
            comparison_block_reasons=comparison_block_reasons,
            missing_required_evidence_fields=tuple(),
        )
        state_records.append(record.to_dict())

    return state_records


def _build_aggregation_reports(c2, fixtures: list[FixtureDocument]) -> list[dict[str, Any]]:
    rows_by_family: dict[str, list[Any]] = defaultdict(list)

    for doc in fixtures:
        fixture = doc.payload
        expected_state = fixture.get("expected_state")
        expected_state_map = expected_state if isinstance(expected_state, Mapping) else {}

        current_run_value = str(expected_state_map.get("current_run_computability") or "")
        counted = current_run_value == c2.CurrentRunComputabilityState.COMPUTABLE.value

        row = c2.build_aggregation_row(
            {
                "family_id": _family_scope(fixture),
                "concept_id": _concept_scope(fixture),
                "row_id": str(fixture.get("fixture_id") or doc.path.stem),
                "split_id": "all_splits",
                "sub_slice_id": _subslice_scope(fixture),
                "eligible": True,
                "counted": counted,
                "excluded": False,
                "provenance_ref": f"fixture:{doc.path}",
                "evidence_ref": f"fixture_id:{fixture.get('fixture_id')}",
            }
        )
        rows_by_family[row.family_id].append(row)

    reports: list[dict[str, Any]] = []
    for family_id in sorted(rows_by_family):
        report = c2.aggregate_family_rows(family_id, rows_by_family[family_id])
        reports.append(report.to_dict())
    return reports


def _build_reconciliation_report(c2, state_records: list[dict[str, Any]], harness_report: dict[str, Any], aggregation_reports: list[dict[str, Any]]) -> dict[str, Any]:
    fixture_count = int(harness_report["fixture_count"])
    valid_count = int(harness_report["valid_fixture_count"])
    invalid_count = int(harness_report["invalid_fixture_count"])

    completeness_counter = Counter(record["completeness"] for record in state_records)
    comparability_counter = Counter(record["comparability"] for record in state_records)
    computable_count = sum(1 for record in state_records if record["current_run_computability"] == c2.CurrentRunComputabilityState.COMPUTABLE.value)

    family_counts = [int(report["total_rows"]) for report in aggregation_reports]
    family_labels = [str(report["family_id"]) for report in aggregation_reports]

    comparability_labels = sorted(comparability_counter.keys())
    comparability_denominators = [comparability_counter[label] for label in comparability_labels]
    comparability_computable_numerators = [
        sum(
            1
            for record in state_records
            if record["comparability"] == label
            and record["current_run_computability"] == c2.CurrentRunComputabilityState.COMPUTABLE.value
        )
        for label in comparability_labels
    ]

    checks = [
        c2.validate_denominator_partition(
            {
                "check_id": "fixture_inventory_completeness_partition",
                "parent_denominator": fixture_count,
                "partition_denominators": [
                    completeness_counter.get(c2.CompletenessState.COMPLETE.value, 0),
                    completeness_counter.get(c2.CompletenessState.PARTIAL.value, 0),
                    completeness_counter.get(c2.CompletenessState.MISSING.value, 0),
                ],
                "partition_labels": [
                    c2.CompletenessState.COMPLETE.value,
                    c2.CompletenessState.PARTIAL.value,
                    c2.CompletenessState.MISSING.value,
                ],
            }
        ),
        c2.validate_parent_subslice_boundary(
            {
                "check_id": "computability_by_comparability_boundary",
                "parent_numerator": computable_count,
                "parent_denominator": fixture_count,
                "subslice_numerators": comparability_computable_numerators,
                "subslice_denominators": comparability_denominators,
                "subslice_labels": comparability_labels,
            }
        ),
        c2.validate_split_to_aggregate(
            {
                "check_id": "family_inventory_split_to_aggregate",
                "aggregate_numerator": fixture_count,
                "aggregate_denominator": fixture_count,
                "split_numerators": family_counts,
                "split_denominators": family_counts,
                "split_labels": family_labels,
            }
        ),
        c2.validate_coverage_arithmetic(
            {
                "check_id": "fixture_validation_coverage_arithmetic",
                "covered_count": valid_count,
                "uncovered_count": invalid_count,
                "total_count": fixture_count,
            }
        ),
    ]

    return c2.build_reconciliation_report(checks).to_dict()


def _build_governance_guardrail_artifact(harness_report: dict[str, Any], row_fact_records: list[dict[str, Any]]) -> dict[str, Any]:
    issue_counts = harness_report.get("issue_counts_by_code", {})
    collapsed_state_issues = int(issue_counts.get("collapsed_state_field", 0))
    forbidden_detector_behavior_issues = int(issue_counts.get("forbidden_detector_behavior", 0))
    invalid_state_issues = sum(
        int(issue_counts.get(code, 0))
        for code in (
            "invalid_completeness_state",
            "invalid_current_run_computability_state",
            "invalid_comparability_state",
        )
    )

    inference_flags = 0
    substitution_flags = 0
    reconstruction_flags = 0
    ownership_fields_present = 0

    for record in row_fact_records:
        evidence = record.get("evidence") or {}
        guardrail_flags = evidence.get("guardrail_flags") if isinstance(evidence, Mapping) else {}
        if isinstance(guardrail_flags, Mapping):
            if bool(guardrail_flags.get("inference_used")):
                inference_flags += 1
            if bool(guardrail_flags.get("substitution_used")):
                substitution_flags += 1
            if bool(guardrail_flags.get("reconstruction_used")):
                reconstruction_flags += 1

        ownership = record.get("ownership_markers") or {}
        if isinstance(ownership, Mapping):
            present = any(
                bool(ownership.get(key))
                for key in (
                    "symbol_name_membership_owner",
                    "anchor_assignment_owner",
                    "anchor_taxonomy_owner",
                )
            )
            if present:
                ownership_fields_present += 1

    return {
        "guardrail_status": {
            "collapsed_state_behavior_detected": collapsed_state_issues > 0,
            "forbidden_detector_behavior_detected": forbidden_detector_behavior_issues > 0,
            "invalid_state_axis_values_detected": invalid_state_issues > 0,
            "inference_behavior_detected": inference_flags > 0,
            "substitution_behavior_detected": substitution_flags > 0,
            "reconstruction_behavior_detected": reconstruction_flags > 0,
        },
        "guardrail_counts": {
            "collapsed_state_issues": collapsed_state_issues,
            "forbidden_detector_behavior_issues": forbidden_detector_behavior_issues,
            "invalid_state_axis_issues": invalid_state_issues,
            "inference_flags": inference_flags,
            "substitution_flags": substitution_flags,
            "reconstruction_flags": reconstruction_flags,
            "records_with_ownership_fields_present": ownership_fields_present,
            "total_row_fact_records": len(row_fact_records),
        },
    }


def _build_fixture_inventory_artifact(fixtures: list[FixtureDocument], harness_report: dict[str, Any]) -> dict[str, Any]:
    fixture_ids = [str(doc.payload.get("fixture_id") or doc.path.stem) for doc in fixtures]
    source_definition_ids = [str(doc.payload.get("source_definition_id") or "") for doc in fixtures]

    return {
        "fixture_count": len(fixtures),
        "fixture_ids": fixture_ids,
        "source_definition_ids": source_definition_ids,
        "family_group_counts": harness_report.get("fixture_counts_by_family_group", {}),
        "state_tuple_counts": harness_report.get("state_tuple_counts", {}),
        "harness_issue_count": int(harness_report.get("issue_count", 0)),
        "harness_invalid_fixture_count": int(harness_report.get("invalid_fixture_count", 0)),
    }


def _build_validation_issue_artifact(harness_report: dict[str, Any]) -> dict[str, Any]:
    return {
        "issue_count": int(harness_report.get("issue_count", 0)),
        "invalid_fixture_count": int(harness_report.get("invalid_fixture_count", 0)),
        "issue_counts_by_code": dict(harness_report.get("issue_counts_by_code", {})),
        "issues": list(harness_report.get("issues", [])),
    }


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_stage_c3_runtime_integration(fixtures_root: Path, artifacts_dir: Path) -> dict[str, Any]:
    c1, c2 = _load_foundations()

    fixtures_root = fixtures_root.resolve()
    artifacts_dir = artifacts_dir.resolve()
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    harness = c1.run_fixture_harness(fixtures_root).to_dict()
    fixtures = _load_fixture_documents(fixtures_root)
    row_facts = _build_row_fact_records(c1, fixtures)
    state_records = _build_state_axis_records(c2, fixtures)
    aggregation_reports = _build_aggregation_reports(c2, fixtures)
    reconciliation_report = _build_reconciliation_report(c2, state_records, harness, aggregation_reports)

    fixture_inventory = _build_fixture_inventory_artifact(fixtures, harness)
    governance_guardrails = _build_governance_guardrail_artifact(harness, row_facts)
    validation_issues = _build_validation_issue_artifact(harness)

    artifact_payloads: dict[str, dict[str, Any]] = {
        "fixture_inventory": fixture_inventory,
        "row_fact_metadata": {
            "row_fact_count": len(row_facts),
            "records": row_facts,
        },
        "state_axis": {
            "record_count": len(state_records),
            "records": state_records,
        },
        "aggregation_summary": {
            "family_report_count": len(aggregation_reports),
            "family_reports": aggregation_reports,
        },
        "reconciliation_summary": reconciliation_report,
        "governance_guardrails": governance_guardrails,
        "validation_issues": validation_issues,
        "runtime_contract_summary": {
            "fixtures_root": str(fixtures_root),
            "artifacts_dir": str(artifacts_dir),
            "generated_at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "contract_scope": "stage_c3_baseline_integration",
            "harness_issue_count": validation_issues["issue_count"],
            "reconciliation_fail_count": reconciliation_report["fail_count"],
            "guardrail_status": governance_guardrails["guardrail_status"],
        },
    }

    artifact_paths: dict[str, str] = {}
    for name, payload in artifact_payloads.items():
        out_path = artifacts_dir / f"c3_{name}_artifact.json"
        _write_json(out_path, payload)
        artifact_paths[name] = str(out_path)

    summary = {
        "artifact_paths": artifact_paths,
        "fixture_count": fixture_inventory["fixture_count"],
        "harness_issue_count": validation_issues["issue_count"],
        "reconciliation_fail_count": reconciliation_report["fail_count"],
        "reconciliation_blocked_count": reconciliation_report["blocked_count"],
        "guardrail_status": governance_guardrails["guardrail_status"],
    }

    summary_path = artifacts_dir / "c3_runtime_integration_summary.json"
    _write_json(summary_path, summary)
    summary["summary_path"] = str(summary_path)
    return summary


def _default_fixtures_root() -> Path:
    return Path("/opt/ai-stack/assistant-training/manifests/reports/stage_b_wp8_validation/fixtures")


def _default_artifacts_dir() -> Path:
    return Path("/opt/ai-stack/assistant-training/reports/stage_c3/baseline_contract_artifacts")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stage C3 evaluator runtime integration and baseline contract artifact emission"
    )
    parser.add_argument(
        "--fixtures-root",
        default=str(_default_fixtures_root()),
        help="Path to Stage B fixture root",
    )
    parser.add_argument(
        "--artifacts-dir",
        default=str(_default_artifacts_dir()),
        help="Output directory for baseline contract artifacts",
    )
    args = parser.parse_args()

    summary = run_stage_c3_runtime_integration(
        fixtures_root=Path(args.fixtures_root),
        artifacts_dir=Path(args.artifacts_dir),
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    if summary["harness_issue_count"] > 0:
        return 1
    if summary["reconciliation_fail_count"] > 0:
        return 1
    guardrails = summary["guardrail_status"]
    if any(bool(v) for v in guardrails.values()):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
