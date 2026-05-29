# Geometry Digest Recommendation

## Recommendation
- `SPLIT_INTO_DISTINCT_DIGEST_TYPES`

## Why
1. Current evidence indicates two different semantics are already present.
- Mapping stack digest is a reduced, stable geometry-mapping identity digest.
- Detector stack digest is a full detector geometry-context input digest.

2. Treating this as a single canonical digest either loses identity stability or loses context fidelity.
- Harmonizing to mapping (Option A) weakens detector-context traceability.
- Harmonizing to detector (Option B) weakens stable cell identity and increases accidental identity drift.

3. Rehearsal findings point to a lineage-modeling issue, not only a hashing defect.
- Divergence is currently expected by implementation logic but flagged by governance reporting.
- Explicitly typed digests resolve that mismatch without forcing semantic collapse.

## Proposed semantic split (analysis-only)
- `geometry_mapping_identity_digest`:
  - hash basis: `{geometry_schema_version, sweep_id, cell_id, axis_levels, weighting_mode}`
  - purpose: stable mapping cell identity and comparability.
- `geometry_context_input_digest`:
  - hash basis: full supplied geometry context object.
  - purpose: detector/gate input traceability.

## Governance interpretation
- Keep both digests in lineage reconstruction.
- Use mapping identity digest for cross-run cell equivalence checks.
- Use context input digest for detector reproducibility and provenance checks.

## Decision
- Final recommendation class: `SPLIT_INTO_DISTINCT_DIGEST_TYPES`.
