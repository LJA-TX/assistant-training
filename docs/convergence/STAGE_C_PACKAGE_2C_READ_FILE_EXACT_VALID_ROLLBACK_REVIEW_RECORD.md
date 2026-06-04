# Stage C Package 2C Read-File Exact-Valid Rollback Review Record

## Scope

This rollback review record covers the remaining Package 1E gate-evidence requirement for:

- `read_file_exact_valid_rate`

This is rollback assessment only.

It does not implement rollback behavior or authorize migration.

## Conformance Targets

This review checks whether the repository now has an explicit rollback record proving:

1. prior detector behavior remains recoverable;
2. old and new outputs remain separable during migration review;
3. partial or unstable evidence becomes noncomputable rather than silently passing;
4. audit artifacts are retained for failed attempts.

The review also records the user-requested expansion:

5. missing or partial Stage C input behavior for this surface;
6. current rollback-readiness state;
7. exact future rollback artifacts required if a later migration slice is authorized.

## Rollback Requirement Inventory

### Package 1E Rollback Requirements

Package 1E requires an explicit rollback record proving:

1. prior detector behavior remains recoverable;
2. old and new outputs remain separable during migration review;
3. partial or unstable evidence becomes noncomputable rather than silently passing;
4. audit artifacts are retained for failed attempts.

### Additional Doctrine

Stage B implementation-readiness doctrine adds:

1. preserve prior detector behavior until new emissions are validated;
2. keep old and new outputs separable during transition;
3. make partial emission noncomputable rather than silently accepted;
4. retain audit artifacts for failed attempts.

Family A rollback doctrine adds:

1. rollback must not relax governance rules;
2. rollback must not convert missing evidence into passing state;
3. rollback must preserve the distinction between current-run noncomputability and baseline comparison blockage.

## Surface-Specific Rollback Boundary

### Legacy Source Boundary

Active legacy source for this surface:

1. `summary.json`
2. path: `failure_profile.read_file_exact_valid.rate`

Active construction site:

1. `scripts/eval_canonical_manifest.py::_build_failure_profile`

Active detector consumer boundary:

1. `scripts/post_eval_collapse_detector.py::_resolve_metric_from_catalog`
2. `scripts/post_eval_collapse_detector.py::_resolve_required_metrics`
3. `scripts/post_eval_collapse_detector.py::_run_detector`

Active threshold consumer boundary:

1. `manifests/reports/stage_b_v1_threshold_profile.json`
2. catastrophic rule `read_file_exact_valid_rate_lt_0_40`
3. watch rule `read_file_exact_valid_rate_lt_0_70`

### Prospective Authoritative Source Boundary

Current authoritative passive source artifacts:

1. `stage_c_row_fact_metadata_artifact.json`
2. `stage_c_family_a_scorer_evidence_artifact.json`

Current authoritative passive construction path:

1. Package 1C reconciliation surface consumes:
   - `records[].membership_markers.family_b1_read_file_eligible == true`
   - `sides.base.records[].exact_valid joined by row_id`

Current authoritative passive readiness path:

1. Package 1D consumes Package 1C reconciliation output and classifies this surface as `migration-ready`

### Separable Artifacts Boundary

The following surfaces must remain separable in any later migration review:

1. legacy `summary.json`
2. legacy `comparison_rows.jsonl`
3. legacy detector outputs:
   - `collapse_watch_interpretation.json`
   - `gate_assessment.json`
4. Stage C row-fact artifact
5. Stage C Family A scorer-evidence artifact
6. Stage C governance guardrails artifact
7. Stage C runtime contract summary artifact
8. Package 1B governance report
9. Package 1C reconciliation report
10. Package 1D readiness report
11. Package 2A gate-evidence bundle and stability assessment

## Current Rollback-Readiness Assessment

