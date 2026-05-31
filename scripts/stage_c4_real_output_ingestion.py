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


class OutputIngestionError(RuntimeError):
    """Raised when Stage C4 output ingestion cannot proceed."""


@dataclass(frozen=True)
class FixtureDocument:
    path: Path
    payload: dict[str, Any]


def _load_module(module_path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, str(module_path))
    if spec is None or spec.loader is None:
        raise OutputIngestionError(f"unable to load module at {module_path}")
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
    c3 = _load_module(scripts_dir / "stage_c3_evaluator_runtime_integration.py", "stage_c3_evaluator_runtime_integration")
    return c1, c2, c3


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _as_nonempty_str(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _load_fixture_documents(fixtures_root: Path) -> list[FixtureDocument]:
    docs: list[FixtureDocument] = []
    for path in sorted(fixtures_root.rglob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise OutputIngestionError(f"fixture root must be object: {path}")
        docs.append(FixtureDocument(path=path, payload=payload))
    return docs


def _build_fixture_indexes(fixtures: list[FixtureDocument]) -> tuple[dict[str, FixtureDocument], dict[str, FixtureDocument]]:
    by_fixture_id: dict[str, FixtureDocument] = {}
    by_source_definition_id: dict[str, FixtureDocument] = {}

    for doc in fixtures:
        fixture_id = _as_nonempty_str(doc.payload.get("fixture_id"))
        source_definition_id = _as_nonempty_str(doc.payload.get("source_definition_id"))
        if fixture_id and fixture_id not in by_fixture_id:
            by_fixture_id[fixture_id] = doc
        if source_definition_id and source_definition_id not in by_source_definition_id:
            by_source_definition_id[source_definition_id] = doc

    return by_fixture_id, by_source_definition_id


def _normalize_raw_response(value: Any) -> tuple[str, bool]:
    if isinstance(value, str):
        return value, False
    return json.dumps(value, ensure_ascii=False, sort_keys=True), True


def _parse_raw_model_response(raw_model_response: str) -> dict[str, Any]:
    stripped = raw_model_response.strip()
    if not stripped:
        return {
            "parse_status": "empty_output",
            "strict_json_object": False,
            "parsed_root": None,
            "parse_error": "empty output",
            "wrapper_or_prose_leakage": False,
            "embedded_payload_candidate": None,
        }

    try:
        parsed = json.loads(stripped)
    except Exception as exc:
        first = stripped.find("{")
        last = stripped.rfind("}")
        if first >= 0 and last > first:
            candidate_text = stripped[first : last + 1]
            try:
                candidate = json.loads(candidate_text)
            except Exception:
                candidate = None
            if isinstance(candidate, dict):
                return {
                    "parse_status": "invalid_json_with_embedded_object",
                    "strict_json_object": False,
                    "parsed_root": None,
                    "parse_error": str(exc),
                    "wrapper_or_prose_leakage": True,
                    "embedded_payload_candidate": candidate,
                }
        return {
            "parse_status": "invalid_json",
            "strict_json_object": False,
            "parsed_root": None,
            "parse_error": str(exc),
            "wrapper_or_prose_leakage": False,
            "embedded_payload_candidate": None,
        }

    if isinstance(parsed, dict):
        return {
            "parse_status": "strict_json_object",
            "strict_json_object": True,
            "parsed_root": parsed,
            "parse_error": None,
            "wrapper_or_prose_leakage": False,
            "embedded_payload_candidate": None,
        }

    return {
        "parse_status": "strict_json_non_object",
        "strict_json_object": False,
        "parsed_root": parsed,
        "parse_error": "strict JSON root is not an object",
        "wrapper_or_prose_leakage": False,
        "embedded_payload_candidate": None,
    }


def _inspect_tool_call_status(parsed_root: Any) -> dict[str, Any]:
    if not isinstance(parsed_root, dict):
        return {
            "tool_call_status": "tool_call_unavailable_parse_failure",
            "parsed_tool_call_payload": None,
            "no_call_emitted": None,
            "tool_call_entry_issue_count": 0,
        }

    if "tool_calls" not in parsed_root:
        return {
            "tool_call_status": "tool_calls_key_missing",
            "parsed_tool_call_payload": None,
            "no_call_emitted": None,
            "tool_call_entry_issue_count": 0,
        }

    tool_calls = parsed_root.get("tool_calls")
    if not isinstance(tool_calls, list):
        return {
            "tool_call_status": "tool_calls_not_list",
            "parsed_tool_call_payload": {"tool_calls": tool_calls},
            "no_call_emitted": None,
            "tool_call_entry_issue_count": 1,
        }

    if len(tool_calls) == 0:
        return {
            "tool_call_status": "no_tool_calls_emitted",
            "parsed_tool_call_payload": {"tool_calls": []},
            "no_call_emitted": True,
            "tool_call_entry_issue_count": 0,
        }

    entry_issues = 0
    for call in tool_calls:
        if not isinstance(call, dict):
            entry_issues += 1
            continue
        function_block = call.get("function")
        if not isinstance(function_block, dict):
            entry_issues += 1
            continue
        name = function_block.get("name")
        if not isinstance(name, str) or not name.strip():
            entry_issues += 1
        if "arguments" not in function_block:
            entry_issues += 1

    status = "tool_call_payload_present" if entry_issues == 0 else "tool_call_payload_partial_or_invalid"
    return {
        "tool_call_status": status,
        "parsed_tool_call_payload": {"tool_calls": tool_calls},
        "no_call_emitted": False,
        "tool_call_entry_issue_count": entry_issues,
    }


def _derive_no_call_status(no_call_expected: bool | None, no_call_emitted: bool | None) -> str:
    if no_call_expected is None:
        return "no_call_expectation_not_declared"
    if no_call_emitted is None:
        return "no_call_emission_unknown"
    if no_call_expected and no_call_emitted:
        return "expected_no_call_emitted"
    if no_call_expected and not no_call_emitted:
        return "expected_no_call_not_emitted"
    if not no_call_expected and no_call_emitted:
        return "unexpected_no_call_emitted"
    return "tool_call_emitted"


def _row_fact_payload_from_output(c1, now_utc: str, record: Mapping[str, Any], matched_fixture: FixtureDocument | None) -> dict[str, Any]:
    ownership_map: Mapping[str, Any] = {}
    if matched_fixture is not None:
        candidate = matched_fixture.payload.get("ownership_expectations")
        if isinstance(candidate, Mapping):
            ownership_map = candidate

    evidence_digest = hashlib.sha256(str(record.get("raw_model_response") or "").encode("utf-8")).hexdigest()

    return {
        "row_id": str(record["record_id"]),
        "split_id": "all_splits",
        "excluded": False,
        "expected_tool_name": _as_nonempty_str(record.get("expected_tool_name")),
        "membership_markers": {
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
            "row_source": "stage_c4_output_ingestion",
            "dataset_id": "stage_c4_model_output_records",
            "dataset_version": "contract-baseline",
            "extraction_timestamp_utc": now_utc,
            "evidence_digest": evidence_digest,
        },
        "denominator_provenance": {
            "eligible_population_source": "stage_c4_output_record_population",
            "non_exact_population_source": "stage_c4_output_record_population",
            "read_file_population_source": None,
            "symbol_name_population_source": None,
            "anchor_population_source": None,
            "no_anchor_population_source": None,
        },
        "evidence": {
            "fixture_reference": record.get("fixture_id"),
            "source_definition_reference": record.get("source_definition_id"),
            "model_identifier": record.get("model_identifier"),
            "prompt_reference": record.get("prompt_reference"),
            "parse_status": record.get("parse_status"),
            "tool_call_status": record.get("tool_call_status"),
            "raw_model_response": record.get("raw_model_response"),
            "wrapper_or_prose_leakage": record.get("wrapper_or_prose_leakage"),
            "guardrail_flags": {
                "inference_used": False,
                "substitution_used": False,
                "reconstruction_used": False,
            },
        },
    }


def _ingest_output_records(
    output_records_path: Path,
    fixture_by_id: Mapping[str, FixtureDocument],
    fixture_by_source_definition_id: Mapping[str, FixtureDocument],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    ingested: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []

    lines = output_records_path.read_text(encoding="utf-8").splitlines()
    for line_no, line in enumerate(lines, start=1):
        raw_line = line.rstrip("\n")
        if not raw_line.strip():
            continue

        line_issue_prefix = {
            "line_number": line_no,
            "record_id": f"line-{line_no}",
            "severity": "error",
        }

        try:
            row = json.loads(raw_line)
        except Exception as exc:
            issues.append(
                {
                    **line_issue_prefix,
                    "issue_code": "invalid_json_line",
                    "message": str(exc),
                    "raw_line": raw_line,
                }
            )
            ingested.append(
                {
                    "record_id": f"line-{line_no}",
                    "line_number": line_no,
                    "fixture_id": None,
                    "source_definition_id": None,
                    "model_identifier": None,
                    "prompt_reference": None,
                    "raw_model_response": raw_line,
                    "raw_response_mutated": False,
                    "parse_status": "record_json_invalid",
                    "parse_error": str(exc),
                    "parsed_tool_call_payload": None,
                    "embedded_payload_candidate": None,
                    "tool_call_status": "tool_call_unavailable_record_invalid",
                    "tool_call_entry_issue_count": 0,
                    "wrapper_or_prose_leakage": False,
                    "no_call_expected": None,
                    "no_call_emitted": None,
                    "no_call_status": "no_call_emission_unknown",
                    "contract_valid": False,
                    "contract_issues": ["invalid_json_line"],
                    "matched_fixture": None,
                    "evidence_provenance": {
                        "source_path": str(output_records_path),
                        "line_number": line_no,
                        "captured_at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                    },
                }
            )
            continue

        contract_issues: list[str] = []
        if not isinstance(row, dict):
            contract_issues.append("record_not_object")
            row = {"raw_record": row}

        record_id = _as_nonempty_str(row.get("record_id")) or f"line-{line_no}"
        fixture_id = _as_nonempty_str(row.get("fixture_id"))
        source_definition_id = _as_nonempty_str(row.get("source_definition_id"))
        model_identifier = _as_nonempty_str(row.get("model_identifier"))
        prompt_reference = _as_nonempty_str(row.get("prompt_reference") or row.get("input_reference"))

        if not fixture_id and not source_definition_id:
            contract_issues.append("missing_fixture_and_source_definition_reference")
        if not model_identifier:
            contract_issues.append("missing_model_identifier")
        if not prompt_reference:
            contract_issues.append("missing_prompt_or_input_reference")
        if "raw_model_response" not in row:
            contract_issues.append("missing_raw_model_response")

        raw_response_value = row.get("raw_model_response", "")
        normalized_raw_response, mutated_raw_response = _normalize_raw_response(raw_response_value)
        if mutated_raw_response:
            contract_issues.append("raw_model_response_not_string")

        matched_fixture = None
        if fixture_id and fixture_id in fixture_by_id:
            matched_fixture = fixture_by_id[fixture_id]
        elif source_definition_id and source_definition_id in fixture_by_source_definition_id:
            matched_fixture = fixture_by_source_definition_id[source_definition_id]
        else:
            contract_issues.append("fixture_reference_unresolved")

        parse_info = _parse_raw_model_response(normalized_raw_response)
        tool_info = _inspect_tool_call_status(parse_info.get("parsed_root"))

        no_call_expected = row.get("no_call_expected")
        if no_call_expected is not None and not isinstance(no_call_expected, bool):
            contract_issues.append("no_call_expected_not_bool")
            no_call_expected = None

        no_call_status = _derive_no_call_status(no_call_expected, tool_info["no_call_emitted"])

        if parse_info["parse_status"] != "strict_json_object":
            issues.append(
                {
                    "line_number": line_no,
                    "record_id": record_id,
                    "severity": "warning",
                    "issue_code": "parse_status_non_strict_object",
                    "message": f"parse status is {parse_info['parse_status']}",
                }
            )

        if tool_info["tool_call_status"] in {
            "tool_calls_key_missing",
            "tool_calls_not_list",
            "tool_call_payload_partial_or_invalid",
            "tool_call_unavailable_parse_failure",
        }:
            issues.append(
                {
                    "line_number": line_no,
                    "record_id": record_id,
                    "severity": "warning",
                    "issue_code": "tool_call_status_not_clean",
                    "message": f"tool_call_status={tool_info['tool_call_status']}",
                }
            )

        for issue_code in contract_issues:
            issues.append(
                {
                    "line_number": line_no,
                    "record_id": record_id,
                    "severity": "error",
                    "issue_code": issue_code,
                    "message": issue_code,
                }
            )

        ingested.append(
            {
                "record_id": record_id,
                "line_number": line_no,
                "fixture_id": fixture_id,
                "source_definition_id": source_definition_id,
                "model_identifier": model_identifier,
                "prompt_reference": prompt_reference,
                "raw_model_response": normalized_raw_response,
                "raw_response_mutated": mutated_raw_response,
                "parse_status": parse_info["parse_status"],
                "parse_error": parse_info["parse_error"],
                "parsed_tool_call_payload": tool_info["parsed_tool_call_payload"],
                "embedded_payload_candidate": parse_info["embedded_payload_candidate"],
                "tool_call_status": tool_info["tool_call_status"],
                "tool_call_entry_issue_count": tool_info["tool_call_entry_issue_count"],
                "wrapper_or_prose_leakage": bool(parse_info["wrapper_or_prose_leakage"]),
                "no_call_expected": no_call_expected,
                "no_call_emitted": tool_info["no_call_emitted"],
                "no_call_status": no_call_status,
                "contract_valid": len(contract_issues) == 0,
                "contract_issues": contract_issues,
                "matched_fixture": str(matched_fixture.path) if matched_fixture else None,
                "evidence_provenance": {
                    "source_path": str(output_records_path),
                    "line_number": line_no,
                    "captured_at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                    "record_metadata": row.get("evidence_provenance") if isinstance(row.get("evidence_provenance"), dict) else {},
                },
            }
        )

    return ingested, issues


def _build_state_axis_from_outputs(c2, ingested_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    state_records: list[dict[str, Any]] = []
    for record in ingested_records:
        required_evidence_fields = (
            "record_reference",
            "model_identifier",
            "prompt_reference",
            "raw_model_response",
            "parse_status",
            "tool_call_status",
        )

        present_evidence_fields = tuple(
            field
            for field, value in (
                ("record_reference", record.get("record_id")),
                ("model_identifier", record.get("model_identifier")),
                ("prompt_reference", record.get("prompt_reference")),
                ("raw_model_response", record.get("raw_model_response")),
                ("parse_status", record.get("parse_status")),
                ("tool_call_status", record.get("tool_call_status")),
            )
            if value not in (None, "")
        )

        explicit_reasons: list[str] = []
        parse_status = str(record.get("parse_status") or "")
        if parse_status != "strict_json_object":
            explicit_reasons.append(f"parse status is {parse_status}")

        tool_call_status = str(record.get("tool_call_status") or "")
        if tool_call_status in {
            "tool_calls_key_missing",
            "tool_calls_not_list",
            "tool_call_payload_partial_or_invalid",
            "tool_call_unavailable_parse_failure",
            "tool_call_unavailable_record_invalid",
        }:
            explicit_reasons.append(f"tool call status is {tool_call_status}")

        if not bool(record.get("contract_valid")):
            explicit_reasons.append("model-output record contract violation")

        state_record = c2.evaluate_concept_state(
            c2.StateEvaluationInput(
                concept_id=str(record.get("record_id")),
                required_evidence_fields=required_evidence_fields,
                present_evidence_fields=present_evidence_fields,
                explicit_noncomputability_reasons=tuple(explicit_reasons),
                declared_comparability=c2.ComparabilityState.BLOCKED,
                comparison_block_reasons=(
                    "comparability baseline not enabled for stage c4 output ingestion",
                ),
            )
        )
        state_records.append(state_record.to_dict())

    return state_records


def _build_output_aggregation(c2, ingested_records: list[dict[str, Any]], state_records: list[dict[str, Any]], fixture_by_id: Mapping[str, FixtureDocument], fixture_by_source_definition_id: Mapping[str, FixtureDocument]) -> list[dict[str, Any]]:
    state_by_id = {str(state["concept_id"]): state for state in state_records}
    by_family: dict[str, list[Any]] = defaultdict(list)

    for record in ingested_records:
        matched_fixture = None
        fixture_id = _as_nonempty_str(record.get("fixture_id"))
        source_definition_id = _as_nonempty_str(record.get("source_definition_id"))
        if fixture_id and fixture_id in fixture_by_id:
            matched_fixture = fixture_by_id[fixture_id]
        elif source_definition_id and source_definition_id in fixture_by_source_definition_id:
            matched_fixture = fixture_by_source_definition_id[source_definition_id]

        if matched_fixture is not None:
            family_id = _as_nonempty_str(matched_fixture.payload.get("family")) or "Unspecified family scope"
            concept_id = _as_nonempty_str(matched_fixture.payload.get("governed_concept")) or str(
                matched_fixture.payload.get("source_definition_id") or record.get("record_id")
            )
            sub_slice_id = _as_nonempty_str(matched_fixture.payload.get("intended_subtype")) or _as_nonempty_str(
                matched_fixture.payload.get("intended_subslice_or_state")
            )
        else:
            family_id = "Unresolved fixture scope"
            concept_id = str(record.get("source_definition_id") or record.get("record_id"))
            sub_slice_id = None

        state = state_by_id.get(str(record.get("record_id")), {})
        counted = state.get("current_run_computability") == c2.CurrentRunComputabilityState.COMPUTABLE.value

        row = c2.build_aggregation_row(
            {
                "family_id": family_id,
                "concept_id": concept_id,
                "row_id": str(record.get("record_id")),
                "split_id": "all_splits",
                "sub_slice_id": sub_slice_id,
                "eligible": True,
                "counted": bool(counted),
                "excluded": False,
                "provenance_ref": str(record.get("evidence_provenance", {}).get("source_path") or "stage_c4_output_records"),
                "evidence_ref": str(record.get("record_id")),
            }
        )
        by_family[family_id].append(row)

    reports: list[dict[str, Any]] = []
    for family_id in sorted(by_family):
        report = c2.aggregate_family_rows(family_id, by_family[family_id])
        reports.append(report.to_dict())

    return reports


def _build_output_reconciliation(c2, ingested_records: list[dict[str, Any]], state_records: list[dict[str, Any]], aggregation_reports: list[dict[str, Any]]) -> dict[str, Any]:
    total_records = len(ingested_records)
    parse_status_counts = Counter(str(record.get("parse_status") or "unknown") for record in ingested_records)

    strict_object_count = parse_status_counts.get("strict_json_object", 0)
    non_strict_count = total_records - strict_object_count

    state_by_id = {str(state["concept_id"]): state for state in state_records}
    computable_count = sum(
        1
        for record in ingested_records
        if state_by_id.get(str(record.get("record_id")), {}).get("current_run_computability")
        == c2.CurrentRunComputabilityState.COMPUTABLE.value
    )

    tool_status_counts = Counter(str(record.get("tool_call_status") or "unknown") for record in ingested_records)
    tool_labels = sorted(tool_status_counts.keys())
    tool_denominators = [tool_status_counts[label] for label in tool_labels]
    tool_numerators = [
        sum(
            1
            for record in ingested_records
            if str(record.get("tool_call_status") or "") == label
            and state_by_id.get(str(record.get("record_id")), {}).get("current_run_computability")
            == c2.CurrentRunComputabilityState.COMPUTABLE.value
        )
        for label in tool_labels
    ]

    family_counts = [int(report["total_rows"]) for report in aggregation_reports]
    family_labels = [str(report["family_id"]) for report in aggregation_reports]

    valid_count = sum(1 for record in ingested_records if bool(record.get("contract_valid")))
    invalid_count = total_records - valid_count

    checks = [
        c2.validate_denominator_partition(
            {
                "check_id": "output_parse_status_partition",
                "parent_denominator": total_records,
                "partition_denominators": [strict_object_count, non_strict_count],
                "partition_labels": ["strict_json_object", "non_strict_or_invalid_json"],
            }
        ),
        c2.validate_parent_subslice_boundary(
            {
                "check_id": "output_tool_status_computability_boundary",
                "parent_numerator": computable_count,
                "parent_denominator": total_records,
                "subslice_numerators": tool_numerators,
                "subslice_denominators": tool_denominators,
                "subslice_labels": tool_labels,
            }
        ),
        c2.validate_split_to_aggregate(
            {
                "check_id": "output_family_split_to_aggregate",
                "aggregate_numerator": total_records,
                "aggregate_denominator": total_records,
                "split_numerators": family_counts,
                "split_denominators": family_counts,
                "split_labels": family_labels,
            }
        ),
        c2.validate_coverage_arithmetic(
            {
                "check_id": "output_contract_coverage_arithmetic",
                "covered_count": valid_count,
                "uncovered_count": invalid_count,
                "total_count": total_records,
            }
        ),
    ]
    return c2.build_reconciliation_report(checks).to_dict()


def _build_validation_issue_artifact(issues: list[dict[str, Any]]) -> dict[str, Any]:
    by_code = Counter(str(issue.get("issue_code") or "unknown") for issue in issues)
    by_severity = Counter(str(issue.get("severity") or "unknown") for issue in issues)
    return {
        "issue_count": len(issues),
        "issue_counts_by_code": dict(sorted(by_code.items())),
        "issue_counts_by_severity": dict(sorted(by_severity.items())),
        "issues": issues,
    }


def _build_governance_guardrail_artifact(ingested_records: list[dict[str, Any]], validation_issue_artifact: dict[str, Any], state_records: list[dict[str, Any]]) -> dict[str, Any]:
    wrapper_count = sum(1 for r in ingested_records if bool(r.get("wrapper_or_prose_leakage")))
    parse_failure_count = sum(1 for r in ingested_records if str(r.get("parse_status")) != "strict_json_object")
    mutated_raw_count = sum(1 for r in ingested_records if bool(r.get("raw_response_mutated")))
    partial_tool_payload_count = sum(
        1 for r in ingested_records if str(r.get("tool_call_status")) == "tool_call_payload_partial_or_invalid"
    )

    collapsed_state_detected = any("state" in record or "combined_state" in record for record in state_records)

    return {
        "guardrail_status": {
            "collapsed_state_behavior_detected": collapsed_state_detected,
            "inference_behavior_detected": False,
            "substitution_behavior_detected": False,
            "reconstruction_behavior_detected": False,
            "tool_call_reconstruction_performed": False,
            "argument_reconstruction_performed": False,
            "fallback_tool_name_inference_performed": False,
        },
        "guardrail_counts": {
            "record_count": len(ingested_records),
            "parse_failure_count": parse_failure_count,
            "wrapper_or_prose_leakage_count": wrapper_count,
            "partial_tool_payload_count": partial_tool_payload_count,
            "raw_response_mutated_count": mutated_raw_count,
            "validation_issue_count": int(validation_issue_artifact.get("issue_count", 0)),
        },
    }


def _build_output_inventory_artifact(ingested_records: list[dict[str, Any]]) -> dict[str, Any]:
    model_counts = Counter(_as_nonempty_str(r.get("model_identifier")) or "unknown_model" for r in ingested_records)
    parse_counts = Counter(str(r.get("parse_status") or "unknown") for r in ingested_records)
    tool_status_counts = Counter(str(r.get("tool_call_status") or "unknown") for r in ingested_records)
    no_call_status_counts = Counter(str(r.get("no_call_status") or "unknown") for r in ingested_records)

    return {
        "record_count": len(ingested_records),
        "model_identifier_counts": dict(sorted(model_counts.items())),
        "parse_status_counts": dict(sorted(parse_counts.items())),
        "tool_call_status_counts": dict(sorted(tool_status_counts.items())),
        "no_call_status_counts": dict(sorted(no_call_status_counts.items())),
        "records": ingested_records,
    }


def _build_parse_toolcall_status_artifact(ingested_records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "record_count": len(ingested_records),
        "records": [
            {
                "record_id": record.get("record_id"),
                "line_number": record.get("line_number"),
                "fixture_id": record.get("fixture_id"),
                "source_definition_id": record.get("source_definition_id"),
                "parse_status": record.get("parse_status"),
                "parse_error": record.get("parse_error"),
                "tool_call_status": record.get("tool_call_status"),
                "tool_call_entry_issue_count": record.get("tool_call_entry_issue_count"),
                "wrapper_or_prose_leakage": record.get("wrapper_or_prose_leakage"),
                "no_call_expected": record.get("no_call_expected"),
                "no_call_emitted": record.get("no_call_emitted"),
                "no_call_status": record.get("no_call_status"),
            }
            for record in ingested_records
        ],
    }


def run_stage_c4_output_ingestion(
    fixtures_root: Path,
    output_records_path: Path,
    artifacts_dir: Path,
) -> dict[str, Any]:
    c1, c2, c3 = _load_foundations()

    fixtures_root = fixtures_root.resolve()
    output_records_path = output_records_path.resolve()
    artifacts_dir = artifacts_dir.resolve()
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    fixture_baseline_dir = artifacts_dir / "fixture_baseline"
    fixture_baseline_summary = c3.run_stage_c3_runtime_integration(fixtures_root, fixture_baseline_dir)

    fixtures = _load_fixture_documents(fixtures_root)
    fixture_by_id, fixture_by_source_definition_id = _build_fixture_indexes(fixtures)

    ingested_records, issues = _ingest_output_records(
        output_records_path=output_records_path,
        fixture_by_id=fixture_by_id,
        fixture_by_source_definition_id=fixture_by_source_definition_id,
    )

    now_utc = datetime.now(UTC).isoformat().replace("+00:00", "Z")

    row_fact_records: list[dict[str, Any]] = []
    for record in ingested_records:
        matched_fixture = None
        fixture_id = _as_nonempty_str(record.get("fixture_id"))
        source_definition_id = _as_nonempty_str(record.get("source_definition_id"))
        if fixture_id and fixture_id in fixture_by_id:
            matched_fixture = fixture_by_id[fixture_id]
        elif source_definition_id and source_definition_id in fixture_by_source_definition_id:
            matched_fixture = fixture_by_source_definition_id[source_definition_id]

        row_fact = c1.build_row_fact_record(
            _row_fact_payload_from_output(c1, now_utc, record, matched_fixture)
        )
        row_fact_records.append(row_fact.to_dict())

    state_records = _build_state_axis_from_outputs(c2, ingested_records)
    aggregation_reports = _build_output_aggregation(
        c2,
        ingested_records,
        state_records,
        fixture_by_id,
        fixture_by_source_definition_id,
    )
    reconciliation_report = _build_output_reconciliation(c2, ingested_records, state_records, aggregation_reports)

    output_inventory = _build_output_inventory_artifact(ingested_records)
    parse_toolcall_status = _build_parse_toolcall_status_artifact(ingested_records)
    validation_issues = _build_validation_issue_artifact(issues)
    governance_guardrails = _build_governance_guardrail_artifact(ingested_records, validation_issues, state_records)

    artifact_payloads = {
        "output_inventory": output_inventory,
        "parse_toolcall_status": parse_toolcall_status,
        "row_fact_metadata": {
            "row_fact_count": len(row_fact_records),
            "records": row_fact_records,
        },
        "state_axis_from_outputs": {
            "record_count": len(state_records),
            "records": state_records,
        },
        "aggregation_summary_from_outputs": {
            "family_report_count": len(aggregation_reports),
            "family_reports": aggregation_reports,
        },
        "reconciliation_summary_from_outputs": reconciliation_report,
        "validation_issues": validation_issues,
        "governance_guardrails": governance_guardrails,
        "runtime_contract_summary": {
            "contract_scope": "stage_c4_real_output_ingestion_baseline",
            "fixtures_root": str(fixtures_root),
            "output_records_path": str(output_records_path),
            "artifacts_dir": str(artifacts_dir),
            "generated_at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "record_count": len(ingested_records),
            "validation_issue_count": validation_issues["issue_count"],
            "reconciliation_fail_count": reconciliation_report["fail_count"],
            "guardrail_status": governance_guardrails["guardrail_status"],
            "fixture_baseline_summary": fixture_baseline_summary,
        },
    }

    artifact_paths: dict[str, str] = {}
    for name, payload in artifact_payloads.items():
        out_path = artifacts_dir / f"c4_{name}_artifact.json"
        _write_json(out_path, payload)
        artifact_paths[name] = str(out_path)

    summary = {
        "artifact_paths": artifact_paths,
        "record_count": len(ingested_records),
        "validation_issue_count": validation_issues["issue_count"],
        "reconciliation_fail_count": reconciliation_report["fail_count"],
        "reconciliation_blocked_count": reconciliation_report["blocked_count"],
        "guardrail_status": governance_guardrails["guardrail_status"],
    }

    summary_path = artifacts_dir / "c4_runtime_integration_summary.json"
    _write_json(summary_path, summary)
    summary["summary_path"] = str(summary_path)
    return summary


def _default_fixtures_root() -> Path:
    return Path("/opt/ai-stack/assistant-training/manifests/reports/stage_b_wp8_validation/fixtures")


def _default_output_records_path() -> Path:
    return Path("/opt/ai-stack/assistant-training/reports/stage_c4/input/stage_c4_sample_output_records.jsonl")


def _default_artifacts_dir() -> Path:
    return Path("/opt/ai-stack/assistant-training/reports/stage_c4/contract_artifacts")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stage C4 real-output ingestion and contract artifact population"
    )
    parser.add_argument(
        "--fixtures-root",
        default=str(_default_fixtures_root()),
        help="Path to Stage B fixture root",
    )
    parser.add_argument(
        "--output-records-path",
        default=str(_default_output_records_path()),
        help="Path to model-output record JSONL",
    )
    parser.add_argument(
        "--artifacts-dir",
        default=str(_default_artifacts_dir()),
        help="Output directory for Stage C4 artifacts",
    )
    args = parser.parse_args()

    summary = run_stage_c4_output_ingestion(
        fixtures_root=Path(args.fixtures_root),
        output_records_path=Path(args.output_records_path),
        artifacts_dir=Path(args.artifacts_dir),
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    if summary["reconciliation_fail_count"] > 0:
        return 1

    guardrails = summary["guardrail_status"]
    if any(bool(value) for value in guardrails.values()):
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
