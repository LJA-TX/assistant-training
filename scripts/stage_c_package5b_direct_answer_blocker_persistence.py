#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping


SUMMARY_ARTIFACT_NAME = "summary.json"
COMPARISON_ROWS_ARTIFACT_NAME = "comparison_rows.jsonl"
STAGE_C_ROW_FACT_ARTIFACT_NAME = "stage_c_row_fact_metadata_artifact.json"
STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME = "stage_c_family_a_scorer_evidence_artifact.json"
STAGE_C_GOVERNANCE_GUARDRAILS_ARTIFACT_NAME = "stage_c_governance_guardrails_artifact.json"
STAGE_C_RUNTIME_CONTRACT_SUMMARY_ARTIFACT_NAME = "stage_c_runtime_contract_summary_artifact.json"
STAGE_C_PACKAGE1B_GOVERNANCE_REPORT_NAME = "stage_c_package1b_passive_governance_report.json"
STAGE_C_PACKAGE1C_RECONCILIATION_REPORT_NAME = "stage_c_package1c_passive_reconciliation_report.json"
STAGE_C_PACKAGE1D_READINESS_REPORT_NAME = "stage_c_package1d_migration_readiness_assessment.json"

DEFAULT_THRESHOLD_PROFILE_PATH = Path(
    "/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_threshold_profile.json"
)
FOCUS_SURFACE_ID = "direct_answer_substitution_count"


