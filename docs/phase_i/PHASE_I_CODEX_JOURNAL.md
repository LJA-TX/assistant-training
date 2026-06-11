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
- Executed the H0 training run successfully after fixing the local runtime package set (`bitsandbytes` and `transformers`).
- Ran the H0 canonical evaluator with the approved local base-model mirror and the correct adapter output directory.
- Captured the H0 checkpoint metrics and found a hard-stop regression on the adversarial no-call invariant.
- Stopped the first-screen sequence after H0 and did not launch H2 or H1.
- Wrote the H0 checkpoint report at `docs/phase_i/H0_CHECKPOINT_REPORT.md`.
- Recorded the earlier H0 infrastructure blockers and recoveries:
  - missing `bitsandbytes` package,
  - `transformers` 5.x incompatible with the frozen trainer surface,
  - stale partial H0 artifacts requiring cleanup before retry,
  - canonical eval base-model path override to the local mirror,
  - canonical eval adapter-path correction from run root to adapter output.

## 2026-06-11 Resumed Continuation Authority Review

- Reviewed `docs/phase_i/PHASE_H_GATE_REVIEW_AND_PHASE_I_CONTINUATION_DETERMINATION.md` as the controlling authority for resumed Phase I execution.
- Reviewed the supporting continuation-review artifacts:
  - `docs/phase_i/Phase_I_H0_Hard_Stop_Assessment_Grok-Build.md`
  - `docs/phase_i/Phase_I_H0_Hard_Stop_Assessment_GB-Composer.md`
- Re-verified the treatment asset surfaces against their draft counterparts:
  - the H1 and H2 config diffs collapse to approved run-state and approval metadata only,
  - the H1 and H2 run-manifest diffs collapse to approved run-state and approval metadata only,
  - the treatment datasets keep the frozen row counts and holdout contamination gates intact,
  - and the published dataset hashes match the Phase I records.
- Reconfirmed the H1 and H2 treatment hashes:
  - H1 train `fb488f828b9ff42f2c067031ae4e7d65edecd791420c2d6daf79e27422e4e947`
  - H1 val `d1bde5c675e22a88df250ac91e13522bb4d9ff8685d86e3b885f6d8d106d661f`
  - H2 train `41834b7dd1b06bf90bfdb38b77c15f67a3dfdab802d164b0edddfcc686a75fd5`
  - H2 val `d1bde5c675e22a88df250ac91e13522bb4d9ff8685d86e3b885f6d8d106d661f`
- Recorded the continuation authority inventory in `docs/phase_i/CONTINUATION_AUTHORITY_RECORD.md`.
- Confirmed the resumed execution scope is still limited to `H2_commitment_patch` and `H1_diversity_patch` as diagnostic/report-only probes.

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
- `python scripts/train_lora_sft.py --config configs/lora/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.config.json`
- `python -m pip install -U 'bitsandbytes>=0.46.1'`
- `python -m pip install -U 'transformers==4.57.3'`
- `python scripts/eval_canonical_manifest.py --manifest evals/canonical_eval_manifest_v1.json --model-name-or-path /mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base --adapter-dir artifacts/adapters/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro --out-dir evals/runs/stage_b_v1_phase_i_h0_control_i3_micro_eval_20260611T103048Z`

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
- Verified that the H0 training run completed successfully.
- Verified that the H0 canonical eval completed successfully with the correct adapter path and base-model mirror.
- Verified that the H0 adapter violates the Phase H no-call/adversarial invariant.

## Stop-Rule Decisions

- No Phase H stop rule tripped during the dataset-preparation slice.
- No Phase H stop rule tripped during the execution-gate verification slice.
- Phase H kill metric tripped during the H0 checkpoint (`adversarial no_call_correctness = 0.75`).
- The first-screen sequence halted after H0.
- No contamination or repository anomaly required escalation.
- No methodology redesign was requested or introduced.

## Escalation Decisions

- Escalated to runtime/evaluation remediation after H0.
- The next step is external remediation or revalidation, not more internal runs.
