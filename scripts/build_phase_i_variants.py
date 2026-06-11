#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SYSTEM_TOOL = (
    "You are a runtime tool-call assistant. Return only strict JSON tool calls when a tool is required. "
    "Do not add prose, markdown, or shell blocks."
)

PHASE_I_H1_NAME = "H1_diversity_patch"
PHASE_I_H2_NAME = "H2_commitment_patch"
PHASE_I_H0_NAME = "H0_control_i3_micro"

CONFIG_TEMPLATE_PATH = Path("configs/lora/stage_b_llama31_8b_base_v1_i10r_microprobe.config.json")
CANONICAL_EVAL_MANIFEST_PATH = Path("evals/canonical_eval_manifest_v1.json")
PHASE_I_JOURNAL_PATH = Path("docs/phase_i/PHASE_I_CODEX_JOURNAL.md")
PHASE_I_CONTROL_VERIFICATION_PATH = Path("docs/phase_i/CONTROL_SURFACE_VERIFICATION.md")
PHASE_I_VARIANT_VALIDATION_PATH = Path("docs/phase_i/DATASET_VARIANT_VALIDATION.md")

H1_TOOL_ALLOCATION = {
    "list_dir": 30,
    "list_models": 30,
    "move_path": 30,
    "git_diff": 4,
    "list_active_ports": 4,
    "write_file": 2,
}


@dataclass(frozen=True)
class JsonlRow:
    raw: str
    obj: dict[str, Any]


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"expected object JSON at {path}")
    return payload


def _load_jsonl_rows(path: Path) -> list[JsonlRow]:
    rows: list[JsonlRow] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            raw = line.rstrip("\n")
            if not raw.strip():
                continue
            try:
                obj = json.loads(raw)
            except Exception as exc:
                raise RuntimeError(f"invalid JSONL {path}:{line_no}: {exc}") from exc
            if not isinstance(obj, dict):
                raise RuntimeError(f"invalid JSONL {path}:{line_no}: expected object rows")
            rows.append(JsonlRow(raw=raw, obj=obj))
    return rows


