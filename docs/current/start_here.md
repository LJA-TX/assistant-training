# Start Here

Use this page as the fastest useful navigation path into the repository. If you only have a few minutes, read the first three sections and then inspect the quick targets listed below.

## 1. Confirm Current State

Read [current_status.md](current_status.md) for the accepted repository state, the closed Wave 1 and compatibility status, and the current boundary.

## 2. Read The Governing Doctrine

The reusable regimen is governed by:

- [../goal_charter_v5a.md](../goal_charter_v5a.md)
- [../appendix_a_operational_execution_contract_v3a.md](../appendix_a_operational_execution_contract_v3a.md)
- [../metric_specification_v1a.md](../metric_specification_v1a.md)

These are doctrine surfaces, not optional background reading.

## 3. Identify The Reusable Framework

Read [framework_vs_history.md](framework_vs_history.md) to distinguish reusable regimen assets from preserved project history.

The main reusable framework surfaces are:

- [../../AGENTS.md](../../AGENTS.md)
- [../framework/process_infrastructure/](../framework/process_infrastructure/)
- [../framework/lineages/](../framework/lineages/)
- [../framework/methodology/](../framework/methodology/)
- [../../scripts/repo_paths.py](../../scripts/repo_paths.py)
- [status/STAGE_B_COMPLETION_DETERMINATION.md](status/STAGE_B_COMPLETION_DETERMINATION.md)
- [roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md](roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md)
- [../../evals/canonical_eval_manifest_v1.json](../../evals/canonical_eval_manifest_v1.json)
- [../../evals/data/canonical_v1/](../../evals/data/canonical_v1/)
- [../../scripts/train_lora_sft.py](../../scripts/train_lora_sft.py)
- [../../scripts/preflight_lora_run.py](../../scripts/preflight_lora_run.py)
- [../../scripts/build_dataset_v1.py](../../scripts/build_dataset_v1.py)
- [../../scripts/eval_canonical_manifest.py](../../scripts/eval_canonical_manifest.py)

## 3.1 Quick Inspection Targets

If you want the smallest useful inspection set, focus on these files and directories:

- [../goal_charter_v5a.md](../goal_charter_v5a.md): what the repository is trying to do
- [../appendix_a_operational_execution_contract_v3a.md](../appendix_a_operational_execution_contract_v3a.md): how the regimen is governed
- [../metric_specification_v1a.md](../metric_specification_v1a.md): how the canonical evals are scored
- [../../evals/canonical_eval_manifest_v1.json](../../evals/canonical_eval_manifest_v1.json): the pinned evaluation contract
- [../../scripts/build_dataset_v1.py](../../scripts/build_dataset_v1.py): how the dataset and eval corpora are constructed
- [../../scripts/eval_canonical_manifest.py](../../scripts/eval_canonical_manifest.py): how canonical evaluation is scored
- [../../scripts/train_lora_sft.py](../../scripts/train_lora_sft.py): the main training entrypoint
- [../../tests/test_dataset_contract.py](../../tests/test_dataset_contract.py): one concrete contract check

## 4. Check Housekeeping Boundaries

Read [housekeeping_status.md](housekeeping_status.md) before planning any structural repository work.

That page explains:

- which housekeeping documents are accepted authorities
- what Wave 1 and compatibility adoption changed
- what remains out of scope on the current baseline

## 5. Use History Deliberately

Project history remains preserved in its current locations. Use it when you need provenance, methodological evidence, or lineage-specific context.

Primary preserved history surfaces:

- `../convergence/`
- `../continuity/`
- `../deprecated/`
- `../../configs/lora/`
- `../../manifests/runs/`
- `../../manifests/reports/`
- `../../data/v1_0/`
- `../../reports/stage_c1/` through `../../reports/stage_c6/`

## 6. Parked Family Status

The runtime-output / corpus-behavior investigation family is defined but parked.

Planning anchor:

- [roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md](roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md)

Do not treat that family as active implementation work unless a later phase explicitly reactivates it.
