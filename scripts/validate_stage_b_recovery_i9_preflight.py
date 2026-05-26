#!/usr/bin/env python3
"""
i9 preflight validation (bounded training-review readiness phase).

What this script does:
- Validates i9 builder/config/manifest/report artifacts.
- Re-checks ambiguity, contamination, and collapse-watch readiness telemetry.
- Produces a fail-fast review report.

What this script does NOT do:
- No training.
- No canonical eval execution.
- No approval gate activation.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

RUN_NAME = "stage_b_llama31_8b_base_v1_i9"
TARGETED_TOOLS = ("rg_search", "read_file")
EXPECTED_NON_TOOL_COUNTS = {"train": 756, "val": 84}
MAX_ANCHOR_DOMINANCE_RATIO = 0.65
MAX_TOP1_BEHAVIOR_SHARE = 0.70


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    detail: str


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"invalid JSON at {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"expected object JSON at {path}")
    return payload


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            raw = line.strip()
            if not raw:
                continue
            try:
                obj = json.loads(raw)
            except Exception as exc:
                raise RuntimeError(f"invalid JSONL at {path}:{line_no}: {exc}") from exc
            if not isinstance(obj, dict):
                raise RuntimeError(f"invalid JSONL row type at {path}:{line_no}; expected object")
            rows.append(obj)
    return rows


def _is_tool_row(row: dict[str, Any]) -> bool:
    msgs = row.get("messages")
    if not isinstance(msgs, list):
        return False
    for msg in msgs:
        if isinstance(msg, dict) and msg.get("role") == "assistant":
            tc = msg.get("tool_calls")
            return isinstance(tc, list) and bool(tc)
    return False


def _nested_get(obj: dict[str, Any], dotted: str) -> Any:
    cur: Any = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _require_paths_exist(paths: list[Path]) -> None:
    missing = [str(p) for p in paths if not p.exists()]
    if missing:
        raise RuntimeError("missing required path(s):\n- " + "\n- ".join(missing))


def _check_eq(name: str, actual: Any, expected: Any, *, detail_prefix: str = "") -> CheckResult:
    if actual == expected:
        return CheckResult(name=name, status="pass", detail=f"{detail_prefix}expected={expected}")
    return CheckResult(name=name, status="fail", detail=f"{detail_prefix}expected={expected} actual={actual}")


def _check_true(name: str, condition: bool, detail_on_fail: str, detail_on_pass: str = "ok") -> CheckResult:
    return CheckResult(name=name, status="pass" if condition else "fail", detail=detail_on_pass if condition else detail_on_fail)


def _check_warn(name: str, condition: bool, detail_on_warn: str, detail_on_pass: str = "ok") -> CheckResult:
    return CheckResult(name=name, status="pass" if condition else "warn", detail=detail_on_pass if condition else detail_on_warn)


def _tool_name(row: dict[str, Any]) -> str:
    msgs = row.get("messages")
    if not isinstance(msgs, list):
        return ""
    for msg in msgs:
        if isinstance(msg, dict) and msg.get("role") == "assistant":
            tc = msg.get("tool_calls")
            if isinstance(tc, list) and tc and isinstance(tc[0], dict):
                fn = tc[0].get("function")
                if isinstance(fn, dict):
                    return str(fn.get("name") or "").strip()
    return ""


def _user_prompt(row: dict[str, Any]) -> str:
    msgs = row.get("messages")
    if not isinstance(msgs, list):
        return ""
    for msg in msgs:
        if isinstance(msg, dict) and msg.get("role") == "user":
            return str(msg.get("content") or "")
    return ""


def _assistant_target_canon(row: dict[str, Any]) -> str:
    msgs = row.get("messages")
    if not isinstance(msgs, list):
        return ""
    for msg in msgs:
        if not isinstance(msg, dict) or msg.get("role") != "assistant":
            continue
        tc = msg.get("tool_calls")
        if isinstance(tc, list) and tc:
            return json.dumps({"tool_calls": tc}, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return str(msg.get("content") or "")
    return ""


def _source_case_id(row: dict[str, Any], fallback: str) -> str:
    meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    return str(meta.get("source_case_id") or meta.get("case_id") or fallback)


def _collect_eval_exclusions(path: Path) -> set[str]:
    prompts: set[str] = set()
    for row in _load_jsonl(path):
        prompts.add(_user_prompt(row))
    return prompts


def _overlap_report(candidate_rows: list[dict[str, Any]], eval_rows: list[dict[str, Any]]) -> dict[str, int]:
    cand_prompts = {_user_prompt(r) for r in candidate_rows}
    cand_targets = {_assistant_target_canon(r) for r in candidate_rows}
    cand_cases = {_source_case_id(r, "") for r in candidate_rows}

    eval_prompts = {_user_prompt(r) for r in eval_rows}
    eval_targets = {_assistant_target_canon(r) for r in eval_rows}
    eval_cases = {_source_case_id(r, "") for r in eval_rows}

    return {
        "prompt_overlap": len(cand_prompts.intersection(eval_prompts)),
        "target_overlap": len(cand_targets.intersection(eval_targets)),
        "source_case_id_overlap": len(cand_cases.intersection(eval_cases)),
    }


def _validate_builder_lock(builder_script: Path) -> list[CheckResult]:
    text = builder_script.read_text(encoding="utf-8")
    return [
        _check_true(
            "builder_requires_enable_dataset_emission",
            "--enable-dataset-emission" in text,
            "missing --enable-dataset-emission gate",
        ),
        _check_true(
            "builder_requires_allow_generation_phase",
            "--allow-generation-phase" in text,
            "missing --allow-generation-phase gate",
        ),
        _check_true(
            "builder_requires_enable_i9_commitment_conversion",
            "--enable-i9-commitment-conversion" in text,
            "missing --enable-i9-commitment-conversion gate",
        ),
    ]


def _validate_config_manifest(config: dict[str, Any], manifest: dict[str, Any]) -> list[CheckResult]:
    checks: list[CheckResult] = []
    checks.append(_check_eq("config_name", _nested_get(config, "name"), RUN_NAME))
    checks.append(_check_eq("manifest_name", _nested_get(manifest, "name"), RUN_NAME))
    checks.append(_check_eq("config_approved_to_run_false", _nested_get(config, "safety.approved_to_run"), False))
    checks.append(_check_eq("manifest_approved_to_run_false", _nested_get(manifest, "review_gate.approved_to_run"), False))
    checks.append(_check_eq("manifest_training_started_false", _nested_get(manifest, "training_started"), False))
    checks.append(
        _check_eq(
            "manifest_canonical_eval_manifest_fixed",
            _nested_get(manifest, "inputs.canonical_eval_manifest"),
            "/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json",
        )
    )
    return checks


def _validate_templates(
    intervention: dict[str, Any],
    readiness: dict[str, Any],
    risk: dict[str, Any],
    diagnostics_schema: dict[str, Any],
) -> list[CheckResult]:
    checks: list[CheckResult] = []
    checks.append(
        _check_eq(
            "intervention_targeted_tools",
            tuple(_nested_get(intervention, "SCOPE.targeted_tools") or []),
            TARGETED_TOOLS,
        )
    )
    checks.append(_check_eq("intervention_approved_to_run_false", _nested_get(intervention, "approval_state.approved_to_run"), False))

    collapse = _nested_get(readiness, "collapse_watch_conditions")
    checks.append(
        _check_true(
            "readiness_has_collapse_watch_conditions",
            isinstance(collapse, list) and len(collapse) >= 6,
            "readiness missing collapse_watch_conditions list",
        )
    )
    checks.append(
        _check_eq(
            "readiness_approved_to_run_false",
            _nested_get(readiness, "approval_state.approved_to_run"),
            False,
        )
    )

    checks.append(
        _check_true(
            "risk_assessment_has_primary_risks",
            isinstance(_nested_get(risk, "primary_risks"), list) and len(_nested_get(risk, "primary_risks")) >= 4,
            "risk assessment missing primary_risks list",
        )
    )

    checks.append(
        _check_true(
            "diagnostics_schema_has_commitment_conversion_telemetry",
            bool(_nested_get(diagnostics_schema, "sections.commitment_conversion_telemetry")),
            "diagnostics schema missing commitment_conversion_telemetry section",
        )
    )
    checks.append(
        _check_true(
            "diagnostics_schema_has_anchor_dominance",
            bool(_nested_get(diagnostics_schema, "sections.anchor_dominance_telemetry")),
            "diagnostics schema missing anchor_dominance_telemetry section",
        )
    )
    return checks


def _validate_generated_artifacts(
    dataset_summary: dict[str, Any],
    diagnostics: dict[str, Any],
    contamination: dict[str, Any],
    ambiguity: dict[str, Any],
    collapse_watch: dict[str, Any],
    anchor: dict[str, Any],
) -> list[CheckResult]:
    checks: list[CheckResult] = []

    checks.append(_check_eq("dataset_summary_iteration", dataset_summary.get("iteration"), RUN_NAME))
    checks.append(_check_eq("dataset_summary_approved_to_run_false", _nested_get(dataset_summary, "approval_state.approved_to_run"), False))

    hard = ambiguity.get("hard_block_candidates", {}) if isinstance(ambiguity.get("hard_block_candidates"), dict) else {}
    checks.append(_check_eq("ambiguity_prompt_to_multiple_targets_false", bool(hard.get("prompt_to_multiple_targets", False)), False))
    checks.append(_check_eq("ambiguity_prompt_to_multiple_tools_false", bool(hard.get("prompt_to_multiple_tools", False)), False))
    checks.append(_check_eq("ambiguity_prompt_tool_to_multiple_arguments_false", bool(hard.get("prompt_tool_to_multiple_arguments", False)), False))

    checks.append(
        _check_eq(
            "contamination_heldout_overlap_zero",
            contamination.get("combined_overlap", {}).get("heldout_validation"),
            {"prompt_overlap": 0, "target_overlap": 0, "source_case_id_overlap": 0},
        )
    )
    checks.append(
        _check_eq(
            "contamination_tool_holdout_overlap_zero",
            contamination.get("combined_overlap", {}).get("tool_holdout"),
            {"prompt_overlap": 0, "target_overlap": 0, "source_case_id_overlap": 0},
        )
    )

    commit = diagnostics.get("checks", {}).get("commitment_conversion_telemetry", {})
    checks.append(
        _check_true(
            "diagnostics_has_commitment_conversion_telemetry",
            bool(commit),
            "diagnostics missing commitment_conversion_telemetry block",
        )
    )

    top1 = float(commit.get("top1_behavioral_category_share", {}).get("top1_behavioral_category_share", 0.0) or 0.0)
    checks.append(
        _check_warn(
            "top1_behavioral_share_below_threshold",
            top1 <= MAX_TOP1_BEHAVIOR_SHARE,
            f"top1 behavioral share {top1:.6f} exceeds threshold {MAX_TOP1_BEHAVIOR_SHARE:.2f}",
        )
    )

    ratio = float(anchor.get("ratio", 0.0) or 0.0)
    checks.append(
        _check_warn(
            "anchor_dominance_ratio_below_threshold",
            ratio <= MAX_ANCHOR_DOMINANCE_RATIO,
            f"anchor dominance ratio {ratio:.6f} exceeds threshold {MAX_ANCHOR_DOMINANCE_RATIO:.2f}",
        )
    )

    checks.append(
        _check_true(
            "collapse_watch_has_abort_list",
            isinstance(collapse_watch.get("abort_or_halt_recommendation_if"), list)
            and len(collapse_watch.get("abort_or_halt_recommendation_if", [])) >= 6,
            "collapse watch artifact missing abort conditions",
        )
    )
    return checks


def _validate_dataset_rows(train_rows: list[dict[str, Any]], val_rows: list[dict[str, Any]]) -> list[CheckResult]:
    non_tool_train = sum(1 for row in train_rows if not _is_tool_row(row))
    non_tool_val = sum(1 for row in val_rows if not _is_tool_row(row))

    targeted_i9_rows = 0
    for row in train_rows + val_rows:
        tool = _tool_name(row)
        if tool not in TARGETED_TOOLS:
            continue
        meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        if bool(meta.get("intervention_i9_row", False)):
            targeted_i9_rows += 1

    checks = [
        _check_eq("non_tool_train_count_preserved", non_tool_train, EXPECTED_NON_TOOL_COUNTS["train"]),
        _check_eq("non_tool_val_count_preserved", non_tool_val, EXPECTED_NON_TOOL_COUNTS["val"]),
        _check_true(
            "i9_intervention_rows_present",
            targeted_i9_rows > 0,
            "no i9 intervention rows detected in dataset",
        ),
    ]
    return checks


def _summarize_results(checks: list[CheckResult]) -> dict[str, int]:
    out = {"pass": 0, "warn": 0, "fail": 0}
    for c in checks:
        out[c.status] = out.get(c.status, 0) + 1
    return out


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run i9 preflight validation checks.")

    parser.add_argument("--builder-script", default="/opt/ai-stack/assistant-training/scripts/build_stage_b_recovery_i9_dataset.py")
    parser.add_argument("--config-draft", default="/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_i9.config.draft.json")
    parser.add_argument("--run-manifest-draft", default="/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_i9.run_manifest.draft.json")
    parser.add_argument("--intervention-declaration", default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i9_intervention_declaration.json")
    parser.add_argument("--readiness-criteria", default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i9_training_eval_readiness_criteria.json")
    parser.add_argument("--risk-assessment", default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i9_expected_risk_assessment.json")
    parser.add_argument("--diagnostics-schema-template", default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i9_diagnostics_schema.template.json")

    parser.add_argument("--dataset-train-jsonl", default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i9_train.jsonl")
    parser.add_argument("--dataset-val-jsonl", default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i9_val.jsonl")
    parser.add_argument("--dataset-summary-json", default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i9_summary.json")

    parser.add_argument("--diagnostics-json", default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i9_dataset_diagnostics.json")
    parser.add_argument("--contamination-audit-json", default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i9_contamination_audit.json")
    parser.add_argument("--prompt-ambiguity-audit-json", default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i9_prompt_ambiguity_audit.json")
    parser.add_argument("--collapse-watch-json", default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i9_collapse_watch_telemetry.json")
    parser.add_argument("--anchor-dominance-json", default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i9_anchor_dominance_telemetry.json")

    parser.add_argument("--eval-heldout-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/heldout_validation.jsonl")
    parser.add_argument("--eval-tool-holdout-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/tool_holdout.jsonl")

    parser.add_argument("--output-json", default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i9_preflight_validation.json")
    parser.add_argument(
        "--attempt-open-approval-gate",
        action="store_true",
        help="Explicitly blocked: approvals cannot be opened in preflight phase.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.attempt_open_approval_gate:
        raise RuntimeError("approval-gate opening is prohibited in i9 preflight phase")

    paths = {
        "builder_script": Path(args.builder_script).resolve(),
        "config_draft": Path(args.config_draft).resolve(),
        "run_manifest_draft": Path(args.run_manifest_draft).resolve(),
        "intervention_declaration": Path(args.intervention_declaration).resolve(),
        "readiness_criteria": Path(args.readiness_criteria).resolve(),
        "risk_assessment": Path(args.risk_assessment).resolve(),
        "diagnostics_schema_template": Path(args.diagnostics_schema_template).resolve(),
        "dataset_train_jsonl": Path(args.dataset_train_jsonl).resolve(),
        "dataset_val_jsonl": Path(args.dataset_val_jsonl).resolve(),
        "dataset_summary_json": Path(args.dataset_summary_json).resolve(),
        "diagnostics_json": Path(args.diagnostics_json).resolve(),
        "contamination_audit_json": Path(args.contamination_audit_json).resolve(),
        "prompt_ambiguity_audit_json": Path(args.prompt_ambiguity_audit_json).resolve(),
        "collapse_watch_json": Path(args.collapse_watch_json).resolve(),
        "anchor_dominance_json": Path(args.anchor_dominance_json).resolve(),
        "eval_heldout_jsonl": Path(args.eval_heldout_jsonl).resolve(),
        "eval_tool_holdout_jsonl": Path(args.eval_tool_holdout_jsonl).resolve(),
    }

    _require_paths_exist(list(paths.values()))

    config = _load_json(paths["config_draft"])
    manifest = _load_json(paths["run_manifest_draft"])
    intervention = _load_json(paths["intervention_declaration"])
    readiness = _load_json(paths["readiness_criteria"])
    risk = _load_json(paths["risk_assessment"])
    diagnostics_schema = _load_json(paths["diagnostics_schema_template"])

    train_rows = _load_jsonl(paths["dataset_train_jsonl"])
    val_rows = _load_jsonl(paths["dataset_val_jsonl"])
    dataset_summary = _load_json(paths["dataset_summary_json"])

    diagnostics = _load_json(paths["diagnostics_json"])
    contamination = _load_json(paths["contamination_audit_json"])
    ambiguity = _load_json(paths["prompt_ambiguity_audit_json"])
    collapse_watch = _load_json(paths["collapse_watch_json"])
    anchor = _load_json(paths["anchor_dominance_json"])

    all_checks: list[CheckResult] = []
    all_checks.extend(_validate_builder_lock(paths["builder_script"]))
    all_checks.extend(_validate_config_manifest(config, manifest))
    all_checks.extend(_validate_templates(intervention, readiness, risk, diagnostics_schema))
    all_checks.extend(_validate_dataset_rows(train_rows, val_rows))
    all_checks.extend(_validate_generated_artifacts(dataset_summary, diagnostics, contamination, ambiguity, collapse_watch, anchor))

    # Independent overlap verification from raw eval splits.
    heldout_rows = _load_jsonl(paths["eval_heldout_jsonl"])
    tool_holdout_rows = _load_jsonl(paths["eval_tool_holdout_jsonl"])
    combined_rows = train_rows + val_rows

    heldout_overlap = _overlap_report(combined_rows, heldout_rows)
    tool_holdout_overlap = _overlap_report(combined_rows, tool_holdout_rows)

    all_checks.append(
        _check_eq(
            "raw_overlap_vs_heldout_zero",
            heldout_overlap,
            {"prompt_overlap": 0, "target_overlap": 0, "source_case_id_overlap": 0},
        )
    )
    all_checks.append(
        _check_eq(
            "raw_overlap_vs_tool_holdout_zero",
            tool_holdout_overlap,
            {"prompt_overlap": 0, "target_overlap": 0, "source_case_id_overlap": 0},
        )
    )

    summary = _summarize_results(all_checks)
    has_failures = summary.get("fail", 0) > 0

    report = {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "iteration": RUN_NAME,
        "status": "preflight_validation_completed" if not has_failures else "preflight_validation_failed",
        "summary": summary,
        "checks": [{"name": c.name, "status": c.status, "detail": c.detail} for c in all_checks],
        "overlap_reverification": {
            "heldout_validation": heldout_overlap,
            "tool_holdout": tool_holdout_overlap,
        },
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }

    out = Path(args.output_json).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not has_failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
