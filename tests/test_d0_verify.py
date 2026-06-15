from __future__ import annotations

import json
import sys
import subprocess
from pathlib import Path

import pytest


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from repo_paths import resolve_repo_root

from d0_verification import cli, inventory, paths
from d0_verification.artifacts import ArtifactSpec
from d0_verification.hashing import sha256_file
from d0_verification.source_map import build_historical_source_map


REPO_ROOT = resolve_repo_root(start=Path(__file__))


def test_dry_run_cli_writes_expected_artifacts(tmp_path):
    output_root = tmp_path / "d0-output"
    run_id = "d0_20260615T010203Z"

    exit_code = cli.main(["--run-id", run_id, "--output-root", str(output_root)])
    assert exit_code == 1

    dry_run_root = output_root / "dry_runs" / run_id
    authority_path = dry_run_root / "authority" / "authority_resolution.json"
    inventory_path = dry_run_root / "inventory" / "source_artifact_inventory.json"
    ledger_path = dry_run_root / "ledgers" / "hash_ledger.json"
    summary_path = dry_run_root / "reports" / "dry_run_summary.json"
    log_path = dry_run_root / "logs" / "dry_run.log"

    for path in (authority_path, inventory_path, ledger_path, summary_path, log_path):
        assert path.is_file(), path

    authority = json.loads(authority_path.read_text(encoding="utf-8"))
    assert authority["status"] == "pass"
    assert authority["missing_authority_input_count"] == 0

    inventory_payload = json.loads(inventory_path.read_text(encoding="utf-8"))
    assert inventory_payload["status"] == "blocked"
    assert inventory_payload["historical_source_map_status"] == "not_provided"
    assert inventory_payload["counts"]["artifact_count"] > 0
    assert inventory_payload["blocked_artifact_ids"] == ["dataset_builder", "training_script"]
    assert inventory_payload["provenance_status_counts"]["current_match"] == 1
    assert inventory_payload["provenance_status_counts"]["stale_unresolved"] == 2
    assert inventory_payload["provenance_status_counts"]["missing_required_source"] == 0
    assert inventory_payload["provenance_status_counts"]["hash_mismatch"] == 0
    assert inventory_payload["provenance_status_counts"]["stale_but_resolvable"] == 0
    assert inventory_payload["counts"]["provenance_artifact_count"] == 3
    assert inventory_payload["counts"]["blocked_provenance_artifact_count"] == 2

    ledger_payload = json.loads(ledger_path.read_text(encoding="utf-8"))
    assert ledger_payload["historical_source_map_status"] == "not_provided"
    i3_train_entry = next(item for item in ledger_payload["entries"] if item["artifact_id"] == "i3_train")
    assert i3_train_entry["computed_sha256"] == "c19dbab14d930c39b90f85de8f7bf820f1ac37035756a9ca5063f823369e3f9a"
    scorer_entry = next(item for item in ledger_payload["entries"] if item["artifact_id"] == "eval_scorer")
    assert scorer_entry["current_live_sha256"] == "08a5cec22a781193365bed85b709ceebef534846602004bbfa047f4e0b59d738"
    assert scorer_entry["published_sha256"] == "08a5cec22a781193365bed85b709ceebef534846602004bbfa047f4e0b59d738"
    assert scorer_entry["provenance_status"] == "current_match"
    assert scorer_entry["historical_source_map"] is None
    training_entry = next(item for item in ledger_payload["entries"] if item["artifact_id"] == "training_script")
    assert training_entry["current_live_sha256"] == "faf6cd4b676e230c5d2797392bc2fca204752d012f3e80e71c0af4ced7288432"
    assert training_entry["published_sha256"] == "28900accae3d6abf05ddb9e86b41c03ad3c812a683f3af343bffa94281e14c8b"
    assert training_entry["provenance_status"] == "stale_unresolved"
    dataset_builder_entry = next(item for item in ledger_payload["entries"] if item["artifact_id"] == "dataset_builder")
    assert dataset_builder_entry["current_live_sha256"] == "de830e5e444c811aefb27b2ead056f13611609021f7c2faed0e4ad8ad422ead3"
    assert dataset_builder_entry["published_sha256"] == "05843673f68fc8a492e889fb9e96e87dff09d189f5df220b092f233de82839d9"
    assert dataset_builder_entry["provenance_status"] == "stale_unresolved"

    summary_payload = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary_payload["status"] == "blocked"
    assert summary_payload["historical_source_map_status"] == "not_provided"
    assert summary_payload["blocked_artifact_ids"] == ["dataset_builder", "training_script"]
    assert summary_payload["provenance_status_counts"]["current_match"] == 1
    assert summary_payload["provenance_status_counts"]["stale_unresolved"] == 2
    assert summary_payload["provenance_status_counts"]["missing_required_source"] == 0
    assert summary_payload["provenance_status_counts"]["hash_mismatch"] == 0
    assert summary_payload["provenance_status_counts"]["stale_but_resolvable"] == 0

    summary = cli.run_dry_run(repo_root=REPO_ROOT, output_root=output_root, run_id="d0_20260615T020304Z")
    assert summary["status"] == "blocked"
    assert summary["counts"]["artifact_count"] > 0
    assert summary["counts"]["authority_input_count"] > 0
    assert summary["counts"]["missing_required_artifact_count"] == 0
    assert summary["counts"]["hash_mismatch_count"] == 2
    assert summary["counts"]["provenance_artifact_count"] == 3
    assert summary["counts"]["blocked_provenance_artifact_count"] == 2
    assert summary["blocked_artifact_ids"] == ["dataset_builder", "training_script"]
    assert summary["provenance_status_counts"]["current_match"] == 1
    assert summary["provenance_status_counts"]["stale_unresolved"] == 2
    assert summary["provenance_status_counts"]["missing_required_source"] == 0
    assert summary["provenance_status_counts"]["hash_mismatch"] == 0
    assert summary["provenance_status_counts"]["stale_but_resolvable"] == 0
    failure_codes = [item["failure_code"] for item in summary["failures"]]
    assert failure_codes.count("HASH_MISMATCH") == 2


