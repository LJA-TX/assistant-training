# Phase H Controlled Experiment Design

## Executive Summary

Phase H recommends a bounded internal-first proving experiment, not Dataset v1.1 implementation.

The design uses:

- a fresh bounded control repro on the i3 recovery corpus,
- a commitment-only patch,
- a diversity-only patch,
- and conditional schema or methodology follow-ups only if the first screen does not settle the question.

This is the smallest realistic experiment that can distinguish whether the next useful internal move is broader diversity, stronger tool-call commitment, cleaner schema realization, a config-only methodology change, or some combination.

## Competing Hypotheses

### Hypothesis A

Dataset diversity remains the dominant bottleneck.

### Hypothesis B

Tool-call commitment remains the dominant bottleneck.

### Hypothesis C

Schema realization remains the dominant bottleneck.

### Hypothesis D

Training methodology remains the dominant bottleneck.

### Hypothesis E

No single factor dominates; the remaining deficit is combined.

## Proposed Experiment

### Control

Train a fresh bounded control repro on exact i3 recovery dataset bytes using the proven microprobe execution shape.

### First-screen treatments

1. `commitment-only` bounded patch
2. `diversity-only` bounded patch

### Conditional treatments

1. `schema-only` bounded patch if commitment wins or residual invalid-schema remains dominant
2. `methodology-only` probe if content probes remain inconclusive

### Boundaries

- internal data only
- fixed row counts
- fixed non-tool slices
- fixed eval contract
- fixed scoring contract
- no hidden retries

## Why This Experiment

This design matches the current evidence.

Phase G already showed:

- collapse repair matters,
- diversity repair alone is not obviously enough,
- commitment failure dominates residual non-exact rows,
- schema drift is still significant,
- and methodology cannot be ruled out without a config-only test.

A full Dataset v1.1 build would spend far more effort before answering that question.

## Expected Learning Value

The experiment is expected to answer:

1. whether more internal diversity still unlocks meaningful unseen-tool lift,
2. whether the main missing behavior is entering tool-call mode under weaker anchors,
3. whether schema-specific correction is the real blocker after commitment improves,
4. whether content changes matter more than config-only changes,
5. and when internal-only iteration should stop.

## Risks

1. Commitment and schema are partially coupled, so perfect isolation is not possible.
2. Internal source depth is still thin, so diversity-only gains may saturate quickly.
3. Safety regressions can masquerade as tool gains, especially on no-call behavior.
4. Methodology-only testing can sprawl unless limited to existing supported trainer surfaces.

These risks are controlled through bounded patch sizes, frozen contracts, kill metrics, and a maximum run count.

## Stop Rules

The experiment stops when:

1. a leading hypothesis is established,
2. a combined-bottleneck determination is established,
3. or internal-only runs fail to produce informative lift and the external-first stop rule triggers.

It also stops immediately for contamination, wrapper leakage, contract drift, repeated safety regressions, or post-hoc reinterpretation pressure.

## Recommended Next Action

Execute `H1: internal proving experiment only`.

That means:

1. run the fresh control repro,
2. run commitment-only and diversity-only first,
3. branch into schema or methodology only if the first screen leaves ambiguity,
4. and stop internal-only iteration if the matrix remains weak.

## Confidence Assessment

**Medium**

The design is strong enough to be useful because:

- it is narrow,
- it is executable locally,
- it directly targets the unresolved causal question,
- and it prevents the project from drifting prematurely into Dataset v1.1 work.

Confidence is not high because internal depth is still limited and some interaction between commitment and schema is unavoidable.

## Sources Used

- `docs/Phase_H_Work_packages.md`
- `docs/phase_g/INTERNAL_SIGNAL_INVENTORY.md`
- `docs/phase_g/RECOVERY_CORPUS_ANALYSIS.md`
- `docs/phase_g/FAILURE_ATTRIBUTION_ANALYSIS.md`
- `docs/phase_g/COUNTERFACTUAL_ASSESSMENT.md`
- `docs/phase_g/INTERNAL_VS_EXTERNAL_STRATEGY_ASSESSMENT.md`
- `configs/lora/stage_b_llama31_8b_base_v1_i10r_microprobe.config.json`
- `manifests/reports/stage_b_v1_i10r_microprobe_canonical_eval_summary.json`
- `manifests/reports/stage_b_v1_i10r_counterbalanced_probe_canonical_eval_summary.json`
- `manifests/reports/stage_b_v1_i10r_nocall_probe_canonical_eval_summary.json`
