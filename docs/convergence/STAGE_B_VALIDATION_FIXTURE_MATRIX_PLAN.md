# Stage B WP8 Validation Fixture Matrix Plan

## Scope

This document plans the validation-fixture matrix required by WP8 before Stage B Evaluation Redesign implementation begins.

This is documentation-only planning. It does not implement fixtures, modify runtime behavior, modify schemas, modify detectors, modify evaluators, modify scorers, modify thresholds, modify governance rules, modify mappings, or modify manifests.

Reference inputs:

- `STAGE_B_IMPLEMENTATION_WORKPACKETS.md`
- `STAGE_B_EVAL_REDESIGN_IMPLEMENTATION_READINESS.md`
- `STAGE_B_EVAL_REDESIGN_SCHEMA_PROPOSAL.md`
- `STAGE_B_PLANNING_COMPLETENESS_ASSESSMENT.md`

WP8 purpose:

- Provide fixture coverage proving complete, partial, missing, noncomputable, and comparison-blocked behavior across all approved families.
- Prove detector non-inference.
- Prove reconciliation for counts, denominators, rates, coverage, and split summaries.
- Prove historical comparison is blocked unless migration review explicitly allows it.

## Fixture Doctrine

- Fixtures must test emitted facts and emitted states, not detector reconstruction.
- Every governed family and governed sub-slice must have complete, partial, and missing scenarios.
- Every rate-like concept must have count, denominator, and rate reconciliation scenarios.
- Missing required facts must produce noncomputability, not zero values.
- Missing comparability markers must block comparison, even when current-run facts are computable.
- Parent aggregates must not substitute for governed sub-slices.
- Historical values must not become comparable without explicit migration status.
- Fixture expected outcomes must be defined before implementation acceptance.

## Fixture Matrix Dimensions

The fixture matrix should be organized across the following dimensions:

| Dimension | Required Coverage |
|---|---|
| Family | Family A, Family B1, Family B2 |
| Governed sub-slice | direct-answer subtype, symbol-name sub-slice, no-anchor sub-slice |
| Emission completeness | complete, partial, missing |
| Current-run computability | computable, noncomputable |
| Comparability | comparison-allowed, bridge-required, reference-only, comparison-blocked |
| Missing-state reason | missing family, missing sub-slice, missing marker, missing denominator, missing source fact |
| Detector behavior | consume emitted facts, reject missing facts, block comparison, avoid inference |
| Reconciliation | counts, denominators, rates, split summaries, coverage summaries |
| Negative substitution | proxy aggregate, inferred row label, reconstructed denominator, historical report-layer substitute |

## Family A Fixture Categories

Family A covers the Governed Failure-Subtype Taxonomy, including direct-answer substitution as a governed subtype.

### Complete Family A Fixtures

Required categories:

- Exact-valid tool-expected row.
- Direct-answer substitution row.
- Scalar substitution row.
- Malformed JSON row.
- Wrapper or envelope drift row.
- Missing-tool-call row.
- Wrong-tool-name row.
- Wrong-argument row.
- Excluded tool-expected row.
- Multiple split coverage when split-scoped governance is active.

Expected validation:

- Every eligible non-exact tool-expected row receives exactly one approved subtype.
- Direct-answer substitution remains visible as its own governed subtype.
- Eligible tool-expected denominator reconciles.
- Non-exact tool-expected denominator reconciles.
- Direct-answer count and rates reconcile against both denominator bases when both are emitted.
- Excluded rows are visible and do not enter governed denominators.

### Partial Family A Fixtures

Required categories:

- Family aggregate present but one subtype summary missing.
- Direct-answer count present without denominator basis.
- Direct-answer subtype present without taxonomy marker.
- Split-scoped subtype summary missing when split-scoped governance is active.
- Non-exact denominator present but eligible tool-expected denominator missing.

Expected validation:

- Affected governed subtype is partial or noncomputable.
- Count-only direct-answer evidence does not become a complete governed metric.
- Detector does not infer missing subtype, denominator, or taxonomy state.

### Missing Family A Fixtures

Required categories:

- Failure-subtype family missing.
- Direct-answer governed subtype missing.
- Failure taxonomy missing.
- Missing scorer primary outcome.
- Missing exact-valid fact for a tool-expected row.
- Missing subtype for a non-exact tool-expected row.

Expected validation:

- Affected Family A rule inputs are noncomputable.
- Missing subtype is not converted into "other" unless the taxonomy explicitly emits that subtype.
- Detector does not inspect generated text to classify direct-answer substitution.

