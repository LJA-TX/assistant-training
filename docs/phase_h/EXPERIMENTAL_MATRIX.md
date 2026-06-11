# Experimental Matrix

## Design Shape

Phase H uses a staged matrix:

- a fresh bounded control run,
- a first-screen pair that tests diversity versus commitment,
- a conditional schema probe,
- and an optional methodology-only probe if content changes do not settle the question.

This is smaller and cleaner than a full fixed grid while still allowing all hypotheses to be distinguished.

## Run Definitions

| Run ID | Type | Dataset variant | Training variant | Control relationship | Expected learning value |
|---|---|---|---|---|---|
| `H0_control_i3_micro` | control | exact i3 recovery dataset bytes | frozen microprobe config clone | baseline for all Phase I treatments | establishes a same-budget comparator on current internal recovery signal |
| `H1_diversity_patch` | treatment | bounded internal diversity patch on tool-positive rows only | same as control | compare directly to `H0` | tests Hypothesis A without confounding config changes |
| `H2_commitment_patch` | treatment | bounded commitment patch on tool-positive rows only | same as control | compare directly to `H0` | tests Hypothesis B with tool/case family held near control |
| `H3_schema_patch` | conditional treatment | bounded schema-realization patch on tool-positive rows only | same as control | compare directly to `H0` and `H2` | tests whether C explains residual failure after commitment-related movement |
| `H4_methodology_only` | optional treatment | exact `H0` dataset bytes | config-only methodology change | compare directly to `H0` | tests Hypothesis D without dataset-content changes |

## Minimum Viable Run Set

The smallest useful execution set is:

1. `H0_control_i3_micro`
2. `H2_commitment_patch`
3. `H1_diversity_patch`

This minimum set answers the first question:

Is the next most informative internal move about broader diversity or about tool-call commitment?

## Preferred Run Set

The preferred complete set is:

1. `H0_control_i3_micro`
2. `H2_commitment_patch`
3. `H1_diversity_patch`
4. `H3_schema_patch` if commitment wins or invalid-schema remains dominant
5. `H4_methodology_only` if content probes remain inconclusive or if methodology still looks plausible

## Training Variant

### Frozen microprobe config for content runs

All content runs should inherit the proven bounded microprobe shape:

- base model: `llama-3.1-8b-base`
- QLoRA topology unchanged
- loss masking unchanged
- prompt-template mode unchanged
- optimizer defaults unchanged
- `num_train_epochs = 0.2`
- canonical eval manifest unchanged

This keeps local runtime realistic and makes the comparison attributable to dataset interventions rather than topology drift.

### Methodology-only variant

Preferred:

- exact control dataset bytes,
- geometry or exposure weighting only if implemented through the existing trainer surface without redesign.

Fallback:

- exact control dataset bytes,
- simple schedule extension to `0.35` epochs with all other config fields frozen.

## Local Execution Realism

The matrix is realistic for local execution because prior bounded runs already show:

- training runtime around `170` seconds per run,
- eval runtime around `35` seconds per run,
- and stable use of the same base model / QLoRA / canonical eval path.

That means the preferred five-run set is operationally plausible if executed one run at a time with no hidden chaining.

## Interpretation Table

| Result pattern | Leading hypothesis |
|---|---|
| `H1` clearly beats `H2` on tool-holdout and tool accuracy while commitment failures move less | `A` diversity-dominant |
| `H2` clearly beats `H1` by reducing direct-answer and scalar substitutions and improving no-anchor exact-valid | `B` commitment-dominant |
| `H2` moves commitment but `H3` then produces the largest invalid-schema reduction | `C` schema-dominant |
| `H4` on frozen bytes matches or beats the content treatments | `D` methodology-dominant |
| `H1`, `H2`, and `H3` each win different metric families or none dominate cleanly | `E` combined bottleneck |

## Recommended Execution Order

1. `H0_control_i3_micro`
2. `H2_commitment_patch`
3. `H1_diversity_patch`
4. `H3_schema_patch` only if required by the first-screen result
5. `H4_methodology_only` only if required by the first-screen result

This order spends the cheapest and highest-probability diagnostic budget first.

## Sources Used

- `docs/Phase_H_Work_packages.md`
- `docs/phase_g/FAILURE_ATTRIBUTION_ANALYSIS.md`
- `docs/phase_g/COUNTERFACTUAL_ASSESSMENT.md`
- `configs/lora/stage_b_llama31_8b_base_v1_i10r_microprobe.config.json`
- `manifests/reports/stage_b_v1_i10r_microprobe_training_summary.json`
- `manifests/reports/stage_b_v1_i10r_microprobe_canonical_eval_summary.json`
- `manifests/reports/stage_b_v1_i10r_counterbalanced_probe_canonical_eval_summary.json`
- `manifests/reports/stage_b_v1_i10r_nocall_probe_canonical_eval_summary.json`
