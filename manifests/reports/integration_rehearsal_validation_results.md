# Integration Rehearsal Validation Results

## Validation Matrix
1. Geometry Context Flow
- `geometry_context` propagated into resolved config, declared/realized/drift ledgers, sampler determinism, collapse watch, and gate.
- Mapping digest consistency across mapping artifacts: `PASS`.
- Cross-stack digest equivalence (mapping vs detector): `FAIL` (known contract divergence).

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

5. Collapse Detection Flow
- Threshold profile ingestion: `PASS`.
- Geometry context linkage: `PASS`.
- Detector input preparation with synthetic eval/baseline: `PASS`.
- Gate reporter compatibility: `PASS` (`status=watch`, `progression_allowed=true`).

6. End-to-End Reconstruction Test
- Intended geometry reconstruction: `PASS`.
- Realized geometry reconstruction: `PASS`.
- Weighting configuration reconstruction: `PASS`.
- Threshold profile reconstruction: `PASS`.
- Full lineage chain reconstruction: `PASS`.

## Remaining Gaps
- Digest semantics mismatch:
  - Mapping stack digest: `1f35b81bfe3dfae09e675361b193620955d2a2c51e6d720ad3b0b8cea4f13348`
  - Detector stack digest: `04a286d67a82dbd054ebcdc2c5ca485881534a0674a1241abcc64c4421797e9e`
- Missing shared digest-contract artifact that declares canonical digest basis across subsystems.

## Remaining Scientific Risks
- Synthetic rehearsal confirms plumbing but not behavioral outcomes under real training/eval noise.
- Weight-induced drift magnitude could trigger false concern without explicit per-cell tolerance policy.
- Delta-based detector rules remain baseline-sensitive; baseline governance policy is still required for live probes.

## Readiness Recommendation
- `NOT_READY`
- Reason: resolve geometry-context digest contract divergence before single-cell probe so lineage reconstruction remains deterministic across all emitted artifacts.
