# Phase ZC Treatment C Execution Review

## Executive Summary

Phase ZC executed the Treatment C arm of the Phase Y preservation ablation and completed the final governed execution point in the anchor-concentration sweep.

The run is scientifically valid, contamination-clean, and operationally successful. It is **Do Not Promote**.

Treatment C improves over Control and over the Treatment A/B plateau on the exact-call metrics, but it still does not recover H1/H2-level capability and it destroys the adversarial no-call surface relative to Phase ZB.

## Execution Summary

| Item | Value |
|---|---|
| Arm | Treatment C |
| Train rows | `2160` |
| Val rows | `240` |
| Tool families represented | `26` |
| Config | [configs/lora/stage_b_llama31_8b_base_v1_phase_zc_treatment_c.config.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_zc_treatment_c.config.json) |
| Manifest | [manifests/runs/stage_b_llama31_8b_base_v1_phase_zc_treatment_c.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_zc_treatment_c.run_manifest.json) |
| Training summary | [artifacts/stage_b_llama31_8b_base_v1_phase_zc_treatment_c/training_summary.json](/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_zc_treatment_c/training_summary.json) |
| Canonical eval summary | [evals/runs/phase_zc_treatment_c_eval_20260613T212800Z/summary.json](/opt/ai-stack/assistant-training/evals/runs/phase_zc_treatment_c_eval_20260613T212800Z/summary.json) |
| Comparison rows | [evals/runs/phase_zc_treatment_c_eval_20260613T212800Z/comparison_rows.jsonl](/opt/ai-stack/assistant-training/evals/runs/phase_zc_treatment_c_eval_20260613T212800Z/comparison_rows.jsonl) |

## Validation Results

- Preflight: PASS
- Training: PASS
- Canonical evaluation: PASS
- Contamination: PASS
- `git diff --check`: PASS

## Metric Summary

| Metric | Treatment C |
|---|---:|
| exact JSON validity | `0.085` |
| tool-name accuracy | `0.2857142857142857` |
| argument accuracy | `0.18571428571428572` |
| wrapper leakage | `0.0` |
| no-call correctness | `0.6666666666666666` |
| adversarial no-call correctness | `0.0` |

## Baseline Comparison

Relative to Control, Treatment C shows the strongest capability lift in the sweep:

- exact JSON validity: `+0.03`
- tool-name accuracy: `+0.08571428571428572`
- argument accuracy: `+0.05`

Relative to Treatment A and Treatment B, Treatment C breaks the plateau:

- exact JSON validity: `+0.015`
- tool-name accuracy: `+0.07142857142857142`
- argument accuracy: `+0.03571428571428572`

The safety surfaces do not hold the same shape:

- no-call correctness returns to the Control level
- adversarial no-call correctness falls back to `0.0`
- wrapper leakage returns to `0.0`

Relative to H1/H2, Treatment C is still far below the H1/H2 capability floor:

- H1 exact JSON validity: `0.44`
- H2 exact JSON validity: `0.48`
- Treatment C exact JSON validity: `0.085`

## Failure Profile

Treatment C remains dominated by envelope and realization failures, but the balance shifts toward substitution and drift rather than a clean exact-call regime.

| Failure category | Count |
|---|---:|
| direct-answer substitution | `30` |
| scalar substitution | `31` |
| malformed partial JSON | `4` |
| near-canonical wrapper or envelope drift | `58` |

The sweep therefore ends with a mixed result: higher anchor concentration helps exact-call realization, but it does not preserve the safety gains seen in earlier arms and it does not recover H1/H2-level competence.

## Boundary Confirmation

- No dataset contents were modified during execution.
- No evaluator logic changed.
- No scoring logic changed.
- No governance or threshold changes were made.
- The run stayed within the approved Phase L geometry.
