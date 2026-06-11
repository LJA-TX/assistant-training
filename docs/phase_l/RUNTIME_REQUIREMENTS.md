# Runtime Requirements

## Compute Envelope

Phase L reuses the same trainer geometry as the Phase I H1/H2 runs.

Required compute characteristics:

- one GPU capable of running Llama 3.1 8B in 4-bit QLoRA mode
- BF16 support
- enough VRAM for gradient checkpointing plus adapter training
- local access to the model mirror path used by prior phases

Practical sizing:

- 24 GB VRAM minimum
- 32 GB VRAM preferred
- local SSD space for adapters, logs, and eval outputs

## Software Surfaces

Required repository surfaces:

- `scripts/train_lora_sft.py`
- `scripts/eval_canonical_manifest.py`
- `scripts/preflight_lora_run.py`
- `evals/canonical_eval_manifest_v1.json`
- `data/v1_1/dataset_v1_1_train.jsonl`
- `data/v1_1/dataset_v1_1_val.jsonl`

## Expected Wall Clock

Based on the Phase I H1/H2 runs on the same model class and similar epoch budget:

- training: about 160 to 180 seconds
- canonical evaluation: about 30 to 45 seconds
- total train plus eval cycle: budget 10 minutes to allow for artifact writing and variance

## Runtime Settings Kept Fixed

| Setting | Value |
|---|---|
| epochs | `0.2` |
| train batch size | `1` |
| eval batch size | `1` |
| grad accumulation | `16` |
| max sequence length | `2048` |
| LoRA | `r=16`, `alpha=32`, `dropout=0.05` |
| quantization | 4-bit NF4 QLoRA |
| scheduler | cosine |
| learning rate | `0.0001` |

## Why These Requirements Are Enough

The Phase I training summaries show that this geometry is already sufficient to produce a signal on the same model family.
Phase L therefore does not need a larger or more exotic runtime shape to answer the question at hand.
