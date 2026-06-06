# W1-07 Wave 1 Authorization Gap Closure

## Work Package

- ID: `W1-07`
- Title: `Wave 1 Authorization Gap Closure`
- Repository: `/opt/ai-stack/assistant-training`
- Scope: planning only
- Authority basis:
  - `docs/housekeeping/W1-05_REVISED_MINIMAL_FRAMEWORK_SEPARATION_EXECUTION_PLAN.md`
  - `docs/housekeeping/W1-06_FINAL_WAVE_1_AUTHORIZATION_REVIEW.md`
- Out of scope:
  - implementation
  - file movement
  - restructuring
  - archive creation
  - code changes
  - doctrine changes

## Current-State Basis

- W1-05 produced the revised execution plan.
- W1-06 concluded that the repository was only conditionally ready.
- W1-06 identified three narrow remaining authorization gaps:
  1. path-dependent factual staleness in one moved methodology record
  2. sampled rather than exhaustive historical citation validation
  3. missing explicit semantics for `conv:seed:0001`

## Gap-Closure Principle

Wave 1 does not need a new architecture decision.

It needs three explicit execution-plan decisions:

1. how to treat the path-dependent closure determination
2. how to validate the finite alias/citation surface exhaustively
3. how the convergence seed entry behaves after the Stage B completion record moves

## A. Path-Dependent Methodology Record Resolution

### Record Under Review

`docs/convergence/STAGE_BC_PHASE1_PROCESS_INFRASTRUCTURE_CLOSURE_DETERMINATION.md`

### Option Evaluation

#### 1. Reconcile And Move

Assessment:

- preserves the H-01 classification of this record as future-primary reusable methodology
- keeps the framework methodology surface coherent
- avoids leaving one primary process-infrastructure closure record stranded in the historical convergence surface
- can be done without changing doctrine or the closure outcome if edits are strictly limited to path-dependent factual framing

#### 2. Move Unchanged

Assessment:

- not acceptable
- the moved primary record would become factually stale because it currently states present-tense findings tied to `docs/process_infrastructure/...`
- this would create a new primary-path document whose content is immediately inaccurate after execution

#### 3. Remove From Wave 1 Scope

Assessment:

- acceptable as a fallback only
- avoids factual staleness
- but weakens the methodology extraction surface and creates an unnecessary exception inside the H-01 primary record set

### Correct Resolution

`1. reconcile and move`

### Justification

This is the strongest option because it preserves both:

1. the methodological importance of the record
2. the truthfulness of the moved primary-path content

The required reconciliation is narrow and does not require doctrine redesign.

It should be limited to path-dependent factual statements only.

### Required Reconciliation Boundaries

The execution package should allow only the following content updates in this record:

1. convert present-tense path claims into closure-time historical statements
2. add a short post-move note that the canonical process-infrastructure location is now `docs/framework/process_infrastructure/...`
3. preserve the original closure result, criteria statuses, and closure-ready determination unchanged

The execution package should explicitly forbid:

1. changing the closure outcome
2. changing pass/fail criterion results
3. changing doctrine or route semantics
4. changing the historical statement that the closure review originally validated the old `docs/process_infrastructure/...` layout

### Minimum Acceptance Rule

The moved record is acceptable on the future primary path only if:

1. its closure-time findings remain historically true
2. its post-move canonical-path note is current and correct
3. it no longer states the old physical location as the current canonical location

## B. Exhaustive Historical Citation Validation Plan

### Exact Validation Scope

The alias validation surface is finite and should be treated as exhaustive, not sampled.

The exact alias scope is:

1. `17` `docs/process_infrastructure/*` alias files
2. `12` `docs/lineages/*` alias files
3. `11` moved primary convergence alias files

Total exact-file alias surface:

- `40` alias paths

### Citation Families Covered

Exhaustive validation must cover:

1. process infrastructure aliases
2. lineage aliases
3. moved convergence aliases
4. tracked historical citations that reference any of those old paths, including exact relative paths and exact absolute repository paths

### Exhaustive Validation Requirements

#### 1. Alias Completeness Validation

Validate all `40` exact-file aliases directly.

For each alias path:

1. confirm the old path exists
2. confirm the old path points to the intended new canonical target
3. confirm the old path remains text-readable in the repository UI
4. confirm the alias does not claim independent canonical authority

