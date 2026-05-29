# Integration Rehearsal Validation Results (Typed Digest Semantics)

## Validation Matrix
1. Geometry Context Flow
- `geometry_mapping_identity_digest` consistency across mapping artifacts: `PASS`.
- `geometry_context_input_digest` consistency across resolved/detector artifacts: `PASS`.
- Typed digest divergence (`mapping_identity` vs `context_input`) handling: `PASS` (expected when scopes differ).
- Legacy alias semantics (`geometry_context_digest_alias_of`) correctness: `PASS`.

2. Exposure Accounting Flow
- Declared ledger generation: `PASS`.
- Realized ledger generation (weighted captured mode): `PASS`.
- Drift ledger generation: `PASS`.

3. Weighted Sampling Flow
- Deterministic sampler metadata emitted: `PASS`.
- Sampled-stream capture emitted: `PASS`.
- Weight digest generation and consistency: `PASS`.

4. Traceability Flow
- Artifact linkage present and machine-readable graph emitted: `PASS`.
- Threshold profile digest consistency (collapse/gate): `PASS`.
- Typed digest relationship encoding in artifact graph: `PASS`.

5. Collapse Detection Flow
- Threshold profile ingestion: `PASS`.
- Geometry context linkage: `PASS`.
- Detector typed digest emission: `PASS`.
- Gate reporter compatibility: `PASS` (`status=watch`, `progression_allowed=true`).

6. End-to-End Reconstruction Test
- Intended geometry reconstruction: `PASS`.
- Realized geometry reconstruction: `PASS`.
- Weighting configuration reconstruction: `PASS`.
- Threshold profile reconstruction: `PASS`.
- Full lineage chain reconstruction with typed digests: `PASS`.

## Remaining Gaps
- No hard runtime assertion yet for cross-artifact `geometry_context_input_digest` equivalence when both artifacts are present.
- Semantic misuse detection remains in governance/reporting layer.

## Remaining Scientific Risks
- Synthetic rehearsal validates instrumentation semantics, not final behavioral tradeoff quality.
- Live-cell decisions still need pre-agreed drift tolerances and baseline governance.

## Readiness Recommendation
- `READY_FOR_SINGLE_CELL_PROBE`
- Reason: digest ambiguity has been resolved by explicit typed semantics with backward-compatible aliasing; remaining risk is scientific/gov calibration.
