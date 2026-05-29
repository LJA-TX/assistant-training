# Stage B First Probe Cleanup Plan

Generated: 2026-05-29 (analysis only; no cleanup executed)

## Objective
Consolidate all currently known launch blockers into one pre-retry cleanup plan to avoid one-at-a-time failure discovery.

## Consolidated Remediation Items

1. Path:
`/opt/ai-stack/assistant-training/artifacts/adapters/stage_b_llama31_8b_base_v1_geometry_probe_mh`

- Why it blocks execution:
  - Fails preflight condition `adapter_output_not_present`.
- Safe to remove:
  - Yes. It is runtime-generated output and currently empty.
- Governance/provenance impact:
  - None to canonical probe package, geometry contract, sidecar, thresholds, or datasets.
- Cleanup timing:
  - Required before retry.

2. Path:
`/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_mh`

- Why it blocks execution:
  - Fails startup overwrite protections with `allow_overwrite_run_root=false` due existing artifact hits and non-preflight entries.
- Safe to remove:
  - Yes. It is stale runtime output from prior failed attempt.
- Governance/provenance impact:
  - Preserved. Authoritative package/probe governance artifacts live under `manifests/reports/` and committed config/manifest paths.
- Cleanup timing:
  - Required before retry.

3. Path (optional hygiene):
`/opt/ai-stack/assistant-training/artifacts/logs/stage_b_llama31_8b_base_v1_geometry_probe_mh`

- Why it can matter:
  - Appears in overwrite `artifact_hits` when run_root exists.
- Safe to remove:
  - Yes.
- Governance/provenance impact:
  - None.
- Cleanup timing:
  - Optional if item 2 is removed; recommended for clean slate clarity.

## Must-Preserve Paths (Do Not Remove)

- `/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_geometry_probe_mh.run_manifest.json`
- `/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_geometry_probe_mh.config.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_weights_sidecar.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_geometry_context_input.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_threshold_profile.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_counterbalanced_probe_canonical_eval_summary.json`
- `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i10r_counterbalanced_train.jsonl`
- `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i10r_counterbalanced_val.jsonl`

## Minimal Safe Cleanup Set

1. Remove:
`/opt/ai-stack/assistant-training/artifacts/adapters/stage_b_llama31_8b_base_v1_geometry_probe_mh`

2. Remove:
`/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_mh`

Expected result after cleanup:
- preflight gate can clear adapter-not-present check,
- training startup can pass run-root overwrite protections,
- retry has highest chance to reach actual training entry without changing governed probe semantics.

## Readiness Outcome
`READY_AFTER_CLEANUP`