### Family A Negative Non-Inference Fixtures

Required categories:

- Generated text appears prose-like, but no direct-answer subtype is emitted.
- Scalar-looking output exists, but scorer subtype is missing.
- Historical direct-answer count exists, but current taxonomy or denominator is missing.
- No-call correctness changes, but direct-answer subtype facts are absent.

Expected validation:

- Detector does not classify generated text.
- Detector does not reinterpret no-call correctness as direct-answer substitution.
- Historical direct-answer evidence remains reference-only or bridge-required unless migration review allows comparison.

## Family B1 Fixture Categories

Family B1 covers the Read-File Preservation Family, including aggregate read-file preservation and the symbol-name governed sub-slice.

### Complete Family B1 Fixtures

Required categories:

- Exact-valid read-file row.
- Non-exact read-file row.
- Exact-valid read-file symbol-name row.
- Non-exact read-file symbol-name row.
- Read-file row outside symbol-name sub-slice.
- Non-read-file tool row.
- Excluded read-file row.
- Small-denominator symbol-name set.
- Split-scoped read-file and symbol-name coverage when active.

Expected validation:

- Read-file eligible denominator reconciles.
- Read-file exact-valid numerator and rate reconcile.
- Symbol-name denominator, numerator, and rate reconcile.
- Symbol-name summary carries parent read-file context.
- Non-read-file rows do not enter read-file denominators.
- Excluded rows are visible and excluded from governed denominators.

### Partial Family B1 Fixtures

Required categories:

- Read-file aggregate present but symbol-name sub-slice missing.
- Symbol-name numerator present but denominator missing.
- Symbol-name sub-slice present without parent read-file context.
- Read-file aggregate present without expected-tool marker.
- Split-scoped symbol-name summary missing when split-scoped governance is active.

Expected validation:

- Read-file aggregate may remain diagnostic or computable when complete, but symbol-name remains noncomputable.
- Parent aggregate does not satisfy symbol-name governed sub-slice requirements.
- Detector does not infer symbol-name membership from prompt text.

### Missing Family B1 Fixtures

Required categories:

- Read-file family missing.
- Read-file eligibility marker missing.
- Expected tool identity missing.
- Symbol-name membership marker missing.
- Exact-valid scorer fact missing.
- Read-file denominator missing.

Expected validation:

- Affected read-file aggregate or symbol-name sub-slice becomes noncomputable.
- Missing symbol-name membership blocks symbol-name aggregation.
- Missing read-file eligibility blocks read-file aggregation.

### Family B1 Negative Non-Inference Fixtures

Required categories:

- Mixed-tool exact-valid aggregate exists, but read-file aggregate is absent.
- Read-file aggregate exists, but symbol-name sub-slice is absent.
- Prompt contains symbol-like text, but symbol-name marker is missing.
- Historical symbol-name rate exists, but current subpopulation marker is missing.

Expected validation:

- Detector does not substitute mixed-tool exact-valid for read-file exact-valid.
- Detector does not substitute read-file aggregate for symbol-name sub-slice.
- Detector does not infer symbol-name from prompt text.
- Historical symbol-name evidence remains blocked unless migration review allows comparison.

## Family B2 Fixture Categories

Family B2 covers the Anchor-Generalization Family, including no-anchor as a governed sub-slice.

### Complete Family B2 Fixtures

Required categories:

- Exact-valid no-anchor row.
- Non-exact no-anchor row.
- Exact-valid row in another approved anchor category.
- Non-exact row in another approved anchor category.
- Row outside anchor-generalization population.
- Excluded anchor-eligible row.
- Multi-category anchor distribution.
- Split-scoped anchor summaries when active.

Expected validation:

- Anchor category assignment exists for every eligible row.
- No-anchor denominator, numerator, and rate reconcile.
- Sibling anchor-category summaries reconcile with family totals.
- Rows outside the anchor-generalization population do not enter denominators.
- Exclusions are visible and do not enter governed denominators.

### Partial Family B2 Fixtures

Required categories:

- Anchor family aggregate present but no-anchor sub-slice missing.
- No-anchor count present without denominator.
- Anchor categories present without assignment ownership marker.
- Anchor taxonomy marker present but category distribution incomplete.
- Split-scoped no-anchor summary missing when split-scoped governance is active.

Expected validation:

