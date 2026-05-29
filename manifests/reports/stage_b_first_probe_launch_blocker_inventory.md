# Stage B First Probe Launch Blocker Inventory

Generated: 2026-05-29 (read-only analysis)

## Scope
Comprehensive launch-time blocker inventory for the first live Stage B geometry probe:

- sweep_id: `stage_b_v1_geometry_first_live_probe`
- cell_id: `cell_live_mh_nocall_medium_readfile_high_v1`
- authorized package commit: `ae559bacef10648250f56b20b5303bd91bc3f820`

Boundaries:
- No training/eval/probe execution performed.
- No code/config/dataset/sidecar modifications performed.

## Startup Gates Mapped
Execution path analyzed up to `trainer.train()` entry:

1. `scripts/preflight_lora_run.py` checks.
2. `scripts/train_lora_sft.py` startup gates before trainer loop:
   - approval gate,
   - loss contract,
   - dataset format + load + non-empty,
   - output overwrite protections,
   - geometry sidecar/digest/weight validations,
   - sampler hook compatibility,
   - tokenizer-only full-row masking assertions.

## Active Halting Blockers (Current State)
From `stage_b_first_probe_launch_blocker_matrix.json`:

1. `pref_adapter_output_not_present` (FAIL)
- Source: `scripts/preflight_lora_run.py:34`
- Current state: adapter output dir exists.
- Retry impact: preflight halts immediately.

2. `train_prepare_output_dirs_artifact_hits` (FAIL)
- Source: `scripts/train_lora_sft.py:1816-1840`
- Current state: stale artifact hits detected under probe output paths (`adapter`, `logs`, `checkpoints`, `resolved_config.json`, `masking_audit.json`).
- Retry impact: training startup halts before dataset/model path reaches trainer loop.

3. `train_prepare_output_dirs_non_preflight_only` (FAIL)
- Source: `scripts/train_lora_sft.py:1842-1847`
- Current state: run root contains non-`preflight` entries.
- Retry impact: training startup halts before trainer loop entry.

## Non-Blocking Gates Verified PASS
Key previously problematic gates now pass:

- runtime approval gate (`manifest_approved_to_run=true`) -> PASS
- typed digest alignment (mapping + context input) -> PASS
- sidecar weight validation (positive coverage, deterministic summary) -> PASS
- weighted sampler Trainer hook signature compatibility -> PASS
- tokenizer-only full-row masking assertions across all train+val rows -> PASS

## Full Matrix Reference
See machine-readable condition inventory:

- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_launch_blocker_matrix.json`

Summary snapshot:
- total conditions: 21
- pass: 18
- fail: 3
- halting now: 3

## Readiness Determination
`READY_AFTER_CLEANUP`

Rationale:
- Current halts are filesystem-state blockers, not geometry/governance/digest/sampler-contract blockers.
- Cleanup of stale probe runtime output paths is required before retry.

## Minimal Safe Cleanup Set
Smallest filesystem action set to maximize probability that next retry reaches actual training:

1. Remove adapter output directory:
- `/opt/ai-stack/assistant-training/artifacts/adapters/stage_b_llama31_8b_base_v1_geometry_probe_mh`

2. Remove probe run root directory:
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_mh`

Why minimal:
- Item 1 clears preflight `adapter_output_not_present`.
- Item 2 clears runtime overwrite/reuse protections (`artifact_hits`, `non_preflight_entries`).
- No geometry/threshold/dataset/sidecar/governance artifacts are altered by this cleanup.
