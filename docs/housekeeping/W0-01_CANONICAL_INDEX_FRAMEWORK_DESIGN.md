# Canonical Index Framework Design

## Work Package

- ID: `W0-01`
- Title: `Canonical Index Framework Design`
- Repository: `/opt/ai-stack/assistant-training`
- Scope: index framework design only
- Authority basis:
  - `docs/housekeeping/HOUSEKEEPING_PRESERVATION_INDEX.md`
  - `docs/housekeeping/HOUSEKEEPING_ARCHITECTURE_AND_MIGRATION_PLAN.md`
  - `docs/housekeeping/HOUSEKEEPING_PATH_DECOUPLING_AND_COMPATIBILITY_STRATEGY.md`
  - `docs/housekeeping/HOUSEKEEPING_COMPATIBILITY_LAYER_IMPLEMENTATION_PLAN.md`
  - `docs/housekeeping/MP-01_MIGRATION_PREPARATION_BOUNDARY_ASSESSMENT.md`
  - `docs/housekeeping/MP-02_CANONICAL_MIGRATION_MAP_AND_INDEXING_PLAN.md`
- Out of scope:
  - file moves
  - archive creation
  - restructuring
  - code changes
  - doctrine changes
  - deletions
  - index implementation

## Current State Basis

- MP-02 identified Wave 0 as `Navigation and Index Foundation`.
- The repository is ready for migration planning, but not ready for structural migration.
- CL-01 and CL-02 reduced active path coupling enough to make a canonical index framework feasible.
- No structural movement is authorized.

## Planning Principles

1. Indexes are authoritative navigation records, not content migrations.
2. Stable IDs are immutable once minted.
3. Every moved or promoted artifact must keep a source-path crosswalk.
4. Historical evidence retains original path strings as provenance.
5. A future move is invalid unless its index entry exists first.

## A. Index Architecture

### Overall Structure

The index framework should be a small registry of family indexes, all rooted in one governance-adjacent location:

- `docs/housekeeping/indexes/`

Recommended file set:

- `docs/housekeeping/indexes/index_registry.json`
- `docs/housekeeping/indexes/convergence_history_index.json`
- `docs/housekeeping/indexes/reports_index.json`
- `docs/housekeeping/indexes/manifests_index.json`
- `docs/housekeeping/indexes/fixture_index.json`
- `docs/housekeeping/indexes/sample_artifact_index.json`
- `docs/housekeeping/indexes/archive_index.json`
- optional human-readable companions:
  - `docs/housekeeping/indexes/README.md`
  - family-specific `*.md` summaries when needed for navigation

### Registry Role

`index_registry.json` should be the top-level directory for the family indexes. It should list:

- schema version
- family name
- owning steward
- canonical file path
- status
- last verified timestamp
- relationships to other families

### Family Index Roles

| Family index | Primary purpose | Recommended granularity | Key relationship |
|---|---|---|---|
| Convergence history index | Track canonical convergence records and their current locations | package-level plus record-level | references history, selected synthesis, and archive families |
| Reports index | Track run and report bundles, including active sample-bearing reports | run-level plus report-bundle-level | references manifests, samples, and archives |
| Manifests index | Track run manifests, config families, and canonical evaluation manifest records | manifest-family plus version-level | references reports, fixtures, and active scripts/tests |
| Fixture index | Track reusable fixtures and threshold profiles | fixture-family plus content-level | references active evaluator chain and sample artifacts |
| Sample-artifact index | Track promoted sample inputs extracted from report surfaces | sample-artifact-level plus source-bundle-level | references reports and active evaluator consumers |
| Archive index | Track preserved-but-off-path materials and their discoverability | archive-bundle-level plus source-family-level | references all historical families and redirect targets |

### Required Common Fields

Each family entry should expose, at minimum:

- `stable_id`
- `current_path`
- `canonical_path`
- `source_path`
- `previous_paths`
- `status`
- `role`
- `hash` where content identity matters
- `provenance_note`
- `related_ids`
- `last_verified`

## B. Index Storage Strategy

### File Formats

- Canonical index records should be stored in JSON.
- Markdown should be used only as a human-readable companion layer.
- JSON is preferred for the authoritative ledgers because the repository already uses JSON for manifests and the indexes will need deterministic validation.
- Markdown summaries are optional renderings for navigation and review.

### Locations

- Immediate Wave 0 implementation location: `docs/housekeeping/indexes/`
- Future extracted location, only if later authorized: `docs/framework/indexes/` or an equivalent framework surface

Keeping the initial implementation under `docs/housekeeping/` keeps the first index work close to governance and away from structural movement.

### Maintenance Model

