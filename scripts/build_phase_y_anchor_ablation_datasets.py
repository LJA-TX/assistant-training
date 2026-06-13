#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_dataset_v1_1 import (  # noqa: E402
    SourceRow,
    _load_source_rows,
    _prompt_shell,
    _source_row_lineage,
    _tool_args,
    _tool_groups,
    _sha256_file,
)


SYSTEM_EXACT_TOOL_REQUEST = (
    "Use ONLY the exact tool requested. Keep final answer concise. If a tool result already answers the task, "
    "stop and finalize. Return only strict JSON tool calls when a tool is required. Do not add prose, markdown, "
    "or shell blocks."
)

ANCHOR_TOOLS = ["rg_search", "read_file", "find_files", "debug_tools", "run_command"]
ALL_TOOL_FAMILIES = [
    "apply_unified_diff",
    "archive_create",
    "archive_extract",
    "check_service_health",
    "copy_path",
    "debug_tools",
    "find_files",
    "get_system_datetime",
    "get_system_version",
    "git_diff",
    "git_status",
    "http_request",
    "json_edit",
    "list_active_ports",
    "list_dir",
    "list_models",
    "list_tools",
    "move_path",
    "read_file",
    "rg_search",
    "run_command",
    "service_control",
    "sha256_file",
    "stat_path",
    "test_run",
    "write_file",
]

TRAIN_ROWS = 2160
VAL_ROWS = 240
TRAIN_TOOL_POSITIVE_ROWS = 1393
TRAIN_SAFETY_ROWS = 767
VAL_TOOL_POSITIVE_ROWS = 155
VAL_SAFETY_ROWS = 85

BASE_DIR = Path("data/v1_2")
SOURCE_POOL = Path("data/tool_ft_allaliases_20260525_from_qual_reports_freq.jsonl")
BASE_TRAIN = BASE_DIR / "dataset_v1_2_train.jsonl"
BASE_VAL = BASE_DIR / "dataset_v1_2_val.jsonl"
EVAL_ROOT = Path("evals/data/canonical_v1")

ARM_SPECS = {
    "control": {
        "anchor_rows": 726,
        "long_tail_rows": 667,
        "prefix": "dataset_v1_2_phase_y_control",
    },
    "treatment_a": {
        "anchor_rows": 819,
        "long_tail_rows": 574,
        "prefix": "dataset_v1_2_phase_y_treatment_a",
    },
    "treatment_b": {
        "anchor_rows": 912,
        "long_tail_rows": 481,
        "prefix": "dataset_v1_2_phase_y_treatment_b",
    },
    "treatment_c": {
        "anchor_rows": 1011,
        "long_tail_rows": 382,
        "prefix": "dataset_v1_2_phase_y_treatment_c",
    },
}


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"expected object JSON at {path}")
    return payload


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            raw = line.strip()
            if not raw:
                continue
            try:
                obj = json.loads(raw)
            except Exception as exc:  # pragma: no cover - invalid repo data is fatal
                raise RuntimeError(f"invalid JSONL at {path}:{line_no}: {exc}") from exc
            if not isinstance(obj, dict):
                raise RuntimeError(f"expected object row at {path}:{line_no}")
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


