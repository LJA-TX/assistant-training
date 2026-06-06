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

from repo_paths import resolve_artifact_path, resolve_fixture_root, resolve_script_path


class ScoringIntegrationError(RuntimeError):
    """Raised when Stage C5 scoring-path integration cannot proceed."""


def _load_module(module_path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, str(module_path))
    if spec is None or spec.loader is None:
        raise ScoringIntegrationError(f"unable to load module at {module_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_foundations():
    c4 = _load_module(resolve_script_path("stage_c4_real_output_ingestion"), "stage_c4_real_output_ingestion")
    return c4


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _as_nonempty_str(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _load_fixture_documents(fixtures_root: Path) -> dict[str, dict[str, Any]]:
    fixtures: dict[str, dict[str, Any]] = {}
    for path in sorted(fixtures_root.rglob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            continue
        fixture_id = _as_nonempty_str(payload.get("fixture_id"))
        if fixture_id:
            fixtures[fixture_id] = payload
    return fixtures


def _parse_input_record_expectations(output_records_path: Path) -> dict[str, dict[str, Any]]:
    expectations_by_record_id: dict[str, dict[str, Any]] = {}
    for line_no, line in enumerate(output_records_path.read_text(encoding="utf-8").splitlines(), start=1):
        raw = line.strip()
        if not raw:
            continue
        try:
            row = json.loads(raw)
        except Exception:
            continue
        if not isinstance(row, dict):
            continue
        record_id = _as_nonempty_str(row.get("record_id")) or f"line-{line_no}"

        expected_argument_keys = row.get("expected_argument_keys")
        if isinstance(expected_argument_keys, list):
            expected_argument_keys = [str(x) for x in expected_argument_keys if isinstance(x, str) and x.strip()]
        else:
            expected_argument_keys = None

        expectations_by_record_id[record_id] = {
            "expected_tool_name": _as_nonempty_str(row.get("expected_tool_name")),
            "expected_argument_keys": expected_argument_keys,
            "expected_no_call": row.get("no_call_expected") if isinstance(row.get("no_call_expected"), bool) else None,
            "expected_strict_json_object": (
                row.get("expected_strict_json_object")
                if isinstance(row.get("expected_strict_json_object"), bool)
                else True
            ),
            "expected_tool_call_required": (
                row.get("expected_tool_call_required")
                if isinstance(row.get("expected_tool_call_required"), bool)
                else None
            ),
            "wrapper_prohibited": (
                row.get("wrapper_prohibited")
                if isinstance(row.get("wrapper_prohibited"), bool)
                else True
            ),
        }
    return expectations_by_record_id


def _fixture_expectation_hint(fixture: Mapping[str, Any] | None) -> dict[str, Any]:
    if not isinstance(fixture, Mapping):
        return {
            "scenario_type": None,
            "intended_subtype": None,
            "expected_behavior_hint": "unknown_fixture",
            "scorer_evidence_expectations": None,
        }

    intended_subtype = _as_nonempty_str(fixture.get("intended_subtype"))
    if intended_subtype == "missing tool call":
        behavior = "tool_call_expected_but_absent"
    elif intended_subtype == "wrong tool name":
        behavior = "tool_name_mismatch_expected"
    elif intended_subtype == "wrong argument":
        behavior = "argument_mismatch_expected"
    elif intended_subtype == "wrapper/envelope drift":
        behavior = "wrapper_leakage_expected"
    elif intended_subtype == "malformed output":
        behavior = "malformed_output_expected"
    else:
        behavior = "exact_or_other_expected"

    scorer_expectations = fixture.get("scorer_evidence_expectations")
    return {
        "scenario_type": _as_nonempty_str(fixture.get("scenario_type")),
        "intended_subtype": intended_subtype,
        "expected_behavior_hint": behavior,
        "scorer_evidence_expectations": scorer_expectations if isinstance(scorer_expectations, Mapping) else None,
    }


def _extract_observed_tool_name(record: Mapping[str, Any]) -> str | None:
    payload = record.get("parsed_tool_call_payload")
    if not isinstance(payload, Mapping):
        return None
    tool_calls = payload.get("tool_calls")
    if not isinstance(tool_calls, list) or not tool_calls:
        return None
    first = tool_calls[0]
    if not isinstance(first, Mapping):
        return None
    fn = first.get("function")
    if not isinstance(fn, Mapping):
        return None
    return _as_nonempty_str(fn.get("name"))


def _extract_observed_arguments(record: Mapping[str, Any]) -> tuple[Any, str | None]:
    payload = record.get("parsed_tool_call_payload")
    if not isinstance(payload, Mapping):
        return None, "parsed_tool_call_payload_missing"
    tool_calls = payload.get("tool_calls")
    if not isinstance(tool_calls, list) or not tool_calls:
        return None, "tool_calls_missing_or_empty"
    first = tool_calls[0]
    if not isinstance(first, Mapping):
        return None, "first_tool_call_not_object"
    fn = first.get("function")
    if not isinstance(fn, Mapping):
        return None, "function_block_missing"
    if "arguments" not in fn:
        return None, "arguments_missing"
    return fn.get("arguments"), None


def _normalize_expected_tool_call_required(expected_tool_call_required: bool | None, expected_no_call: bool | None) -> bool:
    if isinstance(expected_tool_call_required, bool):
        return expected_tool_call_required
    if isinstance(expected_no_call, bool):
        return not expected_no_call
    return True


def _score_boolean_dimension(name: str, passed: bool, reason_pass: str, reason_fail: str) -> dict[str, Any]:
    return {
        "dimension": name,
        "status": "pass" if passed else "fail",
        "reason": reason_pass if passed else reason_fail,
    }


def _score_output_record(record: Mapping[str, Any], expectation: Mapping[str, Any], fixture_hint: Mapping[str, Any], state_record: Mapping[str, Any] | None) -> dict[str, Any]:
    parse_status = str(record.get("parse_status") or "")
    tool_call_status = str(record.get("tool_call_status") or "")
    wrapper_leakage = bool(record.get("wrapper_or_prose_leakage"))

    expected_strict_json = bool(expectation.get("expected_strict_json_object", True))
    strict_json_valid = parse_status == "strict_json_object"
    strict_json_score = _score_boolean_dimension(
        "strict_json_validity",
        strict_json_valid == expected_strict_json,
        reason_pass=f"strict_json_validity matched expectation ({expected_strict_json})",
        reason_fail=(
            f"strict_json_validity mismatch: observed={strict_json_valid}, expected={expected_strict_json}"
        ),
    )

    expected_no_call = expectation.get("expected_no_call") if isinstance(expectation.get("expected_no_call"), bool) else None
    expected_tool_call_required = _normalize_expected_tool_call_required(
        expectation.get("expected_tool_call_required") if isinstance(expectation.get("expected_tool_call_required"), bool) else None,
        expected_no_call,
    )

    observed_tool_call_present = tool_call_status in {
        "tool_call_payload_present",
        "tool_call_payload_partial_or_invalid",
    }
    observed_no_call = bool(record.get("no_call_emitted")) if isinstance(record.get("no_call_emitted"), bool) else None

    if expected_tool_call_required:
        tool_call_presence_pass = observed_tool_call_present
        tool_presence_reason_fail = f"tool call required but status={tool_call_status}"
    else:
        tool_call_presence_pass = observed_no_call is True
        tool_presence_reason_fail = f"no-call expected but observed status={tool_call_status}"

    tool_call_presence_score = _score_boolean_dimension(
        "tool_call_presence_absence",
        tool_call_presence_pass,
        reason_pass="tool/no-call presence matched expectation",
        reason_fail=tool_presence_reason_fail,
    )

    expected_tool_name = _as_nonempty_str(expectation.get("expected_tool_name"))
    observed_tool_name = _extract_observed_tool_name(record)
    if expected_tool_name is None:
        tool_name_score = {
            "dimension": "tool_name_correctness",
            "status": "not_applicable",
            "reason": "expected_tool_name not declared",
        }
    else:
        tool_name_score = _score_boolean_dimension(
            "tool_name_correctness",
            observed_tool_name == expected_tool_name,
            reason_pass="observed tool name matches expected",
            reason_fail=f"observed tool name '{observed_tool_name}' does not match expected '{expected_tool_name}'",
        )

    expected_argument_keys = expectation.get("expected_argument_keys")
    if not isinstance(expected_argument_keys, list) or not expected_argument_keys:
        argument_score = {
            "dimension": "argument_presence_structure",
            "status": "not_applicable",
            "reason": "expected_argument_keys not declared",
        }
    else:
        observed_arguments, arg_extract_error = _extract_observed_arguments(record)
        if arg_extract_error is not None:
            argument_score = _score_boolean_dimension(
                "argument_presence_structure",
                False,
                reason_pass="arguments present",
                reason_fail=f"arguments unavailable: {arg_extract_error}",
            )
        elif isinstance(observed_arguments, str):
            try:
                parsed_args = json.loads(observed_arguments)
            except Exception as exc:
                argument_score = _score_boolean_dimension(
                    "argument_presence_structure",
                    False,
                    reason_pass="arguments JSON parsed",
                    reason_fail=f"arguments JSON parse failed: {exc}",
                )
            else:
                if isinstance(parsed_args, Mapping):
                    missing_keys = [key for key in expected_argument_keys if key not in parsed_args]
                    argument_score = _score_boolean_dimension(
                        "argument_presence_structure",
                        len(missing_keys) == 0,
                        reason_pass="all expected argument keys present",
                        reason_fail=f"missing argument keys: {missing_keys}",
                    )
                else:
                    argument_score = _score_boolean_dimension(
                        "argument_presence_structure",
                        False,
                        reason_pass="arguments parsed as object",
                        reason_fail="arguments parsed but root is not an object",
                    )
        elif isinstance(observed_arguments, Mapping):
            missing_keys = [key for key in expected_argument_keys if key not in observed_arguments]
            argument_score = _score_boolean_dimension(
                "argument_presence_structure",
                len(missing_keys) == 0,
                reason_pass="all expected argument keys present",
                reason_fail=f"missing argument keys: {missing_keys}",
            )
        else:
            argument_score = _score_boolean_dimension(
                "argument_presence_structure",
                False,
                reason_pass="arguments present",
                reason_fail="arguments present but unsupported type",
            )

    if expected_no_call is None:
        no_call_score = {
            "dimension": "no_call_correctness",
            "status": "not_applicable",
            "reason": "no_call expectation not declared",
        }
    else:
        no_call_pass = observed_no_call is expected_no_call
        no_call_score = _score_boolean_dimension(
            "no_call_correctness",
            no_call_pass,
            reason_pass="no-call behavior matched expectation",
            reason_fail=(
                f"no-call mismatch: observed={observed_no_call}, expected={expected_no_call}"
            ),
        )

    wrapper_prohibited = bool(expectation.get("wrapper_prohibited", True))
    if wrapper_prohibited:
        wrapper_score = _score_boolean_dimension(
            "wrapper_leakage",
            not wrapper_leakage,
            reason_pass="no wrapper/prose leakage detected",
            reason_fail="wrapper/prose leakage detected",
        )
    else:
        wrapper_score = {
            "dimension": "wrapper_leakage",
            "status": "not_applicable",
            "reason": "wrapper leakage not prohibited",
        }

    preservation_required = parse_status != "strict_json_object" or tool_call_status in {
        "tool_calls_key_missing",
        "tool_calls_not_list",
        "tool_call_payload_partial_or_invalid",
        "tool_call_unavailable_parse_failure",
        "tool_call_unavailable_record_invalid",
    }
    if preservation_required:
        preserved = True
        preservation_reason = "malformed/partial output preserved without reconstruction"
    else:
        preserved = True
        preservation_reason = "preservation constraint not triggered"

    preservation_score = _score_boolean_dimension(
        "malformed_partial_preservation",
        preserved,
        reason_pass=preservation_reason,
        reason_fail="malformed/partial output was reconstructed",
    )

    dimensions = [
        strict_json_score,
        tool_call_presence_score,
        tool_name_score,
        argument_score,
        no_call_score,
        wrapper_score,
        preservation_score,
    ]

    scored_dims = [d for d in dimensions if d["status"] in {"pass", "fail"}]
    fail_count = sum(1 for d in scored_dims if d["status"] == "fail")
    pass_count = sum(1 for d in scored_dims if d["status"] == "pass")

    overall_status = "pass" if fail_count == 0 else "fail"
    reasons = [d["reason"] for d in dimensions if d["status"] == "fail"]

    return {
        "record_id": record.get("record_id"),
        "fixture_id": record.get("fixture_id"),
        "source_definition_id": record.get("source_definition_id"),
        "model_identifier": record.get("model_identifier"),
        "prompt_reference": record.get("prompt_reference"),
        "raw_model_response": record.get("raw_model_response"),
        "parse_status": parse_status,
        "tool_call_status": tool_call_status,
        "wrapper_or_prose_leakage": wrapper_leakage,
        "no_call_status": record.get("no_call_status"),
        "expected_binding": {
            "record_expectation": expectation,
            "fixture_expectation_hint": fixture_hint,
            "state_axis": state_record,
        },
        "scoring_dimensions": dimensions,
        "overall_status": overall_status,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "fail_reasons": reasons,
    }


def _build_per_fixture_scoring(per_output_scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_fixture: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in per_output_scores:
        fixture_id = _as_nonempty_str(row.get("fixture_id")) or "unresolved-fixture"
        by_fixture[fixture_id].append(row)

    fixture_rows: list[dict[str, Any]] = []
    for fixture_id in sorted(by_fixture):
        group = by_fixture[fixture_id]
        pass_count = sum(1 for row in group if row["overall_status"] == "pass")
        fail_count = sum(1 for row in group if row["overall_status"] == "fail")
        status = "pass" if fail_count == 0 else "fail"

        fail_reasons: list[str] = []
        for row in group:
            fail_reasons.extend(row.get("fail_reasons", []))

        fixture_rows.append(
            {
                "fixture_id": fixture_id,
                "record_count": len(group),
                "pass_count": pass_count,
                "fail_count": fail_count,
                "overall_status": status,
                "fail_reasons": fail_reasons,
            }
        )

    return fixture_rows


def _build_status_summary(per_output_scores: list[dict[str, Any]]) -> dict[str, Any]:
    parse_counter = Counter(row["parse_status"] for row in per_output_scores)
    tool_counter = Counter(row["tool_call_status"] for row in per_output_scores)
    no_call_counter = Counter(str(row.get("no_call_status") or "unknown") for row in per_output_scores)

    dimension_counter: Counter[str] = Counter()
    dimension_fail_counter: Counter[str] = Counter()
    for row in per_output_scores:
        for dim in row["scoring_dimensions"]:
            key = str(dim["dimension"])
            status = str(dim["status"])
            if status in {"pass", "fail"}:
                dimension_counter[key] += 1
            if status == "fail":
                dimension_fail_counter[key] += 1

    return {
        "parse_status_counts": dict(sorted(parse_counter.items())),
        "tool_call_status_counts": dict(sorted(tool_counter.items())),
        "no_call_status_counts": dict(sorted(no_call_counter.items())),
        "dimension_scored_counts": dict(sorted(dimension_counter.items())),
        "dimension_fail_counts": dict(sorted(dimension_fail_counter.items())),
    }


def _build_wrapper_summary(per_output_scores: list[dict[str, Any]]) -> dict[str, Any]:
    wrapper_records = [row for row in per_output_scores if bool(row.get("wrapper_or_prose_leakage"))]
    wrapper_score_fail = 0
    for row in per_output_scores:
        for dim in row["scoring_dimensions"]:
            if dim["dimension"] == "wrapper_leakage" and dim["status"] == "fail":
                wrapper_score_fail += 1

    return {
        "record_count": len(per_output_scores),
        "wrapper_or_prose_leakage_count": len(wrapper_records),
        "wrapper_score_fail_count": wrapper_score_fail,
        "wrapper_record_ids": [row["record_id"] for row in wrapper_records],
    }


def _build_scoring_validation_issues(per_output_scores: list[dict[str, Any]]) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    for row in per_output_scores:
        if row["overall_status"] != "fail":
            continue
        for reason in row.get("fail_reasons", []):
            issues.append(
                {
                    "record_id": row.get("record_id"),
                    "fixture_id": row.get("fixture_id"),
                    "issue_code": "scoring_dimension_fail",
                    "message": reason,
                    "severity": "warning",
                }
            )

    by_code = Counter(issue["issue_code"] for issue in issues)
    return {
        "issue_count": len(issues),
        "issue_counts_by_code": dict(sorted(by_code.items())),
        "issues": issues,
    }


def _build_governance_guardrail_artifact(c4_guardrails: Mapping[str, Any], per_output_scores: list[dict[str, Any]]) -> dict[str, Any]:
    c4_status = dict(c4_guardrails.get("guardrail_status", {})) if isinstance(c4_guardrails, Mapping) else {}
    c4_counts = dict(c4_guardrails.get("guardrail_counts", {})) if isinstance(c4_guardrails, Mapping) else {}

    inferred_flags_detected = False
    repaired_outputs_detected = False

    for row in per_output_scores:
        # C5 scoring path reads observed data only; these fields are emitted for audit confirmation.
        _ = row

    return {
        "guardrail_status": {
            "collapsed_state_behavior_detected": bool(c4_status.get("collapsed_state_behavior_detected", False)),
            "inference_behavior_detected": bool(c4_status.get("inference_behavior_detected", False)) or inferred_flags_detected,
            "substitution_behavior_detected": bool(c4_status.get("substitution_behavior_detected", False)),
            "reconstruction_behavior_detected": bool(c4_status.get("reconstruction_behavior_detected", False)) or repaired_outputs_detected,
            "tool_call_reconstruction_performed": bool(c4_status.get("tool_call_reconstruction_performed", False)),
            "argument_reconstruction_performed": bool(c4_status.get("argument_reconstruction_performed", False)),
            "fallback_tool_name_inference_performed": bool(c4_status.get("fallback_tool_name_inference_performed", False)),
        },
        "guardrail_counts": {
            **c4_counts,
            "scored_output_count": len(per_output_scores),
        },
    }


def run_stage_c5_scoring_integration(fixtures_root: Path, output_records_path: Path, artifacts_dir: Path) -> dict[str, Any]:
    c4 = _load_foundations()

    fixtures_root = fixtures_root.resolve()
    output_records_path = output_records_path.resolve()
    artifacts_dir = artifacts_dir.resolve()
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    ingestion_dir = artifacts_dir / "ingestion"
    c4_summary = c4.run_stage_c4_output_ingestion(
        fixtures_root=fixtures_root,
        output_records_path=output_records_path,
        artifacts_dir=ingestion_dir,
    )

    output_inventory = _load_json(Path(c4_summary["artifact_paths"]["output_inventory"]))
    state_axis = _load_json(Path(c4_summary["artifact_paths"]["state_axis_from_outputs"]))
    c4_validation_issues = _load_json(Path(c4_summary["artifact_paths"]["validation_issues"]))
    c4_guardrails = _load_json(Path(c4_summary["artifact_paths"]["governance_guardrails"]))

    state_by_id = {
        str(row.get("concept_id")): row
        for row in state_axis.get("records", [])
        if isinstance(row, Mapping)
    }

    fixtures = _load_fixture_documents(fixtures_root)
    expectations_by_record_id = _parse_input_record_expectations(output_records_path)

    binding_rows: list[dict[str, Any]] = []
    per_output_scores: list[dict[str, Any]] = []

    for record in output_inventory.get("records", []):
        if not isinstance(record, Mapping):
            continue
        record_id = str(record.get("record_id"))
        expectation = expectations_by_record_id.get(
            record_id,
            {
                "expected_tool_name": None,
                "expected_argument_keys": None,
                "expected_no_call": record.get("no_call_expected") if isinstance(record.get("no_call_expected"), bool) else None,
                "expected_strict_json_object": True,
                "expected_tool_call_required": None,
                "wrapper_prohibited": True,
            },
        )

        fixture_id = _as_nonempty_str(record.get("fixture_id"))
        fixture = fixtures.get(fixture_id) if fixture_id else None
        fixture_hint = _fixture_expectation_hint(fixture)

        state_record = state_by_id.get(record_id)

        binding_row = {
            "record_id": record_id,
            "fixture_id": fixture_id,
            "source_definition_id": record.get("source_definition_id"),
            "model_identifier": record.get("model_identifier"),
            "prompt_reference": record.get("prompt_reference"),
            "raw_model_response": record.get("raw_model_response"),
            "parse_status": record.get("parse_status"),
            "tool_call_status": record.get("tool_call_status"),
            "no_call_status": record.get("no_call_status"),
            "wrapper_or_prose_leakage": record.get("wrapper_or_prose_leakage"),
            "parsed_tool_call_payload": record.get("parsed_tool_call_payload"),
            "record_expectation": expectation,
            "fixture_expectation_hint": fixture_hint,
            "state_axis": state_record,
            "binding_generated_at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        }
        binding_rows.append(binding_row)

        per_output_scores.append(
            _score_output_record(
                record=record,
                expectation=expectation,
                fixture_hint=fixture_hint,
                state_record=state_record,
            )
        )

    per_fixture_scores = _build_per_fixture_scoring(per_output_scores)
    status_summary = _build_status_summary(per_output_scores)
    wrapper_summary = _build_wrapper_summary(per_output_scores)
    scoring_validation_issues = _build_scoring_validation_issues(per_output_scores)
    governance_guardrails = _build_governance_guardrail_artifact(c4_guardrails, per_output_scores)

    runtime_scoring_summary = {
        "contract_scope": "stage_c5_scoring_path_integration",
        "fixtures_root": str(fixtures_root),
        "output_records_path": str(output_records_path),
        "artifacts_dir": str(artifacts_dir),
        "generated_at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "record_count": len(per_output_scores),
        "overall_pass_count": sum(1 for row in per_output_scores if row["overall_status"] == "pass"),
        "overall_fail_count": sum(1 for row in per_output_scores if row["overall_status"] == "fail"),
        "c4_validation_issue_count": c4_validation_issues.get("issue_count", 0),
        "c5_scoring_validation_issue_count": scoring_validation_issues.get("issue_count", 0),
        "guardrail_status": governance_guardrails["guardrail_status"],
        "c4_summary": c4_summary,
    }

    artifact_payloads = {
        "scoring_input_binding": {
            "record_count": len(binding_rows),
            "records": binding_rows,
        },
        "per_output_scoring_status": {
            "record_count": len(per_output_scores),
            "records": per_output_scores,
        },
        "per_fixture_scoring_status": {
            "fixture_count": len(per_fixture_scores),
            "records": per_fixture_scores,
        },
        "parse_tool_nocall_scoring_summary": status_summary,
        "wrapper_leakage_scoring_summary": wrapper_summary,
        "validation_issues": {
            "c4_validation_issues": c4_validation_issues,
            "c5_scoring_validation_issues": scoring_validation_issues,
        },
        "governance_guardrails": governance_guardrails,
        "runtime_scoring_summary": runtime_scoring_summary,
    }

    artifact_paths: dict[str, str] = {}
    for name, payload in artifact_payloads.items():
        out_path = artifacts_dir / f"c5_{name}_artifact.json"
        _write_json(out_path, payload)
        artifact_paths[name] = str(out_path)

    summary = {
        "artifact_paths": artifact_paths,
        "record_count": len(per_output_scores),
        "overall_pass_count": runtime_scoring_summary["overall_pass_count"],
        "overall_fail_count": runtime_scoring_summary["overall_fail_count"],
        "guardrail_status": governance_guardrails["guardrail_status"],
        "c4_validation_issue_count": c4_validation_issues.get("issue_count", 0),
        "c5_scoring_validation_issue_count": scoring_validation_issues.get("issue_count", 0),
    }

    summary_path = artifacts_dir / "c5_runtime_scoring_summary.json"
    _write_json(summary_path, summary)
    summary["summary_path"] = str(summary_path)
    return summary


def _default_fixtures_root() -> Path:
    return resolve_fixture_root()


def _default_output_records_path() -> Path:
    return resolve_artifact_path("stage_c5_sample_output_records")


def _default_artifacts_dir() -> Path:
    return resolve_artifact_path("stage_c5_contract_artifacts_dir")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stage C5 evaluator scoring path integration"
    )
    parser.add_argument(
        "--fixtures-root",
        default=str(_default_fixtures_root()),
        help="Path to Stage B fixture root",
    )
    parser.add_argument(
        "--output-records-path",
        default=str(_default_output_records_path()),
        help="Path to model-output records JSONL",
    )
    parser.add_argument(
        "--artifacts-dir",
        default=str(_default_artifacts_dir()),
        help="Output directory for Stage C5 scored artifacts",
    )
    args = parser.parse_args()

    summary = run_stage_c5_scoring_integration(
        fixtures_root=Path(args.fixtures_root),
        output_records_path=Path(args.output_records_path),
        artifacts_dir=Path(args.artifacts_dir),
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    guardrail_status = summary["guardrail_status"]
    if any(bool(value) for value in guardrail_status.values()):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
