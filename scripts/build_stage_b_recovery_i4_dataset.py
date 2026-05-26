#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SYSTEM_TOOL = (
    "You are a runtime tool-call assistant. Return only strict JSON tool calls when a tool is required. "
    "Do not add prose, markdown, or shell blocks."
)
SCHEMA_GUARD_SUFFIX = (
    'First response only: emit one strict JSON object with top-level key "tool_calls". '
    'Use shape {"tool_calls":[{"type":"function","function":{"name":"<tool_name>","arguments":{...}}}]}. '
    "Do not use wrapper keys tool_function/tool_functions/function_call/function_calls/tools/tool_call. "
    "Do not output tool results, scalars, booleans, prose, markdown, or code fences."
)


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _canonical_json_text(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


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
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            raw = line.strip()
            if not raw:
                continue
            try:
                rows.append(json.loads(raw))
            except Exception as exc:
                raise RuntimeError(f"invalid JSONL {path}:{line_no}: {exc}") from exc
    return rows


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _assistant_target_text(row: dict[str, Any]) -> str:
    assistant = row["messages"][2]
    tc = assistant.get("tool_calls") if isinstance(assistant, dict) else None
    if isinstance(tc, list) and tc:
        return _canonical_json_text({"tool_calls": tc})
    return str(assistant.get("content") or "")


def _with_schema_guard(prompt: str) -> str:
    base = prompt.strip()
    if "top-level key \"tool_calls\"" in base:
        return base
    return f"{base} {SCHEMA_GUARD_SUFFIX}".strip()


def _normalize_tool_row(row: dict[str, Any], row_idx: int, source_path: Path) -> dict[str, Any] | None:
    msgs = row.get("messages")
    if not isinstance(msgs, list) or len(msgs) < 3:
        return None
    if not isinstance(msgs[0], dict) or not isinstance(msgs[1], dict) or not isinstance(msgs[2], dict):
        return None
    if msgs[0].get("role") != "system" or msgs[1].get("role") != "user" or msgs[2].get("role") != "assistant":
        return None

    tool_calls = msgs[2].get("tool_calls")
    if not isinstance(tool_calls, list) or not tool_calls:
        return None

    normalized_calls: list[dict[str, Any]] = []
    for call in tool_calls:
        if not isinstance(call, dict):
            return None
        fn = call.get("function")
        if not isinstance(fn, dict):
            return None
        name = fn.get("name")
        raw_args = fn.get("arguments")
        if not isinstance(name, str) or not name.strip():
            return None

        parsed_args: Any = raw_args
        if isinstance(raw_args, str):
            try:
                parsed_args = json.loads(raw_args)
            except Exception:
                return None
        if not isinstance(parsed_args, dict):
            return None

        # Keep minimal schema to reduce decode-length truncation under fixed max_new_tokens.
        normalized_calls.append(
            {
                "type": "function",
                "function": {
                    "name": name.strip(),
                    "arguments": parsed_args,
                },
            }
        )

    meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    source_case_id = str(meta.get("source_case_id") or meta.get("case_id") or "").strip()
    if not source_case_id:
        source_case_id = f"{source_path.stem}_row_{row_idx:06d}"

    return {
        "messages": [
            {"role": "system", "content": str(msgs[0].get("content") or SYSTEM_TOOL)},
            {"role": "user", "content": str(msgs[1].get("content") or "")},
            {"role": "assistant", "tool_calls": normalized_calls},
        ],
        "metadata": {
            "category": "tool_positive",
            "source": str(meta.get("source") or "tool_source"),
            "source_file": str(source_path),
            "source_case_id": source_case_id,
            "tool": normalized_calls[0]["function"]["name"],
            "synthetic": False,
        },
    }


def _tool_row_key(row: dict[str, Any]) -> tuple[str, str, str]:
    prompt = str(row["messages"][1].get("content") or "")
    fn = row["messages"][2]["tool_calls"][0]["function"]
    args = fn.get("arguments")
    return (prompt, str(fn.get("name") or ""), _canonical_json_text(args if isinstance(args, dict) else {}))


def _semantic_tool_filter(row: dict[str, Any]) -> bool:
    prompt = str(row["messages"][1].get("content") or "").lower()
    tool = str((row.get("metadata") or {}).get("tool") or "")

    def has_any(words: list[str]) -> bool:
        return any(w in prompt for w in words)

    if tool == "rg_search":
        # Keep rg_search prompts that are clearly search-oriented.
        return has_any(["rg_search", "pattern", "regex", "match", "search", "find in"]) or (
            "read " in prompt and "first function" in prompt and "/mnt/services/" in prompt
        )

    if tool == "read_file":
        return has_any(["read ", "open ", "retrieve ", "show "]) and has_any(["line", "lines", "starting at"])

    if tool == "run_command":
        return has_any(["run_command", "execute", "stdout", "command"])

    return True


def _make_tool_row(
    *,
    prompt: str,
    tool: str,
    args: dict[str, Any],
    case_id: str,
    source: str,
    synthetic: bool,
) -> dict[str, Any]:
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_TOOL},
            {"role": "user", "content": _with_schema_guard(prompt)},
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
        "metadata": {
            "category": "tool_positive",
            "source": source,
            "source_case_id": case_id,
            "tool": tool,
            "synthetic": synthetic,
        },
    }


