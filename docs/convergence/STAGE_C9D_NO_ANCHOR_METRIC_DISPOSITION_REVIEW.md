# Stage C9-D No-Anchor Metric Disposition Review

## Scope

This review determines the authoritative disposition of the unresolved `no_anchor_exact_valid_share` detector-migration blocker.

Route selected from `AGENTS.md`: `migration_gate`.

This is an authority and governance analysis only. It does not implement evaluator behavior, modify detector behavior, modify threshold profiles, authorize detector migration, or authorize threshold-profile migration.

## Authoritative Inputs Reviewed

1. `AGENTS.md`
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
13. Stage C0 contract-lock artifacts and Stage B closure artifacts as referenced by C7 through C9-B

## Reconstructed Authoritative Findings

### C7 Migration Gate

C7 identified `no_anchor_exact_valid_share` as a legacy detector metric mapped to:

- `failure_profile.anchor_exact_share.no_anchor_phrase`

C7 classified the closest Stage C source as the `No-anchor governed sub-slice` rate, but blocked projection because the legacy share definition was semantically mismatched with the current B2 emitted surface.

C7 did not approve authoritative detector projection migration.

### C8 Non-Authoritative Adapter

C8 implemented a non-authoritative projection adapter and left `no_anchor_exact_valid_share` explicitly blocked:

- `projection_status=noncomputable_blocked`
- `value=null`
- reason code `blocked_no_anchor_share_semantic_mismatch`

C8 preserved:

- `authoritative_detector_output=false`
- `detector_migration_enabled=false`
- `threshold_profile_migration_enabled=false`

C8 compatibility validation confirmed that blocked detector rules remain readable as noncomputable rather than inferred, substituted, or dropped.

### C9-B Semantic-Equivalence Review

C9-B determined:

1. The legacy metric path is `failure_profile.anchor_exact_share.no_anchor_phrase`.
2. The legacy metric is a distribution-of-successes metric: share of exact-valid rows assigned to the historical no-anchor bucket.
3. The closest Stage C concept is `Family B2` / `No-anchor governed sub-slice`.
4. Stage C B2 no-anchor governed-rate denominator is eligible rows in the declared no-anchor category.
5. The legacy denominator and Stage C denominator answer different questions.
6. Semantic equivalence cannot be established from current authority.
7. The Stage C B2 governed rate must not be substituted into `no_anchor_exact_valid_share`.

C9-B identified three possible future dispositions:

1. preserve the legacy share metric as a separately emitted Stage C surface;
2. replace it with a renamed B2 no-anchor governed-rate detector metric through an explicit non-equivalence migration;
3. keep the legacy metric reference-only/noncomputable and use B2 governed-rate evidence separately for review.

### C9 Post-Blocker Reassessment

The C9 post-blocker reassessment classified no-anchor semantic equivalence as unresolved because no later artifact had selected a metric disposition.

It recommended resolving disposition before treating no-anchor as closed for later detector-migration planning.

## Candidate Disposition Assessment

### Candidate 1: Authoritative Equivalence

Disposition:

- Treat `no_anchor_exact_valid_share` as semantically equivalent to the Stage C B2 no-anchor governed-rate surface.

Supporting authority:

- C9-B identifies B2 no-anchor governed sub-slice as the closest related Stage C concept.
- Both concepts may involve exact-valid no-anchor rows when explicit category and scorer evidence exist.

Missing authority:

1. approved taxonomy bridge equating historical `no_anchor_phrase` bucket assignment with Stage C no-anchor category assignment;
2. approved ownership bridge from historical prompt-derived bucket assignment to Stage C dataset/evaluator-owned category assignment;
3. denominator bridge equating share-of-exact-valid denominator semantics to eligible-no-anchor denominator semantics;
4. current-run emitted exact-valid-share surface;
5. migration-gate approval for semantic equivalence.

Governance implications:

1. would violate denominator non-substitution doctrine;
2. would collapse a historical share metric into a governed-rate metric;
3. would permit detector inference from historical report structure;
4. would contradict B2 no-anchor membership doctrine and B2-NI-002.

Disposition support status: **not supported**.

### Candidate 2: Authoritative Replacement

Disposition:

- Replace `no_anchor_exact_valid_share` with a renamed Stage C B2 no-anchor governed-rate detector metric.

Supporting authority:

- Stage B and Stage C preserve no-anchor behavior as a governed B2 sub-slice.
- B2 doctrine authorizes current-run no-anchor governed-rate computation when explicit membership, denominator, scorer, ownership, and provenance evidence exist.

Missing authority:

