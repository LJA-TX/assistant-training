# W1-02 Minimal Framework Separation Implementation Plan

## Work Package

- ID: `W1-02`
- Title: `Minimal Framework Separation Implementation Plan`
- Repository: `/opt/ai-stack/assistant-training`
- Scope: Wave 1 planning only
- Authority basis:
  - `docs/housekeeping/HOUSEKEEPING_PRESERVATION_INDEX.md`
  - `docs/housekeeping/HOUSEKEEPING_ARCHITECTURE_AND_MIGRATION_PLAN.md`
  - `docs/housekeeping/HOUSEKEEPING_PATH_DECOUPLING_AND_COMPATIBILITY_STRATEGY.md`
  - `docs/housekeeping/HOUSEKEEPING_COMPATIBILITY_LAYER_IMPLEMENTATION_PLAN.md`
  - `docs/housekeeping/MP-01_MIGRATION_PREPARATION_BOUNDARY_ASSESSMENT.md`
  - `docs/housekeeping/MP-02_CANONICAL_MIGRATION_MAP_AND_INDEXING_PLAN.md`
  - `docs/housekeeping/W0-01_CANONICAL_INDEX_FRAMEWORK_DESIGN.md`
  - `docs/housekeeping/W0-02_CANONICAL_INDEX_INFRASTRUCTURE_IMPLEMENTATION.md`
  - `docs/housekeeping/W0-03_INDEX_POPULATION_STRATEGY_AND_SCOPE_DETERMINATION.md`
  - `docs/housekeeping/W0-04` anchor population artifacts
  - `docs/housekeeping/W1-01_FRAMEWORK_HISTORY_SEPARATION_ASSESSMENT.md`
- Out of scope:
  - file moves
  - archive creation
  - restructuring
  - code changes
  - doctrine changes
  - migration execution

## Current-State Basis

- W1-01 determined that the repository is ready for Wave 1 migration planning.
- Only the minimal framework-first separation wave is justified.
- Provenance-heavy history remains out of scope for the first wave.
- Current navigation already distinguishes reusable framework surfaces from preserved history.

## Minimal Wave Definition

The minimal Wave 1 separation moves the already-classified framework and current-state surfaces out of the mixed convergence/history surface while leaving provenance-heavy history in place.

This plan keeps the first wave small enough to validate the framework/history split without forcing a bulk history relocation.

## A. Exact Move Inventory

### Directory-Level Moves

| Source | Target | Scope Note |
|---|---|---|
| `docs/process_infrastructure/` | `docs/framework/process_infrastructure/` | Move the entire subtree, preserving internal filenames and relative links. |
| `docs/lineages/` | `docs/framework/lineages/` | Move the entire subtree, preserving internal filenames and relative links. |

### Exact File Moves

