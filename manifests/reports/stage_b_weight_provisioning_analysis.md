# Stage B Weight Provisioning Analysis

## Current-State Observations
- First probe package was blocked by `NO_GO_PENDING_WEIGHT_COVERAGE_RESOLUTION`.
- Probe sampling was already configured for weighted mode with strict metadata defaults (`default_weight=0.0`) but dataset rows had no recognized metadata weight keys.
- The training dataset has repeated row content hashes:
  - train rows: `1982`
  - unique row hashes: `1785`
  - hash-collision rowsets: `157`
- Existing weighted-sampler infrastructure already supported sidecar ingestion but lacked lineage-grade checks for:
  - row-identity digest binding,
  - geometry digest binding,
  - row hash verification in row-list sidecars.

## Option Evaluation Summary
- Option A (direct dataset metadata weights) is fastest but violates Stage B lineage hygiene by embedding probe intent into dataset content.
- Option B (hash->weight sidecar) is directionally correct but collision-prone unless duplicate-hash semantics are explicit and validated.
- Option C (probe-specific overlay sidecar with explicit row identity rows) preserves canonical data and removes collision ambiguity.

## Selected Approach
Selected: `C_probe_specific_overlay_row_identity_rows`

Why:
- Best doctrine fit for Stage B objective-interaction geometry work.
- Minimal attribution ambiguity: explicit `train_index_0based` + `row_hash_sha256` + `weight` per row.
- Preserves dataset lineage: no row edits, no dataset regeneration, no dataset mutation.
- Replayable under digest checks.

## Implementation Scope
1. Trainer-side sidecar ingestion hardening in `scripts/train_lora_sft.py`:
- Added row-identity aware sidecar validation and source-details reporting.
- Added digest checks for optional sidecar envelope fields:
  - `row_identity_reference.rows_digest_sha256`
  - `geometry_mapping_identity_digest`
  - `geometry_context_input_digest`
- Added `rows`-mode row hash verification against runtime row-identity map.
- Added duplicate-aware hash map support for optional `weights_by_row_hash` mode.

2. Probe overlay generator script:
- Added `scripts/provision_geometry_probe_weights.py`.
- Deterministically compiles declared exposure selectors + units into row-level weights.
- Emits sidecar with:
  - `row_identity_reference` digests,
  - typed geometry digests,
  - explicit `rows` list (`train_index_0based`, `row_hash_sha256`, `weight`),
  - family allocation summary and weight summary.

3. First-probe provisioning artifact:
- Generated `manifests/reports/stage_b_first_probe_weights_sidecar.json`.
- Coverage result:
  - positive-weight rows: `13`
  - zero-weight rows: `1969`
  - weights sum: `36.0`

## Doctrine and Governance Notes
- Dataset remains untouched; weighting intent is externalized.
- Sidecar is probe-specific and removable.
- Fail-fast behavior is enforced at load-time for missing rows, bad digests, and row hash mismatch.

## Complexity Assessment
- Implementation complexity: `medium`.
- Risk class: `controlled`, because changes are additive and scoped to weight resolution paths.
