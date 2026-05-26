#!/usr/bin/env python3
"""
Build Stage B i9 candidate dataset package.

Governance boundaries:
- Explicit unlock flags are required for dataset emission.
- No training, no canonical eval, no gate opening.
- Intervention is localized to commitment-conversion repair families.
- Ambiguity, contamination, and anti-homogenization invariants are fail-fast.
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
from typing import Any

from i9_diagnostics_scaffold import (
    build_full_diagnostics_report,
    build_intervention_annotations,
    run_prompt_ambiguity_audit,
    scaffold_policy_defaults,
)

RUN_NAME = "stage_b_llama31_8b_base_v1_i9"
PARENT_DATASET_ITERATION = "stage_b_llama31_8b_base_v1_i8"
PARENT_CHECKPOINT = "stage_b_llama31_8b_base_v1_i3"
TARGETED_TOOLS = ("rg_search", "read_file")

PRIMARY_FAMILY = "near_miss_wrapper_envelope_repair_pairs"
SECONDARY_FAMILY = "semantic_substitution_conversion_pairs"
TERTIARY_FAMILY = "uncertainty_conditioned_canonical_fallback"

TRAIN_QUOTAS = {
    PRIMARY_FAMILY: 24,
    SECONDARY_FAMILY: 56,
    TERTIARY_FAMILY: 8,
}
VAL_QUOTAS = {
    PRIMARY_FAMILY: 4,
    SECONDARY_FAMILY: 8,
    TERTIARY_FAMILY: 2,
}

FORBIDDEN_GLOBAL_PRESSURES = (
    "global_negation_heavy_schema_pressure",
    "global_imperative_template_rewrites",
    "wrapper_key_blacklist_flooding",
    "semantic_flattening",
    "lexical_trigger_memorization_campaign",
)

NEAR_MISS_CUES = (
    "Emit one canonical tool-invocation payload object.",
    "Return exactly one structured function-call envelope.",
    "Output a single parseable call payload for this request.",
    "Respond with one canonical tool call payload only.",
)

SEMANTIC_CONVERSION_CUES = (
    "First return the tool invocation payload instead of result content.",
    "Provide the acquisition call payload before any result text.",
    "Return only the structured tool invocation needed to gather evidence.",
    "Commit to the canonical retrieval call payload, not direct result prose.",
)

UNCERTAINTY_FALLBACK_CUES = (
    "If unsure about the result, return the canonical retrieval call payload.",
    "When uncertain, commit to the tool invocation payload for evidence gathering.",
    "Under uncertainty, emit the structured tool call payload first.",
)

# Upper bounds prevent local-template collapse and concentration spikes.
MAX_PER_SKELETON = 4
MAX_PER_SOURCE_CASE = 12
MAX_PER_BASE_PROMPT = 2
MAX_PER_TRANSFORM_MODE_SHARE = 0.45
MAX_LITERAL_ANCHOR_SHARE = 0.65
MAX_TOP1_FAMILY_SHARE = 0.70


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
    eval_comparison_rows_jsonl: Path
    i8_behavioral_analysis_json: Path
    i9_recon_json: Path
    i9_taxonomy_json: Path
    i9_risk_matrix_json: Path


@dataclass(frozen=True)
class OutputPaths:
    train_jsonl: Path
    val_jsonl: Path
    summary_json: Path
    diagnostics_json: Path
    contamination_audit_json: Path
    prompt_ambiguity_audit_json: Path
    collapse_watch_telemetry_json: Path
    anchor_dominance_telemetry_json: Path
    review_package_json: Path


@dataclass(frozen=True)
class Candidate:
    split: str
    row_index_1based: int
    source_case_id: str
    tool: str
    source_prompt: str
    source_target: str
    source_args_canon: str
    skeleton_id: str
    source_schema_reason: str
    source_behavior: str
    source_family: str
    source_exact_valid: bool


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


def _stable_int(text: str) -> int:
    return int(hashlib.sha1(text.encode("utf-8")).hexdigest()[:12], 16)


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
    value = str(meta.get("source_case_id") or meta.get("case_id") or "").strip()
    return value or fallback


def _is_tool_row(row: dict[str, Any]) -> bool:
    return bool(_tool_name(row))


def _strip_i8_tail(prompt: str) -> str:
    pats = [
        r"\s*return strict json tool_calls only\.?$",
        r"\s*return strict json only\.?$",
        r"\s*respond with exactly one parseable json object containing tool_calls\.?$",
        r"\s*return one valid json object with top-level key tool_calls\.?$",
        r"\s*output one strict json object only, with top-level key tool_calls\.?$",
        r"\s*produce only json: a single object whose top-level key is tool_calls\.?$",
        r"\s*emit a single parseable json object; top-level key must be tool_calls\.?$",
        r"\s*disambiguation:\s*call\s+[^.]+\.$",
    ]
    out = prompt.strip()
    low = out.lower()
    changed = True
    while changed:
        changed = False
        for pat in pats:
            m = re.search(pat, low)
            if not m:
                continue
            out = out[: m.start()].rstrip()
            low = out.lower()
            changed = True
            break
    return out


def _normalize_prompt_skeleton(prompt: str) -> str:
    text = _strip_i8_tail(prompt).lower().strip()
    text = re.sub(r"`[^`]*`", "`<code>`", text)
    text = re.sub(r'"[^"]*"', '"<str>"', text)
    text = re.sub(r"'[^']*'", "'<str>'", text)
    text = re.sub(r"\b\d+\b", "<num>", text)
    text = re.sub(r"(?:/[a-z0-9._\-]+)+", "<path>", text)
    text = re.sub(r"[a-z]:\\(?:[^\\\s]+\\)*[^\\\s]*", "<path>", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _skeleton_id(prompt: str) -> str:
    return hashlib.sha1(_normalize_prompt_skeleton(prompt).encode("utf-8")).hexdigest()[:12]


def _prompt_anchor_bucket(prompt: str) -> str:
    p = prompt.lower()
    if "tool_calls" in p:
        return "literal_tool_calls"
    if "tool call" in p or "tool-call" in p or "function call" in p:
        return "paraphrastic_tool_call"
    if "json object" in p or "structured payload" in p or "canonical payload" in p:
        return "schema_paraphrase"
    return "no_anchor_phrase"


def _behavior_from_eval(schema_reason: str, generated_text: str) -> str:
    text = (generated_text or "").strip()
    low = text.lower()

    if schema_reason == "missing_tool_calls":
        if "tool_function" in low or "tool_functions" in low:
            return "wrapper_key_drift"
        return "envelope_omission"

    if schema_reason == "payload_not_object":
        return "direct_scalar_answer_substitution"

    if schema_reason == "payload_not_parsed":
        if text.startswith("{") and "tool_calls" not in low:
            return "object_missing_commitment_envelope"
        if "\n" in text:
            return "code_excerpt_result_substitution"
        if len(text.split()) <= 3:
            return "token_scalar_substitution"
        return "semantic_textual_substitution"

    return "other"


def _family_from_behavior_and_prompt(behavior: str, prompt: str) -> str:
    if behavior in {"wrapper_key_drift", "envelope_omission", "object_missing_commitment_envelope"}:
        return PRIMARY_FAMILY

    p = prompt.lower()
    if "whether" in p or "zero or non-zero" in p or "if unsure" in p:
        return TERTIARY_FAMILY

    return SECONDARY_FAMILY


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
        eval_comparison_rows_jsonl=Path(args.eval_comparison_rows_jsonl).resolve(),
        i8_behavioral_analysis_json=Path(args.i8_behavioral_analysis_json).resolve(),
        i9_recon_json=Path(args.i9_recon_json).resolve(),
        i9_taxonomy_json=Path(args.i9_taxonomy_json).resolve(),
        i9_risk_matrix_json=Path(args.i9_risk_matrix_json).resolve(),
    )


def _resolve_outputs(args: argparse.Namespace) -> OutputPaths:
    out_root = Path(args.output_root).resolve()
    report_root = Path(args.report_root).resolve()
    return OutputPaths(
        train_jsonl=out_root / "dataset_v1_0_stage_b_recovery_i9_train.jsonl",
        val_jsonl=out_root / "dataset_v1_0_stage_b_recovery_i9_val.jsonl",
        summary_json=out_root / "dataset_v1_0_stage_b_recovery_i9_summary.json",
        diagnostics_json=report_root / "stage_b_v1_i9_dataset_diagnostics.json",
        contamination_audit_json=report_root / "stage_b_v1_i9_contamination_audit.json",
        prompt_ambiguity_audit_json=report_root / "stage_b_v1_i9_prompt_ambiguity_audit.json",
        collapse_watch_telemetry_json=report_root / "stage_b_v1_i9_collapse_watch_telemetry.json",
        anchor_dominance_telemetry_json=report_root / "stage_b_v1_i9_anchor_dominance_telemetry.json",
        review_package_json=report_root / "stage_b_v1_i9_human_review_package.json",
    )


def _fail_fast_unlock(args: argparse.Namespace) -> None:
    if not args.enable_dataset_emission:
        raise RuntimeError("dataset emission requires explicit --enable-dataset-emission")
    if not args.allow_generation_phase:
        raise RuntimeError("dataset emission requires explicit --allow-generation-phase")
    if not args.enable_i9_commitment_conversion:
        raise RuntimeError("i9 generation requires explicit --enable-i9-commitment-conversion")


def _fail_fast_inputs(inputs: BuilderInputs) -> None:
    required = [
        inputs.parent_train_jsonl,
        inputs.parent_val_jsonl,
        inputs.parent_summary_json,
        inputs.eval_heldout_jsonl,
        inputs.eval_tool_holdout_jsonl,
        inputs.eval_no_call_jsonl,
        inputs.eval_adversarial_jsonl,
        inputs.eval_direct_answer_jsonl,
        inputs.eval_comparison_rows_jsonl,
        inputs.i8_behavioral_analysis_json,
        inputs.i9_recon_json,
        inputs.i9_taxonomy_json,
        inputs.i9_risk_matrix_json,
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise RuntimeError("missing required inputs:\n- " + "\n- ".join(missing))


def _validate_parent_summary(parent_summary: dict[str, Any]) -> None:
    iteration = str(parent_summary.get("policy", {}).get("targeted_recovery") or "")
    # i8 summary doesn't expose iteration name directly, so validate essential invariants instead.
    if int(parent_summary.get("policy", {}).get("train_rows", 0)) != 2129:
        raise RuntimeError("unexpected i8 parent train row count; expected 2129")
    if int(parent_summary.get("policy", {}).get("val_rows", 0)) != 240:
        raise RuntimeError("unexpected i8 parent val row count; expected 240")
    if not bool(parent_summary.get("policy", {}).get("localized_intervention_only", False)):
        raise RuntimeError("parent summary must preserve localized intervention doctrine")
    _ = iteration


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
    targets = {_assistant_target_canon(r) for r in candidate_rows}
    cases = {_source_case_id(r, "") for r in candidate_rows}

    out: dict[str, dict[str, int]] = {}
    for split, rows in eval_map.items():
        eval_prompts = {_user_prompt(r) for r in rows}
        eval_targets = {_assistant_target_canon(r) for r in rows}
        eval_cases = {_source_case_id(r, f"{split}_unknown") for r in rows}
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


def _build_failure_signature_catalog(comparison_rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    out: dict[tuple[str, str], dict[str, Any]] = {}
    for obj in comparison_rows:
        adapter = obj.get("adapter") if isinstance(obj.get("adapter"), dict) else {}
        if not bool(adapter.get("expected_tool", False)):
            continue
        expected_tools = adapter.get("expected_tool_names")
        if not isinstance(expected_tools, list) or not expected_tools:
            continue
        tool = str(expected_tools[0] or "").strip()
        if tool not in TARGETED_TOOLS:
            continue

        ev = adapter.get("eval") if isinstance(adapter.get("eval"), dict) else {}
        exact = bool(ev.get("exact_valid", False))
        if exact:
            continue

        prompt = str(adapter.get("user_prompt") or "")
        sk = _skeleton_id(prompt)
        schema_reason = str(ev.get("schema_reason") or "unknown")
        behavior = _behavior_from_eval(schema_reason, str(ev.get("generated_text") or ""))
        family = _family_from_behavior_and_prompt(behavior, prompt)

        key = (tool, sk)
        bucket = out.setdefault(
            key,
            {
                "tool": tool,
                "skeleton_id": sk,
                "rows": 0,
                "schema_reason_counts": Counter(),
                "behavior_counts": Counter(),
                "family_counts": Counter(),
            },
        )
        bucket["rows"] += 1
        bucket["schema_reason_counts"][schema_reason] += 1
        bucket["behavior_counts"][behavior] += 1
        bucket["family_counts"][family] += 1

    finalized: dict[tuple[str, str], dict[str, Any]] = {}
    for key, bucket in out.items():
        behavior_counts = bucket["behavior_counts"]
        schema_counts = bucket["schema_reason_counts"]
        family_counts = bucket["family_counts"]
        dominant_behavior = sorted(behavior_counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        dominant_schema = sorted(schema_counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        dominant_family = sorted(family_counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        finalized[key] = {
            "tool": bucket["tool"],
            "skeleton_id": bucket["skeleton_id"],
            "rows": int(bucket["rows"]),
            "dominant_behavior": dominant_behavior,
            "dominant_schema_reason": dominant_schema,
            "dominant_family": dominant_family,
            "schema_reason_counts": dict(sorted(schema_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
            "behavior_counts": dict(sorted(behavior_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
            "family_counts": dict(sorted(family_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        }
    return finalized


def _prompt_maps(rows: list[dict[str, Any]]) -> tuple[dict[str, set[str]], dict[str, set[str]], dict[tuple[str, str], set[str]]]:
    prompt_to_targets: dict[str, set[str]] = defaultdict(set)
    prompt_to_tools: dict[str, set[str]] = defaultdict(set)
    prompt_tool_to_args: dict[tuple[str, str], set[str]] = defaultdict(set)

    for row in rows:
        prompt = _user_prompt(row)
        tool = _tool_name(row)
        target = _assistant_target_canon(row)
        args = _assistant_args_canon(row)
        prompt_to_targets[prompt].add(target)
        prompt_to_tools[prompt].add(tool)
        prompt_tool_to_args[(prompt, tool)].add(args)
    return prompt_to_targets, prompt_to_tools, prompt_tool_to_args


def _can_register_prompt(
    prompt: str,
    tool: str,
    target: str,
    args: str,
    prompt_to_targets: dict[str, set[str]],
    prompt_to_tools: dict[str, set[str]],
    prompt_tool_to_args: dict[tuple[str, str], set[str]],
) -> bool:
    targets = prompt_to_targets.get(prompt)
    if targets and target not in targets:
        return False
    tools = prompt_to_tools.get(prompt)
    if tools and tool not in tools:
        return False
    args_set = prompt_tool_to_args.get((prompt, tool))
    if args_set and args not in args_set:
        return False
    return True


def _register_prompt(
    prompt: str,
    tool: str,
    target: str,
    args: str,
    prompt_to_targets: dict[str, set[str]],
    prompt_to_tools: dict[str, set[str]],
    prompt_tool_to_args: dict[tuple[str, str], set[str]],
) -> None:
    prompt_to_targets[prompt].add(target)
    prompt_to_tools[prompt].add(tool)
    prompt_tool_to_args[(prompt, tool)].add(args)


def _family_cues(family: str) -> tuple[str, ...]:
    if family == PRIMARY_FAMILY:
        return NEAR_MISS_CUES
    if family == SECONDARY_FAMILY:
        return SEMANTIC_CONVERSION_CUES
    if family == TERTIARY_FAMILY:
        return UNCERTAINTY_FALLBACK_CUES
    raise RuntimeError(f"unknown family: {family}")


def _variant_candidates(prompt: str, *, family: str, case_id: str, seed: int) -> list[tuple[str, str]]:
    cues = list(_family_cues(family))
    if not cues:
        return []

    rotate = _stable_int(f"{case_id}|{family}|{seed}") % len(cues)
    ordered = cues[rotate:] + cues[:rotate]

    out: list[tuple[str, str]] = []
    base = _strip_i8_tail(prompt).strip() or prompt.strip()
    for cue in ordered:
        cue_tag = _sha1_text(cue)
        out.append((f"{base} {cue}".strip(), f"append_{cue_tag}"))
        out.append((f"{cue} {base}".strip(), f"prepend_{cue_tag}"))
        if base.endswith("?"):
            out.append((f"{base} {cue}".strip(), f"append_q_{cue_tag}"))
    return out


def _select_candidates(
    rows: list[dict[str, Any]],
    *,
    split: str,
    signature_map: dict[tuple[str, str], dict[str, Any]],
    quotas: dict[str, int],
    seed: int,
    prompt_to_targets: dict[str, set[str]],
    prompt_to_tools: dict[str, set[str]],
    prompt_tool_to_args: dict[tuple[str, str], set[str]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    pool_by_family: dict[str, list[Candidate]] = {k: [] for k in quotas}

    for idx, row in enumerate(rows, start=1):
        tool = _tool_name(row)
        if tool not in TARGETED_TOOLS:
            continue

        prompt = _user_prompt(row)
        sk = _skeleton_id(prompt)
        signature = signature_map.get((tool, sk))
        if signature is None:
            continue

        family = str(signature.get("dominant_family") or SECONDARY_FAMILY)
        if family not in quotas:
            continue

        case_id = _source_case_id(row, f"{split}_{idx:06d}")
        pool_by_family[family].append(
            Candidate(
                split=split,
                row_index_1based=idx,
                source_case_id=case_id,
                tool=tool,
                source_prompt=prompt,
                source_target=_assistant_target_canon(row),
                source_args_canon=_assistant_args_canon(row),
                skeleton_id=sk,
                source_schema_reason=str(signature.get("dominant_schema_reason") or "unknown"),
                source_behavior=str(signature.get("dominant_behavior") or "unknown"),
                source_family=family,
                source_exact_valid=False,
            )
        )

    selected_rows: list[dict[str, Any]] = []
    selected_stats = {
        "quotas": quotas,
        "pool_sizes": {k: len(v) for k, v in pool_by_family.items()},
        "selected_by_family": Counter(),
        "selected_by_tool": Counter(),
        "selected_by_behavior": Counter(),
        "selected_by_transform_mode": Counter(),
        "selected_by_anchor_bucket": Counter(),
        "skipped_due_conflict": 0,
        "skipped_due_diversity_caps": 0,
        "families_not_filled": [],
    }

    per_skeleton = Counter()
    per_case = Counter()
    per_base_prompt = Counter()

    for family, need in quotas.items():
        pool = sorted(
            pool_by_family[family],
            key=lambda c: (_stable_int(f"{c.split}|{c.row_index_1based}|{family}|{seed}"), c.row_index_1based),
        )

        chosen = 0
        for cand in pool:
            if chosen >= need:
                break
            if per_skeleton[cand.skeleton_id] >= MAX_PER_SKELETON:
                selected_stats["skipped_due_diversity_caps"] += 1
                continue
            if per_case[cand.source_case_id] >= MAX_PER_SOURCE_CASE:
                selected_stats["skipped_due_diversity_caps"] += 1
                continue
            if per_base_prompt[cand.source_prompt] >= MAX_PER_BASE_PROMPT:
                selected_stats["skipped_due_diversity_caps"] += 1
                continue

            src = rows[cand.row_index_1based - 1]
            row = json.loads(json.dumps(src, ensure_ascii=False))

            picked_prompt = None
            picked_mode = None
            for transformed, mode in _variant_candidates(
                cand.source_prompt,
                family=family,
                case_id=f"{cand.source_case_id}|{cand.row_index_1based}",
                seed=seed,
            ):
                if transformed == cand.source_prompt:
                    continue
                if not _can_register_prompt(
                    transformed,
                    cand.tool,
                    cand.source_target,
                    cand.source_args_canon,
                    prompt_to_targets,
                    prompt_to_tools,
                    prompt_tool_to_args,
                ):
                    continue
                picked_prompt = transformed
                picked_mode = mode
                break

            if picked_prompt is None:
                selected_stats["skipped_due_conflict"] += 1
                continue

            _set_user_prompt(row, picked_prompt)

            meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
            conversion_id = f"i9c_{_sha1_text(f'{cand.split}|{cand.row_index_1based}|{cand.source_case_id}|{family}|{picked_mode}') }"
            family_short = {
                PRIMARY_FAMILY: "nmr",
                SECONDARY_FAMILY: "ssc",
                TERTIARY_FAMILY: "ucf",
            }[family]

            meta["source"] = "i9_commitment_conversion_from_i8"
            meta["synthetic"] = True
            meta["stage_split"] = "B_RECOVERY_I9"
            meta["recovery_batch"] = split
            meta["intervention_scope"] = "i9_hybrid_localized_commitment_conversion"
            meta["intervention_objective"] = "canonical_commitment_conversion_without_coercive_collapse"
            meta["intervention_targeted_family"] = True
            meta["intervention_forbidden_global_pressure"] = False
            meta["intervention_i9_row"] = True
            meta["intervention_i9_family"] = family
            meta["intervention_i9_behavior_source"] = cand.source_behavior
            meta["intervention_i9_source_schema_reason"] = cand.source_schema_reason
            meta["intervention_i9_source_exact_valid"] = bool(cand.source_exact_valid)
            meta["intervention_i9_conversion_id"] = conversion_id
            meta["intervention_i9_parent_case_id"] = cand.source_case_id
            meta["intervention_i9_parent_prompt_sha1"] = _sha1_text(cand.source_prompt)
            meta["intervention_i9_prompt_transform_mode"] = picked_mode
            meta["intervention_i9_prompt_changed"] = True
            meta["intervention_i9_failure_skeleton_id"] = cand.skeleton_id
            meta["intervention_i9_anchor_bucket"] = _prompt_anchor_bucket(picked_prompt)
            meta["intervention_i9_lineage_tag"] = "derived_from_i8_failure_signature"
            meta["source_case_id"] = f"i9_conv_{family_short}_{cand.source_case_id}"
            row["metadata"] = meta

            _register_prompt(
                picked_prompt,
                cand.tool,
                cand.source_target,
                cand.source_args_canon,
                prompt_to_targets,
                prompt_to_tools,
                prompt_tool_to_args,
            )

            per_skeleton[cand.skeleton_id] += 1
            per_case[cand.source_case_id] += 1
            per_base_prompt[cand.source_prompt] += 1

            selected_rows.append(row)
            selected_stats["selected_by_family"][family] += 1
            selected_stats["selected_by_tool"][cand.tool] += 1
            selected_stats["selected_by_behavior"][cand.source_behavior] += 1
            selected_stats["selected_by_transform_mode"][picked_mode] += 1
            selected_stats["selected_by_anchor_bucket"][_prompt_anchor_bucket(picked_prompt)] += 1
            chosen += 1

        if chosen != need:
            selected_stats["families_not_filled"].append(
                {"family": family, "required": need, "selected": chosen, "pool": len(pool)}
            )

    if selected_stats["families_not_filled"]:
        raise RuntimeError(
            "failed to satisfy i9 quotas exactly: "
            + json.dumps(selected_stats["families_not_filled"], ensure_ascii=False)
        )

    # Convert counters to plain dicts for JSON outputs.
    selected_stats["selected_by_family"] = dict(
        sorted(selected_stats["selected_by_family"].items(), key=lambda kv: (-kv[1], kv[0]))
    )
    selected_stats["selected_by_tool"] = dict(
        sorted(selected_stats["selected_by_tool"].items(), key=lambda kv: (-kv[1], kv[0]))
    )
    selected_stats["selected_by_behavior"] = dict(
        sorted(selected_stats["selected_by_behavior"].items(), key=lambda kv: (-kv[1], kv[0]))
    )
    selected_stats["selected_by_transform_mode"] = dict(
        sorted(selected_stats["selected_by_transform_mode"].items(), key=lambda kv: (-kv[1], kv[0]))
    )
    selected_stats["selected_by_anchor_bucket"] = dict(
        sorted(selected_stats["selected_by_anchor_bucket"].items(), key=lambda kv: (-kv[1], kv[0]))
    )

    return selected_rows, selected_stats


def _build_prompt_ambiguity_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    annotations = build_intervention_annotations(rows, targeted_tools=TARGETED_TOOLS)
    audit = run_prompt_ambiguity_audit(annotations)
    audit["generated_utc"] = _now_utc()
    audit["iteration"] = RUN_NAME
    return audit


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


def _run_diagnostics(
    candidate_train: list[dict[str, Any]],
    candidate_val: list[dict[str, Any]],
    reference_train: list[dict[str, Any]],
    reference_val: list[dict[str, Any]],
    i8_behavioral_analysis: dict[str, Any],
) -> dict[str, Any]:
    policy = scaffold_policy_defaults()
    return build_full_diagnostics_report(
        candidate_train + candidate_val,
        reference_rows=reference_train + reference_val,
        policy=policy,
        i8_behavioral_analysis=i8_behavioral_analysis,
    )


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

    commit = diagnostics.get("checks", {}).get("commitment_conversion_telemetry", {})
    top1 = float(commit.get("top1_behavioral_category_share", {}).get("top1_behavioral_category_share", 0.0) or 0.0)
    if top1 > MAX_TOP1_FAMILY_SHARE:
        raise RuntimeError(
            "behavioral monoculture doctrine violation: "
            f"top1_behavioral_category_share={top1} threshold={MAX_TOP1_FAMILY_SHARE}"
        )

    anchor_ratio = float(commit.get("anchor_dominance_ratio", {}).get("ratio", 0.0) or 0.0)
    if anchor_ratio > MAX_LITERAL_ANCHOR_SHARE:
        raise RuntimeError(
            "anchor dominance doctrine violation: "
            f"ratio={anchor_ratio} threshold={MAX_LITERAL_ANCHOR_SHARE}"
        )


def _build_contamination_audit(
    candidate_train: list[dict[str, Any]],
    candidate_val: list[dict[str, Any]],
    eval_map: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    train_overlap = _overlap_report(candidate_train, eval_map)
    val_overlap = _overlap_report(candidate_val, eval_map)
    combined_overlap = _overlap_report(candidate_train + candidate_val, eval_map)

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
            "approved_to_run": False,
            "approved_to_promote": False,
        },
    }


def _build_review_package(diagnostics: dict[str, Any], selection: dict[str, Any]) -> dict[str, Any]:
    commit = diagnostics.get("checks", {}).get("commitment_conversion_telemetry", {})
    return {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "iteration": RUN_NAME,
        "status": "completed",
        "question": "Are canonical-commitment gains likely generalized, or just lexical/template coercion?",
        "conversion_selection_summary": selection,
        "targeted_prompt_samples": diagnostics.get("review_support", {}).get("targeted_prompt_samples", {}),
        "commitment_conversion_telemetry": commit,
        "risk_flags": {
            "diversity": diagnostics.get("review_support", {}).get("diversity_review_summary", {}),
            "anti_homogenization": diagnostics.get("review_support", {}).get("anti_homogenization_summary", {}),
            "behavioral_monoculture": commit.get("behavioral_monoculture_detection", {}),
            "anchor_dominance": commit.get("anchor_dominance_ratio", {}),
        },
        "interpretation_guidance": [
            "If top1 behavioral source share exceeds 0.70, treat as local conversion monoculture risk.",
            "If literal anchor dominance rises above threshold, treat as brittle token-trigger overfitting risk.",
            "If ambiguity hard blocks are non-zero, invalidate candidate package before training review.",
            "If scalar substitution rebound rises in post-eval, halt and reassess intervention pressure.",
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
    parent_train_rows: int,
    parent_val_rows: int,
    candidate_train: list[dict[str, Any]],
    candidate_val: list[dict[str, Any]],
    selection_stats: dict[str, Any],
    diagnostics: dict[str, Any],
    prompt_ambiguity_audit: dict[str, Any],
    contamination_audit: dict[str, Any],
) -> dict[str, Any]:
    train_overlap = contamination_audit["train_overlap"]
    val_overlap = contamination_audit["val_overlap"]

    added_train = len(candidate_train) - parent_train_rows
    added_val = len(candidate_val) - parent_val_rows

    return {
        "generated_utc": _now_utc(),
        "seed": seed,
        "iteration": RUN_NAME,
        "lineage": {
            "parent_dataset_iteration": PARENT_DATASET_ITERATION,
            "parent_checkpoint": PARENT_CHECKPOINT,
            "objective": "commitment_conversion_behavior_repair",
            "targeted_tools": list(TARGETED_TOOLS),
        },
        "inputs": {
            "parent_train_jsonl": str(inputs.parent_train_jsonl),
            "parent_val_jsonl": str(inputs.parent_val_jsonl),
            "parent_summary_json": str(inputs.parent_summary_json),
            "eval_comparison_rows_jsonl": str(inputs.eval_comparison_rows_jsonl),
            "i8_behavioral_analysis_json": str(inputs.i8_behavioral_analysis_json),
            "i9_recon_json": str(inputs.i9_recon_json),
            "i9_taxonomy_json": str(inputs.i9_taxonomy_json),
            "i9_risk_matrix_json": str(inputs.i9_risk_matrix_json),
        },
        "policy": {
            "localized_intervention_only": True,
            "forbidden_global_pressures": list(FORBIDDEN_GLOBAL_PRESSURES),
            "global_eval_semantics_modified": False,
            "approval_gates_opened": False,
            "approved_to_run": False,
        },
        "composition": {
            "parent_train_rows": parent_train_rows,
            "parent_val_rows": parent_val_rows,
            "candidate_train_rows": len(candidate_train),
            "candidate_val_rows": len(candidate_val),
            "rows_added_train": added_train,
            "rows_added_val": added_val,
            "rows_added_total": added_train + added_val,
        },
        "intervention_selection": selection_stats,
        "overlap_audit": {
            "train": train_overlap,
            "val": val_overlap,
            "combined": contamination_audit["combined_overlap"],
        },
        "diagnostics_highlights": {
            "diversity_review_summary": diagnostics.get("review_support", {}).get("diversity_review_summary", {}),
            "anti_homogenization_summary": diagnostics.get("review_support", {}).get("anti_homogenization_summary", {}),
            "commitment_conversion_telemetry": diagnostics.get("checks", {}).get("commitment_conversion_telemetry", {}),
            "prompt_ambiguity_hard_blocks": prompt_ambiguity_audit.get("hard_block_candidates", {}),
        },
        "outputs": {
            "train_jsonl": str(outputs.train_jsonl),
            "val_jsonl": str(outputs.val_jsonl),
            "summary_json": str(outputs.summary_json),
            "diagnostics_json": str(outputs.diagnostics_json),
            "contamination_audit_json": str(outputs.contamination_audit_json),
            "prompt_ambiguity_audit_json": str(outputs.prompt_ambiguity_audit_json),
            "collapse_watch_telemetry_json": str(outputs.collapse_watch_telemetry_json),
            "anchor_dominance_telemetry_json": str(outputs.anchor_dominance_telemetry_json),
            "review_package_json": str(outputs.review_package_json),
        },
        "hashes": {
            "train_sha256": _sha256_file(outputs.train_jsonl),
            "val_sha256": _sha256_file(outputs.val_jsonl),
        },
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_promote": False,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Stage B i9 candidate dataset package.")
    parser.add_argument(
        "--parent-train-jsonl",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i8_train.jsonl",
    )
    parser.add_argument(
        "--parent-val-jsonl",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i8_val.jsonl",
    )
    parser.add_argument(
        "--parent-summary-json",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i8_summary.json",
    )

    parser.add_argument("--eval-heldout-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/heldout_validation.jsonl")
    parser.add_argument("--eval-tool-holdout-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/tool_holdout.jsonl")
    parser.add_argument("--eval-no-call-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/no_call.jsonl")
    parser.add_argument("--eval-adversarial-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/adversarial.jsonl")
    parser.add_argument("--eval-direct-answer-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/direct_answer.jsonl")
    parser.add_argument(
        "--eval-comparison-rows-jsonl",
        default="/opt/ai-stack/assistant-training/evals/runs/canonical_eval_20260526T172855Z/comparison_rows.jsonl",
    )

    parser.add_argument(
        "--i8-behavioral-analysis-json",
        default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i8_parseability_behavioral_analysis.json",
    )
    parser.add_argument(
        "--i9-recon-json",
        default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i9_commitment_conversion_reconnaissance.json",
    )
    parser.add_argument(
        "--i9-taxonomy-json",
        default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i9_commitment_conversion_taxonomy.json",
    )
    parser.add_argument(
        "--i9-risk-matrix-json",
        default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i9_intervention_risk_matrix.json",
    )

    parser.add_argument("--output-root", default="/opt/ai-stack/assistant-training/data/v1_0")
    parser.add_argument("--report-root", default="/opt/ai-stack/assistant-training/manifests/reports")
    parser.add_argument("--seed", type=int, default=20260526)

    parser.add_argument("--enable-dataset-emission", action="store_true")
    parser.add_argument("--allow-generation-phase", action="store_true")
    parser.add_argument("--enable-i9-commitment-conversion", action="store_true")

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    _fail_fast_unlock(args)

    inputs = _resolve_inputs(args)
    outputs = _resolve_outputs(args)
    _fail_fast_inputs(inputs)

    parent_train = _load_jsonl(inputs.parent_train_jsonl)
    parent_val = _load_jsonl(inputs.parent_val_jsonl)
    parent_summary = _load_json(inputs.parent_summary_json)
    _validate_parent_summary(parent_summary)

    i8_behavioral_analysis = _load_json(inputs.i8_behavioral_analysis_json)
    _ = _load_json(inputs.i9_recon_json)
    _ = _load_json(inputs.i9_taxonomy_json)
    _ = _load_json(inputs.i9_risk_matrix_json)

    comparison_rows = _load_jsonl(inputs.eval_comparison_rows_jsonl)
    signature_map = _build_failure_signature_catalog(comparison_rows)
    if not signature_map:
        raise RuntimeError("empty failure signature catalog from i8 comparison rows")

    candidate_train = json.loads(json.dumps(parent_train, ensure_ascii=False))
    candidate_val = json.loads(json.dumps(parent_val, ensure_ascii=False))

    prompt_to_targets, prompt_to_tools, prompt_tool_to_args = _prompt_maps(candidate_train + candidate_val)

    train_added, train_selection_stats = _select_candidates(
        candidate_train,
        split="train",
        signature_map=signature_map,
        quotas=TRAIN_QUOTAS,
        seed=int(args.seed),
        prompt_to_targets=prompt_to_targets,
        prompt_to_tools=prompt_to_tools,
        prompt_tool_to_args=prompt_tool_to_args,
    )
    val_added, val_selection_stats = _select_candidates(
        candidate_val,
        split="val",
        signature_map=signature_map,
        quotas=VAL_QUOTAS,
        seed=int(args.seed),
        prompt_to_targets=prompt_to_targets,
        prompt_to_tools=prompt_to_tools,
        prompt_tool_to_args=prompt_tool_to_args,
    )

    # Selection-only augmentation; base rows remain unchanged.
    candidate_train.extend(train_added)
    candidate_val.extend(val_added)

    selection_stats = {
        "train": train_selection_stats,
        "val": val_selection_stats,
        "added_rows_total": len(train_added) + len(val_added),
        "added_rows_train": len(train_added),
        "added_rows_val": len(val_added),
    }

    transform_mode_counts = Counter()
    for part in (train_selection_stats, val_selection_stats):
        for mode, count in part.get("selected_by_transform_mode", {}).items():
            transform_mode_counts[mode] += int(count)
    if transform_mode_counts:
        top_mode_share = max(transform_mode_counts.values()) / max(sum(transform_mode_counts.values()), 1)
        if top_mode_share > MAX_PER_TRANSFORM_MODE_SHARE:
            raise RuntimeError(
                "intervention transform-mode concentration exceeded threshold: "
                f"top_mode_share={top_mode_share:.6f} threshold={MAX_PER_TRANSFORM_MODE_SHARE}"
            )

    prompt_ambiguity_audit = _build_prompt_ambiguity_audit(candidate_train + candidate_val)
    _fail_fast_prompt_ambiguity_hard_blocks(prompt_ambiguity_audit, scope="candidate_dataset")

    eval_map = _collect_eval_map(inputs)
    train_overlap = _overlap_report(candidate_train, eval_map)
    val_overlap = _overlap_report(candidate_val, eval_map)
    _fail_fast_overlap_guard(train_overlap, scope="train")
    _fail_fast_overlap_guard(val_overlap, scope="val")

    diagnostics = _run_diagnostics(
        candidate_train,
        candidate_val,
        parent_train,
        parent_val,
        i8_behavioral_analysis=i8_behavioral_analysis,
    )
    _fail_fast_diagnostic_doctrine(diagnostics)

    contamination_audit = _build_contamination_audit(candidate_train, candidate_val, eval_map)
    review_package = _build_review_package(diagnostics, selection_stats)

    collapse_watch = diagnostics.get("checks", {}).get("commitment_conversion_telemetry", {}).get("collapse_watch_conditions", {})
    anchor_dominance = diagnostics.get("checks", {}).get("commitment_conversion_telemetry", {}).get("anchor_dominance_ratio", {})

    _write_jsonl(outputs.train_jsonl, candidate_train)
    _write_jsonl(outputs.val_jsonl, candidate_val)
    _write_json(outputs.diagnostics_json, diagnostics)
    _write_json(outputs.contamination_audit_json, contamination_audit)
    _write_json(outputs.prompt_ambiguity_audit_json, prompt_ambiguity_audit)
    _write_json(outputs.collapse_watch_telemetry_json, collapse_watch)
    _write_json(outputs.anchor_dominance_telemetry_json, anchor_dominance)
    _write_json(outputs.review_package_json, review_package)

    summary = _build_summary(
        inputs=inputs,
        outputs=outputs,
        seed=int(args.seed),
        parent_train_rows=len(parent_train),
        parent_val_rows=len(parent_val),
        candidate_train=candidate_train,
        candidate_val=candidate_val,
        selection_stats=selection_stats,
        diagnostics=diagnostics,
        prompt_ambiguity_audit=prompt_ambiguity_audit,
        contamination_audit=contamination_audit,
    )
    _write_json(outputs.summary_json, summary)

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
