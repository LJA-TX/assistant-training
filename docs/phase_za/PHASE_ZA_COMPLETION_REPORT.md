# Phase ZA Completion Report

## Executive Summary

Phase ZA executed the Treatment A arm of the Phase Y preservation ablation and completed the second governed execution point in the anchor-concentration sweep.

The Treatment A run is scientifically valid and contamination-clean, but it is **Do Not Promote**. Compared with the Control arm, it shows a positive but modest move in the desired direction.

## Dataset And Run Summary

| Item | Value |
|---|---|
| Arm | Treatment A |
| Train rows | `2160` |
| Val rows | `240` |
| Anchor rows | `819` |
| Long-tail rows | `574` |
| Tool-positive rows | `1393` |
| Safety rows | `767` |
| Tool families represented | `26` |

## Execution Summary

| Item | Value |
|---|---|
| Config | [configs/lora/stage_b_llama31_8b_base_v1_phase_za_treatment_a.config.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_za_treatment_a.config.json) |
| Manifest | [manifests/runs/stage_b_llama31_8b_base_v1_phase_za_treatment_a.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_za_treatment_a.run_manifest.json) |
| Training summary | [artifacts/stage_b_llama31_8b_base_v1_phase_za_treatment_a/training_summary.json](/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_za_treatment_a/training_summary.json) |
| Canonical eval summary | [evals/runs/phase_za_treatment_a_eval_20260613T005031Z/summary.json](/opt/ai-stack/assistant-training/evals/runs/phase_za_treatment_a_eval_20260613T005031Z/summary.json) |
| Comparison rows | [evals/runs/phase_za_treatment_a_eval_20260613T005031Z/comparison_rows.jsonl](/opt/ai-stack/assistant-training/evals/runs/phase_za_treatment_a_eval_20260613T005031Z/comparison_rows.jsonl) |

## Validation Results

- Preflight: PASS
- Training: PASS
- Canonical evaluation: PASS
- Contamination: PASS
- `git diff --check`: PASS

## Metric Summary

| Metric | Value |
|---|---:|
| exact JSON validity | `0.07` |
| tool-name accuracy | `0.21428571428571427` |
| argument accuracy | `0.15` |
| wrapper leakage | `0.005` |
| no-call correctness | `0.7333333333333333` |
| adversarial no-call correctness | `0.25` |

## Trajectory Assessment

Treatment A improves on Control in the core capability metrics and on no-call calibration. The gain is small but measurable.

The run is therefore useful evidence for a positive anchor-concentration response, not evidence that the ablation is already resolved.

## Readiness Determination

Treatment A is a valid ablation result but not promotable.

The next phase should continue the sweep to Treatment B.

## Residual Risks

- The improvement is modest, so the next arm could still flatten or reverse the trend.
- Wrapper leakage appeared once, which needs continued watching.
- The result is still far below the H1/H2 floor, so there is no basis for early promotion.

## Recommended Next Phase

Proceed to Phase ZA Treatment B.
