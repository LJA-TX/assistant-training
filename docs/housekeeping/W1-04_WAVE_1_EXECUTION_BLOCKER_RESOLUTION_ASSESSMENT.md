# W1-04 Wave 1 Execution Blocker Resolution Assessment

## Work Package

- ID: `W1-04`
- Title: `Wave 1 Execution Blocker Resolution Assessment`
- Repository: `/opt/ai-stack/assistant-training`
- Scope: planning only
- Authority basis:
  - `docs/housekeeping/W1-02_MINIMAL_FRAMEWORK_SEPARATION_IMPLEMENTATION_PLAN.md`
  - `docs/housekeeping/W1-03_WAVE_1_EXECUTION_READINESS_AND_INDEPENDENT_RISK_REVIEW.md`
- Out of scope:
  - implementation
  - file movement
  - restructuring
  - archive creation
  - code changes
  - doctrine changes

## Current State Basis

- W1-02 defines the first structural Wave 1 execution plan.
- W1-03 rejects execution of W1-02 as written.
- The task for W1-04 is not to relitigate Wave 1 in general.
- The task is to determine the minimum blocker-resolution set required to make a revised Wave 1 execution package authorizable.

## Resolution Principle

Wave 1 should not be broadened to solve repository-wide history migration.

The minimum viable path is:

1. resolve exact-file documentation consumers
2. tighten alias and redirect treatment to file-level compatibility
3. complete convergence index coverage for the moved primary records
4. remove non-primary companion records from the moved current-path set

## A. AGENTS.md Consumer Resolution

### Exact Affected References

`AGENTS.md` is a live hard consumer of `docs/process_infrastructure/...` file paths at [AGENTS.md](/opt/ai-stack/assistant-training/AGENTS.md:28) through [AGENTS.md](/opt/ai-stack/assistant-training/AGENTS.md:43).

The exact affected references are the full current file set under `docs/process_infrastructure/`:

- checklists:
  - `docs/process_infrastructure/checklists/git_ignore_verification_checklist.md`
  - `docs/process_infrastructure/checklists/governance_boundary_verification_checklist.md`
  - `docs/process_infrastructure/checklists/hygiene_review_checklist.md`
  - `docs/process_infrastructure/checklists/publication_readiness_checklist.md`
  - `docs/process_infrastructure/checklists/push_readiness_checklist.md`
  - `docs/process_infrastructure/checklists/review_package_completeness_checklist.md`
  - `docs/process_infrastructure/checklists/validation_evidence_checklist.md`
  - `docs/process_infrastructure/checklists/zip_workflow_checklist.md`
- templates:
  - `docs/process_infrastructure/templates/closure_determination_template.md`
  - `docs/process_infrastructure/templates/conformance_report_template.md`
  - `docs/process_infrastructure/templates/coverage_summary_template.md`
  - `docs/process_infrastructure/templates/implementation_summary_template.md`
  - `docs/process_infrastructure/templates/milestone_determination_template.md`
  - `docs/process_infrastructure/templates/package_review_template.md`
  - `docs/process_infrastructure/templates/readiness_determination_template.md`
  - `docs/process_infrastructure/templates/reconciliation_summary_template.md`
  - `docs/process_infrastructure/templates/transition_readiness_assessment_template.md`

### Required Migration Treatment

Minimum authorizable treatment:

1. `AGENTS.md` must be explicitly included in the Wave 1 execution package as a touched surface.
2. `AGENTS.md` should be updated to the new canonical `docs/framework/process_infrastructure/...` paths.
3. The old exact file paths must remain resolvable through file-level compatibility aliases.

Why:

- leaving `AGENTS.md` unchanged would preserve execution continuity only if all `17` old exact paths remain live
- updating `AGENTS.md` without preserving the old exact paths would break preserved citations elsewhere
- the minimum safe state is therefore both:
  - new canonical paths in `AGENTS.md`
  - old exact-path compatibility for historical and secondary documentation consumers

### Required Validation Additions

Add all of the following to the revised Wave 1 validation plan:

1. pre-move inventory check for all `17` `AGENTS.md` route-asset paths
2. post-move validation that every new `docs/framework/process_infrastructure/...` path referenced by `AGENTS.md` exists
3. post-move validation that every old `docs/process_infrastructure/...` path still resolves through the alias layer
4. link audit specifically for [AGENTS.md](/opt/ai-stack/assistant-training/AGENTS.md:28)
5. grep audit confirming no stale `docs/process_infrastructure/...` canonical references remain in `AGENTS.md`

### Required Rollback Additions

