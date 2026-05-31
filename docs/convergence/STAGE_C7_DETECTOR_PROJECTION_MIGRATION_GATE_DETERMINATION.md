# Stage C7 Detector Projection Migration Gate Determination

## Scope

This determination records the Stage C7 migration safety-gate outcome for detector projection migration.

This is a determination artifact only. No detector migration or threshold-profile migration was executed.

## Determination

Gate classification: **partially ready**.

Authoritative detector projection migration: **not approved**.

## Decision Basis

### Ready Conditions Confirmed

1. existing detector and threshold-profile surfaces are fully inventoried.
2. C6 projection preparation retains all three independent state axes.
3. C6 artifacts retain provenance, denominator provenance, scoring evidence, and validation visibility.
4. non-inference and non-reconstruction guardrails remain explicit and currently clear.

### Blocking Conditions

1. unresolved mapping for `no_call_correctness_adversarial` from Stage C emitted surfaces.
2. unresolved semantic equivalence for `no_anchor_exact_valid_share` versus Stage C B2 emitted concepts.
3. no authoritative baseline-delta comparability gate for detector projection migration path.
4. no compatibility test harness yet for preserving existing detector-output consumer expectations.

## Migration Authorization Result

Allowed now:

- bounded, non-authoritative adapter development,
- mapping proofs for unambiguous metrics,
- explicit noncomputable handling for unresolved metrics,
- migration-compatibility test harness development.

Not allowed now:

- authoritative detector projection migration,
- threshold-profile migration activation,
- replacement of current detector outputs in active manifest-linked flows.

## Smallest Safe Next Slice

1. Implement non-authoritative metric projection adapter from Stage C artifacts to detector-candidate inputs.
2. Emit per-metric mapping evidence with explicit source artifact paths and denominator provenance.
3. Emit unresolved metrics as explicit noncomputable with blocking reason codes.
4. Add compatibility tests for schema continuity, baseline-delta blocking behavior, and axis-independence preservation.
5. Re-run migration gate after these conditions pass.

## Final Result

Stage C7 gate is complete. Detector migration remains gated pending closure of documented blockers.