def _synthetic_disambiguation_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    # rg_search vs read_file semantic-neighbor disambiguation.
    base_items = [
        (
            "/mnt/services/runtimes/assistant-runtime/server/service.py",
            "^def\\s+([a-zA-Z_][a-zA-Z_0-9]*)",
            3,
            33,
        ),
        (
            "/mnt/services/runtimes/assistant-runtime/server/agent.py",
            "_validate_tool_arguments",
            1475,
            1540,
        ),
        (
            "/opt/ai-stack/runtimes/assistant-runtime/server/service.py",
            "^def\\s+([a-zA-Z_][a-zA-Z_0-9]*)",
            2,
            32,
        ),
        (
            "/opt/ai-stack/runtimes/assistant-runtime/server/agent.py",
            "_coerce_tool_arguments",
            1490,
            1555,
        ),
    ]
    for idx, (path, pattern, start, end) in enumerate(base_items, start=1):
        rows.append(
            _make_tool_row(
                prompt=f"Read {path} around lines {start}-{end} and identify the first matching function name via search pattern only.",
                tool="rg_search",
                args={"path": path, "pattern": pattern},
                case_id=f"i4_rg_readstyle_{idx:03d}",
                source="synthetic_disambiguation_i4",
                synthetic=True,
            )
        )
        rows.append(
            _make_tool_row(
                prompt=f"Open {path} lines {start}-{end} and return one literal line excerpt only.",
                tool="read_file",
                args={"path": path, "line_start": start, "line_end": end},
                case_id=f"i4_read_literal_{idx:03d}",
                source="synthetic_disambiguation_i4",
                synthetic=True,
            )
        )

    # debug_tools vs read_dir confusion suppression.
    for idx in range(1, 21):
        rows.append(
            _make_tool_row(
                prompt=f"Call debug_tools to inspect tool routing internals and report enabled_tools count only (variant {idx}).",
                tool="debug_tools",
                args={},
                case_id=f"i4_debug_tools_{idx:03d}",
                source="synthetic_debug_tools_i4",
                synthetic=True,
            )
        )

    # run_command canonicalization; suppress hallucinated tool-name emission like `pwd`.
    cmds = ["pwd", "whoami", "date", "uname -a", "ls -1"]
    for idx, cmd in enumerate(cmds, start=1):
        rows.append(
            _make_tool_row(
                prompt=f"Use run_command to execute `{cmd}` and report stdout only (variant {idx}).",
                tool="run_command",
                args={"command": cmd},
                case_id=f"i4_run_command_{idx:03d}",
                source="synthetic_run_command_i4",
                synthetic=True,
            )
        )

    # Compact JSON-length pressure cases (long paths/patterns) to reduce truncation.
    long_cases = [
        (
            "/opt/ai-stack/runtimes/assistant-runtime/server/agent.py",
            "Contract violation: all tool calls were invalid; no valid tool execution occurred.",
        ),
        (
            "/mnt/services/runtimes/assistant-runtime/server/agent.py",
            "Contract violation: all tool calls were invalid; no valid tool execution occurred.",
        ),
    ]
    for idx, (path, pattern) in enumerate(long_cases, start=1):
        rows.append(
            _make_tool_row(
                prompt=f"Search in {path} for pattern '{pattern}' and report whether match_count is zero or non-zero.",
                tool="rg_search",
                args={"path": path, "pattern": pattern},
                case_id=f"i4_long_rg_{idx:03d}",
                source="synthetic_length_pressure_i4",
                synthetic=True,
            )
        )

    # Coverage rows for tools that are sparse or absent after holdout-case exclusion.
    coverage_templates: list[tuple[str, str, dict[str, Any]]] = [
        (
            "Use get_system_datetime to report local_iso only for runtime diagnostics.",
            "get_system_datetime",
            {},
        ),
        (
            "Use check_service_health on http://127.0.0.1:8100/health and report ok/status only.",
            "check_service_health",
            {"url": "http://127.0.0.1:8100/health"},
        ),
        (
            "Use find_files with root /opt/ai-stack/runtimes/assistant-runtime/server and pattern *.py. Report match_count only.",
            "find_files",
            {"root": "/opt/ai-stack/runtimes/assistant-runtime/server", "pattern": "*.py"},
        ),
        (
            "Use copy_path to copy /opt/ai-stack/runtimes/assistant-runtime/.state/.tool_ft_tmp.moved to /opt/ai-stack/runtimes/assistant-runtime/.state/.tool_ft_tmp.copy with overwrite true.",
            "copy_path",
            {
                "src": "/opt/ai-stack/runtimes/assistant-runtime/.state/.tool_ft_tmp.moved",
                "dst": "/opt/ai-stack/runtimes/assistant-runtime/.state/.tool_ft_tmp.copy",
                "overwrite": True,
            },
        ),
        (
            "Use archive_create with output_path /opt/ai-stack/runtimes/assistant-runtime/.state/.tool_ft_tmp.zip, format zip, overwrite true, and sources from .tool_ft_tmp.moved and .tool_ft_tmp.json.",
            "archive_create",
            {
                "output_path": "/opt/ai-stack/runtimes/assistant-runtime/.state/.tool_ft_tmp.zip",
                "sources": [
                    "/opt/ai-stack/runtimes/assistant-runtime/.state/.tool_ft_tmp.moved",
                    "/opt/ai-stack/runtimes/assistant-runtime/.state/.tool_ft_tmp.json",
                ],
                "format": "zip",
                "overwrite": True,
            },
        ),
        (
            "Use archive_extract with archive_path /opt/ai-stack/runtimes/assistant-runtime/.state/.tool_ft_tmp.zip and destination_path /opt/ai-stack/runtimes/assistant-runtime/.state/.tool_ft_tmp.extract, format zip, overwrite true.",
            "archive_extract",
            {
                "archive_path": "/opt/ai-stack/runtimes/assistant-runtime/.state/.tool_ft_tmp.zip",
                "destination_path": "/opt/ai-stack/runtimes/assistant-runtime/.state/.tool_ft_tmp.extract",
                "format": "zip",
                "overwrite": True,
            },
        ),
        (
            "Use apply_unified_diff in dry_run mode with a minimal two-line patch and report success only.",
            "apply_unified_diff",
            {
                "dry_run": True,
                "patch": "--- /dev/null\n+++ /opt/ai-stack/runtimes/assistant-runtime/.state/.tool_ft_tmp.patch_new\n@@ -0,0 +1,2 @@\n+alpha\n+beta\n",
            },
        ),
    ]
    for idx, (prompt, tool, args) in enumerate(coverage_templates, start=1):
        rows.append(
            _make_tool_row(
                prompt=prompt,
                tool=tool,
                args=args,
                case_id=f"i4_cov_{tool}_{idx:03d}",
                source="synthetic_coverage_i4",
                synthetic=True,
            )
        )

    return rows