def _canonical_json_text(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_jsonl_raw(path: Path, rows: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for raw in rows:
            f.write(raw.rstrip("\n") + "\n")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def _tool_name(row: dict[str, Any]) -> str:
    msgs = row.get("messages")
    if not isinstance(msgs, list):
        return ""
    for msg in msgs:
        if not isinstance(msg, dict) or msg.get("role") != "assistant":
            continue
        tool_calls = msg.get("tool_calls")
        if not isinstance(tool_calls, list) or not tool_calls:
            return ""
        call0 = tool_calls[0]
        if not isinstance(call0, dict):
            return ""
        function = call0.get("function")
        if not isinstance(function, dict):
            return ""
        name = function.get("name")
        return str(name).strip() if isinstance(name, str) else ""
    return ""


def _tool_args(row: dict[str, Any]) -> dict[str, Any]:
    msgs = row.get("messages")
    if not isinstance(msgs, list):
        return {}
    for msg in msgs:
        if not isinstance(msg, dict) or msg.get("role") != "assistant":
            continue
        tool_calls = msg.get("tool_calls")
        if not isinstance(tool_calls, list) or not tool_calls:
            return {}
        call0 = tool_calls[0]
        if not isinstance(call0, dict):
            return {}
        function = call0.get("function")
        if not isinstance(function, dict):
            return {}
        args = function.get("arguments")
        if isinstance(args, dict):
            return dict(args)
        if isinstance(args, str):
            try:
                parsed = json.loads(args)
            except Exception:
                return {}
            return parsed if isinstance(parsed, dict) else {}
    return {}


def _tool_payload_text(row: dict[str, Any]) -> str:
    msgs = row.get("messages")
    if not isinstance(msgs, list):
        return ""
    for msg in msgs:
        if not isinstance(msg, dict) or msg.get("role") != "assistant":
            continue
        tool_calls = msg.get("tool_calls")
        if isinstance(tool_calls, list) and tool_calls:
            return _canonical_json_text({"tool_calls": tool_calls})
        return str(msg.get("content") or "")
    return ""


def _user_prompt(row: dict[str, Any]) -> str:
    msgs = row.get("messages")
    if not isinstance(msgs, list):
        return ""
    for msg in msgs:
        if isinstance(msg, dict) and msg.get("role") == "user":
            return str(msg.get("content") or "")
    return ""


def _source_case_id(row: dict[str, Any]) -> str:
    metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    if not isinstance(metadata, dict):
        return ""
    value = metadata.get("source_case_id") or metadata.get("case_id") or ""
    return str(value).strip()


def _category(row: dict[str, Any]) -> str:
    metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    if not isinstance(metadata, dict):
        return "unknown"
    return str(metadata.get("category") or "unknown")


def _eval_overlap(candidate_rows: list[dict[str, Any]], eval_rows: list[dict[str, Any]]) -> dict[str, int]:
    candidate_prompts = {_user_prompt(row) for row in candidate_rows}
    candidate_targets = {_tool_payload_text(row) for row in candidate_rows}
    candidate_case_ids = {_source_case_id(row) for row in candidate_rows}

    eval_prompts = {_user_prompt(row) for row in eval_rows}
    eval_targets = {_tool_payload_text(row) for row in eval_rows}
    eval_case_ids = {_source_case_id(row) for row in eval_rows}

    return {
        "prompt_overlap": len(candidate_prompts.intersection(eval_prompts)),
        "target_overlap": len(candidate_targets.intersection(eval_targets)),
        "source_case_id_overlap": len(candidate_case_ids.intersection(eval_case_ids)),
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
        "train_overlap": {name: _eval_overlap(train_rows, rows) for name, rows in eval_map.items()},
        "val_overlap": {name: _eval_overlap(val_rows, rows) for name, rows in eval_map.items()},
        "combined_overlap": {name: _eval_overlap(combined, rows) for name, rows in eval_map.items()},
        "blocking_policy": {
            "heldout_tool_holdout_max_allowed_overlap": 0,
            "fail_fast": True,
        },
    }


def _extract_control_split(rows: list[JsonlRow]) -> tuple[list[int], list[int]]:
    tool_positive_indices: list[int] = []
    non_tool_indices: list[int] = []
    for idx, row in enumerate(rows):
        if _category(row.obj) == "tool_positive":
            tool_positive_indices.append(idx)
        else:
            non_tool_indices.append(idx)
    return tool_positive_indices, non_tool_indices


def _anchor_score(row: JsonlRow) -> int:
    text = f"{row.obj.get('messages', [{}])[0].get('content', '')} {row.obj.get('messages', [{}, {}])[1].get('content', '')}"
    lowered = text.lower()
    keywords = [
        "tool_calls",
        "tool-call",
        "tool call",
        "strict json",
        "canonical",
        "return only",
        "one json object",
        "payload",
        "do not add prose",
        "do not output",
        "first response",
        "exact",
        "emit",
    ]
    score = 0
    for keyword in keywords:
        if keyword in lowered:
            score += 1
    if "json" in lowered:
        score += 1
    if "tool" in lowered:
        score += 1
    return score


def _phase_i_variant_suffix(variant_name: str, slot: int) -> str:
    return f" [{variant_name}:{slot:03d}]"


def _ensure_unique_prompt(
    prompt: str,
    *,
    forbidden_prompts: set[str],
    variant_name: str,
    slot: int,
) -> str:
    if prompt in forbidden_prompts:
        return f"{prompt}{_phase_i_variant_suffix(variant_name, slot)}"
    return prompt


def _normalize_source_row(row: dict[str, Any], *, variant_name: str, slot: int) -> dict[str, Any]:
    messages = row.get("messages")
    if not isinstance(messages, list) or len(messages) < 3:
        raise RuntimeError("source row missing messages")
    system_msg = messages[0] if isinstance(messages[0], dict) else {}
    user_msg = messages[1] if isinstance(messages[1], dict) else {}
    assistant_msg = messages[2] if isinstance(messages[2], dict) else {}
    tool_calls = assistant_msg.get("tool_calls")
    if not isinstance(tool_calls, list) or len(tool_calls) != 1:
        raise RuntimeError("source row must contain exactly one tool call")
    call0 = tool_calls[0]
    if not isinstance(call0, dict):
        raise RuntimeError("source row tool call is not an object")
    function = call0.get("function")
    if not isinstance(function, dict):
        raise RuntimeError("source row function is not an object")
    tool = str(function.get("name") or "").strip()
    if not tool:
        raise RuntimeError("source row missing tool name")
    raw_args = function.get("arguments")
    if isinstance(raw_args, str):
        try:
            args = json.loads(raw_args)
        except Exception as exc:
            raise RuntimeError("source row has invalid string arguments") from exc
    elif isinstance(raw_args, dict):
        args = dict(raw_args)
    else:
        raise RuntimeError("source row arguments must be a dict or JSON string")

    base_case_id = _source_case_id(row) or f"source_row_{slot:03d}"
    metadata = dict(row.get("metadata") or {})
    metadata.update(
        {
            "category": "tool_positive",
            "source_case_id": f"{base_case_id}__phase_i_{variant_name}_{slot:03d}",
            "phase_i_parent_case_id": base_case_id,
            "phase_i_variant": variant_name,
            "phase_i_patch_slot": slot,
            "tool": tool,
            "source": metadata.get("source") or "tool_source",
            "synthetic": bool(metadata.get("synthetic", False)),
        }
    )

    normalized = {
        "messages": [
            {"role": "system", "content": str(system_msg.get("content") or SYSTEM_TOOL)},
            {"role": "user", "content": str(user_msg.get("content") or "")},
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "type": "function",
                        "function": {
                            "name": tool,
                            "arguments": args,
                        },
                    }
                ],
            },
        ],
        "metadata": metadata,
    }
    return normalized


