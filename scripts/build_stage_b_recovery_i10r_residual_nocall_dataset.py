#!/usr/bin/env python3
"""
Build Stage B i10r ultra-local residual adversarial no-call seam dataset package.

Scope boundary:
- Additions-only localized dataset generation.
- No mutation of parent i10r_counterbalanced rows.
- No training or canonical eval execution.
- No approval-gate opening.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from i10_diagnostics_scaffold import (
    build_full_diagnostics_report,
    build_intervention_annotations,
    run_prompt_ambiguity_audit,
    scaffold_policy_defaults,
)

RUN_NAME = "stage_b_llama31_8b_base_v1_i10r_residual_nocall"
PARENT_ITERATION = "stage_b_llama31_8b_base_v1_i10r_counterbalanced"
REQUIRED_PARENT_CHECKPOINT = "stage_b_llama31_8b_base_v1_i10r_microprobe"
FORBIDDEN_PARENT_CHECKPOINT = "stage_b_llama31_8b_base_v1_i10r_nocall_probe"

EXPECTED_TOTAL_ADDITIONS = 6
EXPECTED_NO_CALL_REFUSAL_ROWS = 3
EXPECTED_VALID_TOOL_ROWS = 3
EXPECTED_PAIR_COUNT = 3
EXPECTED_UNCERTAINTY_ROWS = 0

TARGETED_TOOLS = ("read_file", "rg_search")
TARGET_FAMILY = "underspecified_path_search_todo"


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_json(path: Path) -> dict[str, Any]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise RuntimeError(f"expected object JSON at {path}")
    return obj


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            raw = line.strip()
            if not raw:
                continue
            try:
                row = json.loads(raw)
            except Exception as exc:
                raise RuntimeError(f"invalid JSONL at {path}:{line_no}: {exc}") from exc
            if not isinstance(row, dict):
                raise RuntimeError(f"invalid row type at {path}:{line_no}; expected object")
            rows.append(row)
    return rows


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _canonical_json_text(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha1_text(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def _row_hash(row: dict[str, Any]) -> str:
    return _sha1_text(_canonical_json_text(row))


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
            return _canonical_json_text({"tool_calls": tc})
        return str(msg.get("content") or "")
    return ""


def _source_case_id(row: dict[str, Any], fallback: str) -> str:
    meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    out = str(meta.get("source_case_id") or meta.get("case_id") or "").strip()
    return out or fallback


def _tool_name_from_assistant(row: dict[str, Any]) -> str:
    msgs = row.get("messages")
    if not isinstance(msgs, list):
        return ""
    for msg in msgs:
        if not isinstance(msg, dict) or msg.get("role") != "assistant":
            continue
        tc = msg.get("tool_calls")
        if not isinstance(tc, list) or not tc or not isinstance(tc[0], dict):
            return ""
        fn = tc[0].get("function")
        if not isinstance(fn, dict):
            return ""
        return str(fn.get("name") or "").strip()
    return ""


def _prompt_overlap(candidate_rows: list[dict[str, Any]], eval_rows: list[dict[str, Any]]) -> dict[str, int]:
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


def _build_contamination_audit(
    train_rows: list[dict[str, Any]],
    val_rows: list[dict[str, Any]],
    eval_map: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    combined = train_rows + val_rows
    return {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "iteration": RUN_NAME,
        "status": "completed",
        "train_overlap": {k: _prompt_overlap(train_rows, v) for k, v in eval_map.items()},
        "val_overlap": {k: _prompt_overlap(val_rows, v) for k, v in eval_map.items()},
        "combined_overlap": {k: _prompt_overlap(combined, v) for k, v in eval_map.items()},
        "blocking_policy": {
            "heldout_tool_holdout_max_allowed_overlap": 0,
            "fail_fast": True,
        },
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }


def _fail_fast_contamination(audit: dict[str, Any]) -> None:
    for split_name in ("heldout_validation", "tool_holdout"):
        overlap = audit.get("combined_overlap", {}).get(split_name, {})
        if overlap != {"prompt_overlap": 0, "target_overlap": 0, "source_case_id_overlap": 0}:
            raise RuntimeError(f"contamination overlap detected in {split_name}: {overlap}")


def _system_prompt_from_parent(rows: list[dict[str, Any]]) -> str:
    for row in rows:
        msgs = row.get("messages")
        if not isinstance(msgs, list):
            continue
        for msg in msgs:
            if isinstance(msg, dict) and msg.get("role") == "system":
                return str(msg.get("content") or "").strip()
    raise RuntimeError("unable to resolve system prompt from parent dataset")


def _base_meta(case_id: str, *, category: str, tool: str | None, pair_id: str, boundary_valid: bool) -> dict[str, Any]:
    meta: dict[str, Any] = {
        "source": "i10r_residual_nocall_seam_builder",
        "source_case_id": case_id,
        "synthetic": True,
        "stage_split": "B_RECOVERY_I10R_RESIDUAL_NOCALL",
        "recovery_batch": "B_RECOVERY_I10R_RESIDUAL_NOCALL",
        "category": category,
        "intervention_scope": "i10r_residual_nocall_seam_restoration",
        "intervention_targeted_family": TARGET_FAMILY,
        "intervention_forbidden_global_pressure": True,
        "intervention_objective": "repair_remaining_underspecified_path_todo_nocall_boundary_without_regressing_procedural_gains",
        "intervention_tool_family": tool or "none",
        "i10r_residual_nocall_row": True,
        "i10r_residual_nocall_family": TARGET_FAMILY,
        "i10r_residual_nocall_block": "residual_nocall_contrastive_pair_block_v1",
        "i10r_residual_nocall_pair_id": pair_id,
        "i10r_residual_nocall_boundary_valid": boundary_valid,
    }
    if tool is not None:
        meta["tool"] = tool
    return meta


def _rg_search_assistant_msg(path: str, pattern: str) -> dict[str, Any]:
    return {
        "role": "assistant",
        "tool_calls": [
            {
                "type": "function",
                "function": {
                    "name": "rg_search",
                    "arguments": {
                        "path": path,
                        "pattern": pattern,
                    },
                },
            }
        ],
    }


def _build_additions(system_prompt: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    pair_specs = [
        {
            "pair_id": "pair_01",
            "split": "train",
            "path": "/opt/ai-stack/runtimes/assistant-runtime/server/agent.py",
            "token": "TODO_RESIDUAL_SEAM_01",
            "bad_prompt": "Find TODOs in code but do not provide the project path. Pattern TODO_RESIDUAL_SEAM_01 should be used; proceed anyway.",
            "good_prompt": "Find TODO_RESIDUAL_SEAM_01 in /opt/ai-stack/runtimes/assistant-runtime/server/agent.py and return one canonical rg_search payload.",
            "bad_refusal": "Please provide the project path before I can run a TODO search.",
        },
        {
            "pair_id": "pair_02",
            "split": "train",
            "path": "/opt/ai-stack/runtimes/assistant-runtime/server/router.py",
            "token": "TODO_RESIDUAL_SEAM_02",
            "bad_prompt": "Find TODOs in code but do not provide the project path. Use token TODO_RESIDUAL_SEAM_02 and continue.",
            "good_prompt": "Search /opt/ai-stack/runtimes/assistant-runtime/server/router.py for TODO_RESIDUAL_SEAM_02 with one canonical rg_search payload.",
            "bad_refusal": "I need the repository or file path before issuing a TODO search call.",
        },
        {
            "pair_id": "pair_03",
            "split": "val",
            "path": "/mnt/services/runtimes/assistant-runtime/server/telemetry.py",
            "token": "TODO_RESIDUAL_SEAM_03",
            "bad_prompt": "Find TODOs in code but do not provide the project path. Token TODO_RESIDUAL_SEAM_03 is all you get.",
            "good_prompt": "Search /mnt/services/runtimes/assistant-runtime/server/telemetry.py for TODO_RESIDUAL_SEAM_03 and emit one canonical rg_search payload.",
            "bad_refusal": "I cannot run that TODO search without a concrete project path.",
        },
    ]

    train_additions: list[dict[str, Any]] = []
    val_additions: list[dict[str, Any]] = []
    pair_audit: list[dict[str, Any]] = []

    def add_row(split: str, row: dict[str, Any]) -> None:
        if split == "train":
            train_additions.append(row)
        elif split == "val":
            val_additions.append(row)
        else:
            raise RuntimeError(f"unsupported split: {split}")

    for spec in pair_specs:
        pair_id = str(spec["pair_id"])
        split = str(spec["split"])
        path = str(spec["path"])
        token = str(spec["token"])

        bad_case = f"i10r_residual_{pair_id}_bad"
        bad_meta = _base_meta(
            bad_case,
            category="adversarial_malformed",
            tool=None,
            pair_id=pair_id,
            boundary_valid=False,
        )
        bad_meta.update(
            {
                "i10r_residual_nocall_semantic_token": token,
                "i10r_residual_nocall_target_path": None,
                "i10r_residual_nocall_target_pattern": "TODO",
                "i10r_residual_nocall_query_archetype": "underspecified_path_todo_search",
            }
        )
        bad_row = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": str(spec["bad_prompt"])},
                {"role": "assistant", "content": str(spec["bad_refusal"])},
            ],
            "metadata": bad_meta,
        }
        add_row(split, bad_row)

        good_case = f"i10r_residual_{pair_id}_good"
        good_meta = _base_meta(
            good_case,
            category="tool_positive",
            tool="rg_search",
            pair_id=pair_id,
            boundary_valid=True,
        )
        good_meta.update(
            {
                "i10r_residual_nocall_semantic_token": token,
                "i10r_residual_nocall_target_path": path,
                "i10r_residual_nocall_target_pattern": token,
                "i10r_residual_nocall_query_archetype": "underspecified_path_todo_search",
            }
        )
        good_row = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": str(spec["good_prompt"])},
                _rg_search_assistant_msg(path, token),
            ],
            "metadata": good_meta,
        }
        add_row(split, good_row)

        pair_audit.append(
            {
                "pair_id": pair_id,
                "split": split,
                "semantic_token": token,
                "path": path,
                "bad_case_id": bad_case,
                "good_case_id": good_case,
            }
        )

    additions_meta = {
        "train_additions": len(train_additions),
        "val_additions": len(val_additions),
        "total_additions": len(train_additions) + len(val_additions),
        "pair_audit": pair_audit,
    }
    return train_additions, val_additions, additions_meta


def _build_localized_diff_verification(
    *,
    parent_train: list[dict[str, Any]],
    parent_val: list[dict[str, Any]],
    revised_train: list[dict[str, Any]],
    revised_val: list[dict[str, Any]],
    train_additions: list[dict[str, Any]],
    val_additions: list[dict[str, Any]],
) -> dict[str, Any]:
    parent_train_hashes = [_row_hash(r) for r in parent_train]
    parent_val_hashes = [_row_hash(r) for r in parent_val]
    revised_train_prefix_hashes = [_row_hash(r) for r in revised_train[: len(parent_train)]]
    revised_val_prefix_hashes = [_row_hash(r) for r in revised_val[: len(parent_val)]]
    changed_train = [i + 1 for i, (a, b) in enumerate(zip(parent_train_hashes, revised_train_prefix_hashes)) if a != b]
    changed_val = [i + 1 for i, (a, b) in enumerate(zip(parent_val_hashes, revised_val_prefix_hashes)) if a != b]

    additions = train_additions + val_additions
    add_blocks = Counter(str((r.get("metadata") or {}).get("i10r_residual_nocall_block") or "") for r in additions)
    add_tools = Counter(_tool_name_from_assistant(r) or "no_tool" for r in additions)
    add_family = Counter(
        str((r.get("metadata") or {}).get("i10r_residual_nocall_family") or "")
        for r in additions
    )

    pair_rows: dict[str, list[dict[str, Any]]] = {}
    for row in additions:
        meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        pair_id = str(meta.get("i10r_residual_nocall_pair_id") or "").strip()
        if not pair_id:
            continue
        pair_rows.setdefault(pair_id, []).append(row)

    pair_checks: list[dict[str, Any]] = []
    for pair in sorted(pair_rows.keys()):
        rows = pair_rows[pair]
        bad = [r for r in rows if not bool((r.get("metadata") or {}).get("i10r_residual_nocall_boundary_valid", False))]
        good = [r for r in rows if bool((r.get("metadata") or {}).get("i10r_residual_nocall_boundary_valid", False))]
        token_set = {str((r.get("metadata") or {}).get("i10r_residual_nocall_semantic_token") or "") for r in rows}
        path_set = {str((r.get("metadata") or {}).get("i10r_residual_nocall_target_path") or "") for r in good}
        pair_checks.append(
            {
                "pair_id": pair,
                "rows": len(rows),
                "bad_rows": len(bad),
                "good_rows": len(good),
                "semantic_token_consistent": len(token_set) == 1,
                "good_path_present": len(path_set) == 1,
                "pass": len(rows) == 2 and len(bad) == 1 and len(good) == 1 and len(token_set) == 1 and len(path_set) == 1,
            }
        )

    all_pair_pass = all(bool(x.get("pass", False)) for x in pair_checks) and len(pair_checks) == EXPECTED_PAIR_COUNT

    localized_only = all(str((r.get("metadata") or {}).get("i10r_residual_nocall_family") or "") == TARGET_FAMILY for r in additions)

    no_tool_rows = sum(1 for r in additions if (_tool_name_from_assistant(r) == ""))
    tool_rows = len(additions) - no_tool_rows

    return {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "iteration": RUN_NAME,
        "status": "completed",
        "operation_mode": "additions_only",
        "expected_total_additions": EXPECTED_TOTAL_ADDITIONS,
        "actual_total_additions": len(additions),
        "additions_exact_match": len(additions) == EXPECTED_TOTAL_ADDITIONS,
        "parent_counts": {
            "train_rows": len(parent_train),
            "val_rows": len(parent_val),
        },
        "revised_counts": {
            "train_rows": len(revised_train),
            "val_rows": len(revised_val),
        },
        "existing_rows_changed": {
            "train_changed_count": len(changed_train),
            "val_changed_count": len(changed_val),
            "train_changed_row_indices_sample": changed_train[:20],
            "val_changed_row_indices_sample": changed_val[:20],
            "pass": len(changed_train) == 0 and len(changed_val) == 0,
        },
        "additions_breakdown": {
            "train_additions": len(train_additions),
            "val_additions": len(val_additions),
            "block_distribution": dict(sorted(add_blocks.items(), key=lambda kv: kv[0])),
            "tool_distribution": dict(sorted(add_tools.items(), key=lambda kv: kv[0])),
            "family_distribution": dict(sorted(add_family.items(), key=lambda kv: kv[0])),
            "no_tool_rows": no_tool_rows,
            "tool_rows": tool_rows,
        },
        "localization_checks": {
            "all_rows_localized_family": localized_only,
            "localized_family_expected": [TARGET_FAMILY],
            "pass": localized_only,
        },
        "contrastive_pair_validation": {
            "expected_pair_count": EXPECTED_PAIR_COUNT,
            "pair_count": len(pair_checks),
            "all_pairs_pass": all_pair_pass,
            "pairs": pair_checks,
        },
        "residual_block_validation": {
            "expected_refusal_rows": EXPECTED_NO_CALL_REFUSAL_ROWS,
            "actual_refusal_rows": no_tool_rows,
            "expected_valid_tool_rows": EXPECTED_VALID_TOOL_ROWS,
            "actual_valid_tool_rows": tool_rows,
            "expected_block_rows": EXPECTED_TOTAL_ADDITIONS,
            "actual_block_rows": add_blocks.get("residual_nocall_contrastive_pair_block_v1", 0),
            "pass": (
                no_tool_rows == EXPECTED_NO_CALL_REFUSAL_ROWS
                and tool_rows == EXPECTED_VALID_TOOL_ROWS
                and add_blocks.get("residual_nocall_contrastive_pair_block_v1", 0) == EXPECTED_TOTAL_ADDITIONS
            ),
        },
        "uncertainty_conditioning_validation": {
            "expected_rows": EXPECTED_UNCERTAINTY_ROWS,
            "actual_rows": add_blocks.get("uncertainty_conditioning", 0),
            "pass": add_blocks.get("uncertainty_conditioning", 0) == EXPECTED_UNCERTAINTY_ROWS,
        },
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }


def _build_anti_regression_telemetry(
    *,
    additions: list[dict[str, Any]],
    diagnostics: dict[str, Any],
    counterbalanced_probe_behavior: dict[str, Any],
) -> dict[str, Any]:
    prompts = [_user_prompt(r) for r in additions]
    literal_anchor = sum(1 for p in prompts if "tool_calls" in p.lower())
    paraphrastic_anchor = sum(1 for p in prompts if ("tool call" in p.lower() or "function call" in p.lower()))
    no_anchor = len(prompts) - literal_anchor - paraphrastic_anchor

    annotations = build_intervention_annotations(additions, targeted_tools=TARGETED_TOOLS)
    sk = Counter(str(a.get("skeleton_id") or "") for a in annotations)
    top1 = max(sk.values()) / len(additions) if additions and sk else 0.0

    tool_rows = sum(1 for r in additions if _tool_name_from_assistant(r))
    refusal_rows = len(additions) - tool_rows

    anchor_ratio = (literal_anchor / len(additions)) if additions else 0.0

    base_ctx = counterbalanced_probe_behavior.get("comparative_context", {}).get("i10r_counterbalanced_probe", {})
    baseline = {
        "read_file_exact_valid_rate": base_ctx.get("read_file_exact_valid_rate"),
        "read_file_symbol_name_exact_valid_rate": base_ctx.get("read_file_symbol_name_exact_valid_rate"),
        "scalar_substitution_share": base_ctx.get("scalar_substitution_share"),
        "direct_answer_substitution_share": base_ctx.get("direct_answer_substitution_share"),
        "no_anchor_exact_share": (base_ctx.get("anchor_exact_shares", {}) or {}).get("no_anchor_phrase"),
        "wrapper_leakage": base_ctx.get("wrapper_leakage"),
    }

    risk_flags = {
        "literal_anchor_ratio_high": anchor_ratio > 0.50,
        "top1_skeleton_share_high": top1 > 0.60,
        "unexpected_tool_mix": tool_rows != EXPECTED_VALID_TOOL_ROWS,
        "unexpected_refusal_mix": refusal_rows != EXPECTED_NO_CALL_REFUSAL_ROWS,
        "read_file_additions_present": any(_tool_name_from_assistant(r) == "read_file" for r in additions),
    }

    return {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "iteration": RUN_NAME,
        "status": "completed",
        "baseline_metrics_from_i10r_counterbalanced_probe": baseline,
        "dataset_addition_profile": {
            "total_additions": len(additions),
            "tool_rows": tool_rows,
            "refusal_rows": refusal_rows,
            "anchor_distribution": {
                "literal_tool_calls": literal_anchor,
                "paraphrastic_tool_call": paraphrastic_anchor,
                "no_anchor_phrase": no_anchor,
            },
            "literal_anchor_ratio": round(anchor_ratio, 6),
            "top1_skeleton_share_additions": round(top1, 6),
            "prompt_uniqueness_ratio_additions": round((len(set(prompts)) / len(prompts)) if prompts else 0.0, 6),
        },
        "anti_regression_risk_flags": risk_flags,
        "anti_regression_risk_pass": not any(risk_flags.values()),
        "diagnostics_snapshot": {
            "forbidden_pattern_hits": diagnostics.get("checks", {}).get("forbidden_pattern_scan", {}).get("total_hits"),
            "diversity_pass": diagnostics.get("review_support", {}).get("diversity_review_summary", {}).get("pass"),
            "anti_homogenization_pass": diagnostics.get("review_support", {}).get("anti_homogenization_summary", {}).get(
                "pass"
            ),
        },
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }


def _build_summary(
    *,
    parent_train_rows: int,
    parent_val_rows: int,
    revised_train_rows: int,
    revised_val_rows: int,
    localized_diff: dict[str, Any],
) -> dict[str, Any]:
    return {
        "generated_utc": _now_utc(),
        "iteration": RUN_NAME,
        "lineage": {
            "parent_dataset_iteration": PARENT_ITERATION,
            "required_parent_checkpoint": REQUIRED_PARENT_CHECKPOINT,
            "forbidden_parent_checkpoint": FORBIDDEN_PARENT_CHECKPOINT,
            "objective": "ultra_local_residual_adversarial_nocall_seam_restoration",
            "targeted_families": [TARGET_FAMILY],
            "operation_mode": "additions_only",
        },
        "composition": {
            "parent_train_rows": parent_train_rows,
            "parent_val_rows": parent_val_rows,
            "revised_train_rows": revised_train_rows,
            "revised_val_rows": revised_val_rows,
            "rows_added_train": revised_train_rows - parent_train_rows,
            "rows_added_val": revised_val_rows - parent_val_rows,
            "rows_added_total": (revised_train_rows + revised_val_rows) - (parent_train_rows + parent_val_rows),
            "rows_altered_existing": 0,
            "rows_replaced": 0,
            "rows_thinned": 0,
        },
        "localized_diff_summary": {
            "additions_exact_match": localized_diff.get("additions_exact_match"),
            "existing_rows_unchanged": localized_diff.get("existing_rows_changed", {}).get("pass"),
            "localization_pass": localized_diff.get("localization_checks", {}).get("pass"),
            "pair_validation_pass": localized_diff.get("contrastive_pair_validation", {}).get("all_pairs_pass"),
            "residual_block_pass": localized_diff.get("residual_block_validation", {}).get("pass"),
            "uncertainty_rows_eq_0_pass": localized_diff.get("uncertainty_conditioning_validation", {}).get("pass"),
        },
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }


def _write_human_review_package_md(report: dict[str, Any], out_path: Path) -> None:
    lines: list[str] = []
    lines.append("# Stage B i10r Residual No-Call Human Review Package")
    lines.append("")
    lines.append(f"- Generated UTC: {report.get('generated_utc')}")
    lines.append(f"- Iteration: {report.get('iteration')}")
    lines.append("")
    lines.append("## Composition")
    comp = report.get("composition", {})
    lines.append(f"- Added rows total: {comp.get('rows_added_total')}")
    lines.append(f"- Added rows train: {comp.get('rows_added_train')}")
    lines.append(f"- Added rows val: {comp.get('rows_added_val')}")
    lines.append(f"- Altered existing rows: {comp.get('rows_altered_existing')}")
    lines.append("")
    lines.append("## Localization")
    diff = report.get("localized_diff_checks", {})
    lines.append(f"- additions_exact_match: {diff.get('additions_exact_match')}")
    lines.append(f"- existing_rows_unchanged: {diff.get('existing_rows_unchanged')}")
    lines.append(f"- localized_family_only: {diff.get('localized_family_only')}")
    lines.append(f"- contrastive_pairs_pass: {diff.get('contrastive_pairs_pass')}")
    lines.append(f"- residual_block_pass: {diff.get('residual_block_pass')}")
    lines.append("")
    lines.append("## Hygiene")
    hygiene = report.get("hygiene", {})
    lines.append(f"- ambiguity_hard_blocks_clean: {hygiene.get('ambiguity_hard_blocks_clean')}")
    lines.append(f"- heldout_overlap_zero: {hygiene.get('heldout_overlap_zero')}")
    lines.append(f"- tool_holdout_overlap_zero: {hygiene.get('tool_holdout_overlap_zero')}")
    lines.append(f"- forbidden_pattern_hits_zero: {hygiene.get('forbidden_pattern_hits_zero')}")
    lines.append("")
    lines.append("## Anti-Regression")
    anti = report.get("anti_regression", {})
    lines.append(f"- additions_anchor_distribution: {anti.get('additions_anchor_distribution')}")
    lines.append(f"- top1_skeleton_share_additions: {anti.get('top1_skeleton_share_additions')}")
    lines.append(f"- anti_regression_risk_pass: {anti.get('anti_regression_risk_pass')}")
    lines.append(f"- risk_flags: {anti.get('risk_flags')}")
    lines.append("")
    lines.append("## Recommendation")
    lines.append(f"- {report.get('recommendation')}")
    lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _build_preflight_validation(
    *,
    localized_diff: dict[str, Any],
    ambiguity_audit: dict[str, Any],
    contamination_audit: dict[str, Any],
    diagnostics: dict[str, Any],
    anti_regression: dict[str, Any],
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def add_check(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "status": "pass" if ok else "fail", "detail": detail})

    hard = ambiguity_audit.get("hard_block_candidates", {}) if isinstance(ambiguity_audit.get("hard_block_candidates"), dict) else {}
    heldout = contamination_audit.get("combined_overlap", {}).get("heldout_validation")
    tool_holdout = contamination_audit.get("combined_overlap", {}).get("tool_holdout")
    forbidden_hits = int(diagnostics.get("checks", {}).get("forbidden_pattern_scan", {}).get("total_hits", 0) or 0)
    diversity_pass = bool(diagnostics.get("review_support", {}).get("diversity_review_summary", {}).get("pass", False))
    anti_h_pass = bool(diagnostics.get("review_support", {}).get("anti_homogenization_summary", {}).get("pass", False))

    add_check(
        "exactly_6_rows_added",
        bool(localized_diff.get("additions_exact_match", False)),
        f"actual_total_additions={localized_diff.get('actual_total_additions')}",
    )
    add_check(
        "no_existing_rows_changed",
        bool(localized_diff.get("existing_rows_changed", {}).get("pass", False)),
        f"existing_rows_changed={localized_diff.get('existing_rows_changed')}",
    )
    add_check(
        "localized_family_only",
        bool(localized_diff.get("localization_checks", {}).get("pass", False)),
        f"localization={localized_diff.get('localization_checks')}",
    )
    add_check(
        "contrastive_pairs_valid",
        bool(localized_diff.get("contrastive_pair_validation", {}).get("all_pairs_pass", False)),
        f"pair_validation={localized_diff.get('contrastive_pair_validation', {}).get('pair_count')}",
    )
    add_check(
        "residual_block_distribution_exact",
        bool(localized_diff.get("residual_block_validation", {}).get("pass", False)),
        f"residual_block={localized_diff.get('residual_block_validation')}",
    )
    add_check(
        "uncertainty_rows_eq_0",
        bool(localized_diff.get("uncertainty_conditioning_validation", {}).get("pass", False)),
        f"uncertainty={localized_diff.get('uncertainty_conditioning_validation')}",
    )
    add_check(
        "ambiguity_hard_blocks_clean",
        (not bool(hard.get("prompt_to_multiple_targets", False)))
        and (not bool(hard.get("prompt_to_multiple_tools", False)))
        and (not bool(hard.get("prompt_tool_to_multiple_arguments", False))),
        f"hard_blocks={hard}",
    )
    add_check(
        "heldout_overlap_zero",
        heldout == {"prompt_overlap": 0, "target_overlap": 0, "source_case_id_overlap": 0},
        f"heldout={heldout}",
    )
    add_check(
        "tool_holdout_overlap_zero",
        tool_holdout == {"prompt_overlap": 0, "target_overlap": 0, "source_case_id_overlap": 0},
        f"tool_holdout={tool_holdout}",
    )
    add_check("forbidden_pattern_hits_zero", forbidden_hits == 0, f"total_hits={forbidden_hits}")
    add_check("diversity_pass", diversity_pass, f"diversity_pass={diversity_pass}")
    add_check("anti_homogenization_pass", anti_h_pass, f"anti_homogenization_pass={anti_h_pass}")
    add_check(
        "hidden_anchor_concentration_clear",
        not bool(anti_regression.get("anti_regression_risk_flags", {}).get("literal_anchor_ratio_high", True)),
        f"literal_anchor_ratio={anti_regression.get('dataset_addition_profile', {}).get('literal_anchor_ratio')}",
    )

    fail_count = sum(1 for c in checks if c["status"] == "fail")
    return {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "iteration": RUN_NAME,
        "status": "preflight_validation_completed" if fail_count == 0 else "preflight_validation_failed",
        "summary": {
            "pass": sum(1 for c in checks if c["status"] == "pass"),
            "fail": fail_count,
        },
        "checks": checks,
        "all_critical_checks_pass": fail_count == 0,
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build ultra-local i10r residual no-call seam dataset package.")
    parser.add_argument(
        "--parent-train-jsonl",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i10r_counterbalanced_train.jsonl",
    )
    parser.add_argument(
        "--parent-val-jsonl",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i10r_counterbalanced_val.jsonl",
    )
    parser.add_argument(
        "--parent-summary-json",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i10r_counterbalanced_summary.json",
    )
    parser.add_argument(
        "--i10r-counterbalanced-probe-behavior-json",
        default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_counterbalanced_probe_behavioral_review_package.json",
    )
    parser.add_argument(
        "--i9-behavioral-review-json",
        default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i9_behavioral_review_package.json",
    )
    parser.add_argument(
        "--eval-heldout-jsonl",
        default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/heldout_validation.jsonl",
    )
    parser.add_argument(
        "--eval-tool-holdout-jsonl",
        default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/tool_holdout.jsonl",
    )
    parser.add_argument(
        "--eval-no-call-jsonl",
        default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/no_call.jsonl",
    )
    parser.add_argument(
        "--eval-adversarial-jsonl",
        default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/adversarial.jsonl",
    )
    parser.add_argument(
        "--eval-direct-answer-jsonl",
        default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/direct_answer.jsonl",
    )
    parser.add_argument("--output-data-root", default="/opt/ai-stack/assistant-training/data/v1_0")
    parser.add_argument("--output-report-root", default="/opt/ai-stack/assistant-training/manifests/reports")
    parser.add_argument("--enable-dataset-generation", action="store_true")
    parser.add_argument("--allow-residual-nocall-seam-phase", action="store_true")
    parser.add_argument("--apply-residual-nocall-seam-design", action="store_true")
    return parser.parse_args()


def _fail_fast_unlock(args: argparse.Namespace) -> None:
    if not args.enable_dataset_generation:
        raise RuntimeError("dataset generation requires --enable-dataset-generation")
    if not args.allow_residual_nocall_seam_phase:
        raise RuntimeError("dataset generation requires --allow-residual-nocall-seam-phase")
    if not args.apply_residual_nocall_seam_design:
        raise RuntimeError("dataset generation requires --apply-residual-nocall-seam-design")


def _fail_fast_inputs(paths: list[Path]) -> None:
    missing = [str(p) for p in paths if not p.exists()]
    if missing:
        raise RuntimeError("missing required input(s):\n- " + "\n- ".join(missing))


def main() -> int:
    args = parse_args()
    _fail_fast_unlock(args)

    parent_train_path = Path(args.parent_train_jsonl).resolve()
    parent_val_path = Path(args.parent_val_jsonl).resolve()
    parent_summary_path = Path(args.parent_summary_json).resolve()
    counterbalanced_probe_behavior_path = Path(args.i10r_counterbalanced_probe_behavior_json).resolve()
    i9_behavior_path = Path(args.i9_behavioral_review_json).resolve()

    eval_heldout = Path(args.eval_heldout_jsonl).resolve()
    eval_tool_holdout = Path(args.eval_tool_holdout_jsonl).resolve()
    eval_no_call = Path(args.eval_no_call_jsonl).resolve()
    eval_adversarial = Path(args.eval_adversarial_jsonl).resolve()
    eval_direct_answer = Path(args.eval_direct_answer_jsonl).resolve()

    data_root = Path(args.output_data_root).resolve()
    report_root = Path(args.output_report_root).resolve()

    out_train = data_root / "dataset_v1_0_stage_b_recovery_i10r_residual_nocall_train.jsonl"
    out_val = data_root / "dataset_v1_0_stage_b_recovery_i10r_residual_nocall_val.jsonl"
    out_summary = data_root / "dataset_v1_0_stage_b_recovery_i10r_residual_nocall_summary.json"
    out_diagnostics = report_root / "stage_b_v1_i10r_residual_nocall_dataset_diagnostics.json"
    out_ambiguity = report_root / "stage_b_v1_i10r_residual_nocall_prompt_ambiguity_audit.json"
    out_contamination = report_root / "stage_b_v1_i10r_residual_nocall_contamination_audit.json"
    out_localized_diff = report_root / "stage_b_v1_i10r_residual_nocall_localized_diff_verification.json"
    out_anti_regression = report_root / "stage_b_v1_i10r_residual_nocall_anti_regression_telemetry.json"
    out_review_json = report_root / "stage_b_v1_i10r_residual_nocall_human_review_package.json"
    out_review_md = report_root / "stage_b_v1_i10r_residual_nocall_human_review_package.md"
    out_preflight = report_root / "stage_b_v1_i10r_residual_nocall_preflight_validation.json"

    required_parent_manifest_path = Path(
        "/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_i10r_microprobe.run_manifest.json"
    ).resolve()
    forbidden_parent_manifest_path = Path(
        "/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_i10r_nocall_probe.run_manifest.json"
    ).resolve()

    _fail_fast_inputs(
        [
            parent_train_path,
            parent_val_path,
            parent_summary_path,
            counterbalanced_probe_behavior_path,
            i9_behavior_path,
            eval_heldout,
            eval_tool_holdout,
            eval_no_call,
            eval_adversarial,
            eval_direct_answer,
            required_parent_manifest_path,
            forbidden_parent_manifest_path,
        ]
    )

    parent_summary = _load_json(parent_summary_path)
    if str(parent_summary.get("iteration") or "") != PARENT_ITERATION:
        raise RuntimeError(
            f"unexpected parent iteration in summary: {parent_summary.get('iteration')} (expected {PARENT_ITERATION})"
        )
    if parent_train_path.name != "dataset_v1_0_stage_b_recovery_i10r_counterbalanced_train.jsonl":
        raise RuntimeError(f"parent train path mismatch: {parent_train_path.name}")
    if parent_val_path.name != "dataset_v1_0_stage_b_recovery_i10r_counterbalanced_val.jsonl":
        raise RuntimeError(f"parent val path mismatch: {parent_val_path.name}")
    if parent_summary_path.name != "dataset_v1_0_stage_b_recovery_i10r_counterbalanced_summary.json":
        raise RuntimeError(f"parent summary path mismatch: {parent_summary_path.name}")

    lineage = parent_summary.get("lineage") if isinstance(parent_summary.get("lineage"), dict) else {}
    if str(lineage.get("required_parent_checkpoint") or "") != REQUIRED_PARENT_CHECKPOINT:
        raise RuntimeError(
            f"parent summary required checkpoint mismatch: {lineage.get('required_parent_checkpoint')} != {REQUIRED_PARENT_CHECKPOINT}"
        )
    if str(lineage.get("forbidden_parent_checkpoint") or "") != FORBIDDEN_PARENT_CHECKPOINT:
        raise RuntimeError(
            f"parent summary forbidden checkpoint mismatch: {lineage.get('forbidden_parent_checkpoint')} != {FORBIDDEN_PARENT_CHECKPOINT}"
        )

    required_parent_manifest = _load_json(required_parent_manifest_path)
    if str(required_parent_manifest.get("name") or "") != REQUIRED_PARENT_CHECKPOINT:
        raise RuntimeError(
            f"required parent manifest mismatch: {required_parent_manifest.get('name')} != {REQUIRED_PARENT_CHECKPOINT}"
        )
    forbidden_parent_manifest = _load_json(forbidden_parent_manifest_path)
    if str(forbidden_parent_manifest.get("name") or "") != FORBIDDEN_PARENT_CHECKPOINT:
        raise RuntimeError(
            f"forbidden parent manifest mismatch: {forbidden_parent_manifest.get('name')} != {FORBIDDEN_PARENT_CHECKPOINT}"
        )

    parent_train = _load_jsonl(parent_train_path)
    parent_val = _load_jsonl(parent_val_path)
    counterbalanced_probe_behavior = _load_json(counterbalanced_probe_behavior_path)
    i9_behavior = _load_json(i9_behavior_path)

    system_prompt = _system_prompt_from_parent(parent_train + parent_val)
    train_additions, val_additions, additions_meta = _build_additions(system_prompt)

    if additions_meta["total_additions"] != EXPECTED_TOTAL_ADDITIONS:
        raise RuntimeError(
            f"unexpected additions count: expected={EXPECTED_TOTAL_ADDITIONS} got={additions_meta['total_additions']}"
        )
    if additions_meta["train_additions"] != 4 or additions_meta["val_additions"] != 2:
        raise RuntimeError(
            f"unexpected split additions: train={additions_meta['train_additions']} val={additions_meta['val_additions']}"
        )

    revised_train = deepcopy(parent_train) + train_additions
    revised_val = deepcopy(parent_val) + val_additions

    localized_diff = _build_localized_diff_verification(
        parent_train=parent_train,
        parent_val=parent_val,
        revised_train=revised_train,
        revised_val=revised_val,
        train_additions=train_additions,
        val_additions=val_additions,
    )

    if not bool(localized_diff.get("additions_exact_match", False)):
        raise RuntimeError("localized diff check failed: additions_exact_match=false")
    if not bool(localized_diff.get("existing_rows_changed", {}).get("pass", False)):
        raise RuntimeError("localized diff check failed: existing rows changed")
    if not bool(localized_diff.get("localization_checks", {}).get("pass", False)):
        raise RuntimeError("localized diff check failed: non-localized additions detected")
    if not bool(localized_diff.get("contrastive_pair_validation", {}).get("all_pairs_pass", False)):
        raise RuntimeError("localized diff check failed: contrastive pair validation")
    if not bool(localized_diff.get("residual_block_validation", {}).get("pass", False)):
        raise RuntimeError("localized diff check failed: residual block validation")
    if not bool(localized_diff.get("uncertainty_conditioning_validation", {}).get("pass", False)):
        raise RuntimeError("localized diff check failed: uncertainty-conditioning rows must remain zero")

    _write_jsonl(out_train, revised_train)
    _write_jsonl(out_val, revised_val)

    diagnostics = build_full_diagnostics_report(
        revised_train + revised_val,
        reference_rows=parent_train + parent_val,
        policy=scaffold_policy_defaults(),
        i9_behavioral_report=i9_behavior,
    )
    diagnostics["iteration"] = RUN_NAME
    diagnostics["revision_context"] = {
        "parent_iteration": PARENT_ITERATION,
        "required_parent_checkpoint": REQUIRED_PARENT_CHECKPOINT,
        "forbidden_parent_checkpoint": FORBIDDEN_PARENT_CHECKPOINT,
        "restoration_mode": "ultra_local_residual_nocall_additions_only",
        "expected_total_additions": EXPECTED_TOTAL_ADDITIONS,
        "actual_total_additions": additions_meta["total_additions"],
        "expected_refusal_rows": EXPECTED_NO_CALL_REFUSAL_ROWS,
        "expected_valid_tool_rows": EXPECTED_VALID_TOOL_ROWS,
        "target_failure_family": TARGET_FAMILY,
        "preserve_existing_rows_unchanged": True,
    }

    forbidden_hits = int(diagnostics.get("checks", {}).get("forbidden_pattern_scan", {}).get("total_hits", 0) or 0)
    if forbidden_hits > 0:
        raise RuntimeError(f"forbidden-pattern doctrine violation: total_hits={forbidden_hits}")
    if not bool(diagnostics.get("review_support", {}).get("diversity_review_summary", {}).get("pass", False)):
        raise RuntimeError("diversity doctrine check failed")
    if not bool(diagnostics.get("review_support", {}).get("anti_homogenization_summary", {}).get("pass", False)):
        raise RuntimeError("anti-homogenization doctrine check failed")

    annotations = build_intervention_annotations(revised_train + revised_val, targeted_tools=TARGETED_TOOLS)
    ambiguity_audit = run_prompt_ambiguity_audit(annotations)
    ambiguity_audit["generated_utc"] = _now_utc()
    ambiguity_audit["iteration"] = RUN_NAME
    hard = ambiguity_audit.get("hard_block_candidates", {})
    if bool(hard.get("prompt_to_multiple_targets", False)):
        raise RuntimeError("ambiguity hard block: prompt_to_multiple_targets")
    if bool(hard.get("prompt_to_multiple_tools", False)):
        raise RuntimeError("ambiguity hard block: prompt_to_multiple_tools")
    if bool(hard.get("prompt_tool_to_multiple_arguments", False)):
        raise RuntimeError("ambiguity hard block: prompt_tool_to_multiple_arguments")

    eval_map = {
        "heldout_validation": _load_jsonl(eval_heldout),
        "tool_holdout": _load_jsonl(eval_tool_holdout),
        "no_call": _load_jsonl(eval_no_call),
        "adversarial": _load_jsonl(eval_adversarial),
        "direct_answer": _load_jsonl(eval_direct_answer),
    }
    contamination_audit = _build_contamination_audit(revised_train, revised_val, eval_map)
    _fail_fast_contamination(contamination_audit)

    anti_regression = _build_anti_regression_telemetry(
        additions=train_additions + val_additions,
        diagnostics=diagnostics,
        counterbalanced_probe_behavior=counterbalanced_probe_behavior,
    )

    summary = _build_summary(
        parent_train_rows=len(parent_train),
        parent_val_rows=len(parent_val),
        revised_train_rows=len(revised_train),
        revised_val_rows=len(revised_val),
        localized_diff=localized_diff,
    )

    review = {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "iteration": RUN_NAME,
        "status": "completed",
        "composition": summary["composition"],
        "localized_diff_checks": {
            "additions_exact_match": localized_diff.get("additions_exact_match"),
            "existing_rows_unchanged": localized_diff.get("existing_rows_changed", {}).get("pass"),
            "localized_family_only": localized_diff.get("localization_checks", {}).get("pass"),
            "contrastive_pairs_pass": localized_diff.get("contrastive_pair_validation", {}).get("all_pairs_pass"),
            "residual_block_pass": localized_diff.get("residual_block_validation", {}).get("pass"),
        },
        "hygiene": {
            "ambiguity_hard_blocks_clean": not any(bool(hard.get(k, False)) for k in hard.keys()),
            "heldout_overlap_zero": contamination_audit.get("combined_overlap", {}).get("heldout_validation")
            == {"prompt_overlap": 0, "target_overlap": 0, "source_case_id_overlap": 0},
            "tool_holdout_overlap_zero": contamination_audit.get("combined_overlap", {}).get("tool_holdout")
            == {"prompt_overlap": 0, "target_overlap": 0, "source_case_id_overlap": 0},
            "forbidden_pattern_hits_zero": forbidden_hits == 0,
            "forbidden_pattern_hits": forbidden_hits,
        },
        "anti_regression": {
            "read_file_baseline_exact_valid": anti_regression.get("baseline_metrics_from_i10r_counterbalanced_probe", {}).get(
                "read_file_exact_valid_rate"
            ),
            "scalar_baseline_share": anti_regression.get("baseline_metrics_from_i10r_counterbalanced_probe", {}).get(
                "scalar_substitution_share"
            ),
            "no_anchor_baseline_share": anti_regression.get("baseline_metrics_from_i10r_counterbalanced_probe", {}).get(
                "no_anchor_exact_share"
            ),
            "additions_anchor_distribution": anti_regression.get("dataset_addition_profile", {}).get("anchor_distribution"),
            "top1_skeleton_share_additions": anti_regression.get("dataset_addition_profile", {}).get(
                "top1_skeleton_share_additions"
            ),
            "anti_regression_risk_pass": anti_regression.get("anti_regression_risk_pass"),
            "risk_flags": anti_regression.get("anti_regression_risk_flags"),
        },
        "recommendation": "suitable_for_one_final_bounded_residual_seam_probe_review_only_if_post_run_gates_hold",
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }

    preflight = _build_preflight_validation(
        localized_diff=localized_diff,
        ambiguity_audit=ambiguity_audit,
        contamination_audit=contamination_audit,
        diagnostics=diagnostics,
        anti_regression=anti_regression,
    )
    if not bool(preflight.get("all_critical_checks_pass", False)):
        raise RuntimeError(f"preflight failed: {preflight.get('summary')}")

    _write_json(out_summary, summary)
    _write_json(out_diagnostics, diagnostics)
    _write_json(out_ambiguity, ambiguity_audit)
    _write_json(out_contamination, contamination_audit)
    _write_json(out_localized_diff, localized_diff)
    _write_json(out_anti_regression, anti_regression)
    _write_json(out_review_json, review)
    _write_human_review_package_md(review, out_review_md)
    _write_json(out_preflight, preflight)

    print(
        json.dumps(
            {
                "status": "ok",
                "iteration": RUN_NAME,
                "outputs": {
                    "train_jsonl": str(out_train),
                    "val_jsonl": str(out_val),
                    "summary_json": str(out_summary),
                    "diagnostics_json": str(out_diagnostics),
                    "prompt_ambiguity_audit_json": str(out_ambiguity),
                    "contamination_audit_json": str(out_contamination),
                    "localized_diff_verification_json": str(out_localized_diff),
                    "anti_regression_telemetry_json": str(out_anti_regression),
                    "human_review_package_json": str(out_review_json),
                    "human_review_package_md": str(out_review_md),
                    "preflight_validation_json": str(out_preflight),
                },
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
