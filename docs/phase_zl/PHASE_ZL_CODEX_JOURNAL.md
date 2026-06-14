# Phase ZL Codex Journal

## Evidence Review

- Reviewed the production model bundle at `/mnt/models/production/llama-3.1-8b-instruct-nvfp4`.
- Confirmed the assistant-runtime alias `llama_3_1_8b_nvfp4` in `docs/assistant-runtime/config.toml`.
- Confirmed the frozen canonical evaluator path in `scripts/eval_canonical_manifest.py`.

## Loader Blocker

- The frozen local evaluator cannot load the NVFP4 checkpoint through Transformers.
- The failure occurs after Transformers warns about the checkpoint quantization metadata and then reaches a weight-shape mismatch while loading a linear layer.

## Service-Backed Benchmark

- Started the production vLLM launcher from `/mnt/models/production/llama-3.1-8b-instruct-nvfp4/serve.sh`.
- Verified the model server came up on `http://127.0.0.1:8012`.
- Ran the frozen canonical manifest through a service-backed inference shim that preserved the manifest, prompt rendering, decode defaults, and scorer logic.

## Persisted Artifacts

- Benchmark output directory: `evals/runs/phase_zl_nvfp4_external_reference_eval_20260614T131002Z/`
- Primary summary: `evals/runs/phase_zl_nvfp4_external_reference_eval_20260614T131002Z/summary.json`
- Row-level comparison: `evals/runs/phase_zl_nvfp4_external_reference_eval_20260614T131002Z/comparison_rows.jsonl`

## Outcome

- External reference classification: `below project-trained adapters`
- No training, dataset, scoring, or governance changes were made.