def _describe_arguments(tool: str, args: dict[str, Any]) -> str:
    if tool in {"rg_search", "read_file", "list_dir", "stat_path", "sha256_file"}:
        path = args.get("path") or args.get("root") or args.get("src") or args.get("source") or ""
        if tool == "rg_search":
            pattern = args.get("pattern") or ""
            if path and pattern:
                return f"{path} for {pattern}"
            if path:
                return f"{path}"
            return "the requested file or path"
        if tool == "read_file":
            line_start = args.get("line_start")
            line_end = args.get("line_end")
            if path and line_start is not None and line_end is not None:
                return f"{path} from line {line_start} to line {line_end}"
            if path:
                return f"{path}"
            return "the requested file"
        if path:
            return path
        return "the requested path"

    if tool == "find_files":
        root = args.get("root") or ""
        pattern = args.get("pattern") or ""
        if root and pattern:
            return f"{root} matching {pattern}"
        return root or "the requested root"

    if tool == "write_file":
        path = args.get("path") or ""
        return path or "the requested file"

    if tool == "git_diff":
        path = args.get("path") or ""
        return path or "the requested repository path"

    if tool == "check_service_health":
        return str(args.get("service") or args.get("service_name") or "the requested service")

    if tool == "git_status":
        return "the repository"

    if tool == "list_active_ports":
        return "the active ports"

    if tool == "run_command":
        command = args.get("command") or ""
        return command or "the requested command"

    if tool == "list_models":
        return "the available models"

    if tool == "get_system_datetime":
        return "the current date and time"

    if tool == "get_system_version":
        return "the current version"

    if tool == "list_tools":
        return "the available tools"

    if tool == "debug_tools":
        return "the tool routing state"

    if tool == "http_request":
        url = args.get("url") or ""
        return url or "the requested URL"

    if tool == "service_control":
        service = args.get("service") or ""
        return service or "the requested service"

    if tool == "test_run":
        return "the requested test"

    if tool == "move_path":
        src = args.get("src") or ""
        dst = args.get("dst") or ""
        if src and dst:
            return f"{src} to {dst}"
        return src or "the requested path"

    if tool == "copy_path":
        src = args.get("src") or ""
        dst = args.get("dst") or ""
        if src and dst:
            return f"{src} to {dst}"
        return src or "the requested path"

    if tool == "archive_create":
        return "the requested archive inputs"

    if tool == "archive_extract":
        return "the requested archive"

    if tool == "apply_unified_diff":
        return "the requested diff"

    if tool == "json_edit":
        return "the requested JSON document"

    return "the provided arguments"


def _paraphrase_commitment_row(row: JsonlRow, *, slot: int, forbidden_prompts: set[str]) -> dict[str, Any]:
    tool = _tool_name(row.obj)
    args = _tool_args(row.obj)
    summary = _describe_arguments(tool, args)
    system_prompt = "Use the requested tool and keep the response concise."

    if tool == "rg_search":
        user_prompt = f"Search {summary} and report the result."
    elif tool == "read_file":
        user_prompt = f"Read {summary} and report the requested symbol or detail."
    elif tool == "find_files":
        user_prompt = f"Find files under {summary}."
    elif tool == "write_file":
        user_prompt = f"Write the requested content to {summary}."
    elif tool == "git_diff":
        user_prompt = f"Show the diff for {summary}."
    elif tool == "check_service_health":
        user_prompt = f"Check health for {summary}."
    elif tool == "list_dir":
        user_prompt = f"List the contents of {summary}."
    elif tool == "stat_path":
        user_prompt = f"Inspect metadata for {summary}."
    elif tool == "git_status":
        user_prompt = "Report git status for the repository."
    elif tool == "list_active_ports":
        user_prompt = "List active ports and report whether the requested one appears."
    elif tool == "run_command":
        user_prompt = f"Run {summary} and return stdout only."
    elif tool == "list_models":
        user_prompt = "List the available models."
    elif tool == "get_system_datetime":
        user_prompt = "Report the current date and time."
    elif tool == "get_system_version":
        user_prompt = "Report the current version."
    elif tool == "list_tools":
        user_prompt = "List the available tools."
    elif tool == "debug_tools":
        user_prompt = "Inspect the tool routing state and report the enabled tool count."
    elif tool == "http_request":
        user_prompt = f"Send the request to {summary}."
    elif tool == "service_control":
        user_prompt = f"Control the service named {summary}."
    elif tool == "test_run":
        user_prompt = "Run the requested test."
    elif tool == "move_path":
        user_prompt = f"Move {summary}."
    elif tool == "sha256_file":
        user_prompt = f"Compute the SHA-256 for {summary}."
    elif tool == "copy_path":
        user_prompt = f"Copy {summary}."
    elif tool == "archive_create":
        user_prompt = "Create the requested archive."
    elif tool == "archive_extract":
        user_prompt = "Extract the requested archive."
    elif tool == "apply_unified_diff":
        user_prompt = "Apply the provided unified diff."
    elif tool == "json_edit":
        user_prompt = "Apply the requested JSON edit."
    else:
        user_prompt = f"Use {tool} with the provided arguments."

    user_prompt = _ensure_unique_prompt(
        user_prompt,
        forbidden_prompts=forbidden_prompts,
        variant_name=PHASE_I_H2_NAME,
        slot=slot,
    )

    base = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "type": "function",
                        "function": {
                            "name": tool,
                            "arguments": args,
                        },
                    }
                ],
            },
        ],
        "metadata": dict(row.obj.get("metadata") or {}),
    }

    metadata = base["metadata"]
    metadata.update(
        {
            "category": "tool_positive",
            "phase_i_variant": PHASE_I_H2_NAME,
            "phase_i_patch_slot": slot,
            "phase_i_parent_case_id": _source_case_id(row.obj),
            "source_case_id": f"{_source_case_id(row.obj) or f'h2_row_{slot:03d}'}__phase_i_h2_{slot:03d}",
            "source": "phase_i_commitment_patch",
            "tool": tool,
            "synthetic": bool(metadata.get("synthetic", True)),
        }
    )
    return base