- No-anchor governed sub-slice remains noncomputable when required facts are missing.
- Anchor-family aggregate does not substitute for no-anchor behavior.
- Detector does not infer no-anchor from prompt text.

### Missing Family B2 Fixtures

Required categories:

- Anchor family missing.
- Anchor taxonomy missing.
- Anchor assignment ownership missing.
- Anchor category missing for eligible row.
- No-anchor sub-slice missing.
- Exact-valid scorer fact missing for anchor-eligible row.

Expected validation:

- Affected anchor-generalization facts become noncomputable.
- Missing anchor taxonomy or ownership blocks comparison.
- Missing no-anchor sub-slice blocks no-anchor governed evaluation.

### Family B2 Negative Non-Inference Fixtures

Required categories:

- Prompt text lacks obvious anchor phrase, but no-anchor marker is missing.
- Historical "share of exact-valid rows that are no-anchor" exists, but no-anchor exact-valid rate is absent.
- Family aggregate exact-valid rate exists, but no-anchor sub-slice is absent.
- Anchor taxonomy changed without approved migration status.

Expected validation:

- Detector does not classify prompt text.
- Historical denominator-incompatible no-anchor share is not substituted.
- Family aggregate does not satisfy no-anchor governed sub-slice requirements.
- Comparison remains blocked when taxonomy changes without approval.

## Emission State Fixture Matrix

### Complete Emission Fixtures

Complete emission fixtures should exist for:

- Family A aggregate plus direct-answer governed subtype.
- Family B1 aggregate plus symbol-name governed sub-slice.
- Family B2 aggregate plus no-anchor governed sub-slice.
- All families emitted together.

Expected validation:

- Completeness state is complete.
- Current-run computability is computable.
- Counts, denominators, rates, split summaries, and coverage summaries reconcile.
- Comparability remains independent and is not automatically allowed.

### Partial Emission Fixtures

Partial emission fixtures should exist for:

- Family aggregate present but governed sub-slice missing.
- Governed sub-slice present but denominator missing.
- Required split summary missing.
- Required marker missing.
- Coverage summary incomplete.

Expected validation:

- Completeness state is partial.
- Current-run computability follows the specific missing fact.
- Detector does not promote partial to complete.
- Parent aggregate remains unable to satisfy missing sub-slice rules.

### Missing Emission Fixtures

Missing emission fixtures should exist for:

- Missing family.
- Missing governed sub-slice.
- Missing denominator.
- Missing row-level source fact.
- Missing scorer fact.
- Missing taxonomy, subpopulation, or anchor marker.

Expected validation:

- Completeness state is missing or noncomputable for the affected concept.
- Missing facts are not represented as zero values.
- Detector reports missing reason rather than constructing the fact.

## Noncomputability State Fixtures

Required noncomputability fixture classes:

- Missing family.
- Missing sub-slice.
- Missing denominator.
- Missing source row fact.
- Missing scorer fact.
- Missing current-run marker.
- Conflicting ownership marker.
- Count-only evidence without denominator.
- Current-run computable family with noncomputable governed sub-slice.

Expected validation:

- Noncomputability reason identifies affected concept and missing state.
- Current-run noncomputability and comparison blockage remain separate.
- Diagnostic availability does not become governed computability.

## Comparability State Fixtures

Required comparability fixture classes:

- Current-run computable and comparison-allowed.
- Current-run computable and bridge-required.
- Current-run computable and reference-only.
- Current-run computable and comparison-blocked.
- Current-run noncomputable and comparison-blocked.
- Family comparison allowed but governed sub-slice comparison blocked.
- Historical baseline present but missing denominator.
- Historical baseline present but taxonomy changed.
- Historical baseline present but subpopulation definition changed.
- Historical baseline report-layer only.

Expected validation:

- Detector compares only when concept-level status is comparison-allowed.
- Bridge-required blocks detector comparison until approved.
- Reference-only does not support deltas or comparative rules.
- Family-level approval does not flow automatically to governed sub-slices.

## Detector Non-Inference Fixture Matrix

Required detector non-inference cases:

