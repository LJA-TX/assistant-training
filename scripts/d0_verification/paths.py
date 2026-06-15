from __future__ import annotations

import re
from pathlib import Path

from repo_paths import resolve_repo_root

from .failures import OutputRootContainmentError, RunIdValidationError
from .schemas import (
    CERTIFICATION_NAMESPACE,
    DEFAULT_OUTPUT_ROOT_RELATIVE,
    DRY_RUN_NAMESPACE,
)

RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def get_repo_root() -> Path:
    return resolve_repo_root()


def validate_run_id(run_id: str) -> str:
    candidate = run_id.strip()
    if not candidate:
        raise RunIdValidationError("run_id must not be empty")
    if not RUN_ID_RE.fullmatch(candidate):
        raise RunIdValidationError(
            "run_id must match ^[A-Za-z0-9][A-Za-z0-9._-]*$ and must not contain path separators"
        )
    return candidate


def default_output_root(repo_root: Path | None = None) -> Path:
    base = repo_root if repo_root is not None else get_repo_root()
    return base / DEFAULT_OUTPUT_ROOT_RELATIVE


def ensure_output_root(output_root: Path | None, repo_root: Path | None = None) -> Path:
    if output_root is not None:
        return Path(output_root).expanduser().resolve()
    return default_output_root(repo_root=repo_root).resolve()


def ensure_contained(base: Path, candidate: Path) -> Path:
    base_resolved = Path(base).expanduser().resolve()
    candidate_resolved = Path(candidate).expanduser().resolve()
    if not candidate_resolved.is_relative_to(base_resolved):
        raise OutputRootContainmentError(f"{candidate_resolved} escapes the allowed base {base_resolved}")
    return candidate_resolved


def build_dry_run_root(output_root: Path, run_id: str) -> Path:
    safe_run_id = validate_run_id(run_id)
    root = ensure_contained(output_root, output_root / DRY_RUN_NAMESPACE / safe_run_id)
    return root


def build_certification_root(output_root: Path, run_id: str) -> Path:
    safe_run_id = validate_run_id(run_id)
    root = ensure_contained(output_root, output_root / CERTIFICATION_NAMESPACE / safe_run_id)
    return root


def repo_relative(repo_root: Path, relative_path: str) -> Path:
    return (Path(repo_root) / Path(relative_path)).resolve()


def safe_relative_path(base: Path, candidate: Path) -> str:
    base_resolved = Path(base).expanduser().resolve()
    candidate_resolved = Path(candidate).expanduser().resolve()
    if not candidate_resolved.is_relative_to(base_resolved):
        raise OutputRootContainmentError(f"{candidate_resolved} escapes the allowed base {base_resolved}")
    return str(candidate_resolved.relative_to(base_resolved))
