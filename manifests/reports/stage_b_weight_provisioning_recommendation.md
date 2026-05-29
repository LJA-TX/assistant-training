# Stage B Weight Provisioning Recommendation

## Recommendation
Adopt a **probe-specific row-identity overlay sidecar** as the canonical Stage B weight provisioning mechanism for the first live geometry probe.

## Rationale
- **Stage B doctrine fit**: keeps calibration geometry controls outside canonical dataset content.
- **Attribution clarity**: explicit row-level assignment (`train_index_0based` + `row_hash_sha256` + `weight`) avoids ambiguity from row-hash collisions.
- **Lineage preservation**: dataset provenance is unchanged; weight intent is isolated to a replayable sidecar artifact.
- **Compatibility**: integrates directly with existing `geometry_sampling.kind=sidecar`, row-identity sidecar, and realized/drift exposure ledgers.
- **Fail-fast guarantees**: sidecar loader now rejects missing rows, digest mismatches, and row-hash mismatches when declared.

## Practical Policy
- Canonical first-probe path: sidecar `rows` structure with full explicit coverage.
- Optional `weights_by_row_hash` remains supported for controlled cases, with duplicate-hash collision accounting and explicit expectations.
- Continue to treat dataset-embedded weights as non-preferred except for controlled temporary experiments.
