# Phase W Recommendation

## Recommended Execution Plan

Run the anchor-concentration ablation as a low-to-high bracket:

1. Control at `0.5212` core anchor share.
2. Treatment A at `0.5879`.
3. Treatment B at `0.6546`.
4. Treatment C at `0.7258`.

## Why This Plan

This is the smallest design that can locate the threshold region while keeping the experiment controlled.

It is higher value than a full-corpus redesign because it:

- changes one variable only,
- preserves the exact cue and scaffold,
- preserves the canonical evaluation contract,
- and gives a threshold estimate instead of a one-off outcome.

## Why Not A Full Redesign

A full redesign would confound the very factors Phase V identified:

- anchor concentration,
- prompt-regime breadth,
- and control-surface preservation.

That would make it impossible to tell whether a success came from anchor mass or from a new prompt mixture.

## Early-Stop Logic

Use adaptive stopping:

- If the control already reaches H1 floor metrics, stop after one confirmatory replicate.
- If Treatment A reaches H1 floor, stop after a confirmatory replicate at the same level.
- If Treatment B reaches H1 floor but A does not, the threshold lies between A and B.
- If only Treatment C reaches H2 floor, the threshold lies between B and C.
- If no arm reaches H1 floor, anchor concentration alone is not enough in the tested range.

## Expected Information Gain

This plan can answer:

- whether anchor concentration is the remaining bottleneck,
- whether the required concentration is closer to v1.2, H1, or H2,
- and whether a future design should aim for H1-like or H2-like anchor mass.

That is more informative than another full-corpus redesign because it preserves causal interpretability.

## Confidence

**Medium-high**

The evidence strongly supports anchor concentration as the last unresolved variable, but the exact threshold still needs an execution result.
