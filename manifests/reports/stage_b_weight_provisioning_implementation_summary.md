# Stage B Weight Provisioning Implementation Summary

## Scope
Implemented deterministic, replayable, fail-fast weight provisioning for Stage B first live probe without training/eval execution and without dataset mutation.

## Code Changes

### 1) Trainer-side sidecar hardening
Updated [train_lora_sft.py](/opt/ai-stack/assistant-training/scripts/train_lora_sft.py):
- Added row-identity hash index builder:
  - `_build_row_hash_index_from_row_identity_sidecar` at [train_lora_sft.py](/opt/ai-stack/assistant-training/scripts/train_lora_sft.py:266)
- Extended sidecar loader contract:
  - `_load_weights_from_sidecar` at [train_lora_sft.py](/opt/ai-stack/assistant-training/scripts/train_lora_sft.py:330)
  - now returns `(weights, source_details)`.
  - supports provenance validation for optional envelope fields:
    - `row_identity_reference.rows_total`
    - `row_identity_reference.rows_digest_sha256`
    - `geometry_mapping_identity_digest`
    - `geometry_context_input_digest`
- Added collision-aware `weights_by_row_hash` resolution.
- Added row-hash verification for `rows` sidecar entries.
- Added `weight_source_details` to resolved geometry sampling plan/summary:
  - `_resolve_geometry_sampling_plan` at [train_lora_sft.py](/opt/ai-stack/assistant-training/scripts/train_lora_sft.py:586)

### 2) Probe overlay generator
Added script [provision_geometry_probe_weights.py](/opt/ai-stack/assistant-training/scripts/provision_geometry_probe_weights.py):
- Deterministically compiles declared exposure selectors into per-row weights.
- Reconstructs row identity view compatible with training-side `rows_digest_sha256`.
- Emits probe-specific sidecar with:
  - typed geometry digests,
  - row-identity digest reference,
  - `rows` weight entries (`train_index_0based`, `row_hash_sha256`, `weight`),
  - family and weight summaries.

## New/Updated Probe Artifacts
- Generated sidecar:
  - [stage_b_first_probe_weights_sidecar.json](/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_weights_sidecar.json)
- Updated planned probe config report linkage:
  - [stage_b_first_probe_resolved_config.json](/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_resolved_config.json)
  - switched weight-source intent from metadata strict mode to sidecar overlay path.
- Validation runtime snapshot:
  - [stage_b_weight_provisioning_validation_runtime.json](/opt/ai-stack/assistant-training/manifests/reports/stage_b_weight_provisioning_validation_runtime.json)

## Implementation Complexity
- Overall complexity: `medium`.
- Change surface: weight provisioning path only; no tensor payload, no loss logic, no default sampler path changes.

## Reproducibility Risk Assessment
- Addressed:
  - row identity binding via digest checks,
  - geometry digest binding,
  - duplicate row-hash handling.
- Residual:
  - runtime realized stream capture still depends on actual training execution (outside this phase).