def _sha1_text(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def _canonical_json_text(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _tool_name(row: dict[str, Any]) -> str:
    meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    return str(meta.get("tool") or meta.get("source_tool") or "").strip()


def _source_rows_by_tool(source_rows: list[SourceRow]) -> dict[str, list[SourceRow]]:
    groups = _tool_groups(source_rows)
    for tool in groups:
        groups[tool].sort(key=lambda row: (row.source_category, row.case_id, row.prompt_sha1, row.target_sha1))
    return groups


def _tool_target_counts(base_counts: dict[str, int], target_total: int) -> dict[str, int]:
    total = sum(base_counts.values())
    if total <= 0:
        raise RuntimeError("base counts must be positive")
    exact = {tool: (count * target_total) / total for tool, count in base_counts.items()}
    counts = {tool: int(math.floor(value)) for tool, value in exact.items()}
    leftover = target_total - sum(counts.values())
    if leftover < 0:
        raise RuntimeError("target rounding underflow")
    remainders = sorted(
        exact.items(),
        key=lambda item: (-(item[1] - math.floor(item[1])), -base_counts[item[0]], item[0]),
    )
    for tool, _ in remainders[:leftover]:
        counts[tool] += 1
    if sum(counts.values()) != target_total:
        raise RuntimeError("target rounding failed to reach desired total")
    return counts


def _build_prompt(tool: str, args: dict[str, Any], slot: int) -> str:
    # Reuse the established prompt shells from the v1.1 builder, but keep the exact cue fixed in the system message.
    return _prompt_shell(tool, "diversity", args, slot)


def _make_tool_row(
    *,
    arm: str,
    tool: str,
    source_row: SourceRow,
    slot: int,
    source_file: str,
) -> dict[str, Any]:
    args = _tool_args(tool, slot)
    prompt = _build_prompt(tool, args, slot)
    source_case_id = f"phase_y_{arm}_{tool}_{source_row.case_id}_{slot:04d}"
    metadata = {
        "category": "tool_positive",
        "source": "phase_y_anchor_ablation",
        "source_file": source_file,
        "source_case_id": source_case_id,
        "tool": tool,
        "synthetic": True,
        "phase_y_arm": arm,
        "phase_y_anchor_family": tool in ANCHOR_TOOLS,
        "phase_y_prompt_style": "exact_tool_request",
        "phase_y_source_category": source_row.source_category,
        "phase_y_source_case_id": source_row.case_id,
        "phase_y_source_prompt_sha1": source_row.prompt_sha1,
        "phase_y_source_target_sha1": source_row.target_sha1,
        "phase_y_source_tool": source_row.tool,
        "phase_y_lineage_tag": f"derived_from_{source_row.source_category}",
    }
    metadata.update(_source_row_lineage(source_row))
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_EXACT_TOOL_REQUEST},
            {"role": "user", "content": prompt},
            {"role": "assistant", "tool_calls": [{"type": "function", "function": {"name": tool, "arguments": args}}]},
        ],
        "metadata": metadata,
    }


