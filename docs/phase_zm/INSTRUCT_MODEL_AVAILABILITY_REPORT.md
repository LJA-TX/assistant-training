# Instruct Model Availability Report

## Scope

This report checks whether `/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-instruct` can be benchmarked against the frozen canonical evaluation contract.

## Availability

| Check | Result | Evidence |
|---|---|---|
| Model path exists | Pass | The full non-quantized Llama-3.1-8B-Instruct checkpoint is present at `/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-instruct`. |
| Tokenizer availability | Pass | `tokenizer.json` and `tokenizer_config.json` are present in the model directory and loaded successfully by the frozen evaluator. |
| Frozen evaluator compatibility | Pass | `scripts/eval_canonical_manifest.py` loaded the model directly through Transformers without any fallback path. |
| Loader behavior | Pass | The checkpoint loaded in 4 shards and completed the canonical run on the local harness. |
| Service fallback needed | No | The frozen evaluator executed directly, so the production service stack was not required. |

## Interpretation

The non-quantized Instruct model is directly compatible with the frozen project evaluator. No accommodation was required beyond the standard canonical manifest override of the model path.

## Notes

- Model path: `/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-instruct`
- Frozen evaluator: `scripts/eval_canonical_manifest.py`
- Canonical run directory: `evals/runs/phase_zm_instruct_external_reference_eval_20260614T131500Z/`

