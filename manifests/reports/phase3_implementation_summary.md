# Stage B v1 Instrumentation Implementation Phase 3 Summary

## Scope Compliance
- Implemented deterministic weighted sampler infrastructure behind explicit `geometry_sampling.enabled` gate.
- Default path remains unchanged when `geometry_sampling` is absent or disabled.
- No training, eval, sweep execution, dataset generation, or dataset mutation performed in this phase.
- No loss behavior changes.
- No tensor payload contract changes.

## Code Changes
Updated [train_lora_sft.py](/opt/ai-stack/assistant-training/scripts/train_lora_sft.py):

1. `geometry_sampling` config contract and resolver
- Added `_resolve_geometry_sampling_cfg` and `_resolve_geometry_sampling_plan`.
- Added disabled-by-default behavior and fail-fast validation for:
  - weight vector length mismatch
  - non-numeric weights
  - non-finite weights
  - negative weights
  - all-zero vectors

2. Weighted sampler trainer hook (minimal override)
- Added `_make_geometry_sampling_trainer_subclass` that overrides only `_get_train_sampler`.
- Added `_create_traceable_weighted_random_sampler` to seed deterministically and capture sampled indices.
- Base `Trainer(...)` path is preserved when sampling gate is disabled.

3. Determinism plumbing
- Seeded weighted sampler from explicit `geometry_sampling.sampler_seed` (fallback `optimization.seed`).
- Added deterministic weight digest via canonical JSON hash.
- Added sampler determinism artifact writer via `_build_sampler_determinism_report`.

4. Realized exposure stream capture
- Added `_build_realized_exposure_ledger_weighted_path` for runtime captured index stream mode.
- Added `_extract_weighted_sampler_runtime_capture`.
- Distinct modes:
  - default/inferred limited confidence
  - weighted/runtime captured high confidence

5. Drift ledger mode distinction
- Updated `_build_exposure_drift_ledger` to derive status/comparison basis/confidence from realized capture mode.

6. Artifact integration
- Extended `resolved_config`, masking audit trace, and training summary with:
  - `geometry_sampling`
  - `sampler_determinism_path`
- Extended realized ledger with geometry sampling trace and mode distinction.
- Extended drift ledger status semantics for weighted runtime capture.

## Behavior Guarantees
- Tensor payload contract unchanged at `_TokenizedDataset.__getitem__`.
- Loss path unchanged at `_validate_loss_requirements`.
- Default trainer/sampler behavior unchanged unless `geometry_sampling.enabled=true`.
- Weighted sampler code path remains dormant by default.
