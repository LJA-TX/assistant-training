#!/usr/bin/env python3
"""
i8 diagnostics and review-support utilities.

Scope boundary:
- This module performs analysis only.
- It never generates i8 train/val datasets.
- It never opens approval gates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from typing import Any, Iterable

RUN_NAME = "stage_b_llama31_8b_base_v1_i8"

DEFAULT_FORBIDDEN_PATTERNS = (
    "never return",
    "must not output",
    "forbidden wrapper key",
    "always include tool_calls key regardless of request",
)

DEFAULT_TARGETED_TOOLS = ("rg_search", "read_file")


@dataclass(frozen=True)
class DiagnosticPolicy:
    targeted_tools: tuple[str, ...]
    forbidden_patterns: tuple[str, ...]
    max_allowed_skeleton_concentration: float
    min_required_style_buckets: int
    min_required_unique_skeletons: int


def scaffold_policy_defaults() -> DiagnosticPolicy:
    # max_allowed_skeleton_concentration=0.0 is a sentinel: compute-only, no threshold enforcement.
    return DiagnosticPolicy(
        targeted_tools=DEFAULT_TARGETED_TOOLS,
        forbidden_patterns=DEFAULT_FORBIDDEN_PATTERNS,
        max_allowed_skeleton_concentration=0.0,
        min_required_style_buckets=2,
        min_required_unique_skeletons=8,
    )


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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
            if isinstance(obj, dict):
                rows.append(obj)
            else:
                raise RuntimeError(f"invalid row type at {path}:{line_no}: expected object")
    return rows


def _user_prompt(row: dict[str, Any]) -> str:
    msgs = row.get("messages")
    if not isinstance(msgs, list):
        return ""
    for msg in msgs:
        if isinstance(msg, dict) and msg.get("role") == "user":
            return str(msg.get("content") or "")
    return ""


def _assistant_tool_name(row: dict[str, Any]) -> str:
    msgs = row.get("messages")
    if not isinstance(msgs, list):
        return ""
    for msg in msgs:
        if not isinstance(msg, dict) or msg.get("role") != "assistant":
            continue
        tc = msg.get("tool_calls")
        if not isinstance(tc, list) or not tc:
            return ""
        first = tc[0]
        if not isinstance(first, dict):
            return ""
        fn = first.get("function")
        if not isinstance(fn, dict):
            return ""
        return str(fn.get("name") or "").strip()
    return ""


def _assistant_tool_arguments_canon(row: dict[str, Any]) -> str:
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
        return json.dumps(args, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "null"


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


def _source_case_id(row: dict[str, Any], row_idx: int) -> str:
    meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    value = str(meta.get("source_case_id") or meta.get("case_id") or "").strip()
    return value or f"row_{row_idx:06d}"


def _normalize_prompt_skeleton(prompt: str) -> str:
    text = prompt.lower().strip()
    text = re.sub(r"`[^`]*`", "`<code>`", text)
    text = re.sub(r'"[^"]*"', '"<str>"', text)
    text = re.sub(r"'[^']*'", "'<str>'", text)
    text = re.sub(r"\b\d+\b", "<num>", text)
    text = re.sub(r"(?:/[a-z0-9._\-]+)+", "<path>", text)
    text = re.sub(r"[a-z]:\\(?:[^\\\s]+\\)*[^\\\s]*", "<path>", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _skeleton_id(prompt: str) -> str:
    norm = _normalize_prompt_skeleton(prompt)
    return hashlib.sha1(norm.encode("utf-8")).hexdigest()[:12]


def _style_bucket(prompt: str) -> str:
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
    )

    if p.endswith("?"):
        return "question_form"
    if any(p.startswith(h) for h in imperative_heads):
        if "line" in p or "lines" in p:
            return "imperative_line_scoped"
        return "imperative_general"
    if "return only" in p or "exactly one" in p or "valid json" in p:
        return "constrained_output"
    if "compare" in p or "difference" in p or "versus" in p:
        return "comparative"
    if "debug" in p or "diagnostic" in p or "health" in p:
        return "diagnostic_request"
    return "task_narrative"


def _list_percentile(values: list[int], pct: float) -> float:
    if not values:
        return 0.0
    if pct <= 0:
        return float(min(values))
    if pct >= 100:
        return float(max(values))
    ordered = sorted(values)
    idx = int(round((pct / 100.0) * (len(ordered) - 1)))
    return float(ordered[idx])


def _numeric_summary(values: list[int]) -> dict[str, float]:
    if not values:
        return {"count": 0.0, "mean": 0.0, "median": 0.0, "p95": 0.0, "max": 0.0}
    return {
        "count": float(len(values)),
        "mean": float(sum(values) / len(values)),
        "median": float(median(values)),
        "p95": _list_percentile(values, 95.0),
        "max": float(max(values)),
    }


def build_intervention_annotations(
    rows: list[dict[str, Any]],
    *,
    targeted_tools: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    targeted = set(targeted_tools or DEFAULT_TARGETED_TOOLS)
    out: list[dict[str, Any]] = []

    for idx, row in enumerate(rows, start=1):
        prompt = _user_prompt(row)
        tool = _assistant_tool_name(row)
        style = _style_bucket(prompt)
        sid = _skeleton_id(prompt)
        case_id = _source_case_id(row, idx)

        tags: list[str] = []
        if tool:
            tags.append("tool_positive")
        else:
            tags.append("non_tool")

        if tool in targeted:
            tags.append("targeted_tool_family")
            if "tool_calls" in prompt.lower():
                tags.append("parse_anchor_present")
            else:
                tags.append("parse_anchor_candidate")
        else:
            tags.append("non_targeted_family")

        if style.startswith("imperative"):
            tags.append("imperative_surface")

        out.append(
            {
                "source_case_id": case_id,
                "tool": tool,
                "target_canon": _assistant_target_canon(row),
                "arguments_canon": _assistant_tool_arguments_canon(row),
                "style_bucket": style,
                "skeleton_id": sid,
                "prompt": prompt,
                "prompt_chars": len(prompt),
                "prompt_words": len([w for w in prompt.strip().split() if w]),
                "intervention_tags": sorted(tags),
                "is_targeted_family": tool in targeted,
            }
        )

    out.sort(key=lambda x: (x["tool"], x["source_case_id"]))
    return out


def run_prompt_ambiguity_audit(
    annotations: list[dict[str, Any]],
    *,
    high_frequency_prompt_threshold: int = 20,
    high_frequency_skeleton_threshold: int = 50,
    top_k: int = 20,
) -> dict[str, Any]:
    by_prompt: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for ann in annotations:
        by_prompt[ann["prompt"]].append(ann)

    duplicate_prompt_groups_identical_target = 0
    duplicate_prompt_groups_different_target = 0
    duplicate_prompt_groups_different_tool = 0
    rows_in_conflicting_prompt_groups = 0

    conflicting_prompt_groups: list[dict[str, Any]] = []

    for prompt, grp in by_prompt.items():
        if len(grp) <= 1:
            continue
        targets = sorted({str(x.get("target_canon") or "") for x in grp})
        tools = sorted({str(x.get("tool") or "") for x in grp})
        if len(targets) == 1:
            duplicate_prompt_groups_identical_target += 1
        else:
            duplicate_prompt_groups_different_target += 1
            rows_in_conflicting_prompt_groups += len(grp)
        if len(tools) > 1:
            duplicate_prompt_groups_different_tool += 1

        if len(targets) > 1 or len(tools) > 1:
            conflicting_prompt_groups.append(
                {
                    "prompt": prompt,
                    "rows": len(grp),
                    "distinct_targets": len(targets),
                    "distinct_tools": len(tools),
                    "tools": tools,
                    "source_case_ids_sample": sorted({x["source_case_id"] for x in grp})[:12],
                }
            )

    by_prompt_tool: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for ann in annotations:
        by_prompt_tool[(ann["prompt"], ann["tool"])].append(ann)

    duplicate_prompt_tool_groups_different_arguments = 0
    conflicting_prompt_tool_groups: list[dict[str, Any]] = []
    for (prompt, tool), grp in by_prompt_tool.items():
        if len(grp) <= 1:
            continue
        args_set = sorted({str(x.get("arguments_canon") or "null") for x in grp})
        if len(args_set) > 1:
            duplicate_prompt_tool_groups_different_arguments += 1
            conflicting_prompt_tool_groups.append(
                {
                    "prompt": prompt,
                    "tool": tool,
                    "rows": len(grp),
                    "distinct_argument_payloads": len(args_set),
                    "arguments_sample": args_set[:8],
                    "source_case_ids_sample": sorted({x["source_case_id"] for x in grp})[:12],
                }
            )

    prompt_freq = Counter(a["prompt"] for a in annotations)
    skeleton_freq = Counter(a["skeleton_id"] for a in annotations)

    high_frequency_prompt_groups = [
        {"prompt": p, "rows": c}
        for p, c in sorted(prompt_freq.items(), key=lambda kv: (-kv[1], kv[0]))
        if c >= high_frequency_prompt_threshold
    ][:top_k]

    high_frequency_skeleton_groups = [
        {"skeleton_id": s, "rows": c}
        for s, c in sorted(skeleton_freq.items(), key=lambda kv: (-kv[1], kv[0]))
        if c >= high_frequency_skeleton_threshold
    ][:top_k]

    by_case: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for ann in annotations:
        by_case[ann["source_case_id"]].append(ann)

    source_case_divergence_groups = []
    for case_id, grp in by_case.items():
        if len(grp) <= 1:
            continue
        target_count = len({x["target_canon"] for x in grp})
        tool_count = len({x["tool"] for x in grp})
        prompt_count = len({x["prompt"] for x in grp})
        arg_count = len({(x["tool"], x["arguments_canon"]) for x in grp})
        if target_count > 1 or tool_count > 1 or arg_count > 1:
            source_case_divergence_groups.append(
                {
                    "source_case_id": case_id,
                    "rows": len(grp),
                    "distinct_targets": target_count,
                    "distinct_tools": tool_count,
                    "distinct_prompts": prompt_count,
                    "distinct_tool_argument_pairs": arg_count,
                }
            )

    source_case_divergence_groups = sorted(
        source_case_divergence_groups,
        key=lambda x: (-x["rows"], -x["distinct_targets"], x["source_case_id"]),
    )[:top_k]

    return {
        "status": "ok",
        "rows_analyzed": len(annotations),
        "duplicate_prompt_groups_identical_target_count": duplicate_prompt_groups_identical_target,
        "duplicate_prompt_groups_different_target_count": duplicate_prompt_groups_different_target,
        "duplicate_prompt_groups_different_tool_count": duplicate_prompt_groups_different_tool,
        "duplicate_prompt_tool_groups_different_arguments_count": duplicate_prompt_tool_groups_different_arguments,
        "rows_in_conflicting_prompt_groups": rows_in_conflicting_prompt_groups,
        "conflicting_prompt_groups": sorted(
            conflicting_prompt_groups,
            key=lambda x: (-x["rows"], -x["distinct_targets"], x["prompt"]),
        )[:top_k],
        "conflicting_prompt_tool_groups": sorted(
            conflicting_prompt_tool_groups,
            key=lambda x: (-x["rows"], -x["distinct_argument_payloads"], x["tool"], x["prompt"]),
        )[:top_k],
        "high_frequency_prompt_reuse": high_frequency_prompt_groups,
        "high_frequency_skeleton_reuse": high_frequency_skeleton_groups,
        "source_case_divergence_groups": source_case_divergence_groups,
        "hard_block_candidates": {
            "prompt_to_multiple_targets": duplicate_prompt_groups_different_target > 0,
            "prompt_to_multiple_tools": duplicate_prompt_groups_different_tool > 0,
            "prompt_tool_to_multiple_arguments": duplicate_prompt_tool_groups_different_arguments > 0,
        },
    }


def run_style_bucket_analysis(
    rows: list[dict[str, Any]],
    *,
    targeted_tools: Iterable[str] | None = None,
) -> dict[str, Any]:
    annotations = build_intervention_annotations(rows, targeted_tools=targeted_tools)

    total = len(annotations)
    overall_counts = Counter(a["style_bucket"] for a in annotations)
    by_tool_counts: dict[str, Counter[str]] = defaultdict(Counter)
    targeted_counts = Counter()
    targeted_total = 0

    for ann in annotations:
        tool = ann["tool"]
        style = ann["style_bucket"]
        by_tool_counts[tool][style] += 1
        if ann["is_targeted_family"]:
            targeted_counts[style] += 1
            targeted_total += 1

    overall = [
        {
            "bucket_name": k,
            "row_count": v,
            "share": round(v / total, 6) if total else 0.0,
        }
        for k, v in sorted(overall_counts.items(), key=lambda kv: (-kv[1], kv[0]))
    ]

    by_tool: list[dict[str, Any]] = []
    for tool in sorted(by_tool_counts.keys()):
        t_total = sum(by_tool_counts[tool].values())
        for bucket, count in sorted(by_tool_counts[tool].items(), key=lambda kv: (-kv[1], kv[0])):
            by_tool.append(
                {
                    "tool_family": tool,
                    "bucket_name": bucket,
                    "row_count": count,
                    "share": round(count / t_total, 6) if t_total else 0.0,
                }
            )

    targeted_only = [
        {
            "bucket_name": k,
            "row_count": v,
            "share": round(v / targeted_total, 6) if targeted_total else 0.0,
        }
        for k, v in sorted(targeted_counts.items(), key=lambda kv: (-kv[1], kv[0]))
    ]

    return {
        "status": "ok",
        "rows_analyzed": total,
        "overall": overall,
        "by_tool": by_tool,
        "targeted_only": targeted_only,
    }


def _skeleton_group_report(
    annotations: list[dict[str, Any]],
    *,
    label: str,
    threshold: float,
    top_k: int,
) -> dict[str, Any]:
    total = len(annotations)
    counts = Counter(a["skeleton_id"] for a in annotations)
    top = []
    for skel, count in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:top_k]:
        share = round(count / total, 6) if total else 0.0
        top.append(
            {
                "skeleton_id": skel,
                "row_count": count,
                "share": share,
                "dominance_flag": bool(threshold > 0.0 and share > threshold),
            }
        )

    shares = [c / total for c in sorted(counts.values(), reverse=True)] if total else []
    top1 = shares[0] if shares else 0.0
    top3 = sum(shares[:3]) if shares else 0.0

    return {
        "group": label,
        "rows": total,
        "unique_skeletons": len(counts),
        "top1_share": round(top1, 6),
        "top3_share": round(top3, 6),
        "top_skeletons": top,
    }


def run_prompt_skeleton_concentration(
    rows: list[dict[str, Any]],
    *,
    targeted_tools: Iterable[str] | None = None,
    max_allowed_concentration: float = 0.0,
    top_k: int = 12,
) -> dict[str, Any]:
    targeted = set(targeted_tools or DEFAULT_TARGETED_TOOLS)
    annotations = build_intervention_annotations(rows, targeted_tools=targeted)

    global_group = _skeleton_group_report(
        annotations,
        label="global",
        threshold=max_allowed_concentration,
        top_k=top_k,
    )

    targeted_group = _skeleton_group_report(
        [a for a in annotations if a["tool"] in targeted],
        label="targeted_tools",
        threshold=max_allowed_concentration,
        top_k=top_k,
    )

    per_tool: list[dict[str, Any]] = []
    tool_buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for ann in annotations:
        tool_buckets[ann["tool"]].append(ann)
    for tool in sorted(tool_buckets.keys()):
        per_tool.append(
            _skeleton_group_report(
                tool_buckets[tool],
                label=tool,
                threshold=max_allowed_concentration,
                top_k=top_k,
            )
        )

    return {
        "status": "ok",
        "max_allowed_concentration": max_allowed_concentration,
        "global": global_group,
        "targeted": targeted_group,
        "per_tool": per_tool,
    }


def run_targeted_tool_distribution_check(
    rows: list[dict[str, Any]],
    *,
    targeted_tools: Iterable[str] | None = None,
    expected_share_map: dict[str, float] | None = None,
) -> dict[str, Any]:
    targeted = tuple(targeted_tools or DEFAULT_TARGETED_TOOLS)
    annotations = build_intervention_annotations(rows, targeted_tools=targeted)

    tool_counts = Counter(a["tool"] for a in annotations if a["tool"])
    total_tool_rows = sum(tool_counts.values())

    if expected_share_map is None:
        eq_share = 1.0 / len(targeted) if targeted else 0.0
        expected_share_map = {t: eq_share for t in targeted}

    by_tool: list[dict[str, Any]] = []
    for tool, count in sorted(tool_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        share = count / total_tool_rows if total_tool_rows else 0.0
        expected = expected_share_map.get(tool)
        deviation = None if expected is None else round(share - expected, 6)
        by_tool.append(
            {
                "tool": tool,
                "row_count": count,
                "share": round(share, 6),
                "expected_share": None if expected is None else round(expected, 6),
                "deviation": deviation,
                "is_targeted": tool in targeted,
            }
        )

    targeted_rows = sum(tool_counts[t] for t in targeted)
    non_targeted_rows = total_tool_rows - targeted_rows

    return {
        "status": "ok",
        "total_tool_rows": total_tool_rows,
        "targeted_rows": targeted_rows,
        "non_targeted_rows": non_targeted_rows,
        "targeted_share": round(targeted_rows / total_tool_rows, 6) if total_tool_rows else 0.0,
        "by_tool": by_tool,
    }


def run_forbidden_pattern_scan(
    rows: list[dict[str, Any]],
    *,
    patterns: Iterable[str] | None = None,
) -> dict[str, Any]:
    pats = [p.strip() for p in (patterns or DEFAULT_FORBIDDEN_PATTERNS) if p.strip()]
    anns = build_intervention_annotations(rows)

    output: list[dict[str, Any]] = []
    total_hits = 0
    for idx, pattern in enumerate(pats, start=1):
        lower = pattern.lower()
        case_hits = [a for a in anns if lower in a["prompt"].lower()]
        hit_count = len(case_hits)
        total_hits += hit_count
        output.append(
            {
                "pattern_id": f"fp_{idx:03d}",
                "pattern": pattern,
                "hit_count": hit_count,
                "sample_source_case_ids": sorted(a["source_case_id"] for a in case_hits)[:8],
            }
        )

    return {
        "status": "ok",
        "patterns_checked": len(pats),
        "total_hits": total_hits,
        "results": output,
    }


def run_intervention_coverage_accounting(
    annotations: list[dict[str, Any]],
    *,
    targeted_tools: Iterable[str] | None = None,
) -> dict[str, Any]:
    targeted = set(targeted_tools or DEFAULT_TARGETED_TOOLS)
    tag_counts = Counter()
    tool_counts = Counter(a["tool"] for a in annotations if a["tool"])

    targeted_annotation_rows = 0
    for ann in annotations:
        for tag in ann["intervention_tags"]:
            tag_counts[tag] += 1
        if ann["tool"] in targeted:
            targeted_annotation_rows += 1

    return {
        "status": "ok",
        "rows": len(annotations),
        "targeted_rows": targeted_annotation_rows,
        "targeted_share": round(targeted_annotation_rows / len(annotations), 6) if annotations else 0.0,
        "tag_counts": dict(sorted(tag_counts.items(), key=lambda kv: kv[0])),
        "tool_counts": dict(sorted(tool_counts.items(), key=lambda kv: kv[0])),
    }


def run_prompt_length_delta_analysis(
    reference_annotations: list[dict[str, Any]],
    candidate_annotations: list[dict[str, Any]],
    *,
    targeted_tools: Iterable[str] | None = None,
) -> dict[str, Any]:
    targeted = set(targeted_tools or DEFAULT_TARGETED_TOOLS)

    def pick(anns: list[dict[str, Any]], only_targeted: bool) -> list[dict[str, Any]]:
        if not only_targeted:
            return anns
        return [a for a in anns if a["tool"] in targeted]

    def summarize(anns: list[dict[str, Any]]) -> dict[str, Any]:
        char_values = [int(a["prompt_chars"]) for a in anns]
        word_values = [int(a["prompt_words"]) for a in anns]
        return {
            "chars": _numeric_summary(char_values),
            "words": _numeric_summary(word_values),
        }

    ref_all = summarize(pick(reference_annotations, False))
    cand_all = summarize(pick(candidate_annotations, False))
    ref_targeted = summarize(pick(reference_annotations, True))
    cand_targeted = summarize(pick(candidate_annotations, True))

    def delta_block(ref: dict[str, Any], cand: dict[str, Any]) -> dict[str, Any]:
        return {
            "chars_mean_delta": round(cand["chars"]["mean"] - ref["chars"]["mean"], 6),
            "chars_p95_delta": round(cand["chars"]["p95"] - ref["chars"]["p95"], 6),
            "words_mean_delta": round(cand["words"]["mean"] - ref["words"]["mean"], 6),
            "words_p95_delta": round(cand["words"]["p95"] - ref["words"]["p95"], 6),
        }

    return {
        "status": "ok",
        "reference_all": ref_all,
        "candidate_all": cand_all,
        "delta_all": delta_block(ref_all, cand_all),
        "reference_targeted": ref_targeted,
        "candidate_targeted": cand_targeted,
        "delta_targeted": delta_block(ref_targeted, cand_targeted),
    }


def extract_targeted_prompt_samples(
    annotations: list[dict[str, Any]],
    *,
    targeted_tools: Iterable[str] | None = None,
    per_tool: int = 3,
    per_bucket: int = 2,
) -> dict[str, Any]:
    targeted = set(targeted_tools or DEFAULT_TARGETED_TOOLS)
    targeted_anns = [a for a in annotations if a["tool"] in targeted]

    by_tool: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_bucket: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for ann in sorted(targeted_anns, key=lambda x: (x["tool"], x["style_bucket"], x["source_case_id"])):
        by_tool[ann["tool"]].append(ann)
        by_bucket[ann["style_bucket"]].append(ann)

    samples_by_tool = {
        tool: [
            {
                "source_case_id": a["source_case_id"],
                "style_bucket": a["style_bucket"],
                "prompt_chars": a["prompt_chars"],
                "prompt": a["prompt"],
            }
            for a in anns[:per_tool]
        ]
        for tool, anns in sorted(by_tool.items(), key=lambda kv: kv[0])
    }

    samples_by_bucket = {
        bucket: [
            {
                "source_case_id": a["source_case_id"],
                "tool": a["tool"],
                "prompt_chars": a["prompt_chars"],
                "prompt": a["prompt"],
            }
            for a in anns[:per_bucket]
        ]
        for bucket, anns in sorted(by_bucket.items(), key=lambda kv: kv[0])
    }

    return {
        "status": "ok",
        "targeted_rows": len(targeted_anns),
        "samples_by_tool": samples_by_tool,
        "samples_by_style_bucket": samples_by_bucket,
    }


def build_diversity_review_summary(
    style_report: dict[str, Any],
    skeleton_report: dict[str, Any],
    policy: DiagnosticPolicy,
) -> dict[str, Any]:
    targeted_styles = style_report.get("targeted_only", [])
    targeted_group = skeleton_report.get("targeted", {})

    dominant_style_share = float(targeted_styles[0]["share"]) if targeted_styles else 0.0
    style_bucket_count = len(targeted_styles)
    top1_skeleton_share = float(targeted_group.get("top1_share", 0.0) or 0.0)
    unique_skeletons = int(targeted_group.get("unique_skeletons", 0) or 0)

    risks = []
    if style_bucket_count < policy.min_required_style_buckets:
        risks.append("insufficient_style_bucket_diversity")
    if unique_skeletons < policy.min_required_unique_skeletons:
        risks.append("insufficient_unique_skeletons")
    if dominant_style_share > 0.75:
        risks.append("dominant_style_bucket_risk")
    if top1_skeleton_share > 0.35:
        risks.append("top_skeleton_concentration_risk")

    if policy.max_allowed_skeleton_concentration > 0.0 and top1_skeleton_share > policy.max_allowed_skeleton_concentration:
        risks.append("policy_max_skeleton_concentration_exceeded")

    return {
        "status": "ok",
        "style_bucket_count_targeted": style_bucket_count,
        "dominant_style_share_targeted": round(dominant_style_share, 6),
        "unique_skeletons_targeted": unique_skeletons,
        "top1_skeleton_share_targeted": round(top1_skeleton_share, 6),
        "risk_flags": risks,
        "pass": not risks,
    }


def build_anti_homogenization_summary(
    forbidden_report: dict[str, Any],
    skeleton_report: dict[str, Any],
    style_report: dict[str, Any],
) -> dict[str, Any]:
    targeted_group = skeleton_report.get("targeted", {})
    dominant_style_share = 0.0
    targeted_styles = style_report.get("targeted_only", [])
    if targeted_styles:
        dominant_style_share = float(targeted_styles[0].get("share", 0.0) or 0.0)

    risk_signals: list[str] = []
    if int(forbidden_report.get("total_hits", 0) or 0) > 0:
        risk_signals.append("forbidden_lexical_pressure_detected")
    if float(targeted_group.get("top1_share", 0.0) or 0.0) > 0.35:
        risk_signals.append("high_top1_skeleton_share")
    if dominant_style_share > 0.75:
        risk_signals.append("style_bucket_dominance")

    return {
        "status": "ok",
        "forbidden_hits_total": int(forbidden_report.get("total_hits", 0) or 0),
        "targeted_top1_skeleton_share": round(float(targeted_group.get("top1_share", 0.0) or 0.0), 6),
        "targeted_top3_skeleton_share": round(float(targeted_group.get("top3_share", 0.0) or 0.0), 6),
        "dominant_style_share": round(dominant_style_share, 6),
        "risk_signals": risk_signals,
        "pass": not risk_signals,
    }


def build_empty_diagnostics_report(policy: DiagnosticPolicy) -> dict[str, Any]:
    return {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "iteration": RUN_NAME,
        "status": "scaffold_not_executed",
        "policy": {
            "targeted_tools": list(policy.targeted_tools),
            "forbidden_patterns": list(policy.forbidden_patterns),
            "max_allowed_skeleton_concentration": policy.max_allowed_skeleton_concentration,
            "min_required_style_buckets": policy.min_required_style_buckets,
            "min_required_unique_skeletons": policy.min_required_unique_skeletons,
        },
        "checks": {
            "style_bucket_analysis": {"status": "todo"},
            "prompt_skeleton_concentration": {"status": "todo"},
            "targeted_tool_distribution": {"status": "todo"},
            "forbidden_pattern_scan": {"status": "todo"},
            "intervention_coverage": {"status": "todo"},
            "prompt_length_delta": {"status": "todo"},
            "prompt_ambiguity_audit": {"status": "todo"},
        },
        "gate_state": {
            "approved_to_generate_dataset": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }


def build_full_diagnostics_report(
    rows: list[dict[str, Any]],
    *,
    reference_rows: list[dict[str, Any]] | None = None,
    policy: DiagnosticPolicy | None = None,
) -> dict[str, Any]:
    pol = policy or scaffold_policy_defaults()
    ref_rows = reference_rows if reference_rows is not None else rows

    candidate_annotations = build_intervention_annotations(rows, targeted_tools=pol.targeted_tools)
    reference_annotations = build_intervention_annotations(ref_rows, targeted_tools=pol.targeted_tools)

    style_report = run_style_bucket_analysis(rows, targeted_tools=pol.targeted_tools)
    skeleton_report = run_prompt_skeleton_concentration(
        rows,
        targeted_tools=pol.targeted_tools,
        max_allowed_concentration=pol.max_allowed_skeleton_concentration,
    )
    distribution_report = run_targeted_tool_distribution_check(rows, targeted_tools=pol.targeted_tools)
    forbidden_report = run_forbidden_pattern_scan(rows, patterns=pol.forbidden_patterns)
    coverage_report = run_intervention_coverage_accounting(candidate_annotations, targeted_tools=pol.targeted_tools)
    length_delta_report = run_prompt_length_delta_analysis(
        reference_annotations,
        candidate_annotations,
        targeted_tools=pol.targeted_tools,
    )
    ambiguity_audit = run_prompt_ambiguity_audit(candidate_annotations)

    diversity_summary = build_diversity_review_summary(style_report, skeleton_report, pol)
    anti_homogenization_summary = build_anti_homogenization_summary(
        forbidden_report,
        skeleton_report,
        style_report,
    )
    targeted_samples = extract_targeted_prompt_samples(candidate_annotations, targeted_tools=pol.targeted_tools)

    review_checklist = [
        "Confirm targeted tools are limited to rg_search/read_file for localized shaping.",
        "Confirm no single prompt skeleton dominates targeted rows.",
        "Confirm no forbidden lexical/schema pressure patterns are present.",
        "Confirm no identical prompts map to conflicting targets/tools/arguments.",
        "Confirm targeted prompt styles remain semantically diverse.",
        "Confirm prompt-length inflation is bounded and not forcing template collapse.",
    ]

    return {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "iteration": RUN_NAME,
        "status": "analysis_completed",
        "policy": {
            "targeted_tools": list(pol.targeted_tools),
            "forbidden_patterns": list(pol.forbidden_patterns),
            "max_allowed_skeleton_concentration": pol.max_allowed_skeleton_concentration,
            "min_required_style_buckets": pol.min_required_style_buckets,
            "min_required_unique_skeletons": pol.min_required_unique_skeletons,
        },
        "checks": {
            "style_bucket_analysis": style_report,
            "prompt_skeleton_concentration": skeleton_report,
            "targeted_tool_distribution": distribution_report,
            "forbidden_pattern_scan": forbidden_report,
            "intervention_coverage": coverage_report,
            "prompt_length_delta": length_delta_report,
            "prompt_ambiguity_audit": ambiguity_audit,
        },
        "review_support": {
            "review_checklist": review_checklist,
            "intervention_budget_summary": {
                "candidate_rows": len(candidate_annotations),
                "reference_rows": len(reference_annotations),
                "targeted_rows": coverage_report["targeted_rows"],
                "targeted_share": coverage_report["targeted_share"],
                "tool_counts": coverage_report["tool_counts"],
            },
            "targeted_prompt_samples": targeted_samples,
            "diversity_review_summary": diversity_summary,
            "anti_homogenization_summary": anti_homogenization_summary,
            "ambiguity_hotspots": {
                "conflicting_prompt_groups": ambiguity_audit["conflicting_prompt_groups"],
                "conflicting_prompt_tool_groups": ambiguity_audit["conflicting_prompt_tool_groups"],
                "high_frequency_prompt_reuse": ambiguity_audit["high_frequency_prompt_reuse"],
                "high_frequency_skeleton_reuse": ambiguity_audit["high_frequency_skeleton_reuse"],
                "source_case_divergence_groups": ambiguity_audit["source_case_divergence_groups"],
            },
        },
        "gate_state": {
            "approved_to_generate_dataset": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run i8 diagnostics on existing JSONL rows (no dataset generation).")
    parser.add_argument("--input-jsonl", required=True)
    parser.add_argument("--reference-jsonl", default="")
    parser.add_argument("--output-json", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = _load_jsonl(Path(args.input_jsonl).resolve())
    reference_rows = None
    if args.reference_jsonl.strip():
        reference_rows = _load_jsonl(Path(args.reference_jsonl).resolve())

    report = build_full_diagnostics_report(rows, reference_rows=reference_rows)

    if args.output_json.strip():
        out = Path(args.output_json).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