def _build_h1_patch_rows(
    source_rows: list[JsonlRow],
    *,
    eval_prompts: set[str],
    eval_targets: set[str],
    eval_case_ids: set[str],
) -> list[dict[str, Any]]:
    clean_rows: dict[str, list[JsonlRow]] = defaultdict(list)
    for row in source_rows:
        metadata = row.obj.get("metadata") if isinstance(row.obj.get("metadata"), dict) else {}
        if not isinstance(metadata, dict):
            continue
        if str(metadata.get("source")) != "canonical_case_template":
            continue
        tool = str(metadata.get("tool") or "").strip()
        if not tool:
            continue
        if _user_prompt(row.obj) in eval_prompts:
            continue
        if _tool_payload_text(row.obj) in eval_targets:
            continue
        if _source_case_id(row.obj) in eval_case_ids:
            continue
        clean_rows[tool].append(row)

    missing_tools = [tool for tool in H1_TOOL_ALLOCATION if tool not in clean_rows]
    if missing_tools:
        raise RuntimeError(f"H1 candidate pool missing clean rows for tools: {', '.join(sorted(missing_tools))}")

    patch_rows: list[dict[str, Any]] = []
    slot = 0
    for tool in H1_TOOL_ALLOCATION:
        quota = H1_TOOL_ALLOCATION[tool]
        tool_rows = clean_rows[tool]
        if len(tool_rows) < quota:
            raise RuntimeError(
                f"H1 candidate pool for {tool} is too small after contamination filtering: "
                f"need {quota}, have {len(tool_rows)}"
            )
        for row in tool_rows[:quota]:
            slot += 1
            normalized = _normalize_source_row(row.obj, variant_name=PHASE_I_H1_NAME, slot=slot)
            patch_rows.append(normalized)
    return patch_rows


def _build_h2_patch_rows(
    control_rows: list[JsonlRow],
    *,
    eval_prompts: set[str],
) -> list[dict[str, Any]]:
    tool_positive_rows = [(idx, row) for idx, row in enumerate(control_rows) if _category(row.obj) == "tool_positive"]
    ranked = sorted(tool_positive_rows, key=lambda item: (-_anchor_score(item[1]), item[0]))
    selected = ranked[:100]
    if len(selected) < 100:
        raise RuntimeError(f"H2 requires 100 tool-positive rows but only {len(selected)} are available")

    patch_rows: list[dict[str, Any]] = []
    for slot, (_, row) in enumerate(selected, start=1):
        patch_rows.append(_paraphrase_commitment_row(row, slot=slot, forbidden_prompts=eval_prompts))
    return patch_rows


def _replace_rows(
    control_rows: list[JsonlRow],
    replacement_positions: list[int],
    patch_rows: list[dict[str, Any]],
) -> list[str]:
    if len(replacement_positions) != len(patch_rows):
        raise RuntimeError(
            f"replacement count mismatch: {len(replacement_positions)} positions vs {len(patch_rows)} patch rows"
        )
    out: list[str] = [row.raw for row in control_rows]
    for position, patch_row in zip(replacement_positions, patch_rows):
        out[position] = json.dumps(patch_row, ensure_ascii=False)
    return out


