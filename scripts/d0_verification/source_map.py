from __future__ import annotations

import json
import re
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .artifacts import ARTIFACT_SPECS
from .hashing import sha256_bytes
from .paths import safe_relative_path
from .schemas import (
    HISTORICAL_SOURCE_MAP_REFERENCE_KINDS,
    HISTORICAL_SOURCE_MAP_STATUSES,
    SCHEMA_VERSION,
)

_OID_RE = re.compile(r"^[0-9a-fA-F]{7,64}$")


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _failure(
    failure_code: str,
    *,
    artifact_id: str | None = None,
    artifact_path: str | None = None,
    expected_value: Any = None,
    observed_value: Any = None,
    notes: list[str] | None = None,
) -> dict[str, Any]:
    payload = {
        "failure_code": failure_code,
        "severity": "blocking",
        "surface_id": "historical_source_map",
        "artifact_id": artifact_id,
        "artifact_path": artifact_path,
        "expected_value": expected_value,
        "observed_value": observed_value,
        "notes": list(notes or []),
    }
    return payload


def _not_provided_report(*, repo_root: Path, source_map_path: Path | None) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": _now_utc(),
        "repo_root": str(Path(repo_root).resolve()),
        "source_map_path": str(source_map_path.resolve()) if source_map_path is not None else None,
        "present": False,
        "status": "not_provided",
        "entries": [],
        "entries_by_artifact_id": {},
        "failures": [],
        "counts": {
            "entry_count": 0,
            "accepted_entry_count": 0,
            "rejected_entry_count": 0,
            "resolution_attempt_count": 0,
            "resolution_success_count": 0,
            "resolution_failure_count": 0,
            "tracked_artifact_entry_count": 0,
            "unknown_artifact_count": 0,
            "untracked_artifact_count": 0,
            "duplicate_artifact_id_count": 0,
            "path_invalid_count": 0,
            "path_mismatch_count": 0,
            "reference_kind_invalid_count": 0,
            "reference_oid_invalid_count": 0,
            "reference_kind_git_commit_count": 0,
            "reference_kind_git_blob_count": 0,
        },
        "notes": [
            "historical source-map parsing is available, but no source map was provided",
        ],
    }


def _normalize_repo_path(repo_root: Path, raw_repo_path: Any) -> tuple[str | None, str | None]:
    if not isinstance(raw_repo_path, str):
        return None, "repo_path must be a string"
    candidate = raw_repo_path.strip()
    if not candidate:
        return None, "repo_path must not be empty"
    candidate_path = Path(candidate)
    if candidate_path.is_absolute():
        return None, "repo_path must be repo-relative"
    resolved = (repo_root / candidate_path).resolve()
    if not resolved.is_relative_to(repo_root):
        return None, "repo_path escapes repository root"
    return safe_relative_path(repo_root, resolved), None


def _validate_reference_oid(reference_kind: str, entry: dict[str, Any]) -> tuple[str | None, dict[str, Any] | None]:
    oid_key = "commit_oid" if reference_kind == "git_commit" else "blob_oid"
    oid = entry.get(oid_key)
    if not isinstance(oid, str) or not _OID_RE.fullmatch(oid.strip()):
        return None, _failure(
            "HISTORICAL_SOURCE_MAP_REFERENCE_OID_INVALID",
            artifact_id=str(entry.get("artifact_id") or ""),
            artifact_path=str(entry.get("repo_path") or ""),
            expected_value=f"hex oid for {reference_kind}",
            observed_value=oid,
            notes=[f"{oid_key} must be a non-empty hexadecimal object id"],
        )
    return oid.strip().lower(), None


def _reference_fields(entry: dict[str, Any]) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    if "commit_oid" in entry:
        fields["commit_oid"] = entry.get("commit_oid")
    if "blob_oid" in entry:
        fields["blob_oid"] = entry.get("blob_oid")
    return fields


def _run_git_text(repo_root: Path, *args: str) -> tuple[str | None, str | None]:
    proc = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=False,
        capture_output=True,
    )
    if proc.returncode != 0:
        stderr = proc.stderr.decode("utf-8", errors="replace").strip()
        return None, stderr or f"git {' '.join(args)} failed with exit code {proc.returncode}"
    return proc.stdout.decode("utf-8", errors="replace").strip(), None


