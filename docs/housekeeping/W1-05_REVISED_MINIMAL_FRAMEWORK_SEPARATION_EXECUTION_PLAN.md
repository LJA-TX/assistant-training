# W1-05 Revised Minimal Framework Separation Execution Plan

## Work Package

- ID: `W1-05`
- Title: `Revised Minimal Framework Separation Execution Plan`
- Repository: `/opt/ai-stack/assistant-training`
- Scope: planning only
- Authority basis:
  - `docs/housekeeping/W1-02_MINIMAL_FRAMEWORK_SEPARATION_IMPLEMENTATION_PLAN.md`
  - `docs/housekeeping/W1-03_WAVE_1_EXECUTION_READINESS_AND_INDEPENDENT_RISK_REVIEW.md`
  - `docs/housekeeping/W1-04_WAVE_1_EXECUTION_BLOCKER_RESOLUTION_ASSESSMENT.md`
- Out of scope:
  - implementation
  - file movement
  - restructuring
  - archive creation
  - code changes
  - doctrine changes

## Current-State Basis

- W1-02 established the original Wave 1 execution plan.
- W1-03 rejected execution of W1-02 as written.
- W1-04 defined the minimum blocker-resolution set required to recover Wave 1.
- W1-05 replaces W1-02 as the controlling execution-plan draft for final authorization review.

## Correction Principles

This revised plan applies four corrections:

1. shrink the moved convergence set to H-01 primary records only
2. treat `AGENTS.md` as a live hard consumer
3. replace directory-level redirect language with exact-file alias requirements
4. complete convergence-index coverage for every moved primary convergence record

## A. Revised Move Inventory

### Retained Move Set

#### Directory Moves

| Source | Target | Role |
|---|---|---|
| `docs/process_infrastructure/` | `docs/framework/process_infrastructure/` | primary reusable process assets |
| `docs/lineages/` | `docs/framework/lineages/` | primary reusable methodology assets |

#### Primary Convergence And Current-State File Moves

| Source | Revised target | Role |
|---|---|---|
| `docs/convergence/STAGE_B_COMPLETION_DETERMINATION.md` | `docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md` | current-state completion marker |
| `docs/convergence/STAGE_BC_PROCESS_EXTRACTION_ASSESSMENT.md` | `docs/framework/methodology/STAGE_BC_PROCESS_EXTRACTION_ASSESSMENT.md` | reusable process methodology |
| `docs/convergence/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md` | `docs/framework/methodology/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md` | reusable process methodology |
| `docs/convergence/STAGE_BC_PHASE1_PROCESS_INFRASTRUCTURE_CLOSURE_DETERMINATION.md` | `docs/framework/methodology/STAGE_BC_PHASE1_PROCESS_INFRASTRUCTURE_CLOSURE_DETERMINATION.md` | reusable framework closure record |
| `docs/convergence/STAGE_C_PACKAGE_3C_REGIMEN_RETROSPECTIVE_AND_REUSABILITY_ASSESSMENT.md` | `docs/framework/methodology/STAGE_C_PACKAGE_3C_REGIMEN_RETROSPECTIVE_AND_REUSABILITY_ASSESSMENT.md` | reusable regimen assessment |
| `docs/convergence/STAGE_C_PACKAGE_5E_DIRECT_ANSWER_LIFECYCLE_RETROSPECTIVE_AND_REGIMEN_GENERALIZATION_ASSESSMENT.md` | `docs/framework/methodology/STAGE_C_PACKAGE_5E_DIRECT_ANSWER_LIFECYCLE_RETROSPECTIVE_AND_REGIMEN_GENERALIZATION_ASSESSMENT.md` | reusable regimen assessment |
| `docs/convergence/STAGE_C_PACKAGE_6A_FORMAL_BLOCKER_ORIENTED_REGIMEN_BRANCH_ADOPTION_ASSESSMENT.md` | `docs/framework/methodology/STAGE_C_PACKAGE_6A_FORMAL_BLOCKER_ORIENTED_REGIMEN_BRANCH_ADOPTION_ASSESSMENT.md` | reusable branch-adoption assessment |
| `docs/convergence/STAGE_C_PACKAGE_6B_CONDITIONAL_BLOCKER_ORIENTED_BRANCH_ADOPTION_DETERMINATION.md` | `docs/framework/methodology/STAGE_C_PACKAGE_6B_CONDITIONAL_BLOCKER_ORIENTED_BRANCH_ADOPTION_DETERMINATION.md` | reusable branch-adoption determination |
| `docs/convergence/STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md` | `docs/framework/methodology/STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md` | reusable transition assessment |
| `docs/convergence/STAGE_C10C_REFRESHED_DETECTOR_MIGRATION_GATE_DETERMINATION.md` | `docs/framework/methodology/STAGE_C10C_REFRESHED_DETECTOR_MIGRATION_GATE_DETERMINATION.md` | reusable migration-gate determination |
| `docs/convergence/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md` | `docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md` | parked investigation-family roadmap anchor |

