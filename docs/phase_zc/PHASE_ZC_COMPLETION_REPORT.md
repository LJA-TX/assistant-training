# Phase ZC Completion Report

## Executive Summary

Phase ZC completed the final arm of the Phase Y preservation ablation.

The result is scientifically valid and contamination-clean, but it is **Do Not Promote**. Treatment C improves exact-call realization relative to the earlier plateau, yet it does not recover the H1/H2 capability regime and it breaks adversarial no-call safety.

## Dataset And Run Summary

| Item | Value |
|---|---|
| Arm | Treatment C |
| Train rows | `2160` |
| Val rows | `240` |
| Tool families represented | `26` |
| Training runtime | `167.0348s` |
| Training loss | `0.6584662331475152` |
| Internal eval loss | `0.5838639140129089` |

## Execution Summary

| Item | Value |
|---|---|
| Config | [configs/lora/stage_b_llama31_8b_base_v1_phase_zc_treatment_c.config.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_zc_treatment_c.config.json) |
| Manifest | [manifests/runs/stage_b_llama31_8b_base_v1_phase_zc_treatment_c.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_zc_treatment_c.run_manifest.json) |
| Training summary | [artifacts/stage_b_llama31_8b_base_v1_phase_zc_treatment_c/training_summary.json](/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_zc_treatment_c/training_summary.json) |
| Canonical eval summary | [evals/runs/phase_zc_treatment_c_eval_20260613T212800Z/summary.json](/opt/ai-stack/assistant-training/evals/runs/phase_zc_treatment_c_eval_20260613T212800Z/summary.json) |

## Validation Results

- Preflight: PASS
- Training: PASS
- Canonical evaluation: PASS
- Contamination: PASS
- `git diff --check`: PASS

## Key Findings

Treatment C is the strongest capability arm in the sweep, but it is still not close to the H1/H2 floor.

| Metric | Control | Treatment A | Treatment B | Treatment C |
|---|---:|---:|---:|---:|
| exact JSON validity | `0.055` | `0.07` | `0.07` | `0.085` |
| tool-name accuracy | `0.2` | `0.21428571428571427` | `0.21428571428571427` | `0.2857142857142857` |
| argument accuracy | `0.1357142857142857` | `0.15` | `0.15` | `0.18571428571428572` |
| wrapper leakage | `0.0` | `0.005` | `0.005` | `0.0` |
| no-call correctness | `0.6666666666666666` | `0.7333333333333333` | `0.7333333333333333` | `0.6666666666666666` |
| adversarial no-call correctness | `0.0` | `0.25` | `0.25` | `0.0` |

## Combined Assessment

The sweep is best described as:

- a modest gain from Control to Treatment A,
- a plateau from Treatment A to Treatment B,
- and a renewed capability gain at Treatment C,
- with a safety collapse on the adversarial no-call surface at the highest anchor concentration.

The final arm therefore supports a mixed-response model, not a single monotonic response model.

## Comparison Against H1/H2

H1 and H2 remain far ahead on the exact-call metrics:

- H1 exact JSON validity: `0.44`
- H1 tool-name accuracy: `0.7142857142857143`
- H1 argument accuracy: `0.6285714285714286`
- H2 exact JSON validity: `0.48`
- H2 tool-name accuracy: `0.7714285714285715`
- H2 argument accuracy: `0.6928571428571428`

Treatment C does not close that gap.

## Contamination Results

Contamination remains clean for the constructed dataset and the governed run stayed within the frozen validation surface.

## Readiness Determination

Treatment C is a valid ablation result, but it is not promotable.

## Risks

- The final arm recovers some capability while collapsing adversarial safety.
- Anchor concentration alone does not produce the H1/H2 regime.
- The sweep ends with a mixed response, so later interpretation must account for confounding factors beyond density.

## Recommended Next Action

Close the ablation and move back to analysis rather than execution.

The evidence now supports a multi-factor explanation, not a single anchor-concentration explanation.

## Recommended Next Phase

Conduct a follow-on investigation of the remaining preserved variables that were not isolated by the anchor sweep.
