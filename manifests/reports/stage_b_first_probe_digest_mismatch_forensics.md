# Stage B First Probe Digest Mismatch Forensics

## Scope
Read-only forensic analysis of the first live probe halt.
No training, eval, probe rerun, code edits, config edits, or sidecar regeneration were performed.

## Probe And Halt Context
- Probe: `stage_b_v1_geometry_first_live_probe / cell_live_mh_nocall_medium_readfile_high_v1`
- Halt message:
  - `geometry_sampling sidecar geometry_mapping_identity_digest mismatch`
  - expected `e7e440b7083160fed25f418e529e67e677f443ddafaa61279fcd614673f7de3b`
  - got `1a0f418214854dd4c1db33e7962169ae23002e1fa9979394860faf89837d4eee`

## 1) Where Expected Digest (`e7e440...`) Was Generated
- Artifact carrying expected digest:
  - `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_weights_sidecar.json`
- Generation path:
  - script: `/opt/ai-stack/assistant-training/scripts/provision_geometry_probe_weights.py`
  - digest function: `_build_geometry_mapping_identity_digest` (`53-61`)
  - sidecar emit callsite: (`379-406`)
- Source geometry context used by sidecar generator:
  - `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_geometry_context_input.json`
  - contains `weighting_mode = deterministic_weighted_sampler_metadata`
- Sidecar `generated_utc`: `2026-05-29T13:17:52Z`

## 2) Where Observed Digest (`1a0f4182...`) Was Generated
- Runtime digest is recomputed from config geometry context in trainer:
  - script: `/opt/ai-stack/assistant-training/scripts/train_lora_sft.py`
  - context resolver: `_resolve_geometry_context` (`40-57`)
  - digest function: `_build_geometry_mapping_identity_digest` (`60-68`)
  - runtime callsite: main flow line `2136`
  - mismatch enforcement: `_load_weights_from_sidecar` check (`386-403`)
- Runtime context evidence is persisted before failure in:
  - `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_mh/exposure_ledger_declared.json`
  - digest there is `1a0f4182...`, with `weighting_mode = deterministic_weighted_sampler_sidecar_overlay`
  - `generated_utc`: `2026-05-29T13:50:07Z`

## 3) Fields Contributing To Each Digest
`geometry_mapping_identity_digest` payload fields (same function on both sides):
1. `geometry_schema_version`
2. `sweep_id`
3. `cell_id`
4. `axis_levels`
5. `weighting_mode`

Expected (`e7e440...`) payload:
- identical probe identity and axes
- `weighting_mode = deterministic_weighted_sampler_metadata`

Observed (`1a0f4182...`) payload:
- identical probe identity and axes
- `weighting_mode = deterministic_weighted_sampler_sidecar_overlay`

## 4) Exact Divergence Field(s)
Only one differing field was found:
- `weighting_mode`

All other digest payload fields matched exactly.

## 5) Which Artifacts Contain Each Weighting Mode
Contains `deterministic_weighted_sampler_sidecar_overlay`:
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_resolved_config.json` (`geometry_mapping.weighting_mode`)
- `/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_geometry_probe_mh.config.json` (`geometry_mapping.weighting_mode`)
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_mh/exposure_ledger_declared.json` (`geometry_context.weighting_mode`)

Contains `deterministic_weighted_sampler_metadata`:
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_geometry_context_input.json` (`weighting_mode`)
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_weights_sidecar.json` (`geometry_context.weighting_mode`)
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_declared_exposure.json` (`probe_identity.weighting_mode`)
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_hypothesis.json` (`probe_identity.weighting_mode`)

## 6) Canonical Value For First Live Probe
Canonical weighting mode should be:
- `deterministic_weighted_sampler_sidecar_overlay`

Rationale:
- Approved live runtime package uses sidecar weight source (`geometry_sampling.weight_source.kind=sidecar`).
- Resolved probe configuration for execution explicitly sets sidecar-overlay weighting mode.
- Go/No-Go refresh shifted governance to sidecar-overlay readiness checks.

## 7) Staleness / Cause Determination
Finding: **mixed-context artifact lineage**, not a trainer algorithm defect.

Detailed diagnosis:
- Sidecar is internally consistent, but it was generated from a metadata-mode geometry context input artifact.
- Runtime execution config switched geometry context to sidecar-overlay mode.
- Runtime package digest fields were not recomputed to the sidecar-overlay context (still show `e7e440...`).
- Trainer recomputes digest from `geometry_mapping` at runtime and validates against sidecar digest envelope, causing fail-fast mismatch.

Conclusion:
- Sidecar is stale relative to current canonical runtime context.
- Runtime package digest annotations are also stale relative to its own `geometry_mapping` payload.
- Operationally, this is a cross-artifact context split.