### Removed Move Candidates

The following W1-02 move candidates are removed from Wave 1 scope and remain in place:

1. `docs/convergence/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN_ACCEPTANCE_ASSESSMENT.md`
2. `docs/convergence/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN_IMPLEMENTATION_SUMMARY.md`

Reason:

- they are companion records, not H-01 primary framework/current-state records
- keeping them in place avoids expanding Wave 1 into reference-layer cleanup

### Revised Non-Move Support Surfaces

The following surfaces are not moved structurally, but are explicitly part of the execution package:

1. `AGENTS.md`
2. `README.md`
3. `docs/current/start_here.md`
4. `docs/current/framework_vs_history.md`
5. `docs/current/current_status.md`
6. `docs/current/housekeeping_status.md`
7. `docs/housekeeping/indexes/convergence_history_index.json`
8. `docs/housekeeping/indexes/index_registry.json`

### Revised Current-Path Targets

The revised target layout for primary moved content is:

1. process assets under `docs/framework/process_infrastructure/`
2. lineage assets under `docs/framework/lineages/`
3. methodology synthesis under `docs/framework/methodology/`
4. current status records under `docs/current/status/`
5. parked investigation roadmap records under `docs/current/roadmap/`

## B. AGENTS.md Migration Treatment

### Touched Surfaces

The revised execution package must explicitly touch:

1. `AGENTS.md`
2. all `17` route-asset files currently referenced by `AGENTS.md`
3. the new canonical target files for those same `17` route assets under `docs/framework/process_infrastructure/`

### Required AGENTS.md Treatment

Execution treatment:

1. update all canonical route-asset references in `AGENTS.md` from `docs/process_infrastructure/...` to `docs/framework/process_infrastructure/...`
2. preserve exact old paths through file-level alias coverage
3. do not change route semantics, route names, authority order, or dispatcher behavior

### Route-Asset Verification

Route-asset verification must cover:

1. pre-flight checklist asset references at [AGENTS.md](/opt/ai-stack/assistant-training/AGENTS.md:28)
2. every route-table asset reference at [AGENTS.md](/opt/ai-stack/assistant-training/AGENTS.md:36)

The exact route-asset set is:

1. `docs/process_infrastructure/checklists/git_ignore_verification_checklist.md`
2. `docs/process_infrastructure/checklists/governance_boundary_verification_checklist.md`
3. `docs/process_infrastructure/checklists/hygiene_review_checklist.md`
4. `docs/process_infrastructure/checklists/publication_readiness_checklist.md`
5. `docs/process_infrastructure/checklists/push_readiness_checklist.md`
6. `docs/process_infrastructure/checklists/review_package_completeness_checklist.md`
7. `docs/process_infrastructure/checklists/validation_evidence_checklist.md`
8. `docs/process_infrastructure/checklists/zip_workflow_checklist.md`
9. `docs/process_infrastructure/templates/closure_determination_template.md`
10. `docs/process_infrastructure/templates/conformance_report_template.md`
11. `docs/process_infrastructure/templates/coverage_summary_template.md`
12. `docs/process_infrastructure/templates/implementation_summary_template.md`
13. `docs/process_infrastructure/templates/milestone_determination_template.md`
14. `docs/process_infrastructure/templates/package_review_template.md`
15. `docs/process_infrastructure/templates/readiness_determination_template.md`
16. `docs/process_infrastructure/templates/reconciliation_summary_template.md`
17. `docs/process_infrastructure/templates/transition_readiness_assessment_template.md`

