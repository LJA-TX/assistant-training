# Phase 2 Validation Results

## Validation Scope
- Validate realized-exposure accounting infrastructure only.
- Prove no tensor payload, loss path, trainer path, or sampler behavior changes.
- Prove backward compatibility when `geometry_mapping` is absent.
- Prove declared ledger stability and honest realized/drift confidence labeling.

## Executed Checks
1. `python -m py_compile scripts/train_lora_sft.py`
- Result: `PASS`.

2. Tensor payload contract check (`_TokenizedDataset.__getitem__`)
- Runtime keys: `['attention_mask', 'input_ids', 'labels']`.
- Result: `PASS` (no tensor contract change).
- Code location: [train_lora_sft.py](/opt/ai-stack/assistant-training/scripts/train_lora_sft.py:845)

3. Sampler/weighted-sampling non-mutation guard
- Pattern scan: `WeightedRandomSampler|get_train_dataloader|_get_train_sampler|sampler=|loss_weight|sample_weight`
- Output: `NO_MATCHES`.
- Result: `PASS` (no weighted sampling behavior, sampler behavior, or sampling hooks added).

4. Trainer path non-mutation guard
- `trainer = Trainer(...)` remains the active construction path.
- No sampler injection argument on the trainer call.
- Result: `PASS`.
- Location: [train_lora_sft.py](/opt/ai-stack/assistant-training/scripts/train_lora_sft.py:1370)

5. Loss-path non-mutation guard
- Diff-hunk scan for loss-path markers in modified hunks returned `NO_LOSS_HUNK_MATCHES`.
- `_validate_loss_requirements` remains present and unchanged as control point.
- Result: `PASS`.
- Location: [train_lora_sft.py](/opt/ai-stack/assistant-training/scripts/train_lora_sft.py:950)

6. Backward compatibility without `geometry_mapping`
- `_resolve_geometry_context({})` returns defaults:
  - `geometry_schema_version='1.0'`
  - `sweep_id='unspecified'`
  - `cell_id='unspecified'`
  - `axis_levels={}`
  - `weighting_mode='none'`
  - `declared_exposure_units={}`
- Result: `PASS`.

7. Declared ledger stability check
- Rebuilt declared ledger twice from committed train/val JSONL.
- Equality (excluding `generated_utc`): `true`.
- Summary equality: `true`.
- Result: `PASS` (declared accounting stable under identical inputs).

8. Stable row identity determinism check
- Rebuilt row identity sidecar twice from identical train rows.
- `rows_digest_sha256` both runs: `6544e7cc0127ceb70d53a9ede4c8c36de1d1f8a764ce935e652e80b2be871c71`.
- Result: `PASS` (stable deterministic row identity).

9. Honest realized/drift labeling check
- [exposure_ledger_realized_example.json](/opt/ai-stack/assistant-training/manifests/reports/exposure_ledger_realized_example.json):
  - `status='realized_exposure_default_path_inferred'`
  - `capture_mode='index_space_inferred_no_sampler_stream_capture'`
  - `confidence='limited'`
  - non-empty `limitations`
- [exposure_ledger_drift_example.json](/opt/ai-stack/assistant-training/manifests/reports/exposure_ledger_drift_example.json):
  - `status='declared_vs_realized_comparison_default_path_inferred'`
  - `comparison_basis='declared_train_split_vs_inferred_realized_index_space'`
  - `confidence='limited'`
  - non-empty `limitations`
- Result: `PASS` (artifacts are emitted/stubbed with explicit constraints and no overclaim).

## Validation Summary
- Tensor payload unchanged.
- Loss path unchanged.
- Trainer/sampler behavior unchanged.
- Backward compatibility maintained when `geometry_mapping` is absent.
- Declared ledger remains stable.
- Realized/drift ledgers are emitted with explicit default-path inference limitations.