| Source | Target | Role In Minimal Wave |
|---|---|---|
| `docs/convergence/STAGE_B_COMPLETION_DETERMINATION.md` | `docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md` | Current-state completion marker. |
| `docs/convergence/STAGE_BC_PROCESS_EXTRACTION_ASSESSMENT.md` | `docs/framework/methodology/STAGE_BC_PROCESS_EXTRACTION_ASSESSMENT.md` | Reusable process methodology. |
| `docs/convergence/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md` | `docs/framework/methodology/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md` | Reusable process methodology. |
| `docs/convergence/STAGE_BC_PHASE1_PROCESS_INFRASTRUCTURE_CLOSURE_DETERMINATION.md` | `docs/framework/methodology/STAGE_BC_PHASE1_PROCESS_INFRASTRUCTURE_CLOSURE_DETERMINATION.md` | Reusable framework closure record. |
| `docs/convergence/STAGE_C_PACKAGE_3C_REGIMEN_RETROSPECTIVE_AND_REUSABILITY_ASSESSMENT.md` | `docs/framework/methodology/STAGE_C_PACKAGE_3C_REGIMEN_RETROSPECTIVE_AND_REUSABILITY_ASSESSMENT.md` | Reusable regimen assessment. |
| `docs/convergence/STAGE_C_PACKAGE_5E_DIRECT_ANSWER_LIFECYCLE_RETROSPECTIVE_AND_REGIMEN_GENERALIZATION_ASSESSMENT.md` | `docs/framework/methodology/STAGE_C_PACKAGE_5E_DIRECT_ANSWER_LIFECYCLE_RETROSPECTIVE_AND_REGIMEN_GENERALIZATION_ASSESSMENT.md` | Reusable regimen assessment. |
| `docs/convergence/STAGE_C_PACKAGE_6A_FORMAL_BLOCKER_ORIENTED_REGIMEN_BRANCH_ADOPTION_ASSESSMENT.md` | `docs/framework/methodology/STAGE_C_PACKAGE_6A_FORMAL_BLOCKER_ORIENTED_REGIMEN_BRANCH_ADOPTION_ASSESSMENT.md` | Reusable branch-adoption assessment. |
| `docs/convergence/STAGE_C_PACKAGE_6B_CONDITIONAL_BLOCKER_ORIENTED_BRANCH_ADOPTION_DETERMINATION.md` | `docs/framework/methodology/STAGE_C_PACKAGE_6B_CONDITIONAL_BLOCKER_ORIENTED_BRANCH_ADOPTION_DETERMINATION.md` | Reusable branch-adoption determination. |
| `docs/convergence/STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md` | `docs/framework/methodology/STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md` | Reusable transition assessment. |
| `docs/convergence/STAGE_C10C_REFRESHED_DETECTOR_MIGRATION_GATE_DETERMINATION.md` | `docs/framework/methodology/STAGE_C10C_REFRESHED_DETECTOR_MIGRATION_GATE_DETERMINATION.md` | Reusable gate determination. |
| `docs/convergence/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md` | `docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md` | Parked investigation launch plan. |
| `docs/convergence/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN_ACCEPTANCE_ASSESSMENT.md` | `docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN_ACCEPTANCE_ASSESSMENT.md` | Canonical acceptance record for the parked launch plan. |
| `docs/convergence/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN_IMPLEMENTATION_SUMMARY.md` | `docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN_IMPLEMENTATION_SUMMARY.md` | Canonical implementation summary for the parked launch plan package. |

### Explicit Non-Moves For This Wave

- `docs/assistant_training_goal_documents_and_artifacts_index.md` stays in place for now.
- Bulk `docs/convergence/` history outside the exact file list above stays in place.
- `docs/continuity/`, `docs/history/`, `configs/lora/`, `manifests/runs/`, `manifests/reports/`, `data/v1_0/`, and `reports/stage_c1/` through `reports/stage_c6/` stay in place.

## B. Alias And Redirect Plan

### Navigation Redirects

- Update `README.md` so the first-level framework pointers resolve to the new framework/current layout.
- Update `docs/current/start_here.md` to point to `docs/framework/process_infrastructure/`, `docs/framework/lineages/`, and the new current-status and roadmap targets.
- Update `docs/current/framework_vs_history.md` so the "reusable framework" list points at the new targets, not the old mixed convergence paths.
- Update `docs/current/current_status.md` and `docs/current/housekeeping_status.md` in place to reflect the new framework/history split and the continuing structural-migration gate.

### Compatibility Aliases

- Keep the old `docs/process_infrastructure/` and `docs/lineages/` locations discoverable through lightweight redirect stubs or pointer pages if the final execution package does not support filesystem aliases.
- Replace moved `docs/convergence/*.md` locations with short redirect notes that point to the new target path and preserve the old path as a discoverability entry.
- Keep the old convergence paths readable until the migration crosswalk is fully updated.

### Index Updates

- Update `docs/housekeeping/indexes/convergence_history_index.json` for every moved convergence record:
  - set `current_path` to the new target
  - preserve the old path in `previous_paths`
  - retain the stable ID
- If the launch-plan acceptance and implementation summary are included in the execution package, add their convergence index records before move execution or create the corresponding crosswalk entries in the same update batch.
- No new repository-wide index family is required before this wave executes.