### Validation Requirements

Add all of the following:

1. pre-move inventory check for the `17` current route-asset paths
2. post-move existence check for the `17` new canonical route-asset paths
3. post-move existence check for the `17` old exact-path aliases
4. post-move link audit for `AGENTS.md`
5. grep audit confirming `AGENTS.md` canonical references now point only to `docs/framework/process_infrastructure/...`

### Rollback Requirements

Add all of the following:

1. preserve pre-move content hash for `AGENTS.md`
2. restore pre-move `AGENTS.md` if any route-asset validation fails
3. restore all `17` old exact-path route-asset aliases before declaring rollback complete
4. revalidate the full route-asset set after rollback

## C. Exact-File Alias Manifest

### Alias Policy

Directory-level redirect language from W1-02 is replaced by exact-file alias requirements.

Minimum policy:

1. every moved file gets an exact-file compatibility alias at its old path
2. each old subtree root gets a directory-level navigation pointer only for human discoverability
3. directory-level pointers do not replace file-level alias coverage

### Exact-File Compatibility Requirements

#### `docs/process_infrastructure/` Alias Set

All `17` moved files require exact-file aliases at their original paths:

1. `docs/process_infrastructure/checklists/git_ignore_verification_checklist.md`
2. `docs/process_infrastructure/checklists/governance_boundary_verification_checklist.md`
3. `docs/process_infrastructure/checklists/hygiene_review_checklist.md`
4. `docs/process_infrastructure/checklists/publication_readiness_checklist.md`
5. `docs/process_infrastructure/checklists/push_readiness_checklist.md`
6. `docs/process_infrastructure/checklists/review_package_completeness_checklist.md`
7. `docs/process_infrastructure/checklists/validation_evidence_checklist.md`
8. `docs/process_infrastructure/checklists/zip_workflow_checklist.md`
9. `docs/process_infrastructure/templates/closure_determination_template.md`
10. `docs/process_infrastructure/templates/conformance_report_template.md`
11. `docs/process_infrastructure/templates/coverage_summary_template.md`
12. `docs/process_infrastructure/templates/implementation_summary_template.md`
13. `docs/process_infrastructure/templates/milestone_determination_template.md`
14. `docs/process_infrastructure/templates/package_review_template.md`
15. `docs/process_infrastructure/templates/readiness_determination_template.md`
16. `docs/process_infrastructure/templates/reconciliation_summary_template.md`
17. `docs/process_infrastructure/templates/transition_readiness_assessment_template.md`

#### `docs/lineages/` Alias Set

All `12` moved files require exact-file aliases at their original paths:

1. `docs/lineages/README.md`
2. `docs/lineages/i10_semantic_commitment_implementation.md`
3. `docs/lineages/i10r_microprobe_checkpoint.md`
4. `docs/lineages/i10r_microprobe_checkpoint_lineage_note.md`
5. `docs/lineages/i2_contamination_event.md`
6. `docs/lineages/i4_i5_overconstraint_collapse.md`
7. `docs/lineages/i6_isolated_variable_pivot.md`
8. `docs/lineages/i7_coupled_schema_dynamics.md`
9. `docs/lineages/i8_bounded_implementation_scaffold.md`
10. `docs/lineages/i8_pre_training_governance_snapshot.md`
11. `docs/lineages/i9_commitment_conversion_implementation.md`
12. `docs/lineages/i9_post_eval_checkpoint.md`

#### Primary Convergence Alias Set

All `11` moved primary convergence records require exact-file aliases at their original paths:

