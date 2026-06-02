#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping


class StageC8ProjectionError(RuntimeError):
    """Raised when Stage C8 projection adapter execution cannot proceed."""


def _load_module(module_path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, str(module_path))
    if spec is None or spec.loader is None:
        raise StageC8ProjectionError(f"unable to load module at {module_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_stage_c6():
    scripts_dir = Path(__file__).resolve().parent
    return _load_module(scripts_dir / "stage_c6_scoring_report_integration.py", "stage_c6_scoring_report_integration")


def _load_detector():
    scripts_dir = Path(__file__).resolve().parent
    return _load_module(scripts_dir / "post_eval_collapse_detector.py", "post_eval_collapse_detector")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        raw = line.strip()
        if not raw:
            continue
        try:
            row = json.loads(raw)
        except Exception as exc:  # pragma: no cover - upstream ingestion validates parse failures.
            raise StageC8ProjectionError(f"unable to parse JSONL row {line_no} from {path}: {exc}") from exc
        if isinstance(row, dict):
            records.append(row)
    return records


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _set_nested_value(root: dict[str, Any], path: str, value: Any) -> None:
    parts = [segment for segment in path.split(".") if segment]
    if not parts:
        raise StageC8ProjectionError("nested-path cannot be empty")

    cursor: dict[str, Any] = root
    for part in parts[:-1]:
        next_node = cursor.get(part)
        if not isinstance(next_node, dict):
            next_node = {}
            cursor[part] = next_node
        cursor = next_node
    cursor[parts[-1]] = value


def _safe_rate(numerator: float, denominator: float) -> float | None:
    if denominator <= 0:
        return None
    return float(numerator) / float(denominator)


def _as_float_or_none(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        out = float(value)
        if out == float("inf") or out == float("-inf"):
            return None
        if out != out:
            return None
        return out
    return None


def _as_bool_or_none(value: Any) -> bool | None:
    return value if isinstance(value, bool) else None


def _as_nonempty_str(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _nested_mapping(root: Mapping[str, Any], *keys: str) -> Mapping[str, Any] | None:
    cursor: Any = root
    for key in keys:
        if not isinstance(cursor, Mapping):
            return None
        cursor = cursor.get(key)
    return cursor if isinstance(cursor, Mapping) else None


def _find_family_concept(
    aggregation_payload: Mapping[str, Any],
    *,
    family_id: str,
    concept_id: str,
) -> Mapping[str, Any] | None:
    family_reports = aggregation_payload.get("family_reports")
    if not isinstance(family_reports, list):
        return None

    for family in family_reports:
        if not isinstance(family, Mapping):
            continue
        if str(family.get("family_id")) != family_id:
            continue
        concept_summaries = family.get("concept_summaries")
        if not isinstance(concept_summaries, list):
            continue
        for concept in concept_summaries:
            if isinstance(concept, Mapping) and str(concept.get("concept_id")) == concept_id:
                return concept
    return None


def _build_no_call_correctness_aggregate(parse_tool_summary: Mapping[str, Any]) -> tuple[float | None, dict[str, Any]]:
    dimension_scored = parse_tool_summary.get("dimension_scored_counts", {})
    dimension_failed = parse_tool_summary.get("dimension_fail_counts", {})
    if not isinstance(dimension_scored, Mapping) or not isinstance(dimension_failed, Mapping):
        return None, {
            "reason_code": "source_summary_missing_dimension_counts",
            "details": "parse/tool/no-call summary is missing dimension count maps",
        }

    scored = _as_float_or_none(dimension_scored.get("no_call_correctness"))
    failed = _as_float_or_none(dimension_failed.get("no_call_correctness")) or 0.0
    if scored is None or scored <= 0:
        return None, {
            "reason_code": "source_summary_missing_no_call_correctness_counts",
            "details": "no_call_correctness scored count is missing or zero",
        }

    passed = scored - failed
    if passed < 0:
        return None, {
            "reason_code": "source_summary_inconsistent_no_call_correctness_counts",
            "details": f"passed count would be negative (scored={scored}, failed={failed})",
        }

    rate = _safe_rate(passed, scored)
    return rate, {
        "numerator": passed,
        "denominator": scored,
        "failed_count": failed,
    }


def _build_wrapper_leakage_overall(wrapper_summary: Mapping[str, Any]) -> tuple[float | None, dict[str, Any]]:
    record_count = _as_float_or_none(wrapper_summary.get("record_count"))
    leakage_count = _as_float_or_none(wrapper_summary.get("wrapper_or_prose_leakage_count"))
    if record_count is None or leakage_count is None:
        return None, {
            "reason_code": "source_summary_missing_wrapper_counts",
            "details": "wrapper summary missing record or leakage count",
        }
    rate = _safe_rate(leakage_count, record_count)
    if rate is None:
        return None, {
            "reason_code": "source_summary_zero_record_count",
            "details": "wrapper summary record_count is zero",
        }
    return rate, {
        "numerator": leakage_count,
        "denominator": record_count,
    }


def _build_invalid_json_overall(parse_tool_summary: Mapping[str, Any]) -> tuple[float | None, dict[str, Any]]:
    parse_counts = parse_tool_summary.get("parse_status_counts", {})
    if not isinstance(parse_counts, Mapping):
        return None, {
            "reason_code": "source_summary_missing_parse_status_counts",
            "details": "parse/tool/no-call summary is missing parse_status_counts",
        }

    total = 0.0
    for value in parse_counts.values():
        numeric = _as_float_or_none(value)
        if numeric is None:
            continue
        total += numeric

    invalid_json = (
        (_as_float_or_none(parse_counts.get("invalid_json")) or 0.0)
        + (_as_float_or_none(parse_counts.get("invalid_json_with_embedded_object")) or 0.0)
    )

    rate = _safe_rate(invalid_json, total)
    if rate is None:
        return None, {
            "reason_code": "source_summary_zero_parse_record_count",
            "details": "parse_status_counts total is zero",
        }
    return rate, {
        "numerator": invalid_json,
        "denominator": total,
    }


def _build_family_rate_metric(
    aggregation_payload: Mapping[str, Any],
    *,
    family_id: str,
    concept_id: str,
) -> tuple[float | None, dict[str, Any]]:
    concept = _find_family_concept(aggregation_payload, family_id=family_id, concept_id=concept_id)
    if concept is None:
        return None, {
            "reason_code": "source_family_concept_missing_in_current_run",
            "details": f"concept '{concept_id}' under family '{family_id}' was not emitted",
        }
    rate = _as_float_or_none(concept.get("rate"))
    numerator = _as_float_or_none(concept.get("numerator"))
    denominator = _as_float_or_none(concept.get("denominator"))
    if rate is None or numerator is None or denominator is None:
        return None, {
            "reason_code": "source_family_concept_missing_numeric_fields",
            "details": f"concept '{concept_id}' is missing numeric rate/numerator/denominator fields",
        }
    return rate, {
        "numerator": numerator,
        "denominator": denominator,
    }


def _build_family_count_metric(
    aggregation_payload: Mapping[str, Any],
    *,
    family_id: str,
    concept_id: str,
) -> tuple[float | None, dict[str, Any]]:
    concept = _find_family_concept(aggregation_payload, family_id=family_id, concept_id=concept_id)
    if concept is None:
        return None, {
            "reason_code": "source_family_concept_missing_in_current_run",
            "details": f"concept '{concept_id}' under family '{family_id}' was not emitted",
        }
    numerator = _as_float_or_none(concept.get("numerator"))
    denominator = _as_float_or_none(concept.get("denominator"))
    if numerator is None or denominator is None:
        return None, {
            "reason_code": "source_family_concept_missing_numeric_fields",
            "details": f"concept '{concept_id}' is missing numeric numerator/denominator fields",
        }
    return numerator, {
        "numerator": numerator,
        "denominator": denominator,
    }


def _input_records_by_id(input_records: list[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    records_by_id: dict[str, Mapping[str, Any]] = {}
    for index, record in enumerate(input_records, start=1):
        record_id = _as_nonempty_str(record.get("record_id")) or f"line-{index}"
        records_by_id[record_id] = record
    return records_by_id


def _extract_adversarial_subset_evidence(record: Mapping[str, Any]) -> dict[str, Any] | None:
    source_split = _as_nonempty_str(record.get("source_split"))
    if source_split == "adversarial":
        return {
            "evidence_field": "source_split",
            "evidence_value": source_split,
        }

    subset_id = _as_nonempty_str(record.get("subset_id")) or _as_nonempty_str(record.get("source_subset"))
    if subset_id == "adversarial_no_call":
        return {
            "evidence_field": "subset_id",
            "evidence_value": subset_id,
        }

    provenance = _nested_mapping(record, "source_provenance") or _nested_mapping(record, "provenance") or {}
    metadata = _nested_mapping(record, "source_metadata") or _nested_mapping(provenance, "source_metadata") or {}
    source_artifact_path = (
        _as_nonempty_str(record.get("source_artifact_path"))
        or _as_nonempty_str(provenance.get("source_artifact_path"))
        or _as_nonempty_str(provenance.get("source_path"))
    )
    category = _as_nonempty_str(metadata.get("category"))
    source = _as_nonempty_str(metadata.get("source"))
    source_case_id = _as_nonempty_str(metadata.get("source_case_id")) or _as_nonempty_str(record.get("source_case_id"))

    if (
        source_artifact_path
        and source_artifact_path.endswith("evals/data/canonical_v1/adversarial.jsonl")
        and category == "adversarial_malformed"
        and source == "synthetic_adversarial_malformed"
        and source_case_id
    ):
        return {
            "evidence_field": "source_provenance",
            "source_artifact_path": source_artifact_path,
            "category": category,
            "source": source,
            "source_case_id": source_case_id,
        }

    return None


def _expected_no_call(score_record: Mapping[str, Any], input_record: Mapping[str, Any]) -> bool | None:
    direct = _as_bool_or_none(input_record.get("no_call_expected"))
    if direct is not None:
        return direct
    expected_binding = _nested_mapping(score_record, "expected_binding", "record_expectation")
    if expected_binding is None:
        return None
    return _as_bool_or_none(expected_binding.get("expected_no_call"))


def _no_call_scoring_status(score_record: Mapping[str, Any]) -> str | None:
    dimensions = score_record.get("scoring_dimensions")
    if not isinstance(dimensions, list):
        return None
    for dimension in dimensions:
        if not isinstance(dimension, Mapping):
            continue
        if str(dimension.get("dimension")) != "no_call_correctness":
            continue
        status = str(dimension.get("status") or "")
        if status in {"pass", "fail"}:
            return status
    return None


def _build_adversarial_no_call_metric(
    *,
    input_records: list[Mapping[str, Any]],
    per_output_scoring_payload: Mapping[str, Any],
) -> tuple[float | None, dict[str, Any]]:
    records_by_id = _input_records_by_id(input_records)
    score_records = per_output_scoring_payload.get("records")
    if not isinstance(score_records, list):
        return None, {
            "reason_code": "source_no_call_scoring_missing",
            "details": "per-output scoring status records are missing",
            "contract_source": "STAGE_C9A_ADVERSARIAL_NO_CALL_SUBSET_MAPPING_REVIEW.md",
        }

    explicit_subset_records: list[dict[str, Any]] = []
    included_records: list[dict[str, Any]] = []
    missing_expectation_record_ids: list[str] = []
    missing_scoring_record_ids: list[str] = []

    for score_record in score_records:
        if not isinstance(score_record, Mapping):
            continue
        record_id = _as_nonempty_str(score_record.get("record_id"))
        if record_id is None:
            continue
        input_record = records_by_id.get(record_id, {})
        subset_evidence = _extract_adversarial_subset_evidence(input_record)
        if subset_evidence is None:
            continue

        explicit_subset_records.append(
            {
                "record_id": record_id,
                "subset_evidence": subset_evidence,
            }
        )

        expected_no_call = _expected_no_call(score_record, input_record)
        if expected_no_call is not True:
            missing_expectation_record_ids.append(record_id)
            continue

        no_call_status = _no_call_scoring_status(score_record)
        if no_call_status is None:
            missing_scoring_record_ids.append(record_id)
            continue

        included_records.append(
            {
                "record_id": record_id,
                "no_call_correctness_status": no_call_status,
                "subset_evidence": subset_evidence,
            }
        )

    if not explicit_subset_records:
        return None, {
            "reason_code": "blocked_adversarial_subset_mapping_unavailable",
            "details": "C9-A requires explicit adversarial no-call subset evidence; no compliant subset marker was present.",
            "contract_source": "STAGE_C9A_ADVERSARIAL_NO_CALL_SUBSET_MAPPING_REVIEW.md",
        }

    if not included_records:
        if missing_expectation_record_ids:
            reason_code = "source_no_call_expectation_missing"
            details = "explicit adversarial subset evidence was present, but no included record had explicit no-call expectation evidence"
        elif missing_scoring_record_ids:
            reason_code = "source_no_call_scoring_missing"
            details = "explicit adversarial no-call records lacked no-call scoring evidence"
        else:
            reason_code = "source_adversarial_subset_denominator_zero"
            details = "explicit adversarial subset evidence was present, but denominator was zero"
        return None, {
            "reason_code": reason_code,
            "details": details,
            "contract_source": "STAGE_C9A_ADVERSARIAL_NO_CALL_SUBSET_MAPPING_REVIEW.md",
            "explicit_subset_record_count": len(explicit_subset_records),
            "missing_no_call_expectation_record_ids": sorted(missing_expectation_record_ids),
            "missing_no_call_scoring_record_ids": sorted(missing_scoring_record_ids),
        }

    numerator = float(sum(1 for row in included_records if row["no_call_correctness_status"] == "pass"))
    denominator = float(len(included_records))
    rate = _safe_rate(numerator, denominator)
    if rate is None:
        return None, {
            "reason_code": "source_adversarial_subset_denominator_zero",
            "details": "adversarial no-call denominator is zero",
            "contract_source": "STAGE_C9A_ADVERSARIAL_NO_CALL_SUBSET_MAPPING_REVIEW.md",
        }

    return rate, {
        "reason_code": "source_adversarial_subset_explicit_evidence_computed",
        "contract_source": "STAGE_C9A_ADVERSARIAL_NO_CALL_SUBSET_MAPPING_REVIEW.md",
        "numerator": numerator,
        "denominator": denominator,
        "failed_count": denominator - numerator,
        "included_records": included_records,
        "explicit_subset_record_count": len(explicit_subset_records),
        "missing_no_call_expectation_record_ids": sorted(missing_expectation_record_ids),
        "missing_no_call_scoring_record_ids": sorted(missing_scoring_record_ids),
        "details": "computed from explicit adversarial subset, no-call expectation, and no-call scoring evidence only",
    }


def _compute_projection_metrics(
    *,
    parse_tool_summary: Mapping[str, Any],
    wrapper_summary: Mapping[str, Any],
    aggregation_payload: Mapping[str, Any],
    per_output_scoring_payload: Mapping[str, Any],
    input_records: list[Mapping[str, Any]],
    source_paths: Mapping[str, str],
) -> dict[str, dict[str, Any]]:
    metric_records: dict[str, dict[str, Any]] = {}

    no_call_rate, no_call_evidence = _build_no_call_correctness_aggregate(parse_tool_summary)
    metric_records["no_call_correctness_aggregate"] = {
        "metric_id": "no_call_correctness_aggregate",
        "projection_status": "computed" if no_call_rate is not None else "noncomputable_missing_source",
        "value": no_call_rate,
        "source_artifact_path": source_paths["parse_tool_summary"],
        "source_field": "dimension_scored_counts.no_call_correctness / dimension_fail_counts.no_call_correctness",
        "evidence": no_call_evidence,
    }

    wrapper_rate, wrapper_evidence = _build_wrapper_leakage_overall(wrapper_summary)
    metric_records["wrapper_leakage_overall"] = {
        "metric_id": "wrapper_leakage_overall",
        "projection_status": "computed" if wrapper_rate is not None else "noncomputable_missing_source",
        "value": wrapper_rate,
        "source_artifact_path": source_paths["wrapper_summary"],
        "source_field": "wrapper_or_prose_leakage_count / record_count",
        "evidence": wrapper_evidence,
    }

    invalid_rate, invalid_evidence = _build_invalid_json_overall(parse_tool_summary)
    metric_records["invalid_json_overall"] = {
        "metric_id": "invalid_json_overall",
        "projection_status": "computed" if invalid_rate is not None else "noncomputable_missing_source",
        "value": invalid_rate,
        "source_artifact_path": source_paths["parse_tool_summary"],
        "source_field": "(invalid_json + invalid_json_with_embedded_object) / total_parse_status_count",
        "evidence": invalid_evidence,
    }

    read_file_rate, read_file_evidence = _build_family_rate_metric(
        aggregation_payload,
        family_id="Family B1",
        concept_id="Read-file aggregate",
    )
    metric_records["read_file_exact_valid_rate"] = {
        "metric_id": "read_file_exact_valid_rate",
        "projection_status": "computed" if read_file_rate is not None else "noncomputable_missing_source",
        "value": read_file_rate,
        "source_artifact_path": source_paths["aggregation_summary"],
        "source_field": "family_reports[Family B1].concept_summaries[Read-file aggregate].rate",
        "evidence": read_file_evidence,
    }

    symbol_rate, symbol_evidence = _build_family_rate_metric(
        aggregation_payload,
        family_id="Family B1",
        concept_id="Symbol-name governed sub-slice",
    )
    metric_records["read_file_symbol_name_exact_valid_rate"] = {
        "metric_id": "read_file_symbol_name_exact_valid_rate",
        "projection_status": "computed" if symbol_rate is not None else "noncomputable_missing_source",
        "value": symbol_rate,
        "source_artifact_path": source_paths["aggregation_summary"],
        "source_field": "family_reports[Family B1].concept_summaries[Symbol-name governed sub-slice].rate",
        "evidence": symbol_evidence,
    }

    direct_answer_count, direct_answer_evidence = _build_family_count_metric(
        aggregation_payload,
        family_id="Family A",
        concept_id="Direct-answer governed subtype",
    )
    metric_records["direct_answer_substitution_count"] = {
        "metric_id": "direct_answer_substitution_count",
        "projection_status": "computed" if direct_answer_count is not None else "noncomputable_missing_source",
        "value": direct_answer_count,
        "source_artifact_path": source_paths["aggregation_summary"],
        "source_field": "family_reports[Family A].concept_summaries[Direct-answer governed subtype].numerator",
        "evidence": direct_answer_evidence,
    }

    adversarial_rate, adversarial_evidence = _build_adversarial_no_call_metric(
        input_records=input_records,
        per_output_scoring_payload=per_output_scoring_payload,
    )
    metric_records["no_call_correctness_adversarial"] = {
        "metric_id": "no_call_correctness_adversarial",
        "projection_status": "computed" if adversarial_rate is not None else "noncomputable_blocked",
        "value": adversarial_rate,
        "source_artifact_path": source_paths["per_output_scoring"],
        "source_field": "records[].scoring_dimensions[dimension=no_call_correctness] joined to explicit input-record subset evidence",
        "contract_sources": [source_paths["c9a_contract"]],
        "evidence": adversarial_evidence,
    }

    metric_records["no_anchor_exact_valid_share"] = {
        "metric_id": "no_anchor_exact_valid_share",
        "projection_status": "noncomputable_blocked",
        "value": None,
        "source_artifact_path": source_paths["c9d_disposition"],
        "source_field": "authoritative noncomputable preservation disposition",
        "contract_sources": [source_paths["c9b_review"], source_paths["c9d_disposition"]],
        "evidence": {
            "reason_code": "blocked_no_anchor_share_semantic_mismatch",
            "details": "C9-D preserves this legacy metric as noncomputable blocked; Stage C B2 governed-rate evidence must not be substituted.",
            "disposition": "authoritative_noncomputable_preservation",
            "semantic_equivalence": "not_supported",
            "replacement": "not_supported_in_current_scope",
            "retirement": "not_supported_in_current_scope",
        },
    }

    return metric_records


def _build_projected_eval_summary(metric_records: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "report_version": "stage_c8_non_authoritative_projection_v1",
        "generated_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "projection_scope": "non_authoritative_adapter_only",
        "metrics": {},
        "failure_profile": {},
    }

    metric_paths = {
        "no_call_correctness_aggregate": "metrics.aggregate.no_call_correctness",
        "wrapper_leakage_overall": "metrics.aggregate.wrapper_leakage",
        "invalid_json_overall": "metrics.aggregate.invalid_json",
        "read_file_exact_valid_rate": "failure_profile.read_file_exact_valid.rate",
        "read_file_symbol_name_exact_valid_rate": "failure_profile.read_file_symbol_name_exact_valid.rate",
        "direct_answer_substitution_count": "failure_profile.failure_categories_non_exact_tool_rows.direct_answer_substitution",
    }

    for metric_id, path in metric_paths.items():
        record = metric_records.get(metric_id, {})
        if str(record.get("projection_status")) != "computed":
            continue
        value = record.get("value")
        numeric = _as_float_or_none(value)
        if numeric is None:
            continue
        _set_nested_value(payload, path, numeric)

    return payload


def _build_noncomputable_metric_artifact(
    metric_records: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for metric_id in sorted(metric_records.keys()):
        metric = metric_records[metric_id]
        status = str(metric.get("projection_status") or "")
        if status == "computed":
            continue
        evidence = metric.get("evidence", {})
        reason_code = None
        details = None
        if isinstance(evidence, Mapping):
            reason_code = evidence.get("reason_code")
            details = evidence.get("details")
        entries.append(
            {
                "metric_id": metric_id,
                "projection_status": status,
                "reason_code": str(reason_code or "noncomputable_unspecified"),
                "details": details,
                "source_artifact_path": metric.get("source_artifact_path"),
                "source_field": metric.get("source_field"),
                "evidence": evidence,
            }
        )
    return {
        "noncomputable_metric_count": len(entries),
        "records": entries,
    }


def _threshold_profile_delta_rules(threshold_profile: Mapping[str, Any]) -> list[dict[str, Any]]:
    rules: list[dict[str, Any]] = []
    for section in ("hard_invariants", "catastrophic_thresholds", "tradeoff_watch_thresholds"):
        raw_rules = threshold_profile.get(section, [])
        if not isinstance(raw_rules, list):
            continue
        for rule in raw_rules:
            if isinstance(rule, Mapping) and str(rule.get("basis")) == "delta_vs_baseline":
                out = dict(rule)
                out["threshold_section"] = section
                rules.append(out)
    return rules


def _build_baseline_delta_gate_artifact(
    *,
    threshold_profile: Mapping[str, Any],
    metric_records: Mapping[str, Mapping[str, Any]],
    projected_baseline_summary: Mapping[str, Any],
    source_paths: Mapping[str, str],
    adapter_flags: Mapping[str, Any],
) -> dict[str, Any]:
    baseline_mode = str(projected_baseline_summary.get("baseline_mode") or "")
    baseline_compatibility_only = baseline_mode == "non_authoritative_same_run_baseline_for_compatibility_only"
    rule_records: list[dict[str, Any]] = []

    for rule in _threshold_profile_delta_rules(threshold_profile):
        rule_id = str(rule.get("rule_id") or "")
        metric_id = str(rule.get("metric_id") or "")
        baseline_metric_id = str(rule.get("baseline_metric_id") or metric_id)
        metric_record = metric_records.get(metric_id, {})
        current_status = str(metric_record.get("projection_status") or "missing")
        current_value = metric_record.get("value")

        reason_codes: list[str] = []
        if current_status == "missing":
            reason_codes.append("current_metric_missing")
        elif current_status != "computed":
            reason_codes.append("current_metric_noncomputable")
        elif _as_float_or_none(current_value) is None:
            reason_codes.append("current_metric_missing")

        # C9-C requires explicit concept-scoped comparison approval. The C8 adapter
        # has no authoritative baseline-comparability surface, so default to blocked.
        reason_codes.append("comparability_status_missing")
        reason_codes.append("migration_status_missing")
        reason_codes.append("denominator_compatibility_missing")

        if baseline_compatibility_only:
            reason_codes.append("baseline_compatibility_only")
        else:
            reason_codes.append("baseline_provenance_missing")

        unique_reason_codes = sorted(set(reason_codes))
        rule_records.append(
            {
                "rule_id": rule_id,
                "metric_id": metric_id,
                "baseline_metric_id": baseline_metric_id,
                "basis": rule.get("basis"),
                "comparator": rule.get("comparator"),
                "threshold": rule.get("threshold"),
                "gate_result": "blocked",
                "evaluated_delta": None,
                "current_metric_projection_status": current_status,
                "current_metric_value": current_value,
                "baseline_mode": baseline_mode,
                "comparability_state": "missing",
                "current_run_computability": "not_evaluated_by_adapter",
                "denominator_compatibility_status": "missing",
                "migration_marker_identity": None,
                "current_source_artifact_path": metric_record.get("source_artifact_path"),
                "baseline_source_artifact_path": None,
                "reason_codes": unique_reason_codes,
                "contract_source": source_paths["c9c_gate"],
            }
        )

    return {
        "artifact_scope": "stage_c10b_non_authoritative_baseline_delta_gate",
        "generated_at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "authoritative_detector_output": adapter_flags.get("authoritative_detector_output"),
        "detector_migration_enabled": adapter_flags.get("detector_migration_enabled"),
        "threshold_profile_migration_enabled": adapter_flags.get("threshold_profile_migration_enabled"),
        "baseline_mode": baseline_mode,
        "compatibility_only_baseline": baseline_compatibility_only,
        "rule_count": len(rule_records),
        "blocked_rule_count": sum(1 for row in rule_records if row["gate_result"] == "blocked"),
        "passed_rule_count": sum(1 for row in rule_records if row["gate_result"] == "pass"),
        "rule_records": rule_records,
        "contract_sources": {
            "baseline_delta_gate": source_paths["c9c_gate"],
            "integration_plan": source_paths["c10a_plan"],
        },
    }


def _check_axis_preservation(detector_projection_preparation: Mapping[str, Any]) -> tuple[bool, dict[str, Any]]:
    rows = detector_projection_preparation.get("prepared_projection_records", [])
    if not isinstance(rows, list) or not rows:
        return False, {
            "reason": "prepared projection records missing",
            "checked_record_count": 0,
        }

    for row in rows:
        if not isinstance(row, Mapping):
            return False, {
                "reason": "projection row is not an object",
                "checked_record_count": 0,
            }
        axes = row.get("projection_state_axes")
        if not isinstance(axes, Mapping):
            return False, {
                "reason": "projection_state_axes missing",
                "checked_record_count": 0,
            }
        required = {"completeness", "current_run_computability", "comparability"}
        if not required.issubset(set(axes.keys())):
            return False, {
                "reason": "projection_state_axes missing one or more required axis keys",
                "checked_record_count": 0,
            }
        if "state" in axes or "combined_state" in axes:
            return False, {
                "reason": "collapsed state field found in projection_state_axes",
                "checked_record_count": 0,
            }

    return True, {
        "reason": "all records preserve independent state axes",
        "checked_record_count": len(rows),
    }


def _check_evidence_preservation(metric_records: Mapping[str, Mapping[str, Any]]) -> tuple[bool, dict[str, Any]]:
    missing_evidence = []
    for metric_id, record in metric_records.items():
        source_path = record.get("source_artifact_path")
        source_field = record.get("source_field")
        evidence = record.get("evidence")
        if not source_path or not source_field or not isinstance(evidence, Mapping):
            missing_evidence.append(metric_id)
    if missing_evidence:
        return False, {
            "reason": "missing source/evidence fields",
            "missing_evidence_metric_ids": sorted(missing_evidence),
        }
    return True, {
        "reason": "source artifact and evidence fields present for all metrics",
        "checked_metric_count": len(metric_records),
    }


def _build_compatibility_harness(
    *,
    detector_mod: Any,
    threshold_profile_path: Path,
    projected_eval_summary_path: Path,
    projected_baseline_summary_path: Path,
    detector_projection_preparation: Mapping[str, Any],
    governance_summary: Mapping[str, Any],
    metric_records: Mapping[str, Mapping[str, Any]],
    adapter_flags: Mapping[str, Any],
    compatibility_dir: Path,
) -> dict[str, Any]:
    threshold_profile = _load_json(threshold_profile_path)
    metric_catalog = threshold_profile.get("metric_catalog", {})
    if not isinstance(metric_catalog, Mapping):
        raise StageC8ProjectionError("threshold profile metric_catalog is invalid")

    metric_resolution_check = []
    for metric_id in sorted(metric_catalog.keys()):
        record = metric_records.get(metric_id)
        if record is None:
            metric_resolution_check.append(
                {
                    "metric_id": metric_id,
                    "status": "fail",
                    "message": "metric missing from projection adapter record set",
                }
            )
            continue
        status = str(record.get("projection_status") or "")
        if status == "computed":
            value = _as_float_or_none(record.get("value"))
            ok = value is not None
            metric_resolution_check.append(
                {
                    "metric_id": metric_id,
                    "status": "pass" if ok else "fail",
                    "message": "computed metric includes numeric value" if ok else "computed metric value is not numeric",
                }
            )
        else:
            evidence = record.get("evidence", {})
            reason_code = evidence.get("reason_code") if isinstance(evidence, Mapping) else None
            ok = isinstance(reason_code, str) and bool(reason_code.strip())
            metric_resolution_check.append(
                {
                    "metric_id": metric_id,
                    "status": "pass" if ok else "fail",
                    "message": "noncomputable metric has blocker reason code" if ok else "noncomputable metric missing blocker reason code",
                }
            )

    axis_pass, axis_detail = _check_axis_preservation(detector_projection_preparation)
    evidence_pass, evidence_detail = _check_evidence_preservation(metric_records)

    guardrail_status = governance_summary.get("guardrail_status", {})
    guardrail_clear = True
    if isinstance(guardrail_status, Mapping):
        guardrail_clear = not any(bool(value) for value in guardrail_status.values())
    else:
        guardrail_clear = False

    collapse_watch, gate = detector_mod._run_detector(
        eval_summary_path=projected_eval_summary_path,
        threshold_profile_path=threshold_profile_path,
        baseline_summary_path=projected_baseline_summary_path,
        geometry_context_path=None,
    )

    compatibility_dir.mkdir(parents=True, exist_ok=True)
    collapse_watch_path = compatibility_dir / "c8_compatibility_collapse_watch_interpretation.json"
    gate_path = compatibility_dir / "c8_compatibility_gate_assessment.json"
    _write_json(collapse_watch_path, collapse_watch)
    _write_json(gate_path, gate)

    noncomputable_rule_ids = []
    noncomputable_rules = collapse_watch.get("noncomputable_rules", [])
    if isinstance(noncomputable_rules, list):
        for rule in noncomputable_rules:
            if isinstance(rule, Mapping):
                rule_id = rule.get("rule_id")
                if isinstance(rule_id, str):
                    noncomputable_rule_ids.append(rule_id)

    checks = [
        {
            "check_id": "schema_continuity_metric_catalog_coverage",
            "result": "pass" if all(row["status"] == "pass" for row in metric_resolution_check) else "fail",
            "details": metric_resolution_check,
        },
        {
            "check_id": "axis_preservation",
            "result": "pass" if axis_pass else "fail",
            "details": axis_detail,
        },
        {
            "check_id": "evidence_preservation",
            "result": "pass" if evidence_pass else "fail",
            "details": evidence_detail,
        },
        {
            "check_id": "guardrail_clearance",
            "result": "pass" if guardrail_clear else "fail",
            "details": {
                "guardrail_status": guardrail_status,
            },
        },
        {
            "check_id": "consumer_readability",
            "result": "pass",
            "details": {
                "collapse_watch_status": collapse_watch.get("status"),
                "gate_status": gate.get("status"),
                "progression_allowed": gate.get("progression_allowed"),
                "halt_recommended": gate.get("halt_recommended"),
                "noncomputable_rule_ids": sorted(noncomputable_rule_ids),
                "collapse_watch_output_path": str(collapse_watch_path),
                "gate_assessment_output_path": str(gate_path),
            },
        },
    ]

    pass_count = sum(1 for check in checks if check["result"] == "pass")
    fail_count = sum(1 for check in checks if check["result"] == "fail")

    return {
        "adapter_flags": dict(adapter_flags),
        "projection_scope": "non_authoritative_adapter_only",
        "check_count": len(checks),
        "pass_count": pass_count,
        "fail_count": fail_count,
        "checks": checks,
        "detector_outputs": {
            "collapse_watch_interpretation_path": str(collapse_watch_path),
            "gate_assessment_path": str(gate_path),
        },
    }


def _build_projection_validation_artifact(
    *,
    metric_records: Mapping[str, Mapping[str, Any]],
    compatibility_artifact: Mapping[str, Any],
    baseline_delta_gate_artifact: Mapping[str, Any],
    governance_summary: Mapping[str, Any],
    adapter_flags: Mapping[str, Any],
) -> dict[str, Any]:
    unambiguous_metric_ids = [
        "no_call_correctness_aggregate",
        "wrapper_leakage_overall",
        "invalid_json_overall",
        "read_file_exact_valid_rate",
        "read_file_symbol_name_exact_valid_rate",
        "direct_answer_substitution_count",
    ]

    unambiguous_stability_checks = []
    for metric_id in unambiguous_metric_ids:
        record = metric_records.get(metric_id, {})
        status = str(record.get("projection_status") or "")
        stable = status in {"computed", "noncomputable_missing_source"}
        unambiguous_stability_checks.append(
            {
                "metric_id": metric_id,
                "projection_status": status,
                "result": "pass" if stable else "fail",
            }
        )

    adversarial_record = metric_records.get("no_call_correctness_adversarial", {})
    adversarial_status = str(adversarial_record.get("projection_status") or "")
    adversarial_evidence = adversarial_record.get("evidence", {})
    adversarial_reason = adversarial_evidence.get("reason_code") if isinstance(adversarial_evidence, Mapping) else None
    adversarial_allowed_block_reasons = {
        "blocked_adversarial_subset_mapping_unavailable",
        "source_adversarial_subset_marker_missing",
        "source_no_call_expectation_missing",
        "source_no_call_scoring_missing",
        "source_adversarial_subset_denominator_zero",
        "source_adversarial_subset_provenance_conflict",
        "source_adversarial_subset_inference_prohibited",
    }
    adversarial_ok = (
        (
            adversarial_status == "computed"
            and _as_float_or_none(adversarial_record.get("value")) is not None
            and adversarial_reason == "source_adversarial_subset_explicit_evidence_computed"
        )
        or (
            adversarial_status == "noncomputable_blocked"
            and isinstance(adversarial_reason, str)
            and adversarial_reason in adversarial_allowed_block_reasons
        )
    )

    no_anchor_record = metric_records.get("no_anchor_exact_valid_share", {})
    no_anchor_status = str(no_anchor_record.get("projection_status") or "")
    no_anchor_evidence = no_anchor_record.get("evidence", {})
    no_anchor_reason = no_anchor_evidence.get("reason_code") if isinstance(no_anchor_evidence, Mapping) else None
    no_anchor_disposition = no_anchor_evidence.get("disposition") if isinstance(no_anchor_evidence, Mapping) else None
    no_anchor_ok = (
        no_anchor_status == "noncomputable_blocked"
        and no_anchor_reason == "blocked_no_anchor_share_semantic_mismatch"
        and no_anchor_disposition == "authoritative_noncomputable_preservation"
        and no_anchor_record.get("value") is None
    )

    gate_rule_records = baseline_delta_gate_artifact.get("rule_records", [])
    gate_checks = []
    if isinstance(gate_rule_records, list):
        for rule in gate_rule_records:
            if not isinstance(rule, Mapping):
                continue
            reason_codes = rule.get("reason_codes")
            if not isinstance(reason_codes, list):
                reason_codes = []
            blocked = (
                str(rule.get("gate_result")) == "blocked"
                and "baseline_compatibility_only" in {str(reason) for reason in reason_codes}
            )
            gate_checks.append(
                {
                    "rule_id": rule.get("rule_id"),
                    "gate_result": rule.get("gate_result"),
                    "reason_codes": reason_codes,
                    "result": "pass" if blocked else "fail",
                }
            )

    guardrail_status = governance_summary.get("guardrail_status", {})
    guardrail_pass = isinstance(guardrail_status, Mapping) and not any(bool(value) for value in guardrail_status.values())

    no_migration_enabled = (
        adapter_flags.get("authoritative_detector_output") is False
        and adapter_flags.get("detector_migration_enabled") is False
        and adapter_flags.get("threshold_profile_migration_enabled") is False
    )

    compatibility_fail_count = int(compatibility_artifact.get("fail_count", 0))

    checks = [
        {
            "check_id": "unambiguous_mapping_stability",
            "result": "pass" if all(row["result"] == "pass" for row in unambiguous_stability_checks) else "fail",
            "details": unambiguous_stability_checks,
        },
        {
            "check_id": "adversarial_mapping_contract_behavior",
            "result": "pass" if adversarial_ok else "fail",
            "details": {
                "metric_id": "no_call_correctness_adversarial",
                "projection_status": adversarial_status,
                "reason_code": adversarial_reason,
                "value": adversarial_record.get("value"),
            },
        },
        {
            "check_id": "no_anchor_noncomputable_preservation",
            "result": "pass" if no_anchor_ok else "fail",
            "details": {
                "metric_id": "no_anchor_exact_valid_share",
                "projection_status": no_anchor_status,
                "reason_code": no_anchor_reason,
                "disposition": no_anchor_disposition,
                "value": no_anchor_record.get("value"),
            },
        },
        {
            "check_id": "baseline_delta_gate_blocked_for_compatibility_baseline",
            "result": "pass" if gate_checks and all(row["result"] == "pass" for row in gate_checks) else "fail",
            "details": gate_checks,
        },
        {
            "check_id": "no_inference_substitution_reconstruction",
            "result": "pass" if guardrail_pass else "fail",
            "details": {"guardrail_status": guardrail_status},
        },
        {
            "check_id": "migration_flags_disabled",
            "result": "pass" if no_migration_enabled else "fail",
            "details": dict(adapter_flags),
        },
        {
            "check_id": "consumer_compatibility_harness",
            "result": "pass" if compatibility_fail_count == 0 else "fail",
            "details": {
                "compatibility_fail_count": compatibility_fail_count,
                "compatibility_check_count": compatibility_artifact.get("check_count"),
            },
        },
    ]

    return {
        "check_count": len(checks),
        "pass_count": sum(1 for check in checks if check["result"] == "pass"),
        "fail_count": sum(1 for check in checks if check["result"] == "fail"),
        "checks": checks,
    }


def run_stage_c8_projection_adapter(
    *,
    fixtures_root: Path,
    output_records_path: Path,
    threshold_profile_path: Path,
    artifacts_dir: Path,
) -> dict[str, Any]:
    c6 = _load_stage_c6()
    detector_mod = _load_detector()

    fixtures_root = fixtures_root.resolve()
    output_records_path = output_records_path.resolve()
    threshold_profile_path = threshold_profile_path.resolve()
    artifacts_dir = artifacts_dir.resolve()
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    c6_artifacts_dir = artifacts_dir / "c6_reporting"
    c6_summary = c6.run_stage_c6_reporting_integration(
        fixtures_root=fixtures_root,
        output_records_path=output_records_path,
        artifacts_dir=c6_artifacts_dir,
    )

    c6_runtime = _load_json(Path(c6_summary["artifact_paths"]["runtime_scoring_summary"]))
    c6_guardrails = _load_json(Path(c6_summary["artifact_paths"]["governance_guardrail_summary"]))
    c6_validation = _load_json(Path(c6_summary["artifact_paths"]["validation_issue_summary"]))
    c6_projection_prep = _load_json(Path(c6_summary["artifact_paths"]["detector_projection_preparation"]))

    c5_artifact_paths = c6_runtime.get("c5_summary", {}).get("artifact_paths", {})

    parse_tool_summary_path = Path(str(c5_artifact_paths["parse_tool_nocall_scoring_summary"]))
    wrapper_summary_path = Path(str(c5_artifact_paths["wrapper_leakage_scoring_summary"]))
    per_output_scoring_path = Path(str(c5_artifact_paths["per_output_scoring_status"]))
    c5_runtime_summary_path = Path(str(c5_artifact_paths["runtime_scoring_summary"]))
    c5_runtime_summary = _load_json(c5_runtime_summary_path)
    c4_artifact_paths = c5_runtime_summary.get("c4_summary", {}).get("artifact_paths", {})
    aggregation_summary_path = Path(str(c4_artifact_paths["aggregation_summary_from_outputs"]))

    input_records = _load_jsonl_records(output_records_path)
    parse_tool_summary = _load_json(parse_tool_summary_path)
    wrapper_summary = _load_json(wrapper_summary_path)
    per_output_scoring = _load_json(per_output_scoring_path)
    aggregation_summary = _load_json(aggregation_summary_path)

    source_paths = {
        "output_records": str(output_records_path),
        "parse_tool_summary": str(parse_tool_summary_path),
        "wrapper_summary": str(wrapper_summary_path),
        "per_output_scoring": str(per_output_scoring_path),
        "aggregation_summary": str(aggregation_summary_path),
        "c7_gate": "/opt/ai-stack/assistant-training/docs/convergence/STAGE_C7_DETECTOR_PROJECTION_MIGRATION_IMPLEMENTATION_GATE.md",
        "c9a_contract": "/opt/ai-stack/assistant-training/docs/convergence/STAGE_C9A_ADVERSARIAL_NO_CALL_SUBSET_MAPPING_REVIEW.md",
        "c9b_review": "/opt/ai-stack/assistant-training/docs/convergence/STAGE_C9B_NO_ANCHOR_SEMANTIC_EQUIVALENCE_BRIDGE_REVIEW.md",
        "c9c_gate": "/opt/ai-stack/assistant-training/docs/convergence/STAGE_C9C_BASELINE_DELTA_COMPARABILITY_GATE_REVIEW.md",
        "c9d_disposition": "/opt/ai-stack/assistant-training/docs/convergence/STAGE_C9D_NO_ANCHOR_METRIC_DISPOSITION_REVIEW.md",
        "c10a_plan": "/opt/ai-stack/assistant-training/docs/convergence/STAGE_C10A_NON_AUTHORITATIVE_ADAPTER_INTEGRATION_PLAN.md",
    }

    metric_records = _compute_projection_metrics(
        parse_tool_summary=parse_tool_summary,
        wrapper_summary=wrapper_summary,
        aggregation_payload=aggregation_summary,
        per_output_scoring_payload=per_output_scoring,
        input_records=input_records,
        source_paths=source_paths,
    )

    adapter_flags = {
        "authoritative_detector_output": False,
        "detector_migration_enabled": False,
        "threshold_profile_migration_enabled": False,
    }

    projected_eval_summary = _build_projected_eval_summary(metric_records)
    projected_eval_summary["adapter_flags"] = dict(adapter_flags)
    projected_eval_summary["source_artifacts"] = {
        "stage_c6_summary_path": str(c6_summary["summary_path"]),
        "stage_c6_runtime_scoring_summary_path": str(Path(c6_summary["artifact_paths"]["runtime_scoring_summary"])),
        "stage_c6_validation_issue_summary_path": str(Path(c6_summary["artifact_paths"]["validation_issue_summary"])),
    }

    projected_baseline_summary = json.loads(json.dumps(projected_eval_summary, ensure_ascii=False))
    projected_baseline_summary["baseline_mode"] = "non_authoritative_same_run_baseline_for_compatibility_only"

    projected_eval_summary_path = artifacts_dir / "c8_projected_eval_summary_non_authoritative.json"
    projected_baseline_summary_path = artifacts_dir / "c8_projected_baseline_summary_non_authoritative.json"
    _write_json(projected_eval_summary_path, projected_eval_summary)
    _write_json(projected_baseline_summary_path, projected_baseline_summary)

    threshold_profile = _load_json(threshold_profile_path)
    baseline_delta_gate_artifact = _build_baseline_delta_gate_artifact(
        threshold_profile=threshold_profile,
        metric_records=metric_records,
        projected_baseline_summary=projected_baseline_summary,
        source_paths=source_paths,
        adapter_flags=adapter_flags,
    )
    baseline_delta_gate_artifact_path = artifacts_dir / "c10b_baseline_delta_gate_non_authoritative_artifact.json"
    _write_json(baseline_delta_gate_artifact_path, baseline_delta_gate_artifact)

    noncomputable_metric_artifact = _build_noncomputable_metric_artifact(metric_records)
    noncomputable_metric_artifact_path = artifacts_dir / "c8_noncomputable_metric_artifact.json"
    _write_json(noncomputable_metric_artifact_path, noncomputable_metric_artifact)

    compatibility_artifact = _build_compatibility_harness(
        detector_mod=detector_mod,
        threshold_profile_path=threshold_profile_path,
        projected_eval_summary_path=projected_eval_summary_path,
        projected_baseline_summary_path=projected_baseline_summary_path,
        detector_projection_preparation=c6_projection_prep,
        governance_summary=c6_guardrails,
        metric_records=metric_records,
        adapter_flags=adapter_flags,
        compatibility_dir=artifacts_dir / "compatibility",
    )
    compatibility_artifact_path = artifacts_dir / "c8_detector_consumer_compatibility_artifact.json"
    _write_json(compatibility_artifact_path, compatibility_artifact)

    projection_validation_artifact = _build_projection_validation_artifact(
        metric_records=metric_records,
        compatibility_artifact=compatibility_artifact,
        baseline_delta_gate_artifact=baseline_delta_gate_artifact,
        governance_summary=c6_guardrails,
        adapter_flags=adapter_flags,
    )
    projection_validation_artifact_path = artifacts_dir / "c8_projection_validation_artifact.json"
    _write_json(projection_validation_artifact_path, projection_validation_artifact)

    projection_adapter_artifact = {
        "adapter_scope": "stage_c8_non_authoritative_detector_projection_adapter",
        "integration_scope": "stage_c10b_non_authoritative_contract_integration",
        "generated_at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        **adapter_flags,
        "metric_records": metric_records,
        "noncomputable_metric_count": noncomputable_metric_artifact["noncomputable_metric_count"],
        "contract_sources": {
            "c9a_adversarial_no_call_subset_mapping": source_paths["c9a_contract"],
            "c9c_baseline_delta_comparability_gate": source_paths["c9c_gate"],
            "c9d_no_anchor_metric_disposition": source_paths["c9d_disposition"],
            "c10a_adapter_integration_plan": source_paths["c10a_plan"],
        },
        "evidence_sources": {
            "stage_c6_runtime_scoring_summary": str(Path(c6_summary["artifact_paths"]["runtime_scoring_summary"])),
            "stage_c6_governance_guardrail_summary": str(Path(c6_summary["artifact_paths"]["governance_guardrail_summary"])),
            "stage_c6_validation_issue_summary": str(Path(c6_summary["artifact_paths"]["validation_issue_summary"])),
            "stage_c6_detector_projection_preparation": str(Path(c6_summary["artifact_paths"]["detector_projection_preparation"])),
            "threshold_profile_path": str(threshold_profile_path),
        },
    }
    projection_adapter_artifact_path = artifacts_dir / "c8_projection_adapter_artifact.json"
    _write_json(projection_adapter_artifact_path, projection_adapter_artifact)

    runtime_summary = {
        "artifact_paths": {
            "projection_adapter": str(projection_adapter_artifact_path),
            "projected_eval_summary": str(projected_eval_summary_path),
            "projected_baseline_summary": str(projected_baseline_summary_path),
            "baseline_delta_gate": str(baseline_delta_gate_artifact_path),
            "noncomputable_metrics": str(noncomputable_metric_artifact_path),
            "compatibility_harness": str(compatibility_artifact_path),
            "projection_validation": str(projection_validation_artifact_path),
            "stage_c6_summary": str(c6_summary["summary_path"]),
            "stage_c6_validation_issue_summary": str(Path(c6_summary["artifact_paths"]["validation_issue_summary"])),
        },
        "adapter_flags": adapter_flags,
        "computed_metric_ids": sorted(
            metric_id
            for metric_id, record in metric_records.items()
            if str(record.get("projection_status")) == "computed"
        ),
        "noncomputable_metric_ids": sorted(
            metric_id
            for metric_id, record in metric_records.items()
            if str(record.get("projection_status")) != "computed"
        ),
        "compatibility_fail_count": compatibility_artifact["fail_count"],
        "projection_validation_fail_count": projection_validation_artifact["fail_count"],
        "guardrail_status": c6_guardrails.get("guardrail_status", {}),
        "validation_issue_count": c6_validation.get("combined_validation_issue_count", 0),
    }
    runtime_summary_path = artifacts_dir / "c8_projection_adapter_summary.json"
    _write_json(runtime_summary_path, runtime_summary)
    runtime_summary["summary_path"] = str(runtime_summary_path)

    return runtime_summary


def _default_fixtures_root() -> Path:
    return Path("/opt/ai-stack/assistant-training/manifests/reports/stage_b_wp8_validation/fixtures")


def _default_output_records_path() -> Path:
    return Path("/opt/ai-stack/assistant-training/reports/stage_c6/input/stage_c6_sample_output_records.jsonl")


def _default_threshold_profile_path() -> Path:
    return Path("/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_threshold_profile.json")


def _default_artifacts_dir() -> Path:
    return Path("/opt/ai-stack/assistant-training/reports/stage_c8/projection_artifacts")


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage C8 non-authoritative detector projection adapter")
    parser.add_argument("--fixtures-root", default=str(_default_fixtures_root()))
    parser.add_argument("--output-records-path", default=str(_default_output_records_path()))
    parser.add_argument("--threshold-profile-path", default=str(_default_threshold_profile_path()))
    parser.add_argument("--artifacts-dir", default=str(_default_artifacts_dir()))
    args = parser.parse_args()

    summary = run_stage_c8_projection_adapter(
        fixtures_root=Path(args.fixtures_root),
        output_records_path=Path(args.output_records_path),
        threshold_profile_path=Path(args.threshold_profile_path),
        artifacts_dir=Path(args.artifacts_dir),
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    adapter_flags = summary.get("adapter_flags", {})
    if adapter_flags.get("authoritative_detector_output") or adapter_flags.get("detector_migration_enabled") or adapter_flags.get("threshold_profile_migration_enabled"):
        return 1

    if int(summary.get("compatibility_fail_count", 1)) > 0:
        return 1

    if int(summary.get("projection_validation_fail_count", 1)) > 0:
        return 1

    guardrail_status = summary.get("guardrail_status", {})
    if isinstance(guardrail_status, Mapping) and any(bool(value) for value in guardrail_status.values()):
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