def _non_tool_slice_unchanged(control_rows: list[JsonlRow], variant_rows: list[str]) -> bool:
    for idx, control_row in enumerate(control_rows):
        if _category(control_row.obj) == "tool_positive":
            continue
        if control_row.raw != variant_rows[idx]:
            return False
    return True


def _count_rows(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter()
    for row in rows:
        counts[_category(row)] += 1
    return dict(sorted(counts.items(), key=lambda kv: kv[0]))


def _tool_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter()
    for row in rows:
        if _category(row) != "tool_positive":
            continue
        counts[_tool_name(row)] += 1
    return dict(sorted(counts.items(), key=lambda kv: kv[0]))


def _parse_rows(raw_rows: list[str]) -> list[dict[str, Any]]:
    parsed: list[dict[str, Any]] = []
    for raw in raw_rows:
        obj = json.loads(raw)
        if not isinstance(obj, dict):
            raise RuntimeError("expected JSON object rows")
        parsed.append(obj)
    return parsed


def _phase_i_run_name(variant_name: str) -> str:
    if variant_name == PHASE_I_H0_NAME:
        return "stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro"
    if variant_name == PHASE_I_H1_NAME:
        return "stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch"
    if variant_name == PHASE_I_H2_NAME:
        return "stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch"
    raise RuntimeError(f"unsupported Phase I variant name: {variant_name}")


def _phase_i_paths(variant_name: str, output_root: Path) -> dict[str, Path]:
    run_name = _phase_i_run_name(variant_name)
    return {
        "run_name": run_name,  # type: ignore[return-value]
        "config_path": Path("configs/lora") / f"{run_name}.config.draft.json",
        "manifest_path": Path("manifests/runs") / f"{run_name}.run_manifest.draft.json",
        "run_root": output_root / run_name,
        "adapter_output_dir": Path("artifacts/adapters") / run_name,
        "logs_output_dir": Path("artifacts/logs") / run_name,
    }


def _build_phase_i_config(
    template_config: dict[str, Any],
    *,
    variant_name: str,
    train_jsonl: Path,
    val_jsonl: Path,
    dataset_manifest: Path,
    run_root: Path,
    adapter_output_dir: Path,
    logs_output_dir: Path,
) -> dict[str, Any]:
    cfg = copy.deepcopy(template_config)
    run_name = _phase_i_run_name(variant_name)
    cfg["name"] = run_name
    cfg["generated_utc"] = _now_utc()
    if variant_name == PHASE_I_H0_NAME:
        cfg["purpose"] = "Phase I H0 control repro on exact i3 recovery bytes."
        cfg["lineage"]["intervention_scope"] = "phase_i_control_repro_from_i3_recovery_bytes"
    elif variant_name == PHASE_I_H1_NAME:
        cfg["purpose"] = "Phase I H1 diversity patch on bounded i3-derived tool-positive replacements."
        cfg["lineage"]["intervention_scope"] = "phase_i_diversity_patch"
    elif variant_name == PHASE_I_H2_NAME:
        cfg["purpose"] = "Phase I H2 commitment patch on bounded paraphrastic tool-expected replacements."
        cfg["lineage"]["intervention_scope"] = "phase_i_commitment_patch"
    else:
        raise RuntimeError(f"unsupported Phase I variant name: {variant_name}")

    cfg["dataset"]["train_jsonl"] = str(train_jsonl)
    cfg["dataset"]["val_jsonl"] = str(val_jsonl)
    cfg["outputs"]["run_root"] = str(run_root)
    cfg["outputs"]["adapter_output_dir"] = str(adapter_output_dir)
    cfg["outputs"]["logs_dir"] = str(logs_output_dir)
    cfg["safety"]["do_not_start_training_automatically"] = True
    cfg["safety"]["requires_manual_review"] = True
    cfg["safety"]["approved_to_run"] = False
    cfg["scaffold_notes"]["execution_state"] = "phase_i_pre_execution"
    cfg["scaffold_notes"]["training_started"] = False
    cfg["scaffold_notes"]["eval_executed"] = False
    cfg["scaffold_notes"]["gate_opened"] = False
    cfg["scaffold_notes"]["auto_continuation_allowed"] = False
    cfg["scaffold_notes"]["hidden_retries_allowed"] = False
    return cfg


def _build_phase_i_run_manifest(
    *,
    variant_name: str,
    config_path: Path,
    train_jsonl: Path,
    val_jsonl: Path,
    dataset_manifest: Path,
    run_root: Path,
    adapter_output_dir: Path,
    logs_output_dir: Path,
) -> dict[str, Any]:
    run_name = _phase_i_run_name(variant_name)
    return {
        "manifest_version": "1.0",
        "name": run_name,
        "generated_utc": _now_utc(),
        "status": "draft_not_started",
        "training_started": False,
        "training_started_utc": None,
        "training_completed_utc": None,
        "config_path": str(config_path),
        "inputs": {
            "train_jsonl": str(train_jsonl),
            "val_jsonl": str(val_jsonl),
            "canonical_eval_manifest": str(CANONICAL_EVAL_MANIFEST_PATH.resolve()),
            "dataset_manifest": str(dataset_manifest),
            "phase_i_journal": str(PHASE_I_JOURNAL_PATH.resolve()),
            "phase_i_control_surface_verification": str(PHASE_I_CONTROL_VERIFICATION_PATH.resolve()),
            "phase_i_dataset_variant_validation": str(PHASE_I_VARIANT_VALIDATION_PATH.resolve()),
        },
        "expected_outputs": {
            "run_root": str(run_root),
            "adapter_output_dir": str(adapter_output_dir),
            "logs_dir": str(logs_output_dir),
            "merge_output_expected": False,
        },
        "review_gate": {
            "approved_to_run": False,
            "approved_by": None,
            "approved_utc": None,
        },
        "scaffold_notes": {
            "implementation_phase": "phase_i_pre_execution",
            "dataset_generation_completed": True,
            "training_started": False,
            "canonical_eval_executed": False,
            "single_run_only": True,
            "auto_chain_disabled": True,
            "hard_stop_triggered": False,
            "auto_progression_halted": False,
        },
        "canonical_eval_run": None,
        "canonical_eval_summary": None,
        "gate_assessment": None,
        "collapse_watch_interpretation": None,
        "behavioral_review_package": None,
    }


def _write_variant_summary(
    *,
    variant_name: str,
    control_train_path: Path,
    control_val_path: Path,
    source_pool_path: Path,
    train_path: Path,
    val_path: Path,
    summary_path: Path,
    train_rows: list[dict[str, Any]],
    val_rows: list[dict[str, Any]],
    patch_rows: list[dict[str, Any]],
    replacement_positions: list[int],
    contamination_audit: dict[str, Any],
    control_rows: list[JsonlRow],
    val_control_rows: list[JsonlRow],
    train_variant_raw_rows: list[str],
) -> None:
    summary = {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "variant_name": variant_name,
        "inputs": {
            "control_train_jsonl": str(control_train_path),
            "control_val_jsonl": str(control_val_path),
            "source_pool_jsonl": str(source_pool_path),
        },
        "policy": {
            "bounded_patch_budget_min": 80,
            "bounded_patch_budget_max": 120,
            "bounded_patch_size_used": len(patch_rows),
            "train_rows_fixed": len(train_rows),
            "val_rows_fixed": len(val_rows),
            "non_tool_slices_frozen": True,
            "eval_contract_frozen": True,
        },
        "patch": {
            "replacement_positions_0_based": replacement_positions,
            "replacement_row_count": len(patch_rows),
            "patch_rows_by_tool": _tool_counts(patch_rows),
            "patch_rows_by_category": _count_rows(patch_rows),
        },
        "composition": {
            "train_categories": _count_rows(train_rows),
            "val_categories": _count_rows(val_rows),
            "train_tool_counts": _tool_counts(train_rows),
            "val_tool_counts": _tool_counts(val_rows),
        },
        "frozen_surface_checks": {
            "train_non_tool_slice_unchanged": _non_tool_slice_unchanged(control_rows, train_variant_raw_rows),
            "val_bytes_copied_from_control": True,
            "train_row_count_matches_control": len(train_rows) == len(control_rows),
            "val_row_count_matches_control": len(val_rows) == len(val_control_rows),
        },
        "contamination_audit": contamination_audit,
        "hashes": {
            "train_sha256": _sha256_file(train_path),
            "val_sha256": _sha256_file(val_path),
        },
        "outputs": {
            "train_jsonl": str(train_path),
            "val_jsonl": str(val_path),
            "summary_json": str(summary_path),
        },
    }
    _write_json(summary_path, summary)


def _build_eval_map(args: argparse.Namespace) -> dict[str, list[dict[str, Any]]]:
    heldout_path = Path(args.eval_heldout_jsonl)
    tool_holdout_path = Path(args.eval_tool_holdout_jsonl)
    no_call_path = Path(args.eval_no_call_jsonl)
    adversarial_path = Path(args.eval_adversarial_jsonl)
    direct_answer_path = Path(args.eval_direct_answer_jsonl)
    return {
        "heldout_validation": _parse_rows([row.raw for row in _load_jsonl_rows(heldout_path)]),
        "tool_holdout": _parse_rows([row.raw for row in _load_jsonl_rows(tool_holdout_path)]),
        "no_call": _parse_rows([row.raw for row in _load_jsonl_rows(no_call_path)]),
        "adversarial": _parse_rows([row.raw for row in _load_jsonl_rows(adversarial_path)]),
        "direct_answer": _parse_rows([row.raw for row in _load_jsonl_rows(direct_answer_path)]),
    }


def _build_variant(
    *,
    variant_name: str,
    control_train_path: Path,
    control_val_path: Path,
    source_pool_path: Path,
    output_root: Path,
    eval_map: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    control_rows = _load_jsonl_rows(control_train_path)
    control_val_rows = _load_jsonl_rows(control_val_path)
    control_tool_indices, _ = _extract_control_split(control_rows)
    control_tool_rows = [control_rows[idx] for idx in control_tool_indices]
    control_tool_counts = Counter(_tool_name(row.obj) for row in control_tool_rows)

    val_out = output_root / f"dataset_v1_0_phase_i_{variant_name.lower()}_val.jsonl"
    shutil.copyfile(control_val_path, val_out)
    val_rows = [row.obj for row in control_val_rows]

    eval_prompts = set()
    eval_targets = set()
    eval_case_ids = set()
    for rows in eval_map.values():
        eval_prompts.update(_user_prompt(row) for row in rows)
        eval_targets.update(_tool_payload_text(row) for row in rows)
        eval_case_ids.update(_source_case_id(row) for row in rows)

    if variant_name == PHASE_I_H1_NAME:
        patch_rows = _build_h1_patch_rows(_load_jsonl_rows(source_pool_path), eval_prompts=eval_prompts, eval_targets=eval_targets, eval_case_ids=eval_case_ids)
        replacement_positions = [idx for idx in control_tool_indices if _tool_name(control_rows[idx].obj) == "rg_search"][: len(patch_rows)]
        if len(replacement_positions) != len(patch_rows):
            raise RuntimeError(
                f"H1 requires {len(patch_rows)} rg_search replacement positions but only {len(replacement_positions)} are available"
            )
    elif variant_name == PHASE_I_H2_NAME:
        patch_rows = _build_h2_patch_rows(control_rows, eval_prompts=eval_prompts)
        ranked_positions = [idx for idx, row in enumerate(control_rows) if _category(row.obj) == "tool_positive"]
        ranked_positions = sorted(
            ranked_positions,
            key=lambda idx: (-_anchor_score(control_rows[idx]), idx),
        )
        replacement_positions = ranked_positions[: len(patch_rows)]
        if len(replacement_positions) != len(patch_rows):
            raise RuntimeError(
                f"H2 requires {len(patch_rows)} replacement positions but only {len(replacement_positions)} are available"
            )
    else:
        raise RuntimeError(f"unsupported variant {variant_name}")

    train_variant_rows = _replace_rows(control_rows, replacement_positions, patch_rows)
    train_out = output_root / f"dataset_v1_0_phase_i_{variant_name.lower()}_train.jsonl"
    _write_jsonl_raw(train_out, train_variant_rows)
    train_rows = _parse_rows(train_variant_rows)

    contamination_audit = _build_contamination_audit(train_rows, val_rows, eval_map)
    if contamination_audit["combined_overlap"]["heldout_validation"] != {"prompt_overlap": 0, "target_overlap": 0, "source_case_id_overlap": 0}:
        raise RuntimeError(f"{variant_name} contaminated heldout_validation: {contamination_audit['combined_overlap']['heldout_validation']}")
    if contamination_audit["combined_overlap"]["tool_holdout"] != {"prompt_overlap": 0, "target_overlap": 0, "source_case_id_overlap": 0}:
        raise RuntimeError(f"{variant_name} contaminated tool_holdout: {contamination_audit['combined_overlap']['tool_holdout']}")

    summary_path = output_root / f"dataset_v1_0_phase_i_{variant_name.lower()}_summary.json"
    _write_variant_summary(
        variant_name=variant_name,
        control_train_path=control_train_path,
        control_val_path=control_val_path,
        source_pool_path=source_pool_path,
        train_path=train_out,
        val_path=val_out,
        summary_path=summary_path,
        train_rows=train_rows,
        val_rows=val_rows,
        patch_rows=patch_rows,
        replacement_positions=replacement_positions,
        contamination_audit=contamination_audit,
        control_rows=control_rows,
        val_control_rows=control_val_rows,
        train_variant_raw_rows=train_variant_rows,
    )

    return {
        "variant_name": variant_name,
        "train_jsonl": str(train_out),
        "val_jsonl": str(val_out),
        "summary_json": str(summary_path),
        "patch_rows": len(patch_rows),
        "replacement_positions": replacement_positions,
        "control_tool_counts": dict(sorted(control_tool_counts.items(), key=lambda kv: kv[0])),
        "train_sha256": _sha256_file(train_out),
        "val_sha256": _sha256_file(val_out),
    }


def _write_phase_i_execution_assets(
    *,
    template_config_path: Path,
    control_train_path: Path,
    control_val_path: Path,
    control_summary_path: Path,
    variant_results: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    template_config = _load_json(template_config_path)
    if not isinstance(template_config, dict):
        raise RuntimeError(f"template config at {template_config_path} must be an object")

    emitted: dict[str, Any] = {}
    for variant_name, variant in (
        (
            PHASE_I_H0_NAME,
            {
                "train_jsonl": control_train_path,
                "val_jsonl": control_val_path,
                "summary_json": control_summary_path,
            },
        ),
        (
            PHASE_I_H1_NAME,
            {
                "train_jsonl": Path(variant_results[PHASE_I_H1_NAME]["train_jsonl"]),
                "val_jsonl": Path(variant_results[PHASE_I_H1_NAME]["val_jsonl"]),
                "summary_json": Path(variant_results[PHASE_I_H1_NAME]["summary_json"]),
            },
        ),
        (
            PHASE_I_H2_NAME,
            {
                "train_jsonl": Path(variant_results[PHASE_I_H2_NAME]["train_jsonl"]),
                "val_jsonl": Path(variant_results[PHASE_I_H2_NAME]["val_jsonl"]),
                "summary_json": Path(variant_results[PHASE_I_H2_NAME]["summary_json"]),
            },
        ),
    ):
        run_name = _phase_i_run_name(variant_name)
        config_path = (Path("configs/lora") / f"{run_name}.config.draft.json").resolve()
        manifest_path = (Path("manifests/runs") / f"{run_name}.run_manifest.draft.json").resolve()
        run_root = (Path("artifacts") / run_name).resolve()
        adapter_output_dir = (Path("artifacts/adapters") / run_name).resolve()
        logs_output_dir = (Path("artifacts/logs") / run_name).resolve()

        cfg = _build_phase_i_config(
            template_config,
            variant_name=variant_name,
            train_jsonl=variant["train_jsonl"],
            val_jsonl=variant["val_jsonl"],
            dataset_manifest=variant["summary_json"],
            run_root=run_root,
            adapter_output_dir=adapter_output_dir,
            logs_output_dir=logs_output_dir,
        )
        manifest = _build_phase_i_run_manifest(
            variant_name=variant_name,
            config_path=config_path,
            train_jsonl=variant["train_jsonl"],
            val_jsonl=variant["val_jsonl"],
            dataset_manifest=variant["summary_json"],
            run_root=run_root,
            adapter_output_dir=adapter_output_dir,
            logs_output_dir=logs_output_dir,
        )
        _write_json(config_path, cfg)
        _write_json(manifest_path, manifest)
        emitted[variant_name] = {
            "config_path": str(config_path),
            "manifest_path": str(manifest_path),
            "run_root": str(run_root),
            "adapter_output_dir": str(adapter_output_dir),
            "logs_output_dir": str(logs_output_dir),
        }

    return emitted


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase I control and treatment dataset variants.")
    parser.add_argument(
        "--control-train-jsonl",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl",
    )
    parser.add_argument(
        "--control-val-jsonl",
        default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_val.jsonl",
    )
    parser.add_argument(
        "--source-pool-jsonl",
        default="/opt/ai-stack/assistant-training/data/tool_ft_allaliases_20260525_from_qual_reports_freq.jsonl",
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
        "--output-root",
        default="/opt/ai-stack/assistant-training/data/v1_0",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    control_train_path = Path(args.control_train_jsonl).resolve()
    control_val_path = Path(args.control_val_jsonl).resolve()
    control_summary_path = control_train_path.with_name("dataset_v1_0_stage_b_recovery_i3_summary.json")
    source_pool_path = Path(args.source_pool_jsonl).resolve()
    output_root = Path(args.output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    eval_map = _build_eval_map(args)

    results = {}
    results[PHASE_I_H1_NAME] = _build_variant(
        variant_name=PHASE_I_H1_NAME,
        control_train_path=control_train_path,
        control_val_path=control_val_path,
        source_pool_path=source_pool_path,
        output_root=output_root,
        eval_map=eval_map,
    )
    results[PHASE_I_H2_NAME] = _build_variant(
        variant_name=PHASE_I_H2_NAME,
        control_train_path=control_train_path,
        control_val_path=control_val_path,
        source_pool_path=source_pool_path,
        output_root=output_root,
        eval_map=eval_map,
    )

    execution_assets = _write_phase_i_execution_assets(
        template_config_path=CONFIG_TEMPLATE_PATH.resolve(),
        control_train_path=control_train_path,
        control_val_path=control_val_path,
        control_summary_path=control_summary_path,
        variant_results=results,
    )

    report = {
        "generated_utc": _now_utc(),
        "control": {
            "train_jsonl": str(control_train_path),
            "val_jsonl": str(control_val_path),
            "summary_json": str(control_summary_path),
            "train_sha256": _sha256_file(control_train_path),
            "val_sha256": _sha256_file(control_val_path),
        },
        "variants": results,
        "execution_assets": execution_assets,
    }
    report_path = output_root / "dataset_v1_0_phase_i_variant_build_report.json"
    _write_json(report_path, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
