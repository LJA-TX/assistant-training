# Stage C9-C Baseline-Delta Comparability Gate Review

## Scope

This review addresses the Stage C9-C baseline-delta comparability gate blocker at the contract-definition and evidence-mapping level only.

Route selected from `AGENTS.md`: `migration_gate`.

This review does not implement evaluator behavior, modify detector behavior, modify threshold profiles, authorize detector migration, or authorize threshold-profile migration.

## Authoritative Inputs Reviewed

1. `AGENTS.md`
2. `docs/convergence/STAGE_C9_BLOCKER_CLOSURE_PLANNING_ASSESSMENT.md`
3. `docs/convergence/STAGE_C7_DETECTOR_PROJECTION_MIGRATION_IMPLEMENTATION_GATE.md`
4. `docs/convergence/STAGE_C7_DETECTOR_PROJECTION_MIGRATION_GATE_DETERMINATION.md`
5. `docs/convergence/STAGE_C8_NON_AUTHORITATIVE_DETECTOR_PROJECTION_ADAPTER.md`
6. `docs/convergence/STAGE_C8_DETECTOR_PROJECTION_ADAPTER_CONFORMANCE_REPORT.md`
7. `docs/convergence/STAGE_C0_EVALUATOR_IMPLEMENTATION_ENTRY_CONTRACT_LOCK.md`
8. `docs/convergence/STAGE_C0_EVALUATOR_CONTRACT_LOCK_DETERMINATION.md`
9. `docs/convergence/STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
10. `docs/convergence/STAGE_B_EVAL_REDESIGN_SCHEMA_PROPOSAL.md`
11. `docs/convergence/STAGE_B_WP8A_SCENARIO_CATALOG.md`
12. Cross-family `X-CMP` fixture corpus under `manifests/reports/stage_b_wp8_validation/fixtures/cross_family/`
13. `manifests/reports/stage_b_v1_threshold_profile.json`
14. `scripts/post_eval_collapse_detector.py`
15. Stage C6 detector-projection preparation and reporting artifacts
16. Stage C8 non-authoritative detector projection adapter and validation surfaces
17. Stage C9-A and C9-B blocker-closure artifacts

## Legacy Detector Baseline-Delta Requirements

The legacy detector path is profile-driven.

Authoritative legacy surfaces:

1. `scripts/post_eval_collapse_detector.py`
2. `manifests/reports/stage_b_v1_threshold_profile.json`

Baseline-delta rule inventory:

| Rule ID | Metric ID | Basis | Comparator | Threshold | Rule Group |
|---|---|---|---|---:|---|
| `direct_answer_substitution_delta_gt_3` | `direct_answer_substitution_count` | `delta_vs_baseline` | `gt` | 3.0 | `tradeoff_watch_thresholds` |

Legacy metric path:

- `failure_profile.failure_categories_non_exact_tool_rows.direct_answer_substitution`

Legacy delta arithmetic:

- evaluated value = current metric value minus baseline metric value.

Legacy baseline policy:

- `missing_baseline_policy=fail_fast` in the current threshold profile.
- `--baseline-summary` is an optional CLI input, but is runtime-required when delta rules exist under `fail_fast`.

Legacy detector behavior:

1. Current metrics are resolved from the current eval summary through threshold-profile metric catalog paths.
2. Baseline metrics are resolved from the baseline summary through the same metric catalog, unless a rule declares a different `baseline_metric_id`.
3. Missing current or baseline metrics become noncomputable rule records, except that missing baseline summary fails fast under current policy.
4. Noncomputable detector rules contribute to `halt_progression` through the profile status decision rules.
5. The detector consumes emitted scalar values only; it does not reconstruct row populations, denominators, scorer evidence, or migration status.

Legacy detector gap:

- The legacy detector can resolve current and baseline scalar values, but does not itself know whether those scalar values are comparable under Stage C doctrine.

## Stage C Comparability Concepts And Evidence Surfaces

### State-Axis Model

Stage C0 locks three independent state axes for every governed concept:

1. `completeness`
2. `current_run_computability`
3. `comparability`

Allowed comparability states:

1. `comparison-allowed`
2. `bridge-required`
3. `reference-only`
4. `comparison-blocked`

Axis constraints relevant to baseline deltas:

1. `current-run computable` does not imply `comparison-allowed`.
2. `comparison-allowed` can be false while current-run computation is true.
3. Family-level comparability must not auto-propagate to governed sub-slices.
4. Comparability must not be derived from completeness or computability.
5. Comparability-state collapse into binary comparable/non-comparable is prohibited.

### Required Stage C Inputs For Comparability

Stage C0 requires `comparability_input` to include:

1. concept-level migration/comparison markers;
2. denominator compatibility markers;
3. provenance markers for baseline use.

Stage C0 requires emitted structures for:

1. `comparability_output` with concept-scoped comparability states and reasons;
2. baseline/migration reference identities;
3. denominator evidence and denominator provenance;
4. scorer/evaluator semantics markers;
5. taxonomy marker versions;
6. row-set, split, and population identity.

### Stage B Comparability Doctrine

Stage B schema doctrine defines:

1. `comparison-allowed`: current-run facts are computable and historical baseline facts passed migration review for the same family or sub-slice.
2. `bridge-required`: historical and current concepts appear related but require explicit bridge approval before detector comparison.
3. `reference-only`: historical value may inform human review but deltas, pass/fail thresholds, and comparative watch rules must not rely on it.
4. `comparison-blocked`: detector comparison must not run for the affected concept.

Historical baselines are conservative by default:

1. historical values are not automatically comparable to future emissions;
2. baseline comparison requires explicit concept-level migration status;
3. family-level migration approval does not automatically approve sub-slice migration;
4. historical artifacts missing denominator, taxonomy, row-set, scorer, split, or provenance markers remain `reference-only` or `bridge-required`;
5. detector comparison remains blocked unless comparison status is explicitly `comparison-allowed`.

### Direct-Answer Delta-Specific Requirements

The delta rule currently applies to `direct_answer_substitution_count`.

Stage B direct-answer contract requires comparisons to preserve:

1. same or explicitly versioned evaluation row population;
2. same tool-expected eligibility rules;
3. same scorer primary-class semantics;
4. same failure-subtype taxonomy;
5. stable treatment of malformed JSON, scalar output, prose output, wrapper drift, and missing-tool-call cases;
6. stable denominator reporting.

The detector must receive baseline value only when delta rules are evaluated, and it must not infer the failure subtype from generated text.

### Stage C Emitted Evidence Surfaces

Current Stage C surfaces relevant to the gate include:

1. C6 detector projection preparation artifact:
   - completeness axis source;
   - current-run computability axis source;
   - comparability axis source;
   - denominator provenance source;
   - scoring evidence source;
   - non-inference guardrail source.
2. C4 row-fact metadata artifact:
   - row/source provenance;
   - denominator provenance.
3. C5 scoring artifacts:
   - per-output scoring dimensions and reasons;
   - Family A direct-answer evidence when emitted through current aggregation path.
4. C8 non-authoritative projection adapter:
   - emits compatibility-only projected current summary;
   - emits compatibility-only projected baseline summary;
   - keeps `authoritative_detector_output=false`, `detector_migration_enabled=false`, and `threshold_profile_migration_enabled=false`.

C8 compatibility-only baseline warning:

- C8 creates a non-authoritative same-run baseline summary for detector-consumer compatibility only.
- That artifact must not be treated as an approved comparable baseline for authoritative delta evaluation.

## Baseline-Delta Comparability Gate Contract

An authoritative baseline-delta comparability gate can be established from current authority at the contract level.

Gate scope:

- applies to every detector rule with `basis=delta_vs_baseline`.
- currently applies to `direct_answer_substitution_delta_gt_3`.
- applies per governed concept, not globally.

### Gate Pass Conditions

A delta-vs-baseline detector rule may be evaluated only when all conditions pass:

1. Current metric value is explicitly emitted or projected from explicit Stage C evidence.
2. Baseline metric value is explicitly available from an approved baseline reference.
3. Current metric concept is current-run computable.
4. Current metric concept has concept-scoped `comparability=comparison-allowed` for the exact detector metric or governed concept being compared.
5. Migration/comparison approval applies to the same concept level as the delta rule.
6. Current and baseline denominator scopes are identical or explicitly bridged.
7. Current and baseline row-set, split scope, scorer semantics, failure taxonomy, eligibility rules, exclusion policy, and population identity are stable or explicitly bridged.
8. Current and baseline provenance are explicit and audit-ready.
9. Current-run reconciliation for the affected concept passes.
10. Baseline reconciliation for the affected concept passes or is explicitly approved by migration review.
11. The baseline is not a compatibility-only synthetic baseline unless an explicit later authority approves it for comparison.
12. Detector migration and threshold migration remain separately gated even if this comparability contract is satisfied.

### Gate Fail Conditions

The gate must block delta evaluation when any of the following applies:

1. current metric is missing, nonnumeric, ambiguous, or noncomputable;
2. baseline summary is missing;
3. baseline metric is missing, nonnumeric, ambiguous, or noncomputable;
4. comparability is `bridge-required`;
5. comparability is `reference-only`;
6. comparability is `comparison-blocked`;
7. comparability status is missing;
8. migration status is inferred from artifact name, path, metric resemblance, or same metric ID;
9. family-level `comparison-allowed` exists but governed sub-slice status is missing or blocked;
10. current denominator or baseline denominator is missing;
11. current and baseline denominator scopes differ without explicit bridge approval;
12. row-set, split, scorer, subtype taxonomy, ownership, exclusion, or provenance markers are missing or incompatible;
13. current metric value is projected through a blocked metric mapping;
14. baseline value is report-layer only or reference-only;
15. baseline is a C8 compatibility-only same-run baseline.

### Gate Outputs

A future implementation of this gate should emit, for each delta rule:

1. rule ID;
2. metric ID;
3. baseline metric ID;
4. current metric value and source artifact/path;
5. baseline metric value and source artifact/path;
6. evaluated delta when gate passes;
7. concept comparability state;
8. current-run computability state;
9. denominator compatibility status;
10. migration/comparison marker identity;
11. provenance references for current and baseline;
12. reconciliation status for current and baseline;
13. gate result: `pass` or `blocked`;
14. blocker reason codes when blocked.

This output is a contract requirement only. It is not implemented in this slice.

## Ownership Contract

### Threshold Profile Owner

The threshold profile owns:

1. rule ID;
2. metric ID;
3. basis;
4. comparator;
5. threshold;
6. missing-baseline policy.

The threshold profile does not own comparability approval.

### Scorer Owner

The scorer owns:

1. exact-valid or failure-subtype evidence;
2. scorer primary-class semantics;
3. scorer semantics marker.

The scorer does not own baseline migration approval.

### Evaluator And Aggregation Owners

The evaluator owns:

1. family and governed concept aggregation;
2. current numerator/count, denominator, and rate emission;
3. reconciliation outputs;
4. row-set and split-scoped aggregation surfaces;
5. detector projection packaging when projection is enabled.

### Comparability Engine Owner

The comparability engine owns:

1. concept-scoped comparability state;
2. comparison block reasons;
3. denominator compatibility marker consumption;
4. baseline reference identity consumption;
5. gate evidence packaging for detector projection.

### Migration/Governance Review Owner

Migration/governance review owns:

1. bridge approval;
2. migration status approval;
3. reference-only classification;
4. rejection of comparison when historical and current concepts are incompatible.

### Detector Owner

The detector remains a consumer only.

The detector must not:

1. infer comparability;
2. infer migration status;
3. infer denominator compatibility;
4. reconstruct missing baseline facts;
5. promote compatibility-only baselines into authoritative baselines.

## Required Evidence

For a delta rule to pass the gate, evidence must include:

1. current governed concept identity;
2. baseline governed concept identity;
3. current metric value;
4. baseline metric value;
5. current denominator and denominator provenance;
6. baseline denominator and denominator provenance where denominator is relevant to the concept;
7. current row-set identity;
8. baseline row-set identity;
9. split scope identity;
10. scorer semantics marker;
11. failure taxonomy marker when subtype concepts are involved;
12. eligibility rule marker;
13. exclusion policy marker;
14. current reconciliation result;
15. baseline reconciliation result or bridge approval;
16. concept-scoped comparability state;
17. migration marker or bridge approval identity;
18. provenance references for source artifacts;
19. non-inference guardrail status.

## Comparability Requirements

Delta comparison is allowed only when:

1. comparability is exactly `comparison-allowed` for the affected concept;
2. current-run computability is exactly `current-run computable` for the affected concept;
3. marker, denominator, provenance, and reconciliation requirements pass;
4. the comparison is concept-scoped and does not inherit from parent/family status.

Delta comparison is blocked when comparability is any of:

1. `bridge-required`;
2. `reference-only`;
3. `comparison-blocked`;
4. missing or unrecognized.

## Computability Requirements

The baseline-delta gate is computable only when:

1. current metric is computable;
2. baseline metric is computable;
3. current and baseline values are finite numeric values;
4. required current and baseline evidence surfaces are present;
5. comparability is `comparison-allowed`;
6. denominator/provenance/migration evidence passes.

If these conditions hold, evaluated delta is:

- current value minus baseline value.

If these conditions do not hold, the delta rule must remain blocked or noncomputable with reason codes.

## Noncomputable And Blocked Conditions

Recommended reason codes for future implementation:

1. `baseline_summary_missing`
2. `baseline_metric_missing`
3. `current_metric_missing`
4. `current_metric_noncomputable`
5. `baseline_metric_noncomputable`
6. `comparability_status_missing`
7. `comparability_bridge_required`
8. `comparability_reference_only`
9. `comparability_comparison_blocked`
10. `migration_status_missing`
11. `denominator_compatibility_missing`
12. `denominator_scope_mismatch`
13. `baseline_provenance_missing`
14. `current_provenance_missing`
15. `family_status_does_not_authorize_subslice`
16. `compatibility_only_baseline_not_authoritative`
17. `blocked_metric_mapping`
18. `scorer_semantics_mismatch`
19. `failure_taxonomy_mismatch`
20. `row_set_or_split_scope_mismatch`

## Blocked-Case Validation Matrix

| Case | Expected Gate Result | Source Doctrine |
|---|---|---|
| Current computable and concept-level migration approved | allow delta evaluation | `X-CMP-001` |
| Related historical concept but bridge not approved | block as bridge-required | `X-CMP-002` |
| Historical value reference-only | block delta; preserve reference visibility | `X-CMP-003` |
| Required migration status missing | block comparison | `X-CMP-004` |
| Current-run concept noncomputable while baseline exists | block current and comparative evaluation | `X-CMP-005` |
| Family comparison allowed but governed sub-slice blocked | allow family only; block sub-slice delta | `X-CMP-006` |
| Historical denominator missing | block delta as reference-only | `X-CMP-007` |
| Historical taxonomy changed without bridge | block as bridge-required | `X-CMP-008` |
| Historical subpopulation changed without bridge | block as bridge-required | `X-CMP-009` |
| Historical value is report-layer only | block delta as reference-only | `X-CMP-010` |
| Historical report-layer value lacks migration status | block; do not infer from path/name | `X-NI-001` |
| Required denominator missing while alternate denominator exists | block; do not substitute denominator | `X-NI-002` |

## Findings

| Target | Status | Evidence |
|---|---|---|
| Legacy delta rule requirements identified | pass | Threshold profile has one `delta_vs_baseline` rule and `missing_baseline_policy=fail_fast`. |
| Stage C comparability state model identified | pass | C0 locks independent `comparability` axis and allowed states. |
| Required provenance/denominator evidence identified | pass | C0 requires baseline/migration refs and denominator provenance for governed rates. |
| Cross-family comparability distinctions preserved | pass | `X-CMP-001` through `X-CMP-010` cover allowed, bridge-required, reference-only, and blocked cases. |
| Authoritative gate contract can be established | pass | Existing C0, Stage B schema doctrine, and X-CMP fixtures define sufficient gate semantics. |
| Detector migration authorized | fail | This slice defines contract only and preserves migration-disabled posture. |
| Threshold-profile migration authorized | fail | This slice does not modify or activate threshold-profile migration. |

## Validation Results

Validation evidence captured for this review:

1. `rg` and direct review of `stage_b_v1_threshold_profile.json`: pass, one delta-vs-baseline rule identified.
2. Direct review of `scripts/post_eval_collapse_detector.py`: pass, baseline summary is fail-fast required for delta rules under current profile; delta arithmetic is current minus baseline.
3. Direct review of Stage C0 contract lock: pass, independent comparability axis, baseline/migration references, denominator provenance, and comparability engine boundary identified.
4. Direct review of Stage B schema proposal: pass, `comparison-allowed`, `bridge-required`, `reference-only`, and `comparison-blocked` definitions identified.
5. Direct review of cross-family `X-CMP` fixture corpus: pass, blocked-case matrix reconciles to authored fixtures.
6. Direct review of Stage C6 projection-preparation artifact: pass, comparability axis, denominator provenance, scoring evidence, and non-inference guardrail sources are present.
7. Direct review of C8 adapter documentation/code/tests: pass, same-run projected baseline is compatibility-only and migration flags remain disabled.
8. Review for migration-enabled behavior in this slice: pass, no detector or threshold migration enabled.

## Governance Concerns

No new governance doctrine is introduced.

Active governance concerns retained:

1. Detector migration remains unauthorized.
2. Threshold-profile migration remains unauthorized.
3. A compatibility-only same-run baseline must not be treated as authoritative baseline evidence.
4. Concept-level comparability must not be inherited from family-level comparability.
5. Bridge-required and reference-only historical values must not feed delta rules.
6. Denominator/provenance substitution remains prohibited.

## Residual Ambiguities

The baseline-delta comparability gate is resolved at contract level.

Remaining ambiguity is implementation-facing:

1. the C8 adapter does not yet enforce this gate for authoritative detector projection;
2. emitted Stage C real-output examples remain limited and do not prove full multi-family baseline comparison execution;
3. other detector-migration blockers still affect overall migration readiness.

## Determination

Stage C9-C establishes the baseline-delta comparability gate contract from current authoritative evidence.

The baseline-delta comparability gate blocker is resolved at contract-definition and evidence-mapping level.

Authoritative detector migration remains blocked until a later migration gate confirms all mapping, comparability, implementation, validation, and consumer-compatibility conditions are satisfied.

## Boundary Confirmation

This review did not modify evaluator runtime code, detector code, threshold profiles, fixture catalogs, fixture definitions, governance doctrine, or repository process infrastructure.

This review does not authorize detector migration, threshold-profile migration, live inference, or replacement of existing detector outputs.
