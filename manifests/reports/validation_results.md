# Phase 1 Validation Results

## Validation Scope
- Validate additive-only metadata plumbing and declared-exposure accounting.
- Prove no tensor contract, loss path, or trainer behavior changes.
- Prove backward compatibility.

## Executed Checks
1. `python -m py_compile scripts/train_lora_sft.py`
- Result: `PASS`.

2. Tensor payload contract check (`_TokenizedDataset.__getitem__`)
- Runtime check returned keys: `['attention_mask', 'input_ids', 'labels']`.
- Result: `PASS` (unchanged tensor contract).
- Code location: [train_lora_sft.py](/opt/ai-stack/assistant-training/scripts/train_lora_sft.py:554).

3. Digest determinism check
- `_build_geometry_context_digest(_resolve_geometry_context({}))` produced identical digest on repeated calls.
- Result: `PASS`.

4. Sampler/trainer behavior guard (no weighted sampling implementation)
- Search pattern: `WeightedRandomSampler|_get_train_sampler|get_train_dataloader|sampler=` in [train_lora_sft.py](/opt/ai-stack/assistant-training/scripts/train_lora_sft.py)
- Matches: none.
- Result: `PASS` (no sampling-path changes).

5. Loss-path non-mutation guard
- Zero-context diff search for loss-path markers (`assistant_completion_only_requested`, `completion_only_loss`, `train_on_inputs`, `fallback_behavior_if_not_supported`) in changed hunks returned no matches.
- Result: `PASS` (loss-path logic unchanged).
- Loss function location remains: [train_lora_sft.py](/opt/ai-stack/assistant-training/scripts/train_lora_sft.py:661).

6. Trainer-call non-mutation guard
- `trainer = Trainer(...)` remains the construction path.
- No custom trainer class or sampler injection added.
- Result: `PASS`.
- Location: [train_lora_sft.py](/opt/ai-stack/assistant-training/scripts/train_lora_sft.py:994).

7. Backward compatibility with existing config (no `geometry_mapping` block)
- Existing config parsed successfully with defaults:
  - `sweep_id="unspecified"`
  - `weighting_mode="none"`
- Declared ledger built successfully from current dataset metadata.
- Result: `PASS`.

8. Declared ledger artifact structure check
- [exposure_ledger_declared_example.json](/opt/ai-stack/assistant-training/manifests/reports/exposure_ledger_declared_example.json) contains:
  - `geometry_context_digest`
  - `declaration`
  - `declared_exposure_by_split`
- Combined row count present (`2218`).
- Result: `PASS`.

## Summary
- No tensor contract changes detected.
- No loss-path changes detected.
- No trainer/sampling behavior changes detected.
- Backward compatibility maintained.
- Declared exposure accounting and geometry trace plumbing validated.