Add all of the following to the revised rollback plan:

1. preserve a pre-move copy and hash of `AGENTS.md`
2. restore the pre-move `AGENTS.md` if any route-asset validation fails
3. restore the full old exact-file compatibility set before considering rollback complete
4. validate all `17` old route-asset paths after rollback

## B. Redirect And Alias Resolution

### Are Directory-Level Redirects Sufficient

No.

Directory-level redirects are not sufficient for either:

- `AGENTS.md` file-specific process-asset references
- preserved historical/manifests/report references to exact lineage files

### Is Exact-File Preservation Required

Yes.

Exact-file preservation is required for:

1. all moved `docs/process_infrastructure/*` files
2. all moved `docs/lineages/*` files
3. all moved selected `docs/convergence/*` primary records

This does not require preserving the old path as the canonical source of truth.

It does require preserving the old path as an exact file-level discoverability surface.

### Acceptable Compatibility Mechanisms

Acceptable:

1. exact-file Markdown compatibility stubs at the old paths, each pointing to the new canonical file and recording the canonical target path
2. symlink-style aliases only if the implementation package explicitly confirms repository portability and renderer behavior

Not acceptable as the sole mechanism:

1. directory-level pointer pages only
2. directory-level redirects without per-file coverage

Not preferred for the minimum path:

1. duplicated canonical copies at old and new paths, because divergence risk is higher than with stubs

### Minimum Viable Alias Model

The minimum viable alias model is:

1. move the canonical file to the new target location
2. create an exact-file compatibility stub at the old path
3. keep a directory-root pointer at the old subtree root for navigation
4. preserve the old path in the relevant crosswalk or index where applicable

This model is sufficient because the moved surfaces in Wave 1 are documentation surfaces, not executable Python entrypoints.

### Practical Alias Burden

The full exact-file alias burden for the two directory moves is bounded:

- `17` files under `docs/process_infrastructure/`
- `12` files under `docs/lineages/`

That is a manageable compatibility surface and does not justify abandoning Wave 1.

## C. Convergence Index Coverage Resolution

### Required Index Additions

W1-02 proposes moving `13` convergence records.

After applying the W1-03 classification correction for the launch-plan companion records, the revised primary moved convergence set should contain `11` records.

Of those `11` primary records, the current `convergence_history_index.json` already covers `5`:

- `conv:stage_b:0001`
- `conv:stage_bc:0001`
- `conv:stage_bc:0002`
- `conv:stage_c:0001`
- `conv:stage_c:0002`

The revised Wave 1 therefore requires `6` new convergence index entries:

1. `docs/convergence/STAGE_BC_PHASE1_PROCESS_INFRASTRUCTURE_CLOSURE_DETERMINATION.md`
2. `docs/convergence/STAGE_C_PACKAGE_3C_REGIMEN_RETROSPECTIVE_AND_REUSABILITY_ASSESSMENT.md`
3. `docs/convergence/STAGE_C_PACKAGE_5E_DIRECT_ANSWER_LIFECYCLE_RETROSPECTIVE_AND_REGIMEN_GENERALIZATION_ASSESSMENT.md`
4. `docs/convergence/STAGE_C_PACKAGE_6A_FORMAL_BLOCKER_ORIENTED_REGIMEN_BRANCH_ADOPTION_ASSESSMENT.md`
5. `docs/convergence/STAGE_C_PACKAGE_6B_CONDITIONAL_BLOCKER_ORIENTED_BRANCH_ADOPTION_DETERMINATION.md`
6. `docs/convergence/STAGE_C10C_REFRESHED_DETECTOR_MIGRATION_GATE_DETERMINATION.md`

### Required Stable-ID Creation

Minimum viable ID creation should stay within the existing stable-ID pattern and avoid introducing a new namespace unless later authority requires it.

Recommended new IDs:

1. `conv:stage_bc:0003`
2. `conv:stage_c:0003`
3. `conv:stage_c:0004`
4. `conv:stage_c:0005`
5. `conv:stage_c:0006`
6. `conv:stage_c:0007`

These IDs are not yet minted by this package.

They are the minimum recommended additions needed to bring the revised Wave 1 moved primary set under full convergence index coverage.

### Required Crosswalk Updates

For all `11` revised Wave 1 moved primary convergence records:

1. `convergence_history_index.json`
   - update `current_path` to the new active location
   - retain `source_path` as the original `docs/convergence/...` path
   - append the original path to `previous_paths`
   - preserve existing stable IDs
