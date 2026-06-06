# W1-06 Final Wave 1 Authorization Review

## Work Package

- ID: `W1-06`
- Title: `Final Wave 1 Authorization Review`
- Repository: `/opt/ai-stack/assistant-training`
- Scope: assessment only
- Review posture: skeptical, authorization-denying unless the revised plan survives final execution scrutiny
- Authority basis:
  - `docs/housekeeping/W1-03_WAVE_1_EXECUTION_READINESS_AND_INDEPENDENT_RISK_REVIEW.md`
  - `docs/housekeeping/W1-04_WAVE_1_EXECUTION_BLOCKER_RESOLUTION_ASSESSMENT.md`
  - `docs/housekeeping/W1-05_REVISED_MINIMAL_FRAMEWORK_SEPARATION_EXECUTION_PLAN.md`
- Out of scope:
  - implementation
  - file movement
  - restructuring
  - archive creation
  - code changes
  - doctrine changes

## Inspection Basis

This review covered:

1. direct comparison of W1-05 against the blocker set in W1-03 and W1-04
2. repository path-consumer checks for:
   - `AGENTS.md`
   - `docs/process_infrastructure/*`
   - `docs/lineages/*`
   - the retained moved convergence records
3. review of the current convergence index and registry semantics
4. review of moved primary documents for path-dependent factual claims, not just citations

## Executive Conclusion

W1-05 is materially better than W1-02 and resolves most of the named Wave 1 blockers.

It does not yet support unconditional authorization.

The repository is close to authorization, but not past the line.

## A. Blocker Resolution Verification

### W1-03 And W1-04 Blockers That Are Resolved

W1-05 fully resolves these previously identified issues:

1. `AGENTS.md` is now treated as an explicit hard-consumer surface.
2. the two launch-plan companion records are removed from the moved current-path set.
3. the alias model is upgraded from directory-level redirects to exact-file alias coverage.
4. six missing convergence stable IDs and associated index additions are explicitly planned.
5. `index_registry.json` entry-count maintenance is explicitly included.

### Blockers That Are Only Partially Resolved

Two areas remain partially resolved:

1. historical-citation protection
   - W1-05 replaces directory-level redirects with exact-file aliases, which is necessary
   - but the validation model still uses sampled historical citation checks rather than exhaustive checks
2. moved-document semantic freshness
   - W1-05 protects old paths and canonical targets
   - but it does not require reconciliation of moved documents whose content makes factual claims about the old physical layout

### New Final-Review Finding

`docs/convergence/STAGE_BC_PHASE1_PROCESS_INFRASTRUCTURE_CLOSURE_DETERMINATION.md` is in the retained move set, but its content includes factual findings such as:

- route references being path-normalized to `docs/process_infrastructure/...`
- checklist and template libraries existing under `docs/process_infrastructure/...`

If the file is moved while those statements remain unchanged, the new primary methodology record becomes factually stale.

This is not a link-only issue.

It is a content-truth issue.

## B. Move Scope Review

### Revised Move Set

The revised Wave 1 move set is appropriately narrower than W1-02:

1. `docs/process_infrastructure/`
2. `docs/lineages/`
3. `11` H-01 primary convergence/current-state records

The removed move candidates are correctly excluded:

1. `STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN_ACCEPTANCE_ASSESSMENT.md`
2. `STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN_IMPLEMENTATION_SUMMARY.md`

### Remaining Overreach

One retained move candidate remains problematic in the current form:

1. `docs/convergence/STAGE_BC_PHASE1_PROCESS_INFRASTRUCTURE_CLOSURE_DETERMINATION.md`

Reason:

- it contains findings whose truth depends on the current old path layout
- W1-05 does not require a content-reconciliation step for path-dependent assertions

### Omitted Hard Consumers

No new omitted hard consumers at the level of W1-03 were found.

`AGENTS.md` is now correctly included.

The remaining issue is not an omitted consumer.

It is that moved primary content may still assert old-path facts after the move.

## C. Alias And Exact-File Preservation Review

### Sufficiency For `AGENTS.md`

For `AGENTS.md`, the exact-file alias manifest is sufficient in structure.

Why:

1. all `17` route assets are enumerated
2. both canonical new references and old exact-path aliases are required
3. validation and rollback both name `AGENTS.md`

### Sufficiency For `docs/process_infrastructure/*`

For exact-path continuity, the manifest is sufficient in structure.

For execution-grade safety, one gap remains:

- W1-05 does not define a concrete alias-file contract beyond being text-readable and naming the canonical target

That is acceptable for planning depth, but weak for final authorization unless the validation becomes exhaustive.

### Sufficiency For `docs/lineages/*`

The manifest is structurally sufficient because all `12` lineage files are enumerated.

The remaining concern is the same one found in W1-03:

- preserved reports and manifests cite exact lineage-file paths, often as absolute repository paths
- sampled validation is weaker than the repository now needs