class DirectAnswerBlockerPersistenceError(RuntimeError):
    """Raised when the Package 5B blocker persistence surface cannot proceed."""


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise DirectAnswerBlockerPersistenceError(f"required artifact missing: {path}") from exc
    except Exception as exc:
        raise DirectAnswerBlockerPersistenceError(f"invalid JSON artifact {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise DirectAnswerBlockerPersistenceError(f"JSON root must be an object: {path}")
    return payload


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_json_digest(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _as_records(payload: Mapping[str, Any], field_name: str) -> list[dict[str, Any]]:
    records = payload.get(field_name)
    if not isinstance(records, list):
        raise DirectAnswerBlockerPersistenceError(f"{field_name} must be a list")
    out: list[dict[str, Any]] = []
    for idx, record in enumerate(records):
        if not isinstance(record, dict):
            raise DirectAnswerBlockerPersistenceError(f"{field_name}[{idx}] must be an object")
        out.append(record)
    return out


def _require_side_records(family_a_artifact: Mapping[str, Any], side: str) -> list[dict[str, Any]]:
    sides = family_a_artifact.get("sides")
    if not isinstance(sides, Mapping):
        raise DirectAnswerBlockerPersistenceError("family_a_scorer_evidence.sides must be an object")
    side_payload = sides.get(side)
    if not isinstance(side_payload, Mapping):
        raise DirectAnswerBlockerPersistenceError(f"family_a_scorer_evidence missing side '{side}'")
    return _as_records(side_payload, "records")


def _find_record(records: list[dict[str, Any]], *, field_name: str, expected: str) -> dict[str, Any]:
    matches = [record for record in records if str(record.get(field_name)) == expected]
    if len(matches) != 1:
        raise DirectAnswerBlockerPersistenceError(
            f"expected exactly one record where {field_name} == {expected!r}; found {len(matches)}"
        )
    return matches[0]


def _as_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    return None


def _sorted_row_ids(row_ids: list[str]) -> list[str]:
    return sorted(str(row_id) for row_id in row_ids)


def _sorted_counts(values: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return {key: counts[key] for key in sorted(counts)}


def _strip_paths(payload: Any) -> Any:
    if isinstance(payload, dict):
        out: dict[str, Any] = {}
        for key, value in payload.items():
            if key in {
                "path",
                "paths",
                "artifact_path",
                "artifact_paths",
                "report_path",
                "run_dir",
                "manifest_path",
            }:
                continue
            out[key] = _strip_paths(value)
        return out
    if isinstance(payload, list):
        return [_strip_paths(item) for item in payload]
    return payload


def _normalized_summary(summary: Mapping[str, Any]) -> dict[str, Any]:
    out = dict(summary)
    out.pop("generated_utc", None)
    return out


def _normalized_row_fact_artifact(row_fact_artifact: Mapping[str, Any]) -> dict[str, Any]:
    out = json.loads(json.dumps(row_fact_artifact))
    for record in out.get("records", []):
        provenance = record.get("provenance")
        if isinstance(provenance, dict):
            provenance.pop("extraction_timestamp_utc", None)
    return out


def _manifest_identity(manifest_path: Path) -> dict[str, Any]:
    manifest = _load_json(manifest_path)
    datasets = manifest.get("datasets") if isinstance(manifest.get("datasets"), dict) else {}
    dataset_rows = {
        str(split): int(spec.get("rows", 0))
        for split, spec in sorted(datasets.items())
        if isinstance(spec, dict)
    }
    return {
        "manifest_path": str(manifest_path),
        "manifest_sha256": _sha256_file(manifest_path),
        "manifest_version": manifest.get("manifest_version"),
        "eval_schema_version": (manifest.get("runtime") or {}).get("eval_schema_version"),
        "dataset_manifest_version": (manifest.get("runtime") or {}).get("dataset_manifest_version"),
        "evaluation_order": list(manifest.get("evaluation_order") or []),
        "split_hashes": dict(sorted((manifest.get("split_hashes") or {}).items())),
        "dataset_rows": dataset_rows,
    }


def _row_identity_snapshot(
    *,
    row_fact_artifact: Mapping[str, Any],
    family_a_records: list[dict[str, Any]],
) -> dict[str, Any]:
    row_fact_records = _as_records(row_fact_artifact, "records")
    row_ids = _sorted_row_ids([str(record.get("row_id")) for record in row_fact_records])
    tool_expected_row_ids = _sorted_row_ids(
        [
            str(record.get("row_id"))
            for record in row_fact_records
            if _as_bool((record.get("membership_markers") or {}).get("family_a_tool_expected_eligible")) is True
        ]
    )
    non_exact_row_ids = _sorted_row_ids(
        [
            str(record.get("row_id"))
            for record in family_a_records
            if _as_bool(record.get("non_exact_tool_expected")) is True
        ]
    )
    return {
        "row_fact_record_count": len(row_ids),
        "unique_row_id_count": len(set(row_ids)),
        "row_id_digest": _canonical_json_digest(row_ids),
        "tool_expected_row_id_count": len(tool_expected_row_ids),
        "tool_expected_row_id_digest": _canonical_json_digest(tool_expected_row_ids),
        "non_exact_row_id_count": len(non_exact_row_ids),
        "non_exact_row_id_digest": _canonical_json_digest(non_exact_row_ids),
    }


def _guardrail_snapshot(
    *,
    guardrails_artifact: Mapping[str, Any],
    runtime_contract_summary: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "guardrail_status": dict(sorted((guardrails_artifact.get("guardrail_status") or {}).items())),
        "runtime_legacy_surface_policy": dict(
            sorted((runtime_contract_summary.get("legacy_surface_policy") or {}).items())
        ),
        "guardrails_clear": not any(
            bool(value) for value in (guardrails_artifact.get("guardrail_status") or {}).values()
        ),
    }


def _package1b_snapshot(report: Mapping[str, Any]) -> dict[str, Any]:
    reported_values = report.get("reported_values") if isinstance(report.get("reported_values"), dict) else {}
    return {
        "consumer_scope": report.get("consumer_scope"),
        "row_fact_record_count": ((reported_values.get("row_fact_record_count") or {}).get("value")),
        "family_a_tool_expected_population_count": (
            (reported_values.get("family_a_tool_expected_population_count") or {}).get("value")
        ),
        "family_a_exact_valid_tool_expected_count": (
            (reported_values.get("family_a_exact_valid_tool_expected_count") or {}).get("value")
        ),
        "family_a_non_exact_tool_expected_count": (
            (reported_values.get("family_a_non_exact_tool_expected_count") or {}).get("value")
        ),
        "family_a_subtype_assigned_count": (
            (reported_values.get("family_a_subtype_assigned_count") or {}).get("value")
        ),
        "family_a_missing_evidence_count": (
            (reported_values.get("family_a_missing_evidence_count") or {}).get("value")
        ),
        "family_a_missing_evidence_reason_counts": (
            (reported_values.get("family_a_missing_evidence_reason_counts") or {}).get("value")
        ),
        "integrity_checks": dict(sorted((report.get("integrity_checks") or {}).items())),
    }


def _focus_reconciliation_snapshot(report: Mapping[str, Any]) -> dict[str, Any]:
    surface = _find_record(
        _as_records(report, "reconciled_surfaces"),
        field_name="surface_id",
        expected=FOCUS_SURFACE_ID,
    )
    return {
        "surface_id": surface["surface_id"],
        "reconciliation_status": surface.get("reconciliation_status"),
        "reason_code": surface.get("reason_code"),
        "reason": surface.get("reason"),
        "authoritative_source": _strip_paths(surface.get("authoritative_source")),
        "legacy_source": _strip_paths(surface.get("legacy_source")),
        "ownership_authority": surface.get("ownership_authority"),
    }


def _focus_readiness_snapshot(report: Mapping[str, Any]) -> dict[str, Any]:
    surface = _find_record(
        _as_records(report, "compatibility_surface_assessments"),
        field_name="surface_id",
        expected=FOCUS_SURFACE_ID,
    )
    return {
        "surface_id": surface["surface_id"],
        "readiness_state": surface.get("readiness_state"),
        "reasoning": surface.get("reasoning"),
        "blocking_conditions": surface.get("blocking_conditions"),
        "reconciliation_record": _strip_paths(surface.get("reconciliation_record")),
        "authoritative_support": surface.get("authoritative_support"),
        "integrity_checks": dict(sorted((report.get("integrity_checks") or {}).items())),
        "readiness_counts": dict(sorted((report.get("readiness_counts") or {}).items())),
    }


def _legacy_surface_snapshot(summary: Mapping[str, Any]) -> dict[str, Any]:
    failure_categories = (
        (summary.get("failure_profile") or {}).get("failure_categories_non_exact_tool_rows") or {}
    )
    if not isinstance(failure_categories, Mapping):
        raise DirectAnswerBlockerPersistenceError(
            "summary.failure_profile.failure_categories_non_exact_tool_rows must be an object"
        )
    return {
        "failure_profile_direct_answer_substitution_count": failure_categories.get(
            "direct_answer_substitution"
        ),
        "failure_profile_failure_categories_non_exact_tool_rows": dict(sorted(failure_categories.items())),
    }


def _dependency_inventory(threshold_profile: Mapping[str, Any]) -> dict[str, Any]:
    metric_catalog = threshold_profile.get("metric_catalog")
    if not isinstance(metric_catalog, Mapping):
        raise DirectAnswerBlockerPersistenceError("threshold profile metric_catalog must be an object")
    metric_spec = metric_catalog.get(FOCUS_SURFACE_ID)
    if not isinstance(metric_spec, Mapping):
        raise DirectAnswerBlockerPersistenceError(f"threshold profile missing metric_catalog entry for {FOCUS_SURFACE_ID}")

    def _matching_rules(group_name: str) -> list[dict[str, Any]]:
        rules = threshold_profile.get(group_name)
        if not isinstance(rules, list):
            raise DirectAnswerBlockerPersistenceError(f"threshold profile {group_name} must be a list")
        return [
            {
                "rule_id": rule.get("rule_id"),
                "basis": rule.get("basis"),
                "comparator": rule.get("comparator"),
                "threshold": rule.get("threshold"),
            }
            for rule in rules
            if isinstance(rule, Mapping) and str(rule.get("metric_id")) == FOCUS_SURFACE_ID
        ]

    return {
        "focus_surface": FOCUS_SURFACE_ID,
        "legacy_metric_path": metric_spec.get("path"),
        "threshold_profile_path": str(DEFAULT_THRESHOLD_PROFILE_PATH),
        "missing_baseline_policy": threshold_profile.get("missing_baseline_policy"),
        "threshold_consumers": {
            "catastrophic_rules": _matching_rules("catastrophic_thresholds"),
            "watch_rules": _matching_rules("tradeoff_watch_thresholds"),
        },
        "detector_consumers": [
            {
                "path": "scripts/post_eval_collapse_detector.py",
                "function": "_resolve_metric_from_catalog",
                "role": "resolves the legacy direct-answer count path from the threshold profile metric catalog",
            },
            {
                "path": "scripts/post_eval_collapse_detector.py",
                "function": "_resolve_required_metrics",
                "role": "collects current-run and baseline dependencies for direct_answer_substitution_count when the delta rule is active",
            },
            {
                "path": "scripts/post_eval_collapse_detector.py",
                "function": "_run_detector",
                "role": "evaluates the delta-vs-baseline watch rule for direct_answer_substitution_count",
            },
        ],
    }


def _blocker_inventory(
    *,
    family_a_records: list[dict[str, Any]],
    package1b_report: Mapping[str, Any],
    package1c_report: Mapping[str, Any],
    package1d_report: Mapping[str, Any],
) -> dict[str, Any]:
    tool_expected_records = [
        record for record in family_a_records if _as_bool(record.get("tool_expected_eligibility")) is True
    ]
    non_exact_records = [
        record for record in family_a_records if _as_bool(record.get("non_exact_tool_expected")) is True
    ]
    subtype_assigned_records = [
        record for record in non_exact_records if isinstance(record.get("subtype_assignment"), str)
    ]
    direct_answer_records = [
        record for record in non_exact_records if record.get("subtype_assignment") == "direct-answer substitution"
    ]
    missing_evidence_records = [
        record for record in non_exact_records if _as_bool(record.get("missing_evidence")) is True
    ]

    missing_reason_to_row_ids: dict[str, list[str]] = {}
    for record in missing_evidence_records:
        row_id = str(record.get("row_id"))
        reasons = record.get("missing_evidence_reasons")
        if not isinstance(reasons, list):
            reasons = list(reasons or ())
        for reason in reasons:
            reason_str = str(reason)
            missing_reason_to_row_ids.setdefault(reason_str, []).append(row_id)

    missing_reason_to_row_ids = {
        key: _sorted_row_ids(value)
        for key, value in sorted(missing_reason_to_row_ids.items())
    }
    missing_reason_counts = {
        key: len(value)
        for key, value in missing_reason_to_row_ids.items()
    }

    subtype_values = [
        str(record.get("subtype_assignment"))
        for record in subtype_assigned_records
    ]
    primary_outcomes = [str(record.get("primary_outcome")) for record in non_exact_records]

    blocker = {
        "tool_expected_population_count": len(tool_expected_records),
        "non_exact_tool_expected_count": len(non_exact_records),
        "subtype_assigned_count": len(subtype_assigned_records),
        "direct_answer_substitution_count": len(direct_answer_records),
        "missing_evidence_count": len(missing_evidence_records),
        "subtype_counts": _sorted_counts(subtype_values),
        "non_exact_primary_outcome_counts": _sorted_counts(primary_outcomes),
        "subtype_assigned_row_ids": _sorted_row_ids(
            [str(record.get("row_id")) for record in subtype_assigned_records]
        ),
        "direct_answer_row_ids": _sorted_row_ids(
            [str(record.get("row_id")) for record in direct_answer_records]
        ),
        "missing_evidence_row_ids": _sorted_row_ids(
            [str(record.get("row_id")) for record in missing_evidence_records]
        ),
        "missing_evidence_reason_counts": missing_reason_counts,
        "missing_evidence_reason_to_row_ids": missing_reason_to_row_ids,
        "subtype_assigned_row_id_digest": _canonical_json_digest(
            _sorted_row_ids([str(record.get("row_id")) for record in subtype_assigned_records])
        ),
        "direct_answer_row_id_digest": _canonical_json_digest(
            _sorted_row_ids([str(record.get("row_id")) for record in direct_answer_records])
        ),
        "missing_evidence_row_id_digest": _canonical_json_digest(
            _sorted_row_ids([str(record.get("row_id")) for record in missing_evidence_records])
        ),
        "missing_evidence_reason_digest": _canonical_json_digest(missing_reason_to_row_ids),
        "package1b_snapshot": _package1b_snapshot(package1b_report),
        "focus_surface_reconciliation": _focus_reconciliation_snapshot(package1c_report),
        "focus_surface_readiness": _focus_readiness_snapshot(package1d_report),
    }
    return blocker


def build_blocker_bundle(
    *,
    run_dir: Path,
    bundle_label: str,
    output_path: Path,
    threshold_profile_path: Path = DEFAULT_THRESHOLD_PROFILE_PATH,
) -> dict[str, Any]:
    run_dir = run_dir.resolve()
    summary_path = run_dir / SUMMARY_ARTIFACT_NAME
    comparison_rows_path = run_dir / COMPARISON_ROWS_ARTIFACT_NAME
    row_fact_path = run_dir / STAGE_C_ROW_FACT_ARTIFACT_NAME
    family_a_path = run_dir / STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME
    guardrails_path = run_dir / STAGE_C_GOVERNANCE_GUARDRAILS_ARTIFACT_NAME
    runtime_contract_path = run_dir / STAGE_C_RUNTIME_CONTRACT_SUMMARY_ARTIFACT_NAME
    package1b_path = run_dir / STAGE_C_PACKAGE1B_GOVERNANCE_REPORT_NAME
    package1c_path = run_dir / STAGE_C_PACKAGE1C_RECONCILIATION_REPORT_NAME
    package1d_path = run_dir / STAGE_C_PACKAGE1D_READINESS_REPORT_NAME

    summary = _load_json(summary_path)
    row_fact_artifact = _load_json(row_fact_path)
    family_a_artifact = _load_json(family_a_path)
    guardrails_artifact = _load_json(guardrails_path)
    runtime_contract_summary = _load_json(runtime_contract_path)
    package1b_report = _load_json(package1b_path)
    package1c_report = _load_json(package1c_path)
    package1d_report = _load_json(package1d_path)
    threshold_profile = _load_json(threshold_profile_path)

    manifest_path = Path(str(summary.get("manifest_path") or "")).resolve()
    if not manifest_path.exists():
        raise DirectAnswerBlockerPersistenceError(
            f"manifest path from summary does not exist: {manifest_path}"
        )

    detector_summary_side = str(summary.get("detector_summary_side") or "base")
    family_a_records = _require_side_records(family_a_artifact, detector_summary_side)
    blocker_inventory = _blocker_inventory(
        family_a_records=family_a_records,
        package1b_report=package1b_report,
        package1c_report=package1c_report,
        package1d_report=package1d_report,
    )

    bundle = {
        "bundle_schema_version": "stage_c_package5b_direct_answer_blocker_bundle_v1",
        "bundle_scope": "stage_c_package5b_direct_answer_blocker_persistence",
        "focus_surface": FOCUS_SURFACE_ID,
        "bundle_label": bundle_label,
        "run_dir": str(run_dir),
        "runtime_configuration": {
            "generated_utc": summary.get("generated_utc"),
            "model_name_or_path": summary.get("model_name_or_path"),
            "adapter_dir": summary.get("adapter_dir"),
            "decode_defaults": summary.get("decode_defaults"),
            "detector_summary_side": detector_summary_side,
        },
        "manifest_identity": _manifest_identity(manifest_path),
        "raw_artifact_hashes": {
            "summary_json": _sha256_file(summary_path),
            "comparison_rows_jsonl": _sha256_file(comparison_rows_path),
            "row_fact_metadata": _sha256_file(row_fact_path),
            "family_a_scorer_evidence": _sha256_file(family_a_path),
            "governance_guardrails": _sha256_file(guardrails_path),
            "runtime_contract_summary": _sha256_file(runtime_contract_path),
            "package1b_governance_report": _sha256_file(package1b_path),
            "package1c_reconciliation_report": _sha256_file(package1c_path),
            "package1d_readiness_report": _sha256_file(package1d_path),
        },
        "normalized_digests": {
            "summary_semantic_digest": _canonical_json_digest(_normalized_summary(summary)),
            "row_fact_semantic_digest": _canonical_json_digest(_normalized_row_fact_artifact(row_fact_artifact)),
            "blocker_inventory_digest": _canonical_json_digest(_strip_paths(blocker_inventory)),
            "focus_reconciliation_digest": _canonical_json_digest(
                _focus_reconciliation_snapshot(package1c_report)
            ),
            "focus_readiness_digest": _canonical_json_digest(_focus_readiness_snapshot(package1d_report)),
            "package1b_semantic_digest": _canonical_json_digest(_package1b_snapshot(package1b_report)),
        },
        "row_identity_snapshot": _row_identity_snapshot(
            row_fact_artifact=row_fact_artifact,
            family_a_records=family_a_records,
        ),
        "guardrail_results": _guardrail_snapshot(
            guardrails_artifact=guardrails_artifact,
            runtime_contract_summary=runtime_contract_summary,
        ),
        "legacy_surface_snapshot": _legacy_surface_snapshot(summary),
        "blocker_inventory": blocker_inventory,
        "dependency_inventory": _dependency_inventory(threshold_profile),
        "supporting_artifacts": {
            "summary_json": str(summary_path),
            "comparison_rows_jsonl": str(comparison_rows_path),
            "row_fact_metadata": str(row_fact_path),
            "family_a_scorer_evidence": str(family_a_path),
            "governance_guardrails": str(guardrails_path),
            "runtime_contract_summary": str(runtime_contract_path),
            "package1b_governance_report": str(package1b_path),
            "package1c_reconciliation_report": str(package1c_path),
            "package1d_readiness_report": str(package1d_path),
        },
    }

    _write_json(output_path.resolve(), bundle)
    return {
        "bundle_path": str(output_path.resolve()),
        "bundle_scope": bundle["bundle_scope"],
        "focus_surface": FOCUS_SURFACE_ID,
        "bundle_label": bundle_label,
        "missing_evidence_count": bundle["blocker_inventory"]["missing_evidence_count"],
        "readiness_state": bundle["blocker_inventory"]["focus_surface_readiness"]["readiness_state"],
        "reconciliation_status": bundle["blocker_inventory"]["focus_surface_reconciliation"][
            "reconciliation_status"
        ],
    }


def compare_blocker_bundles(
    *,
    left_bundle_path: Path,
    right_bundle_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    left = _load_json(left_bundle_path.resolve())
    right = _load_json(right_bundle_path.resolve())

    raw_hash_comparison = {
        key: {
            "left": left["raw_artifact_hashes"].get(key),
            "right": right["raw_artifact_hashes"].get(key),
            "equal": left["raw_artifact_hashes"].get(key) == right["raw_artifact_hashes"].get(key),
        }
        for key in sorted(set(left["raw_artifact_hashes"]) | set(right["raw_artifact_hashes"]))
    }

    blocker_left = left["blocker_inventory"]
    blocker_right = right["blocker_inventory"]
    reconciliation_left = blocker_left["focus_surface_reconciliation"]
    reconciliation_right = blocker_right["focus_surface_reconciliation"]
    readiness_left = blocker_left["focus_surface_readiness"]
    readiness_right = blocker_right["focus_surface_readiness"]

    stability = {
        "manifest_identity_stable": left["manifest_identity"] == right["manifest_identity"],
        "runtime_configuration_stable": (
            {
                "model_name_or_path": left["runtime_configuration"].get("model_name_or_path"),
                "adapter_dir": left["runtime_configuration"].get("adapter_dir"),
                "decode_defaults": left["runtime_configuration"].get("decode_defaults"),
                "detector_summary_side": left["runtime_configuration"].get("detector_summary_side"),
            }
            == {
                "model_name_or_path": right["runtime_configuration"].get("model_name_or_path"),
                "adapter_dir": right["runtime_configuration"].get("adapter_dir"),
                "decode_defaults": right["runtime_configuration"].get("decode_defaults"),
                "detector_summary_side": right["runtime_configuration"].get("detector_summary_side"),
            }
        ),
        "summary_semantic_digest_stable": (
            left["normalized_digests"]["summary_semantic_digest"]
            == right["normalized_digests"]["summary_semantic_digest"]
        ),
        "row_fact_semantic_digest_stable": (
            left["normalized_digests"]["row_fact_semantic_digest"]
            == right["normalized_digests"]["row_fact_semantic_digest"]
        ),
        "comparison_rows_hash_stable": (
            left["raw_artifact_hashes"]["comparison_rows_jsonl"]
            == right["raw_artifact_hashes"]["comparison_rows_jsonl"]
        ),
        "row_identity_stable": (
            left["row_identity_snapshot"]["row_id_digest"]
            == right["row_identity_snapshot"]["row_id_digest"]
        ),
        "tool_expected_row_identity_stable": (
            left["row_identity_snapshot"]["tool_expected_row_id_digest"]
            == right["row_identity_snapshot"]["tool_expected_row_id_digest"]
        ),
        "non_exact_row_identity_stable": (
            left["row_identity_snapshot"]["non_exact_row_id_digest"]
            == right["row_identity_snapshot"]["non_exact_row_id_digest"]
        ),
        "package1b_snapshot_stable": (
            left["normalized_digests"]["package1b_semantic_digest"]
            == right["normalized_digests"]["package1b_semantic_digest"]
        ),
        "blocker_inventory_stable": (
            left["normalized_digests"]["blocker_inventory_digest"]
            == right["normalized_digests"]["blocker_inventory_digest"]
        ),
        "subtype_assigned_row_ids_stable": (
            blocker_left["subtype_assigned_row_id_digest"] == blocker_right["subtype_assigned_row_id_digest"]
        ),
        "direct_answer_row_ids_stable": (
            blocker_left["direct_answer_row_id_digest"] == blocker_right["direct_answer_row_id_digest"]
        ),
        "missing_evidence_row_ids_stable": (
            blocker_left["missing_evidence_row_id_digest"] == blocker_right["missing_evidence_row_id_digest"]
        ),
        "missing_evidence_reasons_stable": (
            blocker_left["missing_evidence_reason_digest"] == blocker_right["missing_evidence_reason_digest"]
        ),
        "focus_reconciliation_stable": (
            left["normalized_digests"]["focus_reconciliation_digest"]
            == right["normalized_digests"]["focus_reconciliation_digest"]
        ),
        "focus_reconciliation_requires_future_migration_both": (
            reconciliation_left["reconciliation_status"] == "requires_future_migration"
            and reconciliation_right["reconciliation_status"] == "requires_future_migration"
        ),
        "focus_readiness_stable": (
            left["normalized_digests"]["focus_readiness_digest"]
            == right["normalized_digests"]["focus_readiness_digest"]
        ),
        "focus_readiness_migration_blocked_both": (
            readiness_left["readiness_state"] == "migration-blocked"
            and readiness_right["readiness_state"] == "migration-blocked"
        ),
        "guardrails_clear_both": (
            bool(left["guardrail_results"]["guardrails_clear"])
            and bool(right["guardrail_results"]["guardrails_clear"])
        ),
        "legacy_surface_stable": left["legacy_surface_snapshot"] == right["legacy_surface_snapshot"],
    }

    if all(stability.values()):
        reproducibility = {
            "classification": "strongly reproducible",
            "rationale": (
                "Counts, blocker row identities, blocker reasons, readiness/reconciliation states, guardrails, "
                "and legacy direct-answer surface snapshots all remained identical across repeated full runs."
            ),
        }
    elif (
        stability["manifest_identity_stable"]
        and stability["runtime_configuration_stable"]
        and stability["focus_reconciliation_stable"]
        and stability["focus_readiness_stable"]
        and stability["missing_evidence_row_ids_stable"]
        and stability["missing_evidence_reasons_stable"]
    ):
        reproducibility = {
            "classification": "stable",
            "rationale": (
                "The blocker state and blocker-supporting row identities remained stable, even if some secondary "
                "artifacts or non-blocker details drifted."
            ),
        }
    elif (
        stability["focus_reconciliation_stable"]
        and stability["focus_readiness_stable"]
        and stability["guardrails_clear_both"]
    ):
        reproducibility = {
            "classification": "partially stable",
            "rationale": (
                "The high-level blocker state remained the same, but row-level blocker support or reason structure drifted."
            ),
        }
    else:
        reproducibility = {
            "classification": "unstable",
            "rationale": (
                "Repeated full runs did not preserve the blocker state or the blocker-supporting evidence structure."
            ),
        }

    comparison = {
        "comparison_schema_version": "stage_c_package5b_direct_answer_blocker_stability_v1",
        "comparison_scope": "stage_c_package5b_direct_answer_blocker_persistence",
        "focus_surface": FOCUS_SURFACE_ID,
        "left_bundle_path": str(left_bundle_path.resolve()),
        "right_bundle_path": str(right_bundle_path.resolve()),
        "left_bundle_label": left.get("bundle_label"),
        "right_bundle_label": right.get("bundle_label"),
        "stability_findings": stability,
        "reproducibility_assessment": reproducibility,
        "raw_hash_comparison": raw_hash_comparison,
        "focus_surface_summary": {
            "left": {
                "legacy_surface_snapshot": left["legacy_surface_snapshot"],
                "blocker_inventory": blocker_left,
                "guardrail_results": left["guardrail_results"],
                "row_identity_snapshot": left["row_identity_snapshot"],
            },
            "right": {
                "legacy_surface_snapshot": right["legacy_surface_snapshot"],
                "blocker_inventory": blocker_right,
                "guardrail_results": right["guardrail_results"],
                "row_identity_snapshot": right["row_identity_snapshot"],
            },
        },
    }

    _write_json(output_path.resolve(), comparison)
    return {
        "comparison_path": str(output_path.resolve()),
        "comparison_scope": comparison["comparison_scope"],
        "focus_surface": FOCUS_SURFACE_ID,
        "reproducibility_classification": reproducibility["classification"],
        "focus_readiness_migration_blocked_both": stability["focus_readiness_migration_blocked_both"],
        "focus_reconciliation_requires_future_migration_both": stability[
            "focus_reconciliation_requires_future_migration_both"
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Stage C Package 5B direct-answer blocker evidence bundling and stability comparison"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build", help="Build a per-run direct-answer blocker bundle")
    build_parser.add_argument("--run-dir", required=True, help="Run directory containing evaluator and Package 1B/1C/1D artifacts")
    build_parser.add_argument("--bundle-label", required=True, help="Short label for this blocker bundle")
    build_parser.add_argument("--output-path", required=True, help="Output JSON path for the blocker bundle")
    build_parser.add_argument(
        "--threshold-profile-path",
        default=str(DEFAULT_THRESHOLD_PROFILE_PATH),
        help="Threshold profile path for dependency inventory",
    )

    compare_parser = subparsers.add_parser("compare", help="Compare two per-run direct-answer blocker bundles")
    compare_parser.add_argument("--left-bundle-path", required=True, help="Left bundle JSON path")
    compare_parser.add_argument("--right-bundle-path", required=True, help="Right bundle JSON path")
    compare_parser.add_argument("--output-path", required=True, help="Output JSON path for the blocker comparison")

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "build":
        summary = build_blocker_bundle(
            run_dir=Path(args.run_dir),
            bundle_label=str(args.bundle_label),
            output_path=Path(args.output_path),
            threshold_profile_path=Path(args.threshold_profile_path),
        )
    else:
        summary = compare_blocker_bundles(
            left_bundle_path=Path(args.left_bundle_path),
            right_bundle_path=Path(args.right_bundle_path),
            output_path=Path(args.output_path),
        )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