def _base_train_split(train_rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    tool_positive = [row for row in train_rows if _tool_name(row) and str((row.get("metadata") or {}).get("category") or "") == "tool_positive"]
    non_tool = [row for row in train_rows if str((row.get("metadata") or {}).get("category") or "") != "tool_positive"]
    return tool_positive, non_tool


def _copy_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return json.loads(json.dumps(rows, ensure_ascii=False))


def _category_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counter = Counter()
    for row in rows:
        meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        counter[str(meta.get("category") or "unknown")] += 1
    return dict(sorted(counter.items(), key=lambda kv: kv[0]))


def _tool_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counter = Counter()
    for row in rows:
        meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        if str(meta.get("category") or "") == "tool_positive":
            counter[str(meta.get("tool") or "unknown")] += 1
    return dict(sorted(counter.items(), key=lambda kv: kv[0]))


def _count_tool_families(rows: list[dict[str, Any]]) -> tuple[int, int]:
    tool_positive = 0
    anchor = 0
    for row in rows:
        meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        if str(meta.get("category") or "") == "tool_positive":
            tool_positive += 1
            if str(meta.get("tool") or "") in ANCHOR_TOOLS:
                anchor += 1
    return tool_positive, anchor


def _overlap(candidate_rows: list[dict[str, Any]], eval_rows: list[dict[str, Any]]) -> dict[str, int]:
    def prompt(row: dict[str, Any]) -> str:
        msgs = row.get("messages")
        if not isinstance(msgs, list):
            return ""
        for msg in msgs:
            if isinstance(msg, dict) and msg.get("role") == "user":
                return str(msg.get("content") or "")
        return ""

    def target(row: dict[str, Any]) -> str:
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

    def case_id(row: dict[str, Any]) -> str:
        meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        return str(meta.get("source_case_id") or meta.get("case_id") or "").strip()

    return {
        "prompt_overlap": len({prompt(r) for r in candidate_rows}.intersection({prompt(r) for r in eval_rows})),
        "target_overlap": len({target(r) for r in candidate_rows}.intersection({target(r) for r in eval_rows})),
        "source_case_id_overlap": len({case_id(r) for r in candidate_rows}.intersection({case_id(r) for r in eval_rows})),
    }


def _build_contamination_report(
    train_rows: list[dict[str, Any]],
    val_rows: list[dict[str, Any]],
    eval_map: dict[str, list[dict[str, Any]]],
    dataset_name: str,
) -> dict[str, Any]:
    combined = train_rows + val_rows
    report = {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "dataset": dataset_name,
        "train_overlap": {name: _overlap(train_rows, rows) for name, rows in eval_map.items()},
        "val_overlap": {name: _overlap(val_rows, rows) for name, rows in eval_map.items()},
        "combined_overlap": {name: _overlap(combined, rows) for name, rows in eval_map.items()},
        "blocking_policy": {
            "heldout_tool_holdout_max_allowed_overlap": 0,
            "fail_fast": True,
        },
    }
    return report


def _build_summary(
    *,
    dataset_name: str,
    arm: str,
    target_anchor_rows: int,
    target_long_tail_rows: int,
    source_files: list[Path],
    train_rows: list[dict[str, Any]],
    val_rows: list[dict[str, Any]],
    train_path: Path,
    val_path: Path,
    leakage_path: Path,
    contamination_report: dict[str, Any],
) -> dict[str, Any]:
    combined = train_rows + val_rows
    train_anchor_rows = sum(
        1
        for row in train_rows
        if str((row.get("metadata") or {}).get("category") or "") == "tool_positive"
        and str((row.get("metadata") or {}).get("tool") or "") in ANCHOR_TOOLS
    )
    train_long_tail_rows = sum(
        1
        for row in train_rows
        if str((row.get("metadata") or {}).get("category") or "") == "tool_positive"
        and str((row.get("metadata") or {}).get("tool") or "") not in ANCHOR_TOOLS
    )
    train_tool_positive_rows, _ = _count_tool_families(train_rows)
    val_tool_positive_rows, _ = _count_tool_families(val_rows)
    tool_counts_train = _tool_counts(train_rows)
    tool_counts_val = _tool_counts(val_rows)
    tool_counts_combined = _tool_counts(combined)
    return {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "dataset": dataset_name,
        "arm": arm,
        "source_files": [str(p.resolve()) for p in source_files],
        "arm_targets": {
            "anchor_rows": target_anchor_rows,
            "long_tail_rows": target_long_tail_rows,
            "tool_positive_rows": TRAIN_TOOL_POSITIVE_ROWS,
            "safety_rows": TRAIN_SAFETY_ROWS,
        },
        "row_counts": {
            "train": len(train_rows),
            "val": len(val_rows),
            "total": len(combined),
        },
        "train_category_counts": _category_counts(train_rows),
        "val_category_counts": _category_counts(val_rows),
        "combined_category_counts": _category_counts(combined),
        "train_tool_counts": tool_counts_train,
        "val_tool_counts": tool_counts_val,
        "combined_tool_counts": tool_counts_combined,
        "phase_y_component_counts": {
            "anchor": train_anchor_rows,
            "long_tail": train_long_tail_rows,
            "safety": len(train_rows) - train_tool_positive_rows,
        },
        "phase_y_validation_component_counts": {
            "anchor": sum(
                1
                for row in val_rows
                if str((row.get("metadata") or {}).get("category") or "") == "tool_positive"
                and str((row.get("metadata") or {}).get("tool") or "") in ANCHOR_TOOLS
            ),
            "long_tail": sum(
                1
                for row in val_rows
                if str((row.get("metadata") or {}).get("category") or "") == "tool_positive"
                and str((row.get("metadata") or {}).get("tool") or "") not in ANCHOR_TOOLS
            ),
            "safety": len(val_rows) - val_tool_positive_rows,
        },
        "hashes": {
            "train_sha256": _sha256_file(train_path),
            "val_sha256": _sha256_file(val_path),
        },
        "contamination_report_path": str(leakage_path),
    }


def _readiness_assessment(summary: dict[str, Any], contamination_report: dict[str, Any]) -> dict[str, Any]:
    combined_overlap = contamination_report.get("combined_overlap", {})
    required_zero = {"prompt_overlap": 0, "target_overlap": 0, "source_case_id_overlap": 0}

    contamination_zero = all(combined_overlap.get(name, {}) == required_zero for name in [
        "heldout_validation",
        "tool_holdout",
        "no_call",
        "adversarial",
        "direct_answer",
    ])

    train_counts = summary.get("train_category_counts", {})
    tool_rows = int(train_counts.get("tool_positive") or 0)
    safety_rows = int(train_counts.get("runtime_alignment") or 0) + int(train_counts.get("no_call_direct_calibration") or 0) + int(
        train_counts.get("refusal_calibration") or 0
    ) + int(train_counts.get("adversarial_no_call_calibration") or 0)
    tool_counts = summary.get("train_tool_counts", {})
    anchor_rows = sum(int(tool_counts.get(tool) or 0) for tool in ANCHOR_TOOLS)
    long_tail_rows = tool_rows - anchor_rows
    target_anchor_rows = int(summary.get("arm_targets", {}).get("anchor_rows") or 0)
    exact_cue_retained = bool(summary.get("checks", {}).get("exact_tool_request_cue_retained"))
    scaffold_invariant = (
        bool(summary.get("checks", {}).get("scaffold_matches_base_train"))
        and bool(summary.get("checks", {}).get("scaffold_matches_base_val"))
        and int(summary.get("row_counts", {}).get("train") or 0) == TRAIN_ROWS
        and int(summary.get("row_counts", {}).get("val") or 0) == VAL_ROWS
    )
    envelope_valid = bool(summary.get("checks", {}).get("tool_calls_envelope_valid"))
    safety_block_preserved = safety_rows == TRAIN_SAFETY_ROWS
    all_families = bool(summary.get("checks", {}).get("all_tool_families_represented"))
    admissible = (
        contamination_zero
        and exact_cue_retained
        and scaffold_invariant
        and envelope_valid
        and safety_block_preserved
        and anchor_rows == target_anchor_rows
        and all_families
    )

    return {
        "generated_utc": _now_utc(),
        "dataset": summary.get("dataset"),
        "arm": summary.get("arm"),
        "status": "Ready" if admissible else "Not Ready",
        "scientifically_admissible": admissible,
        "checks": {
            "contamination_zero_for_all_eval_splits": contamination_zero,
            "anchor_count_matches_target": anchor_rows == target_anchor_rows,
            "exact_tool_request_cue_retained": exact_cue_retained,
            "scaffold_invariant": scaffold_invariant,
            "tool_calls_envelope_valid": envelope_valid,
            "safety_block_preserved": safety_block_preserved,
            "all_tool_families_represented": all_families,
        },
        "summary": {
            "row_counts": summary.get("row_counts", {}),
            "arm_targets": summary.get("arm_targets", {}),
            "train_category_counts": summary.get("train_category_counts", {}),
            "train_tool_counts_top10": dict(list(summary.get("train_tool_counts", {}).items())[:10]),
            "phase_y_component_counts": summary.get("phase_y_component_counts", {}),
            "phase_y_validation_component_counts": summary.get("phase_y_validation_component_counts", {}),
        },
        "rationale": (
            "Ready: contamination is zero, the cue and scaffold are fixed, the tool_calls envelope is canonical, "
            "the safety block is preserved, and the anchor count matches the arm target."
            if admissible
            else "Not ready: one or more fixed-boundary or contamination checks failed."
        ),
    }


def _build_arm(
    *,
    arm: str,
    arm_spec: dict[str, Any],
    base_train_rows: list[dict[str, Any]],
    base_val_rows: list[dict[str, Any]],
    source_rows: list[SourceRow],
    eval_map: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    train_tool_rows, train_non_tool_rows = _base_train_split(base_train_rows)
    if len(train_tool_rows) != TRAIN_TOOL_POSITIVE_ROWS:
        raise RuntimeError(f"unexpected base tool-positive count: {len(train_tool_rows)}")
    if len(train_non_tool_rows) != TRAIN_SAFETY_ROWS:
        raise RuntimeError(f"unexpected base safety count: {len(train_non_tool_rows)}")

    base_train_counts = Counter(_tool_name(row) for row in train_tool_rows)
    base_anchor_counts = {tool: base_train_counts[tool] for tool in ANCHOR_TOOLS}
    base_long_tail_counts = {tool: base_train_counts[tool] for tool in ALL_TOOL_FAMILIES if tool not in ANCHOR_TOOLS}

    target_anchor_rows = int(arm_spec["anchor_rows"])
    target_long_tail_rows = int(arm_spec["long_tail_rows"])
    target_anchor_counts = _tool_target_counts(base_anchor_counts, target_anchor_rows)
    target_long_tail_counts = _tool_target_counts(base_long_tail_counts, target_long_tail_rows)

    source_by_tool = _source_rows_by_tool(source_rows)
    source_file = str(SOURCE_POOL.resolve())
    tool_rows: list[dict[str, Any]] = []
    exact_cue_retained = True
    envelope_valid = True

    ordered_tools = ANCHOR_TOOLS + [tool for tool in ALL_TOOL_FAMILIES if tool not in ANCHOR_TOOLS]
    for tool in ordered_tools:
        count = target_anchor_counts.get(tool, 0) if tool in ANCHOR_TOOLS else target_long_tail_counts.get(tool, 0)
        tool_sources = source_by_tool.get(tool) or [row for row in source_rows if row.tool == tool]
        if not tool_sources:
            raise RuntimeError(f"no source rows available for tool {tool}")
        for idx in range(count):
            src = tool_sources[idx % len(tool_sources)]
            tool_rows.append(
                _make_tool_row(
                    arm=arm,
                    tool=tool,
                    source_row=src,
                    slot=idx,
                    source_file=source_file,
                )
            )
            if tool_rows[-1]["messages"][0]["content"] != SYSTEM_EXACT_TOOL_REQUEST:
                exact_cue_retained = False
            assistant = tool_rows[-1]["messages"][2]
            if not (
                isinstance(assistant, dict)
                and isinstance(assistant.get("tool_calls"), list)
                and len(assistant["tool_calls"]) == 1
            ):
                envelope_valid = False

    if len(tool_rows) != TRAIN_TOOL_POSITIVE_ROWS:
        raise RuntimeError(f"{arm}: expected {TRAIN_TOOL_POSITIVE_ROWS} tool rows, got {len(tool_rows)}")

    generated_iter = iter(tool_rows)
    train_rows: list[dict[str, Any]] = []
    scaffold_matches_base_train = True
    for base_row in base_train_rows:
        category = str((base_row.get("metadata") or {}).get("category") or "")
        if category == "tool_positive":
            new_row = next(generated_iter)
            train_rows.append(new_row)
        else:
            train_rows.append(base_row)
            if base_row != train_rows[-1]:
                scaffold_matches_base_train = False
    if next(generated_iter, None) is not None:
        raise RuntimeError(f"{arm}: unused tool rows remain after replacement")

    val_rows = _copy_rows(base_val_rows)
    scaffold_matches_base_val = val_rows == base_val_rows

    out_root = BASE_DIR.resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    prefix = str(arm_spec["prefix"])
    train_path = out_root / f"{prefix}_train.jsonl"
    val_path = out_root / f"{prefix}_val.jsonl"
    leakage_path = out_root / f"{prefix}_leakage_report.json"
    summary_path = out_root / f"{prefix}_summary.json"
    readiness_path = out_root / f"{prefix}_readiness_assessment.json"

    _write_jsonl(train_path, train_rows)
    _write_jsonl(val_path, val_rows)

    contamination_report = _build_contamination_report(train_rows, val_rows, eval_map, dataset_name=prefix)
    contamination_report["report_path"] = str(leakage_path)
    _write_json(leakage_path, contamination_report)

    summary = _build_summary(
        dataset_name=prefix,
        arm=arm,
        target_anchor_rows=target_anchor_rows,
        target_long_tail_rows=target_long_tail_rows,
        source_files=[SOURCE_POOL],
        train_rows=train_rows,
        val_rows=val_rows,
        train_path=train_path,
        val_path=val_path,
        leakage_path=leakage_path,
        contamination_report=contamination_report,
    )
    summary["checks"] = {
        "exact_tool_request_cue_retained": exact_cue_retained,
        "tool_calls_envelope_valid": envelope_valid,
        "scaffold_matches_base_train": scaffold_matches_base_train,
        "scaffold_matches_base_val": scaffold_matches_base_val,
        "all_tool_families_represented": all(tool in _tool_counts(train_rows) for tool in ALL_TOOL_FAMILIES),
    }
    _write_json(summary_path, summary)

    readiness = _readiness_assessment(summary, contamination_report)
    _write_json(readiness_path, readiness)

    return {
        "arm": arm,
        "train_path": str(train_path),
        "val_path": str(val_path),
        "summary_path": str(summary_path),
        "leakage_path": str(leakage_path),
        "readiness_path": str(readiness_path),
        "summary": summary,
        "readiness": readiness,
        "contamination_report": contamination_report,
    }


def build_all() -> dict[str, Any]:
    if not SOURCE_POOL.exists():
        raise RuntimeError(f"missing source pool: {SOURCE_POOL}")
    if not BASE_TRAIN.exists():
        raise RuntimeError(f"missing base train dataset: {BASE_TRAIN}")
    if not BASE_VAL.exists():
        raise RuntimeError(f"missing base val dataset: {BASE_VAL}")

    base_train_rows = _read_jsonl(BASE_TRAIN)
    base_val_rows = _read_jsonl(BASE_VAL)
    source_rows = _load_source_rows([SOURCE_POOL])
    eval_map = {
        name: _read_jsonl((EVAL_ROOT / f"{name}.jsonl").resolve())
        for name in ["heldout_validation", "tool_holdout", "no_call", "adversarial", "direct_answer"]
    }

    results = {}
    for arm, spec in ARM_SPECS.items():
        results[arm] = _build_arm(
            arm=arm,
            arm_spec=spec,
            base_train_rows=base_train_rows,
            base_val_rows=base_val_rows,
            source_rows=source_rows,
            eval_map=eval_map,
        )

    overview = {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "source_pool": str(SOURCE_POOL.resolve()),
        "base_train": str(BASE_TRAIN.resolve()),
        "base_val": str(BASE_VAL.resolve()),
        "arms": {
            arm: {
                "anchor_rows": ARM_SPECS[arm]["anchor_rows"],
                "long_tail_rows": ARM_SPECS[arm]["long_tail_rows"],
                "prefix": ARM_SPECS[arm]["prefix"],
            }
            for arm in ARM_SPECS
        },
        "outputs": {
            arm: {
                "train": results[arm]["train_path"],
                "val": results[arm]["val_path"],
                "summary": results[arm]["summary_path"],
                "leakage": results[arm]["leakage_path"],
                "readiness": results[arm]["readiness_path"],
            }
            for arm in results
        },
    }

    overview_path = BASE_DIR / "dataset_v1_2_phase_y_overview.json"
    _write_json(overview_path, overview)
    return {"overview": overview, "overview_path": str(overview_path), "results": results}


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Phase Y anchor-concentration ablation datasets.")
    parser.add_argument("--dry-run", action="store_true", help="Validate inputs and compute target counts without writing files.")
    args = parser.parse_args()

    if args.dry_run:
        base_train_rows = _read_jsonl(BASE_TRAIN)
        base_tool_rows = [row for row in base_train_rows if str((row.get("metadata") or {}).get("category") or "") == "tool_positive"]
        base_counts = Counter(str((row.get("metadata") or {}).get("tool") or "") for row in base_tool_rows)
        print(json.dumps({"base_counts": dict(sorted(base_counts.items())), "row_counts": len(base_train_rows)}, indent=2))
        return

    result = build_all()
    print(json.dumps(result["overview"], indent=2))


if __name__ == "__main__":
    main()
