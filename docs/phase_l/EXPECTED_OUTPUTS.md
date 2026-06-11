# Expected Outputs

## If Training Is Later Authorized

The run should create the following surfaces:

- `artifacts/stage_b_llama31_8b_base_v1_phase_l_v1_1_external_first/`
- `artifacts/adapters/stage_b_llama31_8b_base_v1_phase_l_v1_1_external_first/`
- `artifacts/logs/stage_b_llama31_8b_base_v1_phase_l_v1_1_external_first/`

## Expected Training Artifacts

Inside the run root, expect:

- `resolved_config.json`
- `masking_audit.json`
- `training_summary.json`
- `exposure_ledger_declared.json`
- `exposure_row_identity_sidecar.json`
- `exposure_ledger_realized.json`
- `sampler_determinism_report.json`
- `exposure_ledger_drift.json`
- `checkpoints/`

## Expected Evaluation Artifacts

Under the canonical eval output directory, expect:

- `summary.json`
- `comparison_rows.jsonl`

The evaluator writes those files via `scripts/eval_canonical_manifest.py`.

## Expected Review Artifacts

If the run is later elevated into a review bundle, expect a concise report that captures:

- the dataset and config identities
- the canonical evaluation summary
- the delta versus H0, H1, and H2
- the promotion or non-promotion decision

## What Should Not Appear

- merged adapter weights
- modified evaluator code
- modified scorer code
- modified canonical eval data
- unreviewed threshold changes

## Note

No training or evaluation outputs are produced in the current Phase L planning phase.
This file describes the expected surfaces for the later authorized run.
