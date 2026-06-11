# Training Configuration Selection

## Selected Configuration

Use the draft configuration at:

- [configs/lora/stage_b_llama31_8b_base_v1_phase_l_v1_1_external_first.config.draft.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_l_v1_1_external_first.config.draft.json)

## Why This Configuration

This is the Phase L choice because it preserves the proven Phase I trainer geometry and changes only the dataset to Dataset v1.1.
That keeps the comparison interpretable:

- same base model
- same QLoRA adapter shape
- same optimizer and schedule
- same sequence length
- same canonical eval contract
- new dataset only

## Configuration Summary

| Field | Selection |
|---|---|
| Model | `/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base` |
| Train split | `data/v1_1/dataset_v1_1_train.jsonl` |
| Val split | `data/v1_1/dataset_v1_1_val.jsonl` |
| Max sequence length | `2048` |
| Loss | assistant-only / completion-only / fail-fast |
| LoRA | QLoRA, `r=16`, `alpha=32`, `dropout=0.05` |
| Quantization | 4-bit NF4 with double quantization |
| Optimizer | `paged_adamw_8bit` |
| Epoch budget | `0.2` |
| Batch geometry | `1` train batch, `1` eval batch, `16` grad accumulation |
| Checkpointing | gradient checkpointing enabled |
| Output shape | adapter-only save, no merge |

## Selection Rationale

1. The H1 and H2 configs already proved the trainer can complete cleanly with this geometry.
2. Dataset v1.1 is larger and more balanced than the Phase I slices, so changing the dataset is the cleanest way to test the external-first remedy.
3. The config keeps evaluation and decode semantics frozen, which preserves comparability against H0, H1, and H2.
4. The draft status keeps the package honest: the run is defined, but training is not authorized in this phase.

## Operational Note

The selected config is intentionally draft-only.
No training will start until a later authorization step flips the review gate.