1. `docs/convergence/STAGE_B_COMPLETION_DETERMINATION.md`
2. `docs/convergence/STAGE_BC_PROCESS_EXTRACTION_ASSESSMENT.md`
3. `docs/convergence/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md`
4. `docs/convergence/STAGE_BC_PHASE1_PROCESS_INFRASTRUCTURE_CLOSURE_DETERMINATION.md`
5. `docs/convergence/STAGE_C_PACKAGE_3C_REGIMEN_RETROSPECTIVE_AND_REUSABILITY_ASSESSMENT.md`
6. `docs/convergence/STAGE_C_PACKAGE_5E_DIRECT_ANSWER_LIFECYCLE_RETROSPECTIVE_AND_REGIMEN_GENERALIZATION_ASSESSMENT.md`
7. `docs/convergence/STAGE_C_PACKAGE_6A_FORMAL_BLOCKER_ORIENTED_REGIMEN_BRANCH_ADOPTION_ASSESSMENT.md`
8. `docs/convergence/STAGE_C_PACKAGE_6B_CONDITIONAL_BLOCKER_ORIENTED_BRANCH_ADOPTION_DETERMINATION.md`
9. `docs/convergence/STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md`
10. `docs/convergence/STAGE_C10C_REFRESHED_DETECTOR_MIGRATION_GATE_DETERMINATION.md`
11. `docs/convergence/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md`

### Alias Coverage Requirements

Each exact-file alias must:

1. name the new canonical target path
2. state that the old path is preserved for compatibility and discoverability
3. avoid introducing alternate doctrine or methodology semantics
4. remain text-readable in the repository UI

### Directory-Level Navigation Treatment

Directory-level navigation treatment is limited to:

1. pointer page at `docs/process_infrastructure/`
2. pointer page at `docs/lineages/`
3. pointer note at `docs/convergence/` only where needed for moved primary records

Directory-level pages are supplementary only.

They do not satisfy compatibility on their own.

## D. Convergence Index Completion Plan

### Existing Stable IDs Retained

The following existing IDs remain unchanged:

1. `conv:stage_b:0001`
2. `conv:stage_bc:0001`
3. `conv:stage_bc:0002`
4. `conv:stage_c:0001`
5. `conv:stage_c:0002`

### Six Required Stable IDs

The revised Wave 1 requires the following new stable IDs:

1. `conv:stage_bc:0003`
2. `conv:stage_c:0003`
3. `conv:stage_c:0004`
4. `conv:stage_c:0005`
5. `conv:stage_c:0006`
6. `conv:stage_c:0007`

### Required Index Additions

Create new `convergence_history_index.json` entries for:

1. `docs/convergence/STAGE_BC_PHASE1_PROCESS_INFRASTRUCTURE_CLOSURE_DETERMINATION.md` -> `conv:stage_bc:0003`
2. `docs/convergence/STAGE_C_PACKAGE_3C_REGIMEN_RETROSPECTIVE_AND_REUSABILITY_ASSESSMENT.md` -> `conv:stage_c:0003`
3. `docs/convergence/STAGE_C_PACKAGE_5E_DIRECT_ANSWER_LIFECYCLE_RETROSPECTIVE_AND_REGIMEN_GENERALIZATION_ASSESSMENT.md` -> `conv:stage_c:0004`
4. `docs/convergence/STAGE_C_PACKAGE_6A_FORMAL_BLOCKER_ORIENTED_REGIMEN_BRANCH_ADOPTION_ASSESSMENT.md` -> `conv:stage_c:0005`
5. `docs/convergence/STAGE_C_PACKAGE_6B_CONDITIONAL_BLOCKER_ORIENTED_BRANCH_ADOPTION_DETERMINATION.md` -> `conv:stage_c:0006`
6. `docs/convergence/STAGE_C10C_REFRESHED_DETECTOR_MIGRATION_GATE_DETERMINATION.md` -> `conv:stage_c:0007`

### Registry Updates

Update `docs/housekeeping/indexes/index_registry.json` as follows:

