# Stage B First Probe Execution Results

## Probe Identity
- `sweep_id`: `stage_b_v1_geometry_first_live_probe`
- `cell_id`: `cell_live_mh_nocall_medium_readfile_high_v1`
- expected start checkpoint: `3b4812e1bb66ca6936cce3be4869aaa84ab11276`

## Commands Actually Run
1. `git status --short --branch`
2. `git rev-parse HEAD && git rev-parse origin/main`
3. `git rev-parse --verify 3b4812e1bb66ca6936cce3be4869aaa84ab11276`
4. `python /opt/ai-stack/assistant-training/scripts/preflight_lora_run.py /opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_geometry_probe_mh.run_manifest.json`
5. `/home/roy/.venvs/llama/bin/accelerate launch --num_processes 1 /opt/ai-stack/assistant-training/scripts/train_lora_sft.py --config /opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_geometry_probe_mh.config.json`

## Execution Outcome
- start-state checks: passed
- preflight: passed
- training: failed on first attempt (exit code `1`)
- retries: none
- hidden retries: none
- eval: not run (blocked by training failure)
- collapse detector: not run (blocked by training failure)

## Failure Point
Training aborted during geometry-sampling sidecar validation before trainer loop:

`RuntimeError: geometry_sampling sidecar geometry_mapping_identity_digest mismatch: expected e7e440b7083160fed25f418e529e67e677f443ddafaa61279fcd614673f7de3b, got 1a0f418214854dd4c1db33e7962169ae23002e1fa9979394860faf89837d4eee`

Observed context behind mismatch:
- runtime config `geometry_mapping.weighting_mode`: `deterministic_weighted_sampler_sidecar_overlay`
- sidecar `geometry_context.weighting_mode`: `deterministic_weighted_sampler_metadata`
- mapping digest includes `weighting_mode`, so digest divergence is expected under this mismatch.

## Artifacts Emitted Before Failure
Generated under:
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_mh/`

Emitted files:
- `exposure_ledger_declared.json`
- `exposure_row_identity_sidecar.json`

Not emitted (training did not reach those stages):
- `resolved_config.json`
- `masking_audit.json`
- `training_summary.json`
- `exposure_ledger_realized.json`
- `exposure_ledger_drift.json`
- `sampler_determinism_report.json`
- eval outputs
- detector outputs

## Final Recommendation
`NOT_READY`