1. explicit threshold-profile migration authority;
2. detector-consumer migration authority for replacing a legacy metric ID or rule;
3. named replacement metric contract;
4. threshold interpretation for the replacement metric;
5. baseline compatibility decision for non-equivalent metric replacement;
6. migration-gate approval.

Governance implications:

1. replacement is not semantic equivalence and must not be hidden under the legacy metric ID;
2. replacement would require threshold-profile migration, which remains prohibited in this slice;
3. replacement may be valid in a future migration milestone, but current authority does not authorize it.

Disposition support status: **not supported in current scope**.

### Candidate 3: Authoritative Retirement

Disposition:

- Remove `no_anchor_exact_valid_share` from detector projection and threshold watch handling.

Supporting authority:

- Current authority shows the metric cannot be computed safely from Stage C B2 governed-rate surfaces.

Missing authority:

1. threshold-profile retirement authority;
2. detector-consumer compatibility authority for removing the metric and rule;
3. publication or migration decision accepting loss of the legacy watch signal;
4. replacement or reference strategy for historical reports that still expose the metric.

Governance implications:

1. retirement would alter legacy detector surface expectations;
2. retirement could hide an unresolved semantic issue rather than preserving evidence;
3. retirement would exceed this authority-analysis slice.

Disposition support status: **not supported in current scope**.

### Candidate 4: Authoritative Noncomputable Preservation

Disposition:

- Preserve `no_anchor_exact_valid_share` as a visible legacy detector metric record, but keep it noncomputed and blocked unless future authority supplies a separate exact-valid-share contract or an explicit replacement/retirement migration.

Supported current representation:

1. `projection_status=noncomputable_blocked`
2. `value=null`
3. reason code `blocked_no_anchor_share_semantic_mismatch`
4. evidence references to C7/C8/C9-B/C9-D authority
5. no use of Stage C B2 governed rate as the metric value
6. no threshold rule evaluation as a computed pass/fail value

Supporting authority:

1. C7 blocks the metric due to semantic mismatch.
2. C8 already emits the metric as `noncomputable_blocked`.
3. C8 compatibility checks preserve consumer readability for noncomputable rules.
4. C9-B determines semantic equivalence cannot be established.
5. B2 no-anchor doctrine prohibits denominator substitution.
6. B2-NI-002 requires bridge-required and current-run noncomputable handling for denominator-incompatible historical no-anchor share.
7. The C9 post-blocker reassessment identifies a disposition authority as the missing step.

Missing authority:

- None for preserving the metric as noncomputable and blocked.

Future authority would be required only to compute, replace, retire, or migrate the metric.

Governance implications:

1. preserves legacy metric visibility without inventing a value;
2. preserves threshold-profile readability without threshold-profile migration;
3. prevents denominator substitution;
4. prevents prompt-text or report-layer inference;
5. keeps detector as a consumer rather than category owner;
6. maintains migration-disabled posture.

Disposition support status: **supported and selected**.

### Candidate 5: Other Authoritative Disposition

Possible other disposition:

- Treat historical `no_anchor_exact_valid_share` as reference-only reporting context while emitting Stage C B2 no-anchor governed-rate evidence separately.

Supporting authority:

- B2 doctrine allows historical no-anchor values to remain `bridge-required` or `reference-only` when denominator compatibility or ownership comparability is unresolved.
- C9-B identifies reference-only handling as a possible safe path.

Missing authority:

1. reporting-surface contract for reference-only historical context;
2. detector-consumer contract if reference-only context appears beside detector metrics;
3. migration-gate approval if detector consumers treat reference-only fields as actionable.

Governance implications:

1. reference-only context is compatible with noncomputable preservation;
2. reference-only context must not become a computed detector metric;
3. reference-only reporting is optional and outside current implementation scope.

Disposition support status: **compatible with selected noncomputable preservation, but not independently required**.

## Smallest Authority-Consistent Disposition

The smallest authority-consistent disposition is:

**authoritative noncomputable preservation**.

Required disposition contract:

1. `no_anchor_exact_valid_share` remains a legacy detector metric identity for compatibility and evidence visibility.
2. The metric remains `noncomputable_blocked` under current authority.
3. The metric value remains absent/null.
4. The governing reason code remains `blocked_no_anchor_share_semantic_mismatch`.
5. Stage C B2 no-anchor governed-rate evidence must not be substituted into this metric.
6. Historical `failure_profile.anchor_exact_share.no_anchor_phrase` values may be reference context only and must not serve as current-run computed evidence.
7. Threshold rule `no_anchor_exact_valid_share_lt_0_75` remains noncomputable when its source metric is noncomputable.
8. Any later computation requires a separate exact-valid-share contract with numerator, denominator, taxonomy, ownership, provenance, row-set, split-scope, scorer-semantics, and comparability evidence.
9. Any later replacement or retirement requires explicit threshold-profile and detector-consumer migration authority.
10. Detector migration and threshold-profile migration remain disabled.