def test_historical_source_map_parser_accepts_sample_source_map():
    source_map_path = REPO_ROOT / "docs" / "continuity" / "d0_historical_source_map.json"
    report = build_historical_source_map(REPO_ROOT, source_map_path)

    assert report["status"] == "pass"
    assert report["present"] is True
    assert report["counts"]["entry_count"] == 1
    assert report["counts"]["accepted_entry_count"] == 1
    assert report["counts"]["rejected_entry_count"] == 0
    assert report["counts"]["resolution_attempt_count"] == 1
    assert report["counts"]["resolution_success_count"] == 1
    assert report["counts"]["resolution_failure_count"] == 0
    assert report["counts"]["path_invalid_count"] == 0
    assert report["counts"]["path_mismatch_count"] == 0
    assert report["counts"]["reference_kind_invalid_count"] == 0
    assert report["counts"]["reference_oid_invalid_count"] == 0
    dataset_builder_entry = report["entries_by_artifact_id"]["dataset_builder"][0]
    assert dataset_builder_entry["validation_status"] == "accepted"
    assert dataset_builder_entry["resolution_status"] == "resolved"
    assert dataset_builder_entry["selected_evidence_kind"] == "git_commit"
    assert dataset_builder_entry["selected_evidence_sha256"] == "05843673f68fc8a492e889fb9e96e87dff09d189f5df220b092f233de82839d9"
    assert report["entries"][0]["historical_reference"]["reference_kind"] == "git_commit"


