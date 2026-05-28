#!/usr/bin/env python3
"""
Build Stage B i10r localized no-call boundary-restoration dataset package.

Scope boundary:
- Additions-only localized dataset generation.
- No mutation of parent i10r rows.
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

RUN_NAME = "stage_b_llama31_8b_base_v1_i10r_nocall"
PARENT_ITERATION = "stage_b_llama31_8b_base_v1_i10r"

EXPECTED_TOTAL_ADDITIONS = 16
EXPECTED_CONTRASTIVE_ROWS = 12
EXPECTED_UNCERTAINTY_ROWS = 4
EXPECTED_PAIR_COUNT = 6

TARGETED_TOOLS = ("read_file", "rg_search")


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


def _base_meta(case_id: str, *, category: str, tool: str | None) -> dict[str, Any]:
    meta: dict[str, Any] = {
        "source": "i10r_nocall_boundary_restoration_builder",
        "source_case_id": case_id,
        "synthetic": True,
        "stage_split": "B_RECOVERY_I10R_NOCALL",
        "recovery_batch": "B_RECOVERY_I10R_NOCALL",
        "category": category,
        "intervention_scope": "localized_nocall_boundary_restoration",
        "intervention_targeted_family": "malformed_regex_underspecified_search_adversarial_boundary",
        "intervention_forbidden_global_pressure": True,
        "intervention_objective": "restore_nocall_integrity_without_procedural_regression",
        "intervention_tool_family": "rg_search",
        "i10r_nocall_restoration_row": True,
        "i10r_nocall_restoration_family": "malformed_regex_underspecified_search_boundary",
    }
    if tool is not None:
        meta["tool"] = tool
    return meta


def _tool_assistant_msg(path: str, pattern: str) -> dict[str, Any]:
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
            "token": "NOCALL_BOUNDARY_PAIR_01",
            "bad_prompt": "Search for pattern [NOCALL_BOUNDARY_PAIR_01 in /opt/ai-stack/runtimes/assistant-runtime/server/agent.py and proceed even if regex parsing fails.",
            "good_prompt": "Search for pattern NOCALL_BOUNDARY_PAIR_01 in /opt/ai-stack/runtimes/assistant-runtime/server/agent.py and proceed with the regular scan call.",
            "bad_refusal": "The pattern is malformed; provide a valid regex pattern before I can run a search call.",
        },
        {
            "pair_id": "pair_02",
            "split": "train",
            "path": "/opt/ai-stack/runtimes/assistant-runtime/server/tools/io.py",
            "token": "NOCALL_BOUNDARY_PAIR_02",
            "bad_prompt": "Run a search for [NOCALL_BOUNDARY_PAIR_02 in /opt/ai-stack/runtimes/assistant-runtime/server/tools/io.py and continue without validating the regex.",
            "good_prompt": "Run a search for NOCALL_BOUNDARY_PAIR_02 in /opt/ai-stack/runtimes/assistant-runtime/server/tools/io.py using one normal search invocation.",
            "bad_refusal": "I need a syntactically valid pattern; this pattern is malformed.",
        },
        {
            "pair_id": "pair_03",
            "split": "train",
            "path": "/opt/ai-stack/runtimes/assistant-runtime/server/router.py",
            "token": "NOCALL_BOUNDARY_PAIR_03",
            "bad_prompt": "Search /opt/ai-stack/runtimes/assistant-runtime/server/router.py for [NOCALL_BOUNDARY_PAIR_03 and keep going anyway.",
            "good_prompt": "Search /opt/ai-stack/runtimes/assistant-runtime/server/router.py for NOCALL_BOUNDARY_PAIR_03 and return only the retrieval call payload.",
            "bad_refusal": "That pattern is not valid regex syntax. Share a valid pattern and I can proceed.",
        },
        {
            "pair_id": "pair_04",
            "split": "train",
            "path": "/opt/ai-stack/runtimes/assistant-runtime/server/executor.py",
            "token": "NOCALL_BOUNDARY_PAIR_04",
            "bad_prompt": "Use search with pattern [NOCALL_BOUNDARY_PAIR_04 in /opt/ai-stack/runtimes/assistant-runtime/server/executor.py and do not stop for regex validation.",
            "good_prompt": "Use search with pattern NOCALL_BOUNDARY_PAIR_04 in /opt/ai-stack/runtimes/assistant-runtime/server/executor.py with a standard search call.",
            "bad_refusal": "I cannot execute this search because the regex is malformed.",
        },
        {
            "pair_id": "pair_05",
            "split": "train",
            "path": "/opt/ai-stack/runtimes/assistant-runtime/server/telemetry.py",
            "token": "NOCALL_BOUNDARY_PAIR_05",
            "bad_prompt": "Find matches for [NOCALL_BOUNDARY_PAIR_05 in /opt/ai-stack/runtimes/assistant-runtime/server/telemetry.py and proceed regardless.",
            "good_prompt": "Find matches for NOCALL_BOUNDARY_PAIR_05 in /opt/ai-stack/runtimes/assistant-runtime/server/telemetry.py using one canonical search call.",
            "bad_refusal": "The requested pattern is malformed. Please send a valid pattern first.",
        },
        {
            "pair_id": "pair_06",
            "split": "val",
            "path": "/opt/ai-stack/runtimes/assistant-runtime/server/runtime.py",
            "token": "NOCALL_BOUNDARY_PAIR_06",
            "bad_prompt": "Search for [NOCALL_BOUNDARY_PAIR_06 in /opt/ai-stack/runtimes/assistant-runtime/server/runtime.py and continue even if the pattern is broken.",
            "good_prompt": "Search for NOCALL_BOUNDARY_PAIR_06 in /opt/ai-stack/runtimes/assistant-runtime/server/runtime.py with a normal search call payload.",
            "bad_refusal": "I need a valid regex pattern before making a search call.",
        },
    ]

    uncertainty_specs = [
        {
            "uc_id": "uc_01",
            "split": "train",
            "prompt": "Search for pattern [NOCALL_UC_01 and proceed; target path will be provided later.",
            "refusal": "I need both a valid pattern and a concrete target path before issuing a search call.",
        },
        {
            "uc_id": "uc_02",
            "split": "train",
            "prompt": "Run search now with pattern [NOCALL_UC_02 across the codebase (path omitted) and continue anyway.",
            "refusal": "The request is underspecified and includes a malformed pattern; please provide valid search inputs.",
        },
        {
            "uc_id": "uc_03",
            "split": "train",
            "prompt": "Proceed with a search for [NOCALL_UC_03 in an unspecified file location.",
            "refusal": "I can continue once you provide a valid regex and an explicit file or directory path.",
        },
        {
            "uc_id": "uc_04",
            "split": "train",
            "prompt": "Use search immediately with [NOCALL_UC_04; I will supply scope details after execution.",
            "refusal": "I cannot issue a search call with an invalid pattern and missing scope details.",
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
        bad_pattern = f"[{token}"
        good_pattern = token

        bad_case = f"i10r_nocall_{pair_id}_bad"
        bad_meta = _base_meta(bad_case, category="adversarial_malformed", tool=None)
        bad_meta.update(
            {
                "i10r_nocall_restoration_block": "contrastive_pair",
                "i10r_nocall_pair_id": pair_id,
                "i10r_nocall_boundary_valid": False,
                "i10r_nocall_semantic_token": token,
                "i10r_nocall_target_path": path,
                "i10r_nocall_target_pattern": bad_pattern,
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

        good_case = f"i10r_nocall_{pair_id}_good"
        good_meta = _base_meta(good_case, category="tool_positive", tool="rg_search")
        good_meta.update(
            {
                "i10r_nocall_restoration_block": "contrastive_pair",
                "i10r_nocall_pair_id": pair_id,
                "i10r_nocall_boundary_valid": True,
                "i10r_nocall_semantic_token": token,
                "i10r_nocall_target_path": path,
                "i10r_nocall_target_pattern": good_pattern,
                "intervention_i10_row": False,
            }
        )
        good_row = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": str(spec["good_prompt"])},
                _tool_assistant_msg(path, good_pattern),
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
                "bad_pattern": bad_pattern,
                "good_pattern": good_pattern,
            }
        )

    for spec in uncertainty_specs:
        uc_id = str(spec["uc_id"])
        split = str(spec["split"])
        case_id = f"i10r_nocall_{uc_id}"
        meta = _base_meta(case_id, category="adversarial_malformed", tool=None)
        meta.update(
            {
                "i10r_nocall_restoration_block": "uncertainty_conditioning",
                "i10r_nocall_pair_id": None,
                "i10r_nocall_boundary_valid": False,
                "i10r_nocall_semantic_token": f"NOCALL_{uc_id.upper()}",
                "i10r_nocall_target_path": None,
                "i10r_nocall_target_pattern": f"[NOCALL_{uc_id.upper()}",
            }
        )
        row = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": str(spec["prompt"])},
                {"role": "assistant", "content": str(spec["refusal"])},
            ],
            "metadata": meta,
        }
        add_row(split, row)

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
    additions_meta: dict[str, Any],
) -> dict[str, Any]:
    parent_train_hashes = [_row_hash(r) for r in parent_train]
    parent_val_hashes = [_row_hash(r) for r in parent_val]
    revised_train_prefix_hashes = [_row_hash(r) for r in revised_train[: len(parent_train)]]
    revised_val_prefix_hashes = [_row_hash(r) for r in revised_val[: len(parent_val)]]
    changed_train = [i + 1 for i, (a, b) in enumerate(zip(parent_train_hashes, revised_train_prefix_hashes)) if a != b]
    changed_val = [i + 1 for i, (a, b) in enumerate(zip(parent_val_hashes, revised_val_prefix_hashes)) if a != b]

    additions = train_additions + val_additions
    add_blocks = Counter(str((r.get("metadata") or {}).get("i10r_nocall_restoration_block") or "") for r in additions)
    add_tools = Counter(_tool_name_from_assistant(r) or "no_tool" for r in additions)
    add_family = Counter(
        str((r.get("metadata") or {}).get("i10r_nocall_restoration_family") or "")
        for r in additions
    )

    pair_rows: dict[str, list[dict[str, Any]]] = {}
    for row in additions:
        meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        pair_id = meta.get("i10r_nocall_pair_id")
        if not pair_id:
            continue
        pair_rows.setdefault(str(pair_id), []).append(row)

    pair_checks: list[dict[str, Any]] = []
    for pair in sorted(pair_rows.keys()):
        rows = pair_rows[pair]
        bad = [r for r in rows if not bool((r.get("metadata") or {}).get("i10r_nocall_boundary_valid", False))]
        good = [r for r in rows if bool((r.get("metadata") or {}).get("i10r_nocall_boundary_valid", False))]
        token_set = {str((r.get("metadata") or {}).get("i10r_nocall_semantic_token") or "") for r in rows}
        path_set = {str((r.get("metadata") or {}).get("i10r_nocall_target_path") or "") for r in rows}
        pair_checks.append(
            {
                "pair_id": pair,
                "rows": len(rows),
                "bad_rows": len(bad),
                "good_rows": len(good),
                "semantic_token_consistent": len(token_set) == 1,
                "path_consistent": len(path_set) == 1,
                "pass": len(rows) == 2 and len(bad) == 1 and len(good) == 1 and len(token_set) == 1 and len(path_set) == 1,
            }
        )

    all_pair_pass = all(bool(x.get("pass", False)) for x in pair_checks) and len(pair_checks) == EXPECTED_PAIR_COUNT

    localized_only = all(
        str((r.get("metadata") or {}).get("i10r_nocall_restoration_family") or "")
        == "malformed_regex_underspecified_search_boundary"
        for r in additions
    )

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
        },
        "localization_checks": {
            "all_rows_localized_family": localized_only,
            "localized_family_expected": "malformed_regex_underspecified_search_boundary",
            "pass": localized_only,
        },
        "contrastive_pair_validation": {
            "expected_pair_count": EXPECTED_PAIR_COUNT,
            "pair_count": len(pair_checks),
            "all_pairs_pass": all_pair_pass,
            "pairs": pair_checks,
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
    baseline_summary: dict[str, Any],
    scalar_delta: dict[str, Any],
    proc_generalization: dict[str, Any],
    read_file_emergence: dict[str, Any],
    diagnostics: dict[str, Any],
) -> dict[str, Any]:
    prompts = [_user_prompt(r) for r in additions]
    literal_anchor = sum(1 for p in prompts if "tool_calls" in p.lower())
    paraphrastic_anchor = sum(1 for p in prompts if ("tool call" in p.lower() or "function call" in p.lower()))
    no_anchor = len(prompts) - literal_anchor - paraphrastic_anchor

    anns = build_intervention_annotations(additions, targeted_tools=TARGETED_TOOLS)
    sk = Counter(str(a.get("skeleton_id") or "") for a in anns)
    top1 = max(sk.values()) / len(additions) if additions and sk else 0.0
    tool_rows = sum(1 for r in additions if _tool_name_from_assistant(r))
    refusal_rows = len(additions) - tool_rows

    baseline = {
        "read_file_exact_valid_rate": read_file_emergence.get("i10r_microprobe", {}).get("read_file_exact_valid_rate"),
        "scalar_substitution_share": scalar_delta.get("i10r_microprobe_eval", {}).get("scalar_substitution_share"),
        "direct_answer_substitution_share": scalar_delta.get("i10r_microprobe_eval", {}).get(
            "direct_answer_substitution_share"
        ),
        "no_anchor_exact_share": proc_generalization.get("anchor_distribution_exact_valid", {}).get("shares", {}).get(
            "no_anchor_phrase"
        ),
        "wrapper_leakage": baseline_summary.get("metrics", {}).get("stage_b_i10r_microprobe_aggregate", {}).get(
            "wrapper_leakage"
        ),
        "no_call_correctness_aggregate": baseline_summary.get("metrics", {}).get("stage_b_i10r_microprobe_aggregate", {}).get(
            "no_call_correctness"
        ),
    }

    risk_flags = {
        "literal_anchor_additions_present": literal_anchor > 0,
        "top1_skeleton_share_high": top1 > 0.35,
        "tool_rows_too_low_for_contrastive_preservation": tool_rows < EXPECTED_PAIR_COUNT,
        "refusal_rows_too_high": refusal_rows > 12,
    }

    return {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "iteration": RUN_NAME,
        "status": "completed",
        "baseline_metrics_from_i10r_microprobe": baseline,
        "dataset_addition_profile": {
            "total_additions": len(additions),
            "tool_rows": tool_rows,
            "refusal_rows": refusal_rows,
            "refusal_to_tool_ratio": round(refusal_rows / tool_rows, 6) if tool_rows else None,
            "anchor_distribution": {
                "literal_tool_calls": literal_anchor,
                "paraphrastic_tool_call": paraphrastic_anchor,
                "no_anchor_phrase": no_anchor,
            },
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
            "objective": "localized_nocall_boundary_restoration",
            "targeted_family": "malformed_regex_underspecified_search_adversarial_boundary",
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
    lines.append("# Stage B i10r No-Call Restoration Human Review Package")
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
    lines.append("## Localized Diff Checks")
    diff = report.get("localized_diff_checks", {})
    lines.append(f"- additions_exact_match: {diff.get('additions_exact_match')}")
    lines.append(f"- existing_rows_unchanged: {diff.get('existing_rows_unchanged')}")
    lines.append(f"- localized_family_only: {diff.get('localized_family_only')}")
    lines.append(f"- contrastive_pairs_pass: {diff.get('contrastive_pairs_pass')}")
    lines.append("")
    lines.append("## Hygiene Gates")
    hygiene = report.get("hygiene", {})
    lines.append(f"- ambiguity_hard_blocks_clean: {hygiene.get('ambiguity_hard_blocks_clean')}")
    lines.append(f"- heldout_overlap_zero: {hygiene.get('heldout_overlap_zero')}")
    lines.append(f"- tool_holdout_overlap_zero: {hygiene.get('tool_holdout_overlap_zero')}")
    lines.append(f"- forbidden_pattern_hits_zero: {hygiene.get('forbidden_pattern_hits_zero')}")
    lines.append("")
    lines.append("## Anti-Regression Telemetry")
    anti = report.get("anti_regression", {})
    lines.append(f"- read_file_baseline_exact_valid: {anti.get('read_file_baseline_exact_valid')}")
    lines.append(f"- scalar_baseline_share: {anti.get('scalar_baseline_share')}")
    lines.append(f"- no_anchor_baseline_share: {anti.get('no_anchor_baseline_share')}")
    lines.append(f"- additions_anchor_distribution: {anti.get('additions_anchor_distribution')}")
    lines.append(f"- anti_regression_risk_pass: {anti.get('anti_regression_risk_pass')}")
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
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def add_check(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "status": "pass" if ok else "fail", "detail": detail})

    hard = ambiguity_audit.get("hard_block_candidates", {}) if isinstance(ambiguity_audit.get("hard_block_candidates"), dict) else {}
    heldout = contamination_audit.get("combined_overlap", {}).get("heldout_validation")
    tool_holdout = contamination_audit.get("combined_overlap", {}).get("tool_holdout")
    forbidden_hits = int(diagnostics.get("checks", {}).get("forbidden_pattern_scan", {}).get("total_hits", 0) or 0)
    diversity_pass = bool(diagnostics.get("review_support", {}).get("diversity_review_summary", {}).get("pass", False))
    anti_pass = bool(diagnostics.get("review_support", {}).get("anti_homogenization_summary", {}).get("pass", False))

    add_check(
        "exactly_16_rows_added",
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
        "uncertainty_rows_eq_4",
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
    add_check("anti_homogenization_pass", anti_pass, f"anti_pass={anti_pass}")

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
    parser = argparse.ArgumentParser(description="Build localized i10r no-call restoration dataset package.")
    parser.add_argument(
        "--parent-train-jsonl",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i10r_train.jsonl",
    )
    parser.add_argument(
        "--parent-val-jsonl",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i10r_val.jsonl",
    )
    parser.add_argument(
        "--parent-summary-json",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i10r_summary.json",
    )
    parser.add_argument(
        "--i10r-microprobe-summary-json",
        default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_microprobe_canonical_eval_summary.json",
    )
    parser.add_argument(
        "--i10r-scalar-delta-json",
        default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_microprobe_scalar_substitution_delta_analysis.json",
    )
    parser.add_argument(
        "--i10r-procedural-generalization-json",
        default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_microprobe_procedural_generalization_assessment.json",
    )
    parser.add_argument(
        "--i10r-read-file-emergence-json",
        default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_microprobe_read_file_emergence_analysis.json",
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
    parser.add_argument("--allow-nocall-restoration-phase", action="store_true")
    parser.add_argument("--apply-localized-restoration-design", action="store_true")
    return parser.parse_args()


def _fail_fast_unlock(args: argparse.Namespace) -> None:
    if not args.enable_dataset_generation:
        raise RuntimeError("dataset generation requires --enable-dataset-generation")
    if not args.allow_nocall_restoration_phase:
        raise RuntimeError("dataset generation requires --allow-nocall-restoration-phase")
    if not args.apply_localized_restoration_design:
        raise RuntimeError("dataset generation requires --apply-localized-restoration-design")


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
    microprobe_summary_path = Path(args.i10r_microprobe_summary_json).resolve()
    scalar_delta_path = Path(args.i10r_scalar_delta_json).resolve()
    proc_generalization_path = Path(args.i10r_procedural_generalization_json).resolve()
    read_file_path = Path(args.i10r_read_file_emergence_json).resolve()
    i9_behavior_path = Path(args.i9_behavioral_review_json).resolve()

    eval_heldout = Path(args.eval_heldout_jsonl).resolve()
    eval_tool_holdout = Path(args.eval_tool_holdout_jsonl).resolve()
    eval_no_call = Path(args.eval_no_call_jsonl).resolve()
    eval_adversarial = Path(args.eval_adversarial_jsonl).resolve()
    eval_direct_answer = Path(args.eval_direct_answer_jsonl).resolve()

    data_root = Path(args.output_data_root).resolve()
    report_root = Path(args.output_report_root).resolve()

    out_train = data_root / "dataset_v1_0_stage_b_recovery_i10r_nocall_train.jsonl"
    out_val = data_root / "dataset_v1_0_stage_b_recovery_i10r_nocall_val.jsonl"
    out_summary = data_root / "dataset_v1_0_stage_b_recovery_i10r_nocall_summary.json"
    out_diagnostics = report_root / "stage_b_v1_i10r_nocall_dataset_diagnostics.json"
    out_ambiguity = report_root / "stage_b_v1_i10r_nocall_prompt_ambiguity_audit.json"
    out_contamination = report_root / "stage_b_v1_i10r_nocall_contamination_audit.json"
    out_localized_diff = report_root / "stage_b_v1_i10r_nocall_localized_diff_verification.json"
    out_anti_regression = report_root / "stage_b_v1_i10r_nocall_anti_regression_telemetry.json"
    out_review_json = report_root / "stage_b_v1_i10r_nocall_human_review_package.json"
    out_review_md = report_root / "stage_b_v1_i10r_nocall_human_review_package.md"
    out_preflight = report_root / "stage_b_v1_i10r_nocall_preflight_validation.json"

    _fail_fast_inputs(
        [
            parent_train_path,
            parent_val_path,
            parent_summary_path,
            microprobe_summary_path,
            scalar_delta_path,
            proc_generalization_path,
            read_file_path,
            i9_behavior_path,
            eval_heldout,
            eval_tool_holdout,
            eval_no_call,
            eval_adversarial,
            eval_direct_answer,
        ]
    )

    parent_summary = _load_json(parent_summary_path)
    if str(parent_summary.get("iteration") or "") != PARENT_ITERATION:
        raise RuntimeError(
            f"unexpected parent iteration in summary: {parent_summary.get('iteration')} (expected {PARENT_ITERATION})"
        )

    parent_train = _load_jsonl(parent_train_path)
    parent_val = _load_jsonl(parent_val_path)
    baseline_summary = _load_json(microprobe_summary_path)
    scalar_delta = _load_json(scalar_delta_path)
    proc_generalization = _load_json(proc_generalization_path)
    read_file_emergence = _load_json(read_file_path)
    i9_behavior = _load_json(i9_behavior_path)

    system_prompt = _system_prompt_from_parent(parent_train + parent_val)
    train_additions, val_additions, additions_meta = _build_additions(system_prompt)

    if additions_meta["total_additions"] != EXPECTED_TOTAL_ADDITIONS:
        raise RuntimeError(
            f"unexpected additions count: expected={EXPECTED_TOTAL_ADDITIONS} got={additions_meta['total_additions']}"
        )
    if additions_meta["train_additions"] != 14 or additions_meta["val_additions"] != 2:
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
        additions_meta=additions_meta,
    )
    if not bool(localized_diff.get("additions_exact_match", False)):
        raise RuntimeError("localized diff check failed: additions_exact_match=false")
    if not bool(localized_diff.get("existing_rows_changed", {}).get("pass", False)):
        raise RuntimeError("localized diff check failed: existing rows changed")
    if not bool(localized_diff.get("localization_checks", {}).get("pass", False)):
        raise RuntimeError("localized diff check failed: non-localized additions detected")
    if not bool(localized_diff.get("contrastive_pair_validation", {}).get("all_pairs_pass", False)):
        raise RuntimeError("localized diff check failed: contrastive pair validation")

    # Persist revised dataset before downstream utilities that read from disk in review flows.
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
        "restoration_mode": "localized_additions_only",
        "expected_total_additions": EXPECTED_TOTAL_ADDITIONS,
        "actual_total_additions": additions_meta["total_additions"],
        "target_failure_family": "malformed_regex_underspecified_search_adversarial_boundary",
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
        baseline_summary=baseline_summary,
        scalar_delta=scalar_delta,
        proc_generalization=proc_generalization,
        read_file_emergence=read_file_emergence,
        diagnostics=diagnostics,
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
            "read_file_baseline_exact_valid": anti_regression.get("baseline_metrics_from_i10r_microprobe", {}).get(
                "read_file_exact_valid_rate"
            ),
            "scalar_baseline_share": anti_regression.get("baseline_metrics_from_i10r_microprobe", {}).get(
                "scalar_substitution_share"
            ),
            "no_anchor_baseline_share": anti_regression.get("baseline_metrics_from_i10r_microprobe", {}).get(
                "no_anchor_exact_share"
            ),
            "additions_anchor_distribution": anti_regression.get("dataset_addition_profile", {}).get("anchor_distribution"),
            "anti_regression_risk_pass": anti_regression.get("anti_regression_risk_pass"),
            "risk_flags": anti_regression.get("anti_regression_risk_flags"),
        },
        "recommendation": "proceed_to_bounded_training_review_candidate_only_if_future_post_run_gates_hold",
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
