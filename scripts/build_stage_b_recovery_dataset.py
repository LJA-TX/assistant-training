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


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def _canonical_json_text(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True)


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


def _normalize_tool_row(row: dict[str, Any], row_idx: int, source_path: Path) -> dict[str, Any] | None:
    msgs = row.get("messages")
    if not isinstance(msgs, list) or len(msgs) < 3:
        return None
    if not isinstance(msgs[0], dict) or not isinstance(msgs[1], dict) or not isinstance(msgs[2], dict):
        return None
    if msgs[0].get("role") != "system" or msgs[1].get("role") != "user" or msgs[2].get("role") != "assistant":
        return None

    assistant = dict(msgs[2])
    tool_calls = assistant.get("tool_calls")
    if not isinstance(tool_calls, list) or len(tool_calls) < 1:
        return None

    normalized_calls: list[dict[str, Any]] = []
    for i, call in enumerate(tool_calls, start=1):
        if not isinstance(call, dict):
            return None
        fn = call.get("function")
        if not isinstance(fn, dict):
            return None
        name = fn.get("name")
        raw_args = fn.get("arguments")
        if not isinstance(name, str) or not name.strip():
            return None

        parsed_args: dict[str, Any] | None = None
        if isinstance(raw_args, str):
            try:
                obj = json.loads(raw_args)
            except Exception:
                return None
            if not isinstance(obj, dict):
                return None
            parsed_args = obj
        elif isinstance(raw_args, dict):
            parsed_args = raw_args
        else:
            return None

        normalized_calls.append(
            {
                "id": str(call.get("id") or f"call_{i}"),
                "type": "function",
                "function": {
                    "name": name.strip(),
                    "arguments": _canonical_json_text(parsed_args),
                },
            }
        )

    meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    source_case_id = str(meta.get("source_case_id") or meta.get("case_id") or "").strip()
    if not source_case_id:
        source_case_id = f"{source_path.stem}_row_{row_idx:06d}"

    tool_name = normalized_calls[0]["function"]["name"]

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
            "tool": tool_name,
            "synthetic": False,
        },
    }


def _tool_row_key(row: dict[str, Any]) -> tuple[str, str, str]:
    msgs = row["messages"]
    user_text = str(msgs[1].get("content") or "")
    tc = msgs[2]["tool_calls"][0]
    fn = tc["function"]
    return (
        user_text,
        str(fn.get("name") or ""),
        str(fn.get("arguments") or ""),
    )


def _semantic_tool_filter(row: dict[str, Any]) -> bool:
    prompt = str(row["messages"][1].get("content") or "").lower()
    tool = str((row.get("metadata") or {}).get("tool") or "")

    def has_any(words: list[str]) -> bool:
        return any(w in prompt for w in words)

    if tool == "rg_search":
        # Reject misleading "read/open/retrieve lines" phrasing for rg_search unless explicit grep/search cues exist.
        has_read_verb = has_any(["read ", "open ", "retrieve ", "show "]) and "lines" in prompt
        has_search_cue = has_any(["rg_search", "pattern", "regex", "match", "grep", "search"])
        return has_search_cue and not (has_read_verb and "rg_search" not in prompt)

    if tool == "read_file":
        return has_any(["read ", "open ", "retrieve ", "show ", "line", "lines"])

    if tool == "find_files":
        return has_any(["find_files", "root", "pattern", "find file", "find files"])

    if tool == "stat_path":
        return has_any(["stat_path", "exists", "type only", "exists/type", "metadata"])

    if tool == "write_file":
        return has_any(["write_file", "append", "overwrite", "content", "create"])

    if tool == "run_command":
        return has_any(["run_command", "execute", "command", "stdout", "run "])

    return True


