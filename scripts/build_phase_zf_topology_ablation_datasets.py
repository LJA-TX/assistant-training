#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_dataset_v1_1 import SourceRow, _load_source_rows, _prompt_shell, _sha256_file, _tool_args, _source_row_lineage


BASE_DIR = ROOT / "data" / "v1_2"
BASE_TRAIN = BASE_DIR / "dataset_v1_2_phase_y_control_train.jsonl"
BASE_VAL = BASE_DIR / "dataset_v1_2_phase_y_control_val.jsonl"
SOURCE_POOL = ROOT / "data" / "tool_ft_allaliases_20260525_from_qual_reports_freq.jsonl"
EVAL_ROOT = ROOT / "evals" / "data" / "canonical_v1"

SYSTEM_EXACT_TOOL_REQUEST = (
    "Use ONLY the exact tool requested. Keep final answer concise. If a tool result already answers the task, "
    "stop and finalize. Return only strict JSON tool calls when a tool is required. Do not add prose, markdown, "
    "or shell blocks."
)

ANCHOR_TOOLS = ["rg_search", "read_file", "find_files", "debug_tools", "run_command"]
ANCHOR_PATCH_COUNTS = {
    "rg_search": 20,
    "read_file": 20,
    "find_files": 20,
    "debug_tools": 20,
    "run_command": 20,
}

ARM_ORDER = ["control", "treatment_a", "treatment_b", "treatment_c"]
ARM_LABELS = {
    "control": "compact_local",
    "treatment_a": "two_cluster",
    "treatment_b": "four_cluster",
    "treatment_c": "fully_dispersed",
}

ARM_PATTERNS = {
    "control": "minimal_span_window_of_100_rg_search_rows",
    "treatment_a": "two_clusters_50_plus_50_rg_search_rows",
    "treatment_b": "four_clusters_25_plus_25_plus_25_plus_25_rg_search_rows",
    "treatment_c": "quantile_dispersed_100_rg_search_rows",
}


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"expected object JSON at {path}")
    return payload


