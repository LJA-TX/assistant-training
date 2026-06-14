# Topology Ablation Design

## Objective

Isolate whether patch-local replacement topology causally affects capability recovery when all other known signals are fixed.

## Fixed Invariants

Hold constant across every arm:

- `2160` training rows and `240` validation rows,
- the frozen Stage B recovery scaffold,
- the exact-tool-request cue on every tool-positive row,
- the canonical single-call `tool_calls` envelope,
- the safety block and validation surfaces,
- the anchor-heavy positive composition,
- the tool-positive density,
- and the canonical evaluation contract.

## Topology Axis

Vary only the geometry of the fixed positive patch:

- patch locality,
- replacement distribution,
- intervention footprint.

Use the same positive-row budget and the same anchor-heavy mix in every arm.

## Proposed Arms

The smallest useful sweep is one control plus three treatment levels.

| Arm | Topology | Footprint intent | Interpretation target |
|---|---|---|---|
| Control | Compact local patch | Single bounded patch-local span, H1/H2-like footprint | Baseline for topology comparison |
| Treatment A | Split patch | Two disjoint clusters, same total patch budget | Tests mild loss of locality |
| Treatment B | Multi-cluster patch | Four disjoint clusters, same total patch budget | Tests stronger dispersion |
| Treatment C | Dispersed patch | Evenly interleaved across the scaffold | Tests maximum loss of locality |

## Why This Is The Right Geometry

H1/H2 already showed that the successful footprint was small:

- `100` patch rows,
- about `4.63%` of the training corpus,
- spanning only about `20%` of the corpus order.

That makes a compact local control the correct baseline, and increasing dispersion the natural experimental perturbation.

## Construction Rule

All four arms should be built from the same fixed positive composition.

Only the row placement changes:

- no anchor rebalancing,
- no cue mutation,
- no safety-block rewrite,
- no validation-surface changes.

## Expected Readout

If topology matters, the compact local control should outperform the more dispersed arms on at least the exact-call metrics:

- exact JSON validity,
- tool-name accuracy,
- argument accuracy.

If the arms are flat, topology is not the remaining causal factor.

If the arms show a non-monotonic or safety-confounded curve, topology is contributory but not sufficient.
