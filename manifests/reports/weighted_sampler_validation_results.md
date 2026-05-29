# Weighted Sampler Validation Results

## Scope
- Validate Phase 3 instrumentation behavior only.
- No training, no eval, no sweep execution.

## Executed Checks
1. Syntax and import integrity
- Command: `python -m py_compile scripts/train_lora_sft.py`
- Result: `PASS`.

2. Default-path dormancy (`geometry_sampling` absent)
- Unit check on existing config resolved:
  - `plan_enabled=false`
  - `sampler_class=transformers_default_random_sampler_path`
- Result: `PASS` (weighted sampler dormant by default).

3. Tensor payload contract
- `_TokenizedDataset.__getitem__` keys: `['attention_mask', 'input_ids', 'labels']`
- Result: `PASS` (no tensor contract change).
- Code location: [train_lora_sft.py](/opt/ai-stack/assistant-training/scripts/train_lora_sft.py:1468)

4. Loss-path non-mutation guard
- Diff-hunk marker scan for loss controls returned `NO_LOSS_PATH_DIFF_MARKERS`.
- `_validate_loss_requirements` remains intact.
- Result: `PASS`.
- Code location: [train_lora_sft.py](/opt/ai-stack/assistant-training/scripts/train_lora_sft.py:1573)

5. Invalid weight unit checks (fail-fast)
- Cases validated: `length_mismatch`, `negative_weight`, `nonnumeric_weight`, `nonfinite_weight`, `all_zero`.
- All cases raised expected errors.
- Result: `PASS`.

6. Deterministic plan metadata
- Two independent resolutions of identical enabled config produced identical `weights_digest_sha256`.
- Result: `PASS`.

7. Deterministic sampled stream (same seed)
- Two samplers with identical weights/seed produced identical sampled index sequences.
- Result: `PASS`.

8. Weighted realized-ledger mode
- Runtime-captured synthetic stream emitted:
  - `status=realized_exposure_weighted_sampler_stream_captured`
  - `capture_mode=runtime_weighted_sampler_stream_capture`
  - `confidence=high`
- Result: `PASS`.

9. Drift ledger confidence/mode distinction
- Inferred/default path: limited confidence + inferred status.
- Weighted runtime-captured path: high confidence + weighted-stream status.
- Result: `PASS`.

## Key Artifacts
- [sampler_determinism_report.json](/opt/ai-stack/assistant-training/manifests/reports/sampler_determinism_report.json)
- [exposure_ledger_realized_weighted_mode_design.json](/opt/ai-stack/assistant-training/manifests/reports/exposure_ledger_realized_weighted_mode_design.json)
- [weighted_sampler_config_contract.json](/opt/ai-stack/assistant-training/manifests/reports/weighted_sampler_config_contract.json)

## Validation Summary
- Default behavior unchanged and weighted path gated.
- Weighted sampler determinism controls functional.
- Runtime-captured weighted realized-exposure path produces high-confidence mode.
- No tensor/loss contract regressions detected.