2. `index_registry.json`
   - increase `convergence_history` `entry_count` from `6` to `12`
   - keep family `status` as `partially_populated` unless later population work changes it
3. no schema change is required

### Companion Records

If the launch-plan companion records are removed from Wave 1 scope, no convergence index entries are required for them in the Wave 1 execution package.

## D. Launch-Plan Companion Classification Review

### Acceptance Assessment

`docs/convergence/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN_ACCEPTANCE_ASSESSMENT.md`

Determination:

- should remain in place for now
- should be removed from Wave 1 move scope

### Implementation Summary

`docs/convergence/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN_IMPLEMENTATION_SUMMARY.md`

Determination:

- should remain in place for now
- should be removed from Wave 1 move scope

### Why

These two documents are companion records, not primary current-state or primary framework records under H-01.

Moving them into `docs/current/roadmap/` would:

1. overstate their future-primary role
2. blur the framework-history boundary
3. add index and redirect work that is not needed for the minimum authorizable Wave 1

### Resolution

Do not move them in Wave 1.

Do not remove them from the repository.

Leave them in `docs/convergence/` until a later archive or reference-layer wave handles companion records consistently.

## E. Revised Wave 1 Scope

### Scope Determination

Wave 1 should shrink.

### Revised Structural Move Scope

Retain in Wave 1:

1. `docs/process_infrastructure/` subtree
2. `docs/lineages/` subtree
3. the `11` H-01 primary convergence/current-state records:
   - `STAGE_B_COMPLETION_DETERMINATION.md`
   - `STAGE_BC_PROCESS_EXTRACTION_ASSESSMENT.md`
   - `STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md`
   - `STAGE_BC_PHASE1_PROCESS_INFRASTRUCTURE_CLOSURE_DETERMINATION.md`
   - `STAGE_C_PACKAGE_3C_REGIMEN_RETROSPECTIVE_AND_REUSABILITY_ASSESSMENT.md`
   - `STAGE_C_PACKAGE_5E_DIRECT_ANSWER_LIFECYCLE_RETROSPECTIVE_AND_REGIMEN_GENERALIZATION_ASSESSMENT.md`
   - `STAGE_C_PACKAGE_6A_FORMAL_BLOCKER_ORIENTED_REGIMEN_BRANCH_ADOPTION_ASSESSMENT.md`
   - `STAGE_C_PACKAGE_6B_CONDITIONAL_BLOCKER_ORIENTED_BRANCH_ADOPTION_DETERMINATION.md`
   - `STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md`
   - `STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md`
   - `STAGE_C10C_REFRESHED_DETECTOR_MIGRATION_GATE_DETERMINATION.md`

Remove from Wave 1:

1. `STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN_ACCEPTANCE_ASSESSMENT.md`
2. `STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN_IMPLEMENTATION_SUMMARY.md`

### Revised Support-Surface Touch Set

Even though the structural move scope shrinks, the execution package must explicitly touch these non-moved support surfaces:

1. `AGENTS.md`
2. `README.md`
3. `docs/current/start_here.md`
4. `docs/current/framework_vs_history.md`
5. `docs/current/current_status.md`
6. `docs/current/housekeeping_status.md`
7. `docs/housekeeping/indexes/convergence_history_index.json`
8. `docs/housekeeping/indexes/index_registry.json`

### Why This Is The Minimum Path

This revised scope:

1. removes the classification error identified by W1-03
2. keeps the original Wave 1 thesis intact
3. avoids broadening Wave 1 into archive formation or history-family migration
4. keeps the blocker-resolution burden bounded and local

## F. Authorization Readiness Assessment

### Can A Revised Execution Plan Be Produced

Yes.

The blocker set is concrete and bounded.

The minimum blocker-resolution package is small enough that a revised execution plan can be produced without reopening Wave 1 architecture.

### Is Additional Planning Required

Yes.

One additional planning package is still required to convert these resolutions into an execution-authorizable revised Wave 1 plan.

That package should:

1. replace the W1-02 directory-level alias language with an exact-file alias manifest
2. add `AGENTS.md` to the touched-surface inventory, validation plan, and rollback plan
3. remove the two launch-plan companion documents from the move inventory
4. add the six missing convergence index entries and the registry-count update to the plan

### Should Wave 1 Be Abandoned

No.

Wave 1 should not be abandoned.

The blocker burden is real, but it is not large enough to justify canceling the first framework-history separation wave.

### Final Readiness Answer

The repository is not yet ready to authorize W1-02 as written.

The repository is ready to produce a revised execution plan for a slightly smaller, execution-authorizable Wave 1 package.