@pytest.mark.parametrize(
    ("payload", "expected_failure_code"),
    [
        (
            {
                "schema_version": "1.0",
                "references": [
                    {
                        "artifact_id": "training_script",
                        "reference_kind": "git_commit",
                        "commit_oid": "97491ef0a9556dd9357cc87fe0f788bc21b1dd73",
                    }
                ],
            },
            "HISTORICAL_SOURCE_MAP_PATH_INVALID",
        ),
        (
            {
                "schema_version": "1.0",
                "references": [
                    {
                        "artifact_id": "training_script",
                        "reference_kind": "git_commit",
                        "repo_path": "scripts/build_dataset_v1.py",
                        "commit_oid": "97491ef0a9556dd9357cc87fe0f788bc21b1dd73",
                    }
                ],
            },
            "HISTORICAL_SOURCE_MAP_PATH_MISMATCH",
        ),
        (
            {
                "schema_version": "1.0",
                "references": [
                    {
                        "artifact_id": "training_script",
                        "reference_kind": "git_tag",
                        "repo_path": "scripts/train_lora_sft.py",
                        "commit_oid": "97491ef0a9556dd9357cc87fe0f788bc21b1dd73",
                    }
                ],
            },
            "HISTORICAL_SOURCE_MAP_REFERENCE_KIND_INVALID",
        ),
        (
            {
                "schema_version": "1.0",
                "references": [
                    {
                        "artifact_id": "i3_train",
                        "reference_kind": "git_commit",
                        "repo_path": "data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl",
                        "commit_oid": "97491ef0a9556dd9357cc87fe0f788bc21b1dd73",
                    }
                ],
            },
            "HISTORICAL_SOURCE_MAP_ARTIFACT_NOT_TRACKED",
        ),
        (
            {
                "schema_version": "1.0",
                "references": [
                    {
                        "artifact_id": "unknown_artifact",
                        "reference_kind": "git_commit",
                        "repo_path": "scripts/train_lora_sft.py",
                        "commit_oid": "97491ef0a9556dd9357cc87fe0f788bc21b1dd73",
                    }
                ],
            },
            "HISTORICAL_SOURCE_MAP_ARTIFACT_UNKNOWN",
        ),
    ],
)
def test_historical_source_map_validation_rejections(tmp_path, payload, expected_failure_code):
    source_map_path = tmp_path / "repo" / "d0_historical_source_map.json"
    source_map_path.parent.mkdir(parents=True, exist_ok=True)
    source_map_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    report = build_historical_source_map(tmp_path, source_map_path)

    assert report["status"] == "blocked"
    assert report["present"] is True
    assert report["failures"]
    assert report["failures"][0]["failure_code"] == expected_failure_code
    assert report["counts"]["entry_count"] == 1
    assert report["counts"]["rejected_entry_count"] == 1
    assert report["counts"]["accepted_entry_count"] == 0
    assert report["counts"]["resolution_attempt_count"] == 0
    assert report["counts"]["resolution_success_count"] == 0
    assert report["counts"]["resolution_failure_count"] == 0
    assert report["counts"]["reference_kind_invalid_count"] in {0, 1}
    assert report["counts"]["path_invalid_count"] in {0, 1}


