from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .artifacts import ARTIFACT_SPECS, HASH_CLAIMS
from .failures import HashMismatchError, MissingRequiredArtifactError
from .hashing import sha256_file
from .models import ArtifactInventoryEntry
from .source_map import build_historical_source_map
from .schemas import (
    PROVENANCE_BLOCKING_STATUSES,
    PROVENANCE_STATUSES,
    SCHEMA_VERSION,
)


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _first_published_sha256(claims: list[Any]) -> str | None:
    if not claims:
        return None
    value = claims[0].published_sha256
    return str(value) if value is not None else None


def _build_historical_source_map_payload(
    historical_source_map: dict[str, Any],
    *,
    artifact_id: str,
) -> dict[str, Any] | None:
    entries_by_artifact_id = historical_source_map.get("entries_by_artifact_id", {})
    if not isinstance(entries_by_artifact_id, dict):
        return None
    entries = entries_by_artifact_id.get(artifact_id, [])
    if not isinstance(entries, list) or not entries:
        return None
    selected_entry = next(
        (
            entry
            for entry in entries
            if isinstance(entry, dict)
            and entry.get("validation_status") == "accepted"
            and entry.get("resolution_status") == "resolved"
        ),
        None,
    )
    if selected_entry is None:
        selected_entry = next(
            (
                entry
                for entry in entries
                if isinstance(entry, dict) and entry.get("validation_status") == "accepted"
            ),
            None,
        )
    if selected_entry is None:
        selected_entry = entries[0] if isinstance(entries[0], dict) else None
    return {
        "source_map_path": historical_source_map.get("source_map_path"),
        "status": historical_source_map.get("status"),
        "present": historical_source_map.get("present"),
        "entry_count": len(entries),
        "entries": entries,
        "selected_entry": selected_entry,
        "selected_historical_reference": selected_entry.get("historical_reference") if isinstance(selected_entry, dict) else None,
        "counts": historical_source_map.get("counts", {}),
    }


def _classify_provenance_status(
    *,
    tracked: bool,
    required: bool,
    present: bool,
    current_live_sha256: str | None,
    published_sha256: str | None,
    historical_reference: dict[str, Any] | None,
    artifact_path: str,
) -> tuple[str | None, str | None, str | None, str | None, str | None]:
    if not tracked:
        return None, None, None, None, None
    if not present:
        return "missing_required_source" if required else None, None, None, None, None
    if current_live_sha256 is None or published_sha256 is None:
        return "missing_required_source" if required else None, None, None, None, None
    if current_live_sha256 == published_sha256:
        return "current_match", "current", artifact_path, current_live_sha256, None

    if historical_reference is not None:
        resolution_status = str(historical_reference.get("resolution_status") or "")
        selected_sha256 = historical_reference.get("selected_evidence_sha256")
        selected_kind = historical_reference.get("selected_evidence_kind")
        selected_ref = historical_reference.get("selected_evidence_ref")
        resolution_error = historical_reference.get("resolution_error")
        if resolution_status == "resolved" and isinstance(selected_sha256, str):
            if selected_sha256 == published_sha256:
                return "stale_but_resolvable", selected_kind, selected_ref, selected_sha256, resolution_error
            return "hash_mismatch", selected_kind, selected_ref, selected_sha256, resolution_error
        if resolution_status in {"unresolved", "not_attempted"}:
            return "stale_unresolved", "current", artifact_path, current_live_sha256, resolution_error

    return "stale_unresolved", "current", artifact_path, current_live_sha256, None


