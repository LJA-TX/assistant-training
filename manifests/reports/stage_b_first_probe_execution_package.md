# Stage B First Live Geometry Probe Execution Package

## Scope
Execution-preparation package only for:

- `sweep_id`: `stage_b_v1_geometry_first_live_probe`
- `cell_id`: `cell_live_mh_nocall_medium_readfile_high_v1`

No training, eval, or detector execution is performed by this package.

## Current Status
- Weight provisioning mode: `probe_specific_overlay_row_identity_rows`.
- Sidecar overlay provisioning is complete and validated.
- Current package state: `READY_FOR_FINAL_HUMAN_GO`.
- Manual authorization remains required before any execution command.

Historical note:
- Previous state before weight provisioning refresh: `NO_GO_PENDING_WEIGHT_COVERAGE_RESOLUTION`.

## Package Artifacts
- Resolved probe configuration:
  - `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_resolved_config.json`
- Declared exposure and drift expectations:
  - `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_declared_exposure.json`
- Go/No-Go summary:
  - `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_go_no_go_summary.json`
- Detector geometry-context input:
  - `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_geometry_context_input.json`
- Weight sidecar overlay:
  - `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_weights_sidecar.json`
- Readiness reassessment:
  - `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_readiness_reassessment.json`

## Probe Configuration Package
Resolved config includes:
- `geometry_mapping` block:
  - `no_call_pressure=medium`
  - `read_file_counterweight=high`
  - `rg_search_contrastive=medium`
  - `uncertainty_conditioning=zero`
- `geometry_sampling` block:
  - `enabled=true`
  - deterministic weighted sampler settings
  - explicit `sampler_seed`
  - sidecar-based weight source contract (`kind=sidecar`)
- Sidecar linkage:
  - `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_weights_sidecar.json`
- Threshold profile linkage:
  - profile id: `stage_b_v1_geometry_mapping_collapse_profile`
  - profile path: `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_threshold_profile.json`
- Digest contract linkage:
  - contract id: `stage_b_v1_digest_contract`
  - contract path: `/opt/ai-stack/assistant-training/manifests/reports/digest_contract_v1.json`

## Dataset / Exposure Package
Declared exposure package:
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_declared_exposure.json`

Sidecar overlay package:
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_weights_sidecar.json`

Validated sidecar readiness:
- `weights_count=1982`
- `positive_weight_rows=13`
- `zero_weight_rows=1969`
- `weights_sum=36.0`
- `row_identity_reference.rows_digest_sha256=1cb0a23a2038bb949b1e1be90b289eb02f1b05b776a8a2a11af44c961a993549`

## Execution Plan (Commands To Run Later, Not Executed Here)
1. Optional static preflight on existing run-manifest tooling:

```bash
python /opt/ai-stack/assistant-training/scripts/preflight_lora_run.py \
  /opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_geometry_probe_mh.run_manifest.json
```

2. Training launch (only after final manual GO):

```bash
/home/roy/.venvs/llama/bin/accelerate launch --num_processes 1 \
  /opt/ai-stack/assistant-training/scripts/train_lora_sft.py \
  --config /opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_geometry_probe_mh.config.json
```

3. Canonical eval execution (base + adapter comparison):

```bash
python /opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py \
  --manifest /opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json \
  --model-name-or-path /mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base \
  --adapter-dir /opt/ai-stack/assistant-training/artifacts/adapters/stage_b_llama31_8b_base_v1_geometry_probe_mh \
  --out-dir /opt/ai-stack/assistant-training/evals/runs/stage_b_v1_geometry_probe_mh_eval
```

4. Collapse detector invocation:

```bash
python /opt/ai-stack/assistant-training/scripts/post_eval_collapse_detector.py \
  --eval-summary /opt/ai-stack/assistant-training/evals/runs/stage_b_v1_geometry_probe_mh_eval/summary.json \
  --threshold-profile /opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_threshold_profile.json \
  --baseline-summary /opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_counterbalanced_probe_canonical_eval_summary.json \
  --geometry-context /opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_geometry_context_input.json \
  --collapse-watch-output /opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_collapse_watch_interpretation.json \
  --gate-assessment-output /opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_gate_assessment.json
```

## Expected Artifacts and Locations
Training/instrumentation outputs (from resolved config run root):
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_mh/resolved_config.json`
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_mh/masking_audit.json`
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_mh/training_summary.json`
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_mh/exposure_ledger_declared.json`
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_mh/exposure_ledger_realized.json`
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_mh/exposure_ledger_drift.json`
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_mh/sampler_determinism_report.json`

Eval outputs:
- `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_geometry_probe_mh_eval/summary.json`
- `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_geometry_probe_mh_eval/comparison_rows.jsonl`

Detector outputs:
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_collapse_watch_interpretation.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_gate_assessment.json`

## Evaluation and Governance Plan
Eval manifest:
- `/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json`

Required baseline:
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_counterbalanced_probe_canonical_eval_summary.json`

Required detector inputs:
- eval summary JSON
- threshold profile JSON
- baseline summary JSON (required for delta rule)
- geometry context JSON (`stage_b_first_probe_geometry_context_input.json`)

Required governance artifacts for review:
- detector outputs (`collapse_watch_interpretation.json`, `gate_assessment.json`)
- exposure ledgers (declared, realized, drift)
- sampler determinism report
- resolved config with typed digest fields
- sidecar overlay artifact and digest checks

## Final Recommendation
`READY_FOR_FINAL_HUMAN_GO`

Interpretation:
- package is aligned and execution-ready at the artifact/governance level,
- explicit human signoff is still required before launch commands are run.
