#!/usr/bin/env python3
"""Run the dependency-free newcomer validation path for this package."""

from __future__ import annotations

import datetime as _datetime
import importlib.util
import json
import re
import sys
from pathlib import Path
from types import ModuleType
from typing import Callable

sys.dont_write_bytecode = True

REQUIRED_SURFACES = (
    "AGENTS.md",
    "README.md",
    "docs/current/start_here.md",
    "docs/framework/examples/public_sanitized_tool_call_worked_example.md",
    "docs/framework/examples/public_sanitized_tool_call_worked_example.json",
    "docs/publication/public_snapshot.json",
    "docs/publication/public_reference_dispositions.json",
    "scripts/repo_paths.py",
    "scripts/validate_public_package.py",
    "tests/test_public_sanitized_tool_call_worked_example.py",
)

_SNAPSHOT_COMMIT_RE = re.compile(r"[0-9a-f]{40}\Z")
_HARBORVIEW_VALIDATORS = (
    "validate_fixture_contract_and_canonical_evaluator_reuse",
    "validate_documents_links_contamination_boundaries_and_public_portability",
    "validate_fixture_identity_and_join_integrity",
)


class ValidationFailure(Exception):
    """Expected user-facing validation failure."""


def _load_local_module(path: Path, module_name: str) -> ModuleType:
    if not path.is_file():
        raise ValidationFailure(f"local module is missing: {path.name}")
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ValidationFailure(f"local module cannot be loaded: {path.name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise ValidationFailure(f"local module failed to import: {path.name}") from exc
    return module


def _load_repo_paths() -> ModuleType:
    return _load_local_module(Path(__file__).resolve().with_name("repo_paths.py"), "assistant_training_local_repo_paths")


def _load_reference_validator(root: Path) -> ModuleType:
    return _load_local_module(
        root / "scripts" / "validate_public_references.py",
        "assistant_training_local_validate_public_references",
    )


def _require_surfaces(root: Path) -> None:
    missing = [relative for relative in REQUIRED_SURFACES if not (root / relative).is_file()]
    if missing:
        raise ValidationFailure("missing required public surface(s): " + ", ".join(missing))


def _read_text(root: Path, relative: str) -> str:
    try:
        return (root / relative).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ValidationFailure(f"cannot read {relative}") from exc


def _validate_snapshot_front_door(root: Path) -> None:
    snapshot_path = root / "docs" / "publication" / "public_snapshot.json"
    try:
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValidationFailure("snapshot is missing or malformed") from exc

    required_fields = {
        "schema_version",
        "snapshot_id",
        "snapshot_version",
        "publication_date",
        "last_material_update",
        "publication_lineage",
        "status",
        "public_snapshot_commit",
        "private_lineage_commit",
        "relationship",
        "release_model",
    }
    if not isinstance(snapshot, dict) or not required_fields.issubset(snapshot):
        raise ValidationFailure("snapshot required fields are incomplete")
    if snapshot["schema_version"] != 1:
        raise ValidationFailure("snapshot schema_version is invalid")
    if not all(isinstance(snapshot[field], str) and snapshot[field] for field in required_fields - {"schema_version", "publication_lineage"}):
        raise ValidationFailure("snapshot identity fields are not non-empty strings")
    try:
        publication_date = _datetime.date.fromisoformat(snapshot["publication_date"])
    except (TypeError, ValueError) as exc:
        raise ValidationFailure("snapshot publication_date is invalid") from exc
    if snapshot["last_material_update"] != snapshot["publication_date"] or publication_date.isoformat() != snapshot["publication_date"]:
        raise ValidationFailure("snapshot dates are inconsistent")
    lineage = snapshot["publication_lineage"]
    if not isinstance(lineage, dict) or not all(isinstance(lineage.get(field), str) and lineage[field] for field in ("id", "version")):
        raise ValidationFailure("snapshot publication_lineage is invalid")
    if not all(_SNAPSHOT_COMMIT_RE.fullmatch(snapshot[field]) for field in ("public_snapshot_commit", "private_lineage_commit")):
        raise ValidationFailure("snapshot commit identity is invalid")

    readme = _read_text(root, "README.md")
    start_here = _read_text(root, "docs/current/start_here.md")
    identity_values = (
        snapshot["snapshot_id"],
        snapshot["publication_date"],
        lineage["id"],
        snapshot["status"],
        snapshot["public_snapshot_commit"],
        snapshot["private_lineage_commit"],
    )
    if not all(value in readme and value in start_here for value in identity_values):
        raise ValidationFailure("snapshot identity is not reflected in both front doors")
    if "Machine-readable record: [docs/publication/public_snapshot.json](docs/publication/public_snapshot.json)" not in readme:
        raise ValidationFailure("README snapshot link is missing")
    if "Machine-readable record: [../publication/public_snapshot.json](../publication/public_snapshot.json)" not in start_here:
        raise ValidationFailure("start-here snapshot link is missing")


def _load_harborview_module(root: Path) -> ModuleType:
    module_path = root / "tests" / "test_public_sanitized_tool_call_worked_example.py"
    spec = importlib.util.spec_from_file_location("public_harborview_validation", module_path)
    if spec is None or spec.loader is None:
        raise ValidationFailure("Harborview validation module cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise ValidationFailure("Harborview validation module failed to load") from exc
    return module


def _validate_harborview(root: Path) -> None:
    module = _load_harborview_module(root)
    for name in _HARBORVIEW_VALIDATORS:
        validator = getattr(module, name, None)
        if not callable(validator):
            raise ValidationFailure(f"Harborview validator is unavailable: {name}")
        try:
            validator()
        except Exception as exc:
            raise ValidationFailure(f"Harborview validator failed: {name}") from exc


def _run_phase(label: str, callback: Callable[[], None]) -> bool:
    try:
        callback()
    except Exception as exc:
        print(f"[FAIL] {label}: {exc}")
        return False
    print(f"[PASS] {label}")
    return True


def main() -> int:
    root_holder: dict[str, Path] = {}

    def resolve_and_check_root() -> None:
        repo_paths = _load_repo_paths()
        root = repo_paths.resolve_repo_root(start=Path(__file__))
        _require_surfaces(root)
        root_holder["root"] = root

    phases = (
        ("repository root and required public surfaces", resolve_and_check_root),
        ("snapshot/front-door consistency", lambda: _validate_snapshot_front_door(root_holder["root"])),
        (
            "public reference validation",
            lambda: _validate_reference_package(root_holder["root"]),
        ),
        ("Harborview public example validation", lambda: _validate_harborview(root_holder["root"])),
    )
    for label, callback in phases:
        if not _run_phase(label, callback):
            print("Public package validation: FAIL")
            return 1
    print("Public package validation: PASS")
    return 0


def _validate_reference_package(root: Path) -> None:
    validator = _load_reference_validator(root)
    result = validator.validate(root)
    if not result.get("valid", False):
        raise ValidationFailure("public reference validator returned FAIL")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[FAIL] repository root and required public surfaces: {exc}")
        print("Public package validation: FAIL")
        raise SystemExit(1)
