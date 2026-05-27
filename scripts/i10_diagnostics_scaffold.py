#!/usr/bin/env python3
"""
i10 diagnostics and review-support utilities.

Scope boundary:
- Analysis only.
- No dataset generation, no training, no eval execution.
- Approval gates remain closed.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from i8_diagnostics_scaffold import (
    build_anti_homogenization_summary,
    build_diversity_review_summary,
    build_intervention_annotations as _build_intervention_annotations_base,
    extract_targeted_prompt_samples,
    run_forbidden_pattern_scan,
    run_intervention_coverage_accounting,
    run_prompt_ambiguity_audit as _run_prompt_ambiguity_audit_base,
    run_prompt_length_delta_analysis,
    run_prompt_skeleton_concentration,
    run_style_bucket_analysis,
    run_targeted_tool_distribution_check,
)

RUN_NAME = "stage_b_llama31_8b_base_v1_i10"

DEFAULT_TARGETED_TOOLS = ("read_file", "rg_search")
DEFAULT_FORBIDDEN_PATTERNS = (
    "never return",
    "must not output",
    "forbidden wrapper key",
    "always include tool_calls key regardless of request",
    "do not answer directly",
)

COLLAPSE_WATCH_THRESHOLDS = {
    "max_top1_behavioral_category_share": 0.70,
    "max_anchor_dominance_ratio": 0.70,
    "max_scalar_substitution_rebound_delta": 0.05,
}


@dataclass(frozen=True)
class DiagnosticPolicy:
    targeted_tools: tuple[str, ...]
    forbidden_patterns: tuple[str, ...]
    max_allowed_skeleton_concentration: float
    min_required_style_buckets: int
    min_required_unique_skeletons: int


def scaffold_policy_defaults() -> DiagnosticPolicy:
    return DiagnosticPolicy(
        targeted_tools=DEFAULT_TARGETED_TOOLS,
        forbidden_patterns=DEFAULT_FORBIDDEN_PATTERNS,
        max_allowed_skeleton_concentration=0.0,
        min_required_style_buckets=2,
        min_required_unique_skeletons=10,
    )


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
                raise RuntimeError(f"invalid row type at {path}:{line_no}; expected object")
            rows.append(obj)
    return rows


def build_intervention_annotations(
    rows: list[dict[str, Any]],
    *,
    targeted_tools: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    return _build_intervention_annotations_base(rows, targeted_tools=targeted_tools)


def run_prompt_ambiguity_audit(
    annotations: list[dict[str, Any]],
    *,
    high_frequency_prompt_threshold: int = 20,
    high_frequency_skeleton_threshold: int = 50,
    top_k: int = 20,
) -> dict[str, Any]:
    return _run_prompt_ambiguity_audit_base(
        annotations,
        high_frequency_prompt_threshold=high_frequency_prompt_threshold,
        high_frequency_skeleton_threshold=high_frequency_skeleton_threshold,
        top_k=top_k,
    )


def _prompt_anchor_bucket(prompt: str) -> str:
    p = prompt.lower()
    if "tool_calls" in p:
        return "literal_tool_calls"
    if "tool call" in p or "tool-call" in p or "function call" in p:
        return "paraphrastic_tool_call"
    if "json object" in p or "structured payload" in p or "canonical payload" in p:
        return "schema_paraphrase"
    return "no_anchor_phrase"


def _calc_entropy(counter: Counter[str]) -> float:
    total = sum(counter.values())
    if total <= 0:
        return 0.0
    out = 0.0
    for count in counter.values():
        p = count / total
        out -= p * math.log2(p)
    return out


def _intervention_rows(
    rows: list[dict[str, Any]],
    *,
    targeted_tools: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    targeted = set(targeted_tools or DEFAULT_TARGETED_TOOLS)
    out: list[dict[str, Any]] = []
    for row in rows:
        meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        tool = str(meta.get("tool") or "")
        if tool not in targeted:
            continue
        if not bool(meta.get("intervention_i10_row", False)):
            continue
        out.append(row)
    return out


def run_semantic_commitment_telemetry(
    rows: list[dict[str, Any]],
    *,
    targeted_tools: Iterable[str] | None = None,
    i9_behavioral_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    annotations = build_intervention_annotations(rows, targeted_tools=targeted_tools)
    intervention_rows = _intervention_rows(rows, targeted_tools=targeted_tools)

    family_counts = Counter()
    behavior_counts = Counter()
    tool_counts = Counter()
    archetype_counts = Counter()
    anchor_counts = Counter()
    conversion_ids = set()

    scalar_like = 0
    direct_like = 0

    prompts = []
    for row in intervention_rows:
        meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        fam = str(meta.get("intervention_i10_family") or "unknown")
        beh = str(meta.get("intervention_i10_behavior_source") or "unknown")
        arc = str(meta.get("intervention_i10_query_archetype") or "unknown")
        tool = str(meta.get("tool") or "")

        prompt = ""
        msgs = row.get("messages")
        if isinstance(msgs, list):
            for msg in msgs:
                if isinstance(msg, dict) and msg.get("role") == "user":
                    prompt = str(msg.get("content") or "")
                    break

        family_counts[fam] += 1
        behavior_counts[beh] += 1
        archetype_counts[arc] += 1
        tool_counts[tool] += 1
        anchor_counts[_prompt_anchor_bucket(prompt)] += 1
        prompts.append(prompt)

        if "scalar" in beh or "token" in beh:
            scalar_like += 1
        if "direct" in beh or "textual" in beh or "pseudo" in beh:
            direct_like += 1

        cid = str(meta.get("intervention_i10_conversion_id") or "")
        if cid:
            conversion_ids.add(cid)

    total_intervention = len(intervention_rows)
    top_behavior = behavior_counts.most_common(1)[0] if behavior_counts else ("none", 0)
    top1_share = (top_behavior[1] / total_intervention) if total_intervention else 0.0

    literal_anchor = anchor_counts.get("literal_tool_calls", 0)
    anchor_ratio = (literal_anchor / total_intervention) if total_intervention else 0.0

    prompt_counter = Counter(prompts)
    prompt_uniqueness = (len(prompt_counter) / total_intervention) if total_intervention else 0.0
    prompt_entropy = _calc_entropy(prompt_counter)
    top_prompt_shell_share = (prompt_counter.most_common(1)[0][1] / total_intervention) if total_intervention else 0.0

    i9_scalar_share = None
    if i9_behavioral_report:
        failure = i9_behavioral_report.get("commitment_failure_modes", {})
        i9_scalar_share = float(
            (failure.get("category_rates", {}) or {}).get("scalar_or_token_result_substitution", 0.0) or 0.0
        )

    i10_scalar_share_proxy = (scalar_like / total_intervention) if total_intervention else 0.0
    i10_direct_share_proxy = (direct_like / total_intervention) if total_intervention else 0.0

    rebound_delta = None
    rebound_flag = False
    if i9_scalar_share is not None:
        rebound_delta = i10_scalar_share_proxy - i9_scalar_share
        rebound_flag = rebound_delta > COLLAPSE_WATCH_THRESHOLDS["max_scalar_substitution_rebound_delta"]

    read_file_rows = tool_counts.get("read_file", 0)

    return {
        "status": "ok",
        "rows_analyzed": len(rows),
        "intervention_rows": total_intervention,
        "conversion_ids_count": len(conversion_ids),
        "source_family_distribution": dict(sorted(family_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        "source_behavior_distribution": dict(sorted(behavior_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        "query_archetype_distribution": dict(sorted(archetype_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        "source_tool_distribution": dict(sorted(tool_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        "scalar_substitution_rebound_proxy": {
            "i9_scalar_share_baseline": i9_scalar_share,
            "i10_scalar_share_proxy": round(i10_scalar_share_proxy, 6),
            "delta": round(rebound_delta, 6) if rebound_delta is not None else None,
            "threshold_delta": COLLAPSE_WATCH_THRESHOLDS["max_scalar_substitution_rebound_delta"],
            "flag": rebound_flag,
            "note": "Proxy from intervention-source annotations; final rebound evaluated post-canonical-eval.",
        },
        "direct_answer_substitution_proxy": {
            "i10_direct_share_proxy": round(i10_direct_share_proxy, 6),
            "note": "Tracks risk of direct-answer dominance among intervention rows.",
        },
        "anchor_dominance_ratio": {
            "literal_tool_calls_anchor_rows": literal_anchor,
            "intervention_rows": total_intervention,
            "ratio": round(anchor_ratio, 6),
            "threshold": COLLAPSE_WATCH_THRESHOLDS["max_anchor_dominance_ratio"],
            "flag": anchor_ratio > COLLAPSE_WATCH_THRESHOLDS["max_anchor_dominance_ratio"],
            "anchor_bucket_distribution": dict(sorted(anchor_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        },
        "paraphrastic_success_diversity": {
            "anchor_bucket_distribution": dict(sorted(anchor_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
            "prompt_uniqueness_ratio": round(prompt_uniqueness, 6),
            "prompt_entropy_bits": round(prompt_entropy, 6),
            "top_prompt_shell_share": round(top_prompt_shell_share, 6),
            "status": "pre_eval_prompt_diversity_proxy",
        },
        "read_file_exact_valid_emergence": {
            "target_rows_in_intervention": read_file_rows,
            "status": "pending_post_eval",
            "note": "Primary i10 success condition requires read_file exact-valid > 0 with invariant preservation.",
        },
        "commitment_generalization_vs_recitation": {
            "top1_behavioral_category": top_behavior[0],
            "top1_behavioral_category_share": round(top1_share, 6),
            "top1_threshold": COLLAPSE_WATCH_THRESHOLDS["max_top1_behavioral_category_share"],
            "top1_flag": top1_share > COLLAPSE_WATCH_THRESHOLDS["max_top1_behavioral_category_share"],
            "prompt_uniqueness_ratio": round(prompt_uniqueness, 6),
            "top_prompt_shell_share": round(top_prompt_shell_share, 6),
            "interpretation_hint": "High top_prompt_shell_share + low uniqueness may indicate lexical-shell memorization risk.",
        },
        "collapse_watch_conditions": {
            "abort_or_halt_recommendation_if": [
                "payload_not_parsed rises materially while exact_valid stagnates_or_falls",
                "top1_behavioral_category_share > 0.70",
                "scalar_or_direct_answer_substitutions rise materially",
                "no_call_correctness regresses",
                "wrapper_leakage > 0",
                "single-anchor canonical dependence strengthens",
                "paraphrastic canonical success narrows",
            ],
            "status": "pre_eval_monitoring_spec_ready",
        },
    }


def build_full_diagnostics_report(
    rows: list[dict[str, Any]],
    *,
    reference_rows: list[dict[str, Any]] | None = None,
    policy: DiagnosticPolicy | None = None,
    i9_behavioral_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    pol = policy or scaffold_policy_defaults()
    ref_rows = reference_rows if reference_rows is not None else rows

    cand_ann = build_intervention_annotations(rows, targeted_tools=pol.targeted_tools)
    ref_ann = build_intervention_annotations(ref_rows, targeted_tools=pol.targeted_tools)

    style_report = run_style_bucket_analysis(rows, targeted_tools=pol.targeted_tools)
    skeleton_report = run_prompt_skeleton_concentration(
        rows,
        targeted_tools=pol.targeted_tools,
        max_allowed_concentration=pol.max_allowed_skeleton_concentration,
    )
    distribution_report = run_targeted_tool_distribution_check(rows, targeted_tools=pol.targeted_tools)
    forbidden_report = run_forbidden_pattern_scan(rows, patterns=pol.forbidden_patterns)
    coverage_report = run_intervention_coverage_accounting(cand_ann, targeted_tools=pol.targeted_tools)
    length_delta = run_prompt_length_delta_analysis(ref_ann, cand_ann, targeted_tools=pol.targeted_tools)
    ambiguity = run_prompt_ambiguity_audit(cand_ann)

    commitment = run_semantic_commitment_telemetry(
        rows,
        targeted_tools=pol.targeted_tools,
        i9_behavioral_report=i9_behavioral_report,
    )

    diversity_summary = build_diversity_review_summary(style_report, skeleton_report, pol)
    anti_homogenization = build_anti_homogenization_summary(forbidden_report, skeleton_report, style_report)
    samples = extract_targeted_prompt_samples(cand_ann, targeted_tools=pol.targeted_tools)

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
            "prompt_length_delta": length_delta,
            "prompt_ambiguity_audit": ambiguity,
            "semantic_commitment_telemetry": commitment,
        },
        "review_support": {
            "targeted_prompt_samples": samples,
            "diversity_review_summary": diversity_summary,
            "anti_homogenization_summary": anti_homogenization,
            "collapse_watch_preview": {
                "anchor_dominance_ratio": commitment["anchor_dominance_ratio"],
                "scalar_substitution_rebound_proxy": commitment["scalar_substitution_rebound_proxy"],
                "generalization_vs_recitation": commitment["commitment_generalization_vs_recitation"],
            },
        },
        "gate_state": {
            "approved_to_generate_dataset": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run i10 diagnostics on existing JSONL rows (no training/eval).")
    parser.add_argument("--input-jsonl", required=True)
    parser.add_argument("--reference-jsonl", default="")
    parser.add_argument(
        "--i9-behavioral-report-json",
        default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i9_behavioral_review_package.json",
    )
    parser.add_argument("--output-json", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = _load_jsonl(Path(args.input_jsonl).resolve())

    reference_rows = None
    if args.reference_jsonl.strip():
        reference_rows = _load_jsonl(Path(args.reference_jsonl).resolve())

    i9_behavior = None
    if args.i9_behavioral_report_json.strip():
        p = Path(args.i9_behavioral_report_json).resolve()
        if p.exists():
            i9_behavior = _load_json(p)

    report = build_full_diagnostics_report(
        rows,
        reference_rows=reference_rows,
        policy=scaffold_policy_defaults(),
        i9_behavioral_report=i9_behavior,
    )

    if args.output_json.strip():
        out = Path(args.output_json).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
