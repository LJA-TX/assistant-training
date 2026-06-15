from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .schemas import PROVENANCE_BLOCKING_STATUSES, PROVENANCE_STATUSES, SCHEMA_VERSION


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _summarize_provenance_statuses(artifacts: list[dict[str, Any]]) -> tuple[dict[str, int], list[str]]:
    counts = {status: 0 for status in PROVENANCE_STATUSES}
    blocked: list[str] = []
    for artifact in artifacts:
        status = artifact.get("provenance_status")
        if not status:
            continue
        status = str(status)
        if status not in counts:
            continue
        counts[status] += 1
        if status in PROVENANCE_BLOCKING_STATUSES:
            artifact_id = artifact.get("artifact_id")
            if artifact_id:
                blocked.append(str(artifact_id))
    return counts, sorted(dict.fromkeys(blocked))


def build_dry_run_summary(
    *,
    run_id: str,
    repo_root: str,
    output_root: str,
    dry_run_root: str,
    authority_resolution_path: str,
    authority_resolution: dict[str, Any],
    inventory: dict[str, Any],
    hash_ledger: dict[str, Any],
    generated_utc: str,
) -> dict[str, Any]:
    authority_inputs = list(authority_resolution.get("authority_inputs", []))
    authority_failures = list(authority_resolution.get("failures", []))
    inventory_failures = list(inventory.get("failures", []))
    historical_source_map = dict(inventory.get("historical_source_map", {}) or {})
    historical_source_map_status = inventory.get("historical_source_map_status")
    provenance_status_counts, blocked_artifact_ids = _summarize_provenance_statuses(
        list(inventory.get("artifacts", []))
    )
    status = "pass"
    if authority_resolution.get("status") != "pass" or inventory.get("status") != "pass" or hash_ledger.get("status") != "pass":
        status = "blocked"

    counts = {
        "authority_input_count": len(authority_inputs),
        "missing_authority_input_count": sum(1 for item in authority_inputs if not item.get("present")),
        "authority_failure_count": len(authority_failures),
        "authority_surface_count": len(authority_resolution.get("surfaces", [])),
        "artifact_count": inventory.get("counts", {}).get("artifact_count", 0),
        "required_artifact_count": inventory.get("counts", {}).get("required_artifact_count", 0),
        "present_artifact_count": inventory.get("counts", {}).get("present_artifact_count", 0),
        "missing_required_artifact_count": inventory.get("counts", {}).get("missing_required_artifact_count", 0),
        "current_match_count": inventory.get("counts", {}).get("current_match_count", 0),
        "stale_but_resolvable_count": inventory.get("counts", {}).get("stale_but_resolvable_count", 0),
        "stale_unresolved_count": inventory.get("counts", {}).get("stale_unresolved_count", 0),
        "missing_required_source_count": inventory.get("counts", {}).get("missing_required_source_count", 0),
        "hash_match_count": inventory.get("counts", {}).get("hash_match_count", 0),
        "hash_mismatch_count": inventory.get("counts", {}).get("hash_mismatch_count", 0),
        "hash_unclaimed_count": inventory.get("counts", {}).get("hash_unclaimed_count", 0),
        "provenance_artifact_count": inventory.get("counts", {}).get("provenance_artifact_count", 0),
        "blocked_provenance_artifact_count": inventory.get("counts", {}).get("blocked_provenance_artifact_count", 0),
        "ledger_entry_count": hash_ledger.get("counts", {}).get("artifact_count", 0),
        "historical_reference_count": inventory.get("counts", {}).get("historical_reference_count", 0),
        "historical_resolution_success_count": inventory.get("counts", {}).get("historical_resolution_success_count", 0),
        "historical_resolution_failure_count": inventory.get("counts", {}).get("historical_resolution_failure_count", 0),
        "historical_source_map_entry_count": inventory.get("counts", {}).get("historical_source_map_entry_count", 0),
        "historical_source_map_accepted_entry_count": inventory.get("counts", {}).get("historical_source_map_accepted_entry_count", 0),
        "historical_source_map_rejected_entry_count": inventory.get("counts", {}).get("historical_source_map_rejected_entry_count", 0),
        "historical_source_map_path_invalid_count": inventory.get("counts", {}).get("historical_source_map_path_invalid_count", 0),
        "historical_source_map_resolution_attempt_count": inventory.get("counts", {}).get("historical_source_map_resolution_attempt_count", 0),
        "historical_source_map_resolution_success_count": inventory.get("counts", {}).get("historical_source_map_resolution_success_count", 0),
        "historical_source_map_resolution_failure_count": inventory.get("counts", {}).get("historical_source_map_resolution_failure_count", 0),
        "historical_source_map_failure_count": inventory.get("counts", {}).get("historical_source_map_failure_count", 0),
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "repo_root": repo_root,
        "output_root": output_root,
        "dry_run_root": dry_run_root,
        "generated_utc": generated_utc,
        "status": status,
        "authority_resolution_path": authority_resolution_path,
        "inventory_path": str(Path(dry_run_root) / "inventory" / "source_artifact_inventory.json"),
        "hash_ledger_path": str(Path(dry_run_root) / "ledgers" / "hash_ledger.json"),
        "historical_source_map_path": historical_source_map.get("source_map_path"),
        "historical_source_map_status": historical_source_map_status,
        "historical_source_map_entry_count": inventory.get("counts", {}).get("historical_source_map_entry_count", 0),
        "historical_source_map_accepted_entry_count": inventory.get("counts", {}).get("historical_source_map_accepted_entry_count", 0),
        "historical_source_map_rejected_entry_count": inventory.get("counts", {}).get("historical_source_map_rejected_entry_count", 0),
        "historical_source_map_path_invalid_count": inventory.get("counts", {}).get("historical_source_map_path_invalid_count", 0),
        "historical_source_map_resolution_attempt_count": inventory.get("counts", {}).get("historical_source_map_resolution_attempt_count", 0),
        "historical_source_map_resolution_success_count": inventory.get("counts", {}).get("historical_source_map_resolution_success_count", 0),
        "historical_source_map_resolution_failure_count": inventory.get("counts", {}).get("historical_source_map_resolution_failure_count", 0),
        "historical_source_map_failure_count": inventory.get("counts", {}).get("historical_source_map_failure_count", 0),
        "provenance_status_counts": provenance_status_counts,
        "blocked_artifact_ids": blocked_artifact_ids,
        "counts": counts,
        "failures": authority_failures + inventory_failures,
        "notes": [
            "dry-run exercises authority resolution, inventory generation, and hash ledger generation only",
        ],
    }
