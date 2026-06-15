# D0 Reconstruction Implementation Plan

## Objective

Prepare a reconstruction-verification package for:

- `i3` scaffold
- `H0`
- `H1`
- `H2`

This is planning only.

- Do not execute reconstruction.
- Do not modify datasets.
- Do not train.
- Do not create new experimental arms.

## Required Inputs

Use the following source artifact families as the implementation inputs:

- Control and treatment JSONL datasets plus summaries under `/opt/ai-stack/assistant-training/data/v1_0/`
- Final configs under `/opt/ai-stack/assistant-training/configs/lora/`
- Final run manifests under `/opt/ai-stack/assistant-training/manifests/runs/`
- Canonical eval manifest and executed eval bundles under `/opt/ai-stack/assistant-training/evals/`
- Published baseline package manifests under `/opt/ai-stack/assistant-training/evals/baselines/llama31/`
- Governance and closure notes under `/opt/ai-stack/assistant-training/docs/`

## Required Output Artifacts

The D0 implementation package must be able to produce, or already contain links to, the following certification outputs:

1. source artifact inventory
2. hash ledger
3. row ledger
4. dataset integrity report
5. patch accounting report
6. tool-family distribution report
7. field-level config diff certification
8. field-level manifest diff certification
9. eval-surface fidelity report
10. missing-artifact report
11. acceptance summary

## Implementation Sequence

### 1. Lock authority

- Confirm the authority matrix before any comparison work.
- Treat canonical contracts and machine-readable source artifacts as primary.
- Treat prose reports and continuity notes as secondary.

### 2. Inventory the source surfaces

- Enumerate the exact paths for `i3`, `H0`, `H1`, and `H2`.
- Record hashes for every source JSONL, config, manifest, summary, and executed eval bundle.
- Mark any absent required artifact as blocking.
- Record row identity keys explicitly, including `source_case_id`, `phase_i_parent_case_id`, `phase_i_variant`, and `phase_i_patch_slot` where applicable.

### 3. Verify the `i3` scaffold

- Confirm the `i3` train and val bytes match the published hashes.
- Confirm row counts and row ordering match the published `i3` summary.
- Confirm the control scaffold remains the source comparator for `H0`.

### 4. Verify `H0`

- Confirm `H0` is a metadata-only reconstruction of the `i3` control bytes.
- Confirm `H0` config and manifest differ from `i3` only by the certified fields listed below.
- Confirm no dataset mutation exists beyond the shared control bytes.

### 5. Verify `H1`

- Confirm the patch size is exactly `100`.
- Confirm the published replacement positions, row counts, and tool-family counts match the summary.
- Confirm the H1 train and val file hashes match the published values.
- Confirm H1 config and manifest diffs versus H0 are limited to the certified fields below.

### 6. Verify `H2`

- Confirm the patch size is exactly `100`.
- Confirm the published replacement positions, row counts, and tool-family counts match the summary.
- Confirm the H2 train and val file hashes match the published values.
- Confirm H2 config and manifest diffs versus H1 are limited to the certified fields below.

### 7. Certify field-level diffs

The final D0 report must enumerate every difference between the following pairs.

#### i3 -> H0 config diff

Certified differences:

- `generated_utc`
- `lineage` added
- `name`
- `optimization.num_train_epochs`
- `outputs.adapter_output_dir`
- `outputs.logs_dir`
- `outputs.run_root`
- `purpose`
- `scaffold_notes` added

#### i3 -> H0 manifest diff

Certified differences:

- `behavioral_review_package` added
- `canonical_eval_run` added
- `canonical_eval_summary` added
- `collapse_watch_interpretation` added
- `config_path`
- `expected_outputs.adapter_output_dir`
- `expected_outputs.logs_dir`
- `expected_outputs.run_root`
- `gate_assessment` added
- `generated_utc`
- `inputs.dataset_leakage_report` removed
- `inputs.phase_i_control_surface_verification` added
- `inputs.phase_i_dataset_variant_validation` added
- `inputs.phase_i_journal` added
- `name`
- `review_gate.approved_by`
- `review_gate.approved_utc`
- `scaffold_notes` added

#### H0 -> H1 config diff

Certified differences:

- `dataset.train_jsonl`
- `dataset.val_jsonl`
- `lineage.intervention_scope`
- `name`
- `outputs.adapter_output_dir`
- `outputs.logs_dir`
- `outputs.run_root`
- `purpose`

#### H0 -> H1 manifest diff

Certified differences:

- `config_path`
- `expected_outputs.adapter_output_dir`
- `expected_outputs.logs_dir`
- `expected_outputs.run_root`
- `inputs.dataset_manifest`
- `inputs.train_jsonl`
- `inputs.val_jsonl`
- `name`

#### H1 -> H2 config diff

Certified differences:

- `dataset.train_jsonl`
- `dataset.val_jsonl`
- `lineage.intervention_scope`
- `name`
- `outputs.adapter_output_dir`
- `outputs.logs_dir`
- `outputs.run_root`
- `purpose`

#### H1 -> H2 manifest diff

Certified differences:

- `config_path`
- `expected_outputs.adapter_output_dir`
- `expected_outputs.logs_dir`
- `expected_outputs.run_root`
- `inputs.dataset_manifest`
- `inputs.train_jsonl`
- `inputs.val_jsonl`
- `name`

Any additional field delta is a certification failure.

### 8. Assemble the implementation package

Bundle the final D0 package as:

- authority matrix
- implementation plan
- validation checklist
- acceptance criteria
- missing-artifact report

## Blocking Gaps

No blocking repository artifact gaps are currently identified in the present snapshot.

If any of the following were missing, implementation would be blocked:

- `evals/canonical_eval_manifest_v1.json`
- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_val.jsonl`
- `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_train.jsonl`
- `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_val.jsonl`
- `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_train.jsonl`
- `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_val.jsonl`
- the final configs and manifests for `H0`, `H1`, and `H2`
- the published H1 and H2 bundle manifests
- the executed eval summaries and comparison rows for `H0`, `H1`, and `H2`
