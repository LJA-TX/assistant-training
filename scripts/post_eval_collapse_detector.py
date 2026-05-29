#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> dict[str, Any]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise RuntimeError(f"JSON root must be an object: {path}")
    return obj


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _canonical_json_text(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _coerce_finite_number(value: Any, *, context: str) -> float:
    if isinstance(value, bool):
        raise RuntimeError(f"{context}: bool is not a numeric metric value")
    if isinstance(value, (int, float)):
        out = float(value)
    elif isinstance(value, str):
        text = value.strip()
        if not text:
            raise RuntimeError(f"{context}: empty string is not numeric")
        try:
            out = float(text)
        except Exception as exc:
            raise RuntimeError(f"{context}: value '{value}' is not numeric") from exc
    else:
        raise RuntimeError(f"{context}: unsupported numeric type {type(value).__name__}")
    if not math.isfinite(out):
        raise RuntimeError(f"{context}: value must be finite")
    return out


def _iter_path_values(obj: Any, path: str) -> list[tuple[str, Any]]:
    segments = [seg for seg in path.split(".") if seg]
    if not segments:
        return [("", obj)]

    states: list[tuple[str, Any]] = [("", obj)]
    for seg in segments:
        next_states: list[tuple[str, Any]] = []
        for prefix, current in states:
            if seg == "*":
                if isinstance(current, dict):
                    for key, value in current.items():
                        next_prefix = f"{prefix}.{key}" if prefix else str(key)
                        next_states.append((next_prefix, value))
                elif isinstance(current, list):
                    for idx, value in enumerate(current):
                        next_prefix = f"{prefix}.{idx}" if prefix else str(idx)
                        next_states.append((next_prefix, value))
                else:
                    continue
                continue

            if isinstance(current, dict):
                if seg in current:
                    next_prefix = f"{prefix}.{seg}" if prefix else seg
                    next_states.append((next_prefix, current[seg]))
                continue

            if isinstance(current, list):
                try:
                    idx = int(seg)
                except Exception:
                    continue
                if 0 <= idx < len(current):
                    next_prefix = f"{prefix}.{idx}" if prefix else str(idx)
                    next_states.append((next_prefix, current[idx]))

        states = next_states
        if not states:
            break
    return states


def _resolve_metric_from_catalog(
    *,
    metric_id: str,
    metric_catalog: dict[str, Any],
    summary: dict[str, Any],
    summary_label: str,
) -> dict[str, Any]:
    if metric_id not in metric_catalog:
        raise RuntimeError(f"{summary_label}: metric '{metric_id}' is not declared in threshold profile metric_catalog")
    spec = metric_catalog[metric_id]
    if not isinstance(spec, dict):
        raise RuntimeError(f"{summary_label}: metric_catalog entry for '{metric_id}' must be an object")

    direct_path = spec.get("path")
    candidate_paths = spec.get("candidate_paths")
    if direct_path is None and candidate_paths is None:
        raise RuntimeError(f"{summary_label}: metric '{metric_id}' must define path or candidate_paths")

    candidates: list[str] = []
    if isinstance(direct_path, str) and direct_path.strip():
        candidates.append(direct_path.strip())
    if candidate_paths is not None:
        if not isinstance(candidate_paths, list) or not candidate_paths:
            raise RuntimeError(f"{summary_label}: metric '{metric_id}' candidate_paths must be a non-empty list")
        for path in candidate_paths:
            if not isinstance(path, str) or not path.strip():
                raise RuntimeError(f"{summary_label}: metric '{metric_id}' has empty candidate path")
            candidates.append(path.strip())
    if not candidates:
        raise RuntimeError(f"{summary_label}: metric '{metric_id}' has no usable path candidates")

    resolved: list[dict[str, Any]] = []
    for path in candidates:
        values = _iter_path_values(summary, path)
        if not values:
            continue
        if len(values) > 1:
            resolved_paths = [v[0] for v in values]
            raise RuntimeError(
                f"{summary_label}: metric '{metric_id}' candidate '{path}' is ambiguous; "
                f"resolved multiple values at {resolved_paths}"
            )
        resolved_path, raw_value = values[0]
        value = _coerce_finite_number(raw_value, context=f"{summary_label}.{metric_id}@{resolved_path}")
        resolved.append(
            {
                "path_candidate": path,
                "resolved_path": resolved_path,
                "value": value,
            }
        )

    if not resolved:
        raise RuntimeError(f"{summary_label}: required metric '{metric_id}' not found in summary")
    if len(resolved) > 1:
        raise RuntimeError(
            f"{summary_label}: metric '{metric_id}' is ambiguous; matched multiple candidates "
            f"{[r['resolved_path'] for r in resolved]}"
        )
    return resolved[0]


def _compare(lhs: float, comparator: str, rhs: float, *, tolerance: float) -> bool:
    if comparator == "lt":
        return lhs < rhs
    if comparator == "lte":
        return lhs <= rhs
    if comparator == "gt":
        return lhs > rhs
    if comparator == "gte":
        return lhs >= rhs
    if comparator == "eq":
        return abs(lhs - rhs) <= tolerance
    if comparator == "neq":
        return abs(lhs - rhs) > tolerance
    if comparator == "abs_lt":
        return abs(lhs) < rhs
    if comparator == "abs_lte":
        return abs(lhs) <= rhs
    if comparator == "abs_gt":
        return abs(lhs) > rhs
    if comparator == "abs_gte":
        return abs(lhs) >= rhs
    raise RuntimeError(f"unsupported comparator: {comparator}")


def _validate_threshold_profile(profile: dict[str, Any]) -> None:
    required_str = ["profile_schema_version", "threshold_profile_id"]
    for key in required_str:
        value = profile.get(key)
        if not isinstance(value, str) or not value.strip():
            raise RuntimeError(f"threshold profile requires non-empty string field: {key}")

    metric_catalog = profile.get("metric_catalog")
    if not isinstance(metric_catalog, dict) or not metric_catalog:
        raise RuntimeError("threshold profile requires non-empty object: metric_catalog")

    def _validate_rule_list(key: str) -> None:
        rules = profile.get(key)
        if not isinstance(rules, list):
            raise RuntimeError(f"threshold profile field must be a list: {key}")
        for idx, rule in enumerate(rules):
            if not isinstance(rule, dict):
                raise RuntimeError(f"{key}[{idx}] must be an object")
            for req in ("rule_id", "metric_id", "basis", "comparator", "threshold"):
                if req not in rule:
                    raise RuntimeError(f"{key}[{idx}] missing required field: {req}")
            if not isinstance(rule["rule_id"], str) or not rule["rule_id"].strip():
                raise RuntimeError(f"{key}[{idx}].rule_id must be a non-empty string")
            if not isinstance(rule["metric_id"], str) or not rule["metric_id"].strip():
                raise RuntimeError(f"{key}[{idx}].metric_id must be a non-empty string")
            if rule["metric_id"] not in metric_catalog:
                raise RuntimeError(f"{key}[{idx}] references unknown metric_id: {rule['metric_id']}")

            basis = str(rule["basis"])
            if basis not in {"absolute", "delta_vs_baseline"}:
                raise RuntimeError(f"{key}[{idx}].basis unsupported: {basis}")

            comparator = str(rule["comparator"])
            if comparator not in {"lt", "lte", "gt", "gte", "eq", "neq", "abs_lt", "abs_lte", "abs_gt", "abs_gte"}:
                raise RuntimeError(f"{key}[{idx}].comparator unsupported: {comparator}")

            _coerce_finite_number(rule["threshold"], context=f"{key}[{idx}].threshold")

            if "tolerance" in rule:
                tol = _coerce_finite_number(rule["tolerance"], context=f"{key}[{idx}].tolerance")
                if tol < 0:
                    raise RuntimeError(f"{key}[{idx}].tolerance must be nonnegative")

            baseline_metric_id = rule.get("baseline_metric_id")
            if baseline_metric_id is not None:
                if not isinstance(baseline_metric_id, str) or not baseline_metric_id.strip():
                    raise RuntimeError(f"{key}[{idx}].baseline_metric_id must be a non-empty string when present")
                if baseline_metric_id not in metric_catalog:
                    raise RuntimeError(
                        f"{key}[{idx}] references unknown baseline_metric_id: {baseline_metric_id}"
                    )

    _validate_rule_list("hard_invariants")
    _validate_rule_list("catastrophic_thresholds")
    _validate_rule_list("tradeoff_watch_thresholds")

    status_rules = profile.get("status_decision_rules")
    if not isinstance(status_rules, dict):
        raise RuntimeError("threshold profile requires object field: status_decision_rules")
    precedence = status_rules.get("precedence")
    if not isinstance(precedence, list) or not precedence:
        raise RuntimeError("status_decision_rules.precedence must be a non-empty list")
    required_statuses = {"pass", "watch", "halt_progression", "catastrophic_halt"}
    present = {str(x) for x in precedence}
    if present != required_statuses:
        raise RuntimeError(
            "status_decision_rules.precedence must contain exactly "
            f"{sorted(required_statuses)}"
        )

    missing_baseline_policy = str(profile.get("missing_baseline_policy", "fail_fast"))
    if missing_baseline_policy not in {"fail_fast", "mark_noncomputable"}:
        raise RuntimeError("missing_baseline_policy must be fail_fast or mark_noncomputable")


def _collect_rules(profile: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    return {
        "hard_invariants": [dict(rule) for rule in profile.get("hard_invariants", [])],
        "catastrophic_thresholds": [dict(rule) for rule in profile.get("catastrophic_thresholds", [])],
        "tradeoff_watch_thresholds": [dict(rule) for rule in profile.get("tradeoff_watch_thresholds", [])],
    }


def _resolve_required_metrics(
    *,
    rules_by_group: dict[str, list[dict[str, Any]]],
    metric_catalog: dict[str, Any],
    summary: dict[str, Any],
    summary_label: str,
) -> dict[str, dict[str, Any]]:
    metric_ids: set[str] = set()
    for rules in rules_by_group.values():
        for rule in rules:
            metric_ids.add(str(rule["metric_id"]))

    resolved: dict[str, dict[str, Any]] = {}
    for metric_id in sorted(metric_ids):
        resolved[metric_id] = _resolve_metric_from_catalog(
            metric_id=metric_id,
            metric_catalog=metric_catalog,
            summary=summary,
            summary_label=summary_label,
        )
    return resolved


def _resolve_baseline_metrics_if_needed(
    *,
    rules_by_group: dict[str, list[dict[str, Any]]],
    metric_catalog: dict[str, Any],
    baseline_summary: dict[str, Any] | None,
    missing_baseline_policy: str,
) -> tuple[dict[str, dict[str, Any]], set[str]]:
    required_baseline_metric_ids: set[str] = set()
    for rules in rules_by_group.values():
        for rule in rules:
            if str(rule["basis"]) != "delta_vs_baseline":
                continue
            baseline_metric_id = rule.get("baseline_metric_id")
            if isinstance(baseline_metric_id, str) and baseline_metric_id.strip():
                required_baseline_metric_ids.add(baseline_metric_id.strip())
            else:
                required_baseline_metric_ids.add(str(rule["metric_id"]))

    if not required_baseline_metric_ids:
        return {}, set()

    if baseline_summary is None:
        if missing_baseline_policy == "fail_fast":
            raise RuntimeError(
                "baseline summary is required because threshold profile includes delta_vs_baseline rules"
            )
        return {}, required_baseline_metric_ids

    resolved: dict[str, dict[str, Any]] = {}
    for metric_id in sorted(required_baseline_metric_ids):
        resolved[metric_id] = _resolve_metric_from_catalog(
            metric_id=metric_id,
            metric_catalog=metric_catalog,
            summary=baseline_summary,
            summary_label="baseline_summary",
        )
    return resolved, set()


def _evaluate_rules(
    *,
    rules: list[dict[str, Any]],
    current_metrics: dict[str, dict[str, Any]],
    baseline_metrics: dict[str, dict[str, Any]],
    baseline_missing_metric_ids: set[str],
    missing_baseline_policy: str,
    group: str,
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for rule in rules:
        rule_id = str(rule["rule_id"])
        metric_id = str(rule["metric_id"])
        basis = str(rule["basis"])
        comparator = str(rule["comparator"])
        threshold = _coerce_finite_number(rule["threshold"], context=f"{group}.{rule_id}.threshold")
        tolerance = float(rule.get("tolerance", 1e-12))
        baseline_metric_id_raw = rule.get("baseline_metric_id")
        baseline_metric_id = (
            str(baseline_metric_id_raw)
            if isinstance(baseline_metric_id_raw, str) and baseline_metric_id_raw.strip()
            else metric_id
        )

        current = current_metrics[metric_id]
        current_value = float(current["value"])
        current_path = str(current["resolved_path"])

        record: dict[str, Any] = {
            "group": group,
            "rule_id": rule_id,
            "description": str(rule.get("description", "")),
            "metric_id": metric_id,
            "metric_path": current_path,
            "basis": basis,
            "comparator": comparator,
            "threshold": threshold,
            "tolerance": tolerance,
            "current_value": current_value,
            "baseline_metric_id": baseline_metric_id if basis == "delta_vs_baseline" else None,
            "baseline_metric_path": None,
            "baseline_value": None,
            "evaluated_value": None,
            "triggered": False,
            "computable": True,
            "reason": "",
        }

        if basis == "absolute":
            evaluated_value = current_value
        else:
            if baseline_metric_id in baseline_missing_metric_ids:
                if missing_baseline_policy == "fail_fast":
                    raise RuntimeError(
                        f"rule '{rule_id}' requires baseline metric '{baseline_metric_id}' but no baseline was supplied"
                    )
                record["computable"] = False
                record["reason"] = "baseline_missing_noncomputable"
                out.append(record)
                continue
            if baseline_metric_id not in baseline_metrics:
                raise RuntimeError(
                    f"rule '{rule_id}' requires baseline metric '{baseline_metric_id}' which could not be resolved"
                )
            baseline = baseline_metrics[baseline_metric_id]
            baseline_value = float(baseline["value"])
            record["baseline_metric_path"] = str(baseline["resolved_path"])
            record["baseline_value"] = baseline_value
            evaluated_value = current_value - baseline_value

        record["evaluated_value"] = evaluated_value
        record["triggered"] = _compare(evaluated_value, comparator, threshold, tolerance=tolerance)
        out.append(record)
    return out


def _decide_status(
    *,
    profile: dict[str, Any],
    hard_results: list[dict[str, Any]],
    catastrophic_results: list[dict[str, Any]],
    watch_results: list[dict[str, Any]],
    noncomputable_count: int,
) -> str:
    status_rules = profile.get("status_decision_rules", {})
    catastrophic_status = str(status_rules.get("catastrophic_trigger_status", "catastrophic_halt"))
    hard_status = str(status_rules.get("hard_invariant_violation_status", "halt_progression"))
    watch_status = str(status_rules.get("tradeoff_watch_status", "watch"))
    noncomputable_status = str(status_rules.get("noncomputable_status", hard_status))

    catastrophic_count = sum(1 for r in catastrophic_results if r.get("triggered"))
    hard_count = sum(1 for r in hard_results if r.get("triggered"))
    watch_count = sum(1 for r in watch_results if r.get("triggered"))

    if catastrophic_count > 0:
        return catastrophic_status
    if hard_count > 0:
        return hard_status
    if noncomputable_count > 0:
        return noncomputable_status
    if watch_count > 0:
        return watch_status
    return "pass"


def _run_detector(
    *,
    eval_summary_path: Path,
    threshold_profile_path: Path,
    baseline_summary_path: Path | None,
    geometry_context_path: Path | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    eval_summary = _load_json(eval_summary_path)
    threshold_profile = _load_json(threshold_profile_path)
    baseline_summary = _load_json(baseline_summary_path) if baseline_summary_path else None
    geometry_context = _load_json(geometry_context_path) if geometry_context_path else None

    _validate_threshold_profile(threshold_profile)
    metric_catalog = threshold_profile["metric_catalog"]
    rules_by_group = _collect_rules(threshold_profile)
    missing_baseline_policy = str(threshold_profile.get("missing_baseline_policy", "fail_fast"))

    current_metrics = _resolve_required_metrics(
        rules_by_group=rules_by_group,
        metric_catalog=metric_catalog,
        summary=eval_summary,
        summary_label="eval_summary",
    )
    baseline_metrics, baseline_missing_metric_ids = _resolve_baseline_metrics_if_needed(
        rules_by_group=rules_by_group,
        metric_catalog=metric_catalog,
        baseline_summary=baseline_summary,
        missing_baseline_policy=missing_baseline_policy,
    )

    hard_results = _evaluate_rules(
        rules=rules_by_group["hard_invariants"],
        current_metrics=current_metrics,
        baseline_metrics=baseline_metrics,
        baseline_missing_metric_ids=baseline_missing_metric_ids,
        missing_baseline_policy=missing_baseline_policy,
        group="hard_invariants",
    )
    catastrophic_results = _evaluate_rules(
        rules=rules_by_group["catastrophic_thresholds"],
        current_metrics=current_metrics,
        baseline_metrics=baseline_metrics,
        baseline_missing_metric_ids=baseline_missing_metric_ids,
        missing_baseline_policy=missing_baseline_policy,
        group="catastrophic_thresholds",
    )
    watch_results = _evaluate_rules(
        rules=rules_by_group["tradeoff_watch_thresholds"],
        current_metrics=current_metrics,
        baseline_metrics=baseline_metrics,
        baseline_missing_metric_ids=baseline_missing_metric_ids,
        missing_baseline_policy=missing_baseline_policy,
        group="tradeoff_watch_thresholds",
    )

    all_results = hard_results + catastrophic_results + watch_results
    noncomputable_rules = [r["rule_id"] for r in all_results if not r.get("computable", True)]
    hard_violations = [r["rule_id"] for r in hard_results if r.get("triggered")]
    catastrophic_triggers = [r["rule_id"] for r in catastrophic_results if r.get("triggered")]
    tradeoff_watch_warnings = [r["rule_id"] for r in watch_results if r.get("triggered")]

    status = _decide_status(
        profile=threshold_profile,
        hard_results=hard_results,
        catastrophic_results=catastrophic_results,
        watch_results=watch_results,
        noncomputable_count=len(noncomputable_rules),
    )

    profile_digest = _sha256_text(_canonical_json_text(threshold_profile))
    geometry_digest = _sha256_text(_canonical_json_text(geometry_context)) if geometry_context is not None else None

    collapse_watch = {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "status": status,
        "script": "post_eval_collapse_detector.py",
        "inputs": {
            "eval_summary_path": str(eval_summary_path),
            "threshold_profile_path": str(threshold_profile_path),
            "baseline_summary_path": str(baseline_summary_path) if baseline_summary_path else None,
            "geometry_context_path": str(geometry_context_path) if geometry_context_path else None,
        },
        "threshold_profile_id": str(threshold_profile["threshold_profile_id"]),
        "threshold_profile_schema_version": str(threshold_profile["profile_schema_version"]),
        "threshold_profile_digest": profile_digest,
        "geometry_context": geometry_context,
        "geometry_context_digest": geometry_digest,
        "metric_resolution": {
            "current": {k: {"path": v["resolved_path"], "value": v["value"]} for k, v in sorted(current_metrics.items())},
            "baseline": {k: {"path": v["resolved_path"], "value": v["value"]} for k, v in sorted(baseline_metrics.items())},
        },
        "rule_evaluation": {
            "hard_invariants": hard_results,
            "catastrophic_thresholds": catastrophic_results,
            "tradeoff_watch_thresholds": watch_results,
        },
        "summary": {
            "hard_invariant_violations": hard_violations,
            "catastrophic_triggers": catastrophic_triggers,
            "tradeoff_watch_warnings": tradeoff_watch_warnings,
            "noncomputable_rules": noncomputable_rules,
            "missing_baseline_policy": missing_baseline_policy,
        },
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }

    gate = {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "status": status,
        "threshold_profile_id": str(threshold_profile["threshold_profile_id"]),
        "threshold_profile_digest": profile_digest,
        "geometry_context": geometry_context,
        "geometry_context_digest": geometry_digest,
        "inputs": collapse_watch["inputs"],
        "decision_breakdown": {
            "hard_invariant_violation_count": len(hard_violations),
            "catastrophic_trigger_count": len(catastrophic_triggers),
            "tradeoff_watch_warning_count": len(tradeoff_watch_warnings),
            "noncomputable_rule_count": len(noncomputable_rules),
        },
        "active_rule_ids": {
            "hard_invariant_violations": hard_violations,
            "catastrophic_triggers": catastrophic_triggers,
            "tradeoff_watch_warnings": tradeoff_watch_warnings,
            "noncomputable_rules": noncomputable_rules,
        },
        "progression_allowed": status in {"pass", "watch"},
        "halt_recommended": status in {"halt_progression", "catastrophic_halt"},
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }
    return collapse_watch, gate


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Standalone post-eval collapse detector and gate reporter for Stage B geometry mapping."
    )
    parser.add_argument("--eval-summary", required=True, help="Path to canonical eval summary JSON")
    parser.add_argument("--threshold-profile", required=True, help="Path to threshold profile JSON")
    parser.add_argument("--baseline-summary", help="Optional baseline summary JSON path")
    parser.add_argument("--geometry-context", help="Optional geometry context JSON path")
    parser.add_argument(
        "--collapse-watch-output",
        help="Output path for collapse_watch_interpretation.json "
        "(default: <eval-summary-dir>/collapse_watch_interpretation.json)",
    )
    parser.add_argument(
        "--gate-assessment-output",
        help="Output path for gate_assessment.json "
        "(default: <eval-summary-dir>/gate_assessment.json)",
    )
    args = parser.parse_args()

    eval_summary_path = Path(args.eval_summary).resolve()
    threshold_profile_path = Path(args.threshold_profile).resolve()
    baseline_summary_path = Path(args.baseline_summary).resolve() if args.baseline_summary else None
    geometry_context_path = Path(args.geometry_context).resolve() if args.geometry_context else None

    collapse_out = (
        Path(args.collapse_watch_output).resolve()
        if args.collapse_watch_output
        else (eval_summary_path.parent / "collapse_watch_interpretation.json").resolve()
    )
    gate_out = (
        Path(args.gate_assessment_output).resolve()
        if args.gate_assessment_output
        else (eval_summary_path.parent / "gate_assessment.json").resolve()
    )

    collapse_watch, gate = _run_detector(
        eval_summary_path=eval_summary_path,
        threshold_profile_path=threshold_profile_path,
        baseline_summary_path=baseline_summary_path,
        geometry_context_path=geometry_context_path,
    )
    _write_json(collapse_out, collapse_watch)
    _write_json(gate_out, gate)
    print(json.dumps({"collapse_watch_output": str(collapse_out), "gate_assessment_output": str(gate_out)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
