# Stage C9-B No-Anchor Semantic-Equivalence Bridge Review

## Scope

This review addresses the Stage C9-B no-anchor semantic-equivalence bridge blocker at the contract-definition and evidence-mapping level only.

Route selected from `AGENTS.md`: `migration_gate`.

This review does not implement evaluator behavior, modify detector behavior, modify threshold profiles, authorize detector migration, or authorize threshold-profile migration.

## Authoritative Inputs Reviewed

1. `AGENTS.md`
2. `docs/convergence/STAGE_C9_BLOCKER_CLOSURE_PLANNING_ASSESSMENT.md`
3. `docs/convergence/STAGE_C9_BLOCKER_CLOSURE_READINESS_DETERMINATION.md`
4. `docs/convergence/STAGE_C7_DETECTOR_PROJECTION_MIGRATION_IMPLEMENTATION_GATE.md`
5. `docs/convergence/STAGE_C7_DETECTOR_PROJECTION_MIGRATION_GATE_DETERMINATION.md`
6. `docs/convergence/STAGE_C8_NON_AUTHORITATIVE_DETECTOR_PROJECTION_ADAPTER.md`
7. `docs/convergence/STAGE_C8_DETECTOR_PROJECTION_ADAPTER_CONFORMANCE_REPORT.md`
8. `docs/convergence/STAGE_B_EVAL_REDESIGN_METRIC_INVENTORY.md`
9. `docs/convergence/STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
10. `docs/convergence/STAGE_B_EVAL_REDESIGN_EMISSION_DESIGN.md`
11. `docs/convergence/STAGE_B_EVAL_REDESIGN_SCHEMA_PROPOSAL.md`
12. `docs/convergence/STAGE_B_EVAL_REDESIGN_SCHEMA_READINESS.md`
13. `docs/convergence/STAGE_B_B2_NO_ANCHOR_MEMBERSHIP_REVIEW.md`
14. `docs/convergence/STAGE_B_B2_READINESS_CLOSURE_ASSESSMENT.md`
15. `docs/convergence/STAGE_B_WP8A_SCENARIO_CATALOG.md`
16. Family B2 fixture corpus under `manifests/reports/stage_b_wp8_validation/fixtures/family_b2/`
17. `manifests/reports/stage_b_v1_threshold_profile.json`
18. historical procedural-generalization and canonical eval summary artifacts containing `anchor_exact_share`
19. Stage C1 through C8 implementation and reporting surfaces relevant to B2 membership, denominator, provenance, and detector projection

## Legacy Metric Definition

Legacy detector metric ID:

- `no_anchor_exact_valid_share`

Legacy detector path:

- `failure_profile.anchor_exact_share.no_anchor_phrase`

Threshold profile role:

- consumed by tradeoff watch rule `no_anchor_exact_valid_share_lt_0_75` in `manifests/reports/stage_b_v1_threshold_profile.json`.

Historical producer evidence:

1. `docs/convergence/STAGE_B_EVAL_REDESIGN_METRIC_INVENTORY.md` identifies historical fields under `failure_profile.anchor_exact_share.no_anchor_phrase`.
2. `manifests/reports/stage_b_v1_i10r_microprobe_procedural_generalization_assessment.json` records `anchor_distribution_exact_valid.shares.no_anchor_phrase = 0.862069` from exact-valid anchor-bucket counts.
3. `manifests/reports/stage_b_v1_i10r_counterbalanced_probe_procedural_generalization_assessment.json` records `anchor_distribution_exact_valid.shares.no_anchor_phrase = 0.8369565217391305` from exact-valid anchor-bucket counts.
4. `manifests/reports/stage_b_v1_i10r_nocall_probe_canonical_eval_summary.json` records `failure_profile.anchor_exact_share.no_anchor_phrase = 0.8513513513513513`.
5. `manifests/reports/stage_b_v1_i10r_counterbalanced_probe_canonical_eval_summary.json` records `failure_profile.anchor_exact_share.no_anchor_phrase = 0.8369565217391305`.

Historical bucket logic evidence:

1. `scripts/i9_diagnostics_scaffold.py` and `scripts/i10_diagnostics_scaffold.py` include `_prompt_anchor_bucket` logic.
2. Bucket labels include `literal_tool_calls`, `paraphrastic_tool_call`, `schema_paraphrase`, and `no_anchor_phrase`.
3. The historical bucket assignment is prompt-text derived and is not detector-safe under Stage B/C non-inference doctrine.

Legacy numerator and denominator interpretation:

1. Numerator: exact-valid rows assigned to historical bucket `no_anchor_phrase`.
2. Denominator: exact-valid rows assigned to the historical anchor-bucket distribution.
3. Interpretation: share of exact-valid rows that are no-anchor bucket rows.

This is a distribution-of-successes metric, not a no-anchor performance rate.

## Stage C And B2 Related Concepts

### Family B2 Governed Concept

The closest Stage C/B2 concept is:

- `Family B2` / `No-anchor governed sub-slice`

Authoritative B2 doctrine defines this as an anchor-generalization governed sub-slice.

B2 no-anchor governed-rate numerator:

- number of eligible rows in the declared no-anchor category that are exact-valid under scorer semantics.

B2 no-anchor governed-rate denominator:

- number of eligible rows in the declared no-anchor category.

This denominator is explicitly approved in `STAGE_B_B2_NO_ANCHOR_MEMBERSHIP_REVIEW.md`.

### Stage C Row-Fact And Evidence Surfaces

Stage C implementation surfaces that relate to B2 no-anchor evidence include:

1. `membership_markers.family_b2_anchor_eligible`
2. `membership_markers.family_b2_no_anchor_member`
3. `membership_markers.family_b2_anchor_category`
4. `ownership_markers.anchor_assignment_owner`
5. `ownership_markers.anchor_taxonomy_owner`
6. `denominator_provenance.anchor_population_source`
7. `denominator_provenance.no_anchor_population_source`
8. row provenance fields including row source, dataset ID, dataset version, extraction timestamp, and evidence digest
9. scorer exact-valid evidence
10. state axes for completeness, current-run computability, and comparability

These surfaces support the redesigned no-anchor governed rate, not the historical exact-valid-share metric unless additional denominator and taxonomy bridge evidence is approved.

### Stage C Aggregation And Projection Surfaces

Potentially related emitted or prepared surfaces include:

1. `Family B2` concept summary for `No-anchor governed sub-slice`.
2. B2 category and split-scoped fixture/reconciliation evidence.
3. C6 detector-projection preparation evidence for state axes, denominator provenance, and scoring evidence.
4. C8 non-authoritative detector projection adapter metric record for `no_anchor_exact_valid_share`, currently emitted as `noncomputable_blocked`.

Current C8 blocked reason:

- `blocked_no_anchor_share_semantic_mismatch`

## Semantic-Equivalence Analysis

A semantic-equivalence bridge cannot be established from current authoritative evidence.

### Numerator Comparison

The legacy metric and the B2 governed sub-slice can refer to a related numerator concept when both have explicit evidence:

- exact-valid no-anchor rows.

However, even numerator compatibility is not automatic because legacy historical bucket assignment was prompt-text derived and Stage B/C requires approved anchor-category assignment before detector consumption.

Numerator compatibility requires explicit authority for:

1. historical `no_anchor_phrase` bucket equivalence to the Stage C `no-anchor` category;
2. stable or bridged anchor taxonomy;
3. stable or bridged anchor assignment ownership;
4. stable exact-valid scorer semantics;
5. stable row population and split scope.

Current evidence does not provide that bridge.

### Denominator Comparison

The denominator is not equivalent.

Legacy denominator:

- exact-valid rows in the historical anchor-bucket distribution.

Stage C/B2 no-anchor governed-rate denominator:

- eligible rows in the declared no-anchor category, including exact-valid and non-exact rows.

These answer different questions:

1. legacy metric: among exact-valid rows, what share came from no-anchor bucket rows?
2. Stage C/B2 governed rate: among no-anchor eligible rows, what share became exact-valid?

The repository explicitly identifies this as denominator-incompatible:

1. `STAGE_B_EVAL_REDESIGN_CONTRACTS.md` states that the historical share-of-exact-valid interpretation must be separately contracted if needed because it answers a different denominator question.
2. `STAGE_B_B2_NO_ANCHOR_MEMBERSHIP_REVIEW.md` states that historical share of exact-valid rows that are no-anchor is a different denominator concept and cannot be substituted.
3. `B2-NI-002` encodes the historical denominator-incompatible no-anchor share case and requires bridge-required, current-run noncomputable treatment.
4. C7 and C8 classify the metric as blocked due to semantic mismatch.

## Bridge Determination

No semantic-equivalence bridge is established in this slice.

Reason:

1. denominator scope is not identical;
2. historical bucket assignment authority is not equivalent to Stage C B2 anchor-category assignment authority;
3. Stage C B2 governed-rate surfaces are intentionally redesigned and cannot be substituted for the legacy share metric;
4. no approved migration bridge equates historical `no_anchor_phrase` share with current `No-anchor governed sub-slice` rate;
5. detector migration remains disabled.

## Ownership Findings

### Legacy Metric Ownership

Legacy metric identity and threshold-rule ownership belongs to the Stage B threshold profile and historical detector/report surfaces.

The threshold profile owns the legacy metric path and watch threshold. It does not authorize denominator substitution.

### Historical Bucket Ownership

Historical bucket assignment was produced by diagnostic/eval scaffolding and dataset-builder logic.

Under Stage B/C doctrine, detector-time prompt scanning is not an acceptable ownership basis for current detector projection.

### Stage C B2 Ownership

Stage C B2 no-anchor governed sub-slice ownership is distributed as follows:

1. dataset metadata or explicitly approved evaluator pre-aggregation assignment owns anchor-category membership;
2. evaluator owns aggregation by anchor category and governed sub-slice summaries;
3. scorer owns exact-valid outcome;
4. migration/governance review owns any historical/current bridge approval;
5. detector is a consumer only.

## Exact Missing Authority

The exact missing authority required to establish semantic equivalence is:

1. approved taxonomy bridge mapping historical bucket `no_anchor_phrase` and sibling historical anchor buckets to Stage C approved anchor categories;
2. approved ownership bridge proving historical prompt-derived bucket assignment is comparable to Stage C dataset/evaluator-owned anchor assignment, or explicitly limiting historical values to reference-only status;
3. approved denominator bridge proving that share-of-exact-valid denominator semantics may feed a detector metric currently represented by B2 no-anchor governed-rate surfaces;
4. current-run emitted exact-valid-share surface if the legacy metric is to remain numerically preserved, including no-anchor exact-valid count and total exact-valid anchor-bucket denominator;
5. row-set, split-scope, scorer-semantics, exclusion-policy, and baseline/current comparability markers for the legacy share interpretation;
6. explicit migration-gate approval before any detector projection changes from `noncomputable_blocked` to computed.

Without these authorities, the only safe detector-facing status is noncomputable blocked or reference-only, depending on later reporting needs.

## Smallest Safe Blocker-Closure Path

The smallest safe path is not to map the legacy metric to the Stage C B2 governed rate.

Recommended path:

1. Produce a no-anchor metric disposition authority artifact deciding whether the detector migration should preserve the legacy exact-valid-share metric, replace it with a renamed B2 no-anchor governed-rate metric, or keep the legacy metric reference-only.
2. If preserving the legacy metric, contract a separate Stage C exact-valid-share surface with numerator `no-anchor exact-valid count` and denominator `total exact-valid rows across approved anchor categories`.
3. If replacing the legacy metric, require a threshold-profile and detector-consumer migration gate that explicitly recognizes the metric is not semantically equivalent and therefore is not a direct migration.
4. If keeping it reference-only, leave `no_anchor_exact_valid_share` noncomputable for detector projection and emit B2 governed-rate evidence separately for human review.
5. In all paths, preserve explicit taxonomy, ownership, denominator, provenance, and comparability markers.
6. Re-run the detector projection migration gate only after the selected disposition is approved and implemented in a bounded non-authoritative slice.

## Computability Requirements If Future Authority Is Supplied

If a future authority preserves the legacy exact-valid-share metric, computability would require:

1. explicit current-run anchor-generalization eligible population;
2. explicit approved anchor category for every included row;
3. exact-valid scorer result for every included row;
4. no-anchor exact-valid numerator;
5. total exact-valid anchor-bucket denominator;
6. explicit split and row-set scope;
7. taxonomy and assignment-ownership markers;
8. exclusion policy marker;
9. denominator provenance;
10. noncomputable status when numerator, denominator, taxonomy, ownership, scorer, or provenance evidence is missing.

If a future authority uses the redesigned B2 governed rate, computability would require the already documented B2 no-anchor governed sub-slice evidence, but the detector metric ID should not be treated as semantically equivalent without an explicit non-equivalence migration decision.

## Noncomputable Conditions

`no_anchor_exact_valid_share` must remain noncomputable or blocked when any of the following applies:

1. only the Stage C B2 no-anchor governed rate is present;
2. only historical `failure_profile.anchor_exact_share.no_anchor_phrase` is present;
3. current no-anchor exact-valid count is missing;
4. total exact-valid anchor-bucket denominator is missing;
5. no-anchor denominator is present but exact-valid-share denominator is absent;
6. anchor taxonomy marker is missing;
7. anchor assignment ownership marker is missing;
8. historical prompt-derived bucket assignment is the only category evidence;
9. split scope or row-set scope is missing;
10. scorer exact-valid semantics are missing;
11. comparison would require denominator substitution;
12. detector would have to infer anchor category from prompt text, generated text, path conventions, report names, or absence of markers.

Recommended reason codes for later non-authoritative adapter or reporting work:

1. `blocked_no_anchor_share_semantic_mismatch`
2. `source_no_anchor_exact_share_denominator_missing`
3. `source_no_anchor_taxonomy_bridge_missing`
4. `source_no_anchor_assignment_ownership_bridge_missing`
5. `source_no_anchor_share_reference_only`
6. `source_no_anchor_denominator_substitution_prohibited`

## Findings

| Target | Status | Evidence |
|---|---|---|
| Legacy detector metric definition identified | pass | Metric path is `failure_profile.anchor_exact_share.no_anchor_phrase`; threshold rule is `no_anchor_exact_valid_share_lt_0_75`. |
| Historical denominator identified | pass | Historical procedural-generalization artifacts compute shares over exact-valid anchor-bucket distribution. |
| Stage C related B2 concept identified | pass | Closest concept is `Family B2` / `No-anchor governed sub-slice`. |
| Stage C denominator identified | pass | Denominator is eligible rows in declared no-anchor category. |
| Numerator equivalence established | partial | Both concepts can involve exact-valid no-anchor rows, but taxonomy/ownership bridge is missing. |
| Denominator equivalence established | fail | Legacy share denominator and B2 governed-rate denominator answer different questions. |
| Semantic-equivalence bridge established | fail | Current authority prohibits substitution and requires bridge approval. |
| Detector migration authorized | fail | Migration-disabled posture is preserved. |

## Validation Results

Validation evidence captured for this review:

1. `rg` search for `no_anchor_exact_valid_share`, `anchor_exact_share`, `no_anchor_phrase`, and B2 no-anchor terms across docs, manifests, reports, scripts, tests, and evals: pass.
2. Review of `STAGE_B_EVAL_REDESIGN_METRIC_INVENTORY.md`: pass, legacy producer and redesign-required status identified.
3. Review of `STAGE_B_EVAL_REDESIGN_CONTRACTS.md`: pass, no-anchor concept retained but redesigned into Family B2 governed sub-slice; historical share interpretation requires separate contract.
4. Review of `STAGE_B_B2_NO_ANCHOR_MEMBERSHIP_REVIEW.md`: pass, B2 denominator rule and historical-share non-substitution rule identified.
5. Review of `B2-NI-002` fixture: pass, denominator-incompatible historical no-anchor share is bridge-required and current-run noncomputable.
6. Review of Stage C1 row-fact contract fields: pass, B2 membership, ownership, provenance, and denominator fields identified.
7. Review of C7/C8 migration artifacts and tests: pass, `no_anchor_exact_valid_share` remains `noncomputable_blocked` with reason `blocked_no_anchor_share_semantic_mismatch`.
8. Review for migration-enabled behavior in this slice: pass, no detector or threshold migration enabled.

## Governance Concerns

No new governance doctrine is introduced.

Active governance concerns retained:

1. Denominator substitution remains prohibited.
2. Detector prompt-text anchor classification remains prohibited.
3. Historical report-layer values remain insufficient for current-run computation.
4. Stage C B2 governed rate must not be collapsed into the legacy exact-valid-share metric.
5. Detector migration remains unauthorized.
6. Threshold-profile migration remains unauthorized.

## Residual Ambiguities

Residual ambiguity after this review is not whether current surfaces are equivalent; they are not.

Remaining ambiguity is the future disposition decision:

1. preserve the legacy share metric as a separately emitted Stage C surface;
2. replace it with a renamed B2 no-anchor governed-rate detector metric through an explicit non-equivalence migration;
3. keep the legacy metric reference-only/noncomputable and use B2 governed-rate evidence only for review.

That disposition requires later migration authority and is outside C9-B.

## Determination

Stage C9-B does not establish a semantic-equivalence bridge.

The no-anchor semantic-equivalence bridge blocker remains unresolved for authoritative detector migration.

Stage C9-B is closure-ready as a contract-definition and evidence-mapping review because it identifies the legacy definition, Stage C related concepts, exact missing authority, noncomputable conditions, and smallest safe blocker-closure path without expanding scope.

## Boundary Confirmation

This review did not modify evaluator runtime code, detector code, threshold profiles, fixture catalogs, fixture definitions, governance doctrine, or repository process infrastructure.

This review does not authorize detector migration, threshold-profile migration, live inference, or replacement of existing detector outputs.
