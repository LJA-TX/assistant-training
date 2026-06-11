# Phase I Run Comparison Matrix

## Status

The execution gate is open and the matrix is ready for first-screen results.
The dataset-preparation slice is complete; the first-screen runs have not been executed yet.

## Planned Order

1. `H0_control_i3_micro`
2. `H2_commitment_patch`
3. `H1_diversity_patch`

## Comparison Table

| Run | Dataset | Patch size | Execution config | Execution manifest | Execution status | Notes |
|---|---|---:|---|---|---|---|
| `H0_control_i3_micro` | Exact `i3` recovery bytes | `0` | `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.config.json` | `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.run_manifest.json` | Approved, not started | Fresh control repro on frozen i3 bytes |
| `H2_commitment_patch` | `dataset_v1_0_phase_i_h2_commitment_patch_train.jsonl` | `100` | `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.config.json` | `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.run_manifest.json` | Approved, not started | Anchor-light paraphrastic patch on control tool-positive rows |
| `H1_diversity_patch` | `dataset_v1_0_phase_i_h1_diversity_patch_train.jsonl` | `100` | `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.config.json` | `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.run_manifest.json` | Approved, not started | Tail-tool diversity patch from the internal source pool |

## Pending Metrics

Once the runs exist, populate the matrix with:

- tool-expected exact JSON validity
- tool-holdout exact JSON validity
- tool-name accuracy
- argument accuracy
- tool-expected invalid JSON rate
- direct-answer substitution share
- scalar substitution share
- invalid-schema share
- no-call correctness

## Interim Interpretation

No attribution decision should be made from the current state alone.
The current evidence supports execution readiness, not bottleneck attribution.
