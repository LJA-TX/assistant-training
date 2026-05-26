#!/usr/bin/env python3
"""
Build Stage B i8 candidate dataset package.

Governance boundaries:
- Dataset generation is allowed only with explicit unlock flags.
- Training/eval/checkpoint actions are out of scope and not performed.
- Overlap contamination checks are blocking and fail-fast.
- No silent fallback or overlap-bypass prompt mutation is allowed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from i8_diagnostics_scaffold import (
    build_full_diagnostics_report,
    build_intervention_annotations,
    run_prompt_ambiguity_audit,
    scaffold_policy_defaults,
)

RUN_NAME = "stage_b_llama31_8b_base_v1_i8"
PARENT_BASELINE = "stage_b_llama31_8b_base_v1_i3"
TARGETED_TOOLS = ("rg_search", "read_file")
EXPECTED_NON_TOOL_COUNTS = {"train": 756, "val": 84}
EXPECTED_TOTAL_COUNTS = {"train": 2160, "val": 240}

# Parse-anchor variants are intentionally diverse to avoid local-template collapse.
PARSE_ANCHOR_VARIANTS = (
    "Return one valid JSON object with top-level key tool_calls.",
    "Respond with exactly one parseable JSON object containing tool_calls.",
    "Output one strict JSON object only, with top-level key tool_calls.",
    "Produce only JSON: a single object whose top-level key is tool_calls.",
    "Emit a single parseable JSON object; top-level key must be tool_calls.",
)

FORBIDDEN_GLOBAL_PRESSURES = (
    "global_negation_heavy_schema_pressure",
    "global_imperative_template_rewrites",
    "wrapper_key_blacklist_flooding",
    "semantic_flattening",
)


@dataclass(frozen=True)
class BuilderInputs:
    parent_train_jsonl: Path
    parent_val_jsonl: Path
    parent_summary_json: Path
    eval_heldout_jsonl: Path
    eval_tool_holdout_jsonl: Path
    eval_no_call_jsonl: Path
    eval_adversarial_jsonl: Path
    eval_direct_answer_jsonl: Path
    surgical_rebalance_proposal_json: Path


@dataclass(frozen=True)
class OutputPaths:
    train_jsonl: Path
    val_jsonl: Path
    summary_json: Path
    diagnostics_json: Path
    contamination_audit_json: Path
    prompt_ambiguity_audit_json: Path
    review_package_json: Path


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _canonical_json_text(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha1_text(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"invalid JSON at {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise RuntimeError(f"expected JSON object at {path}")
    return data


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
                raise RuntimeError(f"invalid JSONL {path}:{line_no}: {exc}") from exc
            if not isinstance(obj, dict):
                raise RuntimeError(f"invalid row type {path}:{line_no}: expected object")
            rows.append(obj)
    return rows


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _user_prompt(row: dict[str, Any]) -> str:
    msgs = row.get("messages")
    if not isinstance(msgs, list):
        return ""
    for msg in msgs:
        if isinstance(msg, dict) and msg.get("role") == "user":
            return str(msg.get("content") or "")
    return ""


def _set_user_prompt(row: dict[str, Any], prompt: str) -> None:
    msgs = row.get("messages")
    if not isinstance(msgs, list):
        raise RuntimeError("row has invalid messages structure")
    for msg in msgs:
        if isinstance(msg, dict) and msg.get("role") == "user":
            msg["content"] = prompt
            return
    raise RuntimeError("row has no user message")


def _assistant_target_text(row: dict[str, Any]) -> str:
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


def _tool_name(row: dict[str, Any]) -> str:
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


def _assistant_arguments_obj(row: dict[str, Any]) -> dict[str, Any] | None:
    msgs = row.get("messages")
    if not isinstance(msgs, list):
        return None
    for msg in msgs:
        if not isinstance(msg, dict) or msg.get("role") != "assistant":
            continue
        tc = msg.get("tool_calls")
        if not isinstance(tc, list) or not tc or not isinstance(tc[0], dict):
            return None
        fn = tc[0].get("function")
        if not isinstance(fn, dict):
            return None
        args = fn.get("arguments")
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except Exception:
                return None
        if isinstance(args, dict):
            return args
        return None
    return None


def _is_tool_row(row: dict[str, Any]) -> bool:
    return bool(_tool_name(row))


def _row_case_id(row: dict[str, Any], fallback: str) -> str:
    meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    value = str(meta.get("source_case_id") or meta.get("case_id") or "").strip()
    return value or fallback


def _resolve_inputs(args: argparse.Namespace) -> BuilderInputs:
    return BuilderInputs(
        parent_train_jsonl=Path(args.parent_train_jsonl).resolve(),
        parent_val_jsonl=Path(args.parent_val_jsonl).resolve(),
        parent_summary_json=Path(args.parent_summary_json).resolve(),
        eval_heldout_jsonl=Path(args.eval_heldout_jsonl).resolve(),
        eval_tool_holdout_jsonl=Path(args.eval_tool_holdout_jsonl).resolve(),
        eval_no_call_jsonl=Path(args.eval_no_call_jsonl).resolve(),
        eval_adversarial_jsonl=Path(args.eval_adversarial_jsonl).resolve(),
        eval_direct_answer_jsonl=Path(args.eval_direct_answer_jsonl).resolve(),
        surgical_rebalance_proposal_json=Path(args.surgical_rebalance_proposal_json).resolve(),
    )


def _resolve_outputs(args: argparse.Namespace) -> OutputPaths:
    out_root = Path(args.output_root).resolve()
    report_root = Path(args.report_root).resolve()
    return OutputPaths(
        train_jsonl=out_root / "dataset_v1_0_stage_b_recovery_i8_train.jsonl",
        val_jsonl=out_root / "dataset_v1_0_stage_b_recovery_i8_val.jsonl",
        summary_json=out_root / "dataset_v1_0_stage_b_recovery_i8_summary.json",
        diagnostics_json=report_root / "stage_b_v1_i8_dataset_diagnostics.json",
        contamination_audit_json=report_root / "stage_b_v1_i8_contamination_audit.json",
        prompt_ambiguity_audit_json=report_root / "stage_b_v1_i8_prompt_ambiguity_audit.json",
        review_package_json=report_root / "stage_b_v1_i8_human_review_package.json",
    )


def _fail_fast_generation_unlock(args: argparse.Namespace) -> None:
    if not args.enable_dataset_emission:
        raise RuntimeError("dataset emission requires explicit --enable-dataset-emission")
    if not args.allow_generation_phase:
        raise RuntimeError("dataset emission requires explicit --allow-generation-phase")
    if not args.output_root.strip():
        raise RuntimeError("output_root must be set for generation phase")


def _fail_fast_surgical_rebalance_unlock(args: argparse.Namespace) -> None:
    if not bool(args.enable_surgical_rebalance):
        raise RuntimeError(
            "i8 generation now requires explicit --enable-surgical-rebalance "
            "to enforce approved deterministic trim plan"
        )


def _fail_fast_input_validation(inputs: BuilderInputs) -> None:
    required = [
        inputs.parent_train_jsonl,
        inputs.parent_val_jsonl,
        inputs.parent_summary_json,
        inputs.eval_heldout_jsonl,
        inputs.eval_tool_holdout_jsonl,
        inputs.eval_no_call_jsonl,
        inputs.eval_adversarial_jsonl,
        inputs.eval_direct_answer_jsonl,
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise RuntimeError("missing required inputs:\n- " + "\n- ".join(missing))

    if not inputs.surgical_rebalance_proposal_json.exists():
        raise RuntimeError(
            "missing required surgical rebalance proposal JSON: "
            f"{inputs.surgical_rebalance_proposal_json}"
        )


def _validate_parent_invariants(train_rows: list[dict[str, Any]], val_rows: list[dict[str, Any]]) -> dict[str, Any]:
    if len(train_rows) != EXPECTED_TOTAL_COUNTS["train"] or len(val_rows) != EXPECTED_TOTAL_COUNTS["val"]:
        raise RuntimeError(
            "parent row counts drifted from governed envelope: "
            f"train={len(train_rows)} val={len(val_rows)} expected=2160/240"
        )

    non_tool_train = sum(1 for row in train_rows if not _is_tool_row(row))
    non_tool_val = sum(1 for row in val_rows if not _is_tool_row(row))
    if non_tool_train != EXPECTED_NON_TOOL_COUNTS["train"] or non_tool_val != EXPECTED_NON_TOOL_COUNTS["val"]:
        raise RuntimeError(
            "non-tool envelope drift detected: "
            f"train={non_tool_train} val={non_tool_val} expected=756/84"
        )

    tool_train = len(train_rows) - non_tool_train
    tool_val = len(val_rows) - non_tool_val

    return {
        "status": "ok",
        "train_rows": len(train_rows),
        "val_rows": len(val_rows),
        "non_tool_train": non_tool_train,
        "non_tool_val": non_tool_val,
        "tool_train": tool_train,
        "tool_val": tool_val,
    }


def _collect_eval_map(inputs: BuilderInputs) -> dict[str, list[dict[str, Any]]]:
    return {
        "heldout_validation": _load_jsonl(inputs.eval_heldout_jsonl),
        "tool_holdout": _load_jsonl(inputs.eval_tool_holdout_jsonl),
        "no_call": _load_jsonl(inputs.eval_no_call_jsonl),
        "adversarial": _load_jsonl(inputs.eval_adversarial_jsonl),
        "direct_answer": _load_jsonl(inputs.eval_direct_answer_jsonl),
    }


def _overlap_report(candidate_rows: list[dict[str, Any]], eval_map: dict[str, list[dict[str, Any]]]) -> dict[str, dict[str, int]]:
    prompts = {_user_prompt(r) for r in candidate_rows}
    targets = {_assistant_target_text(r) for r in candidate_rows}
    cases = {_row_case_id(r, "") for r in candidate_rows}

    out: dict[str, dict[str, int]] = {}
    for split, rows in eval_map.items():
        eval_prompts = {_user_prompt(r) for r in rows}
        eval_targets = {_assistant_target_text(r) for r in rows}
        eval_cases = {_row_case_id(r, f"{split}_unknown") for r in rows}
        out[split] = {
            "prompt_overlap": len(prompts.intersection(eval_prompts)),
            "target_overlap": len(targets.intersection(eval_targets)),
            "source_case_id_overlap": len(cases.intersection(eval_cases)),
        }
    return out


def _fail_fast_overlap_guard(overlap: dict[str, dict[str, int]], *, scope: str) -> None:
    for split_name in ("heldout_validation", "tool_holdout"):
        split = overlap.get(split_name)
        if split is None:
            raise RuntimeError(f"{scope}: overlap report missing split {split_name}")
        if split["prompt_overlap"] > 0 or split["target_overlap"] > 0 or split["source_case_id_overlap"] > 0:
            raise RuntimeError(
                f"{scope}: contamination overlap detected in {split_name}: "
                f"{json.dumps(split, ensure_ascii=False)}"
            )


def _needs_parse_anchor(prompt: str) -> bool:
    p = prompt.lower()
    indicators = (
        "tool_calls",
        "json object",
        "strict json",
        "parseable json",
    )
    return not any(token in p for token in indicators)


def _anchor_selector(case_id: str, seed: int) -> int:
    digest = hashlib.sha1(f"{case_id}|{seed}".encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def _apply_parse_anchor(prompt: str, *, case_id: str, seed: int) -> tuple[str, str, bool]:
    if not _needs_parse_anchor(prompt):
        return prompt, "existing_anchor_signal", False

    selector = _anchor_selector(case_id, seed)
    mode = selector % 10
    variant = PARSE_ANCHOR_VARIANTS[selector % len(PARSE_ANCHOR_VARIANTS)]

    # Diversity-preserving policy: not all rows get identical anchor placement.
    if mode in (0, 1, 2):
        out = f"{prompt.strip()} {variant}".strip()
        return out, "append", True
    if mode in (3, 4):
        out = f"{variant} {prompt.strip()}".strip()
        return out, "prepend", True
    if mode in (5, 6):
        out = f"{prompt.strip()} Return strict JSON only.".strip()
        return out, "append_compact", True

    # Controlled keep-original branch to avoid anchor-template convergence.
    return prompt, "unchanged_diversity_preserve", False


def _annotate_targeted_row(
    row: dict[str, Any],
    *,
    split: str,
    case_id: str,
    original_prompt: str,
    transformed_prompt: str,
    anchor_mode: str,
    anchor_added: bool,
) -> None:
    meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    meta["stage_split"] = "B_RECOVERY_I8"
    meta["recovery_batch"] = split
    meta["intervention_scope"] = "i8_hybrid_localized"
    meta["intervention_objective"] = "parseability_without_schema_spill"
    meta["intervention_targeted_family"] = True
    meta["intervention_tool_family"] = _tool_name(row)
    meta["intervention_anchor_mode"] = anchor_mode
    meta["intervention_anchor_added"] = bool(anchor_added)
    meta["intervention_anchor_hash"] = _sha1_text(anchor_mode if not anchor_added else transformed_prompt)
    meta["intervention_source_case_id"] = case_id
    meta["intervention_prompt_changed"] = original_prompt != transformed_prompt
    meta["intervention_forbidden_global_pressure"] = False
    row["metadata"] = meta


def _annotate_non_targeted_row(row: dict[str, Any], *, split: str) -> None:
    meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    meta["stage_split"] = "B_RECOVERY_I8"
    meta["recovery_batch"] = split
    meta["intervention_scope"] = "i8_hybrid_localized"
    meta["intervention_targeted_family"] = False
    meta["intervention_forbidden_global_pressure"] = False
    row["metadata"] = meta


def _transform_split_rows(
    parent_rows: list[dict[str, Any]],
    *,
    split: str,
    seed: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    out_rows: list[dict[str, Any]] = []
    anchor_mode_counts = Counter()
    targeted_count = 0
    targeted_changed = 0

    for idx, src_row in enumerate(parent_rows, start=1):
        row = json.loads(json.dumps(src_row, ensure_ascii=False))
        tool = _tool_name(row)
        case_id = _row_case_id(row, f"{split}_{idx:06d}")

        if tool in TARGETED_TOOLS:
            targeted_count += 1
            original_prompt = _user_prompt(row)
            transformed_prompt, anchor_mode, anchor_added = _apply_parse_anchor(
                original_prompt,
                case_id=case_id,
                seed=seed,
            )
            _set_user_prompt(row, transformed_prompt)
            _annotate_targeted_row(
                row,
                split=split,
                case_id=case_id,
                original_prompt=original_prompt,
                transformed_prompt=transformed_prompt,
                anchor_mode=anchor_mode,
                anchor_added=anchor_added,
            )
            anchor_mode_counts[anchor_mode] += 1
            if original_prompt != transformed_prompt:
                targeted_changed += 1
        else:
            _annotate_non_targeted_row(row, split=split)

        out_rows.append(row)

    if targeted_count == 0:
        raise RuntimeError(f"{split}: no targeted rows found for {TARGETED_TOOLS}")

    return out_rows, {
        "targeted_rows": targeted_count,
        "targeted_rows_prompt_changed": targeted_changed,
        "anchor_mode_counts": dict(sorted(anchor_mode_counts.items(), key=lambda kv: kv[0])),
    }


def _validate_localized_integrity(parent_rows: list[dict[str, Any]], candidate_rows: list[dict[str, Any]], *, split: str) -> None:
    if len(parent_rows) != len(candidate_rows):
        raise RuntimeError(f"{split}: row count changed during localized transformation")

    for idx, (base, cand) in enumerate(zip(parent_rows, candidate_rows), start=1):
        base_tool = _tool_name(base)
        cand_tool = _tool_name(cand)
        if base_tool != cand_tool:
            raise RuntimeError(f"{split}:{idx}: tool identity drifted from {base_tool} to {cand_tool}")

        if base_tool not in TARGETED_TOOLS:
            if _user_prompt(base) != _user_prompt(cand):
                raise RuntimeError(f"{split}:{idx}: non-target prompt mutated")
            if _assistant_target_text(base) != _assistant_target_text(cand):
                raise RuntimeError(f"{split}:{idx}: non-target assistant target mutated")


def _count_categories(rows: list[dict[str, Any]]) -> dict[str, int]:
    counter = Counter()
    for row in rows:
        meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        category = str(meta.get("category") or "unknown")
        counter[category] += 1
    return dict(sorted(counter.items(), key=lambda kv: kv[0]))


def _count_tools(rows: list[dict[str, Any]]) -> dict[str, int]:
    counter = Counter()
    for row in rows:
        tool = _tool_name(row)
        if tool:
            counter[tool] += 1
    return dict(sorted(counter.items(), key=lambda kv: kv[0]))


def _combined_rows(train_rows: list[dict[str, Any]], val_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return train_rows + val_rows


def _build_prompt_ambiguity_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    annotations = build_intervention_annotations(rows, targeted_tools=TARGETED_TOOLS)
    audit = run_prompt_ambiguity_audit(annotations)
    audit["generated_utc"] = _now_utc()
    audit["iteration"] = RUN_NAME
    return audit


def _row_unique_id(split: str, idx_1based: int) -> str:
    return f"{split}:{idx_1based}"


def _surgical_trim_index(
    train_rows: list[dict[str, Any]],
    val_rows: list[dict[str, Any]],
) -> dict[tuple[str, str, str], list[tuple[str, int]]]:
    """
    Build deterministic lookup for surgical trimming:
    (source_case_id, tool_name, prompt) -> [(split, idx_0based), ...] in stable row order.
    """
    out: dict[tuple[str, str, str], list[tuple[str, int]]] = {}
    for split, rows in (("train", train_rows), ("val", val_rows)):
        for idx_0, row in enumerate(rows):
            tool = _tool_name(row)
            if tool not in TARGETED_TOOLS:
                continue
            prompt = _user_prompt(row)
            case_id = _row_case_id(row, _row_unique_id(split, idx_0 + 1))
            key = (case_id, tool, prompt)
            out.setdefault(key, []).append((split, idx_0))
    return out


def _surgical_trim_style_bucket(prompt: str) -> str:
    p = prompt.strip().lower()
    if not p:
        return "empty"
    imperative_heads = (
        "use ",
        "call ",
        "invoke ",
        "run ",
        "open ",
        "read ",
        "search ",
        "find ",
        "check ",
        "list ",
        "show ",
        "return ",
        "retrieve ",
    )
    if p.endswith("?"):
        return "question_form"
    if any(p.startswith(h) for h in imperative_heads):
        if "line" in p or "lines" in p:
            return "imperative_line_scoped"
        return "imperative_general"
    return "task_narrative"


def _target_signature(row: dict[str, Any]) -> str:
    return _assistant_target_text(row)


def _family_snapshot(rows: list[dict[str, Any]], family: str) -> dict[str, Any]:
    fam_rows = [r for r in rows if _tool_name(r) in TARGETED_TOOLS and _row_case_id(r, "") == family]
    if not fam_rows:
        return {
            "rows": 0,
            "tools": set(),
            "prompts": set(),
            "targets": set(),
            "skeletons": set(),
            "task_narrative_rows": 0,
            "ambiguity_remediation_rows": 0,
        }
    anns = build_intervention_annotations(fam_rows, targeted_tools=TARGETED_TOOLS)
    return {
        "rows": len(fam_rows),
        "tools": {_tool_name(r) for r in fam_rows},
        "prompts": {_user_prompt(r) for r in fam_rows},
        "targets": {_target_signature(r) for r in fam_rows},
        "skeletons": {a.get("skeleton_id", "") for a in anns},
        "task_narrative_rows": sum(1 for a in anns if a.get("style_bucket") == "task_narrative"),
        "ambiguity_remediation_rows": sum(
            1
            for r in fam_rows
            if bool((r.get("metadata") if isinstance(r.get("metadata"), dict) else {}).get("ambiguity_remediation_applied", False))
        ),
    }


def _global_targeted_snapshot(rows: list[dict[str, Any]]) -> dict[str, Any]:
    targeted_rows = [r for r in rows if _tool_name(r) in TARGETED_TOOLS]
    anns = build_intervention_annotations(targeted_rows, targeted_tools=TARGETED_TOOLS)
    return {
        "rows": len(targeted_rows),
        "targets": {_target_signature(r) for r in targeted_rows},
        "skeletons": {a.get("skeleton_id", "") for a in anns},
        "task_narrative_rows": sum(1 for a in anns if a.get("style_bucket") == "task_narrative"),
        "prompt_uniqueness_ratio": (
            len({a.get("prompt", "") for a in anns}) / len(anns)
            if anns
            else 0.0
        ),
    }


def _load_surgical_rebalance_proposal(path: Path) -> dict[str, Any]:
    proposal = _load_json(path)
    if str(proposal.get("artifact") or "") != "stage_b_v1_i8_surgical_rebalance_proposal":
        raise RuntimeError(f"unexpected surgical proposal artifact id: {proposal.get('artifact')}")
    trim_plan = proposal.get("trim_plan")
    if not isinstance(trim_plan, dict):
        raise RuntimeError("surgical proposal missing trim_plan object")
    families = trim_plan.get("families")
    if not isinstance(families, list) or not families:
        raise RuntimeError("surgical proposal trim_plan.families must be non-empty list")
    if int(trim_plan.get("total_rows_to_trim", -1)) != 31:
        raise RuntimeError(
            "surgical proposal total_rows_to_trim must be exactly 31 "
            f"(got {trim_plan.get('total_rows_to_trim')})"
        )
    return proposal


def _apply_surgical_rebalance_plan(
    candidate_train: list[dict[str, Any]],
    candidate_val: list[dict[str, Any]],
    *,
    proposal: dict[str, Any],
    proposal_path: Path,
) -> dict[str, Any]:
    """
    Apply exactly the approved i8 surgical trim plan with hard preservation checks.
    Fail-fast on any drift from approved quotas/constraints.
    """
    combined_before = _combined_rows(candidate_train, candidate_val)
    global_before = _global_targeted_snapshot(combined_before)

    trim_plan = proposal["trim_plan"]
    family_plans = trim_plan["families"]

    # Validate cap-equivalent regime declared in proposal.
    targeted_total = global_before["rows"]
    cap_rows = int(math.floor(float(proposal.get("baseline", {}).get("cap_share_reference", 0.12)) * targeted_total))
    if cap_rows != int(proposal.get("baseline", {}).get("cap_rows_absolute", 95)):
        raise RuntimeError(
            "proposal cap regime mismatch: "
            f"computed cap_rows={cap_rows} proposal={proposal.get('baseline', {}).get('cap_rows_absolute')}"
        )

    trim_lookup = _surgical_trim_index(candidate_train, candidate_val)
    removal_targets: list[tuple[str, int]] = []
    removal_details: list[dict[str, Any]] = []

    pre_family_state: dict[str, dict[str, Any]] = {}
    for fam_plan in family_plans:
        family = str(fam_plan.get("source_case_id") or "")
        if not family:
            raise RuntimeError("surgical proposal has empty source_case_id")
        pre_family_state[family] = _family_snapshot(combined_before, family)

        family_trim_expected = int(fam_plan.get("trim_rows", 0))
        tool_expected = str(fam_plan.get("from_tool") or "")
        quotas = fam_plan.get("prompt_cluster_quotas")
        if not isinstance(quotas, list) or not quotas:
            raise RuntimeError(f"family {family} missing prompt_cluster_quotas")

        family_trim_applied = 0
        for quota in quotas:
            prompt = str(quota.get("prompt") or "")
            trim_count = int(quota.get("trim_count", 0))
            pre_count_expected = int(quota.get("pre_count", 0))
            post_count_expected = int(quota.get("post_count", 0))
            if trim_count <= 0:
                raise RuntimeError(f"invalid trim_count for family={family} prompt={prompt[:48]}")

            key = (family, tool_expected, prompt)
            matches = list(trim_lookup.get(key, []))
            pre_count_actual = len(matches)
            if pre_count_actual != pre_count_expected:
                raise RuntimeError(
                    f"surgical quota pre_count mismatch family={family} tool={tool_expected} "
                    f"expected={pre_count_expected} actual={pre_count_actual} prompt_sha={_sha1_text(prompt)}"
                )
            if pre_count_expected - trim_count != post_count_expected:
                raise RuntimeError(
                    f"surgical quota post_count mismatch family={family} tool={tool_expected} "
                    f"prompt_sha={_sha1_text(prompt)} expected_post={post_count_expected} "
                    f"computed_post={pre_count_expected - trim_count}"
                )

            selected = matches[:trim_count]
            if len(selected) != trim_count:
                raise RuntimeError(
                    f"insufficient rows for quota family={family} tool={tool_expected} "
                    f"needed={trim_count} have={len(selected)} prompt_sha={_sha1_text(prompt)}"
                )

            for split, idx_0 in selected:
                row = candidate_train[idx_0] if split == "train" else candidate_val[idx_0]
                meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
                style = _surgical_trim_style_bucket(_user_prompt(row))
                if family == "i3_adapt_p0_read_file_1":
                    if bool(meta.get("ambiguity_remediation_applied", False)):
                        raise RuntimeError("preservation violation: attempted to trim ambiguity-remediated row")
                    if style != "imperative_line_scoped":
                        raise RuntimeError(
                            "preservation violation: i3_adapt_p0_read_file_1 trim must remain imperative_line_scoped "
                            f"(got {style})"
                        )
                removal_targets.append((split, idx_0))
                removal_details.append(
                    {
                        "split": split,
                        "row_index_1based": idx_0 + 1,
                        "source_case_id": family,
                        "tool": tool_expected,
                        "prompt_sha1": _sha1_text(prompt),
                    }
                )
            family_trim_applied += trim_count

        if family_trim_applied != family_trim_expected:
            raise RuntimeError(
                f"family trim mismatch for {family}: expected={family_trim_expected} applied={family_trim_applied}"
            )

    # No duplicate row removals allowed.
    uniq_targets = sorted(set(removal_targets), key=lambda x: (x[0], x[1]))
    if len(uniq_targets) != len(removal_targets):
        raise RuntimeError("duplicate row removals detected in surgical plan execution")

    expected_total = int(trim_plan.get("total_rows_to_trim", 0))
    if len(uniq_targets) != expected_total:
        raise RuntimeError(
            f"global trim mismatch: expected={expected_total} applied={len(uniq_targets)}"
        )

    # Apply removals in descending index order per split.
    by_split: dict[str, list[int]] = {"train": [], "val": []}
    for split, idx_0 in uniq_targets:
        by_split[split].append(idx_0)
    for split in ("train", "val"):
        rows = candidate_train if split == "train" else candidate_val
        for idx_0 in sorted(by_split[split], reverse=True):
            if idx_0 < 0 or idx_0 >= len(rows):
                raise RuntimeError(f"trim target index out of range: {split}:{idx_0 + 1}")
            rows.pop(idx_0)

    combined_after = _combined_rows(candidate_train, candidate_val)
    global_after = _global_targeted_snapshot(combined_after)

    # Global preservation checks.
    if global_after["targets"] != global_before["targets"]:
        raise RuntimeError("global target payload class preservation failed after surgical trim")
    if global_after["skeletons"] != global_before["skeletons"]:
        raise RuntimeError("global skeleton family preservation failed after surgical trim")
    if global_after["task_narrative_rows"] != global_before["task_narrative_rows"]:
        raise RuntimeError("global task_narrative coverage changed during surgical trim")
    if global_before["rows"] - global_after["rows"] != expected_total:
        raise RuntimeError(
            f"targeted row reduction mismatch: expected={expected_total} "
            f"actual={global_before['rows'] - global_after['rows']}"
        )

    post_family_state: dict[str, dict[str, Any]] = {}
    for fam_plan in family_plans:
        family = str(fam_plan.get("source_case_id") or "")
        post_family_state[family] = _family_snapshot(combined_after, family)

    # Family-specific preservation checks.
    fam_a = "i3_adapt_p0_read_file_1"
    if fam_a in pre_family_state:
        pre = pre_family_state[fam_a]
        post = post_family_state[fam_a]
        if post["ambiguity_remediation_rows"] != pre["ambiguity_remediation_rows"]:
            raise RuntimeError("family preservation failed: ambiguity-remediated rows changed in i3_adapt_p0_read_file_1")
        if "rg_search" in pre["tools"] and "rg_search" not in post["tools"]:
            raise RuntimeError("family preservation failed: rg_search lineage removed in i3_adapt_p0_read_file_1")
        if post["task_narrative_rows"] != pre["task_narrative_rows"]:
            raise RuntimeError("family preservation failed: task_narrative coverage changed in i3_adapt_p0_read_file_1")

    fam_b = "i3_adapt_p0_rg_search_4"
    if fam_b in pre_family_state:
        pre = pre_family_state[fam_b]
        post = post_family_state[fam_b]
        if post["targets"] != pre["targets"]:
            raise RuntimeError("family preservation failed: target payload class changed in i3_adapt_p0_rg_search_4")
        if post["skeletons"] != pre["skeletons"]:
            raise RuntimeError("family preservation failed: skeleton family changed in i3_adapt_p0_rg_search_4")
        if post["prompts"] != pre["prompts"]:
            raise RuntimeError("family preservation failed: prompt family set changed in i3_adapt_p0_rg_search_4")

    # Enforce intended cap-equivalent regime for top families from proposal projection.
    fam_counts = Counter(
        _row_case_id(r, "")
        for r in combined_after
        if _tool_name(r) in TARGETED_TOOLS
    )
    projection = proposal.get("post_trim_projection", {}).get("family_concentration", [])
    for item in projection:
        if not isinstance(item, dict):
            continue
        fam = str(item.get("source_case_id") or "")
        if fam in ("i3_adapt_p0_read_file_1", "i3_adapt_p0_rg_search_4"):
            expected_rows = int(item.get("post_rows", -1))
            actual_rows = int(fam_counts.get(fam, 0))
            if actual_rows != expected_rows:
                raise RuntimeError(
                    f"post-trim cap regime mismatch for {fam}: expected={expected_rows} actual={actual_rows}"
                )

    return {
        "status": "applied",
        "proposal_json": str(proposal_path),
        "total_rows_trimmed": expected_total,
        "cap_rows_absolute": cap_rows,
        "trimmed_rows_by_split": {
            "train": len(by_split["train"]),
            "val": len(by_split["val"]),
        },
        "trimmed_rows_by_family": {
            fam: int(fam_plan.get("trim_rows", 0))
            for fam, fam_plan in ((str(x.get("source_case_id")), x) for x in family_plans)
        },
        "global_targeted_rows_before": global_before["rows"],
        "global_targeted_rows_after": global_after["rows"],
        "global_prompt_uniqueness_ratio_before": round(global_before["prompt_uniqueness_ratio"], 6),
        "global_prompt_uniqueness_ratio_after": round(global_after["prompt_uniqueness_ratio"], 6),
        "rows_trimmed": removal_details,
    }


def _fail_fast_prompt_ambiguity_hard_blocks(ambiguity_audit: dict[str, Any], *, scope: str) -> None:
    hard = ambiguity_audit.get("hard_block_candidates", {})
    if bool(hard.get("prompt_to_multiple_targets", False)):
        raise RuntimeError(
            f"{scope}: identical prompt mapped to multiple targets; "
            f"groups={ambiguity_audit.get('duplicate_prompt_groups_different_target_count')}"
        )
    if bool(hard.get("prompt_to_multiple_tools", False)):
        raise RuntimeError(
            f"{scope}: identical prompt mapped to multiple tools; "
            f"groups={ambiguity_audit.get('duplicate_prompt_groups_different_tool_count')}"
        )
    if bool(hard.get("prompt_tool_to_multiple_arguments", False)):
        raise RuntimeError(
            f"{scope}: identical (prompt,tool) mapped to multiple argument payloads; "
            f"groups={ambiguity_audit.get('duplicate_prompt_tool_groups_different_arguments_count')}"
        )


def _compose_disambiguation_clause(row: dict[str, Any]) -> str:
    tool = _tool_name(row)
    args = _assistant_arguments_obj(row) or {}

    if tool == "read_file":
        path = str(args.get("path") or "")
        ls = args.get("line_start")
        le = args.get("line_end")
        return (
            f"Disambiguation: call read_file with path={path}, "
            f"line_start={ls}, line_end={le}."
        ).strip()

    if tool == "rg_search":
        path = str(args.get("path") or "")
        pattern = str(args.get("pattern") or "")
        if len(pattern) > 72:
            pattern = f"{pattern[:69]}..."
        return (
            f"Disambiguation: call rg_search with path={path}, "
            f"pattern={pattern}."
        ).strip()

    args_sig = _sha1_text(_canonical_json_text(args))
    return f"Disambiguation: call {tool} with arguments signature {args_sig}."


def _apply_prompt_ambiguity_remediation(
    candidate_train: list[dict[str, Any]],
    candidate_val: list[dict[str, Any]],
    ambiguity_audit: dict[str, Any],
) -> dict[str, Any]:
    conflicting_prompts = {
        str(x.get("prompt") or "")
        for x in ambiguity_audit.get("conflicting_prompt_groups", [])
        if str(x.get("prompt") or "")
    }
    conflicting_prompt_tool = {
        (str(x.get("prompt") or ""), str(x.get("tool") or ""))
        for x in ambiguity_audit.get("conflicting_prompt_tool_groups", [])
        if str(x.get("prompt") or "")
    }

    changed = 0
    by_mode = Counter()
    by_tool = Counter()

    for split, rows in (("train", candidate_train), ("val", candidate_val)):
        for idx, row in enumerate(rows, start=1):
            prompt = _user_prompt(row)
            tool = _tool_name(row)
            key = (prompt, tool)
            if prompt not in conflicting_prompts and key not in conflicting_prompt_tool:
                continue

            if tool not in TARGETED_TOOLS:
                raise RuntimeError(
                    f"ambiguity remediation would mutate non-target tool row {split}:{idx} tool={tool}; aborting"
                )

            clause = _compose_disambiguation_clause(row)
            if clause in prompt:
                mode = "already_disambiguated"
                new_prompt = prompt
            else:
                new_prompt = f"{prompt} {clause}".strip()
                mode = "append_clause"
                _set_user_prompt(row, new_prompt)
                changed += 1

            meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
            meta["ambiguity_remediation_applied"] = True
            meta["ambiguity_remediation_mode"] = mode
            meta["ambiguity_remediation_clause_hash"] = _sha1_text(clause)
            meta["ambiguity_remediation_reason"] = "prompt_conflict_hard_block_resolution"
            row["metadata"] = meta
            by_mode[mode] += 1
            by_tool[tool] += 1

    return {
        "rows_changed": changed,
        "rows_touched_by_mode": dict(sorted(by_mode.items(), key=lambda kv: kv[0])),
        "rows_touched_by_tool": dict(sorted(by_tool.items(), key=lambda kv: kv[0])),
        "conflicting_prompt_groups_input": int(ambiguity_audit.get("duplicate_prompt_groups_different_target_count", 0)),
    }


def _run_diagnostics(
    candidate_train: list[dict[str, Any]],
    candidate_val: list[dict[str, Any]],
    reference_train: list[dict[str, Any]],
    reference_val: list[dict[str, Any]],
) -> dict[str, Any]:
    policy = scaffold_policy_defaults()
    return build_full_diagnostics_report(
        _combined_rows(candidate_train, candidate_val),
        reference_rows=_combined_rows(reference_train, reference_val),
        policy=policy,
    )


def _augment_diagnostics_with_ambiguity(
    diagnostics: dict[str, Any],
    ambiguity_audit: dict[str, Any],
) -> dict[str, Any]:
    out = json.loads(json.dumps(diagnostics, ensure_ascii=False))
    checks = out.get("checks")
    if isinstance(checks, dict):
        checks["prompt_ambiguity_audit"] = ambiguity_audit
    review = out.get("review_support")
    if isinstance(review, dict):
        review["ambiguity_audit_summary"] = {
            "duplicate_prompt_groups_different_target_count": ambiguity_audit.get("duplicate_prompt_groups_different_target_count", 0),
            "duplicate_prompt_groups_different_tool_count": ambiguity_audit.get("duplicate_prompt_groups_different_tool_count", 0),
            "duplicate_prompt_tool_groups_different_arguments_count": ambiguity_audit.get("duplicate_prompt_tool_groups_different_arguments_count", 0),
            "rows_in_conflicting_prompt_groups": ambiguity_audit.get("rows_in_conflicting_prompt_groups", 0),
        }
    return out


def _fail_fast_diagnostic_doctrine(diagnostics: dict[str, Any]) -> None:
    forbidden = diagnostics.get("checks", {}).get("forbidden_pattern_scan", {})
    if int(forbidden.get("total_hits", 0) or 0) > 0:
        raise RuntimeError(
            "forbidden-pattern doctrine violation detected: "
            f"total_hits={forbidden.get('total_hits')}"
        )

    diversity = diagnostics.get("review_support", {}).get("diversity_review_summary", {})
    if not bool(diversity.get("pass", False)):
        raise RuntimeError(
            "diversity doctrine violation detected: "
            f"risk_flags={diversity.get('risk_flags', [])}"
        )

    anti = diagnostics.get("review_support", {}).get("anti_homogenization_summary", {})
    if not bool(anti.get("pass", False)):
        raise RuntimeError(
            "anti-homogenization doctrine violation detected: "
            f"risk_signals={anti.get('risk_signals', [])}"
        )

    ambiguity = diagnostics.get("checks", {}).get("prompt_ambiguity_audit", {})
    hard = ambiguity.get("hard_block_candidates", {}) if isinstance(ambiguity, dict) else {}
    if any(bool(hard.get(k, False)) for k in ("prompt_to_multiple_targets", "prompt_to_multiple_tools", "prompt_tool_to_multiple_arguments")):
        raise RuntimeError(f"prompt ambiguity hard-block violation detected: {hard}")


def _build_contamination_audit(
    candidate_train: list[dict[str, Any]],
    candidate_val: list[dict[str, Any]],
    eval_map: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    train_overlap = _overlap_report(candidate_train, eval_map)
    val_overlap = _overlap_report(candidate_val, eval_map)
    combined_overlap = _overlap_report(_combined_rows(candidate_train, candidate_val), eval_map)

    return {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "iteration": RUN_NAME,
        "status": "completed",
        "train_overlap": train_overlap,
        "val_overlap": val_overlap,
        "combined_overlap": combined_overlap,
        "blocking_policy": {
            "heldout_tool_holdout_max_allowed_overlap": 0,
            "fail_fast": True,
        },
        "approval_state": {
            "clean_for_training": False,
            "approved_to_run": False,
        },
    }


def _build_review_package(
    diagnostics: dict[str, Any],
    transform_stats: dict[str, Any],
) -> dict[str, Any]:
    skeleton = diagnostics.get("checks", {}).get("prompt_skeleton_concentration", {})
    styles = diagnostics.get("checks", {}).get("style_bucket_analysis", {})
    lengths = diagnostics.get("checks", {}).get("prompt_length_delta", {})
    ambiguity = diagnostics.get("checks", {}).get("prompt_ambiguity_audit", {})

    targeted_skeleton = skeleton.get("targeted", {}) if isinstance(skeleton, dict) else {}
    targeted_styles = styles.get("targeted_only", []) if isinstance(styles, dict) else []

    return {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "iteration": RUN_NAME,
        "status": "completed",
        "question": "Are parseability gains likely structural, or are we drifting toward local-template coercion?",
        "targeted_prompt_samples": diagnostics.get("review_support", {}).get("targeted_prompt_samples", {}),
        "anchor_variant_distribution": {
            "train": transform_stats["train"]["anchor_mode_counts"],
            "val": transform_stats["val"]["anchor_mode_counts"],
        },
        "top_skeleton_families": targeted_skeleton.get("top_skeletons", []),
        "dominant_style_buckets": targeted_styles[:6],
        "prompt_length_distribution": {
            "delta_targeted": lengths.get("delta_targeted", {}),
            "reference_targeted": lengths.get("reference_targeted", {}),
            "candidate_targeted": lengths.get("candidate_targeted", {}),
        },
        "risk_flags": {
            "diversity": diagnostics.get("review_support", {}).get("diversity_review_summary", {}),
            "anti_homogenization": diagnostics.get("review_support", {}).get("anti_homogenization_summary", {}),
            "prompt_ambiguity_hard_blocks": ambiguity.get("hard_block_candidates", {}),
        },
        "ambiguity_hotspots": {
            "conflicting_prompt_groups": ambiguity.get("conflicting_prompt_groups", []),
            "conflicting_prompt_tool_groups": ambiguity.get("conflicting_prompt_tool_groups", []),
            "high_frequency_prompt_reuse": ambiguity.get("high_frequency_prompt_reuse", []),
            "high_frequency_skeleton_reuse": ambiguity.get("high_frequency_skeleton_reuse", []),
            "source_case_divergence_groups": ambiguity.get("source_case_divergence_groups", []),
        },
        "interpretation_guidance": [
            "If top1 targeted skeleton share rises while unique skeletons shrink, treat as local-template coercion risk.",
            "If targeted prompt-length deltas spike with stable tool distribution, inspect for anchor over-imprinting.",
            "If forbidden-pattern hits appear, invalidate candidate and revise intervention shaping.",
        ],
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_promote": False,
        },
    }


def _build_summary(
    *,
    inputs: BuilderInputs,
    outputs: OutputPaths,
    seed: int,
    parent_invariants: dict[str, Any],
    candidate_train: list[dict[str, Any]],
    candidate_val: list[dict[str, Any]],
    diagnostics: dict[str, Any],
    prompt_ambiguity_audit: dict[str, Any],
    contamination_audit: dict[str, Any],
    transform_stats: dict[str, Any],
) -> dict[str, Any]:
    train_overlap = contamination_audit["train_overlap"]
    val_overlap = contamination_audit["val_overlap"]
    surgical = transform_stats.get("surgical_rebalance", {}) if isinstance(transform_stats, dict) else {}
    fixed_row_count = not bool(surgical.get("status") == "applied")

    return {
        "generated_utc": _now_utc(),
        "seed": seed,
        "inputs": {
            "parent_train_jsonl": str(inputs.parent_train_jsonl),
            "parent_val_jsonl": str(inputs.parent_val_jsonl),
            "parent_summary_json": str(inputs.parent_summary_json),
            "eval_paths": {
                "heldout_validation": str(inputs.eval_heldout_jsonl),
                "tool_holdout": str(inputs.eval_tool_holdout_jsonl),
                "no_call": str(inputs.eval_no_call_jsonl),
                "adversarial": str(inputs.eval_adversarial_jsonl),
                "direct_answer": str(inputs.eval_direct_answer_jsonl),
            },
        },
        "policy": {
            "fixed_row_count": fixed_row_count,
            "train_rows": len(candidate_train),
            "val_rows": len(candidate_val),
            "targeted_recovery": "localized parse-anchor shaping on rg_search/read_file from i3 parent baseline",
            "localized_intervention_only": True,
            "forbidden_global_pressures": list(FORBIDDEN_GLOBAL_PRESSURES),
            "canonical_eval_rows_used_for_training": False,
            "approved_to_run": False,
        },
        "parent_invariants": parent_invariants,
        "outputs": {
            "train_jsonl": str(outputs.train_jsonl),
            "val_jsonl": str(outputs.val_jsonl),
            "summary_json": str(outputs.summary_json),
            "diagnostics_json": str(outputs.diagnostics_json),
            "contamination_audit_json": str(outputs.contamination_audit_json),
            "prompt_ambiguity_audit_json": str(outputs.prompt_ambiguity_audit_json),
            "review_package_json": str(outputs.review_package_json),
        },
        "composition": {
            "train_categories": _count_categories(candidate_train),
            "val_categories": _count_categories(candidate_val),
            "train_tool_counts": _count_tools(candidate_train),
            "val_tool_counts": _count_tools(candidate_val),
        },
        "intervention": {
            "targeted_tools": list(TARGETED_TOOLS),
            "train": transform_stats["train"],
            "val": transform_stats["val"],
            "surgical_rebalance": surgical,
        },
        "overlap_audit": {
            "train": train_overlap,
            "val": val_overlap,
            "combined": contamination_audit["combined_overlap"],
        },
        "diagnostics_highlights": {
            "diversity_review_summary": diagnostics.get("review_support", {}).get("diversity_review_summary", {}),
            "anti_homogenization_summary": diagnostics.get("review_support", {}).get("anti_homogenization_summary", {}),
            "targeted_distribution": diagnostics.get("checks", {}).get("targeted_tool_distribution", {}),
            "prompt_ambiguity_hard_blocks": prompt_ambiguity_audit.get("hard_block_candidates", {}),
            "prompt_ambiguity_counts": {
                "duplicate_prompt_groups_different_target_count": prompt_ambiguity_audit.get("duplicate_prompt_groups_different_target_count", 0),
                "duplicate_prompt_groups_different_tool_count": prompt_ambiguity_audit.get("duplicate_prompt_groups_different_tool_count", 0),
                "duplicate_prompt_tool_groups_different_arguments_count": prompt_ambiguity_audit.get("duplicate_prompt_tool_groups_different_arguments_count", 0),
            },
        },
        "hashes": {
            "train_sha256": _sha256_file(outputs.train_jsonl),
            "val_sha256": _sha256_file(outputs.val_jsonl),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Stage B i8 candidate dataset package.")
    parser.add_argument(
        "--parent-train-jsonl",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl",
    )
    parser.add_argument(
        "--parent-val-jsonl",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_val.jsonl",
    )
    parser.add_argument(
        "--parent-summary-json",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_summary.json",
    )

    parser.add_argument("--eval-heldout-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/heldout_validation.jsonl")
    parser.add_argument("--eval-tool-holdout-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/tool_holdout.jsonl")
    parser.add_argument("--eval-no-call-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/no_call.jsonl")
    parser.add_argument("--eval-adversarial-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/adversarial.jsonl")
    parser.add_argument("--eval-direct-answer-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/direct_answer.jsonl")
    parser.add_argument(
        "--surgical-rebalance-proposal-json",
        default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i8_surgical_rebalance_proposal.json",
    )

    parser.add_argument("--output-root", default="/opt/ai-stack/assistant-training/data/v1_0")
    parser.add_argument("--report-root", default="/opt/ai-stack/assistant-training/manifests/reports")
    parser.add_argument("--seed", type=int, default=20260526)

    # Explicit unlock flags: generation remains opt-in and auditable.
    parser.add_argument("--enable-dataset-emission", action="store_true")
    parser.add_argument("--allow-generation-phase", action="store_true")
    parser.add_argument("--enable-surgical-rebalance", action="store_true")

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    _fail_fast_generation_unlock(args)
    _fail_fast_surgical_rebalance_unlock(args)

    inputs = _resolve_inputs(args)
    outputs = _resolve_outputs(args)
    _fail_fast_input_validation(inputs)

    parent_train = _load_jsonl(inputs.parent_train_jsonl)
    parent_val = _load_jsonl(inputs.parent_val_jsonl)
    _ = _load_json(inputs.parent_summary_json)

    parent_invariants = _validate_parent_invariants(parent_train, parent_val)

    candidate_train, train_stats = _transform_split_rows(parent_train, split="train", seed=int(args.seed))
    candidate_val, val_stats = _transform_split_rows(parent_val, split="val", seed=int(args.seed))

    _validate_localized_integrity(parent_train, candidate_train, split="train")
    _validate_localized_integrity(parent_val, candidate_val, split="val")

    initial_ambiguity_audit = _build_prompt_ambiguity_audit(_combined_rows(candidate_train, candidate_val))
    remediation_stats = {
        "applied": False,
        "details": {},
    }
    if any(
        bool(initial_ambiguity_audit.get("hard_block_candidates", {}).get(k, False))
        for k in ("prompt_to_multiple_targets", "prompt_to_multiple_tools", "prompt_tool_to_multiple_arguments")
    ):
        remediation_details = _apply_prompt_ambiguity_remediation(
            candidate_train,
            candidate_val,
            initial_ambiguity_audit,
        )
        remediation_stats = {
            "applied": True,
            "details": remediation_details,
        }
    train_stats["ambiguity_remediation"] = remediation_stats
    val_stats["ambiguity_remediation"] = remediation_stats

    # Re-validate localized boundaries after ambiguity remediation pass.
    _validate_localized_integrity(parent_train, candidate_train, split="train")
    _validate_localized_integrity(parent_val, candidate_val, split="val")

    prompt_ambiguity_audit = _build_prompt_ambiguity_audit(_combined_rows(candidate_train, candidate_val))
    prompt_ambiguity_audit["remediation"] = remediation_stats
    _fail_fast_prompt_ambiguity_hard_blocks(prompt_ambiguity_audit, scope="candidate_dataset")

    proposal = _load_surgical_rebalance_proposal(inputs.surgical_rebalance_proposal_json)
    surgical_rebalance_stats = _apply_surgical_rebalance_plan(
        candidate_train,
        candidate_val,
        proposal=proposal,
        proposal_path=inputs.surgical_rebalance_proposal_json,
    )

    # Ambiguity hard blocks must remain clean after deterministic trimming.
    prompt_ambiguity_audit = _build_prompt_ambiguity_audit(_combined_rows(candidate_train, candidate_val))
    prompt_ambiguity_audit["remediation"] = remediation_stats
    prompt_ambiguity_audit["surgical_rebalance"] = {
        "applied": True,
        "proposal_json": str(inputs.surgical_rebalance_proposal_json),
        "stats": surgical_rebalance_stats,
    }
    _fail_fast_prompt_ambiguity_hard_blocks(prompt_ambiguity_audit, scope="candidate_dataset_post_trim")

    eval_map = _collect_eval_map(inputs)
    train_overlap = _overlap_report(candidate_train, eval_map)
    val_overlap = _overlap_report(candidate_val, eval_map)

    _fail_fast_overlap_guard(train_overlap, scope="train")
    _fail_fast_overlap_guard(val_overlap, scope="val")

    diagnostics = _run_diagnostics(candidate_train, candidate_val, parent_train, parent_val)
    diagnostics = _augment_diagnostics_with_ambiguity(diagnostics, prompt_ambiguity_audit)
    _fail_fast_diagnostic_doctrine(diagnostics)

    contamination_audit = _build_contamination_audit(candidate_train, candidate_val, eval_map)
    review_package = _build_review_package(
        diagnostics,
        transform_stats={
            "train": train_stats,
            "val": val_stats,
            "surgical_rebalance": surgical_rebalance_stats,
        },
    )

    # Output emission only after all fail-fast checks pass.
    _write_jsonl(outputs.train_jsonl, candidate_train)
    _write_jsonl(outputs.val_jsonl, candidate_val)
    _write_json(outputs.diagnostics_json, diagnostics)
    _write_json(outputs.contamination_audit_json, contamination_audit)
    _write_json(outputs.prompt_ambiguity_audit_json, prompt_ambiguity_audit)
    _write_json(outputs.review_package_json, review_package)

    summary = _build_summary(
        inputs=inputs,
        outputs=outputs,
        seed=int(args.seed),
        parent_invariants=parent_invariants,
        candidate_train=candidate_train,
        candidate_val=candidate_val,
        diagnostics=diagnostics,
        prompt_ambiguity_audit=prompt_ambiguity_audit,
        contamination_audit=contamination_audit,
        transform_stats={
            "train": train_stats,
            "val": val_stats,
            "surgical_rebalance": surgical_rebalance_stats,
        },
    )
    _write_json(outputs.summary_json, summary)

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
