from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .schemas import SCHEMA_VERSION


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def build_hash_ledger(inventory: dict[str, Any], *, generated_utc: str) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    mismatch_count = 0
    missing_count = 0
    unclaimed_count = 0
    historical_source_map = inventory.get("historical_source_map", {})
    historical_source_map_status = historical_source_map.get("status")

    for artifact in inventory.get("artifacts", []):
        if not isinstance(artifact, dict):
            continue
        entry = {
            "artifact_id": artifact.get("artifact_id"),
            "relative_path": artifact.get("relative_path"),
            "absolute_path": artifact.get("absolute_path"),
            "surface_id": artifact.get("surface_id"),
            "role": artifact.get("role"),
            "required": artifact.get("required"),
            "present": artifact.get("present"),
            "size_bytes": artifact.get("size_bytes"),
            "current_live_sha256": artifact.get("current_live_sha256"),
            "published_sha256": artifact.get("published_sha256"),
            "selected_evidence_kind": artifact.get("selected_evidence_kind"),
            "selected_evidence_ref": artifact.get("selected_evidence_ref"),
            "selected_evidence_sha256": artifact.get("selected_evidence_sha256"),
            "computed_sha256": artifact.get("sha256"),
            "claim_labels": list(artifact.get("claim_labels") or []),
            "claim_sources": list(artifact.get("claim_sources") or []),
            "published_sha256s": list(artifact.get("published_sha256s") or []),
            "provenance_status": artifact.get("provenance_status"),
            "historical_source_map": artifact.get("historical_source_map"),
            "historical_reference": artifact.get("historical_reference"),
            "resolution_error": artifact.get("resolution_error"),
            "hash_status": artifact.get("hash_status"),
            "status": artifact.get("status"),
            "notes": list(artifact.get("notes") or []),
        }
        entries.append(entry)
        status = str(entry["hash_status"] or "")
        if status == "mismatch":
            mismatch_count += 1
        elif status == "missing":
            missing_count += 1
        elif status == "unclaimed":
            unclaimed_count += 1

    status = "pass" if mismatch_count == 0 and missing_count == 0 and historical_source_map_status != "blocked" else "blocked"
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": generated_utc,
        "status": status,
        "historical_source_map": historical_source_map,
        "historical_source_map_status": historical_source_map_status,
        "historical_source_map_path": historical_source_map.get("source_map_path"),
        "historical_source_map_entry_count": int(historical_source_map.get("counts", {}).get("entry_count", 0)),
        "historical_source_map_accepted_entry_count": int(historical_source_map.get("counts", {}).get("accepted_entry_count", 0)),
        "historical_source_map_rejected_entry_count": int(historical_source_map.get("counts", {}).get("rejected_entry_count", 0)),
        "historical_source_map_path_invalid_count": int(historical_source_map.get("counts", {}).get("path_invalid_count", 0)),
        "historical_source_map_failure_count": len(historical_source_map.get("failures", []) or []),
        "entries": entries,
        "counts": {
            "artifact_count": len(entries),
            "mismatch_count": mismatch_count,
            "missing_count": missing_count,
            "unclaimed_count": unclaimed_count,
            "matched_count": max(len(entries) - mismatch_count - missing_count - unclaimed_count, 0),
        },
    }


def dumps_hash_ledger(ledger: dict[str, Any]) -> str:
    return json.dumps(ledger, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
