#!/usr/bin/env python3
"""
Build Stage B i10 candidate dataset package.

Governance boundaries:
- Explicit unlock flags are required for dataset emission.
- No training, no canonical eval, no gate opening.
- Intervention is localized to semantic/scalar substitution conversion families.
- Ambiguity, contamination, and anti-homogenization invariants are fail-fast.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from i10_diagnostics_scaffold import (
    build_full_diagnostics_report,
    build_intervention_annotations,
    run_prompt_ambiguity_audit,
    scaffold_policy_defaults,
)

RUN_NAME = "stage_b_llama31_8b_base_v1_i10"
PARENT_DATASET_ITERATION = "stage_b_llama31_8b_base_v1_i9"
PARENT_CHECKPOINT = "stage_b_llama31_8b_base_v1_i9"
TARGETED_TOOLS = ("read_file", "rg_search")

PRIMARY_FAMILY = "semantic_substitution_conversion_pairs_read_file_primary"
SECONDARY_FAMILY = "semantic_substitution_conversion_pairs_rg_search_scalar_secondary"
TERTIARY_FAMILY = "uncertainty_conditioned_procedural_continuation_smallscale"

TRAIN_QUOTAS = {
    PRIMARY_FAMILY: 52,
    SECONDARY_FAMILY: 28,
    TERTIARY_FAMILY: 8,
}
VAL_QUOTAS = {
    PRIMARY_FAMILY: 8,
    SECONDARY_FAMILY: 4,
    TERTIARY_FAMILY: 2,
}

PRIMARY_ARCHETYPE_MIN_TRAIN = {
    "read_file_boolean_presence": 12,
    "read_file_symbol_name": 12,
    "read_file_first_function_name": 8,
}
PRIMARY_ARCHETYPE_MIN_VAL = {
    "read_file_boolean_presence": 2,
    "read_file_symbol_name": 2,
    "read_file_first_function_name": 2,
}

FORBIDDEN_GLOBAL_PRESSURES = (
    "global_coercive_schema_policing",
    "global_negation_heavy_template_pressure",
    "blacklist_flooding",
    "imperative_monoculture",
    "broad_synthetic_flooding",
)

READ_FILE_SEMANTIC_CONVERSION_CUES = (
    "Return one structured retrieval-call payload before any result text.",
    "Provide the canonical read_file invocation payload needed to gather evidence.",
    "Respond with the procedural file-read call object for this task.",
    "Emit exactly one parseable call payload that retrieves the requested file range.",
    "Output one JSON payload containing the retrieval call in tool_calls.",
    "Return the evidence-acquisition call payload instead of extracted answer text.",
    "Produce a single canonical call envelope for reading the requested span.",
    "Commit to the retrieval procedure payload first and stop after that payload.",
)

RG_SEARCH_SCALAR_CONVERSION_CUES = (
    "Return the canonical rg_search invocation payload before any scalar result.",
    "Provide one structured search-call payload to collect count evidence.",
    "Emit a single parseable call payload that performs the search.",
    "Output one JSON payload with the rg_search call in tool_calls.",
    "Respond with the retrieval procedure payload rather than numeric shortcut output.",
    "Commit to the search invocation payload first and stop after that payload.",
)

UNCERTAINTY_PROCEDURAL_CONTINUATION_CUES = (
    "If uncertainty remains, continue procedurally by emitting the retrieval call payload.",
    "When unsure, prefer the canonical evidence-gathering call payload.",
    "Under uncertainty, provide one structured call payload to gather evidence.",
    "If confidence is low, emit the procedural call envelope first.",
)

# Upper bounds prevent local-template collapse and concentration spikes.
MAX_PER_SKELETON = 4
MAX_PER_SOURCE_CASE = 11
MAX_PER_BASE_PROMPT = 2
MAX_PER_TRANSFORM_MODE_SHARE = 0.40
MAX_LITERAL_ANCHOR_SHARE = 0.55
MAX_TOP1_BEHAVIOR_SHARE = 0.70
MAX_TOP_PROMPT_SHELL_SHARE = 0.25
MAX_PRIMARY_ARCHETYPE_SHARE = 0.55


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
    i9_behavioral_review_json: Path
    i10_recon_json: Path
    i10_taxonomy_json: Path
    i10_risk_matrix_json: Path
    i10_candidate_patterns_json: Path


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
    scalar_substitution_rebound_telemetry_json: Path
    review_package_json: Path
    review_package_md: Path


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
    source_archetype: str
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


def _strip_prior_tail(prompt: str) -> str:
    pats = [
        r"\s*return strict json tool_calls only\.?$",
        r"\s*return strict json only\.?$",
        r"\s*respond with exactly one parseable json object containing tool_calls\.?$",
        r"\s*return one valid json object with top-level key tool_calls\.?$",
        r"\s*output one strict json object only, with top-level key tool_calls\.?$",
        r"\s*produce only json: a single object whose top-level key is tool_calls\.?$",
        r"\s*emit a single parseable json object; top-level key must be tool_calls\.?$",
        r"\s*disambiguation:\s*call\s+[^.]+\.$",
        r"\s*emit one canonical tool-invocation payload object\.?$",
        r"\s*return exactly one structured function-call envelope\.?$",
        r"\s*output a single parseable call payload for this request\.?$",
        r"\s*respond with one canonical tool call payload only\.?$",
        r"\s*first return the tool invocation payload instead of result content\.?$",
        r"\s*provide the acquisition call payload before any result text\.?$",
        r"\s*return only the structured tool invocation needed to gather evidence\.?$",
        r"\s*commit to the canonical retrieval call payload, not direct result prose\.?$",
        r"\s*if unsure about the result, return the canonical retrieval call payload\.?$",
        r"\s*when uncertain, commit to the tool invocation payload for evidence gathering\.?$",
        r"\s*under uncertainty, emit the structured tool call payload first\.?$",
        r"\s*return one structured retrieval-call payload before any result text\.?$",
        r"\s*provide the canonical read_file invocation payload needed to gather evidence\.?$",
        r"\s*respond with the procedural file-read call object for this task\.?$",
        r"\s*emit exactly one parseable call payload that retrieves the requested file range\.?$",
        r"\s*output one json payload containing the retrieval call in tool_calls\.?$",
        r"\s*return the evidence-acquisition call payload instead of extracted answer text\.?$",
        r"\s*produce a single canonical call envelope for reading the requested span\.?$",
        r"\s*commit to the retrieval procedure payload first and stop after that payload\.?$",
        r"\s*return the canonical rg_search invocation payload before any scalar result\.?$",
        r"\s*provide one structured search-call payload to collect count evidence\.?$",
        r"\s*emit a single parseable call payload that performs the search\.?$",
        r"\s*output one json payload with the rg_search call in tool_calls\.?$",
        r"\s*respond with the retrieval procedure payload rather than numeric shortcut output\.?$",
        r"\s*commit to the search invocation payload first and stop after that payload\.?$",
        r"\s*if uncertainty remains, continue procedurally by emitting the retrieval call payload\.?$",
        r"\s*when unsure, prefer the canonical evidence-gathering call payload\.?$",
        r"\s*under uncertainty, provide one structured call payload to gather evidence\.?$",
        r"\s*if confidence is low, emit the procedural call envelope first\.?$",
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
    text = _strip_prior_tail(prompt).lower().strip()
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


def _is_number_token(text: str) -> bool:
    return bool(re.fullmatch(r"[-+]?\d+(\.\d+)?", text.strip()))


def _behavior_from_eval(schema_reason: str, parse_mode: str, generated_text: str) -> str:
    text = (generated_text or "").strip()
    low = text.lower()

    if schema_reason == "missing_tool_calls":
        return "partial_procedural_wrapper_or_envelope"

    if schema_reason == "payload_not_object":
        if _is_number_token(text) or low in {"true", "false", "null"}:
            return "scalar_substitution"
        return "nonobject_substitution"

    if schema_reason == "payload_not_parsed" or parse_mode == "invalid":
        if text.startswith("{") or text.startswith("["):
            return "partial_procedural_malformed_json"
        if _is_number_token(text) or low in {"true", "false", "null"}:
            return "scalar_substitution"
        if "/opt/" in text or "/mnt/" in text or "\n" in text:
            return "pseudo_completion_substitution"
        return "direct_answer_substitution"

    return "other"


def _query_archetype(prompt: str, tool: str) -> str:
    p = prompt.lower()
    if tool == "read_file":
        if "report whether" in p and "appears" in p:
            return "read_file_boolean_presence"
        if "first function name" in p:
            return "read_file_first_function_name"
        if "symbol name" in p:
            return "read_file_symbol_name"
        return "read_file_other"

    if tool == "rg_search":
        if "match_count" in p:
            return "rg_search_match_count"
        if "zero or non-zero" in p or "zero/nonzero" in p:
            return "rg_search_zero_nonzero"
        return "rg_search_other"

    return "non_targeted"


def _family_from_failure(tool: str, behavior: str, archetype: str) -> str:
    if tool == "read_file" and behavior in {
        "scalar_substitution",
        "direct_answer_substitution",
        "pseudo_completion_substitution",
    }:
        return PRIMARY_FAMILY

    if tool == "rg_search" and behavior == "scalar_substitution" and archetype in {
        "rg_search_match_count",
        "rg_search_zero_nonzero",
    }:
        return SECONDARY_FAMILY

    if tool == "rg_search" and behavior in {
        "scalar_substitution",
        "direct_answer_substitution",
        "pseudo_completion_substitution",
    }:
        return TERTIARY_FAMILY

    return "excluded"


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
        i9_behavioral_review_json=Path(args.i9_behavioral_review_json).resolve(),
        i10_recon_json=Path(args.i10_recon_json).resolve(),
        i10_taxonomy_json=Path(args.i10_taxonomy_json).resolve(),
        i10_risk_matrix_json=Path(args.i10_risk_matrix_json).resolve(),
        i10_candidate_patterns_json=Path(args.i10_candidate_patterns_json).resolve(),
    )


def _resolve_outputs(args: argparse.Namespace) -> OutputPaths:
    out_root = Path(args.output_root).resolve()
    report_root = Path(args.report_root).resolve()
    return OutputPaths(
        train_jsonl=out_root / "dataset_v1_0_stage_b_recovery_i10_train.jsonl",
        val_jsonl=out_root / "dataset_v1_0_stage_b_recovery_i10_val.jsonl",
        summary_json=out_root / "dataset_v1_0_stage_b_recovery_i10_summary.json",
        diagnostics_json=report_root / "stage_b_v1_i10_dataset_diagnostics.json",
        contamination_audit_json=report_root / "stage_b_v1_i10_contamination_audit.json",
        prompt_ambiguity_audit_json=report_root / "stage_b_v1_i10_prompt_ambiguity_audit.json",
        collapse_watch_telemetry_json=report_root / "stage_b_v1_i10_collapse_watch_telemetry.json",
        anchor_dominance_telemetry_json=report_root / "stage_b_v1_i10_anchor_dominance_telemetry.json",
        scalar_substitution_rebound_telemetry_json=report_root / "stage_b_v1_i10_scalar_substitution_rebound_telemetry.json",
        review_package_json=report_root / "stage_b_v1_i10_human_review_package.json",
        review_package_md=report_root / "stage_b_v1_i10_human_review_package.md",
    )


def _fail_fast_unlock(args: argparse.Namespace) -> None:
    if not args.enable_dataset_emission:
        raise RuntimeError("dataset emission requires explicit --enable-dataset-emission")
    if not args.allow_generation_phase:
        raise RuntimeError("dataset emission requires explicit --allow-generation-phase")
    if not args.enable_i10_semantic_commitment:
        raise RuntimeError("i10 generation requires explicit --enable-i10-semantic-commitment")


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
        inputs.i9_behavioral_review_json,
        inputs.i10_recon_json,
        inputs.i10_taxonomy_json,
        inputs.i10_risk_matrix_json,
        inputs.i10_candidate_patterns_json,
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise RuntimeError("missing required inputs:\n- " + "\n- ".join(missing))


def _validate_parent_summary(parent_summary: dict[str, Any]) -> None:
    if parent_summary.get("iteration") != "stage_b_llama31_8b_base_v1_i9":
        raise RuntimeError("unexpected parent summary iteration; expected stage_b_llama31_8b_base_v1_i9")
    if int(parent_summary.get("composition", {}).get("candidate_train_rows", 0)) != 2217:
        raise RuntimeError("unexpected i9 parent train row count; expected 2217")
    if int(parent_summary.get("composition", {}).get("candidate_val_rows", 0)) != 254:
        raise RuntimeError("unexpected i9 parent val row count; expected 254")
    if bool(parent_summary.get("policy", {}).get("approval_gates_opened", True)):
        raise RuntimeError("parent summary must have approval_gates_opened=false")


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
        ev = adapter.get("eval") if isinstance(adapter.get("eval"), dict) else {}

        expected_tool = bool(adapter.get("expected_tool", False) or ev.get("expected_tool", False))
        if not expected_tool:
            continue

        expected_tools = adapter.get("expected_tool_names")
        if not isinstance(expected_tools, list) or not expected_tools:
            continue
        tool = str(expected_tools[0] or "").strip()
        if tool not in TARGETED_TOOLS:
            continue

        exact = bool(ev.get("exact_valid", False))
        if exact:
            continue

        prompt = str(adapter.get("user_prompt") or "")
        sk = _skeleton_id(prompt)
        schema_reason = str(ev.get("schema_reason") or "unknown")
        parse_mode = str(ev.get("parse_mode") or "")
        behavior = _behavior_from_eval(schema_reason, parse_mode, str(ev.get("generated_text") or ""))
        archetype = _query_archetype(prompt, tool)
        family = _family_from_failure(tool, behavior, archetype)
        if family == "excluded":
            continue

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
                "archetype_counts": Counter(),
            },
        )
        bucket["rows"] += 1
        bucket["schema_reason_counts"][schema_reason] += 1
        bucket["behavior_counts"][behavior] += 1
        bucket["family_counts"][family] += 1
        bucket["archetype_counts"][archetype] += 1

    finalized: dict[tuple[str, str], dict[str, Any]] = {}
    for key, bucket in out.items():
        behavior_counts = bucket["behavior_counts"]
        schema_counts = bucket["schema_reason_counts"]
        family_counts = bucket["family_counts"]
        archetype_counts = bucket["archetype_counts"]

        dominant_behavior = sorted(behavior_counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        dominant_schema = sorted(schema_counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        dominant_family = sorted(family_counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        dominant_archetype = sorted(archetype_counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]

        finalized[key] = {
            "tool": bucket["tool"],
            "skeleton_id": bucket["skeleton_id"],
            "rows": int(bucket["rows"]),
            "dominant_behavior": dominant_behavior,
            "dominant_schema_reason": dominant_schema,
            "dominant_family": dominant_family,
            "dominant_archetype": dominant_archetype,
            "schema_reason_counts": dict(sorted(schema_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
            "behavior_counts": dict(sorted(behavior_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
            "family_counts": dict(sorted(family_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
            "archetype_counts": dict(sorted(archetype_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
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
        return READ_FILE_SEMANTIC_CONVERSION_CUES
    if family == SECONDARY_FAMILY:
        return RG_SEARCH_SCALAR_CONVERSION_CUES
    if family == TERTIARY_FAMILY:
        return UNCERTAINTY_PROCEDURAL_CONTINUATION_CUES
    raise RuntimeError(f"unknown family: {family}")


def _variant_candidates(
    prompt: str,
    *,
    family: str,
    case_id: str,
    seed: int,
) -> list[tuple[str, str]]:
    cues = list(_family_cues(family))
    if not cues:
        return []

    rotate = _stable_int(f"{case_id}|{family}|{seed}") % len(cues)
    ordered = cues[rotate:] + cues[:rotate]

    base = _strip_prior_tail(prompt).strip() or prompt.strip()
    out: list[tuple[str, str]] = []
    for cue in ordered:
        cue_tag = _sha1_text(cue)
        out.append((f"{base} {cue}".strip(), f"append_{cue_tag}"))
        out.append((f"{cue} {base}".strip(), f"prepend_{cue_tag}"))
        if base.endswith("?"):
            out.append((f"{base} {cue}".strip(), f"append_q_{cue_tag}"))
        else:
            out.append((f"{base} For this request, {cue[0].lower()}{cue[1:]}".strip(), f"bridge_{cue_tag}"))
    return out


def _select_candidates(
    rows: list[dict[str, Any]],
    *,
    split: str,
    signature_map: dict[tuple[str, str], dict[str, Any]],
    quotas: dict[str, int],
    primary_archetype_minimums: dict[str, int],
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

        family = str(signature.get("dominant_family") or "")
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
                source_archetype=str(signature.get("dominant_archetype") or "unknown"),
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
        "selected_by_archetype": Counter(),
        "selected_by_transform_mode": Counter(),
        "selected_by_anchor_bucket": Counter(),
        "skipped_due_conflict": 0,
        "skipped_due_diversity_caps": 0,
        "skipped_due_archetype_cap": 0,
        "families_not_filled": [],
        "primary_archetype_minimums": primary_archetype_minimums,
    }

    per_skeleton = Counter()
    per_case = Counter()
    per_base_prompt = Counter()
    per_primary_archetype = Counter()
    used_candidates: set[tuple[int, str, str]] = set()

    def try_select(cand: Candidate, *, family: str, need: int) -> tuple[bool, str]:
        nonlocal selected_rows
        candidate_key = (cand.row_index_1based, cand.source_case_id, family)
        if candidate_key in used_candidates:
            return False, "already_selected"

        if per_skeleton[cand.skeleton_id] >= MAX_PER_SKELETON:
            return False, "diversity_cap"
        if per_case[cand.source_case_id] >= MAX_PER_SOURCE_CASE:
            return False, "diversity_cap"
        if per_base_prompt[cand.source_prompt] >= MAX_PER_BASE_PROMPT:
            return False, "diversity_cap"

        if family == PRIMARY_FAMILY:
            max_for_arch = max(1, math.ceil(need * MAX_PRIMARY_ARCHETYPE_SHARE))
            if per_primary_archetype[cand.source_archetype] >= max_for_arch:
                return False, "archetype_cap"

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
            return False, "conflict"

        _set_user_prompt(row, picked_prompt)

        meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        conversion_id = f"i10c_{_sha1_text(f'{cand.split}|{cand.row_index_1based}|{cand.source_case_id}|{family}|{picked_mode}') }"
        family_short = {
            PRIMARY_FAMILY: "ssc_rf",
            SECONDARY_FAMILY: "ssc_rg",
            TERTIARY_FAMILY: "ucp",
        }[family]

        meta["source"] = "i10_semantic_commitment_conversion_from_i9"
        meta["synthetic"] = True
        meta["stage_split"] = "B_RECOVERY_I10"
        meta["recovery_batch"] = split
        meta["intervention_scope"] = "i10_hybrid_localized_semantic_commitment"
        meta["intervention_objective"] = "semantic_scalar_substitution_to_canonical_procedural_commitment"
        meta["intervention_targeted_family"] = True
        meta["intervention_forbidden_global_pressure"] = False
        meta["intervention_i10_row"] = True
        meta["intervention_i10_family"] = family
        meta["intervention_i10_behavior_source"] = cand.source_behavior
        meta["intervention_i10_query_archetype"] = cand.source_archetype
        meta["intervention_i10_source_schema_reason"] = cand.source_schema_reason
        meta["intervention_i10_source_exact_valid"] = bool(cand.source_exact_valid)
        meta["intervention_i10_conversion_id"] = conversion_id
        meta["intervention_i10_parent_case_id"] = cand.source_case_id
        meta["intervention_i10_parent_prompt_sha1"] = _sha1_text(cand.source_prompt)
        meta["intervention_i10_prompt_transform_mode"] = picked_mode
        meta["intervention_i10_prompt_changed"] = True
        meta["intervention_i10_failure_skeleton_id"] = cand.skeleton_id
        meta["intervention_i10_anchor_bucket"] = _prompt_anchor_bucket(picked_prompt)
        meta["intervention_i10_lineage_tag"] = "derived_from_i9_failure_signature"
        meta["source_case_id"] = f"i10_conv_{family_short}_{cand.source_case_id}"
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
        if family == PRIMARY_FAMILY:
            per_primary_archetype[cand.source_archetype] += 1
        used_candidates.add(candidate_key)

        selected_rows.append(row)
        selected_stats["selected_by_family"][family] += 1
        selected_stats["selected_by_tool"][cand.tool] += 1
        selected_stats["selected_by_behavior"][cand.source_behavior] += 1
        selected_stats["selected_by_archetype"][cand.source_archetype] += 1
        selected_stats["selected_by_transform_mode"][picked_mode] += 1
        selected_stats["selected_by_anchor_bucket"][_prompt_anchor_bucket(picked_prompt)] += 1
        return True, "selected"

    for family, need in quotas.items():
        pool = sorted(
            pool_by_family[family],
            key=lambda c: (_stable_int(f"{c.split}|{c.row_index_1based}|{family}|{seed}"), c.row_index_1based),
        )

        chosen = 0

        # Preserve read_file archetype spread in the primary family.
        if family == PRIMARY_FAMILY:
            for archetype, minimum in primary_archetype_minimums.items():
                if minimum <= 0:
                    continue
                for cand in pool:
                    if chosen >= need:
                        break
                    if cand.source_archetype != archetype:
                        continue
                    ok, reason = try_select(cand, family=family, need=need)
                    if not ok:
                        if reason == "diversity_cap":
                            selected_stats["skipped_due_diversity_caps"] += 1
                        elif reason == "archetype_cap":
                            selected_stats["skipped_due_archetype_cap"] += 1
                        else:
                            selected_stats["skipped_due_conflict"] += 1
                        continue
                    chosen += 1
                    if per_primary_archetype[archetype] >= minimum:
                        break

            for archetype, minimum in primary_archetype_minimums.items():
                if per_primary_archetype[archetype] < minimum:
                    raise RuntimeError(
                        "failed to satisfy primary archetype minimums: "
                        + json.dumps(
                            {
                                "split": split,
                                "archetype": archetype,
                                "required": minimum,
                                "selected": int(per_primary_archetype[archetype]),
                            },
                            ensure_ascii=False,
                        )
                    )

        for cand in pool:
            if chosen >= need:
                break
            ok, reason = try_select(cand, family=family, need=need)
            if not ok:
                if reason == "diversity_cap":
                    selected_stats["skipped_due_diversity_caps"] += 1
                elif reason == "archetype_cap":
                    selected_stats["skipped_due_archetype_cap"] += 1
                else:
                    selected_stats["skipped_due_conflict"] += 1
                continue
            chosen += 1

        if chosen != need:
            selected_stats["families_not_filled"].append(
                {"family": family, "required": need, "selected": chosen, "pool": len(pool)}
            )

    if selected_stats["families_not_filled"]:
        raise RuntimeError(
            "failed to satisfy i10 quotas exactly: "
            + json.dumps(selected_stats["families_not_filled"], ensure_ascii=False)
        )

    selected_stats["selected_by_family"] = dict(
        sorted(selected_stats["selected_by_family"].items(), key=lambda kv: (-kv[1], kv[0]))
    )
    selected_stats["selected_by_tool"] = dict(
        sorted(selected_stats["selected_by_tool"].items(), key=lambda kv: (-kv[1], kv[0]))
    )
    selected_stats["selected_by_behavior"] = dict(
        sorted(selected_stats["selected_by_behavior"].items(), key=lambda kv: (-kv[1], kv[0]))
    )
    selected_stats["selected_by_archetype"] = dict(
        sorted(selected_stats["selected_by_archetype"].items(), key=lambda kv: (-kv[1], kv[0]))
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
    i9_behavioral_report: dict[str, Any],
) -> dict[str, Any]:
    policy = scaffold_policy_defaults()
    return build_full_diagnostics_report(
        candidate_train + candidate_val,
        reference_rows=reference_train + reference_val,
        policy=policy,
        i9_behavioral_report=i9_behavioral_report,
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
    if any(
        bool(hard.get(k, False))
        for k in ("prompt_to_multiple_targets", "prompt_to_multiple_tools", "prompt_tool_to_multiple_arguments")
    ):
        raise RuntimeError(f"prompt ambiguity hard-block violation detected: {hard}")

    commit = diagnostics.get("checks", {}).get("semantic_commitment_telemetry", {})
    generalization = commit.get("commitment_generalization_vs_recitation", {}) if isinstance(commit, dict) else {}
    top1 = float(generalization.get("top1_behavioral_category_share", 0.0) or 0.0)
    if top1 > MAX_TOP1_BEHAVIOR_SHARE:
        raise RuntimeError(
            "behavioral monoculture doctrine violation: "
            f"top1_behavioral_category_share={top1} threshold={MAX_TOP1_BEHAVIOR_SHARE}"
        )

    anchor_ratio = float(commit.get("anchor_dominance_ratio", {}).get("ratio", 0.0) or 0.0)
    if anchor_ratio > MAX_LITERAL_ANCHOR_SHARE:
        raise RuntimeError(
            "anchor dominance doctrine violation: "
            f"ratio={anchor_ratio} threshold={MAX_LITERAL_ANCHOR_SHARE}"
        )

    top_shell_share = float(commit.get("paraphrastic_success_diversity", {}).get("top_prompt_shell_share", 0.0) or 0.0)
    if top_shell_share > MAX_TOP_PROMPT_SHELL_SHARE:
        raise RuntimeError(
            "prompt shell concentration doctrine violation: "
            f"top_prompt_shell_share={top_shell_share} threshold={MAX_TOP_PROMPT_SHELL_SHARE}"
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
    commit = diagnostics.get("checks", {}).get("semantic_commitment_telemetry", {})
    return {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "iteration": RUN_NAME,
        "status": "completed",
        "question": "Are semantic-substitution conversions producing generalized procedural commitment or lexical-shell recitation?",
        "conversion_selection_summary": selection,
        "targeted_prompt_samples": diagnostics.get("review_support", {}).get("targeted_prompt_samples", {}),
        "semantic_commitment_telemetry": commit,
        "risk_flags": {
            "diversity": diagnostics.get("review_support", {}).get("diversity_review_summary", {}),
            "anti_homogenization": diagnostics.get("review_support", {}).get("anti_homogenization_summary", {}),
            "generalization_vs_recitation": commit.get("commitment_generalization_vs_recitation", {}),
            "anchor_dominance": commit.get("anchor_dominance_ratio", {}),
            "scalar_substitution_rebound_proxy": commit.get("scalar_substitution_rebound_proxy", {}),
        },
        "interpretation_guidance": [
            "Prefer small read_file exact-valid footholds with paraphrastic spread over narrow literal-shell gains.",
            "If top prompt shell share rises above threshold, treat as template coercion risk.",
            "If ambiguity hard blocks are non-zero, invalidate candidate package before training review.",
            "If scalar substitution rebound rises post-eval, halt forward progression.",
        ],
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_promote": False,
        },
    }


def _write_review_package_md(review: dict[str, Any], out_path: Path) -> None:
    sel = review.get("conversion_selection_summary", {})
    tel = review.get("semantic_commitment_telemetry", {})
    risk = review.get("risk_flags", {})

    lines: list[str] = []
    lines.append("# Stage B i10 Human Review Package")
    lines.append("")
    lines.append(f"- Generated UTC: {review.get('generated_utc')}")
    lines.append(f"- Iteration: {review.get('iteration')}")
    lines.append(f"- Status: {review.get('status')}")
    lines.append("")

    lines.append("## Selection")
    lines.append(f"- Added rows total: {sel.get('added_rows_total')}")
    lines.append(f"- Added train: {sel.get('added_rows_train')}")
    lines.append(f"- Added val: {sel.get('added_rows_val')}")
    lines.append("")

    lines.append("## Telemetry Highlights")
    commit_gen = tel.get("commitment_generalization_vs_recitation", {}) if isinstance(tel, dict) else {}
    anchor = tel.get("anchor_dominance_ratio", {}) if isinstance(tel, dict) else {}
    rebound = tel.get("scalar_substitution_rebound_proxy", {}) if isinstance(tel, dict) else {}
    lines.append(
        f"- Top1 behavioral category share: {commit_gen.get('top1_behavioral_category_share')} "
        f"(threshold={commit_gen.get('top1_threshold')})"
    )
    lines.append(
        f"- Anchor dominance ratio: {anchor.get('ratio')} "
        f"(threshold={anchor.get('threshold')})"
    )
    lines.append(
        f"- Scalar rebound proxy delta: {rebound.get('delta')} "
        f"(threshold={rebound.get('threshold_delta')})"
    )
    lines.append("")

    lines.append("## Risk Flags")
    lines.append(f"- Diversity pass: {risk.get('diversity', {}).get('pass')}")
    lines.append(f"- Anti-homogenization pass: {risk.get('anti_homogenization', {}).get('pass')}")
    lines.append(f"- Generalization/recitation flags: {risk.get('generalization_vs_recitation', {})}")
    lines.append(f"- Anchor flags: {risk.get('anchor_dominance', {})}")
    lines.append("")

    lines.append("## Guidance")
    for item in review.get("interpretation_guidance", []):
        lines.append(f"- {item}")
    lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


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
            "objective": "semantic_scalar_substitution_conversion_under_uncertainty",
            "targeted_tools": list(TARGETED_TOOLS),
        },
        "inputs": {
            "parent_train_jsonl": str(inputs.parent_train_jsonl),
            "parent_val_jsonl": str(inputs.parent_val_jsonl),
            "parent_summary_json": str(inputs.parent_summary_json),
            "eval_comparison_rows_jsonl": str(inputs.eval_comparison_rows_jsonl),
            "i9_behavioral_review_json": str(inputs.i9_behavioral_review_json),
            "i10_recon_json": str(inputs.i10_recon_json),
            "i10_taxonomy_json": str(inputs.i10_taxonomy_json),
            "i10_risk_matrix_json": str(inputs.i10_risk_matrix_json),
            "i10_candidate_patterns_json": str(inputs.i10_candidate_patterns_json),
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
            "semantic_commitment_telemetry": diagnostics.get("checks", {}).get("semantic_commitment_telemetry", {}),
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
            "scalar_substitution_rebound_telemetry_json": str(outputs.scalar_substitution_rebound_telemetry_json),
            "human_review_package_json": str(outputs.review_package_json),
            "human_review_package_md": str(outputs.review_package_md),
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
    parser = argparse.ArgumentParser(description="Generate Stage B i10 candidate dataset package.")
    parser.add_argument(
        "--parent-train-jsonl",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i9_train.jsonl",
    )
    parser.add_argument(
        "--parent-val-jsonl",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i9_val.jsonl",
    )
    parser.add_argument(
        "--parent-summary-json",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i9_summary.json",
    )

    parser.add_argument("--eval-heldout-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/heldout_validation.jsonl")
    parser.add_argument("--eval-tool-holdout-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/tool_holdout.jsonl")
    parser.add_argument("--eval-no-call-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/no_call.jsonl")
    parser.add_argument("--eval-adversarial-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/adversarial.jsonl")
    parser.add_argument("--eval-direct-answer-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/direct_answer.jsonl")
    parser.add_argument(
        "--eval-comparison-rows-jsonl",
        default="/opt/ai-stack/assistant-training/evals/runs/canonical_eval_20260526T232239Z/comparison_rows.jsonl",
    )

    parser.add_argument(
        "--i9-behavioral-review-json",
        default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i9_behavioral_review_package.json",
    )
    parser.add_argument(
        "--i10-recon-json",
        default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10_semantic_commitment_reconnaissance.json",
    )
    parser.add_argument(
        "--i10-taxonomy-json",
        default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10_semantic_substitution_taxonomy.json",
    )
    parser.add_argument(
        "--i10-risk-matrix-json",
        default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10_intervention_risk_matrix.json",
    )
    parser.add_argument(
        "--i10-candidate-patterns-json",
        default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10_candidate_intervention_patterns.json",
    )

    parser.add_argument("--output-root", default="/opt/ai-stack/assistant-training/data/v1_0")
    parser.add_argument("--report-root", default="/opt/ai-stack/assistant-training/manifests/reports")
    parser.add_argument("--seed", type=int, default=20260527)

    parser.add_argument("--enable-dataset-emission", action="store_true")
    parser.add_argument("--allow-generation-phase", action="store_true")
    parser.add_argument("--enable-i10-semantic-commitment", action="store_true")

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

    i9_behavioral_report = _load_json(inputs.i9_behavioral_review_json)
    _ = _load_json(inputs.i10_recon_json)
    _ = _load_json(inputs.i10_taxonomy_json)
    _ = _load_json(inputs.i10_risk_matrix_json)
    _ = _load_json(inputs.i10_candidate_patterns_json)

    comparison_rows = _load_jsonl(inputs.eval_comparison_rows_jsonl)
    signature_map = _build_failure_signature_catalog(comparison_rows)
    if not signature_map:
        raise RuntimeError("empty failure signature catalog from i9 comparison rows")

    candidate_train = json.loads(json.dumps(parent_train, ensure_ascii=False))
    candidate_val = json.loads(json.dumps(parent_val, ensure_ascii=False))

    prompt_to_targets, prompt_to_tools, prompt_tool_to_args = _prompt_maps(candidate_train + candidate_val)

    train_added, train_selection_stats = _select_candidates(
        candidate_train,
        split="train",
        signature_map=signature_map,
        quotas=TRAIN_QUOTAS,
        primary_archetype_minimums=PRIMARY_ARCHETYPE_MIN_TRAIN,
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
        primary_archetype_minimums=PRIMARY_ARCHETYPE_MIN_VAL,
        seed=int(args.seed),
        prompt_to_targets=prompt_to_targets,
        prompt_to_tools=prompt_to_tools,
        prompt_tool_to_args=prompt_tool_to_args,
    )

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
        i9_behavioral_report=i9_behavioral_report,
    )
    _fail_fast_diagnostic_doctrine(diagnostics)

    contamination_audit = _build_contamination_audit(candidate_train, candidate_val, eval_map)
    review_package = _build_review_package(diagnostics, selection_stats)

    commit = diagnostics.get("checks", {}).get("semantic_commitment_telemetry", {})
    collapse_watch = commit.get("collapse_watch_conditions", {})
    anchor_dominance = commit.get("anchor_dominance_ratio", {})
    scalar_rebound = commit.get("scalar_substitution_rebound_proxy", {})

    _write_jsonl(outputs.train_jsonl, candidate_train)
    _write_jsonl(outputs.val_jsonl, candidate_val)
    _write_json(outputs.diagnostics_json, diagnostics)
    _write_json(outputs.contamination_audit_json, contamination_audit)
    _write_json(outputs.prompt_ambiguity_audit_json, prompt_ambiguity_audit)
    _write_json(outputs.collapse_watch_telemetry_json, collapse_watch)
    _write_json(outputs.anchor_dominance_telemetry_json, anchor_dominance)
    _write_json(outputs.scalar_substitution_rebound_telemetry_json, scalar_rebound)
    _write_json(outputs.review_package_json, review_package)
    _write_review_package_md(review_package, outputs.review_package_md)

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