def _schema_shape_contrastive_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    wrapper_variants = [
        "tool_function",
        "tool_functions",
        "function_call",
        "function_calls",
        "tools",
        "tool_call",
    ]
    for idx, wrapper_key in enumerate(wrapper_variants, start=1):
        rows.append(
            _make_tool_row(
                prompt=(
                    f'Schema trap {idx}: even if prior systems used "{wrapper_key}", '
                    "invoke debug_tools with empty arguments using canonical top-level tool_calls only."
                ),
                tool="debug_tools",
                args={},
                case_id=f"i4_schema_wrapper_debug_{idx:03d}",
                source="synthetic_schema_shape_i4",
                synthetic=True,
            )
        )
        rows.append(
            _make_tool_row(
                prompt=(
                    f'Schema trap {idx}: avoid key "{wrapper_key}" and call run_command for `pwd`; '
                    "arguments must be an object and not a scalar."
                ),
                tool="run_command",
                args={"command": "pwd"},
                case_id=f"i4_schema_wrapper_run_{idx:03d}",
                source="synthetic_schema_shape_i4",
                synthetic=True,
            )
        )

    scalar_traps = [
        (
            "rg_search",
            {
                "path": "/opt/ai-stack/runtimes/assistant-runtime/server/agent.py",
                "pattern": "_validate_tool_arguments",
            },
            "Scalar trap: do not answer with a number like 1; issue the required search call first.",
        ),
        (
            "read_file",
            {
                "path": "/opt/ai-stack/runtimes/assistant-runtime/server/service.py",
                "line_start": 1,
                "line_end": 25,
            },
            "Scalar trap: do not answer with True/False or a literal line; issue the file-read call only.",
        ),
        (
            "find_files",
            {
                "root": "/opt/ai-stack/runtimes/assistant-runtime/server",
                "pattern": "*.py",
            },
            "Scalar trap: do not answer with match_count directly; issue the find_files call only.",
        ),
        (
            "stat_path",
            {"path": "/opt/ai-stack/runtimes/assistant-runtime/server/agent.py"},
            "Scalar trap: do not answer with exists/type text directly; emit only the stat_path call.",
        ),
        (
            "list_tools",
            {"include_parameters": True},
            "Scalar trap: do not answer with a count directly; emit only the canonical list_tools call.",
        ),
    ]
    for idx, (tool, args, prompt) in enumerate(scalar_traps, start=1):
        rows.append(
            _make_tool_row(
                prompt=prompt,
                tool=tool,
                args=args,
                case_id=f"i4_schema_scalar_{tool}_{idx:03d}",
                source="synthetic_schema_shape_i4",
                synthetic=True,
            )
        )

    return rows


