# Phase I Run Comparison Matrix

## Status

The execution gate was opened, but the first-screen sequence halted after H0.
`H0_control_i3_micro` completed and tripped a Phase H kill metric, so `H2_commitment_patch` and `H1_diversity_patch` were not started.

## Planned Order

1. `H0_control_i3_micro`
2. `H2_commitment_patch`
3. `H1_diversity_patch`

## Comparison Table

| Run | Dataset | Patch size | Execution config | Execution manifest | Execution status | Eval metrics | Delta vs H0 | Stop-rule outcome | Notes |
|---|---|---:|---|---|---|---|---|---|---|
| `H0_control_i3_micro` | Exact `i3` recovery bytes | `0` | `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.config.json` | `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.run_manifest.json` | Completed | `exact_json_validity=0.045`, `invalid_json=0.145`, `tool_name_accuracy=0.07142857142857142`, `argument_accuracy=0.06428571428571428`, `no_call_correctness=0.9166666666666666`, `adversarial_no_call_correctness=0.75` | Control baseline | `kill metric tripped` | Control run is not trustworthy under Phase H |
| `H2_commitment_patch` | `dataset_v1_0_phase_i_h2_commitment_patch_train.jsonl` | `100` | `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.config.json` | `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.run_manifest.json` | Not run | n/a | n/a | Blocked by H0 stop | Not started because H0 failed the no-call/adversarial invariant |
| `H1_diversity_patch` | `dataset_v1_0_phase_i_h1_diversity_patch_train.jsonl` | `100` | `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.config.json` | `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.run_manifest.json` | Not run | n/a | n/a | Blocked by H0 stop | Not started because H0 failed the no-call/adversarial invariant |

## Pending Metrics

The first-screen metrics for the treatments remain pending because the H0 stop rule halted the sequence before H2 and H1 could launch.

## Interim Interpretation

No attribution decision is defensible from the current state alone.
H0 failed the hard-stop invariant, so the first-screen sequence is halted and the experiment must escalate instead of continuing internally.
