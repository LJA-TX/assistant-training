#!/usr/bin/env python3
"""
i9 diagnostics and review-support utilities.

Scope boundary:
- Analysis only.
- No dataset generation, no training, no eval execution.
- Approval gates remain closed.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
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

RUN_NAME = "stage_b_llama31_8b_base_v1_i9"

DEFAULT_FORBIDDEN_PATTERNS = (
    "never return",
    "must not output",
    "forbidden wrapper key",
    "always include tool_calls key regardless of request",
)

DEFAULT_TARGETED_TOOLS = ("rg_search", "read_file")

# Collapse-watch thresholds are interpretive telemetry only in pre-execution phase.
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
                raise RuntimeError(f"invalid row type at {path}:{line_no}: expected object")
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
        if not bool(meta.get("intervention_i9_row", False)):
            continue
        out.append(row)
    return out


def _calc_entropy(counter: Counter[str]) -> float:
    total = sum(counter.values())
    if total <= 0:
        return 0.0
    ent = 0.0
    for count in counter.values():
        p = count / total
        ent -= p * math.log2(p)
    return ent


def run_commitment_conversion_telemetry(
    rows: list[dict[str, Any]],
    *,
    targeted_tools: Iterable[str] | None = None,
    i8_behavioral_analysis: dict[str, Any] | None = None,
) -> dict[str, Any]:
    annotations = build_intervention_annotations(rows, targeted_tools=targeted_tools)
    intervention_rows = _intervention_rows(rows, targeted_tools=targeted_tools)

    # Global targeted behavior source accounting from intervention annotations.
    source_family_counts = Counter()
    source_behavior_counts = Counter()
    source_tool_counts = Counter()
    source_exact_valid_counts = Counter()
    source_total_counts = Counter()
    anchor_bucket_counts = Counter()
    conversion_ids = set()

    for row in intervention_rows:
        meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        family = str(meta.get("intervention_i9_family") or "unknown")
        behavior = str(meta.get("intervention_i9_behavior_source") or "unknown")
        tool = str(meta.get("tool") or "")
        prompt = ""
        msgs = row.get("messages")
        if isinstance(msgs, list):
            for msg in msgs:
                if isinstance(msg, dict) and msg.get("role") == "user":
                    prompt = str(msg.get("content") or "")
                    break

        source_family_counts[family] += 1
        source_behavior_counts[behavior] += 1
        source_tool_counts[tool] += 1
        source_total_counts[family] += 1
        if bool(meta.get("intervention_i9_source_exact_valid", False)):
            source_exact_valid_counts[family] += 1
        anchor_bucket_counts[_prompt_anchor_bucket(prompt)] += 1

        cid = str(meta.get("intervention_i9_conversion_id") or "")
        if cid:
            conversion_ids.add(cid)

    total_intervention = sum(source_family_counts.values())
    top_behavior = source_behavior_counts.most_common(1)[0] if source_behavior_counts else ("none", 0)
    top1_behavior_share = (top_behavior[1] / total_intervention) if total_intervention else 0.0

    literal_anchor_count = anchor_bucket_counts.get("literal_tool_calls", 0)
    anchor_dominance_ratio = (literal_anchor_count / total_intervention) if total_intervention else 0.0

    # Near-canonical-to-exact baseline ratio from i8 behavioral analysis inputs.
    near_canonical_rows = None
    exact_valid_rows = None
    scalar_substitution_share_baseline = None
    paraphrastic_success_distribution = {}
    if i8_behavioral_analysis:
        failure = i8_behavioral_analysis.get("commitment_failure_modes", {})
        near_canonical_rows = int(failure.get("structural_near_miss_count", 0) or 0)
        exact_valid_rows = int(i8_behavioral_analysis.get("canonical_emission_confidence_signals", {}).get("exact_valid_rows", 0) or 0)

        counts = failure.get("category_counts", {}) if isinstance(failure.get("category_counts"), dict) else {}
        scalar_count = int(counts.get("scalar_result_substitution_nonobject", 0) or 0) + int(
            counts.get("scalar_or_token_result_substitution", 0) or 0
        )
        denom = int(failure.get("non_exact_tool_rows", 0) or 0)
        scalar_substitution_share_baseline = (scalar_count / denom) if denom else 0.0

        sig = i8_behavioral_analysis.get("canonical_emission_confidence_signals", {})
        rg_success = sig.get("rg_search_pattern_success", {}) if isinstance(sig, dict) else {}
        if isinstance(rg_success, dict):
            for key, block in sorted(rg_success.items()):
                if not isinstance(block, dict):
                    continue
                total = int(block.get("total", 0) or 0)
                exact = int(block.get("exact_valid", 0) or 0)
                paraphrastic_success_distribution[key] = {
                    "total": total,
                    "exact_valid": exact,
                    "exact_valid_rate": round(exact / total, 6) if total else 0.0,
                }

    near_to_exact_ratio = None
    if near_canonical_rows is not None and exact_valid_rows is not None:
        near_to_exact_ratio = None if exact_valid_rows == 0 else round(near_canonical_rows / exact_valid_rows, 6)

    exact_valid_by_family = []
    for fam, total in sorted(source_total_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        exact = int(source_exact_valid_counts.get(fam, 0))
        exact_valid_by_family.append(
            {
                "conversion_source_family": fam,
                "rows": int(total),
                "source_exact_valid_rows_i8": exact,
                "source_exact_valid_rate_i8": round(exact / total, 6) if total else 0.0,
                "post_eval_exact_valid_rate_i9": None,
            }
        )

    family_source_counts = dict(sorted(source_family_counts.items(), key=lambda kv: (-kv[1], kv[0])))
    behavior_source_counts = dict(sorted(source_behavior_counts.items(), key=lambda kv: (-kv[1], kv[0])))

    intervention_entropy_bits = _calc_entropy(Counter(ann["prompt"] for ann in annotations if ann["is_targeted_family"]))
    intervention_prompt_uniqueness = 0.0
    targeted_annotations = [ann for ann in annotations if ann["is_targeted_family"]]
    if targeted_annotations:
        intervention_prompt_uniqueness = len({ann["prompt"] for ann in targeted_annotations}) / len(targeted_annotations)

    rebound_watch = {
        "baseline_scalar_substitution_share_i8": scalar_substitution_share_baseline,
        "max_allowed_rebound_delta": COLLAPSE_WATCH_THRESHOLDS["max_scalar_substitution_rebound_delta"],
        "trigger_definition": "flag if i9_eval_scalar_substitution_share > baseline + delta",
        "status": "pending_post_eval",
    }

    monoculture_watch = {
        "top1_behavioral_category": top_behavior[0],
        "top1_behavioral_category_share": round(top1_behavior_share, 6),
        "threshold": COLLAPSE_WATCH_THRESHOLDS["max_top1_behavioral_category_share"],
        "flag": top1_behavior_share > COLLAPSE_WATCH_THRESHOLDS["max_top1_behavioral_category_share"],
    }

    return {
        "status": "ok",
        "rows_analyzed": len(rows),
        "intervention_rows": total_intervention,
        "conversion_ids_count": len(conversion_ids),
        "exact_valid_by_failure_family_conversion_source": exact_valid_by_family,
        "wrapper_envelope_repair_success_rate": {
            "status": "pending_post_eval",
            "note": "Computed after canonical eval by tracking i9 intervention_source_family=near_miss_wrapper_envelope_repair_pairs.",
        },
        "semantic_substitution_conversion_success_rate": {
            "status": "pending_post_eval",
            "note": "Computed after canonical eval by tracking i9 intervention_source_family=semantic_substitution_conversion_pairs.",
        },
        "anchor_dominance_ratio": {
            "literal_tool_calls_anchor_rows": literal_anchor_count,
            "intervention_rows": total_intervention,
            "ratio": round(anchor_dominance_ratio, 6),
            "threshold": COLLAPSE_WATCH_THRESHOLDS["max_anchor_dominance_ratio"],
            "flag": anchor_dominance_ratio > COLLAPSE_WATCH_THRESHOLDS["max_anchor_dominance_ratio"],
            "anchor_bucket_distribution": dict(sorted(anchor_bucket_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        },
        "paraphrastic_canonical_success_distribution": {
            "status": "baseline_from_i8",
            "distribution": paraphrastic_success_distribution,
        },
        "top1_behavioral_category_share": monoculture_watch,
        "canonical_commitment_diversity_metrics": {
            "targeted_prompt_entropy_bits": round(intervention_entropy_bits, 6),
            "targeted_prompt_uniqueness_ratio": round(intervention_prompt_uniqueness, 6),
            "source_family_distribution": family_source_counts,
            "source_behavior_distribution": behavior_source_counts,
            "source_tool_distribution": dict(sorted(source_tool_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        },
        "near_canonical_to_exact_conversion_ratio": {
            "baseline_near_canonical_rows_i8": near_canonical_rows,
            "baseline_exact_valid_rows_i8": exact_valid_rows,
            "baseline_ratio": near_to_exact_ratio,
            "status": "baseline_only_pre_eval",
        },
        "scalar_substitution_rebound_detection": rebound_watch,
        "behavioral_monoculture_detection": monoculture_watch,
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
            "commitment_conversion_telemetry": {"status": "todo"},
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
    i8_behavioral_analysis: dict[str, Any] | None = None,
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

    commitment_telemetry = run_commitment_conversion_telemetry(
        rows,
        targeted_tools=pol.targeted_tools,
        i8_behavioral_analysis=i8_behavioral_analysis,
    )

    diversity_summary = build_diversity_review_summary(style_report, skeleton_report, pol)
    anti_homogenization_summary = build_anti_homogenization_summary(
        forbidden_report,
        skeleton_report,
        style_report,
    )
    targeted_samples = extract_targeted_prompt_samples(candidate_annotations, targeted_tools=pol.targeted_tools)

    review_checklist = [
        "Confirm intervention rows are localized to rg_search/read_file conversion families only.",
        "Confirm ambiguity hard-block counters remain zero.",
        "Confirm literal tool_calls anchor dominance ratio stays below collapse-watch threshold.",
        "Confirm top1 behavioral source share does not indicate monoculture.",
        "Confirm source-family mix includes both near-miss and semantic-substitution conversion coverage.",
        "Confirm forbidden-pattern scan has zero hits.",
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
            "commitment_conversion_telemetry": commitment_telemetry,
        },
        "review_support": {
            "review_checklist": review_checklist,
            "intervention_budget_summary": {
                "candidate_rows": len(candidate_annotations),
                "reference_rows": len(reference_annotations),
                "targeted_rows": coverage_report["targeted_rows"],
                "targeted_share": coverage_report["targeted_share"],
                "tool_counts": coverage_report["tool_counts"],
                "i9_intervention_rows": commitment_telemetry["intervention_rows"],
                "i9_source_family_distribution": commitment_telemetry["canonical_commitment_diversity_metrics"][
                    "source_family_distribution"
                ],
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
            "collapse_watch_preview": {
                "top1_behavioral_category_share": commitment_telemetry["top1_behavioral_category_share"],
                "anchor_dominance_ratio": commitment_telemetry["anchor_dominance_ratio"],
                "scalar_substitution_rebound_detection": commitment_telemetry["scalar_substitution_rebound_detection"],
            },
        },
        "gate_state": {
            "approved_to_generate_dataset": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run i9 diagnostics on existing JSONL rows (no training/eval).")
    parser.add_argument("--input-jsonl", required=True)
    parser.add_argument("--reference-jsonl", default="")
    parser.add_argument("--i8-behavioral-analysis-json", default="")
    parser.add_argument("--output-json", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = _load_jsonl(Path(args.input_jsonl).resolve())
    reference_rows = None
    if args.reference_jsonl.strip():
        reference_rows = _load_jsonl(Path(args.reference_jsonl).resolve())

    i8_behavioral = None
    if args.i8_behavioral_analysis_json.strip():
        i8_behavioral = _load_json(Path(args.i8_behavioral_analysis_json).resolve())

    report = build_full_diagnostics_report(
        rows,
        reference_rows=reference_rows,
        policy=scaffold_policy_defaults(),
        i8_behavioral_analysis=i8_behavioral,
    )

    if args.output_json.strip():
        out = Path(args.output_json).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
