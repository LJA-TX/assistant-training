from __future__ import annotations

import json
import os
import re
import subprocess
from datetime import date
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_PATH = REPO_ROOT / "docs" / "publication" / "public_snapshot.json"
ASSESSMENT_PATH = REPO_ROOT / "docs" / "current" / "status" / "PUBLIC_SNAPSHOT_IDENTITY_AND_VERSIONING_ASSESSMENT.md"
EXPECTED_PUBLIC_COMMIT = "05634b6a3f47dfd6cf5656d4ab8da7997bf894d1"
EXPECTED_PRIVATE_COMMIT = "9d88798c506328635200b95b5aff9234dc127079"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict:
    return json.loads(_read_text(path))


def test_public_snapshot_metadata_is_historical_and_well_formed() -> None:
    snapshot = _load_json(SNAPSHOT_PATH)

    assert snapshot["schema_version"] == 1
    assert snapshot["snapshot_id"] == "publication-lineage-v2-snapshot-v1"
    assert snapshot["snapshot_version"] == "v1"
    assert date.fromisoformat(snapshot["publication_date"]).isoformat() == "2026-07-11"
    assert snapshot["last_material_update"] == snapshot["publication_date"]
    assert snapshot["publication_lineage"] == {
        "id": "Publication Lineage Version 2",
        "version": "v2",
    }
    assert snapshot["status"] == "living curated package with a frozen historical publication snapshot"
    assert snapshot["public_snapshot_commit"] == EXPECTED_PUBLIC_COMMIT
    assert snapshot["private_lineage_commit"] == EXPECTED_PRIVATE_COMMIT
    assert re.fullmatch(r"[0-9a-f]{40}", snapshot["public_snapshot_commit"])
    assert re.fullmatch(r"[0-9a-f]{40}", snapshot["private_lineage_commit"])
    assert "future commits do not invalidate" in snapshot["relationship"]
    assert "private engineering continues independently" in snapshot["relationship"]
    assert snapshot["release_model"] == "not a semantic-versioned software release"
    assert "public_commit" not in snapshot
    assert "private_canonical_commit" not in snapshot


def test_public_snapshot_metadata_matches_front_door_docs() -> None:
    snapshot = _load_json(SNAPSHOT_PATH)
    readme = _read_text(REPO_ROOT / "README.md")
    start_here = _read_text(REPO_ROOT / "docs" / "current" / "start_here.md")
    assessment = _read_text(ASSESSMENT_PATH)

    expected_fragments = [
        snapshot["snapshot_id"],
        snapshot["publication_date"],
        snapshot["publication_lineage"]["id"],
        snapshot["status"],
        snapshot["public_snapshot_commit"],
        snapshot["private_lineage_commit"],
    ]
    for fragment in expected_fragments:
        assert fragment in readme
        assert fragment in start_here
        assert fragment in assessment

    assert "Machine-readable record: [docs/publication/public_snapshot.json](docs/publication/public_snapshot.json)" in readme
    assert "Machine-readable record: [../publication/public_snapshot.json](../publication/public_snapshot.json)" in start_here
    assert "[docs/publication/public_snapshot.json](../../publication/public_snapshot.json)" in assessment
    assert "historical frozen publication point" in readme
    assert "related public/private lineage" in start_here


def test_snapshot_identity_uses_historical_fields_not_live_head_fields() -> None:
    snapshot = _load_json(SNAPSHOT_PATH)
    assert "public_snapshot_commit" in snapshot
    assert "private_lineage_commit" in snapshot
    assert "public_head" not in snapshot
    assert "private_head" not in snapshot
    assert snapshot["relationship"].startswith("This record identifies one frozen public publication point")


def test_snapshot_material_contains_no_workstation_paths_or_sensitive_markers() -> None:
    combined = "\n".join(
        [
            _read_text(SNAPSHOT_PATH),
            _read_text(REPO_ROOT / "README.md"),
            _read_text(REPO_ROOT / "docs" / "current" / "start_here.md"),
            _read_text(ASSESSMENT_PATH),
        ]
    )

    assert "/opt/" not in combined
    assert "/home/" not in combined
    assert not re.search(r"[A-Za-z]:\\\\", combined)
    lowered = combined.lower()
    assert "begin private key" not in lowered
    assert "password" not in lowered
    assert "secret" not in lowered


def test_assessment_has_durable_private_acceptance_and_separate_public_governance() -> None:
    assessment = _read_text(ASSESSMENT_PATH)
    assert "Status: accepted snapshot identity; public publication and annotated tagging are separately governed" in assessment
    assert "pending review" not in assessment
    assert "pending separate authorization" not in assessment
    assert "Whether this record is present in a particular checkout or remote is established by that repository's history" in assessment
    assert "Public projection and publication, and annotated-tag creation, remain separately governed operations" in assessment
    assert "This document does not assert that the annotated tag exists; tag presence must be verified independently in Git history" in assessment
    assert "The JSON record remains authoritative whether or not a tag exists" in assessment
    assert "has not yet been projected" not in assessment
    assert "has not yet been published" not in assessment
    assert "No tag has been created or pushed" not in assessment
    assert "has not been accepted" not in assessment
    assert "has not been committed" not in assessment
    assert "/opt/" not in assessment
    assert "/home/" not in assessment

    source = _read_text(Path(__file__))
    head_token = "HE" + "AD"
    assert head_token not in source


def test_optional_snapshot_object_validation_skips_without_explicit_repositories() -> None:
    public_root = os.environ.get("ASSISTANT_TRAINING_SNAPSHOT_PUBLIC_ROOT")
    private_root = os.environ.get("ASSISTANT_TRAINING_SNAPSHOT_PRIVATE_ROOT")
    if not public_root or not private_root:
        pytest.skip("optional snapshot repository integration paths are not configured")

    for root, commit in (
        (Path(public_root), EXPECTED_PUBLIC_COMMIT),
        (Path(private_root), EXPECTED_PRIVATE_COMMIT),
    ):
        if not (root / ".git").exists():
            pytest.skip("configured snapshot repository integration path is unavailable")
        subprocess.run(
            ["git", "-C", str(root), "cat-file", "-e", f"{commit}^{{commit}}"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