def _run_git_bytes(repo_root: Path, *args: str) -> tuple[bytes | None, str | None]:
    proc = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=False,
        capture_output=True,
    )
    if proc.returncode != 0:
        stderr = proc.stderr.decode("utf-8", errors="replace").strip()
        return None, stderr or f"git {' '.join(args)} failed with exit code {proc.returncode}"
    return proc.stdout, None


def _resolve_git_commit_reference(
    repo_root: Path,
    *,
    commit_oid: str,
    repo_path: str,
) -> tuple[str | None, bytes | None, str | None]:
    blob_oid, error = _run_git_text(repo_root, "rev-parse", f"{commit_oid}:{repo_path}")
    if error is not None:
        return None, None, error
    if blob_oid is None or not _OID_RE.fullmatch(blob_oid):
        return None, None, f"git rev-parse returned invalid blob oid for {commit_oid}:{repo_path}"
    blob_bytes, blob_error = _run_git_bytes(repo_root, "cat-file", "blob", blob_oid)
    if blob_error is not None:
        return None, None, blob_error
    return blob_oid.lower(), blob_bytes, None


def _resolve_git_blob_reference(repo_root: Path, *, blob_oid: str) -> tuple[str | None, bytes | None, str | None]:
    blob_bytes, blob_error = _run_git_bytes(repo_root, "cat-file", "blob", blob_oid)
    if blob_error is not None:
        return None, None, blob_error
    return blob_oid.lower(), blob_bytes, None


