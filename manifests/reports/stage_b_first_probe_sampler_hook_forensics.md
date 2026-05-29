# Stage B First Probe Sampler Hook Forensics

## Scope
Bounded read-only forensic analysis of `_GeometrySamplingTrainer._get_train_sampler` integration failure.
No code changes, no train/eval/probe rerun, no commits/pushes.

## 1) Located Components
Custom sampler trainer hook:
- File: `/opt/ai-stack/assistant-training/scripts/train_lora_sft.py`
- Factory: `_make_geometry_sampling_trainer_subclass` (`1333-1359`)
- Hook: `_GeometrySamplingTrainer._get_train_sampler` defined at `1340`

Base Trainer hook (installed Transformers):
- File: `/home/roy/.venvs/llama/lib/python3.12/site-packages/transformers/trainer.py`
- Version: `transformers==5.9.0`
- Hook definition: `_get_train_sampler(self, train_dataset: Dataset | None = None)` (`1053-1080`)

## 2) Signature Comparison
Current custom signature:
- `_get_train_sampler(self)`

Installed base-class signature:
- `_get_train_sampler(self, train_dataset: Dataset | None = None)`

Mismatch:
- Custom hook does not accept the dataset argument now provided by the Trainer call path.

## 3) Invocation Path and Arguments
Invocation path in Transformers 5.9.0:
1. `Trainer.get_train_dataloader` (`1128-1146`) calls `_get_dataloader(..., sampler_fn=self._get_train_sampler, ...)`
2. `Trainer._get_dataloader` (`1082-1126`) invokes `sampler_fn(dataset)` at line `1109`
3. `dataset` is the training dataset (`self.train_dataset` from line `1141`)

Supplied arguments at failure:
- positional args to custom hook: `(self, dataset)`

Observed runtime error:
- `TypeError: _GeometrySamplingTrainer._get_train_sampler() takes 1 positional argument but 2 were given`

## 4) Minimal Compatibility Fix Determination
Minimal fix for current environment:
- **Signature-only** update to custom hook so it accepts the dataset argument expected by current Trainer call path.

Classification:
- signature-only: **yes**
- call-site change: **no** (call-site is inside installed Transformers)
- version-compatibility wrapper: **not required** for this environment
- broader Trainer integration issue: **no evidence**

## 5) Risk Assessment
Tensor contract impact:
- none expected; sampler selection does not alter tokenization/tensor schema.

Loss-path impact:
- none expected; loss computation stack unchanged.

Sampler determinism impact:
- none expected if existing sampler construction remains unchanged (same seed, generator, replacement, num_samples, weights).

Exposure-accounting impact:
- low positive: fixing the hook should unblock full training loop execution so weighted sampled-stream capture and downstream realized/drift ledgers can be produced with normal confidence path.

## Conclusion
Root cause is a strict method signature mismatch between local subclass hook and Transformers 5.9.0 Trainer invocation semantics. The issue is localized and does not indicate broader trainer architecture failure.
