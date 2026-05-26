#!/usr/bin/env python3
"""
i8 preflight validation (implementation-completion phase).

What this script does:
- Validates draft configs/manifests/templates.
- Validates doctrine and invariants against existing reference data.
- Produces review-support outputs.

What this script does NOT do:
- No i8 dataset generation.
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

from i8_diagnostics_scaffold import build_full_diagnostics_report, scaffold_policy_defaults

RUN_NAME = "stage_b_llama31_8b_base_v1_i8"
TARGETED_TOOLS = ("rg_search", "read_file")
EXPECTED_NON_TOOL_COUNTS = {"train": 756, "val": 84}


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


def _collect_eval_exclusions(path: Path) -> set[str]:
    prompts: set[str] = set()
    for row in _load_jsonl(path):
        msgs = row.get("messages")
        if not isinstance(msgs, list):
            continue
        for msg in msgs:
            if isinstance(msg, dict) and msg.get("role") == "user":
                prompts.add(str(msg.get("content") or ""))
                break
    return prompts


def _validate_builder_lock(builder_script: Path) -> list[CheckResult]:
    text = builder_script.read_text(encoding="utf-8")
    return [
        _check_true(
            "builder_requires_explicit_enable_dataset_emission_flag",
            "--enable-dataset-emission" in text,
            "missing explicit --enable-dataset-emission generation gate",
        ),
        _check_true(
            "builder_requires_explicit_allow_generation_phase_flag",
            "--allow-generation-phase" in text,
            "missing explicit --allow-generation-phase generation gate",
        ),
        _check_true(
            "builder_has_fail_fast_generation_unlock_guard",
            "_fail_fast_generation_unlock" in text,
            "missing fail-fast generation unlock guard",
        ),
    ]


def _validate_config_templates(config: dict[str, Any], manifest: dict[str, Any]) -> list[CheckResult]:
    checks: list[CheckResult] = []

    checks.append(_check_eq("config_name", _nested_get(config, "name"), RUN_NAME))
    checks.append(_check_eq("config_safety_approved_to_run_false", _nested_get(config, "safety.approved_to_run"), False))
    checks.append(
        _check_eq(
            "config_do_not_start_training_automatically_true",
            _nested_get(config, "safety.do_not_start_training_automatically"),
            True,
        )
    )
    checks.append(_check_eq("manifest_name", _nested_get(manifest, "name"), RUN_NAME))
    checks.append(_check_eq("manifest_training_started_false", _nested_get(manifest, "training_started"), False))
    checks.append(_check_eq("manifest_approved_to_run_false", _nested_get(manifest, "review_gate.approved_to_run"), False))
    checks.append(
        _check_eq(
            "manifest_canonical_eval_path",
            _nested_get(manifest, "inputs.canonical_eval_manifest"),
            "/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json",
        )
    )

    return checks


def _validate_intervention_templates(
    intervention: dict[str, Any],
    contamination: dict[str, Any],
    diagnostics_schema: dict[str, Any],
    preflight_template: dict[str, Any],
    gate_template: dict[str, Any],
    dataset_summary_template: dict[str, Any],
) -> list[CheckResult]:
    checks: list[CheckResult] = []

    checks.append(
        _check_eq(
            "intervention_targeted_tools",
            tuple(_nested_get(intervention, "SCOPE.targeted_tools") or []),
            TARGETED_TOOLS,
        )
    )
    checks.append(
        _check_eq(
            "intervention_approval_false",
            _nested_get(intervention, "approval_state.approved_to_run"),
            False,
        )
    )
    checks.append(
        _check_eq(
            "contamination_max_overlap_zero",
            _nested_get(contamination, "blocking_policy.max_allowed_overlap"),
            0,
        )
    )
    checks.append(
        _check_eq(
            "contamination_fail_fast_true",
            _nested_get(contamination, "blocking_policy.fail_fast"),
            True,
        )
    )
    checks.append(
        _check_eq(
            "diagnostics_schema_has_style_bucket",
            bool(_nested_get(diagnostics_schema, "sections.style_bucket_analysis")),
            True,
        )
    )
    checks.append(
        _check_eq(
            "diagnostics_schema_has_skeleton",
            bool(_nested_get(diagnostics_schema, "sections.prompt_skeleton_concentration")),
            True,
        )
    )
    checks.append(
        _check_eq(
            "preflight_has_overlap_flow",
            any((x.get("name") == "overlap_audit") for x in (_nested_get(preflight_template, "flow_points") or []) if isinstance(x, dict)),
            True,
        )
    )
    checks.append(
        _check_eq(
            "gate_template_has_spill_guard",
            bool(_nested_get(gate_template, "gate_results.spill_guard")),
            True,
        )
    )
    checks.append(
        _check_eq(
            "dataset_summary_approval_false",
            _nested_get(dataset_summary_template, "approval_state.approved_to_run"),
            False,
        )
    )
    checks.append(
        _check_eq(
            "dataset_summary_approval_generate_false",
            _nested_get(dataset_summary_template, "approval_state.approved_to_generate_dataset"),
            False,
        )
    )

    return checks


def _validate_human_review_checklist(checklist_text: str) -> list[CheckResult]:
    required_markers = [
        "## Hard Blocks",
        "## Localized Intervention Integrity",
        "## Contamination / Overlap",
        "## Diversity / Anti-Homogenization",
        "## Overconstraint Risk",
        "## Decision",
    ]
    checks: list[CheckResult] = []
    for marker in required_markers:
        checks.append(
            _check_true(
                f"human_review_checklist_marker_{marker.replace(' ', '_').replace('/', '_')}",
                marker in checklist_text,
                f"missing checklist marker: {marker}",
            )
        )
    return checks


def _validate_prompt_ambiguity_audit(audit: dict[str, Any]) -> list[CheckResult]:
    hard = audit.get("hard_block_candidates", {}) if isinstance(audit.get("hard_block_candidates"), dict) else {}
    return [
        _check_eq(
            "prompt_ambiguity_prompt_to_multiple_targets_false",
            bool(hard.get("prompt_to_multiple_targets", False)),
            False,
        ),
        _check_eq(
            "prompt_ambiguity_prompt_to_multiple_tools_false",
            bool(hard.get("prompt_to_multiple_tools", False)),
            False,
        ),
        _check_eq(
            "prompt_ambiguity_prompt_tool_to_multiple_arguments_false",
            bool(hard.get("prompt_tool_to_multiple_arguments", False)),
            False,
        ),
    ]


def _validate_reference_invariants(train_rows: list[dict[str, Any]], val_rows: list[dict[str, Any]]) -> list[CheckResult]:
    non_tool_train = sum(1 for row in train_rows if not _is_tool_row(row))
    non_tool_val = sum(1 for row in val_rows if not _is_tool_row(row))

    checks = [
        _check_eq("reference_non_tool_train_count", non_tool_train, EXPECTED_NON_TOOL_COUNTS["train"]),
        _check_eq("reference_non_tool_val_count", non_tool_val, EXPECTED_NON_TOOL_COUNTS["val"]),
        _check_true(
            "reference_contains_targeted_tools",
            any(_tool_name(row) in TARGETED_TOOLS for row in train_rows + val_rows),
            "reference data has no targeted tool rows",
        ),
    ]
    return checks


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


def _validate_contamination_assumptions(train_rows: list[dict[str, Any]], heldout_path: Path, tool_holdout_path: Path) -> list[CheckResult]:
    prompts_train: set[str] = set()
    for row in train_rows:
        msgs = row.get("messages")
        if not isinstance(msgs, list):
            continue
        for msg in msgs:
            if isinstance(msg, dict) and msg.get("role") == "user":
                prompts_train.add(str(msg.get("content") or ""))
                break

    heldout_prompts = _collect_eval_exclusions(heldout_path)
    tool_holdout_prompts = _collect_eval_exclusions(tool_holdout_path)

    heldout_overlap = len(prompts_train.intersection(heldout_prompts))
    tool_holdout_overlap = len(prompts_train.intersection(tool_holdout_prompts))

    return [
        _check_warn(
            "reference_prompt_overlap_vs_heldout",
            heldout_overlap == 0,
            f"prompt overlap count={heldout_overlap}; treat as contamination-risk signal",
            "prompt overlap count=0",
        ),
        _check_warn(
            "reference_prompt_overlap_vs_tool_holdout",
            tool_holdout_overlap == 0,
            f"prompt overlap count={tool_holdout_overlap}; treat as contamination-risk signal",
            "prompt overlap count=0",
        ),
    ]


def _review_checklist() -> list[str]:
    return [
        "Confirm all i8 approval flags remain false across config/manifest/templates.",
        "Confirm builder still hard-stops before dataset emission.",
        "Confirm targeted tools remain rg_search/read_file only.",
        "Confirm concentration and style diagnostics do not indicate local-template collapse.",
        "Confirm forbidden-pattern scan has no intervention-layer hits before unlock request.",
    ]


def _summarize_results(checks: list[CheckResult]) -> dict[str, int]:
    out = {"pass": 0, "warn": 0, "fail": 0}
    for c in checks:
        if c.status not in out:
            out[c.status] = 0
        out[c.status] += 1
    return out


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run i8 preflight validation checks (non-executing phase).")
    parser.add_argument("--builder-script", default="/opt/ai-stack/assistant-training/scripts/build_stage_b_recovery_i8_dataset.py")
    parser.add_argument("--diagnostics-script", default="/opt/ai-stack/assistant-training/scripts/i8_diagnostics_scaffold.py")

    parser.add_argument("--config-draft", default="/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_i8.config.draft.json")
    parser.add_argument("--run-manifest-draft", default="/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_i8.run_manifest.draft.json")
    parser.add_argument("--intervention-template", default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i8_intervention_declaration.template.json")
    parser.add_argument("--gate-template", default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i8_parseability_spill_guard_gate_assessment.template.json")
    parser.add_argument("--contamination-template", default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i8_contamination_audit.template.json")
    parser.add_argument("--diagnostics-schema-template", default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i8_diagnostics_schema.template.json")
    parser.add_argument("--preflight-template", default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i8_preflight_validation_plan.template.json")
    parser.add_argument("--dataset-summary-template", default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i8_summary.template.json")
    parser.add_argument("--human-review-checklist-template", default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i8_human_review_checklist.template.md")

    parser.add_argument("--stage-b-train-jsonl", default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_train.jsonl")
    parser.add_argument("--stage-b-val-jsonl", default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_val.jsonl")
    parser.add_argument("--eval-heldout-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/heldout_validation.jsonl")
    parser.add_argument("--eval-tool-holdout-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/tool_holdout.jsonl")
    parser.add_argument("--prompt-ambiguity-audit-json", default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i8_prompt_ambiguity_audit.json")

    parser.add_argument("--output-json", default="")
    parser.add_argument(
        "--attempt-open-approval-gate",
        action="store_true",
        help="Explicitly blocked: approvals cannot be opened in preflight phase.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.attempt_open_approval_gate:
        raise RuntimeError("approval-gate opening is prohibited in i8 preflight phase")

    paths = {
        "builder_script": Path(args.builder_script).resolve(),
        "diagnostics_script": Path(args.diagnostics_script).resolve(),
        "config_draft": Path(args.config_draft).resolve(),
        "run_manifest_draft": Path(args.run_manifest_draft).resolve(),
        "intervention_template": Path(args.intervention_template).resolve(),
        "gate_template": Path(args.gate_template).resolve(),
        "contamination_template": Path(args.contamination_template).resolve(),
        "diagnostics_schema_template": Path(args.diagnostics_schema_template).resolve(),
        "preflight_template": Path(args.preflight_template).resolve(),
        "dataset_summary_template": Path(args.dataset_summary_template).resolve(),
        "human_review_checklist_template": Path(args.human_review_checklist_template).resolve(),
        "stage_b_train_jsonl": Path(args.stage_b_train_jsonl).resolve(),
        "stage_b_val_jsonl": Path(args.stage_b_val_jsonl).resolve(),
        "eval_heldout_jsonl": Path(args.eval_heldout_jsonl).resolve(),
        "eval_tool_holdout_jsonl": Path(args.eval_tool_holdout_jsonl).resolve(),
        "prompt_ambiguity_audit_json": Path(args.prompt_ambiguity_audit_json).resolve(),
    }
    required_paths = [v for k, v in paths.items() if k != "prompt_ambiguity_audit_json"]
    _require_paths_exist(required_paths)

    config = _load_json(paths["config_draft"])
    manifest = _load_json(paths["run_manifest_draft"])
    intervention = _load_json(paths["intervention_template"])
    gate_template = _load_json(paths["gate_template"])
    contamination = _load_json(paths["contamination_template"])
    diagnostics_schema = _load_json(paths["diagnostics_schema_template"])
    preflight_template = _load_json(paths["preflight_template"])
    dataset_summary_template = _load_json(paths["dataset_summary_template"])
    human_review_checklist_text = paths["human_review_checklist_template"].read_text(encoding="utf-8")
    prompt_ambiguity_audit = None
    if paths["prompt_ambiguity_audit_json"].exists():
        prompt_ambiguity_audit = _load_json(paths["prompt_ambiguity_audit_json"])

    train_rows = _load_jsonl(paths["stage_b_train_jsonl"])
    val_rows = _load_jsonl(paths["stage_b_val_jsonl"])

    all_checks: list[CheckResult] = []
    all_checks.extend(_validate_builder_lock(paths["builder_script"]))
    all_checks.extend(_validate_config_templates(config, manifest))
    all_checks.extend(
        _validate_intervention_templates(
            intervention,
            contamination,
            diagnostics_schema,
            preflight_template,
            gate_template,
            dataset_summary_template,
        )
    )
    all_checks.extend(_validate_human_review_checklist(human_review_checklist_text))
    if prompt_ambiguity_audit is not None:
        all_checks.extend(_validate_prompt_ambiguity_audit(prompt_ambiguity_audit))
    else:
        all_checks.append(
            _check_warn(
                "prompt_ambiguity_audit_present",
                False,
                f"missing prompt ambiguity audit artifact: {paths['prompt_ambiguity_audit_json']}",
            )
        )
    all_checks.extend(_validate_reference_invariants(train_rows, val_rows))
    all_checks.extend(_validate_contamination_assumptions(train_rows, paths["eval_heldout_jsonl"], paths["eval_tool_holdout_jsonl"]))

    policy = scaffold_policy_defaults()
    reference_tool_rows = [row for row in (train_rows + val_rows) if _is_tool_row(row)]
    diagnostics_report = build_full_diagnostics_report(reference_tool_rows, reference_rows=reference_tool_rows, policy=policy)

    # Doctrine-readiness checks from diagnostic outputs.
    diversity = diagnostics_report.get("review_support", {}).get("diversity_review_summary", {})
    anti = diagnostics_report.get("review_support", {}).get("anti_homogenization_summary", {})

    all_checks.append(
        _check_warn(
            "diversity_review_summary_pass",
            bool(diversity.get("pass", False)),
            f"diversity risks detected: {diversity.get('risk_flags', [])}",
        )
    )
    all_checks.append(
        _check_warn(
            "anti_homogenization_summary_pass",
            bool(anti.get("pass", False)),
            f"anti-homogenization risks detected: {anti.get('risk_signals', [])}",
        )
    )

    summary = _summarize_results(all_checks)
    has_failures = summary.get("fail", 0) > 0

    review_questions = {
        "fragile_points": [
            "Localized parse-anchor phrasing can still drift toward repetitive skeletons under hard budget caps.",
            "Blocking contamination on prompt/target/case overlap depends on strict source-case hygiene in incoming tool sources.",
        ],
        "hidden_homogenization_vectors": [
            "Deterministic anchor-variant assignment can still overrepresent one style bucket if source prompts are already skewed.",
            "Imperative-first prompts in rg_search/read_file can collapse into line-scoped command templates without active diversity monitoring.",
        ],
        "hidden_overconstraint_vectors": [
            "Overly strict forbidden-pattern expansion may remove too much lexical variety and reintroduce suppression dynamics.",
            "Parseability emphasis could over-privilege structural compliance tokens and reduce semantic disambiguation range.",
        ],
        "local_template_collapse_signals": [
            "targeted top1 skeleton share rising above 0.35",
            "targeted dominant style share rising above 0.75",
            "shrinking unique skeleton count in targeted tools across successive previews",
            "prompt-length deltas converging toward a narrow high-length band",
        ],
        "additional_diagnostics_needed": [
            "prompt-length delta analysis (implemented)",
            "intervention coverage accounting (implemented)",
            "targeted prompt sample extraction hooks (implemented)",
            "anti-homogenization summary rollup (implemented)",
        ],
    }

    report = {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "iteration": RUN_NAME,
        "status": "preflight_validation_completed_with_findings" if not has_failures else "preflight_validation_failed",
        "summary": summary,
        "checks": [
            {"name": c.name, "status": c.status, "detail": c.detail}
            for c in all_checks
        ],
        "diagnostics_reference_report": diagnostics_report,
        "human_review_support": {
            "review_checklist": _review_checklist(),
            "intervention_budget_summary": diagnostics_report.get("review_support", {}).get("intervention_budget_summary", {}),
            "targeted_prompt_samples": diagnostics_report.get("review_support", {}).get("targeted_prompt_samples", {}),
            "diversity_review_summary": diagnostics_report.get("review_support", {}).get("diversity_review_summary", {}),
            "anti_homogenization_summary": diagnostics_report.get("review_support", {}).get("anti_homogenization_summary", {}),
        },
        "required_review_questions": review_questions,
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }

    if args.output_json.strip():
        out = Path(args.output_json).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not has_failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
