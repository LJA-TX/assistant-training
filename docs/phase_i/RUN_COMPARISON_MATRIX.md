# Phase I Run Comparison Matrix

## Status

The execution gate was opened. `H0_control_i3_micro` completed and tripped a Phase H kill metric. `H2_commitment_patch` then completed and also tripped kill metrics, which blocked `H1_diversity_patch` under the run-level stop ceiling.

## Planned Order

1. `H0_control_i3_micro`
2. `H2_commitment_patch`
3. `H1_diversity_patch`

## Comparison Table

| Run | Dataset | Patch size | Execution config | Execution manifest | Execution status | Eval metrics | Delta vs H0 | Stop-rule outcome | Notes |
|---|---|---:|---|---|---|---|---|---|---|
| `H0_control_i3_micro` | Exact `i3` recovery bytes | `0` | `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.config.json` | `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.run_manifest.json` | Completed | `exact_json_validity=0.045`, `invalid_json=0.145`, `tool_name_accuracy=0.07142857142857142`, `argument_accuracy=0.06428571428571428`, `tool_holdout_exact_valid=0.0`, `heldout_validation_exact_valid=0.09`, `no_call_correctness=0.9166666666666666`, `adversarial_no_call_correctness=0.75`, `no_anchor_exact_valid=0.0` | Control baseline | `kill metric tripped` | Valid report-only comparator; hard-stop baseline |
| `H2_commitment_patch` | `dataset_v1_0_phase_i_h2_commitment_patch_train.jsonl` | `100` | `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.config.json` | `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.run_manifest.json` | Completed | `train_runtime=159.4807s`, `train_loss=0.5947615747098569`, `eval_loss=0.4286271333694458`, `exact_json_validity=0.48`, `invalid_json=0.085`, `tool_name_accuracy=0.7714285714285715`, `argument_accuracy=0.6928571428571428`, `tool_holdout_exact_valid=0.525`, `heldout_validation_exact_valid=0.75`, `wrapper_leakage=0.005`, `no_call_correctness=0.8`, `adversarial_no_call_correctness=0.4`, `no_anchor_exact_valid=0.84375` | `exact_json_validity +0.435`, `invalid_json -0.060`, `tool_name_accuracy +0.700`, `argument_accuracy +0.629`, `tool_holdout_exact_valid +0.525`, `heldout_validation_exact_valid +0.660`, `wrapper_leakage +0.005`, `no_call_correctness -0.117`, `adversarial_no_call_correctness -0.350`, `no_anchor_exact_valid +0.844` | `kill metric tripped` | Strong commitment signal, but wrapper leakage and adversarial no-call regression block continuation |
| `H1_diversity_patch` | `dataset_v1_0_phase_i_h1_diversity_patch_train.jsonl` | `100` | `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.config.json` | `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.run_manifest.json` | Not run | n/a | n/a | Blocked by run-level stop ceiling | Not launched because H0 and H2 had both tripped kill metrics |

## Pending Metrics

The H1 metrics remain pending because the run-level stop ceiling halted the sequence after H2 completed and tripped kill metrics.

## Interim Interpretation

H2 provides a strong commitment-dominant signal on the tool-holdout and no-anchor slices, but the formal first-screen comparison is incomplete because H1 was blocked by the run-level stop ceiling.
The current state does not support a formal A/B/C/D/E winner under the published Phase H thresholds.