- Append-only in intent: new records should be added without reassigning existing IDs.
- Corrections should create a new versioned entry or a superseding entry, not silently repurpose an old ID.
- Any move, promotion, or archive action must update the source and destination crosswalk entries in the same change.
- Family indexes should be updated whenever a touched artifact is moved, promoted, archived, or reclassified.

### Update Responsibilities

| Role | Responsibility |
|---|---|
| Package author | Draft the first index entries for the touched family and keep them aligned with the package scope |
| Housekeeping reviewer | Verify crosswalk completeness, ID uniqueness, and discoverability |
| Repo maintainer | Accept schema changes and ensure the registry remains authoritative |
| Tooling/validation | Check schema, link targets, hashes, and orphan detection |

## C. Identifier Strategy

### Stable ID Rules

- IDs must not encode filesystem location.
- IDs must be immutable once minted.
- If content changes materially, create a new ID and link it to the prior one through `supersedes`, `derived_from`, or `promoted_from`.
- A moved artifact keeps its ID; only the path fields change.

### ID Formats

| Artifact type | Stable ID pattern | Immutability expectation |
|---|---|---|
| Convergence records | `conv:<package_id>:<ordinal>` | Mint once; never reuse; path changes do not change ID |
| Reports | `rpt:<run_id>:<ordinal>` | Mint once per report bundle; derived reports get new IDs |
| Manifests | `mfst:<family>:<version>` | Versioned manifests are immutable; edits produce a new versioned ID |
| Fixtures | `fix:<fixture_family>:<content_hash8>` | Content-derived identity; same content should map to the same ID |
| Sample artifacts | `samp:<source_report_id>:<role>:<ordinal>` | Derived artifact identity; new promotion or extraction yields a new ID |
| Archives | `arc:<source_family>:<ordinal>` | Archive identity is permanent and must never be recycled |

### Immutability Expectations

1. IDs are forever unique within their namespace.
2. IDs are never reassigned to different content.
3. Path moves, redirects, and aliases do not alter the ID.
4. A derived artifact receives a new ID and a recorded parent link.

## D. Crosswalk Strategy

### Forward References

Forward references map the old world to the new one:

- old path -> stable ID
- stable ID -> canonical path
- stable ID -> current role

### Backward References

Backward references keep the historical chain visible:

- stable ID -> prior paths
- stable ID -> source artifact
- stable ID -> predecessor IDs where a record was promoted or superseded

### Provenance References

Provenance references should capture:

- original source path
- canonical target path
- content hash where applicable
- parent or source bundle
- reason for promotion, archive, or move

### Old-Path Preservation Handling

- Historical evidence should keep the original path string in the record itself.
- Indexes may add redirect targets or aliases, but they should not normalize away the preserved path.
- Compatibility layers can resolve old paths for active consumers; provenance records should still show the original path as recorded evidence.
- If a record is archived, the index must preserve both the original location and the discoverability location.

## E. Validation Strategy

### Baseline Validation Requirements

Future indexes should validate that:

1. every indexed entry has a unique stable ID
2. every required family has at least one canonical index entry
3. every active consumer has a resolvable entry
4. every moved or archived item has a forward and backward crosswalk
5. every fixture or sample artifact has provenance back to its source bundle
6. every archive entry preserves original path information
7. no orphaned active dependency remains on an unindexed moved path

### Family-Specific Validation

| Index family | Validation focus |
|---|---|---|
| Convergence history index | package coverage, record coverage, canonical record discoverability, old-path map completeness |
| Reports index | run coverage, report bundle coverage, sample-report split coverage, backward references to source runs |
| Manifests index | version coverage, runtime path resolution, pinned provenance retention |
| Fixture index | hash stability, active-consumer inventory, threshold-profile linkage |
| Sample-artifact index | source bundle linkage, promotion rationale, active evaluator coverage |
| Archive index | discoverability, reason-for-archive, original path preservation |

### Validation Model

- validate schema before use
- validate crosswalk completeness before movement
- validate path resolution after any move or alias update
- validate hash and provenance for copied or promoted content
- validate that no active workflow depends solely on an archive-only path

## F. Wave 0 Readiness Determination

### Determination

The repository will be ready for first index implementation after W0-01, provided this design is accepted as the canonical index framework.

### Why It Is Ready

- The relevant families are identified.
- The storage location and file strategy are defined.
- Stable ID rules are defined.
- Forward, backward, and provenance crosswalks are defined.
- Validation requirements are defined.
- The package remains non-structural and does not depend on moving content first.

### Remaining Boundaries

- This does not authorize any structural move.
- This does not authorize archive creation.
- This does not authorize pruning or deletion.
- This does not change doctrine or runtime behavior.

### Final Readiness Answer

Yes: W0-01 provides sufficient design clarity for the first index implementation package.

The first implementation package should remain a Wave 0 non-structural change set that creates the registry and family indexes without moving repository content.
