# Stage B.4 Evaluation Redesign Schema Readiness

## Scope

This document defines the schema-level information model needed to carry approved Stage B governance concepts.

This is documentation-only planning. It does not implement schemas, name fields, provide JSON examples, modify code, modify outputs, modify detectors, modify thresholds, or relax governance.

Reference inputs:

- `STAGE_B_EVAL_REDESIGN_METRIC_INVENTORY.md`
- `STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
- `STAGE_B_EVAL_REDESIGN_EMISSION_DESIGN.md`
- `STAGE_B_EVAL_REDESIGN_IMPLEMENTATION_READINESS.md`

Approved families:

- Family A: Governed Failure-Subtype Taxonomy
- Family B1: Read-File Preservation Family
- Family B2: Anchor-Generalization Family

## Recommended Schema Architecture

The future schema should be organized around four conceptual layers:

1. Row-fact layer: declared metadata and scorer facts required before aggregation.
2. Family-summary layer: aggregate counts, denominators, rates, and status for each governed family.
3. Comparability layer: markers and migration status needed to decide whether baseline comparison is allowed.
4. Noncomputability layer: explicit representation of missing families, missing sub-slices, missing markers, and missing denominators.

The detector should consume family summaries, comparability evidence, and noncomputability state. It should not consume raw row facts for reconstruction.

## 1. Family Information Model

### Family A: Governed Failure-Subtype Taxonomy

Required information containers:

- Row-fact container for tool-expected eligibility, scorer outcome, exact-valid status, failure subtype, split membership, row identity, and exclusions.
- Family-summary container for the failure-subtype taxonomy.
- Subtype-summary container for each approved failure subtype.
- Direct-answer subtype summary as a governed subtype summary.
- Comparability container for taxonomy, scorer semantics, row population, split scope, and exclusions.
- Noncomputability container for missing subtype facts, missing denominators, and missing comparability markers.

Aggregate concepts:

- total eligible tool-expected population;
- exact-valid eligible tool-expected population;
- non-exact eligible tool-expected population;
- subtype counts;
- subtype rates over the eligible tool-expected population;
- subtype rates over the non-exact eligible tool-expected population;
- split-scoped subtype summaries when required.

Sub-slice concepts:

- direct-answer substitution is a required governed subtype;
- additional subtypes may be carried as sibling subtype summaries;
- each subtype must include its own count, denominator basis, rate, and completeness state.

Comparability-marker placement:

- family-level comparability evidence should describe the taxonomy and scorer semantics;
- population-level comparability evidence should describe row population, split scope, eligibility, and exclusion policy;
- subtype-level comparability evidence should exist when a subtype has special migration risk;
- baseline comparison status should be attached to the family or subtype comparison context, not inferred by the detector.

### Family B1: Read-File Preservation Family

Required information containers:

- Row-fact container for expected tool identity, read-file eligibility, scorer exact-valid status, split membership, row identity, read-file subpopulation membership, and exclusions.
- Family-summary container for aggregate read-file preservation.
- Sub-slice summary container for symbol-name preservation.
- Optional sibling sub-slice summaries for future diagnostic read-file subpopulations.
- Comparability container for scorer semantics, row population, split scope, expected tool identity, read-file eligibility, subpopulation definition, and exclusions.
- Noncomputability container for missing read-file facts, missing symbol-name facts, missing denominators, and missing comparability markers.

Aggregate concepts:

- eligible read-file population;
- exact-valid read-file population;
- read-file exact-valid rate;
- split-scoped read-file summaries when required;
- exclusion summary for read-file rows.

Sub-slice concepts:

- symbol-name sub-slice is a required governed sub-slice;
- symbol-name eligible population;
- symbol-name exact-valid population;
- symbol-name exact-valid rate;
- parent read-file context for interpreting symbol-name behavior;
- split-scoped symbol-name summaries when required.

Comparability-marker placement:

- family-level comparability evidence should describe read-file eligibility and scorer semantics;
- sub-slice-level comparability evidence should describe symbol-name population definition and membership;
- parent-child linkage should preserve the relationship between the read-file family aggregate and symbol-name sub-slice;
- baseline comparison status should be present separately for aggregate read-file and symbol-name sub-slice comparisons.

### Family B2: Anchor-Generalization Family

Required information containers:

- Row-fact container for anchor-generalization eligibility, approved anchor category, tool-expected status, scorer exact-valid status, split membership, row identity, and exclusions.
- Family-summary container for anchor-category generalization.
- Category-summary container for each approved anchor category.
- No-anchor sub-slice summary as a governed category summary.
- Comparability container for anchor taxonomy, anchor assignment ownership, scorer semantics, row population, split scope, and exclusions.
- Noncomputability container for missing anchor category, missing anchor taxonomy, missing no-anchor denominator, and missing comparability markers.

Aggregate concepts:

- eligible population by anchor category;
- exact-valid population by anchor category;
- exact-valid rate by anchor category;
- distribution of eligible rows across anchor categories;
- split-scoped anchor summaries when required.

Sub-slice concepts:

- no-anchor is a required governed sub-slice;
- no-anchor eligible population;
- no-anchor exact-valid population;
- no-anchor exact-valid rate;
- sibling anchor-category summaries for context.

Comparability-marker placement:

- family-level comparability evidence should describe anchor taxonomy and assignment ownership;
- category-level comparability evidence should describe each category's population and denominator;
- no-anchor comparability evidence should be explicit because no-anchor historical values may have heuristic origins;
- baseline comparison status should be attached to the no-anchor comparison context.

## Recommended Family Nesting Structure

Recommended conceptual nesting:

- A top-level governance-metrics area contains one entry per approved family.
- Each family contains a family summary, family completeness state, comparability evidence, and optional sub-slice collection.
- Each sub-slice contains its own summary, completeness state, comparability evidence, and parent-family context.
- A separate noncomputability area records missing required concepts without requiring the detector to inspect family internals.
- A separate migration-compatibility area records baseline comparison status for each family and sub-slice.

This nesting keeps aggregate concepts, sub-slice concepts, comparability, and noncomputability separable while preserving parent-child relationships.

## 2. Completeness Model

### Family A Completeness

Complete emission:

- row eligibility facts exist for every governed row;
- scorer outcome facts exist for every governed row;
- every non-exact tool-expected row has one approved failure subtype;
- direct-answer subtype summary is present;
- counts, denominators, and rates reconcile;
- required comparability evidence is present.

Partial emission:

- family aggregate population exists, but one or more subtype summaries are missing;
- direct-answer subtype exists without one required denominator;
- split-scoped summaries are missing when split-scoped governance is active;
- comparability evidence is present for the family but missing for a governed subtype.

Missing emission:

- failure-subtype family summary is absent;
- governed direct-answer subtype summary is absent;
- row eligibility or scorer outcome facts are insufficient to construct the family summary;
- required comparability evidence is absent.

### Family B1 Completeness

Complete emission:

- read-file eligibility facts exist for every governed row;
- exact-valid scorer facts exist for every governed row;
- read-file aggregate summary is present;
- symbol-name sub-slice summary is present;
- counts, denominators, and rates reconcile for both aggregate and sub-slice;
- parent-family context is present for symbol-name interpretation;
- required comparability evidence is present.

Partial emission:

- read-file aggregate is present but symbol-name sub-slice is absent;
- symbol-name count is present but denominator is missing;
- sub-slice comparability evidence is missing;
- split-scoped summaries are missing when split-scoped governance is active.

Missing emission:

- read-file family summary is absent;
- read-file eligibility facts are absent;
- exact-valid facts are absent;
- required denominator information is absent for the family aggregate.

### Family B2 Completeness

Complete emission:

- anchor-generalization eligibility facts exist for every governed row;
- approved anchor category exists for every eligible row;
- exact-valid scorer facts exist for every governed row;
- anchor family summary is present;
- no-anchor sub-slice summary is present;
- counts, denominators, and rates reconcile;
- anchor taxonomy and assignment ownership evidence are present.

Partial emission:

- anchor family summary is present but no-anchor sub-slice is absent;
- no-anchor count is present but denominator is missing;
- anchor taxonomy evidence is present but assignment ownership evidence is missing;
- sibling category summaries are incomplete.

Missing emission:

- anchor family summary is absent;
- anchor category facts are absent;
- no-anchor sub-slice is absent;
- anchor taxonomy evidence is absent;
- exact-valid facts are absent for the governed population.

## 3. Noncomputability Representation

### Family Missing

A family-missing state should record:

- which governed family is missing;
- whether the missing state is caused by absent row facts, absent scorer facts, absent aggregate summary, or absent comparability evidence;
- affected governed concepts;
- affected detector rules or decision surfaces, if known;
- conservative status that the family cannot be evaluated.

Family missing must not be represented as zero count or zero rate.

### Sub-Slice Missing

A sub-slice-missing state should record:

- parent family;
- governed sub-slice;
- whether parent aggregate exists;
- missing reason;
- affected governed concept;
- whether parent aggregate is still diagnostic-only available;
- conservative status that the sub-slice cannot be evaluated.

Sub-slice missing must not allow the parent aggregate to substitute for the sub-slice.

### Marker Missing

A marker-missing state should record:

- affected family or sub-slice;
- missing comparability evidence type;
- whether current-run computation is possible;
- whether baseline comparison is blocked;
- conservative comparison status.

Marker missing should block comparison even if current counts and rates exist.

### Denominator Missing

A denominator-missing state should record:

- affected family or sub-slice;
- available numerator-like quantities, if any;
- missing denominator basis;
- whether rate computation is blocked;
- whether count-only diagnostic review is possible;
- conservative status that governed rate evaluation is noncomputable.

Denominator missing must not be repaired by using another population's denominator.

## Recommended Noncomputability Representation Model

Recommended model:

- Every family and sub-slice should carry a completeness state.
- Every family and sub-slice should carry a computability state for current-run evaluation.
- Every family and sub-slice should carry a separate comparability state for baseline comparison.
- Noncomputability should distinguish current-run metric missing from baseline-comparison blocked.
- Missing facts, missing markers, missing denominators, and missing sub-slices should be explicit reasons, not collapsed into a generic failure.

## 4. Detector Visibility Requirements

### Information Detector Must Receive

The detector must receive:

- family summaries for active governed families;
- governed sub-slice summaries for active governed sub-slices;
- counts, denominators, and rates needed by active decision surfaces;
- completeness state for each family and sub-slice;
- computability state for current-run evaluation;
- comparability state for baseline comparison;
- comparability evidence sufficient to decide allowed, blocked, or reference-only comparison;
- noncomputability reasons when facts, markers, denominators, or sub-slices are missing.

### Information Detector Must Never Construct

The detector must never construct:

- row eligibility;
- expected tool family membership;
- read-file subpopulation membership;
- symbol-name membership;
- anchor category;
- no-anchor membership;
- exact-valid status;
- failure subtype;
- denominators;
- rates from row-level records;
- historical comparison status from artifact names alone.

The detector may interpret emitted status and emitted facts. It must not reconstruct metrics from lower-level evidence.

## 5. Migration Compatibility Model

### Reference-Only Status

Reference-only status means:

- historical values may inform human review;
- detector comparison is not allowed;
- current-run metric may still be computable;
- no delta or threshold comparison may rely on the historical value;
- reason for reference-only status must be preserved.

Reference-only applies when population, denominator, scorer semantics, taxonomy, split scope, or artifact provenance cannot be aligned.

### Bridge-Required Status

Bridge-required status means:

- historical and future concepts appear related but are not automatically comparable;
- a documented migration review is required;
- comparison must remain blocked until the bridge is approved;
- bridge assumptions must identify population, denominator, scorer semantics, taxonomy, and split-scope differences;
- detector must receive the approved status rather than infer it.

Bridge-required applies when historical reports used related concepts but lacked future comparability markers.

### Comparison-Allowed Status

Comparison-allowed status means:

- migration review has approved comparability;
- population and denominator are stable or explicitly bridged;
- scorer semantics are comparable;
- taxonomy or subpopulation semantics are comparable;
- split scope is known;
- small-denominator risk is visible when relevant;
- detector may evaluate comparative rules using the approved baseline context.

Comparison-allowed status must be attached at the family or sub-slice level. A family-level allowance does not automatically authorize every sub-slice.

## 6. Schema Readiness Gates

### Gate Before Concrete Schema Proposal

A concrete schema proposal may begin only when:

- family information containers are accepted;
- family nesting structure is accepted;
- completeness model is accepted;
- noncomputability representation model is accepted;
- detector visibility boundaries are accepted;
- migration compatibility statuses are accepted;
- no field naming or JSON structure is bundled into readiness approval.

### Gate Before Implementation

Implementation may begin only when:

- concrete schema proposal has been separately reviewed;
- fixture strategy covers complete, partial, and missing emission states;
- migration compatibility representation is reviewed;
- detector consumption remains inference-free;
- noncomputability representation preserves current conservative behavior;
- implementation work packets are sequenced by component ownership.

### Gate Before Threshold Review

Threshold review may begin only when:

- concrete schema is implemented and validated;
- family and sub-slice summaries are emitted;
- completeness and noncomputability states are validated;
- migration compatibility statuses are validated;
- historical baseline review is complete;
- active computable governance findings remain visible;
- no proxy or inferred metric path is used.

Threshold review remains a later phase and is not authorized by this document.

## Highest-Risk Schema-Design Area

The highest-risk schema-design area is separating current-run computability from baseline comparability.

The future schema must allow a metric to be computable for the current run while baseline comparison remains blocked because a taxonomy marker, denominator, population marker, or migration status is missing. Collapsing these states would recreate the same ambiguity that Stage B convergence closed.

Secondary high-risk areas:

- representing symbol-name as a governed sub-slice without allowing read-file aggregate substitution;
- representing no-anchor as a governed sub-slice without detector prompt inference;
- representing direct-answer substitution as a governed subtype without preserving subtype taxonomy evidence.

## Planning Completeness Assessment

Stage B.4 completes schema-readiness planning at the information-structure level.

Additional planning is still required before implementation:

- A concrete schema proposal phase should translate this readiness model into a specific schema design for review.
- An implementation planning phase should follow only after the concrete schema proposal is approved.
- Threshold redesign remains out of scope until redesigned emissions exist, validate, and pass migration compatibility review.
