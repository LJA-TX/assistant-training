# Phase W Attribution Framework

## Goal

Attribute any change in capability to anchor concentration only, without confounding cue or scaffold changes.

## Variable Status

| Factor | Varies in Phase W? | Attribution role |
|---|---|---|
| Anchor concentration | Yes | primary causal variable |
| Exact-tool-request cue | No | controlled constant |
| Frozen scaffold | No | controlled constant |
| Patch-local intervention shape | No | controlled constant |
| Canonical `tool_calls` contract | No | controlled constant |
| Safety block | No | controlled constant |

## Attribution Rules

### Anchor concentration effects

Supported if the following hold:

- the fixed factors remain invariant,
- exact JSON, tool-name accuracy, and argument accuracy improve with anchor concentration,
- and the best-performing arm is the highest-anchor arm or a clear threshold between two adjacent arms.

### Cue effects

The experiment does not vary cue content, so cue effects are not estimated directly.

Cue effects are controlled out by design:

- every arm uses the same exact-tool-request cue,
- so any between-arm difference cannot be caused by cue variation.

Cue relevance remains visible only through external comparison to earlier phases:

- H1/H2 preserved the cue and succeeded,
- v1.1/v1.2 changed the cue regime and failed,
- Phase W holds the cue fixed to isolate anchor mass.

### Scaffold effects

The experiment does not vary scaffold content, so scaffold effects are also not estimated directly.

Scaffold relevance is bounded by invariant control:

- the same train/val shell is used in every arm,
- the same non-tool slices remain frozen,
- and the same canonical evaluation contract is used.

If all arms fail, scaffold insufficiency or a second unmodeled factor remains the likely explanation.

## Decision Logic

### Supported

Anchor concentration is supported as the dominant unresolved variable if:

- metrics rise monotonically with anchor share, or
- a sharp threshold appears between adjacent anchor levels.

### Partially Supported

Anchor concentration is partially supported if:

- there is some lift, but not enough to reach H1/H2 floors,
- and the response is not monotonic or not decisive.

### Not Supported

Anchor concentration is not supported if:

- all arms behave similarly despite different anchor shares,
- or safety/canonical contract drift invalidates the comparison.

## Metric Set

Primary:

- exact JSON validity
- tool-name accuracy
- argument accuracy
- tool-holdout exact-valid
- heldout-validation exact-valid

Safety:

- wrapper leakage
- no-call correctness
- adversarial no-call correctness
- invalid JSON

Interpretation:

- Capability must improve without breaking the safety contract.
- A safe but capability-dead arm is not sufficient.

## Stop Conditions For Attribution

Stop and treat the run as invalid for attribution if any fixed factor drifts:

- contamination overlap > 0
- wrapper leakage > 0.0
- no-call correctness < 1.0
- adversarial no-call correctness < 1.0
- aggregate invalid JSON > 0.30
- canonical eval manifest drift
- decode-default drift
- scoring-semantic drift

## Why This Distinguishes The Variables

The experiment does not estimate cue or scaffold as causal variables inside Phase W. Instead, it keeps them fixed so they cannot explain any within-experiment difference.

That is the cleanest way to distinguish anchor concentration from the other factors without changing multiple variables at once.
