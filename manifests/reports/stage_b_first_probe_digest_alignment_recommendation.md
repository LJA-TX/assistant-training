# Stage B First Probe Digest Alignment Recommendation

## Decision
`REGENERATE_BOTH`

## Why
- Current failure is caused by cross-artifact geometry context divergence:
  - sidecar digest envelope reflects `deterministic_weighted_sampler_metadata`
  - runtime execution geometry context reflects `deterministic_weighted_sampler_sidecar_overlay`
- Runtime package also carries stale digest annotation fields that do not match its own `geometry_mapping` payload.

## Why Not Other Options
- `REGENERATE_SIDECAR_ONLY`:
  - likely resolves immediate runtime mismatch,
  - but leaves stale digest annotations in the runtime package and weaker lineage hygiene.
- `REGENERATE_RUNTIME_PACKAGE_ONLY`:
  - does not fix sidecar envelope mismatch because trainer validates against sidecar-declared digest.
- `IMPLEMENT_CODE_FIX`:
  - not required; existing fail-fast behavior correctly detected provenance inconsistency.

## Canonical Alignment Target
Use one canonical geometry context for all first-live-probe artifacts:
- `weighting_mode = deterministic_weighted_sampler_sidecar_overlay`

Regenerate together from that context:
1. geometry context input artifact used by sidecar provisioning
2. sidecar digest envelope artifact
3. runtime package digest annotations

This preserves deterministic replay, sidecar binding integrity, and typed-digest lineage consistency.