#### 2. Canonical Target Validation

For each of the `40` alias paths:

1. confirm the new canonical target file exists
2. confirm the alias target matches the execution manifest exactly
3. confirm the moved file content hash matches the pre-move baseline where exact identity should be preserved

#### 3. Exhaustive Tracked-Reference Resolution Audit

Run a repo-wide tracked-file scan over:

1. `AGENTS.md`
2. `README.md`
3. `docs/`
4. `manifests/`
5. `reports/`
6. `data/`

For all matches to:

1. `docs/process_infrastructure/`
2. `docs/lineages/`
3. each of the `11` moved primary convergence old paths
4. absolute repository-path forms of moved lineage paths where they exist

Validation rule:

- every tracked reference must resolve either to:
  1. an exact-file alias
  2. an unchanged in-place record
  3. an explicitly updated canonical new path

No unresolved matches are allowed.

#### 4. Wildcard And Directory-Family Reference Validation

Some historical records cite path families such as:

1. `docs/process_infrastructure/checklists/*`
2. `docs/process_infrastructure/templates/*`

For those references, exhaustive validation requires:

1. confirming the old directory root remains discoverable through a directory-level pointer page
2. confirming that the full exact-file alias set beneath that family is complete
3. confirming no file named by the family reference is missing from the alias manifest

#### 5. Historical Absolute-Path Validation

For historical records that contain exact absolute repository paths, such as:

1. `/opt/ai-stack/assistant-training/docs/lineages/i9_post_eval_checkpoint.md`
2. `/opt/ai-stack/assistant-training/docs/lineages/i10r_microprobe_checkpoint.md`

validation must confirm that those old absolute paths still resolve to the expected alias-preserved files after execution and after rollback.

### Post-Move And Post-Rollback Standard

Exhaustive validation is required:

1. after execution
2. after rollback, if rollback is triggered

Sampling is not acceptable at either stage.

## C. Convergence Seed Semantics Clarification

### Seed Entry Under Review

`conv:seed:0001`

### Explicit Treatment

#### source_path

`source_path` remains:

- `docs/convergence/STAGE_B_COMPLETION_DETERMINATION.md`

Reason:

- it records the original path from which the family seed anchor was minted
- preserving that original path is consistent with W0-01 and W1-05 crosswalk rules

#### current_path

After Wave 1 execution, `current_path` should become:

- `docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md`

Reason:

- `current_path` should identify the canonical current live location of the seeded family-anchor record
- it should not point to the compatibility alias

#### Alias Interaction

The old path:

- `docs/convergence/STAGE_B_COMPLETION_DETERMINATION.md`

must remain physically resolvable through the exact-file alias layer, but that alias is:

1. a compatibility and discoverability surface
2. not the canonical `current_path`

The old path should continue to appear in the seed crosswalk as preserved historical location information.

#### Post-Move Semantics

After the move:

1. `conv:seed:0001` remains the family-anchor seed entry
2. `conv:stage_b:0001` remains the migration-boundary anchor for the same underlying record
3. both entries may point to the same moved canonical file through `current_path`
4. the difference between them remains semantic role, not physical content identity

### Recommended Crosswalk Detail

For consistency with the moved primary convergence records:

1. keep `canonical_path` unchanged
2. update `current_path` to the moved canonical file
3. preserve the old convergence path in the seed entry's move crosswalk
4. do not point the seed entry's `current_path` at the alias path

## D. Revised Readiness Assessment

### Remaining Gap Status

The remaining W1-06 authorization gaps are closed at the planning level by this package:

1. the path-dependent methodology record now has an explicit treatment decision
2. sampled historical citation validation is replaced by an exhaustive finite-scope model
3. `conv:seed:0001` post-move semantics are now explicit

### Residual Planning Ambiguity

No additional planning ambiguity remains that would block a final authorization decision.

This does not authorize execution.

It closes the planning gaps that prevented a final authorization decision in W1-06.

## E. Execution Authorization Recommendation

### Recommendation

`3. Ready For Final Authorization Review`

### Why

The remaining issues identified by W1-06 were narrow and execution-adjacent.

This package resolves them without:

1. expanding Wave 1 scope
2. reopening architecture
3. introducing archive work
4. requiring another planning wave

### Final Readiness Answer

The repository is ready for a final authorization decision on the corrected Wave 1 execution package.
