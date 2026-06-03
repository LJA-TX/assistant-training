# Stage B Successor Live Geometry Probe Execution Package

## Scope
Execution-preparation package only for:

- `sweep_id`: `stage_b_v1_geometry_successor_probe`
- `cell_id`: `cell_live_lh_nocall_low_readfile_high_v1`

No training, eval, or detector execution is performed by this package.

## Current Status
- Weight provisioning mode: `probe_specific_overlay_row_identity_rows`.
- Sidecar overlay provisioning is complete and validated.
- Restored detector-facing metric surfaces are now the required raw-summary contract.
- Current package state: `READY_PENDING_MANUAL_GO`.
- Explicit human authorization is still required before any launch command is run.

## Package Artifacts
- Successor design:
  - `/opt/ai-stack/assistant-training/manifests/reports/stage_b_successor_probe_design.md`
- Resolved probe configuration:
  - `/opt/ai-stack/assistant-training/manifests/reports/stage_b_successor_probe_resolved_config.json`
- Declared exposure and drift expectations:
  - `/opt/ai-stack/assistant-training/manifests/reports/stage_b_successor_probe_declared_exposure.json`
- Go/No-Go summary:
  - `/opt/ai-stack/assistant-training/manifests/reports/stage_b_successor_probe_go_no_go_summary.json`
- Detector geometry-context input:
  - `/opt/ai-stack/assistant-training/manifests/reports/stage_b_successor_probe_geometry_context_input.json`
- Weight sidecar overlay:
  - `/opt/ai-stack/assistant-training/manifests/reports/stage_b_successor_probe_weights_sidecar.json`
- Success criteria:
  - `/opt/ai-stack/assistant-training/manifests/reports/stage_b_successor_probe_success_criteria.json`

## Probe Configuration Package
Resolved config includes:
- `geometry_mapping` block:
  - `no_call_pressure=low`
  - `read_file_counterweight=high`
  - `rg_search_contrastive=low`
  - `uncertainty_conditioning=zero`
- `geometry_sampling` block:
  - `enabled=true`
  - deterministic weighted sampler settings
  - explicit `sampler_seed`
  - sidecar-based weight source contract (`kind=sidecar`)
- Sidecar linkage:
  - `/opt/ai-stack/assistant-training/manifests/reports/stage_b_successor_probe_weights_sidecar.json`
- Threshold profile linkage:
  - profile id: `stage_b_v1_geometry_mapping_collapse_profile`
  - profile path: `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_threshold_profile.json`
- Digest contract linkage:
  - contract id: `stage_b_v1_digest_contract`
  - contract path: `/opt/ai-stack/assistant-training/manifests/reports/digest_contract_v1.json`

## Dataset / Exposure Package
Declared exposure package:
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_successor_probe_declared_exposure.json`

Sidecar overlay package:
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_successor_probe_weights_sidecar.json`

Validated sidecar readiness:
- `weights_count=1982`
- `positive_weight_rows=13`
- `zero_weight_rows=1969`
- `weights_sum=30.0`
- `row_identity_reference.rows_digest_sha256=f6e00d5e8a74e63e7e0c73c71b91dddcdc8cbc443e69467362f87200363de4ae`

## Execution Plan (Commands To Run Later, Not Executed Here)
1. Optional static preflight on existing run-manifest tooling:

```bash
python /opt/ai-stack/assistant-training/scripts/preflight_lora_run.py \
  /opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_geometry_probe_lh.run_manifest.json
```

2. Training launch (only after final manual GO):

```bash
/home/roy/.venvs/llama/bin/accelerate launch --num_processes 1 \
  /opt/ai-stack/assistant-training/scripts/train_lora_sft.py \
  --config /opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_geometry_probe_lh.config.json
```

3. Canonical eval execution (base + adapter comparison):

```bash
python /opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py \
  --manifest /opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json \
  --model-name-or-path /mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base \
  --adapter-dir /opt/ai-stack/assistant-training/artifacts/adapters/stage_b_llama31_8b_base_v1_geometry_probe_lh \
  --out-dir /opt/ai-stack/assistant-training/evals/runs/stage_b_v1_geometry_probe_lh_eval
```

4. Collapse detector invocation:

```bash
python /opt/ai-stack/assistant-training/scripts/post_eval_collapse_detector.py \
  --eval-summary /opt/ai-stack/assistant-training/evals/runs/stage_b_v1_geometry_probe_lh_eval/summary.json \
  --threshold-profile /opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_threshold_profile.json \
  --baseline-summary /opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_counterbalanced_probe_canonical_eval_summary.json \
  --geometry-context /opt/ai-stack/assistant-training/manifests/reports/stage_b_successor_probe_geometry_context_input.json \
  --collapse-watch-output /opt/ai-stack/assistant-training/manifests/reports/stage_b_successor_probe_collapse_watch_interpretation.json \
  --gate-assessment-output /opt/ai-stack/assistant-training/manifests/reports/stage_b_successor_probe_gate_assessment.json
```

## Expected Artifacts and Locations
Training/instrumentation outputs:
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_lh/resolved_config.json`
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_lh/masking_audit.json`
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_lh/training_summary.json`
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_lh/exposure_ledger_declared.json`
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_lh/exposure_ledger_realized.json`
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_lh/exposure_ledger_drift.json`
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_lh/sampler_determinism_report.json`

Eval outputs:
- `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_geometry_probe_lh_eval/summary.json`
- `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_geometry_probe_lh_eval/comparison_rows.jsonl`

Detector outputs:
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_successor_probe_collapse_watch_interpretation.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_successor_probe_gate_assessment.json`

## Final Recommendation
`READY_PENDING_MANUAL_GO`

Interpretation:
- the successor package is internally aligned and launch-prepared at the artifact level,
- launch must remain blocked until explicit human authorization is recorded.
