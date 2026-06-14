# NVFP4 Model Availability Report

## Scope

This report checks whether `/mnt/models/production/llama-3.1-8b-instruct-nvfp4` can be used as the external reference model for a frozen-contract benchmark.

## Availability

| Check | Result | Evidence |
|---|---|---|
| Production model repo exists | Pass | The launcher bundle is present at `/mnt/models/production/llama-3.1-8b-instruct-nvfp4`. |
| vLLM launcher exists | Pass | `serve.sh` delegates to `serve-vllm.sh`, which binds `127.0.0.1:8012` and points at `/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-instruct-nvfp4`. |
| assistant-runtime alias exists | Pass | `docs/assistant-runtime/config.toml` defines `llama_3_1_8b_nvfp4` with `base_url = "http://127.0.0.1:8012"`. |
| Tokenizer behavior | Pass | The mirrored model path contains a loadable tokenizer; the benchmark shim rendered prompts with the same chat-template path as the frozen evaluator. |
| vLLM service availability | Pass | The service started successfully on `http://127.0.0.1:8012` and exposed `/health`, `/v1/models`, and OpenAI-compatible completion routes. |
| Frozen HF evaluator load path | Blocked | `scripts/eval_canonical_manifest.py` cannot load the NVFP4 checkpoint through Transformers. The failure is a quantization/load compatibility issue followed by a linear weight shape mismatch. |

## Interpretation

The external reference model is service-available through the production vLLM stack, but it is not loadable through the frozen local Transformers evaluator. That makes a direct HF-only canonical run impossible, while still leaving a service-backed benchmark path available without changing the manifest or scoring rules.

## Notes

- Model path: `/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-instruct-nvfp4`
- Service bind: `http://127.0.0.1:8012`
- Frozen evaluator entrypoint checked: `scripts/eval_canonical_manifest.py`
- Canonical eval artifacts for this phase are stored under `evals/runs/phase_zl_nvfp4_external_reference_eval_20260614T131002Z/`

