from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .artifacts import ARTIFACT_SPECS, AUTHORITY_INPUTS, AUTHORITY_SURFACES, HASH_CLAIMS
from .hashing import sha256_file
from .schemas import SCHEMA_VERSION


AUTHORITY_PRECEDENCE: tuple[str, ...] = (
    "canonical contracts and governance artifacts",
    "executed machine-readable source artifacts",
    "published comparison and bundle manifests",
    "narrative reports, journals, and continuity notes",
    "draft artifacts and unapproved notes",
)


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _artifact_payload(repo_root: Path, spec) -> dict[str, Any]:
    absolute_path = (repo_root / spec.relative_path).resolve()
    return {
        "artifact_id": spec.artifact_id,
        "relative_path": spec.relative_path,
        "absolute_path": str(absolute_path),
        "surface_id": spec.surface_id,
        "role": spec.role,
        "required": spec.required,
        "authority_tier": spec.authority_tier,
        "description": spec.description,
        "notes": list(spec.notes),
    }


def _authority_input_payload(repo_root: Path, relative_path: str) -> dict[str, Any]:
    absolute_path = (repo_root / relative_path).resolve()
    present = absolute_path.exists()
    payload = {
        "relative_path": relative_path,
        "absolute_path": str(absolute_path),
        "present": present,
        "required": True,
        "size_bytes": absolute_path.stat().st_size if present and absolute_path.is_file() else None,
        "sha256": sha256_file(absolute_path) if present and absolute_path.is_file() else None,
        "status": "present" if present else "missing",
    }
    return payload


def build_authority_resolution(repo_root: Path) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    artifact_specs = tuple(ARTIFACT_SPECS)
    claim_specs = tuple(HASH_CLAIMS)

    claim_groups: dict[str, list[Any]] = defaultdict(list)
    for claim in claim_specs:
        claim_groups[claim.artifact_id].append(claim)

    artifact_payloads: dict[str, dict[str, Any]] = {}
    artifacts: list[dict[str, Any]] = []
    for spec in artifact_specs:
        payload = _artifact_payload(repo_root, spec)
        claims = claim_groups.get(spec.artifact_id, [])
        payload["claim_labels"] = [claim.claim_label for claim in claims]
        payload["claim_sources"] = [str((repo_root / claim.claim_source).resolve()) for claim in claims]
        payload["published_sha256s"] = [claim.published_sha256 for claim in claims]
        payload["corroborators"] = [str((repo_root / rel).resolve()) for rel in sorted({rel for claim in claims for rel in claim.corroborators})]
        artifact_payloads[spec.artifact_id] = payload
        artifacts.append(payload)

    surfaces: list[dict[str, Any]] = []
    for surface in AUTHORITY_SURFACES:
        primary_artifacts = [artifact_payloads[artifact_id] for artifact_id in surface.primary_artifact_ids]
        corroborating_artifacts = [artifact_payloads[artifact_id] for artifact_id in surface.corroborating_artifact_ids]
        surfaces.append(
            {
                "surface_id": surface.surface_id,
                "title": surface.title,
                "primary_artifact_ids": list(surface.primary_artifact_ids),
                "corroborating_artifact_ids": list(surface.corroborating_artifact_ids),
                "primary_artifacts": primary_artifacts,
                "corroborating_artifacts": corroborating_artifacts,
                "notes": list(surface.notes),
            }
        )

    authority_inputs = [_authority_input_payload(repo_root, rel) for rel in AUTHORITY_INPUTS]
    missing_authority_inputs = sum(1 for item in authority_inputs if not item["present"])
    authority_failures = []
    for item in authority_inputs:
        if not item["present"]:
            authority_failures.append(
                {
                    "failure_code": "MISSING_REQUIRED_AUTHORITY_INPUT",
                    "severity": "blocking",
                    "surface_id": "authority",
                    "artifact_id": item["relative_path"],
                    "artifact_path": item["absolute_path"],
                    "expected_value": "present",
                    "observed_value": "missing",
                    "notes": [f"required authority input missing: {item['relative_path']}"],
                }
            )

    hash_claims: list[dict[str, Any]] = []
    for claim in claim_specs:
        hash_claims.append(
            {
                "claim_label": claim.claim_label,
                "artifact_id": claim.artifact_id,
                "artifact_path": artifact_payloads[claim.artifact_id]["absolute_path"],
                "published_sha256": claim.published_sha256,
                "claim_source": str((repo_root / claim.claim_source).resolve()),
                "corroborators": [str((repo_root / rel).resolve()) for rel in claim.corroborators],
                "required": claim.required,
                "notes": list(claim.notes),
            }
        )

    status = "blocked" if missing_authority_inputs else "pass"
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": _now_utc(),
        "repo_root": str(repo_root),
        "precedence": list(AUTHORITY_PRECEDENCE),
        "authority_inputs": authority_inputs,
        "missing_authority_input_count": missing_authority_inputs,
        "failures": authority_failures,
        "artifacts": artifacts,
        "artifact_count": len(artifacts),
        "surfaces": surfaces,
        "surface_count": len(surfaces),
        "hash_claims": hash_claims,
        "hash_claim_count": len(hash_claims),
        "status": status,
    }


def iter_artifact_specs():
    return tuple(ARTIFACT_SPECS)


def iter_hash_claims():
    return tuple(HASH_CLAIMS)


def iter_authority_inputs():
    return tuple(AUTHORITY_INPUTS)