1. `convergence_history` `entry_count`: `6` -> `12`
2. keep family `status` as `partially_populated`
3. keep `anchor_entry_id` unchanged
4. no schema change

### Crosswalk Updates

For all `11` moved primary convergence records:

1. update `current_path` to the new canonical location
2. preserve `source_path` as the original `docs/convergence/...` path
3. append the original path to `previous_paths`
4. preserve `related_ids` linkage to the registry and family index
5. keep the old path resolvable through the exact-file alias layer

### Exclusions

No Wave 1 convergence index additions are required for:

1. `STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN_ACCEPTANCE_ASSESSMENT.md`
2. `STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN_IMPLEMENTATION_SUMMARY.md`

## E. Revised Validation And Rollback Plan

### Pre-Move Validation

1. freeze the exact revised move manifest
2. capture content hashes for:
   - all moved canonical files
   - `AGENTS.md`
   - both index files touched by the execution package
3. run `python scripts/validate_housekeeping_indexes.py`
4. run `git diff --check`
5. run `AGENTS.md` route-asset inventory validation for all `17` current route assets
6. run exact-file alias inventory validation for:
   - `17` `docs/process_infrastructure/*` files
   - `12` `docs/lineages/*` files
   - `11` moved primary convergence files
7. run high-citation documentation audit over:
   - `README.md`
   - `docs/current/*`
   - `AGENTS.md`
   - selected moved primary convergence docs
8. run sampled historical citation audit for exact lineage-file and convergence-file references

### Post-Move Validation

1. confirm every canonical target file exists
2. confirm every required exact-file alias exists
3. confirm the two removed companion records remain at their original paths
4. confirm `AGENTS.md` canonical references now resolve to `docs/framework/process_infrastructure/...`
5. confirm old `AGENTS.md` route-asset paths still resolve through alias coverage
6. re-run `python scripts/validate_housekeeping_indexes.py`
7. verify `convergence_history` `entry_count` equals `12`
8. compare post-move hashes of canonical files to the pre-move baseline where identity should be preserved
9. re-run `git diff --check`
10. run sampled historical citation checks against preserved old exact paths

### Rollback Triggers

Rollback is mandatory if any of the following occurs:

1. missing canonical target file
2. missing exact-file alias
3. unresolved `AGENTS.md` route-asset reference
4. index-validator failure
5. `entry_count` mismatch in `index_registry.json`
6. removed companion records are accidentally moved
7. sampled historical citation no longer resolves through the old exact path

### Rollback Procedure

1. stop execution immediately
2. restore moved canonical files to their original paths in reverse dependency order
3. remove newly created target copies
4. restore pre-move `AGENTS.md`
5. restore pre-move `convergence_history_index.json`
6. restore pre-move `index_registry.json`
7. remove all Wave 1 exact-file aliases and restore original content locations
8. restore navigation pages to the pre-move state
9. rerun validation before considering rollback successful

### Rollback Success Criteria

1. every original source path is restored
2. no partial new canonical tree remains
3. the two companion records remain at their original paths
4. all `17` old `AGENTS.md` route-asset paths resolve again
5. `python scripts/validate_housekeeping_indexes.py` passes
6. `git diff --check` passes

## F. Execution Readiness Determination

### Determination

The revised plan is ready for independent authorization review.

### Why

This W1-05 revision incorporates every blocker-resolution requirement identified by W1-04:

1. `AGENTS.md` is now an explicit hard-consumer surface
2. exact-file alias coverage replaces directory-level redirect assumptions
3. the convergence-index completion work is fully enumerated
4. the two launch-plan companion records are removed from Wave 1 move scope
5. validation and rollback coverage now include AGENTS, alias, index, and historical-citation checks

### Remaining Boundary

W1-05 does not authorize execution by itself.

It is the corrected execution-plan draft that should be subjected to final independent authorization review.

### Final Readiness Answer

No additional planning is required before final authorization review.

If this revised plan is accepted, the next correct step is independent authorization review rather than another planning package.
