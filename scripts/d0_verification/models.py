from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ArtifactSpec:
    artifact_id: str
    relative_path: str
    surface_id: str
    role: str
    required: bool = True
    authority_tier: int = 2
    provenance_tracked: bool = False
    description: str = ""
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class HashClaim:
    claim_label: str
    artifact_id: str
    published_sha256: str
    claim_source: str
    corroborators: tuple[str, ...] = ()
    required: bool = True
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class AuthoritySurface:
    surface_id: str
    title: str
    primary_artifact_ids: tuple[str, ...]
    corroborating_artifact_ids: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class AuthorityResolution:
    repo_root: str
    generated_utc: str
    precedence: tuple[str, ...]
    authority_inputs: tuple[str, ...]
    surfaces: tuple[dict[str, Any], ...]
    artifacts: tuple[dict[str, Any], ...]
    hash_claims: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class ArtifactInventoryEntry:
    artifact_id: str
    relative_path: str
    absolute_path: str
    surface_id: str
    role: str
    required: bool
    present: bool
    size_bytes: int | None
    sha256: str | None
    current_live_sha256: str | None = None
    published_sha256: str | None = None
    selected_evidence_kind: str | None = None
    selected_evidence_ref: str | None = None
    selected_evidence_sha256: str | None = None
    claim_labels: tuple[str, ...] = ()
    claim_sources: tuple[str, ...] = ()
    published_sha256s: tuple[str, ...] = ()
    authority_tier: int = 2
    provenance_status: str | None = None
    historical_source_map: dict[str, Any] | None = None
    historical_reference: dict[str, Any] | None = None
    resolution_error: str | None = None
    hash_status: str = "unknown"
    status: str = "unknown"
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "relative_path": self.relative_path,
            "absolute_path": self.absolute_path,
            "surface_id": self.surface_id,
            "role": self.role,
            "required": self.required,
            "present": self.present,
            "size_bytes": self.size_bytes,
            "sha256": self.sha256,
            "current_live_sha256": self.current_live_sha256,
            "published_sha256": self.published_sha256,
            "selected_evidence_kind": self.selected_evidence_kind,
            "selected_evidence_ref": self.selected_evidence_ref,
            "selected_evidence_sha256": self.selected_evidence_sha256,
            "claim_labels": list(self.claim_labels),
            "claim_sources": list(self.claim_sources),
            "published_sha256s": list(self.published_sha256s),
            "authority_tier": self.authority_tier,
            "provenance_status": self.provenance_status,
            "historical_source_map": self.historical_source_map,
            "historical_reference": self.historical_reference,
            "resolution_error": self.resolution_error,
            "hash_status": self.hash_status,
            "status": self.status,
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class HashLedgerEntry:
    artifact_id: str
    relative_path: str
    absolute_path: str
    surface_id: str
    role: str
    required: bool
    present: bool
    size_bytes: int | None
    computed_sha256: str | None = None
    current_live_sha256: str | None = None
    published_sha256: str | None = None
    selected_evidence_kind: str | None = None
    selected_evidence_ref: str | None = None
    selected_evidence_sha256: str | None = None
    claim_labels: tuple[str, ...] = ()
    claim_sources: tuple[str, ...] = ()
    published_sha256s: tuple[str, ...] = ()
    provenance_status: str | None = None
    historical_source_map: dict[str, Any] | None = None
    historical_reference: dict[str, Any] | None = None
    resolution_error: str | None = None
    hash_status: str = "unknown"
    status: str = "unknown"
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "relative_path": self.relative_path,
            "absolute_path": self.absolute_path,
            "surface_id": self.surface_id,
            "role": self.role,
            "required": self.required,
            "present": self.present,
            "size_bytes": self.size_bytes,
            "current_live_sha256": self.current_live_sha256,
            "published_sha256": self.published_sha256,
            "selected_evidence_kind": self.selected_evidence_kind,
            "selected_evidence_ref": self.selected_evidence_ref,
            "selected_evidence_sha256": self.selected_evidence_sha256,
            "computed_sha256": self.computed_sha256,
            "claim_labels": list(self.claim_labels),
            "claim_sources": list(self.claim_sources),
            "published_sha256s": list(self.published_sha256s),
            "provenance_status": self.provenance_status,
            "historical_source_map": self.historical_source_map,
            "historical_reference": self.historical_reference,
            "resolution_error": self.resolution_error,
            "hash_status": self.hash_status,
            "status": self.status,
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class DryRunSummary:
    run_id: str
    repo_root: str
    output_root: str
    dry_run_root: str
    generated_utc: str
    authority_resolution_path: str
    inventory_path: str
    hash_ledger_path: str
    status: str
    counts: dict[str, Any] = field(default_factory=dict)
    errors: tuple[dict[str, Any], ...] = ()
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "run_id": self.run_id,
            "repo_root": self.repo_root,
            "output_root": self.output_root,
            "dry_run_root": self.dry_run_root,
            "generated_utc": self.generated_utc,
            "authority_resolution_path": self.authority_resolution_path,
            "inventory_path": self.inventory_path,
            "hash_ledger_path": self.hash_ledger_path,
            "status": self.status,
            "counts": self.counts,
            "errors": [dict(item) for item in self.errors],
            "notes": list(self.notes),
        }