def _make_tool_row(*, prompt: str, tool: str, args: dict[str, Any], case_id: str, source: str, synthetic: bool) -> dict[str, Any]:
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_TOOL},
            {"role": "user", "content": prompt},
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": "call_1",
                        "type": "function",
                        "function": {
                            "name": tool,
                            "arguments": _canonical_json_text(args),
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


def _contrastive_rows() -> list[dict[str, Any]]:
    items = [
        (
            "/opt/ai-stack/runtimes/assistant-runtime/server/service.py",
            "/opt/ai-stack/runtimes/assistant-runtime/server",
            "service.py",
            "def create_app",
            1,
            25,
        ),
        (
            "/opt/ai-stack/runtimes/assistant-runtime/server/agent.py",
            "/opt/ai-stack/runtimes/assistant-runtime/server",
            "agent.py",
            "_validate_tool_arguments",
            1080,
            1105,
        ),
        (
            "/opt/ai-stack/runtimes/assistant-runtime/server/tools.py",
            "/opt/ai-stack/runtimes/assistant-runtime/server",
            "tools.py",
            "def rg_search",
            1,
            60,
        ),
        (
            "/mnt/services/runtimes/assistant-runtime/server/service.py",
            "/mnt/services/runtimes/assistant-runtime/server",
            "service.py",
            "def create_app",
            1,
            25,
        ),
        (
            "/mnt/services/runtimes/assistant-runtime/server/agent.py",
            "/mnt/services/runtimes/assistant-runtime/server",
            "agent.py",
            "_coerce_tool_arguments",
            1500,
            1560,
        ),
        (
            "/mnt/services/runtimes/assistant-runtime/server/tools.py",
            "/mnt/services/runtimes/assistant-runtime/server",
            "tools.py",
            "def read_file",
            1,
            80,
        ),
    ]

    rows: list[dict[str, Any]] = []
    for idx, (path, root, filename, pattern, line_start, line_end) in enumerate(items, start=1):
        rows.append(
            _make_tool_row(
                prompt=f'Use rg_search in {path} for pattern "{pattern}" and report match_count only.',
                tool="rg_search",
                args={"path": path, "pattern": pattern},
                case_id=f"contrast_rg_{idx:03d}",
                source="contrastive_semantic_v1",
                synthetic=True,
            )
        )
        rows.append(
            _make_tool_row(
                prompt=f"Read {path} lines {line_start}-{line_end} and report one symbol name only.",
                tool="read_file",
                args={"path": path, "line_start": line_start, "line_end": line_end},
                case_id=f"contrast_read_{idx:03d}",
                source="contrastive_semantic_v1",
                synthetic=True,
            )
        )
        rows.append(
            _make_tool_row(
                prompt=f"Use stat_path on {path} and report exists/type only.",
                tool="stat_path",
                args={"path": path},
                case_id=f"contrast_stat_{idx:03d}",
                source="contrastive_semantic_v1",
                synthetic=True,
            )
        )
        rows.append(
            _make_tool_row(
                prompt=f"Use find_files with root {root} and pattern {filename}. Report match_count only.",
                tool="find_files",
                args={"root": root, "pattern": filename},
                case_id=f"contrast_find_{idx:03d}",
                source="contrastive_semantic_v1",
                synthetic=True,
            )
        )

    return rows


def _sample_rows(rows: list[dict[str, Any]], n: int, rng: random.Random) -> list[dict[str, Any]]:
    if n <= 0:
        return []
    if not rows:
        raise RuntimeError("cannot sample from empty rows")
    return [rows[rng.randrange(len(rows))] for _ in range(n)]


def _collect_tool_pool(tool_sources: list[Path]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for path in tool_sources:
        rows = _load_jsonl(path)
        for i, row in enumerate(rows, start=1):
            normalized = _normalize_tool_row(row, i, path)
            if normalized is None:
                continue
            if _semantic_tool_filter(normalized):
                out.append(normalized)

    deduped: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for row in out:
        key = _tool_row_key(row)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def build(args: argparse.Namespace) -> dict[str, Any]:
    rng = random.Random(int(args.seed))

    stage_b_train_path = Path(args.stage_b_train_jsonl).resolve()
    stage_b_val_path = Path(args.stage_b_val_jsonl).resolve()
    if not stage_b_train_path.exists() or not stage_b_val_path.exists():
        raise RuntimeError("stage-b source split(s) missing")

    tool_sources = [Path(p).resolve() for p in args.tool_sources]
    for p in tool_sources:
        if not p.exists():
            raise RuntimeError(f"tool source missing: {p}")

    src_train = _load_jsonl(stage_b_train_path)
    src_val = _load_jsonl(stage_b_val_path)

    non_tool_train = [r for r in src_train if not isinstance(r.get("messages", [{}, {}, {}])[2].get("tool_calls"), list)]
    non_tool_val = [r for r in src_val if not isinstance(r.get("messages", [{}, {}, {}])[2].get("tool_calls"), list)]

    if len(non_tool_train) != 756 or len(non_tool_val) != 84:
        raise RuntimeError(
            f"unexpected non-tool row counts train={len(non_tool_train)} val={len(non_tool_val)}; expected 756/84"
        )

    curated_tool_rows = _collect_tool_pool(tool_sources)
    contrastive = _contrastive_rows()

    tool_pool_by_name: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in curated_tool_rows + contrastive:
        tool = str((row.get("metadata") or {}).get("tool") or "")
        if not tool:
            continue
        tool_pool_by_name[tool].append(row)

    train_tool_targets: dict[str, int] = {
        "rg_search": 520,
        "read_file": 270,
        "find_files": 120,
        "debug_tools": 70,
        "check_service_health": 60,
        "get_system_datetime": 60,
        "archive_create": 40,
        "write_file": 35,
        "run_command": 35,
        "copy_path": 35,
        "archive_extract": 35,
        "stat_path": 25,
        "apply_unified_diff": 25,
        "list_tools": 7,
        "service_control": 7,
        "git_status": 7,
        "git_diff": 7,
        "test_run": 7,
        "get_system_version": 7,
        "json_edit": 8,
        "sha256_file": 8,
        "http_request": 8,
        "list_active_ports": 8,
    }

    if sum(train_tool_targets.values()) != 1404:
        raise RuntimeError("train tool target sum must be 1404")

    scale = 156.0 / 1404.0
    val_tool_targets: dict[str, int] = {tool: int(round(count * scale)) for tool, count in train_tool_targets.items()}

    # Force exact val target count with deterministic adjustment by largest residuals.
    current_val_sum = sum(val_tool_targets.values())
    residuals = sorted(
        ((tool, (train_tool_targets[tool] * scale) - val_tool_targets[tool]) for tool in train_tool_targets),
        key=lambda x: x[1],
        reverse=True,
    )
    while current_val_sum < 156:
        for tool, _ in residuals:
            val_tool_targets[tool] += 1
            current_val_sum += 1
            if current_val_sum >= 156:
                break
    while current_val_sum > 156:
        for tool, _ in reversed(residuals):
            if val_tool_targets[tool] <= 0:
                continue
            val_tool_targets[tool] -= 1
            current_val_sum -= 1
            if current_val_sum <= 156:
                break

    if sum(val_tool_targets.values()) != 156:
        raise RuntimeError("val tool target sum must be 156")

    train_tool_rows: list[dict[str, Any]] = []
    val_tool_rows: list[dict[str, Any]] = []

    for tool, need in train_tool_targets.items():
        pool = tool_pool_by_name.get(tool, [])
        if not pool:
            raise RuntimeError(f"no pool rows for tool {tool}")
        sampled = _sample_rows(pool, need, rng)
        for idx, row in enumerate(sampled, start=1):
            out = json.loads(json.dumps(row, ensure_ascii=False))
            out.setdefault("metadata", {})["stage_split"] = "B_RECOVERY"
            out["metadata"]["recovery_batch"] = "train"
            out["metadata"]["recovery_tool_sample"] = f"{tool}_{idx:04d}"
            train_tool_rows.append(out)

    for tool, need in val_tool_targets.items():
        pool = tool_pool_by_name.get(tool, [])
        if not pool:
            raise RuntimeError(f"no pool rows for tool {tool}")
        sampled = _sample_rows(pool, need, rng)
        for idx, row in enumerate(sampled, start=1):
            out = json.loads(json.dumps(row, ensure_ascii=False))
            out.setdefault("metadata", {})["stage_split"] = "B_RECOVERY"
            out["metadata"]["recovery_batch"] = "val"
            out["metadata"]["recovery_tool_sample"] = f"{tool}_{idx:04d}"
            val_tool_rows.append(out)

    train_rows = non_tool_train + train_tool_rows
    val_rows = non_tool_val + val_tool_rows
    rng.shuffle(train_rows)
    rng.shuffle(val_rows)

    out_root = Path(args.output_root).resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    train_out = out_root / "dataset_v1_0_stage_b_recovery_i2_train.jsonl"
    val_out = out_root / "dataset_v1_0_stage_b_recovery_i2_val.jsonl"
    summary_out = out_root / "dataset_v1_0_stage_b_recovery_i2_summary.json"

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

    curated_tools = Counter(str((r.get("metadata") or {}).get("tool") or "") for r in curated_tool_rows)

    summary = {
        "generated_utc": _now_utc(),
        "seed": int(args.seed),
        "inputs": {
            "stage_b_train_jsonl": str(stage_b_train_path),
            "stage_b_val_jsonl": str(stage_b_val_path),
            "tool_sources": [str(p) for p in tool_sources],
        },
        "policy": {
            "fixed_row_count": True,
            "train_rows": len(train_rows),
            "val_rows": len(val_rows),
            "targeted_recovery": "multi-tool rebalance + contrastive semantic examples",
            "canonical_eval_rows_used_for_training": False,
            "synthetic_growth": "no total row-count expansion vs stage_b_i1",
        },
        "outputs": {
            "train_jsonl": str(train_out),
            "val_jsonl": str(val_out),
            "summary_json": str(summary_out),
        },
        "source_pool": {
            "curated_tool_rows_total": len(curated_tool_rows),
            "curated_tool_rows_by_tool": dict(sorted(curated_tools.items(), key=lambda kv: kv[0])),
            "contrastive_rows_total": len(contrastive),
        },
        "composition": {
            "train_categories": train_cat,
            "val_categories": val_cat,
            "train_tool_counts": train_tools,
            "val_tool_counts": val_tools,
        },
        "hashes": {
            "train_sha256": _sha256_file(train_out),
            "val_sha256": _sha256_file(val_out),
        },
    }

    _write_json(summary_out, summary)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Stage-B semantic recovery dataset i2.")
    parser.add_argument("--stage-b-train-jsonl", default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_train.jsonl")
    parser.add_argument("--stage-b-val-jsonl", default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_val.jsonl")
    parser.add_argument(
        "--tool-sources",
        nargs="+",
        default=[
            "/opt/ai-stack/assistant-training/data/tool_ft_allaliases_20260525_from_qual_reports_freq.jsonl",
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