## Ownership Under Selected Disposition

1. Legacy metric identity and threshold-rule references are owned by the existing threshold profile and historical detector/report surfaces.
2. Stage C B2 no-anchor governed-rate evidence is owned by the evaluator aggregation path using explicit membership, denominator, scorer, provenance, and ownership fields.
3. The selected noncomputable preservation disposition is owned by this migration-gate determination path.
4. The detector remains a consumer only and does not own no-anchor category assignment, denominator construction, or migration bridging.
5. Any future metric replacement, retirement, or threshold change must be owned by a later migration-gate or threshold-profile migration authority.

## Blocker Status Under Selected Disposition

Blocker classification: **resolved at authority-disposition level**.

Reason:

1. C9-D resolves the previously missing disposition decision.
2. The selected disposition is noncomputable preservation, not semantic equivalence.
3. No current authority gap remains for keeping `no_anchor_exact_valid_share` visible and blocked.
4. Implementation and refreshed migration-gate validation remain future work for any broader detector migration path.

This does not make the metric computable.

This does not authorize detector migration.

This does not authorize threshold-profile migration.

## Impact On Remaining Detector-Migration Readiness

No-anchor disposition no longer blocks later planning as an undecided semantic issue, provided later slices preserve it as noncomputable blocked.

Authoritative detector migration remains blocked overall until at least:

1. adversarial no-call emitted-evidence and adapter handling are addressed;
2. C9-C baseline-delta gate behavior is represented in non-authoritative adapter outputs;
3. C9-D noncomputable preservation is reflected in later adapter planning or validation evidence;
4. a refreshed migration gate determines migration readiness;
5. threshold-profile migration remains separately gated if any threshold behavior changes.

## Validation Results

Validation evidence captured for this review:

1. Direct review of C7 migration gate: pass, no-anchor metric classified as blocked due to semantic mismatch.
2. Direct review of C8 adapter/conformance artifacts: pass, metric is emitted as `noncomputable_blocked` with reason `blocked_no_anchor_share_semantic_mismatch`.
3. Direct review of C9-B review and closure determination: pass, semantic equivalence cannot be established and denominator substitution is prohibited.
4. Direct review of C9 post-blocker reassessment: pass, disposition authority is identified as the remaining no-anchor blocker.
5. Direct review of `stage_b_v1_threshold_profile.json`: pass, metric path and watch rule remain present.
6. Direct review of B2 no-anchor membership review: pass, historical share cannot be substituted for no-anchor governed rate.
7. Direct review of B2-NI-002 fixture: pass, denominator-incompatible historical no-anchor share is bridge-required and current-run noncomputable.
8. Review for migration-enabled behavior in this slice: pass, no detector or threshold migration enabled.

## Governance Concerns

No new governance doctrine is introduced.

Active governance concerns retained:

1. The legacy metric must not be computed from Stage C B2 governed-rate surfaces.
2. Historical report-layer values must not become current-run computed evidence.
3. Prompt text, output style, path conventions, and absence of markers must not determine no-anchor membership.
4. Noncomputable preservation must not be misreported as retirement.
5. Noncomputable preservation must not be misreported as threshold-profile migration.
6. Detector migration remains unauthorized pending a refreshed migration gate.

## Residual Ambiguities

No residual ambiguity remains for current no-anchor disposition.

Residual future decisions remain outside this slice:

1. whether to create a separate current-run exact-valid-share surface for the legacy metric;
2. whether to introduce a renamed B2 no-anchor governed-rate detector metric;
3. whether to retire the legacy metric and threshold rule in a later threshold-profile migration;
4. whether to emit historical no-anchor values as reference-only reporting context.

## Determination

Stage C9-D selects authoritative noncomputable preservation for `no_anchor_exact_valid_share`.

The no-anchor metric disposition blocker is closure-ready.

Authoritative detector migration remains blocked overall.

Migration-disabled posture remains mandatory and unchanged.

## Boundary Confirmation

This review did not modify evaluator runtime code, detector code, threshold profiles, fixture catalogs, fixture definitions, governance doctrine, or repository process infrastructure.

This review does not authorize detector migration, threshold-profile migration, live inference, or replacement of existing detector outputs.
