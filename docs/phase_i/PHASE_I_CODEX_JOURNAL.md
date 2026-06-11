# Phase I Codex Journal

Purpose: record Phase I execution progress, validations, and stop-rule decisions for the bounded internal proving experiment.

## 2026-06-11

- Classified the request as Phase I execution work under `docs/Phase_I_Work_packages.md`.
- Confirmed the controlling Phase H bundle, the frozen-surface constraints, and the required Mini execution package.
- Verified the current repo state before new work: the repo started with the untracked Phase I work-package prompt plus the expected Phase H bundle artifacts.
- Reviewed the Phase H control surfaces and the microprobe template config, train script, and canonical eval script.
- Confirmed the control dataset shape: `dataset_v1_0_stage_b_recovery_i3_train.jsonl` has `2160` rows and `dataset_v1_0_stage_b_recovery_i3_val.jsonl` has `240` rows.
- Built a new Phase I dataset-variant builder at `scripts/build_phase_i_variants.py`.
- Compiled the builder with `python -m py_compile scripts/build_phase_i_variants.py` and got a clean result.
- Executed `python scripts/build_phase_i_variants.py` successfully.
- Generated the bounded Phase I treatment datasets, validation summaries, and draft execution assets:
  - `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_train.jsonl`
  - `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_val.jsonl`
  - `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_summary.json`
  - `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_train.jsonl`
  - `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_val.jsonl`
  - `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_summary.json`
  - `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.config.draft.json`
  - `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.config.draft.json`
  - `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.config.draft.json`
  - `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.run_manifest.draft.json`
  - `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.run_manifest.draft.json`
  - `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.run_manifest.draft.json`
- Re-ran the builder after wiring the draft config and run-manifest emission so the execution assets now match the generated datasets.
- Validated that both treatment variants preserve:
  - the full train row count (`2160`),
  - the full val row count (`240`),
  - the non-tool slices unchanged,
  - and zero overlap with `heldout_validation` and `tool_holdout`.
- Recorded the H1 patch shape: `100` tool-positive replacements distributed across `git_diff`, `list_active_ports`, `list_dir`, `list_models`, `move_path`, and `write_file`.
- Recorded the H2 patch shape: `100` tool-positive replacements targeted at anchor-heavy control rows with paraphrased prompt surfaces.
- Checked the variant summaries for the expected hard-stop surfaces. No contamination hit the holdout/tool-holdout gates, and the build did not trip a stop rule.
- Logged the remaining work:
  - execute the first-screen runs in the Phase H order,
  - capture the comparison metrics immediately after each run,
  - and apply the Phase H decision gates without redesigning the experiment.
- Verified the execution gate inputs before training:
  - frozen surfaces remained unchanged,
  - dataset hashes matched the Phase I records,
  - contamination remained clean on the holdout and tool-holdout gates,
  - and the H0/H1/H2 assets only differed in approved run-state and variant-specific fields.
- Promoted the draft configs and run manifests to execution assets:
  - `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.config.json`
  - `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.config.json`
  - `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.config.json`
  - `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.run_manifest.json`
  - `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.run_manifest.json`
  - `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.run_manifest.json`
- Opened the execution gate and recorded the approval in `docs/phase_i/EXECUTION_GATE_APPROVAL.md`.
- Confirmed the planned run roots, adapter roots, and log roots are currently missing, so the first runs can start without overwrite flags.

## Commands Executed

- `git status --short --branch`
- `sha256sum evals/canonical_eval_manifest_v1.json scripts/train_lora_sft.py scripts/eval_canonical_manifest.py configs/lora/stage_b_llama31_8b_base_v1_i10r_microprobe.config.json data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl data/v1_0/dataset_v1_0_stage_b_recovery_i3_val.jsonl`
- `wc -l data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl data/v1_0/dataset_v1_0_stage_b_recovery_i3_val.jsonl data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_train.jsonl data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_train.jsonl`
- `python -m py_compile scripts/build_phase_i_variants.py`
- `python scripts/build_phase_i_variants.py`
- `git diff --check`
- `python -m py_compile scripts/build_phase_i_variants.py`
- `sha256sum data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_train.jsonl data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_val.jsonl data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_train.jsonl data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_val.jsonl data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl data/v1_0/dataset_v1_0_stage_b_recovery_i3_val.jsonl`
- `diff -u <(jq 'del(.generated_utc,.safety.do_not_start_training_automatically,.safety.approved_to_run,.scaffold_notes.execution_state,.scaffold_notes.gate_opened)' configs/lora/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.config.draft.json) <(jq 'del(.generated_utc,.safety.do_not_start_training_automatically,.safety.approved_to_run,.scaffold_notes.execution_state,.scaffold_notes.gate_opened)' configs/lora/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.config.json)`
- `diff -u <(jq 'del(.generated_utc,.status,.config_path,.review_gate.approved_to_run,.review_gate.approved_by,.review_gate.approved_utc,.scaffold_notes.implementation_phase,.scaffold_notes.gate_opened)' manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.run_manifest.draft.json) <(jq 'del(.generated_utc,.status,.config_path,.review_gate.approved_to_run,.review_gate.approved_by,.review_gate.approved_utc,.scaffold_notes.implementation_phase,.scaffold_notes.gate_opened)' manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.run_manifest.json)`
- `test -e artifacts/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro`
- `test -e artifacts/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch`
- `test -e artifacts/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch`

## Validation Performed

- Verified that the Phase I builder compiles.
- Verified that both treatment variants stay within the declared 80-to-120 row patch envelope.
- Verified that the train and val row counts remain frozen relative to the control.
- Verified that non-tool slices are byte-for-byte unchanged in the generated train variants.
- Verified that `heldout_validation` and `tool_holdout` contamination overlap remains zero in both treatment variants.
- Verified that `git diff --check` passed cleanly after the full Phase I asset emission.
- Verified that the promoted execution configs differ from the drafts only in approved run-state fields plus the execution file names.
- Verified that the promoted execution run manifests differ from the drafts only in approved run-state fields plus the execution file names.
- Verified that the planned artifact roots do not already exist.

## Stop-Rule Decisions

- No Phase H stop rule tripped during the dataset-preparation slice.
- No Phase H stop rule tripped during the execution-gate verification slice.
- No contamination or repository anomaly required escalation.
- No methodology redesign was requested or introduced.

## Escalation Decisions

- None yet.
- The next escalation point will be the first-screen execution results, not the dataset-preparation slice.
