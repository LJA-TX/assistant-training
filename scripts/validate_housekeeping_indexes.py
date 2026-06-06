#!/usr/bin/env python3
"""Validate Wave 0 housekeeping index infrastructure."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


INDEX_DIR = Path("docs/housekeeping/indexes")
SCHEMA_FILE = INDEX_DIR / "index_schema.json"
REGISTRY_FILE = INDEX_DIR / "index_registry.json"

VALID_INDEX_STATUSES = {"seeded", "partially_populated", "populated"}
VALID_ENTRY_STATUSES = {"seed", "anchor", "populated"}


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def _require_fields(obj: dict[str, Any], fields: list[str], label: str, errors: list[str]) -> None:
    missing = [field for field in fields if field not in obj]
    if missing:
        errors.append(f"{label}: missing required fields: {', '.join(missing)}")


def _require_type(value: Any, expected: Any) -> bool:
    if isinstance(expected, list):
        return any(_require_type(value, item) for item in expected)
    if expected == "string":
        return isinstance(value, str)
    if expected == "null":
        return value is None
    if expected == "array":
        return isinstance(value, list)
    if expected == "object":
        return isinstance(value, dict)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return False


def _validate_schema(schema: dict[str, Any], errors: list[str]) -> None:
    _require_fields(
        schema,
        [
            "schema_version",
            "registry_required_fields",
            "family_index_required_fields",
            "entry_required_fields",
            "field_types",
            "id_patterns",
            "family_prefixes",
        ],
        "schema",
        errors,
    )
    _require(schema.get("schema_version") == "1.0", "schema: unexpected schema_version", errors)
    prefixes = schema.get("family_prefixes", {})
    for family in ("convergence_history", "reports", "manifests", "fixtures", "sample_artifacts", "archives"):
        _require(family in prefixes, f"schema: missing family prefix for {family}", errors)


def _validate_registry(schema: dict[str, Any], registry: dict[str, Any], root: Path, errors: list[str]) -> None:
    _require_fields(
        registry,
        schema["registry_required_fields"],
        "registry",
        errors,
    )
    _require(registry.get("schema_version") == "1.0", "registry: unexpected schema_version", errors)
    _require(
        re.fullmatch(schema["id_patterns"]["registry_id"], str(registry.get("registry_id") or "")) is not None,
        "registry: invalid registry_id",
        errors,
    )
    _require(
        str(registry.get("status") or "") in VALID_INDEX_STATUSES,
        "registry: invalid status",
        errors,
    )
    schema_path = root / str(registry.get("schema_path") or "")
    _require(schema_path.exists(), "registry: schema_path does not exist", errors)
    families = registry.get("families")
    _require(isinstance(families, list) and families, "registry: families must be a non-empty list", errors)


def _validate_family_index(
    schema: dict[str, Any],
    registry_id: str,
    family_entry: dict[str, Any],
    root: Path,
    all_ids: set[str],
    errors: list[str],
) -> None:
    family = str(family_entry.get("family") or "")
    index_path = root / str(family_entry.get("path") or "")
    _require(index_path.exists(), f"{family}: index file missing", errors)
    if not index_path.exists():
        return

    data = _load_json(index_path)
    _require_fields(data, schema["family_index_required_fields"], family, errors)
    _require(data.get("schema_version") == "1.0", f"{family}: unexpected schema_version", errors)
    _require(data.get("family") == family, f"{family}: family mismatch", errors)
    expected_index_id = str(family_entry.get("index_id") or "")
    _require(data.get("index_id") == expected_index_id, f"{family}: index_id mismatch", errors)
    _require(data.get("registry_id") == registry_id, f"{family}: registry_id mismatch", errors)
    _require(
        re.fullmatch(schema["id_patterns"]["family_index_id"], str(data.get("index_id") or "")) is not None,
        f"{family}: invalid family index_id",
        errors,
    )
    _require(
        str(data.get("status") or "") in VALID_INDEX_STATUSES,
        f"{family}: unexpected status",
        errors,
    )

    entries = data.get("entries")
    _require(isinstance(entries, list), f"{family}: entries must be a list", errors)
    if not isinstance(entries, list):
        return

    expected_count_raw = family_entry.get("entry_count", family_entry.get("seed_count"))
    _require(isinstance(expected_count_raw, int) and expected_count_raw > 0, f"{family}: invalid entry_count", errors)
    expected_count = int(expected_count_raw or 0)
    _require(len(entries) == expected_count, f"{family}: entry_count mismatch", errors)

    anchor_entry_id = str(family_entry.get("anchor_entry_id") or "")
    if anchor_entry_id:
        _require(
            any(isinstance(entry, dict) and str(entry.get("stable_id") or "") == anchor_entry_id for entry in entries),
            f"{family}: anchor_entry_id not present in family entries",
            errors,
        )

    family_prefix = schema["family_prefixes"][family]
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append(f"{family}: entry must be an object")
            continue
        _require_fields(entry, schema["entry_required_fields"], f"{family} entry", errors)
        _require(
            str(entry.get("status") or "") in VALID_ENTRY_STATUSES,
            f"{family}: invalid entry status",
            errors,
        )
        stable_id = str(entry.get("stable_id") or "")
        _require(
            re.fullmatch(schema["id_patterns"]["entry_stable_id"], stable_id) is not None,
            f"{family}: invalid stable_id {stable_id}",
            errors,
        )
        _require(stable_id.startswith(f"{family_prefix}:"), f"{family}: stable_id prefix mismatch", errors)
        _require(stable_id not in all_ids, f"{family}: duplicate stable_id {stable_id}", errors)
        all_ids.add(stable_id)

        for field in ("current_path", "source_path", "canonical_path"):
            _require(field in entry, f"{family}: missing {field}", errors)
        for field in ("current_path", "source_path"):
            path_value = entry.get(field)
            if isinstance(path_value, str) and path_value:
                _require((root / path_value).exists(), f"{family}: {field} does not exist ({path_value})", errors)
        previous_paths = entry.get("previous_paths")
        _require(isinstance(previous_paths, list), f"{family}: previous_paths must be a list", errors)
        related_ids = entry.get("related_ids")
        _require(isinstance(related_ids, list), f"{family}: related_ids must be a list", errors)
        _require(
            registry_id in related_ids,
            f"{family}: related_ids missing registry reference",
            errors,
        )
        _require(
            expected_index_id in related_ids,
            f"{family}: related_ids missing family index reference",
            errors,
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Wave 0 housekeeping index infrastructure.")
    parser.add_argument(
        "--indexes-dir",
        default=str(INDEX_DIR),
        help="Path to the housekeeping indexes directory relative to the repository root.",
    )
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parents[1]
    indexes_dir = (repo_root / args.indexes_dir).resolve()

    errors: list[str] = []
    _require(indexes_dir.exists(), f"indexes directory missing: {indexes_dir}", errors)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    schema = _load_json(indexes_dir / "index_schema.json")
    registry = _load_json(indexes_dir / "index_registry.json")

    _validate_schema(schema, errors)
    _validate_registry(schema, registry, repo_root, errors)

    registry_id = str(registry.get("registry_id") or "")
    all_ids: set[str] = {registry_id}

    for family_entry in registry.get("families", []):
        if not isinstance(family_entry, dict):
            errors.append("registry: family entry must be an object")
            continue
        family_index_id = str(family_entry.get("index_id") or "")
        if family_index_id in all_ids:
            errors.append(f"registry: duplicate stable_id {family_index_id}")
        all_ids.add(family_index_id)
        _require(
            re.fullmatch(schema["id_patterns"]["family_index_id"], family_index_id) is not None,
            f"registry: invalid family index_id {family_index_id}",
            errors,
        )
        _require(
            (repo_root / str(family_entry.get("path") or "")).exists(),
            f"registry: missing family index file for {family_entry.get('family')}",
            errors,
        )

    for family_entry in registry.get("families", []):
        if isinstance(family_entry, dict):
            _validate_family_index(schema, registry_id, family_entry, repo_root, all_ids, errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print(f"PASS: validated {len(registry.get('families', []))} family indexes under {indexes_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
