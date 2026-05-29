# Stage B v1 Instrumentation Implementation Phase 2 Summary

## Scope Compliance
- Implemented only realized-exposure accounting infrastructure.
- No training/eval/sweep execution.
- No dataset generation or mutation.
- No weighted-sampler behavior implementation.
- No sampler behavior changes.
- No loss behavior changes.
- No tensor payload contract changes.

## Code Changes
Updated [train_lora_sft.py](/opt/ai-stack/assistant-training/scripts/train_lora_sft.py):

### 1. Stable Row Identity + Normalized Geometry View
Added helpers:
- `_row_content_hash` (`line 234`)
- `_resolve_normalized_geometry_metadata_view` (`line 238`)
- `_build_train_row_identity_sidecar` (`line 266`)

Row identity sidecar fields:
- `train_index_0based`
- `row_hash_sha256`
- normalized geometry fields (`geometry_family`, `geometry_archetype`, `geometry_axes`, `geometry_pair_id`)
- `geometry_axes_signature`

The sidecar remains outside model tensors and sampler paths.

### 2. Realized Exposure Ledger (Default-Path Inferred)
Added:
- `_build_realized_exposure_ledger_default_path` (`line 353`)

Outputs:
- `exposure_ledger_realized.json`
- status: `realized_exposure_default_path_inferred`
- capture mode explicitly marked as inferred (no sampled-index stream capture yet)
- confidence/limitations explicitly declared

### 3. Drift Ledger Skeleton
Added:
- `_build_dimension_drift_report` (`line 410`)
- `_build_exposure_drift_ledger` (`line 449`)

Outputs:
- `exposure_ledger_drift.json`
- compares declared train split vs inferred realized index-space counts
- includes confidence/limitations and aggregate drift indicators

### 4. Artifact Integration (Non-Breaking)
Added trace paths to resolved/training artifacts:
- `row_identity_sidecar_path`
- `realized_exposure_ledger_path`
- `exposure_drift_ledger_path`

Added summaries to training/masking trace payloads:
- `row_identity_summary`
- `realized_exposure_summary`
- `exposure_drift_summary`

Integration points:
- audit-only path wiring (`lines 1059-1162`)
- full training path wiring (`lines 1223-1405`)

## Behavioral Guardrails Preserved
- Tensor batch contract unchanged: `_TokenizedDataset.__getitem__` still returns only `input_ids`, `labels`, `attention_mask`.
- Trainer construction unchanged: still `Trainer(...)` default path, no sampler subclass/hook.
- Loss requirement logic unchanged (`_validate_loss_requirements`).

## Phase 2 Deliverables
- [exposure_ledger_realized_design.json](/opt/ai-stack/assistant-training/manifests/reports/exposure_ledger_realized_design.json)
- [exposure_ledger_realized_example.json](/opt/ai-stack/assistant-training/manifests/reports/exposure_ledger_realized_example.json)
- [exposure_ledger_drift_example.json](/opt/ai-stack/assistant-training/manifests/reports/exposure_ledger_drift_example.json)
- [phase2_validation_results.md](/opt/ai-stack/assistant-training/manifests/reports/phase2_validation_results.md)
