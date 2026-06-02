# Stage C9-D No-Anchor Metric Disposition Closure Determination

## Scope

This determination closes the Stage C9-D no-anchor metric disposition review.

Decision boundary:

1. reconstruct authoritative no-anchor findings from C7, C8, C9-B, and C9 post-blocker reassessment;
2. assess candidate dispositions for `no_anchor_exact_valid_share`;
3. select the smallest authority-consistent disposition;
4. classify blocker status under the selected disposition;
5. determine closure readiness.

This determination does not authorize detector migration or threshold-profile migration.

## Inputs

1. `docs/convergence/STAGE_C9D_NO_ANCHOR_METRIC_DISPOSITION_REVIEW.md`
2. `docs/convergence/STAGE_C7_DETECTOR_PROJECTION_MIGRATION_IMPLEMENTATION_GATE.md`
3. `docs/convergence/STAGE_C7_DETECTOR_PROJECTION_MIGRATION_GATE_DETERMINATION.md`
4. `docs/convergence/STAGE_C8_NON_AUTHORITATIVE_DETECTOR_PROJECTION_ADAPTER.md`
5. `docs/convergence/STAGE_C8_DETECTOR_PROJECTION_ADAPTER_CONFORMANCE_REPORT.md`
6. `docs/convergence/STAGE_C9B_NO_ANCHOR_SEMANTIC_EQUIVALENCE_BRIDGE_REVIEW.md`
7. `docs/convergence/STAGE_C9B_NO_ANCHOR_SEMANTIC_EQUIVALENCE_CLOSURE_DETERMINATION.md`
8. `docs/convergence/STAGE_C9_POST_BLOCKER_REASSESSMENT.md`
9. `docs/convergence/STAGE_C9_POST_BLOCKER_MIGRATION_READINESS_DETERMINATION.md`
10. `docs/convergence/STAGE_B_B2_NO_ANCHOR_MEMBERSHIP_REVIEW.md`
11. `manifests/reports/stage_b_v1_threshold_profile.json`
12. `manifests/reports/stage_b_wp8_validation/fixtures/family_b2/b2_ni_002_historical_no_anchor_share_denominator_incompatible.json`

## Determinations

1. Authoritative equivalence is not supported.
2. Authoritative replacement is not supported in current scope.
3. Authoritative retirement is not supported in current scope.
4. Authoritative noncomputable preservation is supported and selected.
5. `no_anchor_exact_valid_share` must remain visible as a legacy detector metric identity with `projection_status=noncomputable_blocked`.
6. The selected reason code remains `blocked_no_anchor_share_semantic_mismatch`.
7. Stage C B2 no-anchor governed-rate evidence must not be substituted into `no_anchor_exact_valid_share`.
8. The no-anchor metric disposition blocker is resolved at authority-disposition level.
9. Stage C9-D is closure-ready.
10. Detector migration remains unauthorized.
11. Threshold-profile migration remains unauthorized.

## Basis

### Determination 1 Basis

C9-B determines that the legacy denominator is exact-valid rows in the historical anchor-bucket distribution, while Stage C B2 denominator is eligible rows in the declared no-anchor category. B2 doctrine and B2-NI-002 prohibit substituting the historical share for current no-anchor governed-rate evidence.

### Determination 2 Basis

Stage C B2 supports no-anchor governed-rate evidence, but no current authority defines a replacement detector metric, replacement threshold interpretation, threshold-profile migration, detector-consumer migration, or baseline compatibility decision.

### Determination 3 Basis

The legacy metric and threshold watch rule remain present in `stage_b_v1_threshold_profile.json`. No current authority removes the metric or accepts detector-consumer compatibility impact from removal.

### Determination 4 Basis

C7 blocks the metric due to semantic mismatch, C8 emits it as `noncomputable_blocked`, C9-B confirms semantic equivalence is unavailable, and B2 doctrine requires non-substitution. These authorities jointly support preserving the metric as visible but noncomputed.

### Determinations 5-7 Basis

C8 already uses `projection_status=noncomputable_blocked`, `value=null`, and reason code `blocked_no_anchor_share_semantic_mismatch`. C9-D confirms this is the smallest authority-consistent disposition and prohibits B2 governed-rate substitution.

### Determination 8 Basis

The unresolved C9 post-blocker issue was disposition, not semantic equivalence itself. C9-D supplies the missing disposition by selecting noncomputable preservation. This resolves the no-anchor blocker at authority-disposition level without making the metric computable.

### Determination 9 Basis

The review reconstructs the authority trail, assesses all requested candidate dispositions, selects the smallest authority-consistent disposition, records governance implications, and preserves all migration-disabled boundaries.

## Active Blockers

Active blockers after Stage C9-D:

1. adversarial no-call emitted-evidence and adapter handling remain partially resolved from C9-A;
2. C9-C baseline-delta gate behavior remains unimplemented in non-authoritative adapter outputs;
3. C9-D noncomputable preservation must be carried into any later adapter planning or validation evidence;
4. authoritative detector migration still requires a refreshed migration gate;
5. threshold-profile migration remains separately unauthorized.

## Recommended Next Controlled Step

Recommended next controlled step:

- Stage C10-A Non-Authoritative C9 Contract Integration Adapter Planning.

Reason:

1. C9-A supplies adversarial subset mapping authority but not emitted adapter behavior.
2. C9-C supplies baseline-delta gate authority but not emitted adapter behavior.
3. C9-D supplies no-anchor noncomputable-preservation authority.
4. A bounded planning slice can define the exact non-authoritative adapter integration path while preserving migration-disabled status.

## Boundary Confirmation

This determination does not expand authorized scope.

This determination does not authorize:

1. detector migration;
2. threshold-profile migration;
3. replacement of existing detector outputs;
4. evaluator runtime behavior changes;
5. detector code changes;
6. fixture catalog changes;
7. governance doctrine redesign.
