# Stage B.3 Evaluation Redesign Implementation Readiness

## Scope

This document defines implementation-readiness planning for Stage B Evaluation Redesign.

This is documentation-only planning. It does not design schemas, name fields, implement code, modify outputs, modify detector logic, change threshold profiles, change mappings, modify manifests, or relax governance.

Reference inputs:

- `STAGE_B_EVAL_REDESIGN_METRIC_INVENTORY.md`
- `STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
- `STAGE_B_EVAL_REDESIGN_EMISSION_DESIGN.md`

Approved families:

- Family A: Governed Failure-Subtype Taxonomy
- Family B1: Read-File Preservation Family
- Family B2: Anchor-Generalization Family

## 1. Component Work Breakdown

### Dataset Metadata

Responsibilities:

- Provide stable row identity.
- Provide split membership.
- Declare expected tool behavior and tool-expected eligibility.
- Declare read-file family eligibility.
- Declare read-file subpopulation membership, including symbol-name membership when applicable.
- Declare anchor-generalization eligibility and approved anchor category when anchor ownership is dataset-side.
- Provide pre-scoring exclusion annotations when rows are contaminated, ambiguous, or unsupported.
- Preserve population and row-set comparability evidence for baseline review.

Required future changes:

- Add explicit metadata coverage for the approved governance families.
- Make anchor-category and read-file subpopulation ownership explicit.
- Ensure row identity and split membership are stable enough for baseline comparison.
- Ensure exclusions are declared before aggregation.

Dependencies:

- Approved family contracts.
- Approved taxonomy and population definitions.
- Agreement on anchor-category ownership.
- Agreement on read-file subpopulation definition.

Review requirements:

- Metadata review must confirm every required row-level fact can be supplied without detector inference.
- Coverage review must confirm all eligible rows have complete required facts.
- Drift review must confirm population and split changes are explicitly visible.
- Governance review must confirm no metadata shortcut weakens existing noncomputability behavior.

### Scorer

Responsibilities:

- Emit exact-valid determination.
- Emit primary behavioral outcome.
- Emit non-exact tool-expected failure subtype for Family A.
- Preserve scorer semantics comparability evidence.
- Avoid using detector policy logic as scorer logic.

Required future changes:

- Add approved failure-subtype classification for non-exact tool-expected rows.
- Preserve direct-answer substitution as a governed subtype.
- Ensure exact-valid semantics remain stable or explicitly versioned.
- Emit scorer-level facts needed by evaluator aggregation.

Dependencies:

- Dataset metadata must declare tool-expected eligibility and expected behavior.
- Failure-subtype taxonomy must be approved before scorer implementation planning.
- Existing exact-valid semantics must be reviewed for compatibility with future family aggregation.

Review requirements:

- Taxonomy review must confirm subtype boundaries are deterministic and auditable.
- Fixture review must confirm direct-answer substitution is classified distinctly from scalar substitution, malformed JSON, wrapper/envelope drift, missing tool call, and other failures.
- Regression review must confirm existing active computable metrics are not obscured.
- Governance review must confirm scorer changes do not relax exact-valid requirements.

### Evaluator

Responsibilities:

- Aggregate declared dataset facts and scorer facts into family summaries.
- Construct counts, denominators, and rates for each governed family and sub-slice.
- Emit split-scoped summaries when governance requires split-level interpretation.
- Emit comparability markers and exclusion summaries.
- Preserve missing-fact noncomputability rather than silently inferring missing data.

Required future changes:

- Add family aggregation for failure subtypes.
- Add read-file aggregate and symbol-name sub-slice aggregation.
- Add anchor-category and no-anchor aggregation.
- Add denominator and exclusion reporting for governed populations.
- Add comparability marker propagation.

Dependencies:

- Dataset metadata completeness.
- Scorer exact-valid facts.
- Scorer failure-subtype facts.
- Approved family denominator definitions.
- Approved comparability marker set.

Review requirements:

- Aggregation review must prove denominators are built only from declared facts.
- Fixture review must cover complete emission, partial emission, missing metadata, and missing scorer facts.
- Regression review must confirm aggregate outputs do not mask current governance findings.
- Governance review must confirm evaluator does not reconstruct concepts from prompt text or generated text.

### Detector

Responsibilities:

- Consume emitted aggregate facts and comparability markers.
- Treat missing required emitted facts as noncomputable under conservative governance.
- Use baseline facts only when comparability review allows comparison.
- Avoid row filtering, prompt classification, generated-text classification, subtype inference, and denominator reconstruction.

Required future changes:

- Future work may add consumption of redesigned family summaries after emission is implemented and approved.
- Future work may add explicit noncomputability diagnostics for missing family facts or markers.
- Future work may add comparability-block behavior for historical baseline migration.

Dependencies:

- Evaluator must emit required aggregate facts.
- Comparability markers must be available.
- Baseline migration review must classify comparison status.
- Threshold review must happen only after emitted facts are validated.

Review requirements:

- Detector review must confirm it remains a consumer only.
- Noncomputability review must confirm partial emission cannot pass silently.
- Baseline review must confirm comparison is blocked unless approved.
- Governance review must confirm no relaxation of current halt behavior.

## 2. Dependency Ordering

### Prerequisite Work

1. Approve final family definitions and ownership boundaries.
2. Approve row-level fact requirements.
3. Approve failure-subtype taxonomy semantics.
4. Approve read-file subpopulation semantics.
5. Approve anchor taxonomy and anchor assignment ownership.
6. Approve denominator rules for every governed family and sub-slice.
7. Approve comparability markers and baseline review criteria.

### Implementation Sequence

Recommended sequence:

1. Dataset metadata readiness.
2. Scorer readiness.
3. Evaluator aggregation readiness.
4. Detector consumption readiness.
5. Historical baseline migration review.
6. Threshold review, only after emitted facts are validated.

Rationale:

- Dataset metadata defines row eligibility and populations.
- Scorer facts depend on metadata eligibility.
- Evaluator aggregation depends on metadata and scorer facts.
- Detector consumption depends on evaluator aggregate emission.
- Historical comparison depends on validated emission and comparability markers.
- Threshold review depends on stable emitted metrics.

### Downstream Work

Downstream work should not begin until upstream gates pass:

- Schema design depends on approved readiness gates.
- Implementation depends on schema design and fixture plan.
- Detector consumption depends on evaluator output availability.
- Threshold review depends on validated emitted metrics and baseline migration status.
- Governance promotion decisions depend on successful detector behavior with complete emissions.

## 3. Validation Strategy

### Family A: Governed Failure-Subtype Taxonomy

Validation requirements:

- Confirm every eligible tool-expected row has required metadata.
- Confirm every non-exact tool-expected row receives exactly one approved failure subtype.
- Confirm direct-answer substitution remains visible as a governed subtype.
- Confirm counts, denominators, and rates reconcile.
- Confirm split-scoped summaries reconcile with aggregate summaries.

Fixture requirements:

- Exact-valid tool-expected row.
- Direct-answer substitution row.
- Scalar substitution row.
- Malformed JSON row.
- Wrapper/envelope drift row.
- Missing-tool-call row.
- Wrong-tool-name row.
- Wrong-argument row.
- Excluded row.
- Missing-subtype row.
- Missing-marker row.

Regression requirements:

- Existing exact-valid behavior remains strict.
- Existing invalid JSON and wrapper leakage semantics remain visible.
- Existing no-call correctness signals remain separate and are not reinterpreted as direct-answer substitution.

Governance verification requirements:

- Detector cannot infer subtype from generated text.
- Missing subtype or taxonomy marker creates noncomputability.
- Direct-answer substitution cannot be replaced by a proxy aggregate.

### Family B1: Read-File Preservation Family

Validation requirements:

- Confirm read-file eligibility is declared before aggregation.
- Confirm symbol-name sub-slice membership is declared before aggregation.
- Confirm read-file aggregate count, denominator, and rate reconcile.
- Confirm symbol-name count, denominator, and rate reconcile.
- Confirm symbol-name sub-slice is interpreted with parent read-file context.
- Confirm split-scoped summaries reconcile with aggregate summaries.

Fixture requirements:

- Exact-valid read-file row.
- Non-exact read-file row.
- Exact-valid read-file symbol-name row.
- Non-exact read-file symbol-name row.
- Read-file row outside symbol-name sub-slice.
- Non-read-file tool row.
- Excluded read-file row.
- Missing read-file eligibility marker.
- Missing symbol-name marker.
- Missing exact-valid scorer fact.

Regression requirements:

- Mixed-tool exact-valid aggregates are not accepted as read-file substitutes.
- Overall read-file behavior does not hide symbol-name collapse.
- Symbol-name small-denominator reporting includes counts and denominators.

Governance verification requirements:

- Detector cannot infer read-file membership.
- Detector cannot infer symbol-name membership from prompt text.
- Missing read-file or symbol-name facts create noncomputability for dependent rules.

### Family B2: Anchor-Generalization Family

Validation requirements:

- Confirm anchor taxonomy is approved before emission.
- Confirm anchor assignment ownership is explicit.
- Confirm no-anchor membership is declared before aggregation.
- Confirm no-anchor count, denominator, and rate reconcile.
- Confirm anchor-category family summaries reconcile.
- Confirm split-scoped summaries reconcile with aggregate summaries.

Fixture requirements:

- Exact-valid no-anchor row.
- Non-exact no-anchor row.
- Exact-valid row in another anchor category.
- Non-exact row in another anchor category.
- Row outside anchor-generalization population.
- Excluded row.
- Missing anchor category row.
- Missing anchor taxonomy marker.
- Conflicting anchor assignment ownership scenario.

Regression requirements:

- Prompt text is not scanned by detector for anchor assignment.
- No-anchor rate uses the approved no-anchor denominator.
- Historical "share of exact-valid rows that are no-anchor" is not silently substituted for no-anchor exact-valid rate.

Governance verification requirements:

- Missing anchor category or taxonomy marker creates noncomputability.
- Anchor-family summaries remain contextual and do not weaken current active governance findings.
- No-anchor behavior cannot be replaced by aggregate exact-valid behavior.

## 4. Noncomputability Handling

### Partial Emission Scenarios

If only some families are emitted:

- Emitted families may be evaluated only for rules that require no missing facts.
- Non-emitted families remain noncomputable.
- Overall detector status must follow conservative noncomputability policy.
- No family may be inferred from another family.

If a family aggregate is emitted but a required sub-slice is missing:

- The aggregate may be available for diagnostic review.
- The missing sub-slice remains noncomputable.
- Any rule depending on the missing sub-slice must not pass by using the aggregate.

### Missing Fact Scenarios

Missing row-level facts must prevent downstream governed aggregation for the affected population.

Examples:

- Missing failure subtype blocks Family A subtype aggregation.
- Missing read-file eligibility blocks read-file preservation aggregation.
- Missing symbol-name membership blocks symbol-name sub-slice aggregation.
- Missing anchor category blocks anchor-generalization aggregation.
- Missing exact-valid scorer fact blocks any exact-valid rate.

### Missing Marker Scenarios

Missing comparability markers must block baseline comparison.

Examples:

- Missing failure taxonomy marker blocks direct-answer substitution comparison.
- Missing read-file subpopulation marker blocks symbol-name comparison.
- Missing anchor taxonomy or ownership marker blocks no-anchor comparison.
- Missing scorer semantics marker blocks any exact-valid comparison.
- Missing population marker blocks count-based delta interpretation.

### Expected Detector Behavior

Expected behavior:

- Mark missing required facts as noncomputable.
- Mark missing comparability markers as comparison-blocking.
- Preserve halt behavior when noncomputable governed rules remain active.
- Report which facts or markers are missing.
- Avoid fallback to aggregate, proxy, inferred, or reconstructed metrics.

Unexpected behavior:

- Passing a rule by substituting a mixed-tool aggregate.
- Passing a rule by scanning comparison rows.
- Passing a rule by interpreting prompt text.
- Passing a rule by treating historical values as comparable without review.

## 5. Historical Baseline Migration Review

### Required Review Process

1. Identify the historical artifact and governed concept.
2. Identify the historical population, denominator, split scope, and scorer semantics.
3. Identify whether the historical concept was emitted, inferred, or report-layer reconstructed.
4. Compare historical taxonomy or subpopulation semantics with the future approved family contract.
5. Classify the baseline as comparison-allowed, bridge-required, or reference-only.
6. Record reviewer approval and rationale.

### Approval Criteria

Comparison may be allowed only when:

- population is stable or explicitly bridged;
- denominator is known;
- split scope is known;
- scorer semantics are comparable;
- taxonomy or subpopulation semantics are comparable;
- comparability markers exist or approved bridge evidence exists;
- small-denominator risks are explicitly visible where relevant.

### Reference-Only Conditions

Historical values remain reference-only when:

- denominator is unknown or incompatible;
- split scope is unknown or incompatible;
- subtype or subpopulation assignment was heuristic and not reproducible;
- prompt-anchor classification cannot be validated;
- scorer semantics differ without an approved bridge;
- row population changed in a way that prevents count or rate comparison;
- artifact provenance is report-layer only and cannot be tied to approved future facts.

### Comparison-Allowed Conditions

Historical comparison may be allowed when:

- required comparability criteria pass;
- baseline review explicitly approves comparison;
- any bridge assumptions are documented;
- detector receives comparison status rather than inferring it;
- current active computable governance findings remain separate from redesign migration.

## 6. Audit And Rollback Expectations

### Audit Artifacts

Future implementation phases should emit or preserve:

- family contract reference;
- ownership boundary record;
- row-level completeness report;
- scorer taxonomy validation report;
- evaluator aggregation reconciliation report;
- comparability marker coverage report;
- historical baseline migration review record;
- detector noncomputability validation report;
- governance decision record.

### Review Checkpoints

Required checkpoints:

- metadata readiness review;
- scorer taxonomy review;
- evaluator aggregation review;
- detector consumption review;
- historical baseline migration review;
- full-family validation review;
- governance review before threshold work.

### Rollback Requirements

Rollback must be possible if:

- emitted facts are incomplete;
- subtype classification is unstable;
- denominator reconciliation fails;
- detector consumes inferred or proxy facts;
- historical comparison is incorrectly allowed;
- active computable governance findings are obscured.

Rollback expectations:

- preserve prior detector behavior until new emissions are validated;
- keep old and new outputs separable during transition;
- make partial emission noncomputable rather than silently accepted;
- retain audit artifacts for failed attempts.

### Acceptance Criteria

Readiness is accepted only when:

- all component responsibilities are assigned;
- dependency order is approved;
- validation fixtures are defined;
- noncomputability behavior is explicit;
- baseline migration review process is approved;
- rollback expectations are documented;
- no threshold or governance relaxation is included.

## 7. Implementation Gates

### Gate Before Schema Design

Schema design may begin only when:

- family contracts are accepted;
- ownership boundaries are accepted;
- row-level fact requirements are accepted;
- aggregate fact requirements are accepted;
- comparability marker requirements are accepted;
- noncomputability behavior is accepted;
- baseline migration review process is accepted.

This gate does not approve schema names or structures.

### Gate Before Implementation

Implementation may begin only when:

- schema design has been reviewed separately;
- fixture plan is approved;
- component work packets are sequenced;
- rollback strategy is accepted;
- validation commands and expected outputs are planned;
- detector consumption remains inference-free;
- no threshold changes are bundled.

This gate does not approve threshold changes.

### Gate Before Threshold Review

Threshold review may begin only when:

- emitted metrics are implemented and validated;
- family counts, denominators, and rates reconcile;
- noncomputability behavior is validated;
- baseline migration review has classified comparison status;
- active computable governance findings remain visible;
- detector consumption is validated against complete and partial emission scenarios.

This gate does not imply thresholds should change; it only defines when threshold review becomes eligible.

## Recommended Implementation Sequence

Recommended sequence:

1. Finalize metadata ownership and population definitions.
2. Finalize scorer failure-subtype taxonomy.
3. Finalize evaluator aggregation requirements.
4. Finalize detector consumption and noncomputability expectations.
5. Finalize validation fixtures and reconciliation checks.
6. Review historical baseline migration.
7. Proceed to schema design only after readiness gates pass.

## Risk Assessment

Highest-risk redesign area:

- Family A scorer subtype taxonomy, because direct-answer substitution must be distinguished from scalar substitution, malformed output, wrapper/envelope drift, missing tool calls, wrong tool names, and wrong arguments without relying on detector-time prose interpretation.

Highest-risk migration area:

- Historical baseline comparability for anchor-generalization and symbol-name sub-slices, because historical reports may rely on prompt heuristics, small denominators, and report-layer reconstruction rather than future first-class emitted facts.

Validation-critical items:

- complete row-level metadata coverage;
- deterministic scorer subtype fixtures;
- count/denominator/rate reconciliation;
- no detector inference;
- missing fact and missing marker noncomputability;
- baseline comparison blocking unless explicitly approved;
- preservation of current active computable findings.

## Planning Completeness Assessment

Stage B.3 completes governance-readiness planning at the information-flow level.

Additional planning is still required before implementation:

- Stage B.4 should be a schema-design readiness phase that translates approved information requirements into a concrete schema proposal without implementation.
- Threshold redesign should remain out of scope until emitted metrics exist, validate, and pass historical migration review.
