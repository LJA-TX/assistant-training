# Stage B Successor Probe Launch Blocker Inventory

Generated: 2026-06-03 (package-construction assessment)

## Scope
Launch-time blocker inventory for the successor Stage B geometry probe:

- `sweep_id`: `stage_b_v1_geometry_successor_probe`
- `cell_id`: `cell_live_lh_nocall_low_readfile_high_v1`

Boundaries:
- No training/eval/probe execution performed.
- No cleanup execution performed.
- Package construction only.

## Startup Gates Mapped
Execution path analyzed up to `trainer.train()` entry:

1. `scripts/preflight_lora_run.py` checks.
2. `scripts/train_lora_sft.py` startup gates before trainer loop:
   - approval gate,
   - output overwrite protections,
   - geometry sidecar/digest validation.

## Active Launch Blockers
From `stage_b_successor_probe_launch_blocker_matrix.json`:

1. `train_runtime_approval_gate` (FAIL)
- Description:
  - The successor package keeps `requires_manual_review=true`, `config_approved_to_run=false`, and `manifest_approved_to_run=false`.
- Severity:
  - `critical`
- Estimated effort to resolve:
  - `small`
- Dependencies:
  - explicit human launch review and authorization record.
- Blocks launch authorization:
  - `yes`

## Cleanup Items
Successor-specific cleanup required before launch:
- none

Successor-specific optional cleanup:
- none

The new successor output targets are currently absent:
- `/opt/ai-stack/assistant-training/artifacts/adapters/stage_b_llama31_8b_base_v1_geometry_probe_lh`
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_lh`
- `/opt/ai-stack/assistant-training/artifacts/logs/stage_b_llama31_8b_base_v1_geometry_probe_lh`

## Desirable Future Improvements
- Add explicit realized selector-level accounting for `valid_rg_search_contrastive_family` so future runs can verify that axis directly rather than only through declared exposure and sidecar composition.
- Capture a preserved commit/checkpoint for the constructed successor package before any launch, if provenance tightening is desired.

## Readiness Determination
`READY_PENDING_MANUAL_GO`

Rationale:
- No successor-specific filesystem cleanup is needed.
- Sidecar, geometry context, run manifest, config, and restored metric-path contract are aligned.
- Launch is intentionally blocked only by the unset manual approval gate.
