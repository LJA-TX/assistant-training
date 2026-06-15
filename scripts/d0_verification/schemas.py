from __future__ import annotations

from pathlib import Path

SCHEMA_VERSION = "1.0"

PROVENANCE_STATUSES = (
    "current_match",
    "stale_but_resolvable",
    "stale_unresolved",
    "missing_required_source",
    "hash_mismatch",
)

PROVENANCE_BLOCKING_STATUSES = (
    "stale_unresolved",
    "missing_required_source",
    "hash_mismatch",
)

HISTORICAL_SOURCE_MAP_FILENAME = "d0_historical_source_map.json"
HISTORICAL_SOURCE_MAP_SCHEMA_FILENAME = "d0_historical_source_map.schema.json"
HISTORICAL_SOURCE_MAP_REFERENCE_KINDS = (
    "git_commit",
    "git_blob",
)
HISTORICAL_SOURCE_MAP_STATUSES = (
    "not_provided",
    "pass",
    "blocked",
)

DEFAULT_OUTPUT_ROOT_RELATIVE = Path("artifacts") / "d0_reconstruction_verification"
DRY_RUN_NAMESPACE = "dry_runs"
CERTIFICATION_NAMESPACE = "runs"

AUTHORITY_RESOLUTION_FILENAME = "authority_resolution.json"
SOURCE_INVENTORY_FILENAME = "source_artifact_inventory.json"
HASH_LEDGER_FILENAME = "hash_ledger.json"
DRY_RUN_SUMMARY_FILENAME = "dry_run_summary.json"
DRY_RUN_LOG_FILENAME = "dry_run.log"
