#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> dict[str, Any]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise RuntimeError(f"JSON root must be an object: {path}")
    return obj


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            raw = line.strip()
            if not raw:
                continue
            try:
                parsed = json.loads(raw)
            except Exception as exc:
                raise RuntimeError(f"invalid JSONL {path}:{line_no}: {exc}") from exc
            if not isinstance(parsed, dict):
                raise RuntimeError(f"JSONL row must be object {path}:{line_no}")
            rows.append(parsed)
    return rows


def _canonical_json_text(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _row_content_hash(row: dict[str, Any]) -> str:
    return _sha256_text(_canonical_json_text(row))


def _build_geometry_mapping_identity_digest(geometry_context: dict[str, Any]) -> str:
    digest_payload = {
        "geometry_schema_version": geometry_context.get("geometry_schema_version"),
        "sweep_id": geometry_context.get("sweep_id"),
        "cell_id": geometry_context.get("cell_id"),
        "axis_levels": geometry_context.get("axis_levels"),
        "weighting_mode": geometry_context.get("weighting_mode"),
    }
    return _sha256_text(_canonical_json_text(digest_payload))


def _build_geometry_context_input_digest(geometry_context: dict[str, Any]) -> str:
    return _sha256_text(_canonical_json_text(geometry_context))


def _resolve_geometry_context(raw: dict[str, Any]) -> dict[str, Any]:
    if "geometry_mapping" in raw and isinstance(raw.get("geometry_mapping"), dict):
        src = dict(raw["geometry_mapping"])
    else:
        src = dict(raw)
    axis_levels = src.get("axis_levels")
    if not isinstance(axis_levels, dict):
        axis_levels = {}
    declared_exposure_units = src.get("declared_exposure_units")
    if not isinstance(declared_exposure_units, dict):
        declared_exposure_units = {}
    return {
        "geometry_schema_version": str(src.get("geometry_schema_version", "1.0")),
        "sweep_id": str(src.get("sweep_id", "unspecified")),
        "cell_id": str(src.get("cell_id", "unspecified")),
        "axis_levels": axis_levels,
        "weighting_mode": str(src.get("weighting_mode", "none")),
        "declared_exposure_units": declared_exposure_units,
    }


def _coerce_nonnegative_float(value: Any, *, context: str) -> float:
    if isinstance(value, bool):
        raise RuntimeError(f"{context}: bool is not a numeric weight")
    if isinstance(value, (int, float)):
        out = float(value)
    elif isinstance(value, str):
        text = value.strip()
        if not text:
            raise RuntimeError(f"{context}: empty string is not numeric")
        try:
            out = float(text)
        except Exception as exc:
            raise RuntimeError(f"{context}: cannot parse '{value}' as float") from exc
    else:
        raise RuntimeError(f"{context}: unsupported type {type(value).__name__}")
    if out < 0:
        raise RuntimeError(f"{context}: weight must be nonnegative")
    if not (out == out and abs(out) != float("inf")):
        raise RuntimeError(f"{context}: weight must be finite")
    return out


def _coerce_positive_int(value: Any, *, context: str) -> int:
    try:
        out = int(value)
    except Exception as exc:
        raise RuntimeError(f"{context}: expected integer, got {value}") from exc
    if out <= 0:
        raise RuntimeError(f"{context}: expected > 0, got {out}")
    return out


def _row_matches_filters(meta: dict[str, Any], filters: dict[str, Any]) -> bool:
    for key, expected in filters.items():
        if meta.get(key) != expected:
            return False
    return True


def _meta_string_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return ""
    return str(value).strip()


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


def _build_identity_rows_from_dataset(
    rows: list[dict[str, Any]],
    *,
    fallback_axis_levels: dict[str, Any],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for idx0, row in enumerate(rows):
        meta = row.get("metadata")
        if not isinstance(meta, dict):
            meta = {}
        geom = _resolve_normalized_geometry_metadata_view(
            meta,
            fallback_axis_levels=fallback_axis_levels,
        )
        source_case_id = (
            _meta_string_value(meta.get("source_case_id"))
            or _meta_string_value(meta.get("case_id"))
            or f"train_row_{idx0 + 1}"
        )
        tool = _meta_string_value(meta.get("tool")) or "non_tool"
        axis_signature = _canonical_json_text(geom["geometry_axes"])
        out.append(
            {
                "train_index_0based": idx0,
                "train_index_1based": idx0 + 1,
                "row_hash_sha256": _row_content_hash(row),
                "source_case_id": source_case_id,
                "tool": tool,
                "geometry_family": geom["geometry_family"],
                "geometry_archetype": geom["geometry_archetype"],
                "geometry_axes": geom["geometry_axes"],
                "geometry_axes_signature": axis_signature,
                "geometry_pair_id": geom["geometry_pair_id"] or None,
            }
        )
    return out


def _validate_row_identity_consistency(
    *,
    identity_rows: list[dict[str, Any]],
    row_identity_sidecar: dict[str, Any] | None,
) -> tuple[str | None, str | None]:
    identity_rows_digest = _sha256_text(_canonical_json_text(identity_rows))
    sidecar_rows_digest: str | None = None

    if row_identity_sidecar is None:
        return identity_rows_digest, None

    sidecar_rows = row_identity_sidecar.get("rows")
    if not isinstance(sidecar_rows, list):
        raise RuntimeError("row identity sidecar must contain rows list")
    if len(sidecar_rows) != len(identity_rows):
        raise RuntimeError(
            "row identity sidecar rows length mismatch: "
            f"expected {len(identity_rows)}, got {len(sidecar_rows)}"
        )

    for pos, (lhs, rhs_raw) in enumerate(zip(identity_rows, sidecar_rows)):
        if not isinstance(rhs_raw, dict):
            raise RuntimeError(f"row identity sidecar rows[{pos}] must be object")
        rhs_idx = rhs_raw.get("train_index_0based")
        rhs_hash = rhs_raw.get("row_hash_sha256")
        if int(rhs_idx) != int(lhs["train_index_0based"]):
            raise RuntimeError(
                "row identity sidecar index mismatch at position "
                f"{pos}: expected {lhs['train_index_0based']}, got {rhs_idx}"
            )
        if str(rhs_hash) != str(lhs["row_hash_sha256"]):
            raise RuntimeError(
                "row identity sidecar row_hash mismatch at position "
                f"{pos}: expected {lhs['row_hash_sha256']}, got {rhs_hash}"
            )

    sidecar_rows_digest = str(row_identity_sidecar.get("rows_digest_sha256") or "")
    if sidecar_rows_digest and sidecar_rows_digest != identity_rows_digest:
        raise RuntimeError(
            "row identity sidecar rows_digest_sha256 mismatch: "
            f"expected {identity_rows_digest}, got {sidecar_rows_digest}"
        )
    return identity_rows_digest, sidecar_rows_digest or identity_rows_digest


def _build_overlay_sidecar(
    *,
    train_rows: list[dict[str, Any]],
    identity_rows: list[dict[str, Any]],
    geometry_context: dict[str, Any],
    declared_exposure: dict[str, Any],
    default_weight: float,
    min_positive_rows: int | None,
    require_all_rows_covered: bool,
    source_paths: dict[str, str],
    row_identity_rows_digest: str,
) -> dict[str, Any]:
    plan = declared_exposure.get("declared_exposure_plan")
    if not isinstance(plan, dict):
        raise RuntimeError("declared exposure artifact missing declared_exposure_plan object")

    family_units = plan.get("family_units")
    if not isinstance(family_units, dict) or not family_units:
        raise RuntimeError("declared_exposure_plan.family_units must be non-empty object")
    selectors = plan.get("family_selectors")
    if not isinstance(selectors, dict) or not selectors:
        raise RuntimeError("declared_exposure_plan.family_selectors must be non-empty object")

    positive_families: dict[str, float] = {}
    for family, units_raw in family_units.items():
        units = _coerce_nonnegative_float(units_raw, context=f"family_units.{family}")
        if units > 0:
            positive_families[str(family)] = units

    if not positive_families:
        raise RuntimeError("no positive family units found; at least one positive family is required")

    family_matches: dict[str, list[int]] = {family: [] for family in positive_families}
    row_to_family: dict[int, str] = {}
    unmatched_rows = 0

    for idx0, row in enumerate(train_rows):
        meta = row.get("metadata")
        if not isinstance(meta, dict):
            meta = {}

        matched_families: list[str] = []
        for family in sorted(positive_families):
            spec = selectors.get(family)
            if not isinstance(spec, dict):
                raise RuntimeError(f"declared_exposure_plan.family_selectors.{family} missing object")
            filters = spec.get("metadata_filters")
            if not isinstance(filters, dict):
                raise RuntimeError(
                    f"declared_exposure_plan.family_selectors.{family}.metadata_filters missing object"
                )
            if _row_matches_filters(meta, filters):
                matched_families.append(family)

        if len(matched_families) > 1:
            raise RuntimeError(
                "row matched multiple positive families, attribution ambiguous: "
                f"train_index_0based={idx0}, families={matched_families}"
            )
        if not matched_families:
            unmatched_rows += 1
            continue

        family = matched_families[0]
        family_matches[family].append(idx0)
        row_to_family[idx0] = family

    for family in sorted(positive_families):
        if not family_matches[family]:
            raise RuntimeError(
                f"no rows matched positive family selector: {family}"
            )

    weights = [float(default_weight)] * len(train_rows)
    per_family_row_weight: dict[str, float] = {}
    for family in sorted(positive_families):
        units = positive_families[family]
        matched = family_matches[family]
        row_weight = units / float(len(matched))
        per_family_row_weight[family] = float(row_weight)
        for idx0 in matched:
            weights[idx0] = row_weight

    positive_rows = sum(1 for w in weights if w > 0)
    if min_positive_rows is not None and positive_rows < min_positive_rows:
        raise RuntimeError(
            "positive weight row coverage below minimum: "
            f"required {min_positive_rows}, got {positive_rows}"
        )

    sidecar_rows: list[dict[str, Any]] = []
    family_weight_sum: Counter[str] = Counter()
    family_positive_rows: Counter[str] = Counter()
    for ident in identity_rows:
        idx0 = int(ident["train_index_0based"])
        row_hash = str(ident["row_hash_sha256"])
        weight = float(weights[idx0])
        sidecar_rows.append(
            {
                "train_index_0based": idx0,
                "row_hash_sha256": row_hash,
                "weight": weight,
            }
        )
        family = row_to_family.get(idx0, "unmatched_default")
        family_weight_sum[family] += weight
        if weight > 0:
            family_positive_rows[family] += 1

    row_hash_counts: Counter[str] = Counter()
    for ident in identity_rows:
        row_hash_counts[str(ident["row_hash_sha256"])] += 1

    geometry_mapping_identity_digest = _build_geometry_mapping_identity_digest(geometry_context)
    geometry_context_input_digest = _build_geometry_context_input_digest(geometry_context)
    weights_digest = _sha256_text(_canonical_json_text(weights))

    family_summary: dict[str, Any] = {}
    for family in sorted(positive_families):
        family_summary[family] = {
            "declared_units": float(positive_families[family]),
            "matched_rows": int(len(family_matches[family])),
            "assigned_weight_per_row": float(per_family_row_weight[family]),
            "assigned_weight_sum": float(family_weight_sum.get(family, 0.0)),
            "positive_rows": int(family_positive_rows.get(family, 0)),
        }
    family_summary["unmatched_default"] = {
        "declared_units": 0.0,
        "matched_rows": int(unmatched_rows),
        "assigned_weight_per_row": float(default_weight),
        "assigned_weight_sum": float(family_weight_sum.get("unmatched_default", 0.0)),
        "positive_rows": int(family_positive_rows.get("unmatched_default", 0)),
    }

    return {
        "schema_version": "1.0",
        "weight_provisioning_mode": "probe_specific_overlay_row_identity_rows",
        "generated_utc": _now_utc(),
        "source_paths": source_paths,
        "geometry_mapping_identity_digest": geometry_mapping_identity_digest,
        "geometry_context_input_digest": geometry_context_input_digest,
        "geometry_context": geometry_context,
        "row_identity_reference": {
            "rows_total": len(identity_rows),
            "rows_digest_sha256": row_identity_rows_digest,
        },
        "default_weight": float(default_weight),
        "require_all_rows_covered": bool(require_all_rows_covered),
        "family_weight_summary": family_summary,
        "weights_digest_sha256": weights_digest,
        "weights_summary": {
            "weights_count": len(weights),
            "weights_sum": float(sum(weights)),
            "weights_min": float(min(weights) if weights else 0.0),
            "weights_max": float(max(weights) if weights else 0.0),
            "zero_weight_rows": int(sum(1 for w in weights if w == 0)),
            "positive_weight_rows": int(positive_rows),
            "unique_row_hashes": int(len(row_hash_counts)),
            "row_hash_collision_count": int(sum(1 for c in row_hash_counts.values() if c > 1)),
        },
        "rows": sidecar_rows,
        "approval_state": {
            "approved_to_generate_dataset": False,
            "approved_to_run": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Provision deterministic probe-specific geometry weights sidecar without mutating datasets."
    )
    parser.add_argument("--train-jsonl", required=True, help="Path to train JSONL")
    parser.add_argument(
        "--declared-exposure",
        required=True,
        help="Path to declared exposure plan artifact JSON (stage_b_first_probe_declared_exposure.json)",
    )
    parser.add_argument(
        "--geometry-context",
        required=True,
        help="Path to geometry context JSON (geometry_context object or config with geometry_mapping)",
    )
    parser.add_argument("--output-sidecar", required=True, help="Output path for weight sidecar JSON")
    parser.add_argument(
        "--row-identity-sidecar",
        help="Optional existing row identity sidecar to validate row-hash/index stability",
    )
    parser.add_argument(
        "--default-weight",
        type=float,
        default=0.0,
        help="Default weight for unmatched rows (default: 0.0)",
    )
    parser.add_argument(
        "--min-positive-rows",
        type=int,
        default=0,
        help="Optional minimum positive-weight rows requirement (0 disables check).",
    )
    parser.add_argument(
        "--allow-partial-coverage",
        action="store_true",
        help="Allow sidecar to omit rows from full explicit rows coverage checks.",
    )
    args = parser.parse_args()

    train_jsonl_path = Path(args.train_jsonl).resolve()
    declared_exposure_path = Path(args.declared_exposure).resolve()
    geometry_context_path = Path(args.geometry_context).resolve()
    output_sidecar_path = Path(args.output_sidecar).resolve()
    row_identity_sidecar_path = Path(args.row_identity_sidecar).resolve() if args.row_identity_sidecar else None

    train_rows = _load_jsonl(train_jsonl_path)
    declared_exposure = _load_json(declared_exposure_path)
    geometry_context = _resolve_geometry_context(_load_json(geometry_context_path))
    row_identity_sidecar = _load_json(row_identity_sidecar_path) if row_identity_sidecar_path else None

    axis_levels = geometry_context.get("axis_levels")
    if not isinstance(axis_levels, dict):
        axis_levels = {}
    identity_rows = _build_identity_rows_from_dataset(
        train_rows,
        fallback_axis_levels=axis_levels,
    )
    computed_rows_digest, sidecar_rows_digest = _validate_row_identity_consistency(
        identity_rows=identity_rows,
        row_identity_sidecar=row_identity_sidecar,
    )
    rows_digest = sidecar_rows_digest or computed_rows_digest

    min_positive_rows = _coerce_positive_int(args.min_positive_rows, context="--min-positive-rows") if args.min_positive_rows > 0 else None
    sidecar = _build_overlay_sidecar(
        train_rows=train_rows,
        identity_rows=identity_rows,
        geometry_context=geometry_context,
        declared_exposure=declared_exposure,
        default_weight=_coerce_nonnegative_float(args.default_weight, context="--default-weight"),
        min_positive_rows=min_positive_rows,
        require_all_rows_covered=not bool(args.allow_partial_coverage),
        source_paths={
            "train_jsonl": str(train_jsonl_path),
            "declared_exposure": str(declared_exposure_path),
            "geometry_context": str(geometry_context_path),
            "row_identity_sidecar": str(row_identity_sidecar_path) if row_identity_sidecar_path else None,
        },
        row_identity_rows_digest=str(rows_digest),
    )
    _write_json(output_sidecar_path, sidecar)

    summary = {
        "status": "ok",
        "output_sidecar": str(output_sidecar_path),
        "rows_total": int(sidecar["row_identity_reference"]["rows_total"]),
        "rows_digest_sha256": sidecar["row_identity_reference"]["rows_digest_sha256"],
        "weights_digest_sha256": sidecar["weights_digest_sha256"],
        "weights_summary": sidecar["weights_summary"],
        "geometry_mapping_identity_digest": sidecar["geometry_mapping_identity_digest"],
        "geometry_context_input_digest": sidecar["geometry_context_input_digest"],
        "weight_provisioning_mode": sidecar["weight_provisioning_mode"],
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
