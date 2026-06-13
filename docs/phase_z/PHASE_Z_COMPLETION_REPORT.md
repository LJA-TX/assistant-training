# Phase Z Completion Report

## Executive Summary

Phase Z executed the control arm of the Phase Y preservation ablation and completed the first governed execution gate for the ablation sequence.

The control run is scientifically valid and contamination-clean, but it is **Do Not Promote**. It improves over Phase Q on capability, yet remains far below H1/H2 and loses adversarial no-call safety.

## Dataset And Run Summary

| Item | Value |
|---|---|
| Arm | Control |
| Train rows | `2160` |
| Val rows | `240` |
| Anchor rows | `726` |
| Long-tail rows | `667` |
| Tool-positive rows | `1393` |
| Safety rows | `767` |
| Tool families represented | `26` |

## Execution Summary

| Item | Value |
|---|---|
| Config | [configs/lora/stage_b_llama31_8b_base_v1_phase_z_control.config.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_z_control.config.json) |
| Manifest | [manifests/runs/stage_b_llama31_8b_base_v1_phase_z_control.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_z_control.run_manifest.json) |
| Training summary | [artifacts/stage_b_llama31_8b_base_v1_phase_z_control/training_summary.json](/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_z_control/training_summary.json) |
| Canonical eval summary | [evals/runs/phase_z_control_eval_20260613T002335Z/summary.json](/opt/ai-stack/assistant-training/evals/runs/phase_z_control_eval_20260613T002335Z/summary.json) |
| Comparison rows | [evals/runs/phase_z_control_eval_20260613T002335Z/comparison_rows.jsonl](/opt/ai-stack/assistant-training/evals/runs/phase_z_control_eval_20260613T002335Z/comparison_rows.jsonl) |

## Validation Results

- Preflight: PASS
- Training: PASS
- Canonical evaluation: PASS
- Contamination: PASS
- `git diff --check`: PASS

## Metric Summary

| Metric | Value |
|---|---:|
| exact JSON validity | `0.055` |
| tool-name accuracy | `0.2` |
| argument accuracy | `0.1357142857142857` |
| wrapper leakage | `0.0` |
| no-call correctness | `0.6666666666666666` |
| adversarial no-call correctness | `0.0` |

## Readiness Determination

The control arm is a valid ablation result but not promotable.

The run does not recover H1/H2-level tool-call capability and it regresses adversarial no-call safety to zero.

## Residual Risks

- Treatment A may or may not improve capability enough to matter.
- The safety collapse on the adversarial no-call surface suggests the lower anchor concentration region is not yet stable.
- The result is still useful because it preserves causal interpretability.

## Recommended Next Phase

Proceed to Phase Z Treatment A under the same governed framework.

The control arm establishes the baseline point for the ablation curve; the next step is to test the next anchor-concentration level rather than stopping.
