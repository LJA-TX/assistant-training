# Stage B First Probe Sampler Hook Fix Summary

## Scope
Minimal compatibility fix only for `_GeometrySamplingTrainer._get_train_sampler` in:

- `/opt/ai-stack/assistant-training/scripts/train_lora_sft.py`

No training/eval/probe execution performed.

## Change Applied
Updated sampler-hook signature to match Transformers 5.9.0-compatible call shape.

- Before: `_get_train_sampler(self)`
- After: `_get_train_sampler(self, train_dataset=None)`

Disabled-path delegation updated to pass through the optional dataset argument:

- Before: `super()._get_train_sampler()`
- After: `super()._get_train_sampler(train_dataset)`

## Behavior Preservation
Confirmed unchanged behavior for approved weighted path and default path:

- Geometry-sampling-enabled path still returns the existing traceable weighted sampler logic.
- Geometry-sampling-disabled path still delegates to base Trainer sampler logic.
- Sampler seed/generator/replacement/num_samples behavior unchanged.
- Sampled-index capture path unchanged.
- Exposure-accounting artifact plumbing unchanged.
- No tensor payload contract changes.
- No loss-path logic changes.

## Validation Executed
1. Static compile:

- `python -m py_compile scripts/train_lora_sft.py` -> pass

2. Signature/delegation compatibility:

- Base signature (Transformers 5.9.0): `(self, train_dataset: Dataset | None = None)`
- Custom signature now accepts `train_dataset=None`.
- Disabled-path delegation compatibility check -> pass.

3. Synthetic sampler checks (no training):

- Weighted sampler construction -> pass.
- Determinism metadata stability for same seed/input -> pass.
- Sidecar-backed weight resolution/validation -> pass.
- Positive-weight coverage preserved: `13` rows, `weights_sum=36.0`.

Detailed machine-readable results:

- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_sampler_hook_fix_validation.json`

## Final Recommendation
`READY_FOR_RETRY_SINGLE_ATTEMPT`
