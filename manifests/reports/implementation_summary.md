# Stage B v1 Instrumentation Implementation Phase 1 Summary

## Scope Compliance
- Implemented only metadata propagation + declared-exposure accounting.
- No training, no eval execution, no sweep execution.
- No dataset generation/mutation.
- No weighted sampling implementation.
- No collapse detection implementation.

## Code Changes
### 1. Geometry Context Plumbing (Additive Only)
Updated [train_lora_sft.py](/opt/ai-stack/assistant-training/scripts/train_lora_sft.py) with:
- `geometry_context` resolver with backward-compatible defaults (`lines 39-56`).
- deterministic `geometry_context_digest` (`lines 59-67`).
- additive geometry trace payload plumbing into:
  - `resolved_config.json` (`lines 887-897` and audit-only `818-827`)
  - `masking_audit.json` (`lines 941-950` and audit-only `804-813`)
  - `training_summary.json` (`lines 1012-1026`)

Behavioral note:
- No tensor payload contract changes in `_TokenizedDataset.__getitem__` (`lines 554-562`).
- No Trainer/sampler path changes (`lines 994-1001`).

### 2. Geometry Context Digest
Implemented deterministic digest path in [train_lora_sft.py](/opt/ai-stack/assistant-training/scripts/train_lora_sft.py):
- Required digest fields:
  - `geometry_schema_version`
  - `sweep_id`
  - `cell_id`
  - `axis_levels`
  - `weighting_mode`
- Canonicalization: stable sorted-key JSON via `_canonical_json_text`.
- Hash function: SHA-256.

### 3. Declared Exposure Ledger
Implemented declared-only exposure accounting in [train_lora_sft.py](/opt/ai-stack/assistant-training/scripts/train_lora_sft.py):
- split-level aggregation helper (`lines 95-166`)
- ledger constructor (`lines 169-228`)
- write paths:
  - full path: `run_root/exposure_ledger_declared.json` (`line 885`, write at `914`)
  - audit-only path: `run_root/preflight/exposure_ledger_declared.json` default (`lines 765-780`)

Ledger content includes:
- geometry declaration + digest
- dataset path provenance
- declared exposure breakdown by split (train/val/combined)
- family/archetype/tool/axis-signature/pair-id counts
- metadata coverage metrics

### 4. Artifact Traceability
Added non-breaking fields:
- `geometry_context`
- `geometry_context_digest`
- `declared_exposure_ledger_path`
- `declared_exposure_summary` (masking audit + training summary)

## Backward Compatibility
- If `geometry_mapping` is missing in config, defaults are applied deterministically:
  - `geometry_schema_version="1.0"`
  - `sweep_id="unspecified"`
  - `cell_id="unspecified"`
  - `axis_levels={}`
  - `weighting_mode="none"`
- Existing configs without geometry metadata can still produce a valid declared ledger.

## Generated Artifacts in This Phase
- [geometry_context_digest_design.json](/opt/ai-stack/assistant-training/manifests/reports/geometry_context_digest_design.json)
- [exposure_ledger_declared_example.json](/opt/ai-stack/assistant-training/manifests/reports/exposure_ledger_declared_example.json)
- [validation_results.md](/opt/ai-stack/assistant-training/manifests/reports/validation_results.md)
