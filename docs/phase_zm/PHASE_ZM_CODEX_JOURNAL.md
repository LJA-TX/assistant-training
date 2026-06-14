# Phase ZM Codex Journal

## Evidence Review

- Verified the non-quantized model path at `/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-instruct`.
- Confirmed the frozen canonical evaluator can load the checkpoint directly.
- Executed the frozen canonical evaluation contract without changing the manifest, scorer, or thresholds.

## Run Details

- Run directory: `evals/runs/phase_zm_instruct_external_reference_eval_20260614T131500Z/`
- Model path: `/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-instruct`
- Evaluation path: `scripts/eval_canonical_manifest.py`

## Outcome

- External reference classification: `behaviorally equivalent` relative to NVFP4
- No fallback service accommodation was required
- No training, dataset, scoring, or governance changes were made

