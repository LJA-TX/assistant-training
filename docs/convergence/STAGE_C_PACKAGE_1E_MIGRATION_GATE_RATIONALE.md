# Stage C Package 1E Migration Gate Rationale

## Scope

This artifact defines the formal migration gate that separates:

1. passive readiness assessment; from
2. actual detector or threshold migration authorization work.

This is a governance and assessment slice only.

It does not:

1. migrate detector authority;
2. migrate threshold authority;
3. alter comparability policy;
4. create replacement metrics;
5. authorize migration by itself.

## Why Package 1E Is Needed

Stage C Package 1D introduced readiness states, including `migration-ready`, but explicitly recorded that `migration-ready` is an assessment state only and not a cutover decision.

Existing authority already requires that migration-disabled posture remain unchanged:

1. `authoritative_detector_output=false`
2. `detector_migration_enabled=false`
3. `threshold_profile_migration_enabled=false`

Source authority:

1. `docs/convergence/STAGE_C10C_REFRESHED_DETECTOR_MIGRATION_GATE_DETERMINATION.md`
2. `docs/convergence/STAGE_C9_POST_BLOCKER_MIGRATION_READINESS_DETERMINATION.md`
3. `docs/convergence/STAGE_C_PACKAGE_1D_ACCEPTANCE_ASSESSMENT.md`

Package 1E therefore defines the missing governance layer between:

1. a surface being judged ready enough for further review; and
2. a later explicitly authorized migration slice.

## Gate-State Taxonomy

### `gate-open`

Use when:

1. the surface is already `migration-ready` in Package 1D;
2. the minimum gate evidence bundle is complete;
3. no active blocker remains in guardrail, legacy-stability, row-identity, reconciliation, detector-impact, threshold-impact, or rollback review.

`gate-open` does not authorize migration implementation by itself.

It means only that a later migration slice may be requested without violating current governance.

### `gate-not-open`

Use when:

1. the surface is conceptually migration-eligible; but
2. the required gate evidence bundle is incomplete.

This is the expected state for a surface that is `migration-ready` in bounded evidence but lacks full-run or migration-impact evidence.

### `gate-blocked`

Use when:

1. the surface is conceptually comparable; but
2. current authoritative evidence exposes an explicit blocker that must remain visible.

Examples:

1. preserved missing subtype evidence;
2. explicit linkage incompleteness;
3. guardrail instability;
4. unresolved baseline-delta or detector-impact blockers.

### `not-gate-eligible`

Use when:

1. current authority does not permit the surface to enter migration gating at all.

Examples:

1. semantic non-equivalence;
2. authoritative noncomputable-preservation disposition;
3. explicit doctrine that the legacy surface is not a migratable replacement target.

## Minimum Gate Criteria For A `migration-ready` Surface

For a surface already marked `migration-ready` in Package 1D, the minimum criteria before migration can be authorized are:

### 1. Repeated Runtime Evidence

Required minimum:

1. at least one bounded evidence run already reviewed;
2. at least one full canonical run over the same manifest without bounded sampling;
3. at least one repeated full canonical rerun over the same frozen row set.

Reason:

1. bounded sample evidence proves consumer behavior only;
2. full-run evidence is required before migration review can rely on corpus-wide coverage;
3. repeated full-run evidence is the smallest reproducibility check for migration gating.

### 2. Full-Run Evidence Requirement

Bounded sample evidence is necessary but insufficient.

`gate-open` cannot be assigned on bounded-sample validation alone.

Basis:

1. Package 1D runtime validation used `--max-samples-per-split 3`;
2. Stage C5 already records scale-up from bounded sample to wider corpus execution as an outstanding milestone.

### 3. Guardrail Stability

Across all gate-evidence runs:

1. inference behavior must remain false;
2. substitution behavior must remain false;
3. reconstruction behavior must remain false;
4. legacy-summary modification must remain false;
5. legacy-detector-surface modification must remain false.

### 4. Legacy-Surface Stability

Across all gate-evidence runs:

1. `summary.json` must remain preserved;
2. `comparison_rows.jsonl` must remain preserved;
3. detector-facing legacy outputs must remain unchanged under passive Stage C consumers;
4. threshold-facing legacy inputs must remain unchanged under passive Stage C consumers.

### 5. Row-Identity Stability

Across full-run evidence:

1. `row_id` uniqueness must hold;
2. row resolution from scorer evidence to row facts must hold;
3. the frozen row set and split ordering must remain unchanged for repeated gate runs.

Basis:

1. Package 1A defines current row-identity stability only for the same frozen row set and split ordering.

### 6. Reconciliation Stability

Across the full-run evidence bundle:

1. the relevant Package 1C reconciliation status must remain stable;
2. the relevant Package 1D readiness state must remain stable;
3. any transition from aligned/ready to blocked, unavailable, or non-comparable prevents `gate-open`.

### 7. Readiness-Report Reproducibility

For repeated assessment on the same run directory:

1. the Package 1D readiness artifact must be deterministic;
2. the same integrity-check results must be reproduced;
3. the same readiness determination must be reproduced.

### 8. Detector / Threshold Impact Assessment

Before migration can be authorized, the surface must have an explicit impact review covering:

1. which detector-facing consumer path would be affected;
2. which threshold rules depend on the surface;
3. whether baseline-delta or comparability gates apply;
4. whether any noncomputable or blocked legacy behavior must be preserved during migration.

This is required because the active threshold profile still binds the four legacy surfaces directly.

### 9. Rollback Requirements

Before migration can be authorized, the surface must have an explicit rollback record proving:

1. prior detector behavior remains recoverable;
2. old and new outputs remain separable during migration review;
3. partial or unstable evidence becomes noncomputable rather than silently passing;
4. audit artifacts are retained for failed attempts.

Basis:

1. `docs/convergence/STAGE_B_EVAL_REDESIGN_IMPLEMENTATION_READINESS.md`
2. `docs/convergence/STAGE_B_WP3_SCORER_EVIDENCE_OUTPUT_DESIGN_REVIEW.md`

## Why No Checker Is Added In Package 1E

Package 1E remains documentation-only.

A read-only checker is not yet justified because the gate depends on evidence that is not currently standardized as machine-consumable inputs:

1. repeated full-run evidence bundles;
2. surface-specific detector-impact review records;
3. surface-specific threshold-impact review records;
4. rollback-review records.

Encoding a checker before those artifacts exist would hard-code policy assumptions without a stable evidence contract.

## Boundary Confirmation

This rationale does not authorize:

1. detector migration;
2. threshold-profile migration;
3. migration flag changes;
4. detector projection changes;
5. threshold projection changes;
6. historical metric replacement.