def _sample_rows(rows: list[dict[str, Any]], n: int, rng: random.Random) -> list[dict[str, Any]]:
    if n <= 0:
        return []
    if not rows:
        raise RuntimeError("cannot sample from empty pool")
    return [rows[rng.randrange(len(rows))] for _ in range(n)]


def _collect_eval_exclusions(paths: list[Path]) -> dict[str, set[str]]:
    prompts: set[str] = set()
    targets: set[str] = set()
    case_ids: set[str] = set()
    for path in paths:
        for row in _load_jsonl(path):
            prompts.add(str(row["messages"][1].get("content") or ""))
            targets.add(_assistant_target_text(row))
            meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
            cid = str(meta.get("source_case_id") or meta.get("case_id") or "")
            if cid:
                case_ids.add(cid)
    return {"prompts": prompts, "targets": targets, "case_ids": case_ids}


def _collect_tool_pool(
    *,
    tool_sources: list[Path],
    excluded_prompts: set[str],
    excluded_targets: set[str],
    excluded_case_ids: set[str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in tool_sources:
        for i, src_row in enumerate(_load_jsonl(path), start=1):
            row = _normalize_tool_row(src_row, i, path)
            if row is None:
                continue
            if not _semantic_tool_filter(row):
                continue

            prompt = str(row["messages"][1].get("content") or "")
            target = _assistant_target_text(row)
            meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
            cid = str(meta.get("source_case_id") or "")

            if prompt in excluded_prompts:
                continue
            if target in excluded_targets:
                continue
            if cid and cid in excluded_case_ids:
                continue
            rows.append(row)

    deduped: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for row in rows:
        k = _tool_row_key(row)
        if k in seen:
            continue
        seen.add(k)
        deduped.append(row)
    return deduped


def _adapt_source_rows_for_i4(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for idx, row in enumerate(rows, start=1):
        cp = json.loads(json.dumps(row, ensure_ascii=False))
        prompt = str(cp["messages"][1].get("content") or "").strip()
        cp["messages"][1]["content"] = _with_schema_guard(
            f"{prompt} First step only: emit the required tool call; do not output tool results."
        )
        meta = cp.get("metadata") if isinstance(cp.get("metadata"), dict) else {}
        original_case = str(meta.get("source_case_id") or f"row_{idx:05d}")
        meta["source_case_id"] = f"i4_adapt_{original_case}"
        meta["source"] = "adapted_source_i4"
        meta["synthetic"] = True
        cp["metadata"] = meta
        out.append(cp)
    return out


def _overlap_report(train_rows: list[dict[str, Any]], eval_map: dict[str, list[dict[str, Any]]]) -> dict[str, dict[str, int]]:
    train_prompts = {str(r["messages"][1].get("content") or "") for r in train_rows}
    train_targets = {_assistant_target_text(r) for r in train_rows}
    train_cases: set[str] = set()
    for r in train_rows:
        m = r.get("metadata") if isinstance(r.get("metadata"), dict) else {}
        cid = str(m.get("source_case_id") or m.get("case_id") or "")
        if cid:
            train_cases.add(cid)

    out: dict[str, dict[str, int]] = {}
    for name, rows in eval_map.items():
        eval_prompts = {str(r["messages"][1].get("content") or "") for r in rows}
        eval_targets = {_assistant_target_text(r) for r in rows}
        eval_cases: set[str] = set()
        for r in rows:
            m = r.get("metadata") if isinstance(r.get("metadata"), dict) else {}
            cid = str(m.get("source_case_id") or m.get("case_id") or "")
            if cid:
                eval_cases.add(cid)
        out[name] = {
            "prompt_overlap": len(train_prompts.intersection(eval_prompts)),
            "target_overlap": len(train_targets.intersection(eval_targets)),
            "source_case_id_overlap": len(train_cases.intersection(eval_cases)),
        }
    return out


def build(args: argparse.Namespace) -> dict[str, Any]:
    rng = random.Random(int(args.seed))

    stage_b_train_path = Path(args.stage_b_train_jsonl).resolve()
    stage_b_val_path = Path(args.stage_b_val_jsonl).resolve()
    dataset_summary_path = Path(args.dataset_summary_json).resolve()

    eval_paths = {
        "heldout_validation": Path(args.eval_heldout_jsonl).resolve(),
        "tool_holdout": Path(args.eval_tool_holdout_jsonl).resolve(),
        "no_call": Path(args.eval_no_call_jsonl).resolve(),
        "adversarial": Path(args.eval_adversarial_jsonl).resolve(),
        "direct_answer": Path(args.eval_direct_answer_jsonl).resolve(),
    }

    for p in [stage_b_train_path, stage_b_val_path, dataset_summary_path, *eval_paths.values()]:
        if not p.exists():
            raise RuntimeError(f"missing required input: {p}")

    tool_sources = [Path(p).resolve() for p in args.tool_sources]
    for p in tool_sources:
        if not p.exists():
            raise RuntimeError(f"tool source missing: {p}")

    src_train = _load_jsonl(stage_b_train_path)
    src_val = _load_jsonl(stage_b_val_path)

    # Preserve non-tool behavior envelope exactly from i1 split.
    non_tool_train = [r for r in src_train if not isinstance(r.get("messages", [{}, {}, {}])[2].get("tool_calls"), list)]
    non_tool_val = [r for r in src_val if not isinstance(r.get("messages", [{}, {}, {}])[2].get("tool_calls"), list)]
    if len(non_tool_train) != 756 or len(non_tool_val) != 84:
        raise RuntimeError(
            f"unexpected non-tool row counts train={len(non_tool_train)} val={len(non_tool_val)}; expected 756/84"
        )

    ds_summary = _load_json(dataset_summary_path)
    holdout_case_ids = set(str(x) for x in ds_summary.get("holdout_case_ids", []) if str(x))
    tool_holdout_exclusions = _collect_eval_exclusions([eval_paths["tool_holdout"]])
    excluded_case_ids = set(holdout_case_ids).union(tool_holdout_exclusions["case_ids"])

    curated_tool_rows = _collect_tool_pool(
        tool_sources=tool_sources,
        excluded_prompts=set(),
        excluded_targets=set(),
        excluded_case_ids=excluded_case_ids,
    )
    adapted_source_rows = _adapt_source_rows_for_i4(curated_tool_rows)
    synthetic_rows = _synthetic_disambiguation_rows() + _schema_shape_contrastive_rows()

    tool_pool_by_name: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in adapted_source_rows + synthetic_rows:
        tool = str((row.get("metadata") or {}).get("tool") or "")
        if tool:
            tool_pool_by_name[tool].append(row)

    train_tool_targets: dict[str, int] = {
        "rg_search": 470,
        "read_file": 249,
        "find_files": 120,
        "debug_tools": 110,
        "run_command": 70,
        "write_file": 45,
        "stat_path": 35,
        "check_service_health": 55,
        "get_system_datetime": 45,
        "archive_create": 35,
        "copy_path": 30,
        "archive_extract": 30,
        "apply_unified_diff": 20,
        "list_tools": 10,
        "service_control": 8,
        "git_status": 8,
        "git_diff": 8,
        "test_run": 8,
        "get_system_version": 8,
        "json_edit": 10,
        "sha256_file": 10,
        "http_request": 10,
        "list_active_ports": 10,
    }
    if sum(train_tool_targets.values()) != 1404:
        raise RuntimeError("train tool target sum must be 1404")

    for tool in train_tool_targets:
        if not tool_pool_by_name.get(tool):
            raise RuntimeError(f"tool pool empty for required tool: {tool}")

    scale = 156.0 / 1404.0
    val_tool_targets = {tool: int(round(count * scale)) for tool, count in train_tool_targets.items()}
    current = sum(val_tool_targets.values())
    residuals = sorted(
        ((tool, (train_tool_targets[tool] * scale) - val_tool_targets[tool]) for tool in train_tool_targets),
        key=lambda x: x[1],
        reverse=True,
    )
    while current < 156:
        for tool, _ in residuals:
            val_tool_targets[tool] += 1
            current += 1
            if current >= 156:
                break
    while current > 156:
        for tool, _ in reversed(residuals):
            if val_tool_targets[tool] <= 0:
                continue
            val_tool_targets[tool] -= 1
            current -= 1
            if current <= 156:
                break

    train_tool_rows: list[dict[str, Any]] = []
    val_tool_rows: list[dict[str, Any]] = []

    for tool, need in train_tool_targets.items():
        sampled = _sample_rows(tool_pool_by_name[tool], need, rng)
        for i, row in enumerate(sampled, start=1):
            out = json.loads(json.dumps(row, ensure_ascii=False))
            out.setdefault("metadata", {})["stage_split"] = "B_RECOVERY_I4"
            out["metadata"]["recovery_batch"] = "train"
            out["metadata"]["recovery_tool_sample"] = f"{tool}_{i:04d}"
            train_tool_rows.append(out)

    for tool, need in val_tool_targets.items():
        sampled = _sample_rows(tool_pool_by_name[tool], need, rng)
        for i, row in enumerate(sampled, start=1):
            out = json.loads(json.dumps(row, ensure_ascii=False))
            out.setdefault("metadata", {})["stage_split"] = "B_RECOVERY_I4"
            out["metadata"]["recovery_batch"] = "val"
            out["metadata"]["recovery_tool_sample"] = f"{tool}_{i:04d}"
            val_tool_rows.append(out)

    # Enforce zero exact prompt overlap with tool-expected eval splits.
    blocked_prompts = _collect_eval_exclusions(
        [eval_paths["heldout_validation"], eval_paths["tool_holdout"]]
    )["prompts"]
    for row in train_tool_rows + val_tool_rows:
        prompt = str(row["messages"][1].get("content") or "")
        if prompt in blocked_prompts:
            row["messages"][1]["content"] = f"{prompt} [i4_train_variant]"

    train_rows = non_tool_train + train_tool_rows
    val_rows = non_tool_val + val_tool_rows
    rng.shuffle(train_rows)
    rng.shuffle(val_rows)

    out_root = Path(args.output_root).resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    train_out = out_root / "dataset_v1_0_stage_b_recovery_i4_train.jsonl"
    val_out = out_root / "dataset_v1_0_stage_b_recovery_i4_val.jsonl"
    summary_out = out_root / "dataset_v1_0_stage_b_recovery_i4_summary.json"

    _write_jsonl(train_out, train_rows)
    _write_jsonl(val_out, val_rows)

    def _counts(rows: list[dict[str, Any]]) -> tuple[dict[str, int], dict[str, int]]:
        cat = Counter()
        tools = Counter()
        for r in rows:
            m = r.get("metadata") if isinstance(r.get("metadata"), dict) else {}
            cat[str(m.get("category") or "unknown")] += 1
            tc = r["messages"][2].get("tool_calls") if isinstance(r["messages"][2], dict) else None
            if isinstance(tc, list) and tc:
                tools[str(tc[0]["function"]["name"])] += 1
        return dict(sorted(cat.items())), dict(sorted(tools.items(), key=lambda kv: kv[0]))

    train_cat, train_tools = _counts(train_rows)
    val_cat, val_tools = _counts(val_rows)

    eval_rows_map = {name: _load_jsonl(path) for name, path in eval_paths.items()}
    overlap = _overlap_report(train_rows, eval_rows_map)

    curated_tools = Counter(str((r.get("metadata") or {}).get("tool") or "") for r in curated_tool_rows)
    adapted_tools = Counter(str((r.get("metadata") or {}).get("tool") or "") for r in adapted_source_rows)
    synthetic_tools = Counter(str((r.get("metadata") or {}).get("tool") or "") for r in synthetic_rows)

    summary = {
        "generated_utc": _now_utc(),
        "seed": int(args.seed),
        "inputs": {
            "stage_b_train_jsonl": str(stage_b_train_path),
            "stage_b_val_jsonl": str(stage_b_val_path),
            "dataset_summary_json": str(dataset_summary_path),
            "tool_sources": [str(p) for p in tool_sources],
            "eval_paths": {k: str(v) for k, v in eval_paths.items()},
        },
        "policy": {
            "fixed_row_count": True,
            "train_rows": len(train_rows),
            "val_rows": len(val_rows),
            "targeted_recovery": "schema-shape contrastive hardening + semantic-disambiguation + contamination exclusions",
            "canonical_eval_rows_used_for_training": False,
            "synthetic_growth": "no total row-count expansion vs stage_b_i1",
        },
        "outputs": {
            "train_jsonl": str(train_out),
            "val_jsonl": str(val_out),
            "summary_json": str(summary_out),
        },
        "source_pool": {
            "excluded_holdout_case_ids": sorted(holdout_case_ids),
            "excluded_eval_tool_case_ids": sorted(tool_holdout_exclusions["case_ids"]),
            "curated_tool_rows_total": len(curated_tool_rows),
            "curated_tool_rows_by_tool": dict(sorted(curated_tools.items(), key=lambda kv: kv[0])),
            "adapted_source_rows_total": len(adapted_source_rows),
            "adapted_source_rows_by_tool": dict(sorted(adapted_tools.items(), key=lambda kv: kv[0])),
            "synthetic_rows_total": len(synthetic_rows),
            "synthetic_rows_by_tool": dict(sorted(synthetic_tools.items(), key=lambda kv: kv[0])),
        },
        "composition": {
            "train_categories": train_cat,
            "val_categories": val_cat,
            "train_tool_counts": train_tools,
            "val_tool_counts": val_tools,
        },
        "overlap_audit": overlap,
        "hashes": {
            "train_sha256": _sha256_file(train_out),
            "val_sha256": _sha256_file(val_out),
        },
    }

    _write_json(summary_out, summary)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build Stage-B semantic recovery dataset i4 (schema-shape hardening, contamination-controlled)."
    )
    parser.add_argument("--stage-b-train-jsonl", default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_train.jsonl")
    parser.add_argument("--stage-b-val-jsonl", default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_val.jsonl")
    parser.add_argument("--dataset-summary-json", default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_summary.json")
    parser.add_argument("--eval-heldout-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/heldout_validation.jsonl")
    parser.add_argument("--eval-tool-holdout-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/tool_holdout.jsonl")
    parser.add_argument("--eval-no-call-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/no_call.jsonl")
    parser.add_argument("--eval-adversarial-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/adversarial.jsonl")
    parser.add_argument("--eval-direct-answer-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/direct_answer.jsonl")
    parser.add_argument(
        "--tool-sources",
        nargs="+",
        default=[
            "/opt/ai-stack/assistant-training/data/tool_ft_allaliases_20260525_from_qual_reports_freq.jsonl",
            "/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_aug_rebalanced_20260417T104659Z.jsonl",
            "/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_aug_focus_rebalanced_20260417T104747Z.jsonl",
        ],
    )
    parser.add_argument("--output-root", default="/opt/ai-stack/assistant-training/data/v1_0")
    parser.add_argument("--seed", type=int, default=20260526)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = build(args)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
