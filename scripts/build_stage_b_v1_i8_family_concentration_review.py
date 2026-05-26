#!/usr/bin/env python3
"""
Build family concentration telemetry artifacts for Stage B i8.

This script is analysis-only and does not mutate dataset composition.
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
from typing import Any

from i8_diagnostics_scaffold import build_intervention_annotations

RUN_NAME = "stage_b_llama31_8b_base_v1_i8"
TARGETED_TOOLS = ("rg_search", "read_file")


@dataclass(frozen=True)
class Config:
    min_rows_material: int
    concentration_share_warn: float
    low_effective_diversity_ratio_warn: float
    low_prompt_entropy_bits_warn: float
    low_semantic_variation_warn: float
    high_nn_similarity_warn: float
    top_n: int


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"expected object JSON: {path}")
    return data


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
                raise RuntimeError(f"invalid JSONL {path}:{line_no}: {exc}") from exc
            if not isinstance(row, dict):
                raise RuntimeError(f"invalid row object at {path}:{line_no}")
            rows.append(row)
    return rows


def _assistant_tool_name(row: dict[str, Any]) -> str:
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


def _source_case_id(row: dict[str, Any], idx: int) -> str:
    meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    return str(meta.get("source_case_id") or meta.get("case_id") or f"row_{idx:06d}")


def _prompt(row: dict[str, Any]) -> str:
    msgs = row.get("messages")
    if not isinstance(msgs, list):
        return ""
    for msg in msgs:
        if isinstance(msg, dict) and msg.get("role") == "user":
            return str(msg.get("content") or "")
    return ""


def _tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9_]+", text.lower()))


def _shannon_entropy(items: list[str]) -> float:
    if not items:
        return 0.0
    cnt = Counter(items)
    n = float(len(items))
    h = 0.0
    for c in cnt.values():
        p = c / n
        h -= p * math.log2(p)
    return h


def _effective_count_from_entropy(entropy_bits: float) -> float:
    return float(2 ** entropy_bits)


def _mean_pairwise_jaccard(token_sets: list[set[str]]) -> float:
    n = len(token_sets)
    if n <= 1:
        return 0.0
    num = 0.0
    den = 0
    for i in range(n):
        a = token_sets[i]
        for j in range(i + 1, n):
            b = token_sets[j]
            union = a.union(b)
            if not union:
                sim = 1.0
            else:
                sim = len(a.intersection(b)) / len(union)
            num += sim
            den += 1
    return num / den if den else 0.0


def _mean_nearest_neighbor_jaccard(token_sets: list[set[str]]) -> float:
    n = len(token_sets)
    if n <= 1:
        return 0.0
    sims: list[float] = []
    for i in range(n):
        a = token_sets[i]
        best = 0.0
        for j in range(n):
            if i == j:
                continue
            b = token_sets[j]
            union = a.union(b)
            if not union:
                sim = 1.0
            else:
                sim = len(a.intersection(b)) / len(union)
            if sim > best:
                best = sim
        sims.append(best)
    return float(sum(sims) / len(sims)) if sims else 0.0


def _history_by_family(i3_rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for idx, row in enumerate(i3_rows, start=1):
        tool = _assistant_tool_name(row)
        if tool not in TARGETED_TOOLS:
            continue
        by_family[_source_case_id(row, idx)].append(row)

    out: dict[str, dict[str, Any]] = {}
    for family, rows in by_family.items():
        tools = { _assistant_tool_name(r) for r in rows }
        targets = { _assistant_target_canon(r) for r in rows }
        prompts = { _prompt(r) for r in rows }
        out[family] = {
            "rows": len(rows),
            "distinct_tools": len(tools),
            "distinct_targets": len(targets),
            "distinct_prompts": len(prompts),
            "prior_multi_tool_divergence": len(tools) > 1,
            "prior_ambiguity_involvement": (len(tools) > 1) or (len(targets) > 1),
        }
    return out


def _family_metrics(
    family: str,
    anns: list[dict[str, Any]],
    targeted_rows_total: int,
    history: dict[str, dict[str, Any]],
    cfg: Config,
) -> dict[str, Any]:
    row_count = len(anns)
    tools = sorted({str(a.get("tool") or "") for a in anns})
    targets = {str(a.get("target_canon") or "") for a in anns}
    prompts = [str(a.get("prompt") or "") for a in anns]
    unique_prompts = sorted(set(prompts))
    skeletons = {str(a.get("skeleton_id") or "") for a in anns}

    styles = Counter(str(a.get("style_bucket") or "") for a in anns)
    dominant_style_bucket, dominant_style_count = ("", 0)
    if styles:
        dominant_style_bucket, dominant_style_count = sorted(styles.items(), key=lambda kv: (-kv[1], kv[0]))[0]

    prompt_entropy_bits = _shannon_entropy(prompts)
    effective_prompt_count = _effective_count_from_entropy(prompt_entropy_bits)
    effective_diversity_ratio = (effective_prompt_count / row_count) if row_count else 0.0
    normalized_prompt_uniqueness = (len(unique_prompts) / row_count) if row_count else 0.0

    token_sets = [_tokenize(p) for p in prompts]
    pairwise_jaccard = _mean_pairwise_jaccard(token_sets)
    mean_nn_similarity = _mean_nearest_neighbor_jaccard(token_sets)
    semantic_variation_estimate = 1.0 - mean_nn_similarity

    rem_rows = sum(1 for a in anns if "prompt_conflict_hard_block_resolution" in str(a.get("intervention_tags") or ""))
    # Pull remediation flags directly from source metadata-derived tags if present in prompt text annotations.
    # (The row-level remediation booleans are read from raw rows in caller and merged here.)

    hist = history.get(family, {})
    prior_multi_tool = bool(hist.get("prior_multi_tool_divergence", False))
    prior_ambiguity = bool(hist.get("prior_ambiguity_involvement", False))

    percent_targeted = (row_count / targeted_rows_total * 100.0) if targeted_rows_total else 0.0

    risk_flags: list[str] = []
    if (percent_targeted / 100.0) > cfg.concentration_share_warn:
        risk_flags.append("family_concentration_above_threshold")
    if effective_diversity_ratio < cfg.low_effective_diversity_ratio_warn:
        risk_flags.append("low_effective_diversity_ratio")
    if prompt_entropy_bits < cfg.low_prompt_entropy_bits_warn:
        risk_flags.append("low_prompt_entropy")
    if semantic_variation_estimate < cfg.low_semantic_variation_warn:
        risk_flags.append("low_semantic_variation_estimate")
    if mean_nn_similarity > cfg.high_nn_similarity_warn:
        risk_flags.append("high_nearest_neighbor_similarity")
    if prior_ambiguity:
        risk_flags.append("prior_ambiguity_involvement")
    if prior_multi_tool:
        risk_flags.append("multi_tool_lineage_history")

    # Warning-only concentration risk score.
    score = 0.0
    score += max(0.0, (percent_targeted / 100.0 - cfg.concentration_share_warn) / max(cfg.concentration_share_warn, 1e-9))
    score += max(0.0, (cfg.low_effective_diversity_ratio_warn - effective_diversity_ratio) / max(cfg.low_effective_diversity_ratio_warn, 1e-9))
    score += max(0.0, (cfg.low_prompt_entropy_bits_warn - prompt_entropy_bits) / max(cfg.low_prompt_entropy_bits_warn, 1e-9))
    score += max(0.0, (cfg.low_semantic_variation_warn - semantic_variation_estimate) / max(cfg.low_semantic_variation_warn, 1e-9))
    if prior_ambiguity:
        score += 0.4
    if prior_multi_tool:
        score += 0.3

    return {
        "source_case_id": family,
        "row_count": row_count,
        "percent_of_targeted_dataset": round(percent_targeted, 6),
        "tool_diversity": {
            "distinct_tools": len(tools),
            "tools": tools,
        },
        "target_diversity": {
            "distinct_targets": len(targets),
        },
        "prompt_diversity": {
            "distinct_prompts": len(unique_prompts),
            "normalized_prompt_uniqueness": round(normalized_prompt_uniqueness, 6),
        },
        "unique_skeleton_count": len(skeletons),
        "dominant_style_bucket": {
            "bucket": dominant_style_bucket,
            "share": round(dominant_style_count / row_count, 6) if row_count else 0.0,
        },
        "effective_diversity": {
            "prompt_entropy_bits": round(prompt_entropy_bits, 6),
            "effective_prompt_count": round(effective_prompt_count, 6),
            "effective_diversity_ratio": round(effective_diversity_ratio, 6),
            "mean_pairwise_jaccard": round(pairwise_jaccard, 6),
            "mean_nearest_neighbor_jaccard": round(mean_nn_similarity, 6),
            "semantic_variation_estimate": round(semantic_variation_estimate, 6),
        },
        "ambiguity_remediation_involvement": {
            "rows_with_remediation_flag": 0,
            "share": 0.0,
        },
        "prior_multi_tool_divergence": prior_multi_tool,
        "prior_ambiguity_involvement": prior_ambiguity,
        "risk_flags": risk_flags,
        "concentration_risk_score": round(score, 6),
    }


def _merge_remediation_counts(family_reports: list[dict[str, Any]], targeted_rows: list[dict[str, Any]]) -> None:
    rem = Counter()
    total = Counter()
    for idx, row in enumerate(targeted_rows, start=1):
        family = _source_case_id(row, idx)
        total[family] += 1
        meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        if bool(meta.get("ambiguity_remediation_applied", False)):
            rem[family] += 1

    for rep in family_reports:
        fam = rep["source_case_id"]
        rows = int(total.get(fam, 0))
        r = int(rem.get(fam, 0))
        rep["ambiguity_remediation_involvement"] = {
            "rows_with_remediation_flag": r,
            "share": round(r / rows, 6) if rows else 0.0,
        }
        if r > 0 and "ambiguity_remediation_applied" not in rep["risk_flags"]:
            rep["risk_flags"].append("ambiguity_remediation_applied")


def _concentration_simulation(family_reports: list[dict[str, Any]], targeted_rows_total: int) -> dict[str, Any]:
    family_counts = {f["source_case_id"]: int(f["row_count"]) for f in family_reports}

    def simulate(cap_share: float) -> dict[str, Any]:
        cap_rows = max(1, int(math.floor(cap_share * targeted_rows_total)))
        removed = 0
        capped_families = 0
        post_counts: dict[str, int] = {}
        for fam, cnt in family_counts.items():
            keep = min(cnt, cap_rows)
            post_counts[fam] = keep
            if cnt > cap_rows:
                capped_families += 1
                removed += (cnt - cap_rows)

        remaining = targeted_rows_total - removed
        family_entropy_pre = _shannon_entropy([f for f, cnt in family_counts.items() for _ in range(cnt)])
        family_entropy_post = _shannon_entropy([f for f, cnt in post_counts.items() for _ in range(cnt)])

        return {
            "cap_share": cap_share,
            "cap_rows": cap_rows,
            "targeted_rows_removed": removed,
            "targeted_rows_removed_percent": round(removed / targeted_rows_total * 100.0, 6) if targeted_rows_total else 0.0,
            "targeted_rows_remaining": remaining,
            "families_capped": capped_families,
            "family_entropy_pre": round(family_entropy_pre, 6),
            "family_entropy_post": round(family_entropy_post, 6),
            "diversity_delta_family_entropy": round(family_entropy_post - family_entropy_pre, 6),
            "intervention_dilution_risk": (
                "high" if (removed / targeted_rows_total if targeted_rows_total else 0.0) > 0.2
                else "moderate" if (removed / targeted_rows_total if targeted_rows_total else 0.0) > 0.1
                else "low"
            ),
        }

    return {
        "status": "read_only_simulation",
        "simulated_caps": [simulate(0.20), simulate(0.15), simulate(0.12), simulate(0.10)],
    }


def _memorization_risk_analysis(family_reports: list[dict[str, Any]], *, top_n: int) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for rep in sorted(family_reports, key=lambda x: (-x["concentration_risk_score"], -x["row_count"], x["source_case_id"]))[:top_n]:
        eff = rep["effective_diversity"]
        tool_div = rep["tool_diversity"]["distinct_tools"]
        target_div = rep["target_diversity"]["distinct_targets"]
        prompt_div = rep["prompt_diversity"]["distinct_prompts"]

        structurally_diverse = target_div > 1
        routing_diverse = tool_div > 1
        semantically_diverse = eff["semantic_variation_estimate"] >= 0.45 and rep["prompt_diversity"]["normalized_prompt_uniqueness"] >= 0.35

        memorization_prone = (
            rep["percent_of_targeted_dataset"] >= 10.0
            and eff["effective_diversity_ratio"] < 0.35
            and eff["semantic_variation_estimate"] < 0.45
        )

        likely_safe = (not memorization_prone) and (len(rep["risk_flags"]) <= 2)
        potentially_coercive = memorization_prone or ("high_nearest_neighbor_similarity" in rep["risk_flags"])

        out.append(
            {
                "source_case_id": rep["source_case_id"],
                "row_count": rep["row_count"],
                "risk_score": rep["concentration_risk_score"],
                "structurally_diverse": structurally_diverse,
                "semantically_diverse": semantically_diverse,
                "routing_diverse": routing_diverse,
                "likely_memorization_prone": memorization_prone,
                "likely_safe": likely_safe,
                "ambiguous_historically": bool(rep.get("prior_ambiguity_involvement", False)),
                "potentially_coercive": potentially_coercive,
                "interpretation": (
                    "high concentration with low effective diversity; monitor for memorized routing"
                    if memorization_prone
                    else "concentration present but effective diversity indicates bounded memorization risk"
                ),
                "risk_flags": rep["risk_flags"],
                "prompt_diversity": prompt_div,
                "target_diversity": target_div,
            }
        )
    return out


def build_review(args: argparse.Namespace) -> dict[str, Any]:
    cfg = Config(
        min_rows_material=int(args.min_rows_material),
        concentration_share_warn=float(args.concentration_share_warn),
        low_effective_diversity_ratio_warn=float(args.low_effective_diversity_ratio_warn),
        low_prompt_entropy_bits_warn=float(args.low_prompt_entropy_bits_warn),
        low_semantic_variation_warn=float(args.low_semantic_variation_warn),
        high_nn_similarity_warn=float(args.high_nn_similarity_warn),
        top_n=int(args.top_n),
    )

    i8_train = _load_jsonl(Path(args.i8_train_jsonl).resolve())
    i8_val = _load_jsonl(Path(args.i8_val_jsonl).resolve())
    i3_train = _load_jsonl(Path(args.i3_train_jsonl).resolve())
    i3_val = _load_jsonl(Path(args.i3_val_jsonl).resolve())

    i8_rows = i8_train + i8_val
    i3_rows = i3_train + i3_val

    anns = build_intervention_annotations(i8_rows, targeted_tools=TARGETED_TOOLS)

    by_family_anns: dict[str, list[dict[str, Any]]] = defaultdict(list)
    targeted_rows: list[dict[str, Any]] = []
    for idx, row in enumerate(i8_rows, start=1):
        tool = _assistant_tool_name(row)
        if tool not in TARGETED_TOOLS:
            continue
        targeted_rows.append(row)
        family = _source_case_id(row, idx)

        ann = None
        # Find matching annotation by stable identifiers.
        prompt = _prompt(row)
        for candidate in anns:
            if candidate["source_case_id"] == family and candidate["prompt"] == prompt and candidate["tool"] == tool:
                ann = candidate
                break
        if ann is None:
            # deterministic fallback: build minimal annotation directly.
            ann = {
                "source_case_id": family,
                "tool": tool,
                "target_canon": _assistant_target_canon(row),
                "arguments_canon": "",
                "style_bucket": "",
                "skeleton_id": "",
                "prompt": prompt,
                "prompt_chars": len(prompt),
                "prompt_words": len(prompt.split()),
                "intervention_tags": [],
                "is_targeted_family": True,
            }
        by_family_anns[family].append(ann)

    targeted_rows_total = len(targeted_rows)
    history = _history_by_family(i3_rows)

    family_reports: list[dict[str, Any]] = []
    for family, fam_anns in by_family_anns.items():
        rep = _family_metrics(family, fam_anns, targeted_rows_total, history, cfg)
        if rep["row_count"] >= cfg.min_rows_material:
            family_reports.append(rep)

    _merge_remediation_counts(family_reports, targeted_rows)

    family_reports = sorted(family_reports, key=lambda x: (-x["row_count"], x["source_case_id"]))

    largest = sorted(family_reports, key=lambda x: (-x["row_count"], x["source_case_id"]))[:cfg.top_n]
    lowest_div = sorted(
        family_reports,
        key=lambda x: (
            x["effective_diversity"]["effective_diversity_ratio"],
            x["effective_diversity"]["semantic_variation_estimate"],
            -x["row_count"],
            x["source_case_id"],
        ),
    )[:cfg.top_n]
    highest_risk = sorted(family_reports, key=lambda x: (-x["concentration_risk_score"], -x["row_count"], x["source_case_id"]))[:cfg.top_n]

    risk_summary = {
        "families_with_any_warning": sum(1 for f in family_reports if f["risk_flags"]),
        "families_above_concentration_threshold": sum(1 for f in family_reports if "family_concentration_above_threshold" in f["risk_flags"]),
        "families_with_low_effective_diversity": sum(1 for f in family_reports if "low_effective_diversity_ratio" in f["risk_flags"]),
        "families_with_prior_ambiguity": sum(1 for f in family_reports if bool(f.get("prior_ambiguity_involvement", False))),
        "families_with_multi_tool_history": sum(1 for f in family_reports if bool(f.get("prior_multi_tool_divergence", False))),
    }

    simulation = _concentration_simulation(family_reports, targeted_rows_total)
    memorization = _memorization_risk_analysis(highest_risk, top_n=cfg.top_n)

    return {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "iteration": RUN_NAME,
        "status": "completed",
        "methodology": {
            "effective_diversity_estimation": {
                "prompt_uniqueness": "distinct_prompts / row_count",
                "prompt_entropy_bits": "Shannon entropy over prompt frequency within family",
                "effective_prompt_count": "2 ^ entropy_bits",
                "effective_diversity_ratio": "effective_prompt_count / row_count",
                "lexical_similarity": "pairwise and nearest-neighbor Jaccard overlap on token sets",
                "semantic_variation_estimate": "1 - mean_nearest_neighbor_jaccard",
            },
            "risk_scoring": "warning-only composite of concentration share, effective-diversity shortfall, entropy shortfall, semantic-variation shortfall, and lineage ambiguity history",
            "material_family_cutoff_rows": cfg.min_rows_material,
        },
        "config": {
            "concentration_share_warn": cfg.concentration_share_warn,
            "low_effective_diversity_ratio_warn": cfg.low_effective_diversity_ratio_warn,
            "low_prompt_entropy_bits_warn": cfg.low_prompt_entropy_bits_warn,
            "low_semantic_variation_warn": cfg.low_semantic_variation_warn,
            "high_nn_similarity_warn": cfg.high_nn_similarity_warn,
            "top_n": cfg.top_n,
        },
        "dataset_scope": {
            "targeted_tools": list(TARGETED_TOOLS),
            "targeted_rows_total": targeted_rows_total,
            "material_families_count": len(family_reports),
        },
        "per_family_metrics": family_reports,
        "ranked_summaries": {
            "top_largest_families": largest,
            "top_lowest_diversity_families": lowest_div,
            "top_highest_concentration_risk_families": highest_risk,
        },
        "risk_flags_summary": risk_summary,
        "memorization_risk_analysis": memorization,
        "optional_concentration_simulation": simulation,
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }


def _write_markdown(report: dict[str, Any], out_path: Path) -> None:
    lines: list[str] = []
    lines.append("# Stage B i8 Family Concentration Review")
    lines.append("")
    lines.append(f"- Generated UTC: {report.get('generated_utc')}")
    lines.append(f"- Iteration: {report.get('iteration')}")
    lines.append(f"- Targeted rows: {report.get('dataset_scope', {}).get('targeted_rows_total')}")
    lines.append(f"- Material families: {report.get('dataset_scope', {}).get('material_families_count')}")
    lines.append("")
    lines.append("## Method")
    lines.append("- Effective diversity uses prompt entropy, effective prompt count, prompt uniqueness, and lexical Jaccard overlap.")
    lines.append("- Risk flags are warnings only; no hard-block decisions are made in this artifact.")
    lines.append("")

    lines.append("## Top Largest Families")
    for f in report.get("ranked_summaries", {}).get("top_largest_families", [])[:10]:
        lines.append(
            f"- {f['source_case_id']}: rows={f['row_count']} pct_targeted={f['percent_of_targeted_dataset']} "
            f"eff_div_ratio={f['effective_diversity']['effective_diversity_ratio']} risk={f['concentration_risk_score']}"
        )
    lines.append("")

    lines.append("## Top Lowest-Diversity Families")
    for f in report.get("ranked_summaries", {}).get("top_lowest_diversity_families", [])[:10]:
        lines.append(
            f"- {f['source_case_id']}: rows={f['row_count']} eff_div_ratio={f['effective_diversity']['effective_diversity_ratio']} "
            f"entropy={f['effective_diversity']['prompt_entropy_bits']} semantic_var={f['effective_diversity']['semantic_variation_estimate']}"
        )
    lines.append("")

    lines.append("## Top Concentration-Risk Families")
    for f in report.get("ranked_summaries", {}).get("top_highest_concentration_risk_families", [])[:10]:
        lines.append(
            f"- {f['source_case_id']}: risk={f['concentration_risk_score']} rows={f['row_count']} flags={f['risk_flags']}"
        )
    lines.append("")

    lines.append("## Memorization-Risk Interpretation")
    for m in report.get("memorization_risk_analysis", [])[:10]:
        lines.append(
            f"- {m['source_case_id']}: memorization_prone={m['likely_memorization_prone']} "
            f"semantically_diverse={m['semantically_diverse']} routing_diverse={m['routing_diverse']} "
            f"ambiguous_historically={m['ambiguous_historically']}"
        )
        lines.append(f"  interpretation: {m['interpretation']}")
    lines.append("")

    lines.append("## Optional Cap Simulation (Read-Only)")
    for sim in report.get("optional_concentration_simulation", {}).get("simulated_caps", []):
        lines.append(
            f"- cap={sim['cap_share']:.2f} removed={sim['targeted_rows_removed']} "
            f"({sim['targeted_rows_removed_percent']}%) families_capped={sim['families_capped']} "
            f"entropy_delta={sim['diversity_delta_family_entropy']} dilution_risk={sim['intervention_dilution_risk']}"
        )
    lines.append("")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Stage B i8 family concentration review artifacts.")
    parser.add_argument("--i8-train-jsonl", default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i8_train.jsonl")
    parser.add_argument("--i8-val-jsonl", default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i8_val.jsonl")
    parser.add_argument("--i3-train-jsonl", default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl")
    parser.add_argument("--i3-val-jsonl", default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_val.jsonl")

    parser.add_argument("--output-json", default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i8_family_concentration_review.json")
    parser.add_argument("--output-md", default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i8_family_concentration_review.md")

    parser.add_argument("--min-rows-material", type=int, default=5)
    parser.add_argument("--concentration-share-warn", type=float, default=0.10)
    parser.add_argument("--low-effective-diversity-ratio-warn", type=float, default=0.30)
    parser.add_argument("--low-prompt-entropy-bits-warn", type=float, default=2.0)
    parser.add_argument("--low-semantic-variation-warn", type=float, default=0.35)
    parser.add_argument("--high-nn-similarity-warn", type=float, default=0.65)
    parser.add_argument("--top-n", type=int, default=10)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_review(args)

    out_json = Path(args.output_json).resolve()
    out_md = Path(args.output_md).resolve()
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)

    out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    _write_markdown(report, out_md)

    print(json.dumps({"json": str(out_json), "md": str(out_md)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