def build_historical_source_map(repo_root: Path, source_map_path: Path | None) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    if source_map_path is None:
        return _not_provided_report(repo_root=repo_root, source_map_path=None)

    resolved_source_map_path = Path(source_map_path)
    if not resolved_source_map_path.is_absolute():
        resolved_source_map_path = repo_root / resolved_source_map_path
    resolved_source_map_path = resolved_source_map_path.resolve()
    if not resolved_source_map_path.is_relative_to(repo_root):
        return {
            **_not_provided_report(repo_root=repo_root, source_map_path=resolved_source_map_path),
            "present": False,
            "status": "blocked",
            "failures": [
                _failure(
                    "HISTORICAL_SOURCE_MAP_PATH_OUTSIDE_REPO",
                    artifact_path=str(resolved_source_map_path),
                    expected_value=str(repo_root),
                    observed_value=str(resolved_source_map_path),
                    notes=["historical source map must live inside the repository root"],
                )
            ],
        }
    if not resolved_source_map_path.exists() or not resolved_source_map_path.is_file():
        return {
            **_not_provided_report(repo_root=repo_root, source_map_path=resolved_source_map_path),
            "present": False,
            "status": "blocked",
            "failures": [
                _failure(
                    "HISTORICAL_SOURCE_MAP_FILE_MISSING",
                    artifact_path=str(resolved_source_map_path),
                    expected_value="present",
                    observed_value="missing",
                    notes=["historical source map file is missing"],
                )
            ],
        }

    try:
        payload = json.loads(resolved_source_map_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            **_not_provided_report(repo_root=repo_root, source_map_path=resolved_source_map_path),
            "present": True,
            "status": "blocked",
            "failures": [
                _failure(
                    "HISTORICAL_SOURCE_MAP_PARSE_ERROR",
                    artifact_path=str(resolved_source_map_path),
                    expected_value="valid JSON object",
                    observed_value=str(exc),
                    notes=["historical source map could not be parsed as JSON"],
                )
            ],
        }

    known_specs = {spec.artifact_id: spec for spec in ARTIFACT_SPECS}
    tracked_specs = {spec.artifact_id: spec for spec in ARTIFACT_SPECS if spec.provenance_tracked}
    failures: list[dict[str, Any]] = []
    entries: list[dict[str, Any]] = []
    entries_by_artifact_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    counts: dict[str, int] = {
        "entry_count": 0,
        "accepted_entry_count": 0,
        "rejected_entry_count": 0,
        "resolution_attempt_count": 0,
        "resolution_success_count": 0,
        "resolution_failure_count": 0,
        "tracked_artifact_entry_count": 0,
        "unknown_artifact_count": 0,
        "untracked_artifact_count": 0,
        "duplicate_artifact_id_count": 0,
        "path_invalid_count": 0,
        "path_mismatch_count": 0,
        "reference_kind_invalid_count": 0,
        "reference_oid_invalid_count": 0,
        "reference_kind_git_commit_count": 0,
        "reference_kind_git_blob_count": 0,
    }

    schema_version = str(payload.get("schema_version") or "")
    if schema_version != SCHEMA_VERSION:
        failures.append(
            _failure(
                "HISTORICAL_SOURCE_MAP_SCHEMA_INVALID",
                artifact_path=str(resolved_source_map_path),
                expected_value=SCHEMA_VERSION,
                observed_value=schema_version or None,
                notes=["schema_version must match the D0 schema version"],
            )
        )

    references = payload.get("references")
    if not isinstance(references, list):
        failures.append(
            _failure(
                "HISTORICAL_SOURCE_MAP_SCHEMA_INVALID",
                artifact_path=str(resolved_source_map_path),
                expected_value="references array",
                observed_value=type(references).__name__,
                notes=["historical source map must contain a references array"],
            )
        )
        references = []

    seen_artifact_ids: set[str] = set()
    for index, raw_entry in enumerate(references):
        counts["entry_count"] += 1
        structural_failures: list[dict[str, Any]] = []
        resolution_failures: list[dict[str, Any]] = []
        artifact_id = ""
        raw_repo_path = None
        reference_kind = ""
        canonical_repo_path: str | None = None
        reference_oid: str | None = None
        resolution_status = "not_attempted"
        resolution_error: str | None = None
        selected_evidence_kind: str | None = None
        selected_evidence_ref: str | None = None
        selected_evidence_sha256: str | None = None

        if not isinstance(raw_entry, dict):
            failure = _failure(
                "HISTORICAL_SOURCE_MAP_SCHEMA_INVALID",
                artifact_path=str(resolved_source_map_path),
                expected_value="reference object",
                observed_value=type(raw_entry).__name__,
                notes=[f"references[{index}] must be an object"],
            )
            failures.append(failure)
            counts["rejected_entry_count"] += 1
            entries.append(
                {
                    "entry_index": index,
                    "artifact_id": None,
                    "artifact_known": False,
                    "artifact_tracked": False,
                    "repo_path": None,
                    "canonical_repo_path": None,
                    "reference_kind": None,
                    "reference_oid": None,
                    "reference_fields": {},
                    "validation_status": "rejected",
                    "validation_failures": [failure],
                    "resolution_status": "not_attempted",
                    "resolution_failures": [],
                    "resolution_error": None,
                    "selected_evidence_kind": None,
                    "selected_evidence_ref": None,
                    "selected_evidence_sha256": None,
                    "historical_reference": None,
                    "source_map_path": str(resolved_source_map_path),
                }
            )
            continue

        artifact_id = str(raw_entry.get("artifact_id") or "").strip()
        raw_repo_path = raw_entry.get("repo_path")
        reference_kind = str(raw_entry.get("reference_kind") or "").strip()

        if not artifact_id:
            structural_failures.append(
                _failure(
                    "HISTORICAL_SOURCE_MAP_ARTIFACT_ID_INVALID",
                    artifact_path=str(resolved_source_map_path),
                    expected_value="non-empty artifact_id",
                    observed_value=raw_entry.get("artifact_id"),
                    notes=[f"references[{index}] missing artifact_id"],
                )
            )
        elif artifact_id not in known_specs:
            counts["unknown_artifact_count"] += 1
            structural_failures.append(
                _failure(
                    "HISTORICAL_SOURCE_MAP_ARTIFACT_UNKNOWN",
                    artifact_id=artifact_id,
                    artifact_path=str(resolved_source_map_path),
                    expected_value=sorted(known_specs),
                    observed_value=artifact_id,
                    notes=[f"references[{index}] references an unknown artifact id"],
                )
            )
        elif artifact_id not in tracked_specs:
            counts["untracked_artifact_count"] += 1
            structural_failures.append(
                _failure(
                    "HISTORICAL_SOURCE_MAP_ARTIFACT_NOT_TRACKED",
                    artifact_id=artifact_id,
                    artifact_path=str(resolved_source_map_path),
                    expected_value="provenance-tracked artifact",
                    observed_value=artifact_id,
                    notes=[f"references[{index}] points to an artifact not tracked for historical provenance"],
                )
            )
        else:
            counts["tracked_artifact_entry_count"] += 1

        if artifact_id and artifact_id in seen_artifact_ids:
            counts["duplicate_artifact_id_count"] += 1
            structural_failures.append(
                _failure(
                    "HISTORICAL_SOURCE_MAP_DUPLICATE_ARTIFACT_ID",
                    artifact_id=artifact_id,
                    artifact_path=str(resolved_source_map_path),
                    expected_value="unique artifact_id",
                    observed_value=artifact_id,
                    notes=[f"references[{index}] duplicates a previous entry"],
                )
            )
        elif artifact_id:
            seen_artifact_ids.add(artifact_id)

        if raw_repo_path is None:
            counts["path_invalid_count"] += 1
            structural_failures.append(
                _failure(
                    "HISTORICAL_SOURCE_MAP_PATH_INVALID",
                    artifact_id=artifact_id or None,
                    artifact_path=str(resolved_source_map_path),
                    expected_value="repo-relative path",
                    observed_value=None,
                    notes=[f"references[{index}] missing repo_path"],
                )
            )
        else:
            canonical_repo_path, path_error = _normalize_repo_path(repo_root, raw_repo_path)
            if path_error is not None:
                counts["path_invalid_count"] += 1
                structural_failures.append(
                    _failure(
                        "HISTORICAL_SOURCE_MAP_PATH_INVALID",
                        artifact_id=artifact_id or None,
                        artifact_path=str(resolved_source_map_path),
                        expected_value="repo-relative path",
                        observed_value=raw_repo_path,
                        notes=[path_error],
                    )
                )
            elif artifact_id in tracked_specs and canonical_repo_path != tracked_specs[artifact_id].relative_path:
                counts["path_mismatch_count"] += 1
                structural_failures.append(
                    _failure(
                        "HISTORICAL_SOURCE_MAP_PATH_MISMATCH",
                        artifact_id=artifact_id,
                        artifact_path=str(resolved_source_map_path),
                        expected_value=tracked_specs[artifact_id].relative_path,
                        observed_value=canonical_repo_path,
                        notes=[f"references[{index}] repo_path does not match the registered artifact path"],
                    )
                )

        if reference_kind not in HISTORICAL_SOURCE_MAP_REFERENCE_KINDS:
            counts["reference_kind_invalid_count"] += 1
            structural_failures.append(
                _failure(
                    "HISTORICAL_SOURCE_MAP_REFERENCE_KIND_INVALID",
                    artifact_id=artifact_id or None,
                    artifact_path=str(resolved_source_map_path),
                    expected_value=list(HISTORICAL_SOURCE_MAP_REFERENCE_KINDS),
                    observed_value=reference_kind or None,
                    notes=[f"references[{index}] reference_kind is not supported"],
                )
            )
        else:
            counts[f"reference_kind_{reference_kind}_count"] += 1
            reference_oid, oid_failure = _validate_reference_oid(reference_kind, raw_entry)
            if oid_failure is not None:
                counts["reference_oid_invalid_count"] += 1
                structural_failures.append(oid_failure)

        validation_status = "accepted" if not structural_failures else "rejected"
        if validation_status == "accepted":
            counts["accepted_entry_count"] += 1
        else:
            counts["rejected_entry_count"] += 1
            failures.extend(structural_failures)

        if validation_status == "accepted" and reference_oid is not None:
            counts["resolution_attempt_count"] += 1
            if reference_kind == "git_commit":
                selected_evidence_ref, resolved_bytes, resolution_error = _resolve_git_commit_reference(
                    repo_root,
                    commit_oid=reference_oid,
                    repo_path=str(canonical_repo_path),
                )
                selected_evidence_kind = "git_commit"
                if resolution_error is None and resolved_bytes is not None:
                    resolution_status = "resolved"
                    counts["resolution_success_count"] += 1
                    selected_evidence_sha256 = sha256_bytes(resolved_bytes)
                else:
                    resolution_status = "unresolved"
                    counts["resolution_failure_count"] += 1
                    failure = _failure(
                        "HISTORICAL_SOURCE_MAP_REFERENCE_UNRESOLVABLE",
                        artifact_id=artifact_id,
                        artifact_path=str(resolved_source_map_path),
                        expected_value=f"{reference_kind}:{reference_oid}",
                        observed_value=resolution_error,
                        notes=[f"references[{index}] could not be materialized from git history"],
                    )
                    failures.append(failure)
                    resolution_failures.append(failure)
                    resolution_error = "git_commit_unresolvable"
                    selected_evidence_ref = None
            else:
                selected_evidence_ref, resolved_bytes, resolution_error = _resolve_git_blob_reference(
                    repo_root,
                    blob_oid=reference_oid,
                )
                selected_evidence_kind = "git_blob"
                if resolution_error is None and resolved_bytes is not None:
                    resolution_status = "resolved"
                    counts["resolution_success_count"] += 1
                    selected_evidence_sha256 = sha256_bytes(resolved_bytes)
                else:
                    resolution_status = "unresolved"
                    counts["resolution_failure_count"] += 1
                    failure = _failure(
                        "HISTORICAL_SOURCE_MAP_REFERENCE_UNRESOLVABLE",
                        artifact_id=artifact_id,
                        artifact_path=str(resolved_source_map_path),
                        expected_value=f"{reference_kind}:{reference_oid}",
                        observed_value=resolution_error,
                        notes=[f"references[{index}] could not be materialized from git history"],
                    )
                    failures.append(failure)
                    resolution_failures.append(failure)
                    resolution_error = "git_blob_unresolvable"
                    selected_evidence_ref = None

        historical_reference = {
            "artifact_id": artifact_id or None,
            "repo_path": canonical_repo_path if canonical_repo_path is not None else (str(raw_repo_path).strip() if raw_repo_path is not None else None),
            "canonical_repo_path": canonical_repo_path,
            "reference_kind": reference_kind or None,
            "reference_oid": reference_oid,
            "validation_status": validation_status,
            "resolution_status": resolution_status,
            "resolution_error": resolution_error,
            "selected_evidence_kind": selected_evidence_kind,
            "selected_evidence_ref": selected_evidence_ref,
            "selected_evidence_sha256": selected_evidence_sha256,
        }

        entry = {
            "entry_index": index,
            "artifact_id": artifact_id or None,
            "artifact_known": artifact_id in known_specs if artifact_id else False,
            "artifact_tracked": artifact_id in tracked_specs if artifact_id else False,
            "repo_path": str(raw_repo_path).strip() if raw_repo_path is not None else None,
            "canonical_repo_path": canonical_repo_path,
            "reference_kind": reference_kind or None,
            "reference_oid": reference_oid if reference_kind in HISTORICAL_SOURCE_MAP_REFERENCE_KINDS else None,
            "reference_fields": _reference_fields(raw_entry),
            "validation_status": validation_status,
            "validation_failures": structural_failures,
            "resolution_status": resolution_status,
            "resolution_failures": resolution_failures,
            "resolution_error": resolution_error,
            "selected_evidence_kind": selected_evidence_kind,
            "selected_evidence_ref": selected_evidence_ref,
            "selected_evidence_sha256": selected_evidence_sha256,
            "historical_reference": historical_reference,
            "source_map_path": str(resolved_source_map_path),
        }
        entries.append(entry)
        if artifact_id:
            entries_by_artifact_id[artifact_id].append(entry)

    status = "blocked" if failures else "pass"
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": _now_utc(),
        "repo_root": str(repo_root),
        "source_map_path": str(resolved_source_map_path),
        "present": True,
        "status": status,
        "entries": entries,
        "entries_by_artifact_id": {key: value for key, value in entries_by_artifact_id.items()},
        "failures": failures,
        "counts": counts,
        "notes": [
            "historical source-map parsing and validation are metadata-only in Patch 3",
        ],
    }