def build_source_inventory(
    repo_root: Path,
    *,
    strict: bool = False,
    historical_source_map: dict[str, Any] | None = None,
) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    if historical_source_map is None:
        historical_source_map = build_historical_source_map(repo_root, None)
    claim_groups: dict[str, list[Any]] = defaultdict(list)
    for claim in HASH_CLAIMS:
        claim_groups[claim.artifact_id].append(claim)

    artifacts: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    surface_counts: dict[str, int] = defaultdict(int)
    role_counts: dict[str, int] = defaultdict(int)
    hash_status_counts: dict[str, int] = defaultdict(int)
    provenance_status_counts: dict[str, int] = {status: 0 for status in PROVENANCE_STATUSES}
    blocked_artifact_ids: list[str] = []
    historical_source_map_failures = list(historical_source_map.get("failures", []))
    historical_reference_count = 0
    historical_resolution_success_count = 0
    historical_resolution_failure_count = 0

    for spec in ARTIFACT_SPECS:
        abs_path = (repo_root / spec.relative_path).resolve()
        present = abs_path.exists() and abs_path.is_file()
        size_bytes: int | None = None
        computed_sha256: str | None = None
        current_live_sha256: str | None = None
        published_sha256: str | None = None
        selected_evidence_kind: str | None = None
        selected_evidence_ref: str | None = None
        selected_evidence_sha256: str | None = None
        resolution_error: str | None = None
        historical_reference: dict[str, Any] | None = None
        provenance_status: str | None = None
        hash_status = "missing"
        status = "missing"

        claims = claim_groups.get(spec.artifact_id, [])
        claim_labels = tuple(claim.claim_label for claim in claims)
        claim_sources = tuple(str((repo_root / claim.claim_source).resolve()) for claim in claims)
        published_sha256s = tuple(claim.published_sha256 for claim in claims)
        published_sha256 = _first_published_sha256(claims)
        artifact_historical_source_map = _build_historical_source_map_payload(
            historical_source_map,
            artifact_id=spec.artifact_id,
        )
        if artifact_historical_source_map is not None:
            historical_reference_count += 1
            historical_reference = artifact_historical_source_map.get("selected_historical_reference")
            if isinstance(historical_reference, dict) and historical_reference.get("resolution_status") == "resolved":
                historical_resolution_success_count += 1
            else:
                historical_resolution_failure_count += 1

        if present:
            size_bytes = abs_path.stat().st_size
            computed_sha256 = sha256_file(abs_path)
            current_live_sha256 = computed_sha256
            status = "present"
            historical_resolution = None
            if artifact_historical_source_map is not None:
                selected_entry = artifact_historical_source_map.get("selected_entry")
                if isinstance(selected_entry, dict):
                    selected_reference = selected_entry.get("historical_reference")
                    if isinstance(selected_reference, dict):
                        historical_resolution = selected_reference
            provenance_status, selected_evidence_kind, selected_evidence_ref, selected_evidence_sha256, resolution_error = _classify_provenance_status(
                tracked=bool(spec.provenance_tracked),
                required=spec.required,
                present=present,
                current_live_sha256=current_live_sha256,
                published_sha256=published_sha256,
                historical_reference=historical_resolution,
                artifact_path=str(abs_path),
            )
            if provenance_status in {"current_match", "stale_but_resolvable"}:
                hash_status = "match"
            elif provenance_status == "missing_required_source":
                hash_status = "missing"
            elif provenance_status is None:
                hash_status = "unclaimed"
            else:
                hash_status = "mismatch"
            if provenance_status == "hash_mismatch":
                failures.append(
                    {
                        "failure_code": "HASH_MISMATCH",
                        "severity": "fatal",
                        "surface_id": spec.surface_id,
                        "artifact_id": spec.artifact_id,
                        "artifact_path": str(abs_path),
                        "expected_value": list(published_sha256s),
                        "observed_value": selected_evidence_sha256,
                        "claim_labels": list(claim_labels),
                        "claim_sources": list(claim_sources),
                        "notes": [f"historical evidence mismatch for {spec.artifact_id}"],
                    }
                )
            elif provenance_status == "stale_unresolved":
                failures.append(
                    {
                        "failure_code": "HASH_MISMATCH",
                        "severity": "blocking",
                        "surface_id": spec.surface_id,
                        "artifact_id": spec.artifact_id,
                        "artifact_path": str(abs_path),
                        "expected_value": published_sha256,
                        "observed_value": selected_evidence_sha256,
                        "notes": [resolution_error or f"unresolved provenance gap for {spec.artifact_id}"],
                    }
                )
        else:
            if spec.required:
                failures.append(
                    {
                        "failure_code": "MISSING_REQUIRED_SOURCE_ARTIFACT",
                        "severity": "blocking",
                        "surface_id": spec.surface_id,
                        "artifact_id": spec.artifact_id,
                        "artifact_path": str(abs_path),
                        "expected_value": "present",
                        "observed_value": "missing",
                        "claim_labels": list(claim_labels),
                        "claim_sources": list(claim_sources),
                        "notes": [f"required source artifact missing: {spec.relative_path}"],
                    }
                )
            provenance_status, selected_evidence_kind, selected_evidence_ref, selected_evidence_sha256, resolution_error = _classify_provenance_status(
                tracked=bool(spec.provenance_tracked),
                required=spec.required,
                present=present,
                current_live_sha256=current_live_sha256,
                published_sha256=published_sha256,
                historical_reference=historical_reference,
                artifact_path=str(abs_path),
            )
            if provenance_status == "missing_required_source":
                hash_status = "missing"
            elif provenance_status == "current_match":
                hash_status = "match"
            elif provenance_status in {"stale_but_resolvable"}:
                hash_status = "match"
            elif provenance_status is None:
                hash_status = "unclaimed"
            else:
                hash_status = "mismatch"

        if spec.required:
            surface_counts[spec.surface_id] += 1
        role_counts[spec.role] += 1
        hash_status_counts[hash_status] += 1
        if provenance_status is not None:
            provenance_status_counts[provenance_status] += 1
            if provenance_status in PROVENANCE_BLOCKING_STATUSES:
                blocked_artifact_ids.append(spec.artifact_id)

        entry = ArtifactInventoryEntry(
            artifact_id=spec.artifact_id,
            relative_path=spec.relative_path,
            absolute_path=str(abs_path),
            surface_id=spec.surface_id,
            role=spec.role,
            required=spec.required,
            present=present,
            size_bytes=size_bytes,
            sha256=computed_sha256,
            current_live_sha256=current_live_sha256,
            published_sha256=published_sha256,
            selected_evidence_kind=selected_evidence_kind,
            selected_evidence_ref=selected_evidence_ref,
            selected_evidence_sha256=selected_evidence_sha256,
            claim_labels=claim_labels,
            claim_sources=claim_sources,
            published_sha256s=published_sha256s,
            authority_tier=spec.authority_tier,
            provenance_status=provenance_status,
            hash_status=hash_status,
            status=status,
            notes=spec.notes,
            historical_source_map=artifact_historical_source_map,
            historical_reference=historical_reference,
            resolution_error=resolution_error,
        )
        artifacts.append(entry.to_dict())

    failures.extend(historical_source_map_failures)
    status = "pass" if not failures else "blocked"
    blocked_artifact_ids = sorted(dict.fromkeys(blocked_artifact_ids))
    result = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": _now_utc(),
        "repo_root": str(repo_root),
        "status": status,
        "historical_source_map": historical_source_map,
        "historical_source_map_status": historical_source_map.get("status"),
        "historical_source_map_path": historical_source_map.get("source_map_path"),
        "artifacts": artifacts,
        "failures": failures,
        "provenance_status_counts": provenance_status_counts,
        "blocked_artifact_ids": blocked_artifact_ids,
        "counts": {
            "artifact_count": len(artifacts),
            "required_artifact_count": sum(1 for spec in ARTIFACT_SPECS if spec.required),
            "present_artifact_count": sum(1 for item in artifacts if item["present"]),
            "missing_artifact_count": sum(1 for item in artifacts if not item["present"]),
            "missing_required_artifact_count": sum(1 for item in failures if item["failure_code"] == "MISSING_REQUIRED_SOURCE_ARTIFACT"),
            "current_match_count": sum(1 for item in artifacts if item["provenance_status"] == "current_match"),
            "stale_but_resolvable_count": sum(1 for item in artifacts if item["provenance_status"] == "stale_but_resolvable"),
            "stale_unresolved_count": sum(1 for item in artifacts if item["provenance_status"] == "stale_unresolved"),
            "missing_required_source_count": sum(1 for item in artifacts if item["provenance_status"] == "missing_required_source"),
            "hash_match_count": sum(1 for item in artifacts if item["hash_status"] == "match"),
            "hash_mismatch_count": sum(1 for item in artifacts if item["hash_status"] == "mismatch"),
            "hash_unclaimed_count": sum(1 for item in artifacts if item["hash_status"] == "unclaimed"),
            "provenance_artifact_count": sum(1 for item in artifacts if item.get("provenance_status") is not None),
            "blocked_provenance_artifact_count": len(blocked_artifact_ids),
            "historical_reference_count": historical_reference_count,
            "historical_resolution_success_count": historical_resolution_success_count,
            "historical_resolution_failure_count": historical_resolution_failure_count,
            "historical_source_map_entry_count": int(historical_source_map.get("counts", {}).get("entry_count", 0)),
            "historical_source_map_accepted_entry_count": int(historical_source_map.get("counts", {}).get("accepted_entry_count", 0)),
            "historical_source_map_rejected_entry_count": int(historical_source_map.get("counts", {}).get("rejected_entry_count", 0)),
            "historical_source_map_path_invalid_count": int(historical_source_map.get("counts", {}).get("path_invalid_count", 0)),
            "historical_source_map_resolution_attempt_count": int(historical_source_map.get("counts", {}).get("resolution_attempt_count", 0)),
            "historical_source_map_resolution_success_count": int(historical_source_map.get("counts", {}).get("resolution_success_count", 0)),
            "historical_source_map_resolution_failure_count": int(historical_source_map.get("counts", {}).get("resolution_failure_count", 0)),
            "historical_source_map_failure_count": len(historical_source_map_failures),
        },
        "surface_counts": dict(surface_counts),
        "role_counts": dict(role_counts),
        "hash_status_counts": dict(hash_status_counts),
    }

    if strict and failures:
        first = failures[0]
        if first["failure_code"] == "MISSING_REQUIRED_SOURCE_ARTIFACT":
            raise MissingRequiredArtifactError(first["artifact_path"])
        if first["failure_code"] == "HASH_MISMATCH":
            raise HashMismatchError(first["artifact_path"])
    return result
