#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class EncodedExample:
    input_ids: list[int]
    labels: list[int]
    attention_mask: list[int]
    audit: dict[str, Any]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _canonical_json_text(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _resolve_geometry_context(config: dict[str, Any]) -> dict[str, Any]:
    raw = config.get("geometry_mapping", {})
    if not isinstance(raw, dict):
        raw = {}
    axis_levels = raw.get("axis_levels")
    if not isinstance(axis_levels, dict):
        axis_levels = {}
    declared_exposure_units = raw.get("declared_exposure_units")
    if not isinstance(declared_exposure_units, dict):
        declared_exposure_units = {}
    return {
        "geometry_schema_version": str(raw.get("geometry_schema_version", "1.0")),
        "sweep_id": str(raw.get("sweep_id", "unspecified")),
        "cell_id": str(raw.get("cell_id", "unspecified")),
        "axis_levels": axis_levels,
        "weighting_mode": str(raw.get("weighting_mode", "none")),
        "declared_exposure_units": declared_exposure_units,
    }


def _build_geometry_context_digest(geometry_context: dict[str, Any]) -> str:
    digest_payload = {
        "geometry_schema_version": geometry_context.get("geometry_schema_version"),
        "sweep_id": geometry_context.get("sweep_id"),
        "cell_id": geometry_context.get("cell_id"),
        "axis_levels": geometry_context.get("axis_levels"),
        "weighting_mode": geometry_context.get("weighting_mode"),
    }
    return _sha256_text(_canonical_json_text(digest_payload))


def _resolve_geometry_sampling_cfg(config: dict[str, Any], *, fallback_seed: int) -> dict[str, Any]:
    raw = config.get("geometry_sampling", {})
    if not isinstance(raw, dict):
        raw = {}

    enabled = bool(raw.get("enabled", False))
    sampler_type = str(raw.get("sampler_type", "weighted_random"))
    if sampler_type not in {"weighted_random"}:
        raise RuntimeError(f"geometry_sampling.sampler_type unsupported: {sampler_type}")

    replacement = bool(raw.get("replacement", True))
    num_samples_policy = str(raw.get("num_samples_policy", "dataset_length"))
    if num_samples_policy not in {"dataset_length", "explicit"}:
        raise RuntimeError(
            "geometry_sampling.num_samples_policy unsupported; expected one of "
            "{dataset_length, explicit}"
        )
    explicit_num_samples_raw = raw.get("num_samples")
    explicit_num_samples = int(explicit_num_samples_raw) if explicit_num_samples_raw is not None else None
    if enabled and num_samples_policy == "explicit":
        if explicit_num_samples is None or explicit_num_samples <= 0:
            raise RuntimeError(
                "geometry_sampling enabled with num_samples_policy=explicit but "
                "geometry_sampling.num_samples is missing or <= 0"
            )

    sampler_seed = int(raw.get("sampler_seed", raw.get("seed", fallback_seed)))
    capture_sampled_indices = bool(raw.get("capture_sampled_indices", True))

    weight_source = raw.get("weight_source", {})
    if not isinstance(weight_source, dict):
        weight_source = {}
    source_kind = str(weight_source.get("kind", "metadata"))
    if source_kind not in {"metadata", "sidecar"}:
        raise RuntimeError("geometry_sampling.weight_source.kind unsupported; expected metadata or sidecar")

    metadata_weight_keys_raw = weight_source.get(
        "metadata_weight_keys",
        ["geometry_weight", "sampling_weight", "sample_weight", "weight"],
    )
    if not isinstance(metadata_weight_keys_raw, list) or not metadata_weight_keys_raw:
        raise RuntimeError("geometry_sampling.weight_source.metadata_weight_keys must be a non-empty list")
    metadata_weight_keys = [str(x).strip() for x in metadata_weight_keys_raw if str(x).strip()]
    if not metadata_weight_keys:
        raise RuntimeError("geometry_sampling.weight_source.metadata_weight_keys resolved empty")

    sidecar_weight_key_candidates_raw = weight_source.get(
        "sidecar_weight_key_candidates",
        ["weight", "sampling_weight", "geometry_weight"],
    )
    if not isinstance(sidecar_weight_key_candidates_raw, list) or not sidecar_weight_key_candidates_raw:
        raise RuntimeError("geometry_sampling.weight_source.sidecar_weight_key_candidates must be a non-empty list")
    sidecar_weight_key_candidates = [str(x).strip() for x in sidecar_weight_key_candidates_raw if str(x).strip()]
    if not sidecar_weight_key_candidates:
        raise RuntimeError("geometry_sampling.weight_source.sidecar_weight_key_candidates resolved empty")

    default_weight = float(weight_source.get("default_weight", 1.0))
    if not math.isfinite(default_weight) or default_weight < 0:
        raise RuntimeError("geometry_sampling.weight_source.default_weight must be finite and nonnegative")

    sidecar_json_path_raw = weight_source.get("sidecar_json_path")
    sidecar_json_path = str(sidecar_json_path_raw).strip() if sidecar_json_path_raw is not None else ""
    if enabled and source_kind == "sidecar" and not sidecar_json_path:
        raise RuntimeError("geometry_sampling.weight_source.sidecar_json_path required for kind=sidecar")

    return {
        "enabled": enabled,
        "sampler_type": sampler_type,
        "replacement": replacement,
        "num_samples_policy": num_samples_policy,
        "num_samples": explicit_num_samples,
        "sampler_seed": sampler_seed,
        "capture_sampled_indices": capture_sampled_indices,
        "weight_source": {
            "kind": source_kind,
            "metadata_weight_keys": metadata_weight_keys,
            "sidecar_weight_key_candidates": sidecar_weight_key_candidates,
            "default_weight": float(default_weight),
            "sidecar_json_path": sidecar_json_path,
        },
    }


def _coerce_numeric_weight(raw_value: Any, *, context: str) -> float:
    if isinstance(raw_value, bool):
        raise RuntimeError(f"{context}: bool weights are not allowed")
    if isinstance(raw_value, (int, float)):
        value = float(raw_value)
    elif isinstance(raw_value, str):
        text = raw_value.strip()
        if not text:
            raise RuntimeError(f"{context}: empty string is not a valid weight")
        try:
            value = float(text)
        except Exception as exc:
            raise RuntimeError(f"{context}: cannot parse weight '{raw_value}' as float") from exc
    else:
        raise RuntimeError(f"{context}: unsupported weight type {type(raw_value).__name__}")

    if not math.isfinite(value):
        raise RuntimeError(f"{context}: weight must be finite")
    if value < 0:
        raise RuntimeError(f"{context}: weight must be nonnegative")
    return value


def _validate_weight_vector(raw_weights: list[Any], *, expected_len: int) -> list[float]:
    if len(raw_weights) != expected_len:
        raise RuntimeError(
            "geometry_sampling weight length mismatch: "
            f"expected {expected_len}, got {len(raw_weights)}"
        )

    weights: list[float] = []
    positive = 0
    for idx, raw in enumerate(raw_weights):
        w = _coerce_numeric_weight(raw, context=f"geometry_sampling.weights[{idx}]")
        weights.append(w)
        if w > 0:
            positive += 1

    if positive <= 0:
        raise RuntimeError("geometry_sampling weights invalid: at least one positive weight is required")
    return weights


def _extract_metadata_weight(
    meta: dict[str, Any],
    *,
    key_candidates: list[str],
    default_weight: float,
    geom_axes: dict[str, Any],
) -> float:
    for key in key_candidates:
        if key not in meta:
            continue
        value = meta.get(key)
        if value is None:
            continue
        return _coerce_numeric_weight(value, context=f"geometry_sampling.metadata.{key}")

    # Allow axis-level weight override in normalized geometry axes when present.
    axes_weight = geom_axes.get("weight")
    if axes_weight is not None:
        return _coerce_numeric_weight(axes_weight, context="geometry_sampling.metadata.geometry_axes.weight")

    return _coerce_numeric_weight(default_weight, context="geometry_sampling.weight_source.default_weight")


def _build_weight_vector_from_metadata(
    *,
    train_rows: list[dict[str, Any]],
    fallback_axis_levels: dict[str, Any],
    key_candidates: list[str],
    default_weight: float,
) -> list[float]:
    weights: list[float] = []
    for idx0, row in enumerate(train_rows):
        meta = row.get("metadata")
        if not isinstance(meta, dict):
            meta = {}
        geom = _resolve_normalized_geometry_metadata_view(meta, fallback_axis_levels=fallback_axis_levels)
        weight = _extract_metadata_weight(
            meta,
            key_candidates=key_candidates,
            default_weight=default_weight,
            geom_axes=geom.get("geometry_axes", {}) if isinstance(geom.get("geometry_axes"), dict) else {},
        )
        weights.append(weight)
    return weights


def _load_weights_from_sidecar(
    *,
    sidecar_json_path: str,
    expected_len: int,
    weight_key_candidates: list[str],
) -> list[Any]:
    payload = _load_json(Path(sidecar_json_path))
    if isinstance(payload, list):
        return payload

    if not isinstance(payload, dict):
        raise RuntimeError("geometry_sampling sidecar payload must be object or list")

    weights_list = payload.get("weights")
    if isinstance(weights_list, list):
        return weights_list

    by_index = payload.get("weights_by_train_index")
    if isinstance(by_index, dict):
        out = [None] * expected_len
        for key, value in by_index.items():
            try:
                idx = int(key)
            except Exception as exc:
                raise RuntimeError(f"geometry_sampling sidecar weights_by_train_index key invalid: {key}") from exc
            if idx < 0 or idx >= expected_len:
                raise RuntimeError(f"geometry_sampling sidecar index out of range: {idx}")
            out[idx] = value
        if any(x is None for x in out):
            missing = sum(1 for x in out if x is None)
            raise RuntimeError(f"geometry_sampling sidecar missing {missing} train indices")
        return out

    rows = payload.get("rows")
    if isinstance(rows, list):
        out = [None] * expected_len
        for row in rows:
            if not isinstance(row, dict):
                raise RuntimeError("geometry_sampling sidecar rows entries must be objects")
            idx_raw = row.get("train_index_0based")
            if idx_raw is None:
                raise RuntimeError("geometry_sampling sidecar row missing train_index_0based")
            try:
                idx = int(idx_raw)
            except Exception as exc:
                raise RuntimeError(
                    f"geometry_sampling sidecar row train_index_0based invalid: {idx_raw}"
                ) from exc
            if idx < 0 or idx >= expected_len:
                raise RuntimeError(f"geometry_sampling sidecar row index out of range: {idx}")

            found = False
            for key in weight_key_candidates:
                if key in row:
                    out[idx] = row[key]
                    found = True
                    break
            if not found:
                raise RuntimeError(
                    "geometry_sampling sidecar row missing weight; expected one of "
                    f"{weight_key_candidates}"
                )

        if any(x is None for x in out):
            missing = sum(1 for x in out if x is None)
            raise RuntimeError(f"geometry_sampling sidecar missing {missing} row weights")
        return out

    raise RuntimeError(
        "geometry_sampling sidecar unsupported structure; expected list, "
        "'weights', 'weights_by_train_index', or 'rows'"
    )


def _summarize_weights(weights: list[float]) -> dict[str, Any]:
    zeros = sum(1 for w in weights if w == 0.0)
    positives = sum(1 for w in weights if w > 0.0)
    return {
        "weights_count": len(weights),
        "weights_sum": float(sum(weights)),
        "weights_min": float(min(weights) if weights else 0.0),
        "weights_max": float(max(weights) if weights else 0.0),
        "zero_weight_rows": int(zeros),
        "positive_weight_rows": int(positives),
    }


def _resolve_geometry_sampling_plan(
    *,
    config: dict[str, Any],
    train_rows: list[dict[str, Any]],
    row_identity_sidecar: dict[str, Any],
    geometry_context: dict[str, Any],
    fallback_seed: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    cfg = _resolve_geometry_sampling_cfg(config, fallback_seed=fallback_seed)
    rows_total = len(train_rows)

    base_plan = {
        "enabled": bool(cfg["enabled"]),
        "sampler_type": str(cfg["sampler_type"]),
        "replacement": bool(cfg["replacement"]),
        "num_samples_policy": str(cfg["num_samples_policy"]),
        "sampler_seed": int(cfg["sampler_seed"]),
        "capture_sampled_indices": bool(cfg["capture_sampled_indices"]),
        "weight_source_kind": str(cfg["weight_source"]["kind"]),
    }
    if not base_plan["enabled"]:
        disabled_summary = {
            **base_plan,
            "num_samples": int(rows_total),
            "sampler_class": "transformers_default_random_sampler_path",
            "weights_digest_sha256": None,
            "weights_summary": None,
        }
        return {**base_plan, "num_samples": int(rows_total), "weights": []}, disabled_summary

    fallback_axis_levels = geometry_context.get("axis_levels")
    if not isinstance(fallback_axis_levels, dict):
        fallback_axis_levels = {}

    weight_source = cfg["weight_source"]
    if weight_source["kind"] == "metadata":
        raw_weights = _build_weight_vector_from_metadata(
            train_rows=train_rows,
            fallback_axis_levels=fallback_axis_levels,
            key_candidates=list(weight_source["metadata_weight_keys"]),
            default_weight=float(weight_source["default_weight"]),
        )
    else:
        raw_weights = _load_weights_from_sidecar(
            sidecar_json_path=str(weight_source["sidecar_json_path"]),
            expected_len=rows_total,
            weight_key_candidates=list(weight_source["sidecar_weight_key_candidates"]),
        )

    weights = _validate_weight_vector(raw_weights, expected_len=rows_total)
    if cfg["num_samples_policy"] == "explicit":
        num_samples = int(cfg["num_samples"])
    else:
        num_samples = int(rows_total)
    if num_samples <= 0:
        raise RuntimeError("geometry_sampling.num_samples resolved <= 0")

    weights_digest = _sha256_text(_canonical_json_text(weights))
    weights_summary = _summarize_weights(weights)

    plan = {
        **base_plan,
        "num_samples": num_samples,
        "weights": weights,
        "weights_digest_sha256": weights_digest,
        "weights_summary": weights_summary,
    }
    summary = {
        **base_plan,
        "num_samples": num_samples,
        "sampler_class": "torch.utils.data.WeightedRandomSampler",
        "weights_digest_sha256": weights_digest,
        "weights_summary": weights_summary,
        "row_identity_digest_sha256": row_identity_sidecar.get("rows_digest_sha256"),
        "sidecar_path": weight_source.get("sidecar_json_path") or None,
    }
    return plan, summary


def _redact_sampling_plan(plan: dict[str, Any]) -> dict[str, Any]:
    out = dict(plan)
    out.pop("weights", None)
    return out


def _meta_string_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return ""
    out = str(value).strip()
    return out


def _first_non_empty_metadata_value(meta: dict[str, Any], keys: tuple[str, ...], default: str) -> str:
    for key in keys:
        if key not in meta:
            continue
        value = _meta_string_value(meta.get(key))
        if value:
            return value
    return default


def _normalize_axis_levels(value: Any, fallback: dict[str, Any]) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    return fallback


def _collect_declared_split_exposure(
    rows: list[dict[str, Any]],
    *,
    fallback_axis_levels: dict[str, Any],
) -> dict[str, Any]:
    family_keys = (
        "geometry_family",
        "i10r_counterbalanced_family",
        "i10r_residual_nocall_family",
        "intervention_i10_family",
        "intervention_targeted_family",
    )
    archetype_keys = (
        "geometry_archetype",
        "i10r_counterbalanced_query_archetype",
        "i10r_residual_nocall_query_archetype",
        "intervention_i10_query_archetype",
    )

    family_counts: Counter[str] = Counter()
    archetype_counts: Counter[str] = Counter()
    tool_counts: Counter[str] = Counter()
    axis_signature_counts: Counter[str] = Counter()
    pair_id_counts: Counter[str] = Counter()

    rows_with_metadata = 0
    rows_with_family = 0
    rows_with_archetype = 0
    rows_with_geometry_axes = 0

    for row in rows:
        meta = row.get("metadata")
        if not isinstance(meta, dict):
            meta = {}
        else:
            rows_with_metadata += 1

        family = _first_non_empty_metadata_value(meta, family_keys, default="unspecified")
        archetype = _first_non_empty_metadata_value(meta, archetype_keys, default="unspecified")
        tool = _meta_string_value(meta.get("tool")) or "non_tool"
        axis_levels = _normalize_axis_levels(meta.get("geometry_axes"), fallback_axis_levels)

        if family != "unspecified":
            rows_with_family += 1
        if archetype != "unspecified":
            rows_with_archetype += 1
        if isinstance(meta.get("geometry_axes"), dict):
            rows_with_geometry_axes += 1

        pair_id = _meta_string_value(meta.get("geometry_pair_id"))
        if pair_id:
            pair_id_counts[pair_id] += 1

        family_counts[family] += 1
        archetype_counts[archetype] += 1
        tool_counts[tool] += 1
        axis_signature_counts[_canonical_json_text(axis_levels)] += 1

    return {
        "rows_total": len(rows),
        "metadata_coverage": {
            "rows_with_metadata": rows_with_metadata,
            "rows_with_family": rows_with_family,
            "rows_with_archetype": rows_with_archetype,
            "rows_with_geometry_axes": rows_with_geometry_axes,
        },
        "family_counts": dict(sorted(family_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        "archetype_counts": dict(sorted(archetype_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        "tool_counts": dict(sorted(tool_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        "axis_signature_counts": dict(sorted(axis_signature_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        "pair_id_counts": dict(sorted(pair_id_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
    }


def _build_declared_exposure_ledger(
    *,
    train_rows: list[dict[str, Any]],
    val_rows: list[dict[str, Any]],
    train_jsonl: str,
    val_jsonl: str,
    geometry_context: dict[str, Any],
    geometry_context_digest: str,
    config_path: Path,
    manifest_path: Path | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    fallback_axis_levels = geometry_context.get("axis_levels")
    if not isinstance(fallback_axis_levels, dict):
        fallback_axis_levels = {}

    train_split = _collect_declared_split_exposure(train_rows, fallback_axis_levels=fallback_axis_levels)
    val_split = _collect_declared_split_exposure(val_rows, fallback_axis_levels=fallback_axis_levels)
    combined_split = _collect_declared_split_exposure(train_rows + val_rows, fallback_axis_levels=fallback_axis_levels)

    ledger = {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "status": "declared_exposure_accounting_only",
        "config_path": str(config_path),
        "manifest_path": str(manifest_path) if manifest_path else None,
        "dataset_paths": {
            "train_jsonl": str(train_jsonl),
            "val_jsonl": str(val_jsonl),
        },
        "geometry_context": geometry_context,
        "geometry_context_digest": geometry_context_digest,
        "declaration": {
            "geometry_schema_version": geometry_context.get("geometry_schema_version"),
            "sweep_id": geometry_context.get("sweep_id"),
            "cell_id": geometry_context.get("cell_id"),
            "axis_levels": geometry_context.get("axis_levels"),
            "weighting_mode": geometry_context.get("weighting_mode"),
            "declared_exposure_units": geometry_context.get("declared_exposure_units"),
        },
        "declared_exposure_by_split": {
            "train": train_split,
            "val": val_split,
            "combined": combined_split,
        },
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }
    summary = {
        "rows_total": combined_split["rows_total"],
        "rows_train": train_split["rows_total"],
        "rows_val": val_split["rows_total"],
        "unique_families": len(combined_split["family_counts"]),
        "unique_archetypes": len(combined_split["archetype_counts"]),
        "rows_with_metadata": combined_split["metadata_coverage"]["rows_with_metadata"],
    }
    return ledger, summary


def _row_content_hash(row: dict[str, Any]) -> str:
    return _sha256_text(_canonical_json_text(row))


def _resolve_normalized_geometry_metadata_view(
    meta: dict[str, Any],
    *,
    fallback_axis_levels: dict[str, Any],
) -> dict[str, Any]:
    family_keys = (
        "geometry_family",
        "i10r_counterbalanced_family",
        "i10r_residual_nocall_family",
        "intervention_i10_family",
        "intervention_targeted_family",
    )
    archetype_keys = (
        "geometry_archetype",
        "i10r_counterbalanced_query_archetype",
        "i10r_residual_nocall_query_archetype",
        "intervention_i10_query_archetype",
    )
    pair_id_keys = (
        "geometry_pair_id",
        "i10r_counterbalanced_pair_id",
        "i10r_residual_nocall_pair_id",
    )
    return {
        "geometry_family": _first_non_empty_metadata_value(meta, family_keys, default="unspecified"),
        "geometry_archetype": _first_non_empty_metadata_value(meta, archetype_keys, default="unspecified"),
        "geometry_axes": _normalize_axis_levels(meta.get("geometry_axes"), fallback_axis_levels),
        "geometry_pair_id": _first_non_empty_metadata_value(meta, pair_id_keys, default=""),
    }


def _build_train_row_identity_sidecar(
    *,
    train_rows: list[dict[str, Any]],
    train_jsonl: str,
    geometry_context: dict[str, Any],
    geometry_context_digest: str,
    config_path: Path,
    manifest_path: Path | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    fallback_axis_levels = geometry_context.get("axis_levels")
    if not isinstance(fallback_axis_levels, dict):
        fallback_axis_levels = {}

    rows_out: list[dict[str, Any]] = []
    family_counts: Counter[str] = Counter()
    archetype_counts: Counter[str] = Counter()
    axis_signature_counts: Counter[str] = Counter()
    pair_id_counts: Counter[str] = Counter()

    for idx0, row in enumerate(train_rows):
        meta = row.get("metadata")
        if not isinstance(meta, dict):
            meta = {}
        geom = _resolve_normalized_geometry_metadata_view(meta, fallback_axis_levels=fallback_axis_levels)
        source_case_id = _meta_string_value(meta.get("source_case_id")) or _meta_string_value(meta.get("case_id")) or f"train_row_{idx0 + 1}"
        tool = _meta_string_value(meta.get("tool")) or "non_tool"
        row_hash = _row_content_hash(row)
        axis_signature = _canonical_json_text(geom["geometry_axes"])

        family_counts[geom["geometry_family"]] += 1
        archetype_counts[geom["geometry_archetype"]] += 1
        axis_signature_counts[axis_signature] += 1
        if geom["geometry_pair_id"]:
            pair_id_counts[geom["geometry_pair_id"]] += 1

        rows_out.append(
            {
                "train_index_0based": idx0,
                "train_index_1based": idx0 + 1,
                "row_hash_sha256": row_hash,
                "source_case_id": source_case_id,
                "tool": tool,
                "geometry_family": geom["geometry_family"],
                "geometry_archetype": geom["geometry_archetype"],
                "geometry_axes": geom["geometry_axes"],
                "geometry_axes_signature": axis_signature,
                "geometry_pair_id": geom["geometry_pair_id"] or None,
            }
        )

    sidecar_rows_digest = _sha256_text(_canonical_json_text(rows_out))
    sidecar = {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "status": "train_index_geometry_sidecar",
        "config_path": str(config_path),
        "manifest_path": str(manifest_path) if manifest_path else None,
        "dataset_paths": {
            "train_jsonl": str(train_jsonl),
        },
        "geometry_context": geometry_context,
        "geometry_context_digest": geometry_context_digest,
        "rows_digest_sha256": sidecar_rows_digest,
        "rows_total": len(rows_out),
        "rows": rows_out,
        "summary": {
            "unique_families": len(family_counts),
            "unique_archetypes": len(archetype_counts),
            "unique_axis_signatures": len(axis_signature_counts),
            "rows_with_pair_id": int(sum(pair_id_counts.values())),
        },
        "counts": {
            "family_counts": dict(sorted(family_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
            "archetype_counts": dict(sorted(archetype_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
            "axis_signature_counts": dict(sorted(axis_signature_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
            "pair_id_counts": dict(sorted(pair_id_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        },
    }
    sidecar_summary = {
        "rows_total": len(rows_out),
        "rows_digest_sha256": sidecar_rows_digest,
        "unique_families": len(family_counts),
        "unique_archetypes": len(archetype_counts),
    }
    return sidecar, sidecar_summary


def _build_realized_exposure_ledger_default_path(
    *,
    row_identity_sidecar: dict[str, Any],
    train_jsonl: str,
    geometry_context: dict[str, Any],
    geometry_context_digest: str,
    config_path: Path,
    manifest_path: Path | None,
    geometry_sampling_summary: dict[str, Any] | None = None,
    additional_limitations: list[str] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    counts = row_identity_sidecar.get("counts", {}) if isinstance(row_identity_sidecar.get("counts"), dict) else {}
    family_counts = counts.get("family_counts", {}) if isinstance(counts.get("family_counts"), dict) else {}
    archetype_counts = counts.get("archetype_counts", {}) if isinstance(counts.get("archetype_counts"), dict) else {}
    axis_signature_counts = counts.get("axis_signature_counts", {}) if isinstance(counts.get("axis_signature_counts"), dict) else {}
    pair_id_counts = counts.get("pair_id_counts", {}) if isinstance(counts.get("pair_id_counts"), dict) else {}
    rows_total = int(row_identity_sidecar.get("rows_total", 0))

    limitations = [
        "Exact sampled index stream is not captured in this phase.",
        "Realized accounting is inferred from default-path train index space, not runtime sampler trace.",
        "Future Trainer subclass instrumentation is required for high-confidence sampled-stream realized exposure.",
    ]
    if additional_limitations:
        limitations.extend([str(x) for x in additional_limitations if str(x).strip()])

    status = "realized_exposure_default_path_inferred"
    if geometry_sampling_summary and bool(geometry_sampling_summary.get("enabled")):
        status = "realized_exposure_weighted_configured_runtime_not_captured"

    ledger = {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "status": status,
        "config_path": str(config_path),
        "manifest_path": str(manifest_path) if manifest_path else None,
        "dataset_paths": {
            "train_jsonl": str(train_jsonl),
        },
        "geometry_context": geometry_context,
        "geometry_context_digest": geometry_context_digest,
        "capture_mode": "index_space_inferred_no_sampler_stream_capture",
        "confidence": "limited",
        "limitations": limitations,
        "geometry_sampling": geometry_sampling_summary or {
            "enabled": False,
            "sampler_class": "transformers_default_random_sampler_path",
        },
        "sampler_behavior_assumption": {
            "trainer_sampler_path": "transformers_default_random_sampler_path",
            "sampler_behavior_changed": False,
        },
        "row_identity_reference": {
            "rows_total": rows_total,
            "rows_digest_sha256": row_identity_sidecar.get("rows_digest_sha256"),
        },
        "realized_exposure": {
            "family_counts": family_counts,
            "archetype_counts": archetype_counts,
            "axis_signature_counts": axis_signature_counts,
            "pair_id_counts": pair_id_counts,
        },
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }
    summary = {
        "rows_total": rows_total,
        "unique_families": len(family_counts),
        "unique_archetypes": len(archetype_counts),
        "status": ledger["status"],
        "capture_mode": ledger["capture_mode"],
        "confidence": ledger["confidence"],
    }
    return ledger, summary


def _build_dimension_drift_report(declared: dict[str, Any], realized: dict[str, Any]) -> dict[str, Any]:
    declared_counts = {str(k): int(v) for k, v in declared.items()}
    realized_counts = {str(k): int(v) for k, v in realized.items()}
    keys = sorted(set(declared_counts.keys()).union(realized_counts.keys()))
    deltas: dict[str, Any] = {}
    total_abs_delta = 0
    max_abs_delta = 0
    for key in keys:
        d = int(declared_counts.get(key, 0))
        r = int(realized_counts.get(key, 0))
        delta = r - d
        abs_delta = abs(delta)
        total_abs_delta += abs_delta
        if abs_delta > max_abs_delta:
            max_abs_delta = abs_delta
        deltas[key] = {
            "declared": d,
            "realized": r,
            "delta_realized_minus_declared": delta,
        }
    return {
        "declared_total": int(sum(declared_counts.values())),
        "realized_total": int(sum(realized_counts.values())),
        "total_abs_delta": int(total_abs_delta),
        "max_abs_delta": int(max_abs_delta),
        "exact_match": bool(total_abs_delta == 0),
        "per_key": deltas,
    }


def _build_exposure_drift_ledger(
    *,
    declared_ledger: dict[str, Any],
    realized_ledger: dict[str, Any],
    geometry_context: dict[str, Any],
    geometry_context_digest: str,
    config_path: Path,
    manifest_path: Path | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    declared_by_split = declared_ledger.get("declared_exposure_by_split", {})
    if not isinstance(declared_by_split, dict):
        declared_by_split = {}
    declared_train = declared_by_split.get("train", {})
    if not isinstance(declared_train, dict):
        declared_train = {}

    realized_exposure = realized_ledger.get("realized_exposure", {})
    if not isinstance(realized_exposure, dict):
        realized_exposure = {}

    family_drift = _build_dimension_drift_report(
        declared_train.get("family_counts", {}) if isinstance(declared_train.get("family_counts"), dict) else {},
        realized_exposure.get("family_counts", {}) if isinstance(realized_exposure.get("family_counts"), dict) else {},
    )
    archetype_drift = _build_dimension_drift_report(
        declared_train.get("archetype_counts", {}) if isinstance(declared_train.get("archetype_counts"), dict) else {},
        realized_exposure.get("archetype_counts", {}) if isinstance(realized_exposure.get("archetype_counts"), dict) else {},
    )
    axis_drift = _build_dimension_drift_report(
        declared_train.get("axis_signature_counts", {}) if isinstance(declared_train.get("axis_signature_counts"), dict) else {},
        realized_exposure.get("axis_signature_counts", {}) if isinstance(realized_exposure.get("axis_signature_counts"), dict) else {},
    )

    max_abs_delta = max(family_drift["max_abs_delta"], archetype_drift["max_abs_delta"], axis_drift["max_abs_delta"])
    realized_capture_mode = str(realized_ledger.get("capture_mode", ""))
    realized_confidence = str(realized_ledger.get("confidence", "limited"))
    if realized_capture_mode == "runtime_weighted_sampler_stream_capture":
        status = "declared_vs_realized_comparison_weighted_stream_captured"
        comparison_basis = "declared_train_split_vs_runtime_weighted_sampler_index_stream"
    else:
        status = "declared_vs_realized_comparison_default_path_inferred"
        comparison_basis = "declared_train_split_vs_inferred_realized_index_space"

    drift = {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "status": status,
        "config_path": str(config_path),
        "manifest_path": str(manifest_path) if manifest_path else None,
        "geometry_context": geometry_context,
        "geometry_context_digest": geometry_context_digest,
        "comparison_basis": comparison_basis,
        "confidence": realized_confidence,
        "limitations": list(realized_ledger.get("limitations", [])),
        "drift": {
            "family": family_drift,
            "archetype": archetype_drift,
            "axis_signature": axis_drift,
        },
        "aggregate": {
            "max_abs_delta_any_dimension": int(max_abs_delta),
            "exact_match_all_dimensions": bool(
                family_drift["exact_match"] and archetype_drift["exact_match"] and axis_drift["exact_match"]
            ),
        },
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }
    summary = {
        "confidence": drift["confidence"],
        "max_abs_delta_any_dimension": drift["aggregate"]["max_abs_delta_any_dimension"],
        "exact_match_all_dimensions": drift["aggregate"]["exact_match_all_dimensions"],
    }
    return drift, summary


def _build_realized_counts_from_sampled_indices(
    *,
    sidecar_rows: list[dict[str, Any]],
    sampled_indices: list[int],
) -> dict[str, dict[str, int]]:
    family_counts: Counter[str] = Counter()
    archetype_counts: Counter[str] = Counter()
    axis_signature_counts: Counter[str] = Counter()
    pair_id_counts: Counter[str] = Counter()

    n_rows = len(sidecar_rows)
    for pos, idx in enumerate(sampled_indices):
        if idx < 0 or idx >= n_rows:
            raise RuntimeError(
                "weighted sampler captured out-of-range index "
                f"sampled_indices[{pos}]={idx}, dataset_len={n_rows}"
            )
        row = sidecar_rows[idx]
        family = str(row.get("geometry_family") or "unspecified")
        archetype = str(row.get("geometry_archetype") or "unspecified")
        axis_signature = str(row.get("geometry_axes_signature") or "{}")
        pair_id = row.get("geometry_pair_id")
        pair_id_text = str(pair_id).strip() if pair_id is not None else ""

        family_counts[family] += 1
        archetype_counts[archetype] += 1
        axis_signature_counts[axis_signature] += 1
        if pair_id_text:
            pair_id_counts[pair_id_text] += 1

    return {
        "family_counts": dict(sorted(family_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        "archetype_counts": dict(sorted(archetype_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        "axis_signature_counts": dict(sorted(axis_signature_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        "pair_id_counts": dict(sorted(pair_id_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
    }


def _build_realized_exposure_ledger_weighted_path(
    *,
    row_identity_sidecar: dict[str, Any],
    train_jsonl: str,
    geometry_context: dict[str, Any],
    geometry_context_digest: str,
    config_path: Path,
    manifest_path: Path | None,
    geometry_sampling_summary: dict[str, Any],
    sampled_indices: list[int],
    sampled_indices_digest_sha256: str,
    sampler_iteration_count: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    sidecar_rows = row_identity_sidecar.get("rows")
    if not isinstance(sidecar_rows, list):
        raise RuntimeError("row identity sidecar missing rows for weighted realized exposure accounting")

    realized_counts = _build_realized_counts_from_sampled_indices(
        sidecar_rows=sidecar_rows,
        sampled_indices=sampled_indices,
    )

    rows_total = int(row_identity_sidecar.get("rows_total", 0))
    limitations: list[str] = []
    status = "realized_exposure_weighted_sampler_stream_captured"
    confidence = "high"
    if not sampled_indices:
        status = "realized_exposure_weighted_sampler_enabled_no_samples_captured"
        confidence = "limited"
        limitations.append("No sampled train indices were captured at runtime.")

    ledger = {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "status": status,
        "config_path": str(config_path),
        "manifest_path": str(manifest_path) if manifest_path else None,
        "dataset_paths": {
            "train_jsonl": str(train_jsonl),
        },
        "geometry_context": geometry_context,
        "geometry_context_digest": geometry_context_digest,
        "capture_mode": "runtime_weighted_sampler_stream_capture",
        "confidence": confidence,
        "limitations": limitations,
        "geometry_sampling": geometry_sampling_summary,
        "sampler_runtime": {
            "sampler_iteration_count": int(sampler_iteration_count),
            "sampled_index_stream_total": len(sampled_indices),
            "sampled_index_stream_digest_sha256": sampled_indices_digest_sha256,
            "sampled_index_stream_unique_indices": len(set(sampled_indices)),
            "sampled_index_stream": sampled_indices,
        },
        "row_identity_reference": {
            "rows_total": rows_total,
            "rows_digest_sha256": row_identity_sidecar.get("rows_digest_sha256"),
        },
        "realized_exposure": realized_counts,
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }
    summary = {
        "rows_total": rows_total,
        "sampled_rows_total": len(sampled_indices),
        "unique_families": len(realized_counts["family_counts"]),
        "unique_archetypes": len(realized_counts["archetype_counts"]),
        "status": ledger["status"],
        "capture_mode": ledger["capture_mode"],
        "confidence": ledger["confidence"],
    }
    return ledger, summary


def _create_traceable_weighted_random_sampler(
    *,
    weights: list[float],
    num_samples: int,
    replacement: bool,
    sampler_seed: int,
    capture_sampled_indices: bool,
):
    import torch
    from torch.utils.data import WeightedRandomSampler

    class _TraceableWeightedRandomSampler(WeightedRandomSampler):
        def __init__(
            self,
            *,
            weights: list[float],
            num_samples: int,
            replacement: bool,
            generator: Any,
            capture_sampled_indices: bool,
        ) -> None:
            super().__init__(
                weights=weights,
                num_samples=num_samples,
                replacement=replacement,
                generator=generator,
            )
            self.capture_sampled_indices = bool(capture_sampled_indices)
            self.sampled_indices: list[int] = []
            self.iteration_count = 0

        def __iter__(self):
            self.iteration_count += 1
            for raw_idx in super().__iter__():
                idx = int(raw_idx)
                if self.capture_sampled_indices:
                    self.sampled_indices.append(idx)
                yield idx

    generator = torch.Generator()
    generator.manual_seed(int(sampler_seed))
    return _TraceableWeightedRandomSampler(
        weights=weights,
        num_samples=int(num_samples),
        replacement=bool(replacement),
        generator=generator,
        capture_sampled_indices=bool(capture_sampled_indices),
    )


def _make_geometry_sampling_trainer_subclass(base_trainer_cls: Any):
    class _GeometrySamplingTrainer(base_trainer_cls):
        def __init__(self, *args, geometry_sampling_plan: dict[str, Any] | None = None, **kwargs) -> None:
            self._geometry_sampling_plan = geometry_sampling_plan or {"enabled": False}
            self._geometry_sampler_instance = None
            super().__init__(*args, **kwargs)

        def _get_train_sampler(self):
            plan = self._geometry_sampling_plan
            if not bool(plan.get("enabled", False)):
                return super()._get_train_sampler()
            if str(plan.get("sampler_type", "")) != "weighted_random":
                raise RuntimeError("geometry sampling sampler_type unsupported for trainer subclass")
            weights = plan.get("weights")
            if not isinstance(weights, list) or not weights:
                raise RuntimeError("geometry sampling enabled but weights are missing/empty")
            sampler = _create_traceable_weighted_random_sampler(
                weights=weights,
                num_samples=int(plan["num_samples"]),
                replacement=bool(plan["replacement"]),
                sampler_seed=int(plan["sampler_seed"]),
                capture_sampled_indices=bool(plan.get("capture_sampled_indices", True)),
            )
            self._geometry_sampler_instance = sampler
            return sampler

    return _GeometrySamplingTrainer


def _extract_weighted_sampler_runtime_capture(trainer: Any) -> dict[str, Any]:
    sampler = getattr(trainer, "_geometry_sampler_instance", None)
    if sampler is None:
        return {
            "captured": False,
            "sampled_indices": [],
            "sampled_indices_digest_sha256": "",
            "sampler_iteration_count": 0,
        }
    sampled = list(getattr(sampler, "sampled_indices", []))
    digest = _sha256_text(_canonical_json_text(sampled))
    return {
        "captured": True,
        "sampled_indices": sampled,
        "sampled_indices_digest_sha256": digest,
        "sampler_iteration_count": int(getattr(sampler, "iteration_count", 0)),
    }


def _build_sampler_determinism_report(
    *,
    geometry_sampling_summary: dict[str, Any],
    geometry_context: dict[str, Any],
    geometry_context_digest: str,
    config_path: Path,
    manifest_path: Path | None,
    runtime_capture: dict[str, Any] | None = None,
) -> dict[str, Any]:
    enabled = bool(geometry_sampling_summary.get("enabled"))
    captured = bool(
        runtime_capture
        and runtime_capture.get("captured")
        and runtime_capture.get("sampled_indices")
    )
    status = "geometry_sampling_disabled_default_sampler_path"
    if enabled and captured:
        status = "geometry_sampling_weighted_runtime_stream_captured"
    elif enabled:
        status = "geometry_sampling_weighted_configured_runtime_not_captured"

    report: dict[str, Any] = {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "status": status,
        "config_path": str(config_path),
        "manifest_path": str(manifest_path) if manifest_path else None,
        "geometry_context": geometry_context,
        "geometry_context_digest": geometry_context_digest,
        "geometry_sampling": geometry_sampling_summary,
        "runtime_capture": {
            "captured": captured,
            "sampled_index_stream_total": int(len(runtime_capture.get("sampled_indices", []))) if runtime_capture else 0,
            "sampled_index_stream_digest_sha256": str(runtime_capture.get("sampled_indices_digest_sha256", "")) if runtime_capture else "",
            "sampler_iteration_count": int(runtime_capture.get("sampler_iteration_count", 0)) if runtime_capture else 0,
        },
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }
    return report


def _find_manifest_for_config(repo_root: Path, config_path: Path) -> Path | None:
    manifests_dir = repo_root / "manifests" / "runs"
    if not manifests_dir.exists():
        return None
    config_resolved = config_path.resolve()
    for cand in sorted(manifests_dir.glob("*.json")):
        try:
            obj = _load_json(cand)
        except Exception:
            continue
        mp = obj.get("config_path")
        if not isinstance(mp, str):
            continue
        try:
            if Path(mp).resolve() == config_resolved:
                return cand
        except Exception:
            continue
    return None


def _resolve_run_gate(config: dict[str, Any], manifest: dict[str, Any] | None) -> tuple[bool, dict[str, Any]]:
    safety = config.get("safety", {}) if isinstance(config.get("safety"), dict) else {}
    requires_manual = bool(safety.get("requires_manual_review", False))
    cfg_approved = bool(safety.get("approved_to_run", False))
    man_approved = False
    if isinstance(manifest, dict):
        review_gate = manifest.get("review_gate", {})
        if isinstance(review_gate, dict):
            man_approved = bool(review_gate.get("approved_to_run", False))
    approved = (not requires_manual) or cfg_approved or man_approved
    return approved, {
        "requires_manual_review": requires_manual,
        "config_approved_to_run": cfg_approved,
        "manifest_approved_to_run": man_approved,
    }


def _validate_dataset_row_shape(row: dict[str, Any], row_idx: int) -> None:
    msgs = row.get("messages")
    if not isinstance(msgs, list) or len(msgs) < 3:
        raise RuntimeError(f"row {row_idx}: messages missing/short")
    if msgs[0].get("role") != "system":
        raise RuntimeError(f"row {row_idx}: message[0] must be system")
    if msgs[1].get("role") != "user":
        raise RuntimeError(f"row {row_idx}: message[1] must be user")
    if msgs[2].get("role") != "assistant":
        raise RuntimeError(f"row {row_idx}: message[2] must be assistant")
    assistant = msgs[2]
    tc = assistant.get("tool_calls")
    content = assistant.get("content")
    has_tool_target = isinstance(tc, list) and len(tc) >= 1
    has_text_target = isinstance(content, str) and bool(content.strip())
    if not has_tool_target and not has_text_target:
        raise RuntimeError(f"row {row_idx}: assistant target missing (tool_calls or content)")


def _serialize_assistant_target(assistant_msg: dict[str, Any]) -> str:
    # Support both tool-call JSON targets (Stage B) and plain assistant text targets (Stage A).
    tool_calls = assistant_msg.get("tool_calls")
    if isinstance(tool_calls, list) and tool_calls:
        normalized_calls: list[dict[str, Any]] = []
        for call in tool_calls:
            if not isinstance(call, dict):
                continue
            fn = call.get("function")
            if not isinstance(fn, dict):
                continue
            name = fn.get("name")
            if not isinstance(name, str) or not name.strip():
                continue
            raw_args = fn.get("arguments")
            parsed_args: Any = raw_args
            if isinstance(raw_args, str):
                try:
                    parsed_args = json.loads(raw_args)
                except Exception:
                    parsed_args = raw_args
            normalized_calls.append(
                {
                    "type": "function",
                    "function": {
                        "name": name.strip(),
                        "arguments": parsed_args,
                    },
                }
            )
        if not normalized_calls:
            raise RuntimeError("assistant target tool_calls malformed")
        payload = {"tool_calls": normalized_calls}
        return _canonical_json_text(payload)

    content = assistant_msg.get("content")
    if isinstance(content, str) and content.strip():
        return content

    raise RuntimeError("assistant target missing tool_calls/content")


def _default_prompt_template_cfg() -> dict[str, Any]:
    return {
        "mode": "tokenizer_chat_template",
        "fallback_mode": "fail_fast",
        "custom_template_name": None,
        "allow_custom_fallback": False,
    }


def _resolve_prompt_template_cfg(config: dict[str, Any]) -> dict[str, Any]:
    base = _default_prompt_template_cfg()
    user = config.get("prompt_template", {})
    if isinstance(user, dict):
        base.update(user)

    mode = str(base.get("mode", "tokenizer_chat_template"))
    if mode not in {"tokenizer_chat_template", "custom"}:
        raise RuntimeError(f"prompt_template.mode unsupported: {mode}")

    fallback_mode = str(base.get("fallback_mode", "fail_fast"))
    if fallback_mode not in {"fail_fast", "custom"}:
        raise RuntimeError(f"prompt_template.fallback_mode unsupported: {fallback_mode}")

    allow_custom_fallback = bool(base.get("allow_custom_fallback", False))
    custom_template_name = base.get("custom_template_name")
    if custom_template_name is not None:
        custom_template_name = str(custom_template_name)

    return {
        "mode": mode,
        "fallback_mode": fallback_mode,
        "custom_template_name": custom_template_name,
        "allow_custom_fallback": allow_custom_fallback,
    }


def _render_custom_prompt_prefix(system_text: str, user_text: str, custom_template_name: str | None) -> str:
    name = custom_template_name or "generic_roles_v1"
    if name == "generic_roles_v1":
        # Model-agnostic fallback template (no model-specific control tokens).
        return f"[SYSTEM]\n{system_text}\n[USER]\n{user_text}\n[ASSISTANT]\n"
    raise RuntimeError(f"unsupported custom_template_name: {name}")


def _render_prompt_prefix(
    system_text: str,
    user_text: str,
    tokenizer: Any,
    prompt_template_cfg: dict[str, Any],
    row_idx: int,
) -> tuple[str, dict[str, Any]]:
    mode = str(prompt_template_cfg["mode"])
    fallback_mode = str(prompt_template_cfg["fallback_mode"])
    allow_custom_fallback = bool(prompt_template_cfg["allow_custom_fallback"])
    custom_template_name = prompt_template_cfg.get("custom_template_name")

    if mode == "custom":
        if not custom_template_name:
            raise RuntimeError(
                "prompt_template.mode=custom requires prompt_template.custom_template_name"
            )
        text = _render_custom_prompt_prefix(system_text, user_text, custom_template_name)
        return text, {
            "prompt_template_mode": mode,
            "fallback_used": False,
            "custom_template_name": custom_template_name,
        }

    # mode == tokenizer_chat_template
    if not hasattr(tokenizer, "apply_chat_template"):
        missing_reason = "tokenizer.apply_chat_template missing"
    elif not getattr(tokenizer, "chat_template", None):
        missing_reason = "tokenizer.chat_template missing"
    else:
        missing_reason = ""

    if not missing_reason:
        messages = [
            {"role": "system", "content": system_text},
            {"role": "user", "content": user_text},
        ]
        try:
            text = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )
        except Exception as exc:
            missing_reason = f"apply_chat_template failed: {exc}"
        else:
            if not isinstance(text, str) or not text:
                missing_reason = "apply_chat_template returned empty/non-string"
            else:
                return text, {
                    "prompt_template_mode": mode,
                    "fallback_used": False,
                    "custom_template_name": custom_template_name,
                }

    can_custom_fallback = (
        fallback_mode == "custom"
        and allow_custom_fallback
        and bool(custom_template_name)
    )
    if not can_custom_fallback:
        raise RuntimeError(
            f"row {row_idx}: chat template unavailable ({missing_reason}); "
            "fail-fast per prompt_template policy"
        )

    text = _render_custom_prompt_prefix(system_text, user_text, custom_template_name)
    return text, {
        "prompt_template_mode": mode,
        "fallback_used": True,
        "custom_template_name": custom_template_name,
    }


def _encode_with_explicit_masking(
    row: dict[str, Any],
    row_idx: int,
    tokenizer: Any,
    max_seq_length: int,
    prompt_template_cfg: dict[str, Any] | None = None,
) -> EncodedExample:
    _validate_dataset_row_shape(row, row_idx)
    msgs = row["messages"]
    system_text = str(msgs[0].get("content") or "")
    user_text = str(msgs[1].get("content") or "")
    assistant_msg = msgs[2]
    assistant_target_text = _serialize_assistant_target(assistant_msg)

    pt_cfg = prompt_template_cfg or _default_prompt_template_cfg()
    prefix_text, prefix_meta = _render_prompt_prefix(
        system_text=system_text,
        user_text=user_text,
        tokenizer=tokenizer,
        prompt_template_cfg=pt_cfg,
        row_idx=row_idx,
    )

    prefix_ids = tokenizer.encode(prefix_text, add_special_tokens=False)
    target_ids = tokenizer.encode(assistant_target_text, add_special_tokens=False)
    if len(target_ids) == 0:
        raise RuntimeError(f"row {row_idx}: empty assistant target token span")

    # In tokenizer_chat_template mode, do not prepend BOS manually.
    # The tokenizer template already owns prefix serialization.
    manual_bos_allowed = prefix_meta["prompt_template_mode"] != "tokenizer_chat_template"
    bos: list[int] = []
    if manual_bos_allowed and getattr(tokenizer, "bos_token_id", None) is not None:
        bos = [int(tokenizer.bos_token_id)]
    manual_bos_added = bool(bos)

    eos: list[int] = []
    if getattr(tokenizer, "eos_token_id", None) is not None:
        eos = [int(tokenizer.eos_token_id)]
    eos_appended = bool(eos)

    input_ids = bos + prefix_ids + target_ids + eos
    if len(input_ids) > max_seq_length:
        raise RuntimeError(
            f"row {row_idx}: sequence length {len(input_ids)} exceeds max_seq_length={max_seq_length}; "
            "increase max_seq_length or shorten prompts."
        )

    labels = ([-100] * (len(bos) + len(prefix_ids))) + target_ids + (eos if eos else [])
    if len(labels) != len(input_ids):
        raise RuntimeError(f"row {row_idx}: label/input length mismatch")

    supervised_ids = [tid for tid, lab in zip(input_ids, labels) if lab != -100]
    expected_supervised = target_ids + (eos if eos else [])
    if supervised_ids != expected_supervised:
        raise RuntimeError(f"row {row_idx}: supervised span verification failed")

    decoded_supervised = tokenizer.decode(supervised_ids, skip_special_tokens=False)
    decoded_expected = tokenizer.decode(expected_supervised, skip_special_tokens=False)
    if decoded_supervised != decoded_expected:
        raise RuntimeError(f"row {row_idx}: decoded supervised span mismatch")
    decoded_prefix_tail = tokenizer.decode(prefix_ids[-128:], skip_special_tokens=False) if prefix_ids else ""

    audit = {
        "row_index_1based": row_idx,
        "input_token_count": len(input_ids),
        "supervised_label_token_count": len(supervised_ids),
        "masked_token_count": len(input_ids) - len(supervised_ids),
        "first_input_token_id": input_ids[0] if input_ids else None,
        "tokenizer_bos_token_id": getattr(tokenizer, "bos_token_id", None),
        "tokenizer_eos_token_id": getattr(tokenizer, "eos_token_id", None),
        "manual_bos_added": manual_bos_added,
        "eos_appended": eos_appended,
        "prompt_template_mode": prefix_meta["prompt_template_mode"],
        "fallback_used": bool(prefix_meta["fallback_used"]),
        "custom_template_name": prefix_meta.get("custom_template_name"),
        "decoded_prompt_prefix_tail": decoded_prefix_tail,
        "decoded_supervised_target_text": decoded_supervised,
        "source_case_id": (row.get("metadata") or {}).get("source_case_id")
        or (row.get("metadata") or {}).get("case_id"),
        "tool": ((row.get("metadata") or {}).get("tool") or ""),
    }
    return EncodedExample(
        input_ids=input_ids,
        labels=labels,
        attention_mask=[1] * len(input_ids),
        audit=audit,
    )


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


class _TokenizedDataset:
    def __init__(self, items: list[EncodedExample]) -> None:
        self.items = items

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, idx: int) -> dict[str, Any]:
        item = self.items[idx]
        return {
            "input_ids": item.input_ids,
            "labels": item.labels,
            "attention_mask": item.attention_mask,
        }


class _PadCollator:
    def __init__(self, pad_token_id: int) -> None:
        self.pad_token_id = int(pad_token_id)

    def __call__(self, batch: list[dict[str, Any]]) -> dict[str, torch.Tensor]:
        import torch

        max_len = max(len(x["input_ids"]) for x in batch)
        input_ids, labels, attention = [], [], []
        for x in batch:
            n = len(x["input_ids"])
            pad_n = max_len - n
            input_ids.append(x["input_ids"] + [self.pad_token_id] * pad_n)
            labels.append(x["labels"] + [-100] * pad_n)
            attention.append(x["attention_mask"] + [0] * pad_n)
        return {
            "input_ids": torch.tensor(input_ids, dtype=torch.long),
            "labels": torch.tensor(labels, dtype=torch.long),
            "attention_mask": torch.tensor(attention, dtype=torch.long),
        }


def _build_masking_audit(
    train_items: list[EncodedExample],
    val_items: list[EncodedExample],
    *,
    geometry_trace: dict[str, Any] | None = None,
) -> dict[str, Any]:
    out = {
        "train_first_3": [x.audit for x in train_items[:3]],
        "val_first_2": [x.audit for x in val_items[:2]],
    }
    if geometry_trace is not None:
        out["geometry_trace"] = geometry_trace
    return out


def _resolve_dtype(name: str):
    import torch

    n = str(name).lower()
    if n in {"bf16", "bfloat16"}:
        return torch.bfloat16
    if n in {"fp16", "float16"}:
        return torch.float16
    if n in {"fp32", "float32"}:
        return torch.float32
    return torch.bfloat16


def _prepare_output_dirs(config: dict[str, Any], run_root: Path) -> None:
    outputs = config.get("outputs", {})
    allow_overwrite = bool(outputs.get("allow_overwrite_run_root", False))

    adapter_dir = Path(outputs["adapter_output_dir"])
    logs_dir = Path(outputs["logs_dir"])
    checkpoints_dir = run_root / "checkpoints"
    forbidden_files = [
        run_root / "resolved_config.json",
        run_root / "masking_audit.json",
        run_root / "training_summary.json",
    ]

    if run_root.exists() and not allow_overwrite:
        # Refuse overwrite if any known training artifact already exists.
        artifact_hits: list[str] = []
        for p in [adapter_dir, logs_dir, checkpoints_dir]:
            if p.exists():
                artifact_hits.append(str(p))
        for p in forbidden_files:
            if p.exists():
                artifact_hits.append(str(p))
        if artifact_hits:
            raise RuntimeError(
                "run_root contains existing training artifacts; refusing overwrite unless "
                f"outputs.allow_overwrite_run_root=true. hits={artifact_hits}"
            )

        # Existing run_root is allowed only when it contains preflight artifacts exclusively.
        non_preflight_entries = [p for p in run_root.iterdir() if p.name != "preflight"]
        if non_preflight_entries:
            raise RuntimeError(
                "run_root exists with non-preflight contents; refusing reuse unless "
                f"outputs.allow_overwrite_run_root=true. entries={[str(p) for p in non_preflight_entries]}"
            )

    run_root.mkdir(parents=True, exist_ok=True)
    adapter_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _validate_loss_requirements(config: dict[str, Any]) -> None:
    loss = config.get("loss", {})
    requested = bool(loss.get("assistant_completion_only_requested", False))
    if not requested:
        return
    required_flags = [
        bool(loss.get("assistant_only_loss", False)),
        bool(loss.get("completion_only_loss", False)),
        bool(loss.get("train_on_inputs", True)) is False,
    ]
    if not all(required_flags):
        raise RuntimeError(
            "assistant_completion_only_requested=true but loss flags are inconsistent; "
            "require assistant_only_loss=true, completion_only_loss=true, train_on_inputs=false"
        )
    if str(loss.get("fallback_behavior_if_not_supported", "")).lower() != "fail_fast":
        raise RuntimeError(
            "assistant-only masking requested but fallback_behavior_if_not_supported is not fail_fast"
        )


def _load_tokenizer_only(config: dict[str, Any]):
    from transformers import AutoTokenizer

    model_cfg = config["model"]
    tok = AutoTokenizer.from_pretrained(
        model_cfg["tokenizer_name_or_path"],
        trust_remote_code=bool(model_cfg.get("trust_remote_code", False)),
    )
    if tok.pad_token_id is None:
        if tok.eos_token_id is None:
            raise RuntimeError("tokenizer has neither pad_token_id nor eos_token_id")
        tok.pad_token = tok.eos_token
    return tok


def _load_model_and_tokenizer(config: dict[str, Any]):
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from transformers import AutoModelForCausalLM, BitsAndBytesConfig

    model_cfg = config["model"]
    quant_cfg = config.get("quantization", {})
    lora_cfg = config["lora"]

    tok = _load_tokenizer_only(config)

    model_kwargs: dict[str, Any] = {
        "trust_remote_code": bool(model_cfg.get("trust_remote_code", False)),
        "torch_dtype": _resolve_dtype(model_cfg.get("torch_dtype", "bfloat16")),
        "device_map": "auto",
    }

    if bool(lora_cfg.get("use_qlora", False)) and bool(quant_cfg.get("load_in_4bit", False)):
        bnb_cfg = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type=str(quant_cfg.get("bnb_4bit_quant_type", "nf4")),
            bnb_4bit_use_double_quant=bool(quant_cfg.get("bnb_4bit_use_double_quant", True)),
            bnb_4bit_compute_dtype=_resolve_dtype(quant_cfg.get("bnb_4bit_compute_dtype", "bfloat16")),
        )
        model_kwargs["quantization_config"] = bnb_cfg

    model = AutoModelForCausalLM.from_pretrained(
        model_cfg["model_name_or_path"],
        **model_kwargs,
    )

    if bool(lora_cfg.get("use_qlora", False)):
        model = prepare_model_for_kbit_training(model)

    peft_cfg = LoraConfig(
        r=int(lora_cfg["r"]),
        lora_alpha=int(lora_cfg["alpha"]),
        lora_dropout=float(lora_cfg["dropout"]),
        bias=str(lora_cfg.get("bias", "none")),
        task_type=str(lora_cfg.get("task_type", "CAUSAL_LM")),
        target_modules=list(lora_cfg.get("target_modules", [])),
    )
    model = get_peft_model(model, peft_cfg)
    model.print_trainable_parameters()
    return model, tok


def _run_masking_audit_only(
    *,
    config: dict[str, Any],
    config_path: Path,
    manifest_path: Path | None,
    gate_info: dict[str, Any] | None,
    prompt_template_cfg: dict[str, Any],
    geometry_context: dict[str, Any],
    geometry_context_digest: str,
) -> int:
    dataset_cfg = config.get("dataset", {})
    if dataset_cfg.get("format") != "openai_messages_with_assistant_tool_calls":
        raise RuntimeError(
            f"Unsupported dataset.format={dataset_cfg.get('format')}; "
            "expected openai_messages_with_assistant_tool_calls"
        )
    max_seq_length = int(dataset_cfg.get("max_seq_length", 2048))
    train_rows = _load_jsonl(Path(dataset_cfg["train_jsonl"]))
    val_rows = _load_jsonl(Path(dataset_cfg["val_jsonl"]))
    if not train_rows or not val_rows:
        raise RuntimeError("train/val datasets must be non-empty")

    run_root = Path(config["outputs"]["run_root"])
    declared_ledger_path = Path(
        config.get("outputs", {}).get("declared_exposure_ledger_only_path")
        or (run_root / "preflight" / "exposure_ledger_declared.json")
    )
    row_identity_sidecar_path = Path(
        config.get("outputs", {}).get("row_identity_sidecar_only_path")
        or (run_root / "preflight" / "exposure_row_identity_sidecar.json")
    )
    realized_ledger_path = Path(
        config.get("outputs", {}).get("realized_exposure_ledger_only_path")
        or (run_root / "preflight" / "exposure_ledger_realized.json")
    )
    sampler_determinism_path = Path(
        config.get("outputs", {}).get("sampler_determinism_only_path")
        or (run_root / "preflight" / "sampler_determinism_report.json")
    )
    drift_ledger_path = Path(
        config.get("outputs", {}).get("drift_exposure_ledger_only_path")
        or (run_root / "preflight" / "exposure_ledger_drift.json")
    )
    declared_ledger, declared_summary = _build_declared_exposure_ledger(
        train_rows=train_rows,
        val_rows=val_rows,
        train_jsonl=str(dataset_cfg["train_jsonl"]),
        val_jsonl=str(dataset_cfg["val_jsonl"]),
        geometry_context=geometry_context,
        geometry_context_digest=geometry_context_digest,
        config_path=config_path,
        manifest_path=manifest_path,
    )
    _write_json(declared_ledger_path, declared_ledger)
    row_identity_sidecar, row_identity_summary = _build_train_row_identity_sidecar(
        train_rows=train_rows,
        train_jsonl=str(dataset_cfg["train_jsonl"]),
        geometry_context=geometry_context,
        geometry_context_digest=geometry_context_digest,
        config_path=config_path,
        manifest_path=manifest_path,
    )
    _write_json(row_identity_sidecar_path, row_identity_sidecar)
    opt = config.get("optimization", {})
    geometry_sampling_plan, geometry_sampling_summary = _resolve_geometry_sampling_plan(
        config=config,
        train_rows=train_rows,
        row_identity_sidecar=row_identity_sidecar,
        geometry_context=geometry_context,
        fallback_seed=int(opt.get("seed", 42)),
    )
    realized_ledger, realized_summary = _build_realized_exposure_ledger_default_path(
        row_identity_sidecar=row_identity_sidecar,
        train_jsonl=str(dataset_cfg["train_jsonl"]),
        geometry_context=geometry_context,
        geometry_context_digest=geometry_context_digest,
        config_path=config_path,
        manifest_path=manifest_path,
        geometry_sampling_summary=geometry_sampling_summary,
        additional_limitations=(
            ["Masking-audit-only mode: runtime sampled index stream is not available."]
            if geometry_sampling_plan.get("enabled")
            else None
        ),
    )
    _write_json(realized_ledger_path, realized_ledger)
    drift_ledger, drift_summary = _build_exposure_drift_ledger(
        declared_ledger=declared_ledger,
        realized_ledger=realized_ledger,
        geometry_context=geometry_context,
        geometry_context_digest=geometry_context_digest,
        config_path=config_path,
        manifest_path=manifest_path,
    )
    _write_json(drift_ledger_path, drift_ledger)
    sampler_determinism = _build_sampler_determinism_report(
        geometry_sampling_summary=geometry_sampling_summary,
        geometry_context=geometry_context,
        geometry_context_digest=geometry_context_digest,
        config_path=config_path,
        manifest_path=manifest_path,
        runtime_capture=None,
    )
    _write_json(sampler_determinism_path, sampler_determinism)

    tokenizer = _load_tokenizer_only(config)

    train_items = [
        _encode_with_explicit_masking(
            row,
            i + 1,
            tokenizer,
            max_seq_length,
            prompt_template_cfg=prompt_template_cfg,
        )
        for i, row in enumerate(train_rows[:3])
    ]
    val_items = [
        _encode_with_explicit_masking(
            row,
            i + 1,
            tokenizer,
            max_seq_length,
            prompt_template_cfg=prompt_template_cfg,
        )
        for i, row in enumerate(val_rows[:2])
    ]
    masking_audit = _build_masking_audit(
        train_items,
        val_items,
        geometry_trace={
            "geometry_context": geometry_context,
            "geometry_context_digest": geometry_context_digest,
            "declared_exposure_ledger_path": str(declared_ledger_path),
            "declared_exposure_summary": declared_summary,
            "row_identity_sidecar_path": str(row_identity_sidecar_path),
            "row_identity_summary": row_identity_summary,
            "realized_exposure_ledger_path": str(realized_ledger_path),
            "realized_exposure_summary": realized_summary,
            "exposure_drift_ledger_path": str(drift_ledger_path),
            "exposure_drift_summary": drift_summary,
            "geometry_sampling": geometry_sampling_summary,
            "sampler_determinism_path": str(sampler_determinism_path),
        },
    )

    audit_out = Path(config.get("outputs", {}).get("masking_audit_only_path") or (run_root / "preflight" / "masking_audit.json"))
    _write_json(audit_out, masking_audit)

    resolved = {
        "config_path": str(config_path),
        "manifest_path": str(manifest_path) if manifest_path else None,
        "approval_gate": gate_info,
        "resolved_prompt_template": prompt_template_cfg,
        "geometry_context": geometry_context,
        "geometry_context_digest": geometry_context_digest,
        "declared_exposure_ledger_path": str(declared_ledger_path),
        "row_identity_sidecar_path": str(row_identity_sidecar_path),
        "realized_exposure_ledger_path": str(realized_ledger_path),
        "exposure_drift_ledger_path": str(drift_ledger_path),
        "geometry_sampling": geometry_sampling_summary,
        "sampler_determinism_path": str(sampler_determinism_path),
        "masking_audit_only": True,
    }
    _write_json(run_root / "preflight" / "resolved_config.json", resolved)

    print(json.dumps(masking_audit, indent=2, ensure_ascii=False))
    print(json.dumps({"masking_audit_path": str(audit_out)}, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="LoRA SFT trainer for assistant tool-call dataset.")
    parser.add_argument("--config", required=True, help="Path to training config JSON")
    parser.add_argument(
        "--masking-audit-only",
        action="store_true",
        help="Run tokenizer-based masking audit only; skip model load, trainer construction, and training.",
    )
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    config = _load_json(config_path)
    repo_root = Path(__file__).resolve().parents[1]
    manifest_path = _find_manifest_for_config(repo_root, config_path)
    manifest = _load_json(manifest_path) if manifest_path else None
    prompt_template_cfg = _resolve_prompt_template_cfg(config)
    geometry_context = _resolve_geometry_context(config)
    geometry_context_digest = _build_geometry_context_digest(geometry_context)

    approved, gate_info = _resolve_run_gate(config, manifest)

    if args.masking_audit_only:
        # Audit-only mode intentionally bypasses approval gate because it does not train.
        return _run_masking_audit_only(
            config=config,
            config_path=config_path,
            manifest_path=manifest_path,
            gate_info=gate_info,
            prompt_template_cfg=prompt_template_cfg,
            geometry_context=geometry_context,
            geometry_context_digest=geometry_context_digest,
        )

    if not approved:
        raise RuntimeError(
            "training blocked by approval gate; requires manual review approval in config/manifest. "
            f"gate_info={gate_info}"
        )

    _validate_loss_requirements(config)

    dataset_cfg = config.get("dataset", {})
    if dataset_cfg.get("format") != "openai_messages_with_assistant_tool_calls":
        raise RuntimeError(
            f"Unsupported dataset.format={dataset_cfg.get('format')}; "
            "expected openai_messages_with_assistant_tool_calls"
        )

    run_root = Path(config["outputs"]["run_root"])
    _prepare_output_dirs(config, run_root)
    declared_ledger_path = run_root / "exposure_ledger_declared.json"
    row_identity_sidecar_path = run_root / "exposure_row_identity_sidecar.json"
    realized_ledger_path = run_root / "exposure_ledger_realized.json"
    sampler_determinism_path = run_root / "sampler_determinism_report.json"
    drift_ledger_path = run_root / "exposure_ledger_drift.json"

    train_rows = _load_jsonl(Path(dataset_cfg["train_jsonl"]))
    val_rows = _load_jsonl(Path(dataset_cfg["val_jsonl"]))
    if not train_rows or not val_rows:
        raise RuntimeError("train/val datasets must be non-empty")
    declared_ledger, declared_summary = _build_declared_exposure_ledger(
        train_rows=train_rows,
        val_rows=val_rows,
        train_jsonl=str(dataset_cfg["train_jsonl"]),
        val_jsonl=str(dataset_cfg["val_jsonl"]),
        geometry_context=geometry_context,
        geometry_context_digest=geometry_context_digest,
        config_path=config_path,
        manifest_path=manifest_path,
    )
    _write_json(declared_ledger_path, declared_ledger)
    row_identity_sidecar, row_identity_summary = _build_train_row_identity_sidecar(
        train_rows=train_rows,
        train_jsonl=str(dataset_cfg["train_jsonl"]),
        geometry_context=geometry_context,
        geometry_context_digest=geometry_context_digest,
        config_path=config_path,
        manifest_path=manifest_path,
    )
    _write_json(row_identity_sidecar_path, row_identity_sidecar)
    opt = config.get("optimization", {})
    geometry_sampling_plan, geometry_sampling_summary = _resolve_geometry_sampling_plan(
        config=config,
        train_rows=train_rows,
        row_identity_sidecar=row_identity_sidecar,
        geometry_context=geometry_context,
        fallback_seed=int(opt.get("seed", 42)),
    )
    sampler_determinism = _build_sampler_determinism_report(
        geometry_sampling_summary=geometry_sampling_summary,
        geometry_context=geometry_context,
        geometry_context_digest=geometry_context_digest,
        config_path=config_path,
        manifest_path=manifest_path,
        runtime_capture=None,
    )
    _write_json(sampler_determinism_path, sampler_determinism)

    resolved_config = {
        "config_path": str(config_path),
        "manifest_path": str(manifest_path) if manifest_path else None,
        "approval_gate": gate_info,
        "resolved_prompt_template": prompt_template_cfg,
        "geometry_context": geometry_context,
        "geometry_context_digest": geometry_context_digest,
        "geometry_sampling": geometry_sampling_summary,
        "declared_exposure_ledger_path": str(declared_ledger_path),
        "row_identity_sidecar_path": str(row_identity_sidecar_path),
        "realized_exposure_ledger_path": str(realized_ledger_path),
        "sampler_determinism_path": str(sampler_determinism_path),
        "exposure_drift_ledger_path": str(drift_ledger_path),
        "config": config,
    }
    _write_json(run_root / "resolved_config.json", resolved_config)

    realized_ledger, realized_summary = _build_realized_exposure_ledger_default_path(
        row_identity_sidecar=row_identity_sidecar,
        train_jsonl=str(dataset_cfg["train_jsonl"]),
        geometry_context=geometry_context,
        geometry_context_digest=geometry_context_digest,
        config_path=config_path,
        manifest_path=manifest_path,
        geometry_sampling_summary=geometry_sampling_summary,
        additional_limitations=(
            [
                "Weighted sampling is configured, but runtime sampled index stream "
                "capture is pending until training executes."
            ]
            if geometry_sampling_plan.get("enabled")
            else None
        ),
    )
    _write_json(realized_ledger_path, realized_ledger)
    drift_ledger, drift_summary = _build_exposure_drift_ledger(
        declared_ledger=declared_ledger,
        realized_ledger=realized_ledger,
        geometry_context=geometry_context,
        geometry_context_digest=geometry_context_digest,
        config_path=config_path,
        manifest_path=manifest_path,
    )
    _write_json(drift_ledger_path, drift_ledger)

    # Load model/tokenizer and build datasets with explicit masking
    model, tokenizer = _load_model_and_tokenizer(config)
    max_seq_length = int(dataset_cfg.get("max_seq_length", 2048))

    train_items = [
        _encode_with_explicit_masking(
            row,
            i + 1,
            tokenizer,
            max_seq_length,
            prompt_template_cfg=prompt_template_cfg,
        )
        for i, row in enumerate(train_rows)
    ]
    val_items = [
        _encode_with_explicit_masking(
            row,
            i + 1,
            tokenizer,
            max_seq_length,
            prompt_template_cfg=prompt_template_cfg,
        )
        for i, row in enumerate(val_rows)
    ]

    masking_audit = _build_masking_audit(
        train_items,
        val_items,
        geometry_trace={
            "geometry_context": geometry_context,
            "geometry_context_digest": geometry_context_digest,
            "declared_exposure_ledger_path": str(declared_ledger_path),
            "declared_exposure_summary": declared_summary,
            "row_identity_sidecar_path": str(row_identity_sidecar_path),
            "row_identity_summary": row_identity_summary,
            "realized_exposure_ledger_path": str(realized_ledger_path),
            "realized_exposure_summary": realized_summary,
            "exposure_drift_ledger_path": str(drift_ledger_path),
            "exposure_drift_summary": drift_summary,
            "geometry_sampling": geometry_sampling_summary,
            "sampler_determinism_path": str(sampler_determinism_path),
        },
    )
    _write_json(run_root / "masking_audit.json", masking_audit)
    print(json.dumps(masking_audit, indent=2, ensure_ascii=False))

    train_ds = _TokenizedDataset(train_items)
    val_ds = _TokenizedDataset(val_items)
    pad_token_id = int(tokenizer.pad_token_id)
    collator = _PadCollator(pad_token_id=pad_token_id)

    # Lazy import heavy trainer classes
    from transformers import Trainer, TrainingArguments

    logs_dir = Path(config["outputs"]["logs_dir"])
    output_dir = run_root / "checkpoints"
    output_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=float(opt.get("num_train_epochs", 1)),
        per_device_train_batch_size=int(opt.get("per_device_train_batch_size", 1)),
        per_device_eval_batch_size=int(opt.get("per_device_eval_batch_size", 1)),
        gradient_accumulation_steps=int(opt.get("gradient_accumulation_steps", 1)),
        learning_rate=float(opt.get("learning_rate", 5e-5)),
        lr_scheduler_type=str(opt.get("lr_scheduler_type", "cosine")),
        warmup_ratio=float(opt.get("warmup_ratio", 0.0)),
        weight_decay=float(opt.get("weight_decay", 0.0)),
        max_grad_norm=float(opt.get("max_grad_norm", 1.0)),
        logging_steps=int(opt.get("logging_steps", 10)),
        eval_strategy=str(opt.get("eval_strategy", "steps")),
        eval_steps=int(opt.get("eval_steps", 50)),
        save_strategy=str(opt.get("save_strategy", "steps")),
        save_steps=int(opt.get("save_steps", 50)),
        save_total_limit=int(opt.get("save_total_limit", 2)),
        bf16=bool(opt.get("bf16", True)),
        fp16=bool(opt.get("fp16", False)),
        gradient_checkpointing=bool(opt.get("gradient_checkpointing", True)),
        optim=str(opt.get("optim", "paged_adamw_8bit")),
        seed=int(opt.get("seed", 42)),
        report_to=[],
        logging_dir=str(logs_dir),
    )

    trainer_class_name = "Trainer"
    if geometry_sampling_plan.get("enabled"):
        GeometrySamplingTrainer = _make_geometry_sampling_trainer_subclass(Trainer)
        trainer_class_name = GeometrySamplingTrainer.__name__
        trainer = GeometrySamplingTrainer(
            model=model,
            args=training_args,
            train_dataset=train_ds,
            eval_dataset=val_ds,
            data_collator=collator,
            tokenizer=tokenizer,
            geometry_sampling_plan=geometry_sampling_plan,
        )
    else:
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_ds,
            eval_dataset=val_ds,
            data_collator=collator,
            tokenizer=tokenizer,
        )

    # Train and save adapter only (no merge).
    train_result = trainer.train()
    eval_metrics = trainer.evaluate()

    runtime_capture = _extract_weighted_sampler_runtime_capture(trainer)
    if geometry_sampling_plan.get("enabled"):
        if runtime_capture.get("captured") and runtime_capture.get("sampled_indices"):
            realized_ledger, realized_summary = _build_realized_exposure_ledger_weighted_path(
                row_identity_sidecar=row_identity_sidecar,
                train_jsonl=str(dataset_cfg["train_jsonl"]),
                geometry_context=geometry_context,
                geometry_context_digest=geometry_context_digest,
                config_path=config_path,
                manifest_path=manifest_path,
                geometry_sampling_summary=geometry_sampling_summary,
                sampled_indices=list(runtime_capture.get("sampled_indices", [])),
                sampled_indices_digest_sha256=str(runtime_capture.get("sampled_indices_digest_sha256", "")),
                sampler_iteration_count=int(runtime_capture.get("sampler_iteration_count", 0)),
            )
        else:
            realized_ledger, realized_summary = _build_realized_exposure_ledger_default_path(
                row_identity_sidecar=row_identity_sidecar,
                train_jsonl=str(dataset_cfg["train_jsonl"]),
                geometry_context=geometry_context,
                geometry_context_digest=geometry_context_digest,
                config_path=config_path,
                manifest_path=manifest_path,
                geometry_sampling_summary=geometry_sampling_summary,
                additional_limitations=[
                    "Weighted sampling enabled but runtime sampled index stream was unavailable.",
                ],
            )
        _write_json(realized_ledger_path, realized_ledger)
        drift_ledger, drift_summary = _build_exposure_drift_ledger(
            declared_ledger=declared_ledger,
            realized_ledger=realized_ledger,
            geometry_context=geometry_context,
            geometry_context_digest=geometry_context_digest,
            config_path=config_path,
            manifest_path=manifest_path,
        )
        _write_json(drift_ledger_path, drift_ledger)

    sampler_determinism = _build_sampler_determinism_report(
        geometry_sampling_summary=geometry_sampling_summary,
        geometry_context=geometry_context,
        geometry_context_digest=geometry_context_digest,
        config_path=config_path,
        manifest_path=manifest_path,
        runtime_capture=runtime_capture if geometry_sampling_plan.get("enabled") else None,
    )
    _write_json(sampler_determinism_path, sampler_determinism)

    adapter_out = Path(config["outputs"]["adapter_output_dir"])
    adapter_out.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(str(adapter_out))
    tokenizer.save_pretrained(str(adapter_out))

    summary = {
        "status": "completed",
        "train_rows": len(train_rows),
        "val_rows": len(val_rows),
        "run_root": str(run_root),
        "adapter_output_dir": str(adapter_out),
        "train_metrics": dict(train_result.metrics),
        "eval_metrics": dict(eval_metrics),
        "geometry_context": geometry_context,
        "geometry_context_digest": geometry_context_digest,
        "geometry_sampling": geometry_sampling_summary,
        "trainer_class": trainer_class_name,
        "sampler_determinism_path": str(sampler_determinism_path),
        "sampler_determinism_status": sampler_determinism.get("status"),
        "declared_exposure_ledger_path": str(declared_ledger_path),
        "declared_exposure_summary": declared_summary,
        "row_identity_sidecar_path": str(row_identity_sidecar_path),
        "row_identity_summary": row_identity_summary,
        "realized_exposure_ledger_path": str(realized_ledger_path),
        "realized_exposure_summary": realized_summary,
        "exposure_drift_ledger_path": str(drift_ledger_path),
        "exposure_drift_summary": drift_summary,
        "masking_audit_path": str(run_root / "masking_audit.json"),
        "resolved_config_path": str(run_root / "resolved_config.json"),
    }
    _write_json(run_root / "training_summary.json", summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    raise SystemExit(main())