### Sufficiency For Moved Convergence Records

The alias set is structurally sufficient for the `11` moved primary convergence records.

The remaining weakness is not the file list.

It is that some moved primary docs may keep canonical content that still routes through old aliases or still states the old location as current fact.

### Sufficiency For Preserved Historical Citations

Not yet sufficient for final authorization.

Reason:

1. the exact-file alias list is finite and known
2. the historical citation burden is finite and known enough to check directly
3. W1-05 still uses sampled citation validation

For a first structural migration, sampled validation is too weak.

## D. Index And Crosswalk Review

### Six New Convergence Entries

The six new convergence entries are sufficient in scope.

The chosen additions match the revised retained move set.

### Registry Update

The `entry_count` update from `6` to `12` is internally consistent with:

1. `1` seed entry
2. `5` current non-seed entries
3. `6` newly required entries

### Crosswalk Sufficiency

The crosswalk plan is mostly sufficient.

One remaining ambiguity should be removed before authorization:

- W1-05 describes crosswalk updates for the `11` moved primary convergence records
- the current family-seed entry `conv:seed:0001` also points at `STAGE_B_COMPLETION_DETERMINATION.md`
- the revised plan does not explicitly state whether the seed entry's `current_path` should follow the moved canonical file or remain on the old alias path

This is not a large design gap, but it is a semantic gap in the index model.

## E. Validation And Rollback Review

### What Is Now Execution-Grade

W1-05 is much closer to execution-grade than W1-02:

1. `AGENTS.md` validation is explicit
2. alias existence validation is explicit
3. convergence-index validation is explicit
4. rollback triggers are materially improved
5. removed companion records are explicitly protected

### What Is Still Missing

Two additions are still needed before the plan is execution-grade:

1. replace sampled historical citation validation with exhaustive validation for the exact known alias set
2. add moved-document content validation for path-dependent factual claims

At minimum, that second check must cover:

1. `STAGE_BC_PHASE1_PROCESS_INFRASTRUCTURE_CLOSURE_DETERMINATION.md`

Recommended minimum rule:

- no moved primary document may remain on the future primary path if it still states the old physical location as a present-tense canonical fact

### Rollback Quality

Rollback is strong, but not yet complete enough for unconditional authorization because:

1. it does not name the moved-document content-staleness condition as a rollback trigger
2. it does not require exhaustive post-rollback historical citation verification

## F. Risk Rating

| Risk category | Rating | Justification |
|---|---|---|
| Active workflow risk | `Medium` | `AGENTS.md` is now covered, but execution still depends on exact-file aliases and correct route-asset validation. |
| Provenance risk | `Medium` | file-level alias coverage is planned, but sampled historical citation checks are weaker than needed and one moved primary record would become factually stale without reconciliation. |
| Discoverability risk | `Medium` | the new plan is far better than W1-02, but canonical moved docs may still point through aliases or preserve stale current-path claims. |
| Maintenance risk | `Medium` | the alias burden is bounded and manageable, but it remains a non-trivial `40`-file compatibility surface. |
| Rollback risk | `Medium` | rollback is structured, but still lacks explicit treatment for content-stale moved records and exhaustive historical citation rechecks. |

## G. Authorization Recommendation

### Recommendation

`2. Authorize Only After Specific Modifications`

### Required Specific Modifications

1. Add a moved-document content reconciliation rule for path-dependent factual claims.
   - At minimum, explicitly reconcile or remove from Wave 1 scope `STAGE_BC_PHASE1_PROCESS_INFRASTRUCTURE_CLOSURE_DETERMINATION.md` unless its path-dependent findings are updated to the new canonical layout without changing doctrine semantics.
2. Replace sampled historical citation validation with exhaustive validation for the finite exact-file alias set relevant to:
   - `docs/process_infrastructure/*`
   - `docs/lineages/*`
   - moved primary convergence records
3. Clarify the `conv:seed:0001` treatment in the convergence-history index so `current_path` semantics stay explicit after the Stage B completion record moves.

### Why Not `Do Not Authorize`

W1-05 does resolve the major blockers from W1-03 and W1-04.

The remaining issues are narrow and correctable.

### Why Not `Authorize Minimal Wave 1 Execution As Planned`

Because the remaining issues affect the truthfulness of a moved primary methodology record and the adequacy of first-wave provenance validation.

That is too important to waive in the first structural migration package.

## H. Final Readiness Determination

### Determination

`Conditionally Ready`

### Why

The repository is close enough that no new architectural planning wave is needed.

However, W1-05 is not yet safe enough for unconditional authorization.

The remaining work is narrow:

1. one content-freshness reconciliation decision
2. one validation-strengthening decision
3. one small index-semantics clarification

### Final Readiness Answer

The repository is not `Ready`.

It is `Conditionally Ready` for the first structural migration package once the specific modifications above are incorporated into the execution plan.
