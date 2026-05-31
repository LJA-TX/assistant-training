#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping


class ReportingIntegrationError(RuntimeError):
    """Raised when Stage C6 reporting integration cannot proceed."""


def _load_module(module_path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, str(module_path))
    if spec is None or spec.loader is None:
        raise ReportingIntegrationError(f"unable to load module at {module_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_stage_c5():
    scripts_dir = Path(__file__).resolve().parent
    return _load_module(scripts_dir / "stage_c5_scoring_path_integration.py", "stage_c5_scoring_path_integration")


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _as_nonempty_str(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _build_per_fixture_summary(
    per_fixture_records: list[dict[str, Any]],
    per_output_records: list[dict[str, Any]],
) -> dict[str, Any]:
    outputs_by_fixture: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in per_output_records:
        fixture_id = _as_nonempty_str(row.get("fixture_id")) or "unresolved-fixture"
        outputs_by_fixture[fixture_id].append(row)

    rows: list[dict[str, Any]] = []
    for fixture_row in per_fixture_records:
        fixture_id = _as_nonempty_str(fixture_row.get("fixture_id")) or "unresolved-fixture"
        linked = outputs_by_fixture.get(fixture_id, [])

        evidence_links = [
            {
                "record_id": row.get("record_id"),
                "model_identifier": row.get("model_identifier"),
                "parse_status": row.get("parse_status"),
                "tool_call_status": row.get("tool_call_status"),
                "overall_status": row.get("overall_status"),
                "fail_reasons": row.get("fail_reasons", []),
            }
            for row in linked
        ]

        unique_fail_reasons = sorted(
            {
                str(reason)
                for row in linked
                for reason in row.get("fail_reasons", [])
                if isinstance(reason, str)
            }
        )

        rows.append(
            {
                "fixture_id": fixture_id,
                "record_count": int(fixture_row.get("record_count", 0)),
                "pass_count": int(fixture_row.get("pass_count", 0)),
                "fail_count": int(fixture_row.get("fail_count", 0)),
                "overall_status": fixture_row.get("overall_status"),
                "fail_reasons": fixture_row.get("fail_reasons", []),
                "unique_fail_reasons": unique_fail_reasons,
                "evidence_links": evidence_links,
            }
        )

    return {
        "fixture_count": len(rows),
        "records": rows,
    }


def _build_per_model_summary(per_output_records: list[dict[str, Any]]) -> dict[str, Any]:
    by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in per_output_records:
        model = _as_nonempty_str(row.get("model_identifier")) or "unknown_model"
        by_model[model].append(row)

    model_rows: list[dict[str, Any]] = []
    for model in sorted(by_model):
        rows = by_model[model]
        parse_counter = Counter(str(row.get("parse_status") or "unknown") for row in rows)
        tool_counter = Counter(str(row.get("tool_call_status") or "unknown") for row in rows)
        no_call_counter = Counter(str(row.get("no_call_status") or "unknown") for row in rows)

        fail_reasons = [
            str(reason)
            for row in rows
            for reason in row.get("fail_reasons", [])
            if isinstance(reason, str)
        ]
        fail_reason_counter = Counter(fail_reasons)

        model_rows.append(
            {
                "model_identifier": model,
                "record_count": len(rows),
                "pass_count": sum(1 for row in rows if row.get("overall_status") == "pass"),
                "fail_count": sum(1 for row in rows if row.get("overall_status") == "fail"),
                "parse_status_counts": dict(sorted(parse_counter.items())),
                "tool_call_status_counts": dict(sorted(tool_counter.items())),
                "no_call_status_counts": dict(sorted(no_call_counter.items())),
                "wrapper_or_prose_leakage_count": sum(1 for row in rows if bool(row.get("wrapper_or_prose_leakage"))),
                "failure_reason_counts": dict(sorted(fail_reason_counter.items())),
                "record_ids": [row.get("record_id") for row in rows],
            }
        )

    return {
        "model_count": len(model_rows),
        "records": model_rows,
    }


def _build_parse_tool_nocall_summary(
    c5_parse_summary: Mapping[str, Any],
    per_output_records: list[dict[str, Any]],
) -> dict[str, Any]:
    parse_failure_record_ids = [
        row.get("record_id")
        for row in per_output_records
        if str(row.get("parse_status") or "") != "strict_json_object"
    ]

    tool_call_missing_record_ids = [
        row.get("record_id")
        for row in per_output_records
        if str(row.get("tool_call_status") or "") in {
            "tool_calls_key_missing",
            "tool_calls_not_list",
            "tool_call_unavailable_parse_failure",
            "tool_call_unavailable_record_invalid",
        }
    ]

    no_call_mismatch_record_ids = []
    for row in per_output_records:
        for dimension in row.get("scoring_dimensions", []):
            if (
                isinstance(dimension, Mapping)
                and dimension.get("dimension") == "no_call_correctness"
                and dimension.get("status") == "fail"
            ):
                no_call_mismatch_record_ids.append(row.get("record_id"))
                break

    return {
        "parse_tool_nocall_counts": dict(c5_parse_summary),
        "parse_failure_record_ids": parse_failure_record_ids,
        "tool_call_missing_record_ids": tool_call_missing_record_ids,
        "no_call_mismatch_record_ids": no_call_mismatch_record_ids,
    }


def _build_wrapper_summary(
    c5_wrapper_summary: Mapping[str, Any],
    per_output_records: list[dict[str, Any]],
) -> dict[str, Any]:
    wrapper_failure_reasons = []
    for row in per_output_records:
        for dimension in row.get("scoring_dimensions", []):
            if (
                isinstance(dimension, Mapping)
                and dimension.get("dimension") == "wrapper_leakage"
                and dimension.get("status") == "fail"
            ):
                wrapper_failure_reasons.append(
                    {
                        "record_id": row.get("record_id"),
                        "reason": dimension.get("reason"),
                    }
                )

    return {
        "wrapper_counts": dict(c5_wrapper_summary),
        "wrapper_failure_reasons": wrapper_failure_reasons,
    }


def _build_validation_issue_summary(c5_validation: Mapping[str, Any]) -> dict[str, Any]:
    c4_validation = c5_validation.get("c4_validation_issues", {}) if isinstance(c5_validation, Mapping) else {}
    c5_scoring_validation = c5_validation.get("c5_scoring_validation_issues", {}) if isinstance(c5_validation, Mapping) else {}

    c4_issues = c4_validation.get("issues", []) if isinstance(c4_validation, Mapping) else []
    c5_issues = c5_scoring_validation.get("issues", []) if isinstance(c5_scoring_validation, Mapping) else []

    merged_issues = list(c4_issues) + list(c5_issues)
    merged_counter = Counter(str(issue.get("issue_code") or "unknown") for issue in merged_issues if isinstance(issue, Mapping))

    return {
        "c4_validation_issue_count": int(c4_validation.get("issue_count", 0)) if isinstance(c4_validation, Mapping) else 0,
        "c5_scoring_validation_issue_count": int(c5_scoring_validation.get("issue_count", 0)) if isinstance(c5_scoring_validation, Mapping) else 0,
        "combined_validation_issue_count": len(merged_issues),
        "combined_issue_counts_by_code": dict(sorted(merged_counter.items())),
        "issues": merged_issues,
    }


def _build_governance_summary(c5_governance: Mapping[str, Any]) -> dict[str, Any]:
    status = dict(c5_governance.get("guardrail_status", {})) if isinstance(c5_governance, Mapping) else {}
    counts = dict(c5_governance.get("guardrail_counts", {})) if isinstance(c5_governance, Mapping) else {}

    return {
        "guardrail_status": status,
        "guardrail_counts": counts,
        "migration_authority": {
            "detector_projection_authoritative": False,
            "detector_migration_enabled": False,
            "threshold_profile_migration_enabled": False,
        },
    }


def _build_detector_projection_preparation(
    per_output_records: list[dict[str, Any]],
    c4_state_axis_records: list[dict[str, Any]],
    c4_row_fact_records: list[dict[str, Any]],
    governance_summary: Mapping[str, Any],
) -> dict[str, Any]:
    state_by_record_id = {
        str(record.get("concept_id")): record
        for record in c4_state_axis_records
        if isinstance(record, Mapping)
    }
    row_fact_by_row_id = {
        str(record.get("row_id")): record
        for record in c4_row_fact_records
        if isinstance(record, Mapping)
    }

    projection_rows: list[dict[str, Any]] = []
    for row in per_output_records:
        record_id = str(row.get("record_id"))
        state = state_by_record_id.get(record_id, {})
        row_fact = row_fact_by_row_id.get(record_id, {})

        projection_rows.append(
            {
                "record_id": record_id,
                "fixture_id": row.get("fixture_id"),
                "model_identifier": row.get("model_identifier"),
                "projection_state_axes": {
                    "completeness": state.get("completeness"),
                    "current_run_computability": state.get("current_run_computability"),
                    "comparability": state.get("comparability"),
                    "noncomputability_reasons": state.get("noncomputability_reasons", []),
                    "comparison_block_reasons": state.get("comparison_block_reasons", []),
                },
                "projection_provenance": {
                    "provenance": row_fact.get("provenance"),
                    "denominator_provenance": row_fact.get("denominator_provenance"),
                },
                "projection_scoring_evidence": {
                    "overall_status": row.get("overall_status"),
                    "fail_reasons": row.get("fail_reasons", []),
                    "scoring_dimensions": row.get("scoring_dimensions", []),
                },
                "non_inference_guardrails": governance_summary.get("guardrail_status", {}),
            }
        )

    return {
        "projection_scope": "preparation_only_non_authoritative",
        "authoritative_detector_output": False,
        "detector_migration_enabled": False,
        "threshold_profile_migration_enabled": False,
        "mapping_specification": {
            "completeness_axis_source": "c4_state_axis_from_outputs_artifact.records[].completeness",
            "current_run_computability_axis_source": "c4_state_axis_from_outputs_artifact.records[].current_run_computability",
            "comparability_axis_source": "c4_state_axis_from_outputs_artifact.records[].comparability",
            "non_inference_guardrail_source": "c5_governance_guardrails_artifact.guardrail_status",
            "denominator_provenance_source": "c4_row_fact_metadata_artifact.records[].denominator_provenance",
            "scoring_evidence_source": "c5_per_output_scoring_status_artifact.records[]",
        },
        "prepared_projection_record_count": len(projection_rows),
        "prepared_projection_records": projection_rows,
    }


def run_stage_c6_reporting_integration(
    fixtures_root: Path,
    output_records_path: Path,
    artifacts_dir: Path,
) -> dict[str, Any]:
    c5 = _load_stage_c5()

    fixtures_root = fixtures_root.resolve()
    output_records_path = output_records_path.resolve()
    artifacts_dir = artifacts_dir.resolve()
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    scoring_dir = artifacts_dir / "scoring"
    c5_summary = c5.run_stage_c5_scoring_integration(
        fixtures_root=fixtures_root,
        output_records_path=output_records_path,
        artifacts_dir=scoring_dir,
    )

    c5_per_output = _load_json(Path(c5_summary["artifact_paths"]["per_output_scoring_status"]))
    c5_per_fixture = _load_json(Path(c5_summary["artifact_paths"]["per_fixture_scoring_status"]))
    c5_parse_tool = _load_json(Path(c5_summary["artifact_paths"]["parse_tool_nocall_scoring_summary"]))
    c5_wrapper = _load_json(Path(c5_summary["artifact_paths"]["wrapper_leakage_scoring_summary"]))
    c5_validation = _load_json(Path(c5_summary["artifact_paths"]["validation_issues"]))
    c5_governance = _load_json(Path(c5_summary["artifact_paths"]["governance_guardrails"]))
    c5_runtime = _load_json(Path(c5_summary["artifact_paths"]["runtime_scoring_summary"]))

    c4_summary = c5_runtime.get("c4_summary", {}) if isinstance(c5_runtime, Mapping) else {}
    c4_artifact_paths = c4_summary.get("artifact_paths", {}) if isinstance(c4_summary, Mapping) else {}
    c4_state_axis = _load_json(Path(c4_artifact_paths["state_axis_from_outputs"]))
    c4_row_fact = _load_json(Path(c4_artifact_paths["row_fact_metadata"]))

    per_output_records = c5_per_output.get("records", []) if isinstance(c5_per_output, Mapping) else []
    per_fixture_records = c5_per_fixture.get("records", []) if isinstance(c5_per_fixture, Mapping) else []

    per_fixture_summary = _build_per_fixture_summary(per_fixture_records, per_output_records)
    per_model_summary = _build_per_model_summary(per_output_records)
    parse_tool_nocall_summary = _build_parse_tool_nocall_summary(c5_parse_tool, per_output_records)
    wrapper_summary = _build_wrapper_summary(c5_wrapper, per_output_records)
    validation_summary = _build_validation_issue_summary(c5_validation)
    governance_summary = _build_governance_summary(c5_governance)

    runtime_scoring_summary = {
        "contract_scope": "stage_c6_scoring_report_integration",
        "fixtures_root": str(fixtures_root),
        "output_records_path": str(output_records_path),
        "artifacts_dir": str(artifacts_dir),
        "generated_at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "record_count": len(per_output_records),
        "fixture_count": int(per_fixture_summary.get("fixture_count", 0)),
        "model_count": int(per_model_summary.get("model_count", 0)),
        "overall_pass_count": sum(1 for row in per_output_records if row.get("overall_status") == "pass"),
        "overall_fail_count": sum(1 for row in per_output_records if row.get("overall_status") == "fail"),
        "validation_issue_summary": {
            "c4_validation_issue_count": validation_summary.get("c4_validation_issue_count"),
            "c5_scoring_validation_issue_count": validation_summary.get("c5_scoring_validation_issue_count"),
            "combined_validation_issue_count": validation_summary.get("combined_validation_issue_count"),
        },
        "guardrail_status": governance_summary.get("guardrail_status", {}),
        "c5_summary": c5_summary,
    }

    detector_projection_preparation = _build_detector_projection_preparation(
        per_output_records=per_output_records,
        c4_state_axis_records=c4_state_axis.get("records", []),
        c4_row_fact_records=c4_row_fact.get("records", []),
        governance_summary=governance_summary,
    )

    artifact_payloads = {
        "per_fixture_scoring_summary": per_fixture_summary,
        "per_model_scoring_summary": per_model_summary,
        "parse_tool_nocall_summary": parse_tool_nocall_summary,
        "wrapper_leakage_summary": wrapper_summary,
        "validation_issue_summary": validation_summary,
        "governance_guardrail_summary": governance_summary,
        "runtime_scoring_summary": runtime_scoring_summary,
        "detector_projection_preparation": detector_projection_preparation,
    }

    artifact_paths: dict[str, str] = {}
    for name, payload in artifact_payloads.items():
        out_path = artifacts_dir / f"c6_{name}_artifact.json"
        _write_json(out_path, payload)
        artifact_paths[name] = str(out_path)

    summary = {
        "artifact_paths": artifact_paths,
        "record_count": len(per_output_records),
        "overall_pass_count": runtime_scoring_summary["overall_pass_count"],
        "overall_fail_count": runtime_scoring_summary["overall_fail_count"],
        "guardrail_status": governance_summary.get("guardrail_status", {}),
        "detector_projection_authoritative": detector_projection_preparation["authoritative_detector_output"],
    }

    summary_path = artifacts_dir / "c6_reporting_summary.json"
    _write_json(summary_path, summary)
    summary["summary_path"] = str(summary_path)
    return summary


def _default_fixtures_root() -> Path:
    return Path("/opt/ai-stack/assistant-training/manifests/reports/stage_b_wp8_validation/fixtures")


def _default_output_records_path() -> Path:
    return Path("/opt/ai-stack/assistant-training/reports/stage_c6/input/stage_c6_sample_output_records.jsonl")


def _default_artifacts_dir() -> Path:
    return Path("/opt/ai-stack/assistant-training/reports/stage_c6/reporting_artifacts")


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage C6 scoring report integration")
    parser.add_argument("--fixtures-root", default=str(_default_fixtures_root()))
    parser.add_argument("--output-records-path", default=str(_default_output_records_path()))
    parser.add_argument("--artifacts-dir", default=str(_default_artifacts_dir()))
    args = parser.parse_args()

    summary = run_stage_c6_reporting_integration(
        fixtures_root=Path(args.fixtures_root),
        output_records_path=Path(args.output_records_path),
        artifacts_dir=Path(args.artifacts_dir),
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    if summary.get("detector_projection_authoritative"):
        return 1

    guardrails = summary.get("guardrail_status", {})
    if any(bool(value) for value in guardrails.values()):
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
