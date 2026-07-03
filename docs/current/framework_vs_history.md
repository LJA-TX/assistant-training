# Framework Versus History

This repository separates reusable framework assets from curated historical evidence.

Use this simple rule of thumb:

- if a path defines current behavior, current authority, or current contracts, treat it as framework
- if a path preserves prior decisions, transitions, or continuity evidence, treat it as curated history
- if a path is only useful as evidence of how the regimen evolved, keep it on the evidence spine rather than the main instructional path

## At A Glance

| Category | What it means | Examples |
| --- | --- | --- |
| Reusable framework or active infrastructure | Current doctrine, contracts, code, tests, and active support surfaces | `../goal_charter_v5a.md`, `../appendix_a_operational_execution_contract_v3a.md`, `../metric_specification_v1a.md`, `status/GEN2_PROGRAM_CHARTER.md`, `../../scripts/train_lora_sft.py`, `../../tests/test_dataset_contract.py` |
| Curated historical evidence | Selected records that explain how the method evolved and why the current boundary exists | `../framework/lineages/README.md`, `../framework/lineages/i2_contamination_event.md`, `../framework/lineages/i4_i5_overconstraint_collapse.md`, `../framework/lineages/i6_isolated_variable_pivot.md`, `../framework/lineages/i7_coupled_schema_dynamics.md`, `status/STAGE_B_COMPLETION_DETERMINATION.md`, `status/D1_CLOSURE_AND_D2_READINESS_ASSESSMENT.md`, `../housekeeping/OSS_01_INDEPENDENT_REVIEW_AND_RECONCILIATION_GROK.md` |

## Treat As Reusable Framework Or Active Infrastructure

- `../../AGENTS.md`
- `../goal_charter_v5a.md`
- `../appendix_a_operational_execution_contract_v3a.md`
- `../metric_specification_v1a.md`
- `status/GEN2_PROGRAM_CHARTER.md`
- `../framework/process_infrastructure/`
- `../framework/lineages/`
- `../framework/methodology/`
- `../../evals/canonical_eval_manifest_v1.json`
- `../../scripts/build_dataset_v1.py`
- `../../scripts/preflight_lora_run.py`
- `../../scripts/train_lora_sft.py`
- `../../scripts/eval_canonical_manifest.py`
- `../../scripts/stage_c1_evaluator_foundation.py`
- `../../scripts/repo_paths.py`
- `../../tests/test_dataset_contract.py`
- `../../tests/test_masking_behavior.py`
- `../../tests/test_eval_canonical_manifest.py`
- `../../tests/test_repo_paths.py`
- `../../tests/test_compatibility_path_resolution.py`

Selected records that still belong near the main path because they express current status, current strategic framing, or reusable methodology:

- `status/STAGE_B_COMPLETION_DETERMINATION.md`
- `status/D1_CLOSURE_AND_D2_READINESS_ASSESSMENT.md`
- `status/GEN2_PROGRAM_CHARTER.md`
- `status/GEN2_PROSPECTIVE_EVIDENCE_PROGRAM_ASSESSMENT.md`
- `status/GEN2_STRATEGIC_DIRECTION_OPTIONS_ASSESSMENT.md`
- `status/GEN2_SCOPE_BOUNDARY_ASSESSMENT.md`
- `../continuity/D0_BLOCKER_REGISTER.md`
- `../continuity/D0_TO_CURRENT_TREE_MECHANISM_ISOLATION_GOVERNANCE.md`
- `../continuity/D1_GOVERNANCE_FOUNDATION_PACKAGE.md`
- `../continuity/D1_MECHANISM_HYPOTHESIS_INVENTORY.md`
- `../continuity/D1_MECHANISM_HYPOTHESIS_INVENTORY_SPECIFICATION.md`
- `../framework/methodology/STAGE_BC_PHASE1_PROCESS_INFRASTRUCTURE_CLOSURE_DETERMINATION.md`
- `../framework/methodology/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md`
- `../framework/methodology/STAGE_BC_PROCESS_EXTRACTION_ASSESSMENT.md`

## Treat As Curated Historical Evidence

- `../framework/lineages/i2_contamination_event.md`
- `../framework/lineages/i4_i5_overconstraint_collapse.md`
- `../framework/lineages/i6_isolated_variable_pivot.md`
- `../framework/lineages/i7_coupled_schema_dynamics.md`
- `../framework/methodology/STAGE_C10C_REFRESHED_DETECTOR_MIGRATION_GATE_DETERMINATION.md`
- `../framework/methodology/STAGE_C_PACKAGE_3C_REGIMEN_RETROSPECTIVE_AND_REUSABILITY_ASSESSMENT.md`
- `../framework/methodology/STAGE_C_PACKAGE_5E_DIRECT_ANSWER_LIFECYCLE_RETROSPECTIVE_AND_REGIMEN_GENERALIZATION_ASSESSMENT.md`
- `../framework/methodology/STAGE_C_PACKAGE_6A_FORMAL_BLOCKER_ORIENTED_REGIMEN_BRANCH_ADOPTION_ASSESSMENT.md`
- `../framework/methodology/STAGE_C_PACKAGE_6B_CONDITIONAL_BLOCKER_ORIENTED_BRANCH_ADOPTION_DETERMINATION.md`
- `../housekeeping/OSS_01_INDEPENDENT_REVIEW_AND_RECONCILIATION_GROK.md`
- `../housekeeping/OSS_05_PUBLIC_FRONT_DOOR_IMPLEMENTATION_SUMMARY.md`

## Important Current Reality

Current location does not equal future architectural role.

Examples:

- some current-status records are still presented as framework because they define the accepted baseline
- the `docs/current/status/` directory contains both current authority surfaces and historical milestone records, so it should not be classified as historical evidence as a whole
- Stage C closure artifacts remain curated history because they close a completed branch rather than reopen it
- selected historical records are retained because they explain the method, not because they should expand into an archive
- the evidence spine is bounded and thematic, not a dump of everything the project has ever produced

## Structural Boundary

This page is a navigation aid for the curated public package.

No archive formation is implied.
No deletions or pruning are authorized from this separation alone.
