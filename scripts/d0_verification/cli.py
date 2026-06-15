from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .authority import build_authority_resolution
from .failures import D0VerificationError
from .hashing import build_hash_ledger
from .inventory import build_source_inventory
from .paths import build_dry_run_root, ensure_output_root, get_repo_root, validate_run_id
from .reports import build_dry_run_summary, write_json
from .source_map import build_historical_source_map
from .schemas import (
    AUTHORITY_RESOLUTION_FILENAME,
    DRY_RUN_LOG_FILENAME,
    DRY_RUN_SUMMARY_FILENAME,
    HASH_LEDGER_FILENAME,
    SOURCE_INVENTORY_FILENAME,
)


def _now_run_id() -> str:
    return datetime.now(tz=timezone.utc).strftime("d0_%Y%m%dT%H%M%SZ")


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the D0 dry-run verification scaffold.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        choices=("dry-run",),
        default="dry-run",
        help="Verification mode. Only dry-run is implemented in this phase.",
    )
    parser.add_argument(
        "--run-id",
        default=None,
        help="Run identifier used under the dry-run output namespace.",
    )
    parser.add_argument(
        "--output-root",
        default=None,
        help="Root directory for D0 outputs. Defaults to the canonical repository artifacts path.",
    )
    parser.add_argument(
        "--historical-source-map",
        default=None,
        help="Optional read-only historical source-map JSON used for provenance metadata validation.",
    )
    return parser


def run_dry_run(
    *,
    repo_root: Path | None = None,
    output_root: Path | None = None,
    run_id: str | None = None,
    historical_source_map: Path | None = None,
) -> dict[str, Any]:
    repo_root_path = Path(repo_root).resolve() if repo_root is not None else get_repo_root()
    resolved_output_root = ensure_output_root(output_root, repo_root=repo_root_path)
    safe_run_id = validate_run_id(run_id or _now_run_id())
    dry_run_root = build_dry_run_root(resolved_output_root, safe_run_id)
    dry_run_root.mkdir(parents=True, exist_ok=True)

    authority_resolution = build_authority_resolution(repo_root_path)
    historical_source_map_report = build_historical_source_map(repo_root_path, historical_source_map)
    inventory = build_source_inventory(repo_root_path, historical_source_map=historical_source_map_report)
    hash_ledger = build_hash_ledger(inventory, generated_utc=authority_resolution["generated_utc"])

    authority_path = dry_run_root / "authority" / AUTHORITY_RESOLUTION_FILENAME
    inventory_path = dry_run_root / "inventory" / SOURCE_INVENTORY_FILENAME
    ledger_path = dry_run_root / "ledgers" / HASH_LEDGER_FILENAME
    summary_path = dry_run_root / "reports" / DRY_RUN_SUMMARY_FILENAME
    log_path = dry_run_root / "logs" / DRY_RUN_LOG_FILENAME

    write_json(authority_path, authority_resolution)
    write_json(inventory_path, inventory)
    write_json(ledger_path, hash_ledger)

    summary = build_dry_run_summary(
        run_id=safe_run_id,
        repo_root=str(repo_root_path),
        output_root=str(resolved_output_root),
        dry_run_root=str(dry_run_root),
        authority_resolution_path=str(authority_path),
        authority_resolution=authority_resolution,
        inventory=inventory,
        hash_ledger=hash_ledger,
        generated_utc=authority_resolution["generated_utc"],
    )
    write_json(summary_path, summary)

    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(
        "\n".join(
            [
                f"run_id={safe_run_id}",
                f"status={summary['status']}",
                f"generated_utc={_now_utc()}",
                f"dry_run_root={dry_run_root}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.mode != "dry-run":
        parser.error("only dry-run mode is implemented in this phase")

    try:
        summary = run_dry_run(
            output_root=Path(args.output_root) if args.output_root is not None else None,
            run_id=args.run_id,
            historical_source_map=Path(args.historical_source_map) if args.historical_source_map is not None else None,
        )
    except D0VerificationError as exc:
        print(f"D0 dry-run failed: {exc}", file=sys.stderr)
        return 2

    return 0 if summary["status"] == "pass" else 1
