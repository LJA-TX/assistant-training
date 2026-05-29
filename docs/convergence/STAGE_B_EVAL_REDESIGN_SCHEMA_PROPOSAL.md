# Stage B.5 Evaluation Redesign Schema Proposal

## Scope

This document proposes a concrete schema-level structure for carrying the approved Stage B governance concepts.

This is documentation-only planning. It does not implement schemas, modify code, modify evaluator outputs, modify scorer outputs, modify detector logic, modify thresholds, modify governance rules, modify mappings, or modify manifests.

Reference inputs:

- `STAGE_B_EVAL_REDESIGN_METRIC_INVENTORY.md`
- `STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
- `STAGE_B_EVAL_REDESIGN_EMISSION_DESIGN.md`
- `STAGE_B_EVAL_REDESIGN_IMPLEMENTATION_READINESS.md`
- `STAGE_B_EVAL_REDESIGN_SCHEMA_READINESS.md`

Approved families:

- Family A: Governed Failure-Subtype Taxonomy
- Family B1: Read-File Preservation Family
- Family B2: Anchor-Generalization Family

The proposed structure is a schema architecture for review. It does not authorize rollout.

## Design Principles

- Governance facts must be emitted by the responsible component before detector consumption.
- The detector must consume emitted facts and states; it must not reconstruct row populations, sub-slices, denominators, failure subtypes, or baseline comparability.
- Missing required facts are represented as noncomputable states, not as zero values.
- Current-run computability and historical-baseline comparability are independent schema states.
- Governed sub-slices must remain visible as governed concepts and must not be replaced by parent aggregate metrics.
- Historical artifacts may be reference evidence, but comparison is allowed only when migration status explicitly permits it.
- The schema should use one governed-family envelope so future families can be added without redesigning top-level architecture.

## 1. Proposed Top-Level Schema Structure

### Recommended Top-Level Containers

The proposed schema should contain the following major containers:

1. `evaluation_context`
2. `family_registry`
3. `row_fact_coverage`
4. `governance_families`
5. `noncomputability`
6. `comparability`
7. `detector_consumption_view`
8. `audit`

These names are proposed container concepts. Concrete schema review may revise exact names without changing the required architecture.

### `evaluation_context`

Purpose:

- Identify the evaluation run and population under review.
- Carry run-level split scope, row-set identity, scorer/evaluator provenance, and schema/proposal version context.
- Provide the global context needed to interpret family summaries.

Rationale:

Family metrics cannot be interpreted without knowing which run, population, split scope, and emitted schema context produced them. This container prevents those facts from being repeated inconsistently inside every family while still allowing family-specific overrides when necessary.

### `family_registry`

Purpose:

- Declare which governed families and governed sub-slices are active for the run.
- Declare whether each governed family or sub-slice is required, optional, future-reserved, diagnostic-only, or inactive.
- Preserve family identifiers, sub-slice identifiers, and taxonomy identifiers used by downstream containers.

Rationale:

The detector should not infer that a family is required merely because it appears or does not appear in an artifact. A registry gives the detector an explicit contract surface: active governed concepts must either have emitted facts or explicit noncomputability state.

### `row_fact_coverage`

Purpose:

- Summarize whether required row-level facts existed before aggregation.
- Preserve coverage evidence for dataset metadata facts, scorer facts, and evaluator aggregation prerequisites.
- Carry coverage counts and coverage status by family and governed sub-slice.

Rationale:

The schema should not require the detector to inspect raw row records. However, it must expose enough coverage evidence to distinguish complete aggregation from partial or missing emission. This container is a coverage summary, not a detector-owned reconstruction path.

### `governance_families`

Purpose:

- Hold one governed-family envelope per approved family.
- Carry family aggregate summaries, governed sub-slice summaries, completeness state, computability state, family-specific comparability references, and family-specific noncomputability references.

Rationale:

This is the primary home for current-run governed facts. Keeping all families under one generic container avoids hardcoding Family A, Family B1, and Family B2 as permanent top-level schema concepts.

### `noncomputability`

Purpose:

- Record explicit missing-family, missing-sub-slice, missing-marker, and missing-denominator states.
- Identify affected governed concepts and conservative detector treatment.
- Distinguish current-run noncomputability from historical comparison blockage.

Rationale:

Noncomputability is a governance signal, not an implementation exception. It must be emitted as structured state so missing facts cannot be silently converted to zeros, omitted metrics, or inferred substitutes.

### `comparability`

Purpose:

- Carry baseline-migration and comparison-status state for each family and governed sub-slice.
- Represent `comparison-allowed`, `bridge-required`, `reference-only`, and `comparison-blocked` statuses.
- Preserve marker evidence needed for comparison review, including taxonomy, population, split, scorer, row-set, archetype, anchor-category, and exclusion-policy markers.

Rationale:

Baseline comparability must be separable from current-run computation. A current run may be complete and computable while historical comparison remains blocked. A dedicated comparability container keeps this decision explicit and reviewable.

### `detector_consumption_view`

Purpose:

- Provide the detector-facing projection of emitted facts and states.
- Include only the aggregate facts, governed sub-slice facts, computability states, comparability statuses, noncomputability reasons, and scope markers needed by active decision surfaces.
- Exclude raw row records and ownership-internal evidence.

Rationale:

This container formalizes the detector's role as a policy consumer. It protects against detector-side reconstruction by giving the detector a complete emitted view while keeping ownership of classification, aggregation, and baseline migration outside detector logic.

### `audit`

Purpose:

- Preserve validation, review, provenance, and reconciliation evidence.
- Record whether family summaries reconciled with coverage summaries.
- Record whether migration review approved any historical comparison.
- Preserve review checkpoints without changing governance outcomes.

Rationale:

Stage B redesign requires traceability. Audit evidence must be available for review and rollback decisions without becoming a proxy metric path or a detector-owned source of derived facts.

### Family Placement

Recommended placement:

- Family A, Family B1, and Family B2 should be sibling entries under `governance_families`.
- Each family entry should use the same governed-family envelope.
- Family-specific subtypes, sub-slices, and categories should live inside that family's envelope.
- Future families should be added as sibling family entries, not as new top-level schema containers.

Rationale:

Sibling family placement keeps family semantics independent while preserving a common governance interface. It also prevents the schema from becoming a set of one-off metric fields that would need redesign for every new governed concept.

### Comparability Placement

Recommended placement:

- Run-wide comparability markers should live under `evaluation_context` or `comparability`, depending on whether they apply globally.
- Family-level comparison status should live in `comparability` and be referenced from the relevant family entry.
- Sub-slice comparison status should live in `comparability` and be referenced from the relevant sub-slice entry.
- A family-level `comparison-allowed` status must not automatically authorize sub-slice comparison.

Rationale:

Comparison eligibility is concept-specific. Family aggregate comparability can differ from governed sub-slice comparability, especially for symbol-name and no-anchor behavior.

### Noncomputability Placement

Recommended placement:

- Local completeness and computability summaries should be present on each family and governed sub-slice.
- Detailed missing-state records should live in the top-level `noncomputability` container.
- Family and sub-slice entries should reference their relevant noncomputability records.

Rationale:

Local state makes family summaries self-describing. Centralized missing-state records make it possible to audit all governance blockers without asking the detector to inspect every family internals.

## 2. Family Structure Proposals

### Common Governed-Family Envelope

Every family entry under `governance_families` should use the same high-level structure:

- family identity and family role;
- aggregate summary;
- governed sub-slice collection;
- completeness state;
- current-run computability state;
- comparability reference;
- noncomputability reference;
- source coverage reference;
- audit reference.

The aggregate summary should hold count, denominator, and rate concepts when the governed concern is rate-like. It should also state the denominator basis used for every emitted rate.

The governed sub-slice collection should hold required governed sub-slices and any approved diagnostic sibling sub-slices. Required governed sub-slices must carry the same core state model as the parent family: completeness, current-run computability, comparability, noncomputability, and audit references.

### Family A: Governed Failure-Subtype Taxonomy

Aggregate containers:

- A failure-subtype family summary for eligible tool-expected rows.
- A non-exact tool-expected summary for rows requiring subtype classification.
- A subtype distribution summary across approved failure subtypes.
- Denominator-basis summaries for eligible tool-expected rows and non-exact eligible tool-expected rows.

Sub-slice containers:

- A governed subtype summary for direct-answer substitution.
- Sibling subtype summaries for other approved failure subtypes.
- Optional diagnostic subtype summaries only when explicitly declared in the family registry.

Completeness representation:

- Complete when eligible tool-expected population, scorer outcomes, non-exact population, approved subtype assignment, direct-answer subtype summary, denominators, rates, and required markers are present and reconcile.
- Partial when the aggregate population exists but one or more subtype summaries, denominator bases, split summaries, or markers are missing.
- Missing when the family aggregate is absent, direct-answer governed subtype is absent, subtype taxonomy is absent, or row/scorer facts are insufficient to emit the family summary.

Computability representation:

- The family is current-run computable only when aggregate counts, denominators, rates, subtype summaries, and direct-answer subtype facts are complete enough for the governed decision surface.
- The direct-answer governed subtype is current-run computable only when its count, denominator basis, rate, taxonomy context, and eligible population are emitted.
- Count-only direct-answer emission may support human review, but it is not a complete governed rate contract.

Comparability representation:

- Family comparison status must account for row population, tool-expected eligibility, scorer semantics, failure taxonomy, split scope, and exclusion policy.
- Direct-answer subtype comparison status must be explicit and may differ from the family aggregate.
- Historical direct-answer counts without denominator and taxonomy alignment should be `reference-only` or `bridge-required`, not automatically comparable.

### Family B1: Read-File Preservation Family

Aggregate containers:

- A read-file preservation family summary for eligible read-file tool-expected rows.
- A read-file exact-valid summary with count, denominator, and rate.
- A split-scoped read-file summary when split-specific governance is active.
- An exclusion summary for read-file rows when exclusions exist.

Sub-slice containers:

- A required symbol-name governed sub-slice summary.
- Optional sibling read-file sub-slice summaries for future governed or diagnostic subpopulations.
- Parent read-file context for every read-file sub-slice.

Completeness representation:

- Complete when read-file eligibility, expected tool identity, scorer exact-valid outcome, aggregate count, denominator, rate, symbol-name membership, symbol-name count, symbol-name denominator, symbol-name rate, parent context, and required markers are present and reconcile.
- Partial when the read-file aggregate is present but symbol-name sub-slice, denominator, parent context, split summary, or comparability marker is incomplete.
- Missing when read-file family aggregate is absent, read-file eligibility facts are absent, exact-valid facts are absent, or the denominator basis is absent.

Computability representation:

- The read-file aggregate is current-run computable only when the eligible read-file denominator and exact-valid numerator are emitted and reconciled.
- The symbol-name governed sub-slice is current-run computable only when symbol-name membership, denominator, numerator, rate, and parent read-file context are emitted.
- The read-file aggregate cannot substitute for a missing symbol-name sub-slice.

Comparability representation:

- Read-file aggregate comparison status must account for row-set identity, expected tool identity, expected argument semantics, scorer exact-valid semantics, split scope, and exclusions.
- Symbol-name comparison status must additionally account for subpopulation or archetype definition, small-denominator visibility, and parent-family context.
- Symbol-name comparison status must be explicit even when the read-file aggregate is comparison-allowed.

### Family B2: Anchor-Generalization Family

Aggregate containers:

- An anchor-generalization family summary for the approved anchor-generalization population.
- Anchor-category distribution summaries.
- Exact-valid summaries by approved anchor category.
- Split-scoped anchor-category summaries when split-specific governance is active.

Sub-slice containers:

- A required no-anchor governed sub-slice summary.
- Sibling anchor-category summaries for category context.
- Optional future anchor-category sub-slices only when declared in the family registry.

Completeness representation:

- Complete when anchor-generalization eligibility, approved anchor taxonomy, anchor assignment ownership, anchor category for every eligible row, scorer exact-valid facts, category counts, category denominators, no-anchor count, no-anchor denominator, no-anchor rate, and required markers are present and reconcile.
- Partial when anchor family aggregate exists but no-anchor sub-slice, category distribution, denominator, assignment ownership, split summary, or marker evidence is incomplete.
- Missing when anchor family summary is absent, anchor category facts are absent, no-anchor sub-slice is absent, exact-valid facts are absent, or anchor taxonomy evidence is absent.

Computability representation:

- The family is current-run computable only when approved anchor categories and exact-valid outcomes are present across the eligible population.
- The no-anchor governed sub-slice is current-run computable only when no-anchor membership, numerator, denominator, rate, and taxonomy context are emitted.
- A mixed anchor-category aggregate cannot substitute for missing no-anchor facts.

Comparability representation:

- Family comparison status must account for anchor taxonomy, anchor assignment ownership, row population, scorer exact-valid semantics, split scope, and exclusions.
- No-anchor comparison status must be explicit because historical no-anchor values may have heuristic or report-layer origins.
- No-anchor comparison must remain blocked unless no-anchor population and denominator semantics are stable or approved by migration bridge.

## 3. Completeness And State Model

The schema should distinguish `complete`, `partial`, and `missing` as explicit states for every governed family and governed sub-slice.

### Complete

`complete` means:

- all required row-level fact coverage exists for the family or sub-slice;
- all required scorer facts exist;
- all required aggregate counts, denominators, and rates exist;
- all required governed sub-slices exist;
- required comparability markers exist for current-run interpretation;
- emitted counts and denominators reconcile with coverage summaries;
- no required noncomputability record applies to the concept.

A complete current-run emission does not by itself mean historical comparison is allowed.

### Partial

`partial` means:

- some required facts exist, but at least one required aggregate, denominator, sub-slice, marker, split summary, source coverage fact, or reconciliation check is missing;
- the available facts may support diagnostic review;
- governed evaluation must follow the explicit computability state rather than assume the available facts are sufficient.

Partial emission must not be silently promoted to complete by the detector.

### Missing

`missing` means:

- the required family or governed sub-slice is absent; or
- required row facts, scorer facts, denominator basis, taxonomy marker, anchor category, subpopulation membership, or aggregate summary are absent enough that the concept cannot be evaluated.

Missing emission must not be represented as zero count, zero denominator, zero rate, or successful pass.

### State Ownership

The evaluator should emit completeness state from source coverage and aggregation results. The detector may consume the state and apply policy. The detector must not construct completeness state by reading raw rows, prompt text, generated text, artifact names, or historical report shape.

## 4. Computability And Comparability Model

The schema should represent current-run computability and historical-baseline comparability as separate state axes.

### Current-Run Computable

`current-run computable` means:

- the current run emitted the required count, denominator, rate, governed sub-slice, completeness, and marker facts for the governed concept;
- the current-run facts reconcile;
- no current-run missing-denominator, missing-sub-slice, missing-family, or missing-required-marker state blocks computation.

This state answers whether the current run can be evaluated for the concept.

### Current-Run Noncomputable

`current-run noncomputable` means:

- at least one required fact, denominator, family summary, governed sub-slice, scorer result, taxonomy, category, source coverage fact, or current-run marker is missing;
- the affected governed concept cannot support active governance evaluation for the current run;
- conservative detector behavior remains required.

This state must include reason categories so noncomputability remains auditable.

### Comparison-Allowed

`comparison-allowed` means:

- current-run facts are computable for the governed concept;
- historical baseline facts have passed migration review for the same family or sub-slice;
- population, denominator, scorer semantics, taxonomy or subpopulation semantics, split scope, and exclusion policy are stable or explicitly bridged;
- any small-denominator risk is visible where relevant.

This status authorizes detector comparison against the approved baseline context only for the concept to which it is attached.

### Bridge-Required

`bridge-required` means:

- historical and current concepts appear related but are not automatically comparable;
- a migration review must decide whether a bridge is acceptable;
- detector comparison remains blocked until approval is emitted;
- bridge assumptions must be documented outside detector inference.

This is likely for historical direct-answer, no-anchor, and symbol-name artifacts that lack future marker coverage.

### Reference-Only

`reference-only` means:

- historical values may inform human review;
- detector comparison is not allowed;
- current-run computation may still be possible;
- deltas, pass/fail thresholds, and comparative watch rules must not rely on the historical value.

Reference-only status applies when marker, population, denominator, scorer, taxonomy, split, or provenance evidence cannot support approved comparison.

### Comparison-Blocked

`comparison-blocked` means:

- the concept cannot be compared because current-run facts are noncomputable, baseline facts are absent, required migration status is absent, bridge review rejected comparability, or a required marker is missing;
- detector comparison must not run for the affected concept;
- the affected concept should remain governed through noncomputability or current-run-only review if applicable.

### Orthogonality Requirement

The schema must support the following combinations without conflation:

- current-run computable and comparison-allowed;
- current-run computable and bridge-required;
- current-run computable and reference-only;
- current-run computable and comparison-blocked;
- current-run noncomputable and comparison-blocked.

This separation is required because current-run computability and baseline comparability answer different governance questions.

## 5. Extensibility Analysis

### Future Family C

The proposed structure can accommodate a future Family C by adding a sibling family entry under `governance_families`, registering it in `family_registry`, and attaching family-specific coverage, noncomputability, comparability, detector-view, and audit records.

No top-level redesign is required if Family C follows the governed-family envelope and declares its aggregate and sub-slice contracts explicitly.

### Future Family D

The same structure can accommodate a future Family D even if it has a different metric shape, such as a taxonomy, per-tool preservation family, generalization family, or safety-style family, provided it can express:

- an aggregate summary;
- zero or more governed sub-slices;
- completeness state;
- current-run computability state;
- comparability status;
- noncomputability reasons;
- source coverage;
- detector consumption projection.

If a future family cannot express these concepts, it should trigger a new schema-readiness review rather than ad hoc top-level fields.

### Future Governed Sub-Slices

Future governed sub-slices should be added as entries inside the relevant family's sub-slice collection. Each governed sub-slice should carry its own:

- denominator basis;
- numerator or count basis;
- rate or metric value when applicable;
- completeness state;
- current-run computability state;
- comparability status;
- noncomputability reference;
- parent-family context.

Adding a governed sub-slice must not require adding a new top-level schema container.

### Extensibility Assessment

The proposal is extensible if future concepts are added through:

- registry declaration;
- governed-family envelope reuse;
- sub-slice collection reuse;
- centralized comparability and noncomputability state;
- detector-view projection.

The proposal becomes brittle if future concepts are represented as standalone top-level metric fields, detector-derived aliases, or family-specific one-off missing-state structures.

## 6. Detector Consumption View

### Information The Detector Receives

The detector should receive a policy-facing projection that includes:

- active family and governed sub-slice identifiers from the family registry;
- current-run aggregate summaries for active governed families;
- current-run summaries for active governed sub-slices;
- counts, denominators, and rates required by active decision surfaces;
- completeness state for each active family and governed sub-slice;
- current-run computability state for each active family and governed sub-slice;
- comparability status for each family and governed sub-slice when baseline comparison is requested;
- noncomputability reason records relevant to active governed concepts;
- split, population, taxonomy, subpopulation, anchor-category, row-set, scorer, and exclusion markers needed to interpret emitted facts;
- approved baseline facts only when comparison status allows detector comparison.

### Information Intentionally Hidden From Detector Ownership

The detector should not own or construct:

- raw row eligibility;
- expected tool family membership;
- read-file eligibility;
- symbol-name membership;
- anchor category;
- no-anchor membership;
- exact-valid status;
- failure subtype;
- direct-answer substitution classification;
- row exclusions;
- denominator construction;
- rate construction from lower-level records;
- historical bridge decisions;
- migration comparability status;
- prompt-text classification;
- generated-text classification;
- artifact-name-based metric reconstruction.

The detector may reject or halt on missing emitted facts according to governance policy. It must not repair missing facts.

### Detector View Rationale

The detector-facing projection should be sufficient for policy evaluation but insufficient for reconstructing metrics. This keeps the detector accountable for governance interpretation while preserving dataset metadata, scorer, evaluator, and migration-review ownership.

## 7. Schema Risks

### Highest-Risk Schema Area

The highest-risk schema area is the separation of completeness, current-run computability, and historical comparability.

If these states are collapsed, a complete current-run metric may incorrectly permit historical comparison, or a comparison-blocked metric may be mistaken for current-run noncomputability. That would recreate the ambiguity Stage B convergence closed.

### Highest-Risk Migration Area

The highest-risk migration area is historical baseline treatment for the four redesign-required concepts.

Historical direct-answer substitution, no-anchor, read-file, and symbol-name artifacts may look similar to future governed concepts but lack future comparability markers, denominator evidence, taxonomy evidence, or subpopulation ownership. They should remain `reference-only` or `bridge-required` until migration review approves comparison for the specific family or sub-slice.

### Highest-Risk Extensibility Area

The highest-risk extensibility area is hardcoding approved Stage B families as permanent top-level schema fields.

If Family A, Family B1, and Family B2 are encoded as special top-level structures rather than entries in a generic governed-family envelope, future Family C or Family D will likely require another schema redesign and may encourage proxy mappings.

### Secondary Risks

- Treating parent family aggregates as substitutes for governed sub-slices.
- Treating missing denominators as zero or as implicit population totals.
- Allowing detector-side row filtering to compensate for incomplete evaluator emission.
- Allowing family-level comparison approval to flow automatically to sub-slices.
- Emitting diagnostic sub-slices without distinguishing them from governed sub-slices.
- Allowing audit artifacts to become alternate metric sources.

## Recommended Schema Architecture

The recommended architecture is:

- a top-level evaluation context for run and population scope;
- a family registry for active governed concepts;
- a row-fact coverage container for non-detector coverage evidence;
- a generic governed-family container with one family envelope per approved family;
- family-local aggregate and sub-slice summaries;
- centralized noncomputability records;
- centralized comparability records;
- a detector-facing projection that contains only emitted facts and emitted states;
- an audit container for validation and review evidence.

This architecture preserves the approved governance doctrine while allowing concrete schema design to proceed.

## Recommended Family Nesting Structure

Recommended nesting:

- `governance_families`
  - Family A
    - failure-subtype aggregate
    - direct-answer governed subtype
    - sibling failure subtype summaries
  - Family B1
    - read-file aggregate
    - symbol-name governed sub-slice
    - sibling read-file sub-slice summaries
  - Family B2
    - anchor-generalization aggregate
    - no-anchor governed sub-slice
    - sibling anchor-category summaries

All governed sub-slices should remain children of their parent family while retaining independent completeness, computability, and comparability state.

## Migration Assessment

Historical baselines should be treated conservatively:

- Historical values are not automatically comparable to future emissions.
- Baseline comparison requires explicit concept-level migration status.
- Family-level migration approval does not automatically approve sub-slice migration.
- Historical artifacts missing denominator, taxonomy, row-set, scorer, split, or provenance markers should remain `reference-only` or `bridge-required`.
- Detector comparison should remain blocked unless comparison status is explicitly `comparison-allowed`.

This model preserves historical evidence without turning historical report-layer artifacts into proxy metrics.

## Remaining Blockers Before Implementation Planning

Implementation planning should not begin until the following blockers are resolved:

- Review and approval of the proposed top-level container architecture.
- Review and approval of the common governed-family envelope.
- Review and approval of the state model for completeness, current-run computability, and comparability.
- Review and approval of family-specific aggregate and sub-slice nesting.
- Review and approval of detector consumption boundaries.
- Review and approval of migration-status representation for historical baselines.
- Fixture plan covering complete, partial, missing, current-run noncomputable, comparison-allowed, bridge-required, reference-only, and comparison-blocked cases.
- Ownership review confirming dataset metadata, scorer, evaluator, detector, and migration review responsibilities remain separate.

## Stage B Planning Completeness Recommendation

Stage B.5 completes the first concrete schema proposal for the approved governance concepts.

Additional planning is still required before implementation planning:

- Stage B.6 should produce a schema review packet and fixture matrix for this proposal.
- The review packet should include acceptance criteria, migration-review scenarios, detector-consumption examples at the conceptual level, and explicit rejection cases for proxy or inferred metrics.
- Implementation planning should begin only after Stage B.6 approves the concrete schema proposal and validation fixture strategy.

Threshold redesign remains out of scope until redesigned emissions are implemented, validated, and migration status is reviewed.
