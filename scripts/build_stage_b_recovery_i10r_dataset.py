#!/usr/bin/env python3
"""
Build Stage B i10r deterministic exposure-correction dataset package.

Governance boundaries:
- Deterministic thinning only (S2_balanced_recommended).
- No semantic prompt rewrites, no synthetic row creation.
- No training, no canonical eval execution, no approval-gate opening.
- Canonical evaluation semantics and thresholds remain unchanged.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from build_stage_b_v1_i10_family_concentration_review import (
    build_review as build_family_concentration_review,
    _write_markdown as write_family_concentration_markdown,
)
from i10_diagnostics_scaffold import (
    build_full_diagnostics_report,
    build_intervention_annotations,
    run_prompt_ambiguity_audit,
    scaffold_policy_defaults,
)

RUN_NAME = "stage_b_llama31_8b_base_v1_i10r"
PARENT_ITERATION = "stage_b_llama31_8b_base_v1_i10"
TARGETED_TOOLS = ("read_file", "rg_search")

GROUP_I10_CONV = "i10_conversion"
GROUP_I9_CONV = "i9_conversion"
GROUP_I3_ADAPT = "i3_adapt"
GROUP_RISKY_LEGACY = "legacy_risky"

RISKY_PREFIXES = ("i3_read_literal_", "i3_rg_readstyle_", "i3_long_rg_")

# Approved S2 retention policy.
S2_RETAIN = {
    GROUP_I10_CONV: 1.00,
    GROUP_I9_CONV: 1.00,
    GROUP_I3_ADAPT: 0.55,
    GROUP_RISKY_LEGACY: 0.30,
}
S2_FLOOR_CAP = {
    GROUP_I10_CONV: (0, 10_000),
    GROUP_I9_CONV: (0, 10_000),
    GROUP_I3_ADAPT: (28, 52),
    GROUP_RISKY_LEGACY: (2, 4),
}

TARGET_ENVELOPE = {
    "legacy_total_min": 0.64,
    "legacy_total_max": 0.69,
    "healthy_conversion_min": 0.31,
    "healthy_conversion_max": 0.36,
}


@dataclass(frozen=True)
class Inputs:
    parent_train_jsonl: Path
    parent_val_jsonl: Path
    parent_summary_json: Path
    i9_behavioral_review_json: Path
    i3_train_jsonl: Path
    i3_val_jsonl: Path
    eval_heldout_jsonl: Path
    eval_tool_holdout_jsonl: Path
    eval_no_call_jsonl: Path
    eval_adversarial_jsonl: Path
    eval_direct_answer_jsonl: Path
    strategy_json: Path


@dataclass(frozen=True)
class Outputs:
    train_jsonl: Path
    val_jsonl: Path
    summary_json: Path
    diagnostics_json: Path
    family_concentration_json: Path
    family_concentration_md: Path
    effective_exposure_projection_json: Path
    prompt_ambiguity_audit_json: Path
    contamination_audit_json: Path
    collapse_watch_telemetry_json: Path
    human_review_package_json: Path
    human_review_package_md: Path
    preflight_validation_json: Path


@dataclass(frozen=True)
class RowRef:
    split: str
    index_0: int
    row: dict[str, Any]
    source_case_id: str
    tool: str
    prompt: str
    target_canon: str
    args_canon: str


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_json(path: Path) -> dict[str, Any]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise RuntimeError(f"expected JSON object at {path}")
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


def _assistant_args_canon(row: dict[str, Any]) -> str:
    msgs = row.get("messages")
    if not isinstance(msgs, list):
        return "null"
    for msg in msgs:
        if not isinstance(msg, dict) or msg.get("role") != "assistant":
            continue
        tc = msg.get("tool_calls")
        if not isinstance(tc, list) or not tc or not isinstance(tc[0], dict):
            return "null"
        fn = tc[0].get("function")
        if not isinstance(fn, dict):
            return "null"
        args = fn.get("arguments")
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except Exception:
                pass
        return _canonical_json_text(args)
    return "null"


def _source_case_id(row: dict[str, Any], fallback: str) -> str:
    meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    out = str(meta.get("source_case_id") or meta.get("case_id") or "").strip()
    return out or fallback


def _sha1_text(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def _is_tool_row(row: dict[str, Any]) -> bool:
    return bool(_tool_name(row))


def _group_from_case_id(case_id: str) -> str:
    if case_id.startswith("i10_conv_"):
        return GROUP_I10_CONV
    if case_id.startswith("i9_conv_"):
        return GROUP_I9_CONV
    if case_id.startswith("i3_adapt_"):
        return GROUP_I3_ADAPT
    if case_id.startswith(RISKY_PREFIXES):
        return GROUP_RISKY_LEGACY
    raise RuntimeError(f"unexpected targeted source_case_id group: {case_id}")


def _round_half_up(x: float) -> int:
    return int(math.floor(x + 0.5))


def _compute_keep_count(group: str, row_count: int) -> int:
    factor = float(S2_RETAIN[group])
    raw = _round_half_up(row_count * factor)
    floor_rows, cap_rows = S2_FLOOR_CAP[group]
    return max(floor_rows, min(cap_rows, raw))


def _stable_row_key(ref: RowRef) -> tuple[str, str]:
    key = "|".join(
        [
            ref.source_case_id,
            ref.tool,
            ref.prompt,
            ref.target_canon,
            ref.args_canon,
            ref.split,
            str(ref.index_0),
        ]
    )
    return (_sha1_text(key), f"{ref.split}:{ref.index_0:08d}")


def _allocate_quotas(counts: dict[str, int], keep_total: int, *, preserve_min_one: bool = True) -> dict[str, int]:
    active = {k: int(v) for k, v in counts.items() if int(v) > 0}
    if keep_total < 0:
        raise RuntimeError("keep_total must be non-negative")
    if keep_total > sum(active.values()):
        raise RuntimeError("keep_total exceeds available rows")
    if not active:
        return {k: 0 for k in counts}

    quotas = {k: 0 for k in active}
    total = sum(active.values())
    fractional: list[tuple[float, str]] = []
    for k, c in active.items():
        raw = keep_total * (c / total)
        base = int(math.floor(raw))
        quotas[k] = min(base, c)
        fractional.append((raw - base, k))

    if preserve_min_one and keep_total >= len(active):
        for k, c in active.items():
            if quotas[k] == 0 and c > 0:
                quotas[k] = 1

    assigned = sum(quotas.values())
    if assigned > keep_total:
        # Reduce deterministically from the largest quotas first.
        for _, k in sorted(((quotas[k], k) for k in quotas), key=lambda kv: (-kv[0], kv[1])):
            if assigned <= keep_total:
                break
            if quotas[k] <= 0:
                continue
            quotas[k] -= 1
            assigned -= 1

    if assigned < keep_total:
        for _, k in sorted(fractional, key=lambda kv: (-kv[0], kv[1])):
            if assigned >= keep_total:
                break
            if quotas[k] >= active[k]:
                continue
            quotas[k] += 1
            assigned += 1

    if assigned < keep_total:
        # Final deterministic fill from any remaining capacity.
        for k in sorted(active.keys()):
            if assigned >= keep_total:
                break
            room = active[k] - quotas[k]
            if room <= 0:
                continue
            add = min(room, keep_total - assigned)
            quotas[k] += add
            assigned += add

    if assigned != keep_total:
        raise RuntimeError(f"quota allocation mismatch: expected={keep_total} got={assigned}")

    out = {k: 0 for k in counts}
    out.update(quotas)
    return out


def _select_family_rows(family: str, refs: list[RowRef], keep_total: int) -> list[RowRef]:
    if keep_total <= 0:
        return []
    if keep_total > len(refs):
        raise RuntimeError(f"family={family} keep_total exceeds row count")
    if keep_total == len(refs):
        return sorted(refs, key=_stable_row_key)

    by_split: dict[str, list[RowRef]] = defaultdict(list)
    for r in refs:
        by_split[r.split].append(r)

    split_counts = {k: len(v) for k, v in by_split.items()}
    split_quota = _allocate_quotas(split_counts, keep_total, preserve_min_one=True)

    selected: list[RowRef] = []
    for split in sorted(by_split.keys()):
        split_refs = sorted(by_split[split], key=_stable_row_key)
        need = split_quota.get(split, 0)
        if need <= 0:
            continue
        if need > len(split_refs):
            raise RuntimeError(f"family={family} split={split} quota exceeds rows")

        by_tool: dict[str, list[RowRef]] = defaultdict(list)
        for ref in split_refs:
            by_tool[ref.tool].append(ref)

        if len(by_tool) == 1:
            selected.extend(split_refs[:need])
            continue

        tool_counts = {k: len(v) for k, v in by_tool.items()}
        tool_quota = _allocate_quotas(tool_counts, need, preserve_min_one=True)
        picked: list[RowRef] = []
        for tool in sorted(by_tool.keys()):
            rows = sorted(by_tool[tool], key=_stable_row_key)
            take = tool_quota.get(tool, 0)
            picked.extend(rows[:take])

        if len(picked) < need:
            picked_keys = {(r.split, r.index_0) for r in picked}
            for ref in split_refs:
                if len(picked) >= need:
                    break
                if (ref.split, ref.index_0) in picked_keys:
                    continue
                picked.append(ref)

        if len(picked) != need:
            raise RuntimeError(
                f"family={family} split={split} tool-stratified selection mismatch: "
                f"expected={need} got={len(picked)}"
            )
        selected.extend(sorted(picked, key=_stable_row_key))

    if len(selected) != keep_total:
        raise RuntimeError(f"family={family} selected row mismatch: expected={keep_total} got={len(selected)}")
    return selected


def _collect_rows(train_rows: list[dict[str, Any]], val_rows: list[dict[str, Any]]) -> list[RowRef]:
    out: list[RowRef] = []
    for split, rows in (("train", train_rows), ("val", val_rows)):
        for idx_0, row in enumerate(rows):
            tool = _tool_name(row)
            if tool not in TARGETED_TOOLS:
                continue
            case_id = _source_case_id(row, f"{split}:{idx_0 + 1}")
            out.append(
                RowRef(
                    split=split,
                    index_0=idx_0,
                    row=row,
                    source_case_id=case_id,
                    tool=tool,
                    prompt=_user_prompt(row),
                    target_canon=_assistant_target_canon(row),
                    args_canon=_assistant_args_canon(row),
                )
            )
    return out


def _summarize_group_counts(refs: list[RowRef]) -> dict[str, int]:
    out = Counter()
    for ref in refs:
        out[_group_from_case_id(ref.source_case_id)] += 1
    return dict(sorted(out.items(), key=lambda kv: kv[0]))


def _targeted_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    annotations = [
        a
        for a in build_intervention_annotations(rows, targeted_tools=TARGETED_TOOLS)
        if bool(a.get("is_targeted_family", False))
    ]
    prompt_count = len(annotations)
    prompt_unique = len({str(a.get("prompt") or "") for a in annotations})
    skeleton_unique = len({str(a.get("skeleton_id") or "") for a in annotations})
    tool_args_unique = len(
        {
            (str(a.get("tool") or ""), str(a.get("arguments_canon") or ""))
            for a in annotations
        }
    )
    return {
        "targeted_rows": prompt_count,
        "prompt_uniqueness_ratio": round(prompt_unique / prompt_count, 6) if prompt_count else 0.0,
        "skeleton_uniqueness_ratio": round(skeleton_unique / prompt_count, 6) if prompt_count else 0.0,
        "unique_tool_args_ratio": round(tool_args_unique / prompt_count, 6) if prompt_count else 0.0,
    }


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
    train_overlap = {k: _prompt_overlap(train_rows, v) for k, v in eval_map.items()}
    val_overlap = {k: _prompt_overlap(val_rows, v) for k, v in eval_map.items()}
    combined_overlap = {k: _prompt_overlap(combined, v) for k, v in eval_map.items()}
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


def _build_ambiguity_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    annotations = build_intervention_annotations(rows, targeted_tools=TARGETED_TOOLS)
    audit = run_prompt_ambiguity_audit(annotations)
    audit["generated_utc"] = _now_utc()
    audit["iteration"] = RUN_NAME
    return audit


def _fail_fast_ambiguity_hard_blocks(audit: dict[str, Any]) -> None:
    hard = audit.get("hard_block_candidates", {}) if isinstance(audit.get("hard_block_candidates"), dict) else {}
    if bool(hard.get("prompt_to_multiple_targets", False)):
        raise RuntimeError("ambiguity hard block: prompt_to_multiple_targets")
    if bool(hard.get("prompt_to_multiple_tools", False)):
        raise RuntimeError("ambiguity hard block: prompt_to_multiple_tools")
    if bool(hard.get("prompt_tool_to_multiple_arguments", False)):
        raise RuntimeError("ambiguity hard block: prompt_tool_to_multiple_arguments")


def _hash_row(row: dict[str, Any]) -> str:
    return _sha1_text(_canonical_json_text(row))


def _non_tool_hash_multiset(rows: list[dict[str, Any]]) -> Counter[str]:
    out = Counter()
    for row in rows:
        if _is_tool_row(row):
            continue
        out[_hash_row(row)] += 1
    return out


def _build_effective_exposure_projection(
    baseline_rows: list[dict[str, Any]],
    revised_rows: list[dict[str, Any]],
    *,
    baseline_targeted_refs: list[RowRef],
    revised_targeted_refs: list[RowRef],
) -> dict[str, Any]:
    before_groups = Counter(_group_from_case_id(r.source_case_id) for r in baseline_targeted_refs)
    after_groups = Counter(_group_from_case_id(r.source_case_id) for r in revised_targeted_refs)
    before_total = sum(before_groups.values())
    after_total = sum(after_groups.values())

    before_legacy = before_groups.get(GROUP_I3_ADAPT, 0) + before_groups.get(GROUP_RISKY_LEGACY, 0)
    after_legacy = after_groups.get(GROUP_I3_ADAPT, 0) + after_groups.get(GROUP_RISKY_LEGACY, 0)

    before_healthy = before_groups.get(GROUP_I9_CONV, 0) + before_groups.get(GROUP_I10_CONV, 0)
    after_healthy = after_groups.get(GROUP_I9_CONV, 0) + after_groups.get(GROUP_I10_CONV, 0)

    before_metrics = _targeted_metrics(baseline_rows)
    after_metrics = _targeted_metrics(revised_rows)

    legacy_share_after = (after_legacy / after_total) if after_total else 0.0
    healthy_share_after = (after_healthy / after_total) if after_total else 0.0

    return {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "iteration": RUN_NAME,
        "strategy_reference": "S2_balanced_recommended",
        "target_envelope": TARGET_ENVELOPE,
        "before": {
            "iteration": PARENT_ITERATION,
            "targeted_total_rows": before_total,
            "group_counts": dict(sorted(before_groups.items(), key=lambda kv: kv[0])),
            "group_shares": {
                "legacy_total": round(before_legacy / before_total, 6) if before_total else 0.0,
                "healthy_conversion_total": round(before_healthy / before_total, 6) if before_total else 0.0,
            },
            "effective_exposure_proxies": before_metrics,
        },
        "after": {
            "iteration": RUN_NAME,
            "targeted_total_rows": after_total,
            "group_counts": dict(sorted(after_groups.items(), key=lambda kv: kv[0])),
            "group_shares": {
                "legacy_total": round(legacy_share_after, 6),
                "healthy_conversion_total": round(healthy_share_after, 6),
            },
            "effective_exposure_proxies": after_metrics,
        },
        "delta_after_minus_before": {
            "targeted_rows": after_total - before_total,
            "legacy_total_share": round(
                (after_legacy / after_total if after_total else 0.0) - (before_legacy / before_total if before_total else 0.0),
                6,
            ),
            "healthy_conversion_share": round(
                (after_healthy / after_total if after_total else 0.0) - (before_healthy / before_total if before_total else 0.0),
                6,
            ),
            "prompt_uniqueness_ratio": round(
                after_metrics["prompt_uniqueness_ratio"] - before_metrics["prompt_uniqueness_ratio"], 6
            ),
            "skeleton_uniqueness_ratio": round(
                after_metrics["skeleton_uniqueness_ratio"] - before_metrics["skeleton_uniqueness_ratio"], 6
            ),
            "unique_tool_args_ratio": round(
                after_metrics["unique_tool_args_ratio"] - before_metrics["unique_tool_args_ratio"], 6
            ),
        },
        "envelope_assessment": {
            "legacy_total_share": round(legacy_share_after, 6),
            "healthy_conversion_total_share": round(healthy_share_after, 6),
            "legacy_within_target": TARGET_ENVELOPE["legacy_total_min"] <= legacy_share_after <= TARGET_ENVELOPE["legacy_total_max"],
            "healthy_conversion_within_target": (
                TARGET_ENVELOPE["healthy_conversion_min"] <= healthy_share_after <= TARGET_ENVELOPE["healthy_conversion_max"]
            ),
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
    lines.append("# Stage B i10r Human Review Package")
    lines.append("")
    lines.append(f"- Generated UTC: {report.get('generated_utc')}")
    lines.append(f"- Iteration: {report.get('iteration')}")
    lines.append("")
    lines.append("## Exposure Envelope")
    env = report.get("exposure_envelope", {})
    lines.append(f"- legacy_total_share: {env.get('legacy_total_share')}")
    lines.append(f"- healthy_conversion_total_share: {env.get('healthy_conversion_total_share')}")
    lines.append(f"- envelope_pass: {env.get('pass')}")
    lines.append("")
    lines.append("## Diversity / Concentration")
    div = report.get("diversity", {})
    lines.append(f"- prompt_uniqueness_ratio_delta: {div.get('prompt_uniqueness_ratio_delta')}")
    lines.append(f"- skeleton_uniqueness_ratio_delta: {div.get('skeleton_uniqueness_ratio_delta')}")
    lines.append(f"- top_family_share_after: {div.get('top_family_share_after')}")
    lines.append("")
    lines.append("## Hygiene Gates")
    hygiene = report.get("hygiene", {})
    lines.append(f"- ambiguity_hard_blocks_clean: {hygiene.get('ambiguity_hard_blocks_clean')}")
    lines.append(f"- contamination_heldout_clean: {hygiene.get('contamination_heldout_clean')}")
    lines.append(f"- contamination_tool_holdout_clean: {hygiene.get('contamination_tool_holdout_clean')}")
    lines.append("")
    lines.append("## Doctrine Guidance")
    for item in report.get("interpretation_guidance", []):
        lines.append(f"- {item}")
    lines.append("")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _build_preflight_validation(
    *,
    parent_train: list[dict[str, Any]],
    parent_val: list[dict[str, Any]],
    revised_train: list[dict[str, Any]],
    revised_val: list[dict[str, Any]],
    summary: dict[str, Any],
    diagnostics: dict[str, Any],
    ambiguity_audit: dict[str, Any],
    contamination_audit: dict[str, Any],
    family_report: dict[str, Any],
    exposure_projection: dict[str, Any],
    human_review: dict[str, Any],
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def add_check(name: str, ok: bool, detail: str, *, level: str = "fail") -> None:
        checks.append(
            {
                "name": name,
                "status": "pass" if ok else ("warn" if level == "warn" else "fail"),
                "detail": detail if ok else detail,
            }
        )

    parent_non_tool_train = _non_tool_hash_multiset(parent_train)
    parent_non_tool_val = _non_tool_hash_multiset(parent_val)
    revised_non_tool_train = _non_tool_hash_multiset(revised_train)
    revised_non_tool_val = _non_tool_hash_multiset(revised_val)

    add_check("summary_iteration_i10r", summary.get("iteration") == RUN_NAME, f"iteration={summary.get('iteration')}")
    add_check(
        "summary_approval_flags_closed",
        summary.get("approval_state") == {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
        f"approval_state={summary.get('approval_state')}",
    )

    hard = ambiguity_audit.get("hard_block_candidates", {}) if isinstance(ambiguity_audit.get("hard_block_candidates"), dict) else {}
    add_check(
        "ambiguity_hard_blocks_clean",
        (not bool(hard.get("prompt_to_multiple_targets", False)))
        and (not bool(hard.get("prompt_to_multiple_tools", False)))
        and (not bool(hard.get("prompt_tool_to_multiple_arguments", False))),
        f"hard_blocks={hard}",
    )

    heldout = contamination_audit.get("combined_overlap", {}).get("heldout_validation")
    tool_holdout = contamination_audit.get("combined_overlap", {}).get("tool_holdout")
    add_check(
        "contamination_heldout_zero",
        heldout == {"prompt_overlap": 0, "target_overlap": 0, "source_case_id_overlap": 0},
        f"heldout={heldout}",
    )
    add_check(
        "contamination_tool_holdout_zero",
        tool_holdout == {"prompt_overlap": 0, "target_overlap": 0, "source_case_id_overlap": 0},
        f"tool_holdout={tool_holdout}",
    )

    forbidden_hits = int(diagnostics.get("checks", {}).get("forbidden_pattern_scan", {}).get("total_hits", 0) or 0)
    add_check("forbidden_pattern_hits_zero", forbidden_hits == 0, f"total_hits={forbidden_hits}")

    diversity_pass = bool(diagnostics.get("review_support", {}).get("diversity_review_summary", {}).get("pass", False))
    anti_pass = bool(diagnostics.get("review_support", {}).get("anti_homogenization_summary", {}).get("pass", False))
    add_check("diversity_pass", diversity_pass, f"diversity_pass={diversity_pass}")
    add_check("anti_homogenization_pass", anti_pass, f"anti_pass={anti_pass}")

    add_check(
        "non_tool_train_unchanged",
        parent_non_tool_train == revised_non_tool_train,
        f"parent_non_tool_train={sum(parent_non_tool_train.values())} revised_non_tool_train={sum(revised_non_tool_train.values())}",
    )
    add_check(
        "non_tool_val_unchanged",
        parent_non_tool_val == revised_non_tool_val,
        f"parent_non_tool_val={sum(parent_non_tool_val.values())} revised_non_tool_val={sum(revised_non_tool_val.values())}",
    )

    env = exposure_projection.get("envelope_assessment", {})
    add_check(
        "exposure_envelope_target_hit",
        bool(env.get("legacy_within_target", False)) and bool(env.get("healthy_conversion_within_target", False)),
        f"envelope={env}",
    )

    largest = family_report.get("ranked_summaries", {}).get("top_largest_families", [])
    top_share = float(largest[0].get("percent_of_targeted_dataset", 0.0) / 100.0) if largest else 0.0
    add_check("top_family_share_below_10pct_warn", top_share <= 0.10, f"top_share={top_share:.6f}", level="warn")

    # Explicitly preserve i3_adapt_p0_read_file_1 as a retained but thinned stress anchor.
    per_family = family_report.get("per_family_metrics", [])
    rf1 = None
    for fam in per_family:
        if fam.get("source_case_id") == "i3_adapt_p0_read_file_1":
            rf1 = fam
            break
    add_check(
        "i3_adapt_p0_read_file_1_retained_and_thinned",
        bool(rf1) and 0 < int(rf1.get("row_count", 0)) < 95,
        f"row_count={(rf1 or {}).get('row_count')}",
    )

    add_check(
        "human_review_approval_closed",
        human_review.get("approval_state")
        == {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
        f"approval_state={human_review.get('approval_state')}",
    )

    summary_counts = Counter(c["status"] for c in checks)
    status = "preflight_validation_completed"
    if summary_counts.get("fail", 0) > 0:
        status = "preflight_validation_failed"
    return {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "iteration": RUN_NAME,
        "status": status,
        "summary": {
            "pass": int(summary_counts.get("pass", 0)),
            "warn": int(summary_counts.get("warn", 0)),
            "fail": int(summary_counts.get("fail", 0)),
        },
        "checks": checks,
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }


def _build_summary(
    *,
    inputs: Inputs,
    outputs: Outputs,
    parent_train: list[dict[str, Any]],
    parent_val: list[dict[str, Any]],
    revised_train: list[dict[str, Any]],
    revised_val: list[dict[str, Any]],
    retention_by_family: dict[str, dict[str, int]],
    removed_rows: list[dict[str, Any]],
    contamination_audit: dict[str, Any],
    diagnostics: dict[str, Any],
    ambiguity_audit: dict[str, Any],
) -> dict[str, Any]:
    parent_targeted = _collect_rows(parent_train, parent_val)
    revised_targeted = _collect_rows(revised_train, revised_val)
    parent_group_counts = _summarize_group_counts(parent_targeted)
    revised_group_counts = _summarize_group_counts(revised_targeted)

    parent_total = sum(parent_group_counts.values())
    revised_total = sum(revised_group_counts.values())

    legacy_parent = parent_group_counts.get(GROUP_I3_ADAPT, 0) + parent_group_counts.get(GROUP_RISKY_LEGACY, 0)
    legacy_revised = revised_group_counts.get(GROUP_I3_ADAPT, 0) + revised_group_counts.get(GROUP_RISKY_LEGACY, 0)

    healthy_parent = parent_group_counts.get(GROUP_I9_CONV, 0) + parent_group_counts.get(GROUP_I10_CONV, 0)
    healthy_revised = revised_group_counts.get(GROUP_I9_CONV, 0) + revised_group_counts.get(GROUP_I10_CONV, 0)

    return {
        "generated_utc": _now_utc(),
        "iteration": RUN_NAME,
        "lineage": {
            "parent_dataset_iteration": PARENT_ITERATION,
            "objective": "deterministic_exposure_geometry_correction_without_procedural_drift",
            "targeted_tools": list(TARGETED_TOOLS),
        },
        "inputs": {
            "parent_train_jsonl": str(inputs.parent_train_jsonl),
            "parent_val_jsonl": str(inputs.parent_val_jsonl),
            "parent_summary_json": str(inputs.parent_summary_json),
            "strategy_json": str(inputs.strategy_json),
        },
        "policy": {
            "s2_balanced_recommended": True,
            "prompt_rewrite_allowed": False,
            "synthetic_row_generation_allowed": False,
            "approval_gates_opened": False,
            "approved_to_run": False,
        },
        "composition": {
            "parent_train_rows": len(parent_train),
            "parent_val_rows": len(parent_val),
            "revised_train_rows": len(revised_train),
            "revised_val_rows": len(revised_val),
            "rows_removed_train": len(parent_train) - len(revised_train),
            "rows_removed_val": len(parent_val) - len(revised_val),
            "rows_removed_total": (len(parent_train) + len(parent_val)) - (len(revised_train) + len(revised_val)),
        },
        "targeted_exposure": {
            "parent_group_counts": parent_group_counts,
            "revised_group_counts": revised_group_counts,
            "parent_group_shares": {
                "legacy_total": round(legacy_parent / parent_total, 6) if parent_total else 0.0,
                "healthy_conversion_total": round(healthy_parent / parent_total, 6) if parent_total else 0.0,
            },
            "revised_group_shares": {
                "legacy_total": round(legacy_revised / revised_total, 6) if revised_total else 0.0,
                "healthy_conversion_total": round(healthy_revised / revised_total, 6) if revised_total else 0.0,
            },
            "target_envelope": TARGET_ENVELOPE,
        },
        "retention_by_family": retention_by_family,
        "removed_rows": {
            "count": len(removed_rows),
            "examples": removed_rows[:40],
        },
        "overlap_audit": contamination_audit.get("combined_overlap", {}),
        "diagnostics_highlights": {
            "diversity_review_summary": diagnostics.get("review_support", {}).get("diversity_review_summary", {}),
            "anti_homogenization_summary": diagnostics.get("review_support", {}).get("anti_homogenization_summary", {}),
            "semantic_commitment_telemetry": diagnostics.get("checks", {}).get("semantic_commitment_telemetry", {}),
            "prompt_ambiguity_hard_blocks": ambiguity_audit.get("hard_block_candidates", {}),
        },
        "outputs": {
            "train_jsonl": str(outputs.train_jsonl),
            "val_jsonl": str(outputs.val_jsonl),
            "summary_json": str(outputs.summary_json),
            "diagnostics_json": str(outputs.diagnostics_json),
            "family_concentration_json": str(outputs.family_concentration_json),
            "effective_exposure_projection_json": str(outputs.effective_exposure_projection_json),
            "prompt_ambiguity_audit_json": str(outputs.prompt_ambiguity_audit_json),
            "contamination_audit_json": str(outputs.contamination_audit_json),
            "collapse_watch_telemetry_json": str(outputs.collapse_watch_telemetry_json),
            "human_review_package_json": str(outputs.human_review_package_json),
            "preflight_validation_json": str(outputs.preflight_validation_json),
        },
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }


def _resolve_inputs(args: argparse.Namespace) -> Inputs:
    return Inputs(
        parent_train_jsonl=Path(args.parent_train_jsonl).resolve(),
        parent_val_jsonl=Path(args.parent_val_jsonl).resolve(),
        parent_summary_json=Path(args.parent_summary_json).resolve(),
        i9_behavioral_review_json=Path(args.i9_behavioral_review_json).resolve(),
        i3_train_jsonl=Path(args.i3_train_jsonl).resolve(),
        i3_val_jsonl=Path(args.i3_val_jsonl).resolve(),
        eval_heldout_jsonl=Path(args.eval_heldout_jsonl).resolve(),
        eval_tool_holdout_jsonl=Path(args.eval_tool_holdout_jsonl).resolve(),
        eval_no_call_jsonl=Path(args.eval_no_call_jsonl).resolve(),
        eval_adversarial_jsonl=Path(args.eval_adversarial_jsonl).resolve(),
        eval_direct_answer_jsonl=Path(args.eval_direct_answer_jsonl).resolve(),
        strategy_json=Path(args.strategy_json).resolve(),
    )


def _resolve_outputs(args: argparse.Namespace) -> Outputs:
    data_root = Path(args.output_data_root).resolve()
    report_root = Path(args.output_report_root).resolve()
    return Outputs(
        train_jsonl=data_root / "dataset_v1_0_stage_b_recovery_i10r_train.jsonl",
        val_jsonl=data_root / "dataset_v1_0_stage_b_recovery_i10r_val.jsonl",
        summary_json=data_root / "dataset_v1_0_stage_b_recovery_i10r_summary.json",
        diagnostics_json=report_root / "stage_b_v1_i10r_dataset_diagnostics.json",
        family_concentration_json=report_root / "stage_b_v1_i10r_family_concentration_review.json",
        family_concentration_md=report_root / "stage_b_v1_i10r_family_concentration_review.md",
        effective_exposure_projection_json=report_root / "stage_b_v1_i10r_effective_exposure_projection.json",
        prompt_ambiguity_audit_json=report_root / "stage_b_v1_i10r_prompt_ambiguity_audit.json",
        contamination_audit_json=report_root / "stage_b_v1_i10r_contamination_audit.json",
        collapse_watch_telemetry_json=report_root / "stage_b_v1_i10r_collapse_watch_telemetry.json",
        human_review_package_json=report_root / "stage_b_v1_i10r_human_review_package.json",
        human_review_package_md=report_root / "stage_b_v1_i10r_human_review_package.md",
        preflight_validation_json=report_root / "stage_b_v1_i10r_preflight_validation.json",
    )


def _fail_fast_unlock(args: argparse.Namespace) -> None:
    if not args.enable_dataset_revision:
        raise RuntimeError("dataset revision requires --enable-dataset-revision")
    if not args.allow_revision_phase:
        raise RuntimeError("dataset revision requires --allow-revision-phase")
    if not args.apply_s2_balanced_recommended:
        raise RuntimeError("dataset revision requires --apply-s2-balanced-recommended")


def _fail_fast_inputs(inputs: Inputs) -> None:
    req = [
        inputs.parent_train_jsonl,
        inputs.parent_val_jsonl,
        inputs.parent_summary_json,
        inputs.i9_behavioral_review_json,
        inputs.i3_train_jsonl,
        inputs.i3_val_jsonl,
        inputs.eval_heldout_jsonl,
        inputs.eval_tool_holdout_jsonl,
        inputs.eval_no_call_jsonl,
        inputs.eval_adversarial_jsonl,
        inputs.eval_direct_answer_jsonl,
        inputs.strategy_json,
    ]
    missing = [str(p) for p in req if not p.exists()]
    if missing:
        raise RuntimeError("missing required input(s):\n- " + "\n- ".join(missing))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build deterministic i10r exposure-correction dataset package.")
    parser.add_argument(
        "--parent-train-jsonl",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i10_train.jsonl",
    )
    parser.add_argument(
        "--parent-val-jsonl",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i10_val.jsonl",
    )
    parser.add_argument(
        "--parent-summary-json",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i10_summary.json",
    )
    parser.add_argument(
        "--i9-behavioral-review-json",
        default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i9_behavioral_review_package.json",
    )
    parser.add_argument(
        "--i3-train-jsonl",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl",
    )
    parser.add_argument(
        "--i3-val-jsonl",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_val.jsonl",
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
    parser.add_argument(
        "--strategy-json",
        default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10_dataset_revision_strategy.json",
    )

    parser.add_argument("--output-data-root", default="/opt/ai-stack/assistant-training/data/v1_0")
    parser.add_argument("--output-report-root", default="/opt/ai-stack/assistant-training/manifests/reports")

    parser.add_argument("--enable-dataset-revision", action="store_true")
    parser.add_argument("--allow-revision-phase", action="store_true")
    parser.add_argument("--apply-s2-balanced-recommended", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    _fail_fast_unlock(args)
    inputs = _resolve_inputs(args)
    outputs = _resolve_outputs(args)
    _fail_fast_inputs(inputs)

    parent_summary = _load_json(inputs.parent_summary_json)
    if str(parent_summary.get("iteration") or "") != PARENT_ITERATION:
        raise RuntimeError(
            f"unexpected parent iteration in summary: {parent_summary.get('iteration')} (expected {PARENT_ITERATION})"
        )
    strategy = _load_json(inputs.strategy_json)
    if str(strategy.get("recommended_scenario") or "") != "S2_balanced_recommended":
        raise RuntimeError("strategy JSON does not declare S2_balanced_recommended")

    parent_train = _load_jsonl(inputs.parent_train_jsonl)
    parent_val = _load_jsonl(inputs.parent_val_jsonl)

    parent_refs = _collect_rows(parent_train, parent_val)
    if not parent_refs:
        raise RuntimeError("parent i10 targeted rows not found")

    family_to_refs: dict[str, list[RowRef]] = defaultdict(list)
    for ref in parent_refs:
        family_to_refs[ref.source_case_id].append(ref)

    keep_by_family: dict[str, int] = {}
    retention_by_family: dict[str, dict[str, int]] = {}
    for family, refs in sorted(family_to_refs.items()):
        group = _group_from_case_id(family)
        keep = _compute_keep_count(group, len(refs))
        if keep <= 0:
            raise RuntimeError(f"invalid keep count for family={family}")
        keep_by_family[family] = keep
        retention_by_family[family] = {
            "group": group,
            "before_rows": len(refs),
            "keep_rows": keep,
            "remove_rows": len(refs) - keep,
            "retain_ratio": round(keep / len(refs), 6),
        }

    # Validate required S2 group counts exactly.
    before_group_counts = _summarize_group_counts(parent_refs)
    expected_after_group_counts = Counter()
    for family, refs in family_to_refs.items():
        expected_after_group_counts[_group_from_case_id(family)] += keep_by_family[family]
    after_group_counts = dict(sorted(expected_after_group_counts.items(), key=lambda kv: kv[0]))

    expected_s2_group_counts = {
        GROUP_I3_ADAPT: 367,
        GROUP_RISKY_LEGACY: 30,
        GROUP_I9_CONV: 102,
        GROUP_I10_CONV: 102,
    }
    if after_group_counts != expected_s2_group_counts:
        raise RuntimeError(
            f"S2 group-count mismatch: expected={expected_s2_group_counts} actual={after_group_counts}"
        )

    selected_keys: set[tuple[str, int]] = set()
    for family, refs in sorted(family_to_refs.items()):
        selected_refs = _select_family_rows(family, refs, keep_by_family[family])
        for ref in selected_refs:
            key = (ref.split, ref.index_0)
            if key in selected_keys:
                raise RuntimeError(f"duplicate selected row key: {key}")
            selected_keys.add(key)

    revised_train: list[dict[str, Any]] = []
    revised_val: list[dict[str, Any]] = []
    removed_rows: list[dict[str, Any]] = []

    for split, parent_rows, out_rows in (
        ("train", parent_train, revised_train),
        ("val", parent_val, revised_val),
    ):
        for idx_0, row in enumerate(parent_rows):
            tool = _tool_name(row)
            if tool not in TARGETED_TOOLS:
                out_rows.append(row)
                continue
            key = (split, idx_0)
            if key in selected_keys:
                out_rows.append(row)
            else:
                removed_rows.append(
                    {
                        "split": split,
                        "row_index_1based": idx_0 + 1,
                        "source_case_id": _source_case_id(row, f"{split}:{idx_0 + 1}"),
                        "tool": tool,
                    }
                )

    revised_refs = _collect_rows(revised_train, revised_val)
    revised_group_counts = _summarize_group_counts(revised_refs)
    if revised_group_counts != expected_s2_group_counts:
        raise RuntimeError(
            f"revised group counts drifted from deterministic selection: "
            f"expected={expected_s2_group_counts} actual={revised_group_counts}"
        )

    # Non-targeted/no-call surface must remain unchanged.
    if _non_tool_hash_multiset(parent_train) != _non_tool_hash_multiset(revised_train):
        raise RuntimeError("non-tool train rows changed during exposure correction")
    if _non_tool_hash_multiset(parent_val) != _non_tool_hash_multiset(revised_val):
        raise RuntimeError("non-tool val rows changed during exposure correction")

    # Diagnostics and audits.
    i9_behavior = _load_json(inputs.i9_behavioral_review_json)
    diagnostics = build_full_diagnostics_report(
        revised_train + revised_val,
        reference_rows=parent_train + parent_val,
        policy=scaffold_policy_defaults(),
        i9_behavioral_report=i9_behavior,
    )
    diagnostics["iteration"] = RUN_NAME
    diagnostics["revision_context"] = {
        "parent_iteration": PARENT_ITERATION,
        "strategy": "S2_balanced_recommended",
        "targeted_group_counts_before": before_group_counts,
        "targeted_group_counts_after": revised_group_counts,
    }

    forbidden_hits = int(diagnostics.get("checks", {}).get("forbidden_pattern_scan", {}).get("total_hits", 0) or 0)
    if forbidden_hits > 0:
        raise RuntimeError(f"forbidden-pattern doctrine violation: total_hits={forbidden_hits}")
    if not bool(diagnostics.get("review_support", {}).get("diversity_review_summary", {}).get("pass", False)):
        raise RuntimeError("diversity doctrine check failed")
    if not bool(diagnostics.get("review_support", {}).get("anti_homogenization_summary", {}).get("pass", False)):
        raise RuntimeError("anti-homogenization doctrine check failed")

    ambiguity_audit = _build_ambiguity_audit(revised_train + revised_val)
    _fail_fast_ambiguity_hard_blocks(ambiguity_audit)

    eval_map = {
        "heldout_validation": _load_jsonl(inputs.eval_heldout_jsonl),
        "tool_holdout": _load_jsonl(inputs.eval_tool_holdout_jsonl),
        "no_call": _load_jsonl(inputs.eval_no_call_jsonl),
        "adversarial": _load_jsonl(inputs.eval_adversarial_jsonl),
        "direct_answer": _load_jsonl(inputs.eval_direct_answer_jsonl),
    }
    contamination_audit = _build_contamination_audit(revised_train, revised_val, eval_map)
    _fail_fast_contamination(contamination_audit)

    # Family concentration telemetry.
    family_args = SimpleNamespace(
        i10_train_jsonl=str(outputs.train_jsonl),
        i10_val_jsonl=str(outputs.val_jsonl),
        i3_train_jsonl=str(inputs.i3_train_jsonl),
        i3_val_jsonl=str(inputs.i3_val_jsonl),
        min_rows_material=5,
        concentration_share_warn=0.10,
        low_effective_diversity_ratio_warn=0.30,
        low_prompt_entropy_bits_warn=2.0,
        low_semantic_variation_warn=0.35,
        high_nn_similarity_warn=0.65,
        top_n=10,
    )

    # Write revised dataset before running family review helper that loads from disk.
    _write_jsonl(outputs.train_jsonl, revised_train)
    _write_jsonl(outputs.val_jsonl, revised_val)

    family_report = build_family_concentration_review(family_args)
    family_report["iteration"] = RUN_NAME

    exposure_projection = _build_effective_exposure_projection(
        parent_train + parent_val,
        revised_train + revised_val,
        baseline_targeted_refs=parent_refs,
        revised_targeted_refs=revised_refs,
    )

    commit_telemetry = diagnostics.get("checks", {}).get("semantic_commitment_telemetry", {})
    collapse_watch_telemetry = {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "iteration": RUN_NAME,
        "status": "completed",
        "top1_behavioral_category_share": commit_telemetry.get("commitment_generalization_vs_recitation", {}).get(
            "top1_behavioral_category_share"
        ),
        "top1_behavioral_category": commit_telemetry.get("commitment_generalization_vs_recitation", {}).get(
            "top1_behavioral_category"
        ),
        "anchor_dominance_ratio": commit_telemetry.get("anchor_dominance_ratio", {}).get("ratio"),
        "scalar_substitution_rebound_proxy": commit_telemetry.get("scalar_substitution_rebound_proxy", {}),
        "paraphrastic_success_diversity": commit_telemetry.get("paraphrastic_success_diversity", {}),
        "abort_or_halt_recommendation_if": commit_telemetry.get("collapse_watch_conditions", {}).get(
            "abort_or_halt_recommendation_if", []
        ),
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }

    largest = family_report.get("ranked_summaries", {}).get("top_largest_families", [])
    top_family_share = float(largest[0].get("percent_of_targeted_dataset", 0.0) / 100.0) if largest else 0.0
    env = exposure_projection.get("envelope_assessment", {})
    hard = ambiguity_audit.get("hard_block_candidates", {})
    human_review = {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "iteration": RUN_NAME,
        "status": "completed",
        "question": "Did deterministic exposure correction reduce legacy ritualization pressure without procedural drift?",
        "exposure_envelope": {
            "legacy_total_share": env.get("legacy_total_share"),
            "healthy_conversion_total_share": env.get("healthy_conversion_total_share"),
            "legacy_within_target": env.get("legacy_within_target"),
            "healthy_conversion_within_target": env.get("healthy_conversion_within_target"),
            "pass": bool(env.get("legacy_within_target", False) and env.get("healthy_conversion_within_target", False)),
        },
        "diversity": {
            "prompt_uniqueness_ratio_delta": exposure_projection.get("delta_after_minus_before", {}).get(
                "prompt_uniqueness_ratio"
            ),
            "skeleton_uniqueness_ratio_delta": exposure_projection.get("delta_after_minus_before", {}).get(
                "skeleton_uniqueness_ratio"
            ),
            "unique_tool_args_ratio_delta": exposure_projection.get("delta_after_minus_before", {}).get(
                "unique_tool_args_ratio"
            ),
            "top_family_share_after": round(top_family_share, 6),
        },
        "hygiene": {
            "ambiguity_hard_blocks_clean": not any(bool(hard.get(k, False)) for k in hard.keys()),
            "contamination_heldout_clean": contamination_audit.get("combined_overlap", {}).get("heldout_validation")
            == {"prompt_overlap": 0, "target_overlap": 0, "source_case_id_overlap": 0},
            "contamination_tool_holdout_clean": contamination_audit.get("combined_overlap", {}).get("tool_holdout")
            == {"prompt_overlap": 0, "target_overlap": 0, "source_case_id_overlap": 0},
            "forbidden_pattern_hits": forbidden_hits,
        },
        "collapse_watch_preview": {
            "top1_behavioral_category_share": collapse_watch_telemetry.get("top1_behavioral_category_share"),
            "anchor_dominance_ratio": collapse_watch_telemetry.get("anchor_dominance_ratio"),
            "scalar_substitution_rebound_proxy": collapse_watch_telemetry.get("scalar_substitution_rebound_proxy"),
        },
        "interpretation_guidance": [
            "Treat rising lexical diversity without procedural diversity as a failure signal.",
            "Preserve read_file procedural footholds over cosmetic shell improvements.",
            "If scalar substitution rebounds post-training, halt progression.",
            "Do not relax ambiguity or contamination hard blocks.",
        ],
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }

    summary = _build_summary(
        inputs=inputs,
        outputs=outputs,
        parent_train=parent_train,
        parent_val=parent_val,
        revised_train=revised_train,
        revised_val=revised_val,
        retention_by_family=retention_by_family,
        removed_rows=removed_rows,
        contamination_audit=contamination_audit,
        diagnostics=diagnostics,
        ambiguity_audit=ambiguity_audit,
    )

    preflight = _build_preflight_validation(
        parent_train=parent_train,
        parent_val=parent_val,
        revised_train=revised_train,
        revised_val=revised_val,
        summary=summary,
        diagnostics=diagnostics,
        ambiguity_audit=ambiguity_audit,
        contamination_audit=contamination_audit,
        family_report=family_report,
        exposure_projection=exposure_projection,
        human_review=human_review,
    )
    if preflight.get("status") != "preflight_validation_completed":
        raise RuntimeError(f"preflight failed: {preflight.get('summary')}")

    # Persist all outputs.
    _write_json(outputs.summary_json, summary)
    _write_json(outputs.diagnostics_json, diagnostics)
    _write_json(outputs.family_concentration_json, family_report)
    write_family_concentration_markdown(family_report, outputs.family_concentration_md)
    _write_json(outputs.effective_exposure_projection_json, exposure_projection)
    _write_json(outputs.prompt_ambiguity_audit_json, ambiguity_audit)
    _write_json(outputs.contamination_audit_json, contamination_audit)
    _write_json(outputs.collapse_watch_telemetry_json, collapse_watch_telemetry)
    _write_json(outputs.human_review_package_json, human_review)
    _write_human_review_package_md(human_review, outputs.human_review_package_md)
    _write_json(outputs.preflight_validation_json, preflight)

    print(
        json.dumps(
            {
                "status": "ok",
                "iteration": RUN_NAME,
                "targeted_group_counts_after": revised_group_counts,
                "outputs": {
                    "train_jsonl": str(outputs.train_jsonl),
                    "val_jsonl": str(outputs.val_jsonl),
                    "summary_json": str(outputs.summary_json),
                    "diagnostics_json": str(outputs.diagnostics_json),
                    "family_concentration_json": str(outputs.family_concentration_json),
                    "effective_exposure_projection_json": str(outputs.effective_exposure_projection_json),
                    "prompt_ambiguity_audit_json": str(outputs.prompt_ambiguity_audit_json),
                    "contamination_audit_json": str(outputs.contamination_audit_json),
                    "collapse_watch_telemetry_json": str(outputs.collapse_watch_telemetry_json),
                    "human_review_package_json": str(outputs.human_review_package_json),
                    "preflight_validation_json": str(outputs.preflight_validation_json),
                },
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
