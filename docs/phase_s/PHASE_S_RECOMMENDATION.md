# Phase S Recommendation

## Recommendation

Authorize the **60-row schema-repair micro-patch** as the first experiment.

If only one experiment is allowed, this is the one with the highest information value because it directly targets the observed failure surface:

- exact JSON validity,
- `tool_calls` envelope realization,
- and wrapper drift.

## Why Not Jump To A Full Redesign

A full redesign is a remediation candidate, not the smallest diagnostic experiment.

It would change too many variables at once and would not isolate the schema-realization hypothesis.

## Why Not Start With Anchor-Only Or Prompt-Only Changes

Those are useful ablations, but they are secondary.

They answer narrower questions:

- anchor-only asks whether concentration alone is enough;
- prompt-regime asks whether wording alone is enough.

Neither is as direct a test of the schema hypothesis as the schema-repair patch.

## Recommended Next Phase

The next execution phase should be a controlled schema-repair run on the frozen Stage B scaffold.

Recommended order:

1. schema-repair micro-patch,
2. anchor-only ablation if needed,
3. prompt-regime ablation if needed,
4. only then consider broader dataset redesign.

## Confidence

Confidence is high that the schema patch is the best first test.

Confidence is moderate that 60 rows is enough to produce a decisive directional signal.

Confidence is low that a full redesign would improve attribution quality for this question.

