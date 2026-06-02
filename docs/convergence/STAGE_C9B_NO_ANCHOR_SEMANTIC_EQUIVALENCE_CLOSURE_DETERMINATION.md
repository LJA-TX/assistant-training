# Stage C9-B No-Anchor Semantic-Equivalence Closure Determination

## Scope

This determination closes the Stage C9-B no-anchor semantic-equivalence bridge review slice.

Decision boundary:

1. determine the authoritative legacy detector metric definition for `no_anchor_exact_valid_share`;
2. identify Stage C emitted concepts and evidence surfaces that could relate to the metric;
3. determine whether semantic equivalence can be established;
4. identify exact missing authority and smallest safe blocker-closure path if equivalence cannot be established;
5. determine blocker status and Stage C9-B closure readiness.

This determination does not authorize detector migration or threshold-profile migration.

## Inputs

1. `AGENTS.md`
2. `docs/convergence/STAGE_C9B_NO_ANCHOR_SEMANTIC_EQUIVALENCE_BRIDGE_REVIEW.md`
3. `docs/convergence/STAGE_C9_BLOCKER_CLOSURE_PLANNING_ASSESSMENT.md`
4. `docs/convergence/STAGE_C7_DETECTOR_PROJECTION_MIGRATION_IMPLEMENTATION_GATE.md`
5. `docs/convergence/STAGE_C8_NON_AUTHORITATIVE_DETECTOR_PROJECTION_ADAPTER.md`
6. `docs/convergence/STAGE_B_EVAL_REDESIGN_METRIC_INVENTORY.md`
7. `docs/convergence/STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
8. `docs/convergence/STAGE_B_EVAL_REDESIGN_EMISSION_DESIGN.md`
9. `docs/convergence/STAGE_B_B2_NO_ANCHOR_MEMBERSHIP_REVIEW.md`
10. `docs/convergence/STAGE_B_EVAL_REDESIGN_SCHEMA_PROPOSAL.md`
11. `manifests/reports/stage_b_v1_threshold_profile.json`
12. Family B2 fixture corpus
13. Stage C1 through C8 implementation/reporting surfaces relevant to B2 and detector projection

## Determinations

1. The authoritative legacy metric path is `failure_profile.anchor_exact_share.no_anchor_phrase`.
2. The authoritative legacy metric represents a share of exact-valid rows in the historical no-anchor prompt bucket, not a no-anchor exact-valid performance rate.
3. The closest Stage C concept is `Family B2` / `No-anchor governed sub-slice`.
4. The Stage C B2 denominator is eligible rows in the declared no-anchor category.
5. Semantic equivalence cannot be established from current authoritative evidence.
6. The no-anchor semantic-equivalence bridge blocker remains unresolved for authoritative detector migration.
7. Stage C9-B is closure-ready as a contract-definition and evidence-mapping review slice.
8. Detector migration remains unauthorized.
9. Threshold-profile migration remains unauthorized.

## Basis

### Determination 1 Basis

`manifests/reports/stage_b_v1_threshold_profile.json` maps `no_anchor_exact_valid_share` to `failure_profile.anchor_exact_share.no_anchor_phrase` and uses it in the tradeoff watch rule `no_anchor_exact_valid_share_lt_0_75`.

### Determination 2 Basis

Historical procedural-generalization artifacts compute `anchor_distribution_exact_valid.shares.no_anchor_phrase` from exact-valid anchor-bucket counts. Canonical eval summaries expose the same value under `failure_profile.anchor_exact_share.no_anchor_phrase`.

### Determination 3 Basis

Stage B redesign contracts retain the no-anchor concern by merging it into Family B2 as a governed no-anchor anchor-generalization sub-slice.

### Determination 4 Basis

`STAGE_B_B2_NO_ANCHOR_MEMBERSHIP_REVIEW.md` approves the no-anchor governed-rate denominator as eligible rows in the declared no-anchor category. B2 complete fixtures encode exact-valid and non-exact no-anchor rows against that denominator.

### Determination 5 Basis

The denominator semantics are not equivalent:

1. legacy denominator: exact-valid rows in the historical anchor-bucket distribution;
2. Stage C denominator: eligible rows in the declared no-anchor category.

The repository explicitly prohibits substituting the historical share for the current B2 rate. `B2-NI-002` encodes the incompatible historical no-anchor share as `bridge-required` and `current-run noncomputable`.

### Determination 6 Basis

C7 and C8 already classify `no_anchor_exact_valid_share` as blocked due to semantic mismatch. C9-B confirms that no current authority supplies the required taxonomy, ownership, denominator, provenance, or comparability bridge.

### Determination 7 Basis

Stage C9-B satisfies the requested bounded scope by identifying the legacy definition, related Stage C concepts, missing authority, noncomputable conditions, and smallest safe path while preserving all migration-disabled boundaries.

## Active Blockers

Active blockers after Stage C9-B:

1. no-anchor semantic-equivalence bridge remains unresolved;
2. baseline-delta comparability gate remains unresolved;
3. any future no-anchor detector-projection change requires a metric disposition decision and a later migration gate.

C9-A adversarial no-call mapping remains partially resolved at contract level from the prior slice.

## Recommended Next Controlled Step

Recommended next controlled step:

- Stage C9-C Baseline-Delta Comparability Gate Contract.

Reason:

1. C9-B established that no-anchor equivalence cannot be safely bridged from current evidence;
2. detector migration remains blocked regardless of no-anchor disposition until baseline-delta comparability is addressed;
3. no-anchor disposition should be handled as a later migration-authority decision, not as an implicit equivalence bridge.

Alternative controlled step if no-anchor remains priority:

- produce a no-anchor metric disposition authority artifact deciding whether the legacy share metric is preserved separately, replaced by a renamed B2 governed-rate metric, or held reference-only.

## Boundary Confirmation

This determination does not expand authorized scope.

This determination does not authorize:

1. detector migration;
2. threshold-profile migration;
3. replacement of existing detector outputs;
4. evaluator runtime behavior changes;
5. fixture catalog changes;
6. governance doctrine redesign;
7. detector code changes.
