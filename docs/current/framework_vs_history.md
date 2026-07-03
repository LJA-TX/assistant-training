# Framework Versus History

This repository still mixes reusable framework assets with preserved project history, but the completed Wave 1 separation and completed compatibility adoption slice are now part of the current repository state.

Use this simple rule of thumb:

- if a path defines current behavior, current authority, or current contracts, treat it as framework
- if a path preserves prior runs, prior architecture, or continuity evidence, treat it as history
- if a path is a historical container that still holds active fixtures or compatibility aliases, treat it as mixed and inspect the current boundary carefully

## At A Glance

| Category | What it means | Examples |
| --- | --- | --- |
| Reusable framework or active infrastructure | Current doctrine, contracts, code, tests, and active support surfaces | `../goal_charter_v5a.md`, `../appendix_a_operational_execution_contract_v3a.md`, `../metric_specification_v1a.md`, `../../scripts/train_lora_sft.py`, `../../tests/test_dataset_contract.py` |
| Preserved history or reference material | Prior runs, continuity records, and historical artifacts kept for provenance | `../convergence/`, `../continuity/`, `../deprecated/`, `../../data/v1_0/`, `../../reports/stage_c1/` through `../../reports/stage_c6/` |
| Mixed surface | Historical container that still hosts active fixtures or compatibility aliases | `../../manifests/reports/stage_b_wp8_validation/fixtures/`, `../../manifests/reports/stage_b_v1_threshold_profile.json` |

## Treat As Reusable Framework Or Active Infrastructure

- `../../AGENTS.md`
- `../goal_charter_v5a.md`
- `../appendix_a_operational_execution_contract_v3a.md`
- `../metric_specification_v1a.md`
- `../framework/process_infrastructure/`
- `../framework/lineages/`
- `../framework/methodology/`
- `../../evals/canonical_eval_manifest_v1.json`
- `../../evals/data/canonical_v1/`
- `../../scripts/train_lora_sft.py`
- `../../scripts/preflight_lora_run.py`
- `../../scripts/build_dataset_v1.py`
- `../../scripts/eval_canonical_manifest.py`
- `../../scripts/stage_c1_evaluator_foundation.py`
- `../../scripts/repo_paths.py`
- `../../tests/test_dataset_contract.py`
- `../../tests/test_masking_behavior.py`
- `../../tests/test_eval_canonical_manifest.py`
- `../../tests/test_repo_paths.py`
- `../../tests/test_compatibility_path_resolution.py`
- `../../manifests/reports/stage_b_wp8_validation/fixtures/`
- `../../manifests/reports/stage_b_v1_threshold_profile.json`

Selected convergence documents also remain on the future primary path because they express current status or reusable methodology:

- `status/STAGE_B_COMPLETION_DETERMINATION.md`
- `../framework/methodology/STAGE_BC_PROCESS_EXTRACTION_ASSESSMENT.md`
- `../framework/methodology/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md`
- `../framework/methodology/STAGE_BC_PHASE1_PROCESS_INFRASTRUCTURE_CLOSURE_DETERMINATION.md`
- `../framework/methodology/STAGE_C_PACKAGE_3C_REGIMEN_RETROSPECTIVE_AND_REUSABILITY_ASSESSMENT.md`
- `../framework/methodology/STAGE_C_PACKAGE_5E_DIRECT_ANSWER_LIFECYCLE_RETROSPECTIVE_AND_REGIMEN_GENERALIZATION_ASSESSMENT.md`
- `../framework/methodology/STAGE_C_PACKAGE_6A_FORMAL_BLOCKER_ORIENTED_REGIMEN_BRANCH_ADOPTION_ASSESSMENT.md`
- `../framework/methodology/STAGE_C_PACKAGE_6B_CONDITIONAL_BLOCKER_ORIENTED_BRANCH_ADOPTION_DETERMINATION.md`
- `../framework/methodology/STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md`
- `roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md`
- `../framework/methodology/STAGE_C10C_REFRESHED_DETECTOR_MIGRATION_GATE_DETERMINATION.md`

## Treat As Preserved History Or Reference Material

- bulk `../convergence/` package records not listed above
- `../continuity/`
- `../deprecated/`
- `../../configs/lora/`
- `../../manifests/runs/`
- bulk `../../manifests/reports/` outside active fixture surfaces
- `../../data/v1_0/`
- `../../reports/stage_c1/` through `../../reports/stage_c6/`

Some of these surfaces still have active test or script dependencies. That means they are preserved in place for now even if they are primarily historical.

## Important Current Reality

Current location does not equal future architectural role.

Examples:

- active fixtures currently live under `manifests/reports/`
- sample artifacts currently live under `reports/stage_c*`
- active evaluator and core entrypoint path resolution now runs through `../../scripts/repo_paths.py`
- bulk project execution history remains under `docs/convergence/`, while selected current-state and methodology records now have canonical paths elsewhere

That mixed state is known and intentional during housekeeping preparation.

## Structural Boundary

This page is a navigation aid after the completed Wave 1 move and completed compatibility adoption merge.

Old exact file paths for moved Wave 1 records remain preserved through compatibility aliases.
No history has been archived.
No deletions or pruning are authorized from this separation alone.
