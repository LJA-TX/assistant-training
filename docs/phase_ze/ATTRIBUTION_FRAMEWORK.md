# Attribution Framework

## Goal

Attribute any measured movement to patch-local replacement topology only.

## Variables Held Constant

These are fixed by construction and should not be treated as causal candidates inside the experiment:

- frozen scaffold,
- exact-tool-request cue,
- anchor-heavy positive composition,
- tool-positive density,
- safety rows,
- validation surfaces,
- evaluation contract.

## Variable Under Test

Only this variable is allowed to change:

- patch-local replacement topology.

## Distinguishing Logic

### Topology effects

Supported if capability changes track footprint geometry while all invariants stay fixed.

Examples:

- compact local topology outperforms split or dispersed topology,
- or performance degrades as the patch becomes more dispersed.

### Cue effects

Not attributable in this experiment because the cue is fixed.

If the cue is missing or mutated, the experiment is invalid.

### Anchor effects

Not attributable in this experiment because anchor concentration is fixed.

If anchor share drifts, the experiment is invalid.

### Scaffold effects

Not attributable in this experiment because the scaffold is frozen.

If non-tool rows or validation surfaces change, the experiment is invalid.

## Inference Rule

A topology claim is supported only when:

- cue invariance passes,
- anchor invariance passes,
- scaffold invariance passes,
- and a systematic capability delta remains across topology levels.

## Readout Priority

Primary metrics:

- exact JSON validity,
- tool-name accuracy,
- argument accuracy.

Secondary safety checks:

- wrapper leakage,
- no-call correctness,
- adversarial no-call correctness.

## Interpretation Bands

- `supported`: compact topology beats more dispersed topology on the primary metrics without breaking safety.
- `contributory`: topology changes help, but the response is mixed or safety-confounded.
- `weakened`: topology changes do not explain the main delta.
- `not supported`: no meaningful difference across topology levels.

## Stop Conditions

Abort attribution if any invariant fails, because topology is no longer isolated.
