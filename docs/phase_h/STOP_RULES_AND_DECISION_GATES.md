# Stop Rules And Decision Gates

## Purpose

These rules exist to prevent:

- endless internal-only iteration,
- uncontrolled dataset expansion,
- ambiguous "some gain happened" storytelling,
- and post-hoc reinterpretation.

## Global Caps

1. Maximum fresh control runs: `1`
2. Maximum first-screen treatment runs: `2`
3. Maximum schema follow-up runs: `1`
4. Maximum methodology follow-up runs: `1`
5. Maximum total training runs in the preferred set: `5`
6. Maximum retries per run: `1`, and only for infrastructure failure before metrics exist

No metric-driven reruns are allowed.

## Pre-Execution Stop Rules

Stop before training if any of the following is true:

1. canonical eval manifest, decode defaults, or scoring semantics differ from Phase E
2. bounded dataset variants cannot be built inside the declared patch budget
3. heldout or tool-holdout contamination checks fail
4. the planned methodology probe requires trainer redesign rather than using an existing supported surface
5. repository state shows unrelated runtime, evaluator, or governance modifications that would confound the experiment

## Run-Level Stop Rules

After each run:

1. score the run against kill metrics immediately
2. if a kill metric trips, document the run as report-only evidence
3. do not continue to another internal-only run if two runs have already tripped kill metrics

This avoids turning internal experimentation into open-ended tradeoff chasing.

## Decision Gate After `H0`

Proceed only if:

1. `H0` executes cleanly,
2. all frozen surfaces match the declared control,
3. and the eval outputs are internally consistent.

If `H0` is not trustworthy, stop and escalate.

## Decision Gate After First Screen (`H2` then `H1`)

After the first-screen pair:

### Stop in favor of diversity

Stop and favor `A` if:

- `H1` clears the diversity thresholds,
- and `H2` does not clear the commitment thresholds.

### Stop in favor of commitment

Stop and favor `B` if:

- `H2` clears the commitment thresholds,
- and `H1` does not clearly beat it on tool-holdout metrics.

### Continue to schema split

Run `H3` only if:

1. `H2` wins the first screen or ties the first screen,
2. and invalid-schema remains a major share of residual failures,
3. and kill metrics are still clean enough to justify one more content run.

### Continue to methodology-only probe

Run `H4` only if:

1. `H1` and `H2` are both inconclusive,
2. or content probes improve metrics but still leave methodology plausibly dominant,
3. and the methodology probe can be executed on frozen dataset bytes without redesign.

## External-First Stop Rule

Terminate internal-only continuation and hand off to external-first work if any of the following occurs:

1. none of the internal content probes produce nonzero tool-holdout exact-valid when the control remains zero,
2. none of the internal content probes beat control by at least `5` points on tool-expected exact-valid,
3. schema and commitment probes both improve only marginally inside the inconclusive band,
4. or safety regressions recur while the main tool metrics remain weak.

This is the main anti-loop rule.

## No Reinterpretation Rule

The following are prohibited after results land:

1. changing the hypothesis definitions,
2. swapping primary and diagnostic metrics to salvage a weak run,
3. loosening kill metrics,
4. inventing new "qualitative wins" outside the declared matrix.

If the declared rules do not yield a winner, the result is inconclusive by definition.

## Completion Gate

The experiment is complete when one of these is true:

1. a hypothesis winner is declared under the Phase H thresholds,
2. a combined-bottleneck determination is declared,
3. or the external-first stop rule is triggered and documented.

Completion does not require all preferred runs if the matrix already reached a decisive gate earlier.

## Sources Used

- `docs/Phase_H_Work_packages.md`
- `docs/phase_g/INTERNAL_VS_EXTERNAL_STRATEGY_ASSESSMENT.md`
- `docs/phase_g/FAILURE_ATTRIBUTION_ANALYSIS.md`
- `manifests/reports/stage_b_v1_geometry_risk_assessment.json`
