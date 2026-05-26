# assistant-training

Dedicated repository for SFT/LoRA training workflows for assistant models.

## Scope
- Dataset intake, validation, and split management
- Training configs and run manifests
- Training scripts and preflight checks
- Adapter artifact metadata and evaluation handoff

## Non-scope
- Production serving/runtime code (stays in `runtimes/assistant-runtime`)
- Runtime tool execution logic

## First probe assets
- Config: `configs/lora/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1.config.json`
- Run manifest: `manifests/runs/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1.run_manifest.json`

## Suggested workflow
1. Run preflight checks (`scripts/preflight_lora_run.py`).
2. Review config + manifest.
3. Start training only after explicit approval.
4. Save adapter-only output under `artifacts/adapters/...`.
5. Publish post-train evaluation summary for promotion decisions.

## Adapter Evaluation Harness
- Script: `scripts/eval_adapter_toolcalls.py`
- Purpose: compare `base` vs `base+adapter` on the same held-out validation prompts and report:
  - exact tool-call JSON validity
  - tool name accuracy
  - argument accuracy
  - wrapper/prose leakage
  - no-call behavior (if present)
  - failure categories
- Example:
  - `/home/roy/.venvs/llama/bin/python scripts/eval_adapter_toolcalls.py --config configs/lora/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1.config.json`
