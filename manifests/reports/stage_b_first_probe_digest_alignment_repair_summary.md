# Stage B First Probe Digest Alignment Repair Summary

## Scope
Artifact repair and validation only.
No training, no evals, and no probe execution were performed.

Canonical alignment target enforced:
- `weighting_mode = deterministic_weighted_sampler_sidecar_overlay`

## Repair Actions Completed
1. Regenerated canonical geometry context input:
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_geometry_context_input.json`

2. Regenerated sidecar from canonical context:
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_weights_sidecar.json`
- command used:
```bash
python scripts/provision_geometry_probe_weights.py \
  --train-jsonl /opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i10r_counterbalanced_train.jsonl \
  --declared-exposure /opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_declared_exposure.json \
  --geometry-context /opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_geometry_context_input.json \
  --output-sidecar /opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_weights_sidecar.json \
  --default-weight 0.0 \
  --min-positive-rows 13
```

3. Regenerated runtime package alignment fields:
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_resolved_config.json`
- `/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_geometry_probe_mh.config.json`
- `/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_geometry_probe_mh.run_manifest.json`

4. Refreshed dependent first-probe review/readiness artifacts with the repaired digest set:
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_go_no_go_summary.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_readiness_reassessment.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_execution_package.md`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_final_review_refresh_results.md`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_declared_exposure.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_hypothesis.json`

Historical forensic artifacts were preserved and not rewritten:
- `stage_b_first_probe_digest_mismatch_forensics.md`
- `stage_b_first_probe_digest_field_diff.json`
- `stage_b_first_probe_digest_alignment_recommendation.md`

## Validation Executed
Validation artifact:
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_digest_alignment_validation.json`

Checks passed:
- runtime `geometry_mapping_identity_digest` equals sidecar `geometry_mapping_identity_digest`
- runtime `geometry_context_input_digest` equals sidecar `geometry_context_input_digest`
- digest contract fields in runtime/resolved config match recomputed values
- sidecar coverage retained:
  - `positive_weight_rows = 13` (>=13)
  - `weights_sum = 36.0`
- sidecar fail-fast behavior retained:
  - deterministic two-pass resolution equality: pass
  - missing-row sidecar failure raises expected error: pass
- preflight passes:
  - `python /opt/ai-stack/assistant-training/scripts/preflight_lora_run.py /opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_geometry_probe_mh.run_manifest.json`

## Operational Note
Preflight initially failed on `adapter_output_not_present` because prior failed-run output directories existed.
Only this probe's prior runtime output directories were removed to restore clean preflight conditions:
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_mh`
- `/opt/ai-stack/assistant-training/artifacts/adapters/stage_b_llama31_8b_base_v1_geometry_probe_mh`
- `/opt/ai-stack/assistant-training/artifacts/logs/stage_b_llama31_8b_base_v1_geometry_probe_mh`

## Final Recommendation
`READY_FOR_RETRY_SINGLE_ATTEMPT`