def test_historical_source_map_git_blob_resolution(tmp_path):
    blob_oid = subprocess.check_output(
        ["git", "-C", str(REPO_ROOT), "rev-parse", "7b694fb:scripts/build_dataset_v1.py"],
        text=True,
    ).strip()
    source_map_path = REPO_ROOT / "docs" / "continuity" / ".tmp_d0_historical_source_map_blob_test.json"
    source_map_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "references": [
                    {
                        "artifact_id": "dataset_builder",
                        "reference_kind": "git_blob",
                        "repo_path": "scripts/build_dataset_v1.py",
                        "blob_oid": blob_oid,
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    try:
        report = build_historical_source_map(REPO_ROOT, source_map_path)

        assert report["status"] == "pass"
        assert report["counts"]["resolution_attempt_count"] == 1
        assert report["counts"]["resolution_success_count"] == 1
        entry = report["entries_by_artifact_id"]["dataset_builder"][0]
        assert entry["validation_status"] == "accepted"
        assert entry["resolution_status"] == "resolved"
        assert entry["selected_evidence_kind"] == "git_blob"
        assert entry["selected_evidence_sha256"] == "05843673f68fc8a492e889fb9e96e87dff09d189f5df220b092f233de82839d9"
    finally:
        source_map_path.unlink(missing_ok=True)


def test_dry_run_with_historical_source_map_integration(tmp_path):
    output_root = tmp_path / "d0-output"
    source_map_path = REPO_ROOT / "docs" / "continuity" / "d0_historical_source_map.json"

    summary = cli.run_dry_run(
        repo_root=REPO_ROOT,
        output_root=output_root,
        run_id="d0_20260615T050607Z",
        historical_source_map=source_map_path,
    )

    assert summary["status"] == "blocked"
    assert summary["historical_source_map_status"] == "pass"
    assert summary["historical_source_map_entry_count"] == 1
    assert summary["historical_source_map_accepted_entry_count"] == 1
    assert summary["historical_source_map_rejected_entry_count"] == 0
    assert summary["historical_source_map_resolution_attempt_count"] == 1
    assert summary["historical_source_map_resolution_success_count"] == 1
    assert summary["historical_source_map_resolution_failure_count"] == 0
    assert summary["counts"]["historical_reference_count"] == 1
    assert summary["counts"]["historical_resolution_success_count"] == 1
    assert summary["counts"]["historical_resolution_failure_count"] == 0
    assert summary["counts"]["blocked_provenance_artifact_count"] == 1
    assert summary["counts"]["hash_match_count"] == 2
    assert summary["counts"]["hash_mismatch_count"] == 1
    assert summary["historical_source_map_failure_count"] == 0
    assert summary["provenance_status_counts"]["current_match"] == 1
    assert summary["provenance_status_counts"]["stale_but_resolvable"] == 1
    assert summary["provenance_status_counts"]["stale_unresolved"] == 1

    dry_run_root = output_root / "dry_runs" / "d0_20260615T050607Z"
    inventory_payload = json.loads((dry_run_root / "inventory" / "source_artifact_inventory.json").read_text(encoding="utf-8"))
    ledger_payload = json.loads((dry_run_root / "ledgers" / "hash_ledger.json").read_text(encoding="utf-8"))
    summary_payload = json.loads((dry_run_root / "reports" / "dry_run_summary.json").read_text(encoding="utf-8"))

    assert inventory_payload["historical_source_map_status"] == "pass"
    assert inventory_payload["historical_source_map"]["status"] == "pass"
    assert inventory_payload["counts"]["historical_source_map_entry_count"] == 1
    assert inventory_payload["counts"]["historical_source_map_accepted_entry_count"] == 1
    assert inventory_payload["counts"]["historical_source_map_rejected_entry_count"] == 0
    assert inventory_payload["counts"]["historical_source_map_path_invalid_count"] == 0
    assert inventory_payload["counts"]["historical_reference_count"] == 1
    assert inventory_payload["counts"]["historical_resolution_success_count"] == 1
    assert inventory_payload["counts"]["historical_resolution_failure_count"] == 0
    assert inventory_payload["counts"]["blocked_provenance_artifact_count"] == 1
    assert inventory_payload["counts"]["historical_source_map_failure_count"] == 0
    dataset_builder_entry = next(item for item in ledger_payload["entries"] if item["artifact_id"] == "dataset_builder")
    assert dataset_builder_entry["selected_evidence_kind"] == "git_commit"
    assert dataset_builder_entry["selected_evidence_sha256"] == dataset_builder_entry["published_sha256"]
    assert dataset_builder_entry["hash_status"] == "match"
    assert dataset_builder_entry["provenance_status"] == "stale_but_resolvable"
    assert dataset_builder_entry["historical_reference"]["resolution_status"] == "resolved"
    training_entry = next(item for item in ledger_payload["entries"] if item["artifact_id"] == "training_script")
    assert training_entry["selected_evidence_kind"] == "current"
    assert training_entry["selected_evidence_sha256"] == training_entry["current_live_sha256"]
    assert training_entry["hash_status"] == "mismatch"
    assert training_entry["provenance_status"] == "stale_unresolved"
    assert ledger_payload["historical_source_map_status"] == "pass"
    assert ledger_payload["historical_source_map_entry_count"] == 1
    assert ledger_payload["historical_source_map_accepted_entry_count"] == 1
    assert ledger_payload["historical_source_map_rejected_entry_count"] == 0
    assert ledger_payload["historical_source_map_path_invalid_count"] == 0
    assert ledger_payload["historical_source_map_failure_count"] == 0
    assert summary_payload["historical_source_map_status"] == "pass"
    assert summary_payload["historical_source_map_entry_count"] == 1
    assert summary_payload["historical_source_map_accepted_entry_count"] == 1
    assert summary_payload["historical_source_map_rejected_entry_count"] == 0
    assert summary_payload["historical_source_map_path_invalid_count"] == 0
    assert summary_payload["historical_source_map_resolution_attempt_count"] == 1
    assert summary_payload["historical_source_map_resolution_success_count"] == 1
    assert summary_payload["historical_source_map_resolution_failure_count"] == 0
    assert summary_payload["counts"]["historical_reference_count"] == 1
    assert summary_payload["counts"]["historical_resolution_success_count"] == 1
    assert summary_payload["counts"]["historical_resolution_failure_count"] == 0
    assert summary_payload["counts"]["blocked_provenance_artifact_count"] == 1
    assert summary_payload["blocked_artifact_ids"] == ["training_script"]
    assert summary_payload["provenance_status_counts"]["stale_but_resolvable"] == 1
    assert summary_payload["provenance_status_counts"]["stale_unresolved"] == 1
    assert summary_payload["counts"]["hash_match_count"] == 2
    assert summary_payload["counts"]["hash_mismatch_count"] == 1
    assert summary_payload["historical_source_map_failure_count"] == 0


def test_sha256_file_matches_known_control_hash():
    path = REPO_ROOT / "data" / "v1_0" / "dataset_v1_0_stage_b_recovery_i3_train.jsonl"
    assert sha256_file(path) == "c19dbab14d930c39b90f85de8f7bf820f1ac37035756a9ca5063f823369e3f9a"


def test_output_root_containment_and_run_id_validation(tmp_path):
    base = tmp_path / "allowed"
    escaped = tmp_path / "outside"
    base.mkdir(parents=True, exist_ok=True)
    escaped.mkdir(parents=True, exist_ok=True)

    with pytest.raises(paths.OutputRootContainmentError):
        paths.ensure_contained(base, escaped / "escape")

    with pytest.raises(paths.RunIdValidationError):
        paths.validate_run_id("../escape")

    safe_root = paths.build_dry_run_root(base, "d0_20260615T030405Z")
    assert safe_root.is_relative_to(base.resolve())


def test_missing_required_artifact_is_reported(monkeypatch, tmp_path):
    missing_spec = ArtifactSpec(
        artifact_id="missing_required",
        relative_path="missing_required.jsonl",
        surface_id="test_surface",
        role="primary",
        required=True,
        provenance_tracked=True,
        description="synthetic missing artifact",
    )
    monkeypatch.setattr(inventory, "ARTIFACT_SPECS", (missing_spec,))
    monkeypatch.setattr(inventory, "HASH_CLAIMS", ())

    result = inventory.build_source_inventory(tmp_path)

    assert result["status"] == "blocked"
    assert result["counts"]["missing_required_artifact_count"] == 1
    assert result["failures"][0]["failure_code"] == "MISSING_REQUIRED_SOURCE_ARTIFACT"
    assert result["failures"][0]["artifact_id"] == "missing_required"
    assert result["artifacts"][0]["provenance_status"] == "missing_required_source"
    assert result["provenance_status_counts"]["missing_required_source"] == 1
    assert result["blocked_artifact_ids"] == ["missing_required"]


def test_dry_run_does_not_mutate_source_artifacts(tmp_path):
    target = REPO_ROOT / "data" / "v1_0" / "dataset_v1_0_stage_b_recovery_i3_train.jsonl"
    before_hash = sha256_file(target)
    before_mtime = target.stat().st_mtime_ns

    summary = cli.run_dry_run(
        repo_root=REPO_ROOT,
        output_root=tmp_path / "out",
        run_id="d0_20260615T040506Z",
        historical_source_map=REPO_ROOT / "docs" / "continuity" / "d0_historical_source_map.json",
    )
    assert summary["status"] == "blocked"

    after_hash = sha256_file(target)
    after_mtime = target.stat().st_mtime_ns

    assert after_hash == before_hash
    assert after_mtime == before_mtime
