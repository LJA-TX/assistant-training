# Phase I Execution Gate Approval

## Approval Result

**PASS**

The Phase I first-screen sequence is authorized to execute in this order:

1. `H0_control_i3_micro`
2. `H2_commitment_patch`
3. `H1_diversity_patch`

## Approval Rationale

- The frozen surfaces remain unchanged:
  - `evals/canonical_eval_manifest_v1.json`
  - `scripts/train_lora_sft.py`
  - `scripts/eval_canonical_manifest.py`
  - base model path `llama-3.1-8b-base`
  - tokenizer / prompt-template mode `tokenizer_chat_template` with `generic_roles_v1` fallback
- The Phase I dataset variants were constructed inside the declared bounded patch envelope.
- The H1 and H2 treatment datasets preserve the frozen train/val row counts and clear the declared holdout contamination gates.
- The H0 control uses the exact frozen i3 recovery bytes.
- The promoted execution assets differ from the drafts only in approved run-state and approval metadata.
- No methodology, masking, optimizer, LoRA topology, evaluation topology, thresholds, or promotion gates were changed.

## Validation Results

| Check | Result | Evidence |
|---|---|---|
| Frozen surfaces unchanged | PASS | `docs/phase_i/CONTROL_SURFACE_VERIFICATION.md` |
| H0 control hashes match Phase I record | PASS | `c19dbab14d930c39b90f85de8f7bf820f1ac37035756a9ca5063f823369e3f9a` train, `d1bde5c675e22a88df250ac91e13522bb4d9ff8685d86e3b885f6d8d106d661f` val |
| H1 hashes match Phase I record | PASS | `fb488f828b9ff42f2c067031ae4e7d65edecd791420c2d6daf79e27422e4e947` train, `d1bde5c675e22a88df250ac91e13522bb4d9ff8685d86e3b885f6d8d106d661f` val |
| H2 hashes match Phase I record | PASS | `41834b7dd1b06bf90bfdb38b77c15f67a3dfdab802d164b0edddfcc686a75fd5` train, `d1bde5c675e22a88df250ac91e13522bb4d9ff8685d86e3b885f6d8d106d661f` val |
| Holdout contamination clean | PASS | `heldout_validation` and `tool_holdout` overlap remain `0` across the treatment summaries |
| Promotion deltas are approved-only | PASS | see below |

### Promotion Deltas

#### Config files

Changed fields from the draft configs:

- `generated_utc`
- `safety.do_not_start_training_automatically`
- `safety.approved_to_run`
- `scaffold_notes.execution_state`
- `scaffold_notes.gate_opened`

#### Run manifests

Changed fields from the draft run manifests:

- `generated_utc`
- `status`
- `config_path`
- `review_gate.approved_to_run`
- `review_gate.approved_by`
- `review_gate.approved_utc`
- `scaffold_notes.implementation_phase`
- `scaffold_notes.gate_opened`

## Exact Assets Approved For Execution

### H0_control_i3_micro

- Config: `/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.config.json`
- Run manifest: `/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.run_manifest.json`
- Train data: `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl`
- Val data: `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_val.jsonl`
- Run root: `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro`

### H2_commitment_patch

- Config: `/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.config.json`
- Run manifest: `/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.run_manifest.json`
- Train data: `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_train.jsonl`
- Val data: `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_val.jsonl`
- Run root: `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch`

### H1_diversity_patch

- Config: `/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.config.json`
- Run manifest: `/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.run_manifest.json`
- Train data: `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_train.jsonl`
- Val data: `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_val.jsonl`
- Run root: `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch`

## Execution Notes

- The execution gate is open.
- The first-screen runs remain bounded and must still be evaluated immediately after each run.
- The Phase H stop rules still apply after every run.