| Case | Prohibited Detector Behavior | Expected Outcome |
|---|---|---|
| Family A prose output without subtype | Classify direct-answer substitution from generated text | Noncomputable or blocked for missing subtype |
| Family A no-call metric movement | Reinterpret no-call correctness as direct-answer substitution | Direct-answer remains missing/noncomputable |
| Family B1 mixed-tool aggregate only | Use mixed-tool exact-valid as read-file rate | Read-file governed concept remains missing/noncomputable |
| Family B1 read-file aggregate only | Use read-file aggregate as symbol-name rate | Symbol-name remains missing/noncomputable |
| Family B1 symbol-like prompt | Infer symbol-name membership from prompt text | Symbol-name remains missing/noncomputable |
| Family B2 prompt without anchor text | Infer no-anchor membership from prompt text | No-anchor remains missing/noncomputable |
| Family B2 anchor aggregate only | Use anchor aggregate as no-anchor rate | No-anchor remains missing/noncomputable |
| Historical report-layer value | Treat historical value as comparable without migration status | Comparison blocked |
| Missing denominator | Use another population's denominator | Current-run noncomputable for affected rate |

## Reconciliation Fixture Matrix

Required reconciliation cases:

- Family numerator plus non-numerator partitions equal eligible denominator.
- Sub-slice denominator is bounded by parent family denominator.
- Excluded rows are reported and excluded from governed denominator.
- Split-scoped summaries reconcile with aggregate summaries.
- Coverage summary counts reconcile with family denominator.
- Family A subtype counts reconcile with non-exact eligible denominator.
- Family B1 symbol-name denominator reconciles with read-file parent context.
- Family B2 anchor-category distribution reconciles with anchor family denominator.
- Rate values reconcile with count and denominator.
- Small-denominator sub-slice reports count and denominator visibly.

Expected validation:

- Reconciliation failures block acceptance.
- Reconciliation failures do not trigger detector repair.
- Count and rate mismatches become validation failures or noncomputability, depending on implementation phase.

## Fixture Packetization

### WP8-A: Scenario Catalog And Expected Outcomes

Purpose:

- Convert this plan into a scenario catalog with expected completeness, computability, comparability, and detector behavior for each fixture.

Why first:

- It remains documentation-oriented and can be reviewed before fixture files or validators exist.
- It prevents implementation from inventing expected outcomes after code is written.

### WP8-B: Common State Fixtures

Purpose:

- Author common complete, partial, missing, noncomputable, and comparability-state fixtures that are independent of family-specific row semantics.

Why second:

- These fixtures validate the core state model shared by all families.

### WP8-C: Family A Fixture Set

Purpose:

- Author scorer-taxonomy and direct-answer subtype fixtures.

Dependency:

- Requires Family A subtype scenario catalog approval.

### WP8-D: Family B1 Fixture Set

Purpose:

- Author read-file aggregate and symbol-name sub-slice fixtures.

Dependency:

- Requires symbol-name ownership and declaration rule approval.

### WP8-E: Family B2 Fixture Set

Purpose:

- Author anchor-generalization and no-anchor sub-slice fixtures.

Dependency:

- Requires anchor taxonomy and assignment ownership approval.

### WP8-F: Detector Non-Inference And Reconciliation Fixtures

Purpose:

- Author negative substitution, detector non-inference, and reconciliation fixtures across all families.

Dependency:

- Requires family fixture expectations to be stable.

### WP8-G: Migration-State Fixtures

Purpose:

- Author comparison-allowed, bridge-required, reference-only, and comparison-blocked scenarios.

Dependency:

- Requires comparability marker representation and migration-review status model.

## Acceptance Criteria For WP8 Planning

WP8 planning is complete when:

- Every approved family and governed sub-slice has fixture categories.
- Complete, partial, missing, and noncomputable states are covered.
- Comparability states are covered independently from current-run computability.
- Detector non-inference cases are explicit.
- Reconciliation cases are explicit.
- First fixture-authoring packet is identified.
- No fixture expectation weakens governance or thresholds.

## Recommended First Fixture-Authoring Packet

Recommended first fixture-authoring packet: WP8-A Scenario Catalog And Expected Outcomes.

Rationale:

- It is the lowest-risk starting point.
- It does not require runtime changes.
- It forces expected completeness, computability, comparability, and detector behavior to be reviewed before any fixture files or validators are implemented.
- It creates the acceptance contract for later family-specific fixture authoring.

Immediate scope:

- Assign stable scenario identifiers.
- List required input conditions for each scenario.
- List expected emitted state for each scenario.
- List expected detector treatment for each scenario.
- Mark each scenario as required, optional diagnostic, or future-reserved.

Out of scope for the first packet:

- Creating actual fixture files.
- Implementing validators.
- Modifying schema or runtime code.
- Enabling detector consumption of redesigned metrics.