### Crosswalk Updates

- Preserve old-path references in `previous_paths` for the moved convergence records.
- Update current navigation pages so they reference only the new primary paths.
- Keep the redirect story one-to-one:
  - old mixed convergence path
  - new framework or current path
  - stable ID in the index

## C. Validation Plan

### Pre-Move Validation

1. Freeze the exact move manifest for the inventory above.
2. Capture content hashes for each source file and directory subtree in scope.
3. Run `python scripts/validate_housekeeping_indexes.py` to confirm the Wave 0 registry and family indexes are still valid.
4. Run `git diff --check` to ensure the worktree is clean of whitespace and patch-format problems before execution.
5. Run a targeted link audit over `README.md`, `docs/current/*`, and the selected convergence files to confirm all current source paths are known and accounted for.

### Post-Move Validation

1. Confirm every target file exists at its new location.
2. Confirm every planned redirect stub exists at the old path.
3. Confirm the current-navigation pages resolve to the new framework/current layout.
4. Re-run `python scripts/validate_housekeeping_indexes.py`.
5. Re-run `git diff --check`.
6. Verify that the selected old paths are still discoverable only through the intended redirect or crosswalk mechanism.

### Rollback Validation

1. Restore the source locations from the move manifest in reverse dependency order.
2. Remove the target copies and any redirect stubs created for the wave.
3. Revert the convergence-history crosswalk updates.
4. Restore the pre-move navigation links.
5. Re-run the index validator and `git diff --check` to confirm the repository is back at the baseline state.

## D. Rollback Plan

### Rollback Triggers

- A moved file is missing or duplicated.
- A redirect stub does not resolve to the intended target.
- A navigation page points at the wrong path.
- `convergence_history_index.json` no longer matches the physical layout.
- The validation commands fail after the move batch.

### Rollback Procedure

1. Stop the move batch immediately.
2. Restore the deepest moved files first, then the directory subtrees.
3. Revert any crosswalk or index updates made for the wave.
4. Restore the navigation pages and redirect stubs to the pre-move state.
5. Re-run validation before considering the repository recovered.

### Rollback Success Criteria

- Every source path from the move manifest is back at its original location.
- No partial target tree remains for the wave.
- The validator passes again.
- The navigation layer once again points at the baseline layout.

## E. Execution Sequencing

1. Freeze the move manifest and baseline hashes.
2. Prepare any required crosswalk entries for the selected convergence records.
3. Create the destination directories:
   - `docs/framework/process_infrastructure/`
   - `docs/framework/lineages/`
   - `docs/framework/methodology/`
   - `docs/current/status/`
   - `docs/current/roadmap/`
4. Move `docs/process_infrastructure/` to `docs/framework/process_infrastructure/`.
5. Move `docs/lineages/` to `docs/framework/lineages/`.
6. Move the framework methodology convergence records into `docs/framework/methodology/`.
7. Move `docs/convergence/STAGE_B_COMPLETION_DETERMINATION.md` to `docs/current/status/`.
8. Move the launch-plan trio into `docs/current/roadmap/`.
9. Install redirect stubs or pointer pages at the old locations.
10. Update `README.md`, `docs/current/start_here.md`, `docs/current/framework_vs_history.md`, `docs/current/current_status.md`, `docs/current/housekeeping_status.md`, and `docs/housekeeping/indexes/convergence_history_index.json`.
11. Run post-move validation.
12. If any validation step fails, execute the rollback procedure in reverse order.

## F. Readiness Determination

### Determination

The repository will be ready for a first structural migration package after W1-02, but only for the minimal Wave 1 scope defined above.

### What This Means

- The exact move inventory is now bounded.
- The alias and redirect requirements are explicit.
- The validation and rollback paths are defined.
- The first structural wave can be executed safely once implementation authorization is granted.

### Boundary Statement

This plan does not authorize execution.

It defines the smallest framework-history separation package that can be implemented without broadening into provenance-heavy history, archive formation, or repository-wide restructuring.
