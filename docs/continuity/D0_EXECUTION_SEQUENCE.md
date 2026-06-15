# D0 Execution Sequence

## Purpose

This sequence defines the future read-only order for D0 reconstruction certification once implementation is authorized to execute.

It does not start execution now.

The authorized run directory for a future execution is:

`/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/`

- No reconstruction is run here.
- No datasets are modified here.
- No configs are modified here.
- No manifests are modified here.
- No training is launched here.

## Execution Order

### Stage 0: Authority lock

Inputs:

- `/opt/ai-stack/assistant-training/docs/continuity/D0_RECONSTRUCTION_AUTHORITY_MATRIX.md`
- `/opt/ai-stack/assistant-training/docs/continuity/D0_RECONSTRUCTION_IMPLEMENTATION_PLAN.md`
- `/opt/ai-stack/assistant-training/docs/continuity/D0_VALIDATION_CHECKLIST.md`
- `/opt/ai-stack/assistant-training/docs/continuity/D0_ACCEPTANCE_CRITERIA.md`
- `/opt/ai-stack/assistant-training/docs/continuity/D0_HASH_AUTHORITY_VERIFICATION.md`

Actions:

1. resolve the authority matrix
2. resolve hash precedence
3. resolve the allowed output root
4. freeze the execution snapshot id

Stop condition:

- any authority conflict or unresolved precedence question

### Stage 1: Source snapshot and inventory

Inputs:

- all source artifact paths listed in the implementation plan

Actions:

1. enumerate every required source artifact
2. compute raw-byte hashes
3. capture artifact roles
4. record blocking vs non-blocking status

Outputs:

- `/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/inventory/source_artifact_inventory.json`
- `/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/ledgers/hash_ledger.json`
- optional human-readable mirrors

Stop condition:

- any required source artifact missing or any hash mismatch

### Stage 2: Row ledger generation

Inputs:

- `i3` train and val JSONL
- `H0` control JSONL reference
- `H1` train and val JSONL
- `H2` train and val JSONL

Actions:

1. parse each JSONL row without reserialization normalization
2. emit row positions and identity keys
3. compute row payload hashes
4. tag each row with a surface id and split id

Outputs:

- `/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/ledgers/row_ledger.jsonl`

Stop condition:

- any row identity gap, duplicate, or order drift

### Stage 3: `i3` scaffold certification

Inputs:

- `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl`
- `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_val.jsonl`
- `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_summary.json`

Actions:

1. verify the control train hash
2. verify the control val hash
3. verify row counts and order
4. verify the control summary matches the ledger
5. seed the cumulative dataset integrity report with the `i3` control entry

Outputs:

- `/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/reports/dataset_integrity_report.json`

Stop condition:

- any mismatch with the published control summary or published hashes

### Stage 4: H0 control certification

Inputs:

- `/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_i3.config.json`
- `/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.config.json`
- `/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_i3.run_manifest.json`
- `/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.run_manifest.json`

Actions:

1. certify the `i3 -> H0` config diff
2. certify the `i3 -> H0` manifest diff
3. verify that H0 reuses the control scaffold bytes
4. append the H0 control entry to the cumulative dataset integrity report
5. seed the cumulative diff certification files with the `i3__H0` pair

Outputs:

- `/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/diffs/config_diff_certification.json`
- `/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/diffs/manifest_diff_certification.json`
- `/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/reports/dataset_integrity_report.json`

Stop condition:

- any config or manifest delta outside the certified field set

### Stage 5: H1 certification

Inputs:

- `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_train.jsonl`
- `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_val.jsonl`
- `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_summary.json`
- `/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.config.json`
- `/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.run_manifest.json`

Actions:

1. verify H1 file hashes
2. verify patch size and replacement positions
3. verify patch-by-tool accounting
4. certify the `H0 -> H1` config and manifest diffs
5. verify H1 val remains control-bytes identical
6. append the H1 entry to the cumulative dataset integrity report
7. append the `H0__H1` pair to the cumulative diff certification files

Outputs:

- `/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/reports/dataset_integrity_report.json`
- `/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/reports/patch_accounting_report.json`
- `/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/reports/tool_family_distribution_report.json`
- `/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/diffs/config_diff_certification.json`
- `/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/diffs/manifest_diff_certification.json`

Stop condition:

- any patch, distribution, or diff mismatch

### Stage 6: H2 certification

Inputs:

- `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_train.jsonl`
- `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_val.jsonl`
- `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_summary.json`
- `/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.config.json`
- `/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.run_manifest.json`

Actions:

1. verify H2 file hashes
2. verify patch size and replacement positions
3. verify patch-by-tool accounting
4. certify the `H1 -> H2` config and manifest diffs
5. verify H2 val remains control-bytes identical
6. append the H2 entry to the cumulative dataset integrity report
7. append the `H1__H2` pair to the cumulative diff certification files

Outputs:

- `/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/reports/dataset_integrity_report.json`
- `/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/reports/patch_accounting_report.json`
- `/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/reports/tool_family_distribution_report.json`
- `/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/diffs/config_diff_certification.json`
- `/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/diffs/manifest_diff_certification.json`

Stop condition:

- any patch, distribution, or diff mismatch

### Stage 7: Eval-surface fidelity

Inputs:

- `/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json`
- `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_phase_i_h0_control_i3_micro_eval_20260611T103048Z/summary.json`
- `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_phase_i_h1_diversity_patch_eval_20260611T125835Z/summary.json`
- `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_phase_i_h2_commitment_patch_eval_20260611T120228Z/summary.json`
- the corresponding `comparison_rows.jsonl` files
- the published bundle manifests under `evals/baselines/llama31/internal_reference_regimes/`

Actions:

1. verify decode defaults
2. verify split hashes
3. verify script hashes
4. verify environment snapshot and dependency lock hashes
5. verify bundle artifact surfaces

Output:

- `/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/reports/eval_surface_fidelity_report.json`

Stop condition:

- any canonical-contract drift

### Stage 8: Missing artifact report

Inputs:

- all previous stages

Actions:

1. list any absent required source artifact
2. separate blocking gaps from non-blocking future outputs
3. record whether implementation is currently blocked

Output:

- `/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/reports/missing_artifact_report.json`

Stop condition:

- any required source artifact missing

### Stage 9: Acceptance summary

Inputs:

- all generated reports and ledgers

Actions:

1. aggregate gate statuses
2. record blocking failures
3. record non-blocking observations
4. mark readiness for future execution or blocked status

Output:

- `/opt/ai-stack/assistant-training/artifacts/d0_reconstruction_verification/runs/<run_id>/reports/acceptance_summary.json`

Stop condition:

- none; this is the closeout step

## Execution Guarantees

The future run must be:

- read-only with respect to source artifacts
- deterministic with respect to ordered inputs
- fail-fast on any fatal mismatch
- non-repairing and non-inferential

## Current Implementation Status

No execution has occurred yet.

No blocking repository artifact gaps are currently known.
