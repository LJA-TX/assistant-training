# Phase ZB Completion Report

## Executive Summary

Phase ZB completed the Treatment B governed execution and produced a valid, contamination-clean result.

The run is **Do Not Promote**. It preserves the safety gains seen in the preservation sweep, but it does not recover H1/H2-style tool-call capability and it does not improve over Treatment A.

## Dataset And Run Summary

| Item | Value |
|---|---|
| Arm | Treatment B |
| Train rows | `2160` |
| Val rows | `240` |
| Tool families represented | `26` |
| Training runtime | `166.1638s` |
| Training loss | `0.6634314899091367` |
| Internal eval loss | `0.5361461043357849` |

## Execution Summary

| Item | Value |
|---|---|
| Config | [configs/lora/stage_b_llama31_8b_base_v1_phase_zb_treatment_b.config.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_zb_treatment_b.config.json) |
| Manifest | [manifests/runs/stage_b_llama31_8b_base_v1_phase_zb_treatment_b.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_zb_treatment_b.run_manifest.json) |
| Training summary | [artifacts/stage_b_llama31_8b_base_v1_phase_zb_treatment_b/training_summary.json](/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_zb_treatment_b/training_summary.json) |

## Validation Results

- Preflight: PASS
- Training: PASS
- Canonical evaluation: PASS
- Contamination: PASS
- `git diff --check`: PASS

## Key Findings

Treatment B is better than Control, but only marginally, and it is flat versus Treatment A.

| Metric | Control | Treatment A | Treatment B |
|---|---:|---:|---:|
| exact JSON validity | `0.055` | `0.07` | `0.07` |
| tool-name accuracy | `0.2` | `0.21428571428571427` | `0.21428571428571427` |
| argument accuracy | `0.1357142857142857` | `0.15` | `0.15` |
| wrapper leakage | `0.0` | `0.005` | `0.005` |
| no-call correctness | `0.6666666666666666` | `0.7333333333333333` | `0.7333333333333333` |
| adversarial no-call correctness | `0.0` | `0.25` | `0.25` |

## Combined Assessment

Treatment B confirms that the sweep found a modest improvement over Control, but the improvement saturates at Treatment A.

The run does not recover the H1/H2 capability regime:

- H1 exact JSON validity: `0.44`
- H2 exact JSON validity: `0.48`
- Treatment B exact JSON validity: `0.07`

The failure profile remains dominated by envelope drift and substitution failures rather than clean exact tool calls.

## Contamination Results

Contamination remains clean for the constructed dataset and the governed run stayed within the frozen validation surface.

## Readiness Determination

Treatment B is a valid ablation result, but it is not promotable.

## Risks

- The trajectory flattened at Treatment B, so the remaining arm may still be needed to resolve the concentration curve.
- Wrapper leakage is still nonzero.
- Capability remains far below the H1/H2 floor.

## Recommended Next Phase

Proceed to Phase ZC / Treatment C.