| Rollback Requirement | Current Evidence | Status | Notes |
|---|---|---|---|
| Legacy detector behavior recoverability | Active detector and threshold profile remain legacy-authoritative; Package 2A preserves `summary.json`, threshold profile path, detector dependency inventory, and full supporting artifact paths | satisfied | Recoverability is currently strongest because no detector migration has been enacted. |
| Old/new output separability | Package 1A and Package 2A preserve additive Stage C artifacts; runtime contract summary reports `summary_json=preserved`, `detector_metrics=unchanged`, `threshold_behavior=unchanged`; legacy and Stage C artifact paths remain distinct | satisfied | The current repo already keeps legacy and Stage C surfaces separate rather than overloading one artifact. |
| Missing or partial Stage C input behavior | Package 2B records that future migrated handling must preserve explicit noncomputable behavior if row facts, scorer evidence, row-ID joins, or denominators are missing; current live detector remains legacy-only | partially satisfied | The requirement is documented and bounded, but the focus surface has not exercised missing-authoritative-input handling under an authoritative detector path because migration is still disabled. |
| Noncomputable handling for unstable or incomplete evidence | Active detector already marks unresolved required metrics as noncomputable; Stage B doctrine requires partial emission to remain noncomputable; Stage C passive artifacts preserve missingness without reconstruction | partially satisfied | The governing behavior is explicit and conservative, but it has not been executed for an active authoritative detector input path for this surface. |
| Audit artifact preservation | Package 2A stores raw hashes, normalized digests, row-identity digests, supporting artifact paths, reconciliation snapshot, readiness snapshot, and stability results for the focus surface | satisfied | Current full-run gate evidence already preserves the audit trail needed to reproduce the legacy and passive-authoritative view of this surface. |
| Failed-attempt preservation | Current repo preserves the artifact classes that a failed future migration attempt would need to keep, but no migration-attempt-specific preservation manifest or rollback trigger record exists yet | partially satisfied | This is expected before migration authorization; the missing pieces are future attempt-time artifacts, not current evidence blockers. |

## Assessment Interpretation

Current repository state is strongest on:

1. legacy recoverability;
2. output separability;
3. audit preservation.

Current repository state is only partial on:

1. future authoritative missing-input handling under active detector consumption;
2. future attempt-specific failed-migration preservation artifacts.

These partial states do not create an active rollback blocker for Package 1E gate evidence because:

1. detector migration is still disabled;
2. the rollback review requirement is the existence of an explicit rollback record, not pre-creation of migration-attempt artifacts;
3. the partial items are now surfaced as mandatory artifacts for any later authorized migration slice.

## Required Future Rollback Artifact Inventory

If a later migration slice is authorized, the following artifacts would be required to preserve rollback safety for this surface:

1. dual-surface comparison record for the same frozen row set:
   - legacy `failure_profile.read_file_exact_valid`
   - authoritative Stage C read-file exact-valid surface
2. pre-migration detector snapshot:
   - `summary.json` hash
   - threshold profile digest
   - `collapse_watch_interpretation.json`
   - `gate_assessment.json`
3. post-migration detector snapshot on the same frozen row set:
   - migrated detector input artifact hash
   - detector outputs
   - triggered rule IDs and status
4. rollback trigger conditions record:
   - detector status divergence policy
   - rule-trigger divergence policy
   - noncomputable escalation conditions
   - missing-artifact escalation conditions
5. noncomputable fallback record for authoritative input failure modes:
   - missing row-fact artifact
   - missing scorer-evidence artifact
   - unresolved `row_id` join
   - denominator failure
6. audit preservation manifest:
   - manifest identity
   - row-set identity
   - pre/post artifact paths
   - raw hashes
   - normalized semantic digests
   - reviewer decision record
7. failed-attempt preservation record when applicable:
   - rollback invocation reason
   - preserved pre/post outputs
   - preserved noncomputable evidence
   - retained gate decision artifacts

Package 2C does not implement these artifacts.

It records them as the minimum future preservation set for any later authorized migration attempt.

## Rollback Review Determination

The Package 1E rollback-review requirement is satisfied for `read_file_exact_valid_rate`.

Basis:

1. the rollback guarantees are now explicit and surface-specific;
2. the live legacy detector path is demonstrably recoverable in current repo state;
3. legacy and Stage C outputs are demonstrably separable in current repo state;
4. noncomputable expectations for missing or unstable evidence are explicit in both active detector behavior and governing doctrine;
5. current audit evidence preservation is already strong enough to support rollback review;
6. the remaining partial items are future migration-attempt artifacts, now explicitly inventoried rather than left implicit.

## Governance Concerns

1. The active detector still has no authoritative Stage C input path for this surface, so authoritative missing-input behavior is not runtime-executed yet.
2. Failed-attempt preservation is currently contractual and inventory-based, not exercised by an actual migration attempt.
3. These concerns remain compatible with a gate-evidence completion determination because no migration authority is being changed in this package.

## Determination

Package 2C closes the final Package 1E rollback-review evidence gap for `read_file_exact_valid_rate`.

## Boundary Confirmation

This rollback review does not:

1. modify detector behavior;
2. modify threshold behavior;
3. alter threshold profiles;
4. create replacement metrics;
5. implement rollback behavior;
6. authorize migration.
