# Phase ZB Treatment B Execution Review

## Executive Summary

Phase ZB executed the Treatment B arm of the Phase Y preservation ablation and completed the third governed execution point in the anchor-concentration sweep.

The run is scientifically valid, contamination-clean, and operationally successful. It is **Do Not Promote**.

Treatment B improves over the Control arm, but it does not materially improve over Treatment A. The top-line capability metrics plateau at the same level as Phase ZA, and the run remains far below the H1/H2 capability floor.

## Execution Summary

| Item | Value |
|---|---|
| Arm | Treatment B |
| Train rows | `2160` |
| Val rows | `240` |
| Tool families represented | `26` |
| Config | [configs/lora/stage_b_llama31_8b_base_v1_phase_zb_treatment_b.config.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_zb_treatment_b.config.json) |
| Manifest | [manifests/runs/stage_b_llama31_8b_base_v1_phase_zb_treatment_b.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_zb_treatment_b.run_manifest.json) |
| Training summary | [artifacts/stage_b_llama31_8b_base_v1_phase_zb_treatment_b/training_summary.json](/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_zb_treatment_b/training_summary.json) |

## Validation Results

- Preflight: PASS
- Training: PASS
- Canonical evaluation: PASS
- Contamination: PASS
- `git diff --check`: PASS

## Metric Summary

| Metric | Treatment B |
|---|---:|
| exact JSON validity | `0.07` |
| tool-name accuracy | `0.21428571428571427` |
| argument accuracy | `0.15` |
| wrapper leakage | `0.005` |
| no-call correctness | `0.7333333333333333` |
| adversarial no-call correctness | `0.25` |

## Baseline Comparison

Relative to Control, Treatment B shows a small but real capability lift:

- exact JSON validity: `+0.015`
- tool-name accuracy: `+0.014285714285714285`
- argument accuracy: `+0.01428571428571429`
- no-call correctness: `+0.06666666666666665`
- adversarial no-call correctness: `+0.25`

Relative to Treatment A, Treatment B is flat on the published metrics:

- exact JSON validity: unchanged
- tool-name accuracy: unchanged
- argument accuracy: unchanged
- wrapper leakage: unchanged
- no-call correctness: unchanged
- adversarial no-call correctness: unchanged

Relative to H1/H2, Treatment B remains far below the tool-call floor:

- H1 exact JSON validity: `0.44`
- H2 exact JSON validity: `0.48`
- Treatment B exact JSON validity: `0.07`

## Failure Profile

Treatment B remains dominated by envelope and realization failures rather than clean exact tool calls.

| Failure category | Count |
|---|---:|
| direct-answer substitution | `34` |
| scalar substitution | `39` |
| malformed partial JSON | `4` |
| near-canonical wrapper or envelope drift | `49` |

The failure mix is the same plateau observed in Treatment A, which means the higher anchor concentration in Treatment B did not move the model into the H1/H2 regime.

## Boundary Confirmation

- No dataset contents were modified during execution.
- No evaluator logic changed.
- No scoring logic changed.
- No governance or threshold changes were made.
- The run stayed within the approved Phase L geometry.