def _read_jsonl_raw(path: Path) -> list[str]:
    return [line.rstrip("\n") for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _parse_rows(raw_rows: list[str]) -> list[dict[str, Any]]:
    parsed: list[dict[str, Any]] = []
    for raw in raw_rows:
        obj = json.loads(raw)
        if not isinstance(obj, dict):
            raise RuntimeError("expected object rows")
        parsed.append(obj)
    return parsed


def _canonical_json_text(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _category(row: dict[str, Any]) -> str:
    meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    return str(meta.get("category") or "unknown")


def _tool_name(row: dict[str, Any]) -> str:
    meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    return str(meta.get("tool") or "").strip()


def _tool_positive_rows(rows: list[dict[str, Any]]) -> list[tuple[int, dict[str, Any]]]:
    return [(idx, row) for idx, row in enumerate(rows) if _category(row) == "tool_positive"]


def _tool_positions(rows: list[dict[str, Any]], tool: str) -> list[int]:
    return [idx for idx, row in enumerate(rows) if _category(row) == "tool_positive" and _tool_name(row) == tool]


def _tool_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counter = Counter()
    for row in rows:
        if _category(row) == "tool_positive":
            counter[_tool_name(row)] += 1
    return dict(sorted(counter.items(), key=lambda kv: kv[0]))


def _category_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counter = Counter(_category(row) for row in rows)
    return dict(sorted(counter.items(), key=lambda kv: kv[0]))


def _user_prompt(row: dict[str, Any]) -> str:
    for message in row.get("messages", []):
        if isinstance(message, dict) and message.get("role") == "user":
            return str(message.get("content") or "")
    return ""


def _assistant_target(row: dict[str, Any]) -> str:
    for message in row.get("messages", []):
        if not isinstance(message, dict) or message.get("role") != "assistant":
            continue
        tool_calls = message.get("tool_calls")
        if isinstance(tool_calls, list) and tool_calls:
            return _canonical_json_text({"tool_calls": tool_calls})
        return str(message.get("content") or "")
    return ""


def _source_case_id(row: dict[str, Any]) -> str:
    meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    return str(meta.get("source_case_id") or meta.get("case_id") or "").strip()


def _load_eval_map() -> dict[str, list[dict[str, Any]]]:
    eval_files = {
        "heldout_validation": EVAL_ROOT / "heldout_validation.jsonl",
        "tool_holdout": EVAL_ROOT / "tool_holdout.jsonl",
        "no_call": EVAL_ROOT / "no_call.jsonl",
        "adversarial": EVAL_ROOT / "adversarial.jsonl",
        "direct_answer": EVAL_ROOT / "direct_answer.jsonl",
    }
    out: dict[str, list[dict[str, Any]]] = {}
    for name, path in eval_files.items():
        rows: list[dict[str, Any]] = []
        for raw in _read_jsonl_raw(path):
            rows.append(json.loads(raw))
        out[name] = rows
    return out


def _overlap(candidate_rows: list[dict[str, Any]], eval_rows: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "prompt_overlap": len({_user_prompt(row) for row in candidate_rows}.intersection({_user_prompt(row) for row in eval_rows})),
        "target_overlap": len({_assistant_target(row) for row in candidate_rows}.intersection({_assistant_target(row) for row in eval_rows})),
        "source_case_id_overlap": len({_source_case_id(row) for row in candidate_rows}.intersection({_source_case_id(row) for row in eval_rows})),
    }


def _build_contamination_report(train_rows: list[dict[str, Any]], val_rows: list[dict[str, Any]], eval_map: dict[str, list[dict[str, Any]]], dataset_name: str) -> dict[str, Any]:
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
    report["report_path"] = str((BASE_DIR / f"{dataset_name}_leakage_report.json").resolve())
    return report


def _select_source_rows_by_tool(source_rows: list[SourceRow]) -> dict[str, list[SourceRow]]:
    groups: dict[str, list[SourceRow]] = defaultdict(list)
    for row in source_rows:
        groups[row.tool].append(row)
    for tool in groups:
        groups[tool].sort(key=lambda row: (row.source_category, row.case_id, row.prompt_sha1, row.target_sha1))
    return groups


def _make_patch_row(tool: str, source_row: SourceRow, slot: int) -> dict[str, Any]:
    args = _tool_args(tool, slot)
    prompt = _prompt_shell(tool, "diversity", args, slot)
    metadata = {
        "category": "tool_positive",
        "source": "phase_zf_topology_patch",
        "source_file": str(SOURCE_POOL.resolve()),
        "source_case_id": f"phase_zf_anchor_patch_{tool}_{source_row.case_id}_{slot:04d}",
        "tool": tool,
        "synthetic": True,
        "phase_zf_arm": "shared_anchor_patch",
        "phase_zf_patch_slot": slot,
        "phase_zf_anchor_family": True,
        "phase_zf_prompt_style": "exact_tool_request",
        "phase_zf_source_category": source_row.source_category,
        "phase_zf_source_case_id": source_row.case_id,
        "phase_zf_source_prompt_sha1": source_row.prompt_sha1,
        "phase_zf_source_target_sha1": source_row.target_sha1,
        "phase_zf_source_tool": source_row.tool,
        "phase_zf_lineage_tag": f"derived_from_{source_row.source_category}",
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


def _select_patch_rows(source_rows: list[SourceRow]) -> list[dict[str, Any]]:
    groups = _select_source_rows_by_tool(source_rows)
    patch_rows: list[dict[str, Any]] = []
    slot = 1
    for tool in ANCHOR_TOOLS:
        candidates = groups.get(tool) or []
        need = ANCHOR_PATCH_COUNTS[tool]
        if len(candidates) < need:
            raise RuntimeError(f"not enough source rows for tool {tool}: need {need}, have {len(candidates)}")
        for candidate in candidates[:need]:
            patch_rows.append(_make_patch_row(tool, candidate, slot))
            slot += 1
    if len(patch_rows) != 100:
        raise RuntimeError(f"expected 100 patch rows, got {len(patch_rows)}")
    return patch_rows


def _minimal_window_positions(positions: list[int], width: int = 100) -> list[int]:
    if len(positions) < width:
        raise RuntimeError(f"need at least {width} positions, have {len(positions)}")
    best_start = 0
    best_span = None
    for start in range(0, len(positions) - width + 1):
        window = positions[start : start + width]
        span = window[-1] - window[0]
        if best_span is None or span < best_span:
            best_span = span
            best_start = start
    return positions[best_start : best_start + width]


def _two_cluster_positions(positions: list[int]) -> list[int]:
    return positions[:50] + positions[-50:]


def _four_cluster_positions(positions: list[int]) -> list[int]:
    if len(positions) < 100:
        raise RuntimeError("need at least 100 positions for four-cluster topology")
    starts = [0, 81, 163, 244]
    out: list[int] = []
    for start in starts:
        out.extend(positions[start : start + 25])
    if len(out) != 100:
        raise RuntimeError(f"four-cluster topology produced {len(out)} positions")
    return out


def _dispersed_positions(positions: list[int]) -> list[int]:
    if len(positions) < 100:
        raise RuntimeError("need at least 100 positions for dispersed topology")
    out: list[int] = []
    length = len(positions)
    for i in range(100):
        idx = min(length - 1, int(i * length / 100))
        out.append(positions[idx])
    if len(set(out)) != 100:
        raise RuntimeError("dispersed topology produced duplicate positions")
    return out


def _position_stats(positions: list[int]) -> dict[str, Any]:
    ordered = sorted(positions)
    gaps = [b - a for a, b in zip(ordered, ordered[1:])]
    return {
        "min_position": ordered[0],
        "max_position": ordered[-1],
        "span": ordered[-1] - ordered[0],
        "mean_gap": round(sum(gaps) / len(gaps), 6) if gaps else 0.0,
        "median_gap": statistics.median(gaps) if gaps else 0.0,
    }


def _replace_rows(base_raw_rows: list[str], positions: list[int], patch_rows: list[dict[str, Any]]) -> list[str]:
    if len(positions) != len(patch_rows):
        raise RuntimeError(f"replacement count mismatch: {len(positions)} positions vs {len(patch_rows)} patch rows")
    out = list(base_raw_rows)
    for position, patch_row in zip(positions, patch_rows):
        out[position] = json.dumps(patch_row, ensure_ascii=False)
    return out


def _build_summary(
    *,
    dataset_name: str,
    arm: str,
    topology_label: str,
    base_train_rows: list[dict[str, Any]],
    base_val_rows: list[dict[str, Any]],
    train_rows: list[dict[str, Any]],
    val_rows: list[dict[str, Any]],
    patch_rows: list[dict[str, Any]],
    positions: list[int],
    train_raw_rows: list[str],
    train_variant_raw_rows: list[str],
    leakage_path: Path,
) -> dict[str, Any]:
    combined = train_rows + val_rows
    base_tool_counts = _tool_counts(base_train_rows)
    train_tool_counts = _tool_counts(train_rows)
    val_tool_counts = _tool_counts(val_rows)
    base_anchor_rows = sum(
        1
        for row in base_train_rows
        if _category(row) == "tool_positive" and _tool_name(row) in ANCHOR_TOOLS
    )
    final_anchor_rows = sum(
        1
        for row in train_rows
        if _category(row) == "tool_positive" and _tool_name(row) in ANCHOR_TOOLS
    )
    final_long_tail_rows = sum(
        1
        for row in train_rows
        if _category(row) == "tool_positive" and _tool_name(row) not in ANCHOR_TOOLS
    )
    train_category_counts = _category_counts(train_rows)
    val_category_counts = _category_counts(val_rows)
    return {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "dataset": dataset_name,
        "arm": arm,
        "topology_label": topology_label,
        "topology_pattern": ARM_PATTERNS[arm],
        "inputs": {
            "base_train_jsonl": str(BASE_TRAIN.resolve()),
            "base_val_jsonl": str(BASE_VAL.resolve()),
            "source_pool_jsonl": str(SOURCE_POOL.resolve()),
        },
        "policy": {
            "fixed_patch_budget": 100,
            "fixed_anchor_patch_rows": 100,
            "fixed_anchor_family_pattern": "rg_search-base replacement with anchor-only patch content",
            "train_rows_fixed": len(train_rows),
            "val_rows_fixed": len(val_rows),
            "non_tool_slices_frozen": True,
            "eval_contract_frozen": True,
        },
        "patch": {
            "replacement_positions_0_based": positions,
            "replacement_row_count": len(patch_rows),
            "patch_rows_by_tool": _tool_counts(patch_rows),
            "patch_rows_by_category": _category_counts(patch_rows),
            "base_rows_replaced_by_tool": {"rg_search": len(positions)},
            "position_stats": _position_stats(positions),
        },
        "composition": {
            "train_categories": train_category_counts,
            "val_categories": val_category_counts,
            "train_tool_counts": train_tool_counts,
            "val_tool_counts": val_tool_counts,
            "combined_tool_counts": _tool_counts(combined),
            "anchor_rows": final_anchor_rows,
            "long_tail_rows": final_long_tail_rows,
            "base_anchor_rows": base_anchor_rows,
        },
        "frozen_surface_checks": {
            "train_non_tool_slice_unchanged": all(
                base_raw == new_raw
                for idx, (base_raw, new_raw) in enumerate(zip(train_raw_rows, train_variant_raw_rows))
                if _category(base_train_rows[idx]) != "tool_positive"
            ),
            "val_bytes_copied_from_control": True,
            "train_row_count_matches_control": len(train_rows) == len(base_train_rows),
            "val_row_count_matches_control": len(val_rows) == len(base_val_rows),
            "exact_tool_request_cue_retained": all(
                message.get("content") == SYSTEM_EXACT_TOOL_REQUEST
                for row in train_rows
                if _category(row) == "tool_positive"
                for message in row.get("messages", [])
                if isinstance(message, dict) and message.get("role") == "system"
            ),
            "tool_calls_envelope_valid": all(
                isinstance(message.get("tool_calls"), list) and len(message.get("tool_calls")) == 1
                for row in train_rows
                if _category(row) == "tool_positive"
                for message in row.get("messages", [])
                if isinstance(message, dict) and message.get("role") == "assistant"
            ),
            "all_tool_families_represented": all(tool in train_tool_counts for tool in [
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
            ]),
        },
        "contamination_report_path": str(leakage_path.resolve()),
        "hashes": {
            "train_sha256": _sha256_file(BASE_DIR / f"{dataset_name}_train.jsonl"),
            "val_sha256": _sha256_file(BASE_DIR / f"{dataset_name}_val.jsonl"),
        },
        "outputs": {
            "train_jsonl": str((BASE_DIR / f"{dataset_name}_train.jsonl").resolve()),
            "val_jsonl": str((BASE_DIR / f"{dataset_name}_val.jsonl").resolve()),
            "summary_json": str((BASE_DIR / f"{dataset_name}_summary.json").resolve()),
        },
    }


def _readiness_assessment(summary: dict[str, Any], contamination: dict[str, Any]) -> dict[str, Any]:
    required_zero = {"prompt_overlap": 0, "target_overlap": 0, "source_case_id_overlap": 0}
    combined = contamination.get("combined_overlap", {})
    contamination_zero = all(combined.get(name, {}) == required_zero for name in [
        "heldout_validation",
        "tool_holdout",
        "no_call",
        "adversarial",
        "direct_answer",
    ])
    train_counts = summary.get("composition", {}).get("train_categories", {})
    tool_counts = summary.get("composition", {}).get("train_tool_counts", {})
    tool_rows = int(train_counts.get("tool_positive") or 0)
    safety_rows = int(train_counts.get("runtime_alignment") or 0) + int(train_counts.get("no_call_direct_calibration") or 0) + int(
        train_counts.get("refusal_calibration") or 0
    ) + int(train_counts.get("adversarial_no_call_calibration") or 0)
    anchor_rows = int(summary.get("composition", {}).get("anchor_rows") or 0)
    target_anchor_rows = int(summary.get("composition", {}).get("base_anchor_rows") or 0)
    checks = summary.get("frozen_surface_checks", {})
    admissible = (
        contamination_zero
        and bool(checks.get("exact_tool_request_cue_retained"))
        and bool(checks.get("tool_calls_envelope_valid"))
        and bool(checks.get("val_bytes_copied_from_control"))
        and bool(checks.get("train_row_count_matches_control"))
        and bool(checks.get("val_row_count_matches_control"))
        and bool(checks.get("all_tool_families_represented"))
        and bool(checks.get("train_non_tool_slice_unchanged"))
        and tool_rows == 1393
        and safety_rows == 767
        and anchor_rows == target_anchor_rows
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
            "exact_tool_request_cue_retained": bool(checks.get("exact_tool_request_cue_retained")),
            "scaffold_invariant": bool(checks.get("train_non_tool_slice_unchanged"))
            and bool(checks.get("val_bytes_copied_from_control"))
            and bool(checks.get("train_row_count_matches_control"))
            and bool(checks.get("val_row_count_matches_control")),
            "tool_calls_envelope_valid": bool(checks.get("tool_calls_envelope_valid")),
            "safety_block_preserved": safety_rows == 767,
            "all_tool_families_represented": bool(checks.get("all_tool_families_represented")),
        },
        "summary": {
            "row_counts": summary.get("row_counts", {}),
            "train_category_counts": summary.get("composition", {}).get("train_categories", {}),
            "train_tool_counts_top10": dict(list(tool_counts.items())[:10]),
            "anchor_rows": anchor_rows,
            "long_tail_rows": int(summary.get("composition", {}).get("long_tail_rows") or 0),
            "patch_rows": summary.get("patch", {}).get("replacement_row_count", 0),
            "position_stats": summary.get("patch", {}).get("position_stats", {}),
        },
        "rationale": (
            "Ready: the patch is contamination-clean, the exact tool cue and canonical envelope are retained, the scaffold is frozen, "
            "the safety block is preserved, all tool families remain represented, and the anchor row count matches the frozen scaffold."
            if admissible
            else "Not ready: one or more fixed-boundary, contamination, or composition checks failed."
        ),
    }


def _arm_positions(rg_positions: list[int]) -> dict[str, list[int]]:
    control = _minimal_window_positions(rg_positions, 100)
    treatment_a = _two_cluster_positions(rg_positions)
    treatment_b = _four_cluster_positions(rg_positions)
    treatment_c = _dispersed_positions(rg_positions)
    return {
        "control": control,
        "treatment_a": sorted(treatment_a),
        "treatment_b": sorted(treatment_b),
        "treatment_c": sorted(treatment_c),
    }


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_all() -> dict[str, Any]:
    if not BASE_TRAIN.exists():
        raise RuntimeError(f"missing base train scaffold: {BASE_TRAIN}")
    if not BASE_VAL.exists():
        raise RuntimeError(f"missing base val scaffold: {BASE_VAL}")
    if not SOURCE_POOL.exists():
        raise RuntimeError(f"missing source pool: {SOURCE_POOL}")

    base_train_raw = _read_jsonl_raw(BASE_TRAIN)
    base_val_raw = _read_jsonl_raw(BASE_VAL)
    base_train_rows = _parse_rows(base_train_raw)
    base_val_rows = _parse_rows(base_val_raw)

    rg_positions = _tool_positions(base_train_rows, "rg_search")
    if len(rg_positions) < 100:
        raise RuntimeError(f"need at least 100 rg_search rows, found {len(rg_positions)}")

    source_rows = _load_source_rows([SOURCE_POOL])
    patch_rows = _select_patch_rows(source_rows)
    eval_map = _load_eval_map()

    arm_positions = _arm_positions(rg_positions)
    outputs: dict[str, Any] = {}
    combined_rows_by_arm: dict[str, list[dict[str, Any]]] = {}

    for arm in ARM_ORDER:
        dataset_name = f"dataset_v1_2_phase_zf_{arm}"
        positions = arm_positions[arm]
        train_variant_raw = _replace_rows(base_train_raw, positions, patch_rows)
        train_variant_rows = _parse_rows(train_variant_raw)
        val_variant_raw = list(base_val_raw)
        val_variant_rows = _parse_rows(val_variant_raw)

        train_path = BASE_DIR / f"{dataset_name}_train.jsonl"
        val_path = BASE_DIR / f"{dataset_name}_val.jsonl"
        summary_path = BASE_DIR / f"{dataset_name}_summary.json"
        leakage_path = BASE_DIR / f"{dataset_name}_leakage_report.json"
        readiness_path = BASE_DIR / f"{dataset_name}_readiness_assessment.json"

        _write_jsonl(train_path, train_variant_raw)
        _write_jsonl(val_path, val_variant_raw)

        contamination = _build_contamination_report(train_variant_rows, val_variant_rows, eval_map, dataset_name)
        _write_json(leakage_path, contamination)

        summary = _build_summary(
            dataset_name=dataset_name,
            arm=arm,
            topology_label=ARM_LABELS[arm],
            base_train_rows=base_train_rows,
            base_val_rows=base_val_rows,
            train_rows=train_variant_rows,
            val_rows=val_variant_rows,
            patch_rows=patch_rows,
            positions=positions,
            train_raw_rows=base_train_raw,
            train_variant_raw_rows=train_variant_raw,
            leakage_path=leakage_path,
        )
        _write_json(summary_path, summary)

        readiness = _readiness_assessment(summary, contamination)
        _write_json(readiness_path, readiness)

        outputs[arm] = {
            "train": str(train_path.resolve()),
            "val": str(val_path.resolve()),
            "summary": str(summary_path.resolve()),
            "leakage": str(leakage_path.resolve()),
            "readiness": str(readiness_path.resolve()),
            "topology": ARM_LABELS[arm],
            "position_stats": summary["patch"]["position_stats"],
            "anchor_rows": summary["composition"]["anchor_rows"],
            "long_tail_rows": summary["composition"]["long_tail_rows"],
            "tool_positive_rows": summary["composition"]["train_categories"].get("tool_positive", 0),
        }
        combined_rows_by_arm[arm] = train_variant_rows

    overview = {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "source_pool": str(SOURCE_POOL.resolve()),
        "base_train": str(BASE_TRAIN.resolve()),
        "base_val": str(BASE_VAL.resolve()),
        "patch_rows": 100,
        "anchor_patch_counts": ANCHOR_PATCH_COUNTS,
        "arms": {
            arm: {
                "topology": ARM_LABELS[arm],
                "topology_pattern": ARM_PATTERNS[arm],
                "position_stats": outputs[arm]["position_stats"],
                "anchor_rows": outputs[arm]["anchor_rows"],
                "long_tail_rows": outputs[arm]["long_tail_rows"],
                "tool_positive_rows": outputs[arm]["tool_positive_rows"],
                "paths": {k: outputs[arm][k] for k in ["train", "val", "summary", "leakage", "readiness"]},
            }
            for arm in ARM_ORDER
        },
        "comparability": {
            "train_tool_counts_identical_across_arms": len({tuple(sorted(_tool_counts(rows).items())) for rows in combined_rows_by_arm.values()}) == 1,
            "anchor_rows_identical_across_arms": len({outputs[arm]["anchor_rows"] for arm in ARM_ORDER}) == 1,
            "long_tail_rows_identical_across_arms": len({outputs[arm]["long_tail_rows"] for arm in ARM_ORDER}) == 1,
        },
    }
    _write_json(BASE_DIR / "dataset_v1_2_phase_zf_overview.json", overview)
    return {
        "overview": str((BASE_DIR / "dataset_v1_2_phase_zf_overview.json").resolve()),
        "arms": outputs,
    }


def _write_jsonl(path: Path, rows: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(row + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Phase ZF topology ablation datasets.")
    parser.add_argument("--output-root", default=str(BASE_DIR))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = build_all()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
