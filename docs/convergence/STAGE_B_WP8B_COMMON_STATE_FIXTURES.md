# Stage B WP8-B Common State Fixture Definitions

## Scope

This document converts WP8-A cross-family state scenarios into fixture-ready definitions.

This is documentation-only planning. It does not create fixture files, implement validators, implement schemas, modify code, modify detectors, modify evaluators, modify scorers, modify thresholds, modify governance rules, modify mappings, or modify manifests.

Reference inputs:

- `STAGE_B_VALIDATION_FIXTURE_MATRIX_PLAN.md`
- `STAGE_B_WP8A_SCENARIO_CATALOG.md`

WP8-B purpose:

- Define common state fixture expectations before family-specific fixtures are authored.
- Cover complete, partial, missing, current-run computable, current-run noncomputable, comparability, denominator-missing, marker-missing, parent/sub-slice divergence, and detector non-inference negative cases.
- Keep fixture expectations independent of concrete schema field names.

## Common Fixture Rules

- A fixture may be family-neutral, but every fixture must be applicable to at least one approved family or governed sub-slice.
- Expected emitted state must distinguish completeness, current-run computability, and comparability.
- Missing facts must not be represented as zero counts, zero denominators, or zero rates.
- Detector behavior must consume emitted facts and states only.
- Detector behavior must not reconstruct missing row facts, sub-slices, denominators, rates, markers, or migration status.
- Parent-family computability must not imply governed sub-slice computability.
- Current-run computability must not imply historical comparison eligibility.

## Fixture Definition Index

| Fixture ID | Primary Coverage |
|---|---|
| WP8B-CS-001 | Complete state and current-run computable |
| WP8B-CS-002 | Partial state |
| WP8B-CS-003 | Missing family |
| WP8B-CS-004 | Missing governed sub-slice |
| WP8B-CS-005 | Denominator missing |
| WP8B-CS-006 | Marker missing |
| WP8B-CS-007 | Current-run computable and comparison-blocked |
| WP8B-CS-008 | Current-run noncomputable and comparison-blocked |
| WP8B-CS-009 | Comparison-allowed |
| WP8B-CS-010 | Bridge-required |
| WP8B-CS-011 | Reference-only |
| WP8B-CS-012 | Parent computable and sub-slice noncomputable |
| WP8B-CS-013 | Missing source row fact |
| WP8B-CS-014 | Missing scorer fact |
| WP8B-CS-015 | Conflicting ownership marker |
| WP8B-NI-001 | Detector non-inference: alternate denominator |
| WP8B-NI-002 | Detector non-inference: historical report-layer value |
| WP8B-NI-003 | Detector non-inference: prompt or generated-text classification |

## Fixture Definitions

### WP8B-CS-001: Complete State

Purpose:

- Prove that a governed concept with all required inputs emits complete state and is current-run computable.

Required inputs:

- Active family or governed sub-slice is registered.
- Required source row facts are present.
- Required scorer facts are present.
- Required count, denominator, and rate concepts are present for rate-like metrics.
- Required completeness, noncomputability, and comparability markers are present.
- Reconciliation evidence is present.

Expected emitted state:

- Completeness state: complete.
- Current-run computability state: current-run computable.
- Comparability state: comparison-blocked unless a comparison-allowed fixture explicitly applies.
- Noncomputability reasons: none for the governed concept.

Expected detector behavior:

- Consume emitted facts and emitted states.
- Treat the concept as available for current-run evaluation.
- Do not infer historical comparison eligibility.

Expected reconciliation behavior:

- Count, denominator, and rate reconcile.
- Coverage count reconciles with governed denominator.
- Split summaries reconcile when active.
- Exclusions are visible and omitted from governed denominators.

Acceptance criteria:

- Fixture passes only when all required emitted facts and state markers are present.
- Any missing required fact changes expected outcome to partial, missing, or noncomputable.

### WP8B-CS-002: Partial State

Purpose:

- Prove that incomplete but present emission is represented as partial and cannot pass as complete.

Required inputs:

- Active family or governed sub-slice is registered.
- Some required aggregate or state facts are present.
- At least one required sub-slice, denominator, marker, split summary, source coverage item, or reconciliation item is absent.

Expected emitted state:

- Completeness state: partial.
- Current-run computability state: current-run noncomputable for the affected governed concept unless the missing item is explicitly diagnostic-only.
- Comparability state: comparison-blocked.
- Noncomputability reasons: present for missing required facts.

Expected detector behavior:

- Report partial state.
- Evaluate only independent concepts that remain complete and computable.
- Do not promote partial emission to complete.

Expected reconciliation behavior:

- Available facts may reconcile locally.
- Governed concept reconciliation fails or remains blocked for the missing required item.

Acceptance criteria:

- Fixture fails if detector accepts partial emission as complete.
- Fixture fails if a parent aggregate or sibling concept fills the missing state.

### WP8B-CS-003: Missing Family

Purpose:

- Prove that an active governed family absent from emission is missing and current-run noncomputable.

Required inputs:

- Family registry declares a governed family active.
- The corresponding family summary is absent.
- No approved non-emission exemption is present.

Expected emitted state:

- Completeness state: missing.
- Current-run computability state: current-run noncomputable.
- Comparability state: comparison-blocked.
- Noncomputability reasons: missing family.

Expected detector behavior:

- Report missing family.
- Preserve conservative governance behavior for dependent rules.
- Do not infer the family from lower-level rows, sibling families, or historical artifacts.

Expected reconciliation behavior:

- No family count, denominator, rate, or sub-slice reconciliation is allowed.

Acceptance criteria:

- Fixture passes only if the missing family blocks dependent governed evaluation.
- Fixture fails if the missing family is treated as zero, ignored, or reconstructed.

### WP8B-CS-004: Missing Governed Sub-Slice

Purpose:

- Prove that a missing required sub-slice remains noncomputable even when the parent family exists.

Required inputs:

- Parent family is active and emitted.
- Governed sub-slice is registered as required.
- Governed sub-slice summary is absent.

Expected emitted state:

- Parent completeness state: complete or partial according to parent facts.
- Sub-slice completeness state: missing.
- Sub-slice current-run computability state: current-run noncomputable.
- Sub-slice comparability state: comparison-blocked.
- Noncomputability reasons: missing governed sub-slice.

Expected detector behavior:

- Consume parent family only for independent parent-level review.
- Block sub-slice governed evaluation.
- Do not substitute the parent family aggregate for the sub-slice.

Expected reconciliation behavior:

- Parent family may reconcile.
- Sub-slice count, denominator, rate, and parent-child reconciliation are blocked.

Acceptance criteria:

- Fixture fails if parent aggregate satisfies sub-slice expectations.
- Fixture passes only if sub-slice missing state is explicit.

### WP8B-CS-005: Denominator Missing

Purpose:

- Prove that count-only evidence does not become a governed rate or comparison input.

Required inputs:

- Governed concept is active.
- Numerator-like count is present.
- Required denominator basis is absent.
- No approved denominator substitute exists.

Expected emitted state:

- Completeness state: partial.
- Current-run computability state: current-run noncomputable for the rate-like concept.
- Comparability state: comparison-blocked.
- Noncomputability reasons: missing denominator.

Expected detector behavior:

- Treat count-only evidence as diagnostic at most.
- Do not compute rate.
- Do not borrow another denominator.

Expected reconciliation behavior:

- Rate reconciliation is blocked.
- Count may be visible but does not satisfy governed rate requirements.

Acceptance criteria:

- Fixture fails if any alternate denominator is used.
- Fixture fails if count-only evidence is treated as complete.

### WP8B-CS-006: Marker Missing

Purpose:

- Prove that missing required markers block governed computation or comparison according to marker role.

Required inputs:

- Governed concept is active.
- Counts, denominators, and rates may be present.
- Required taxonomy, subpopulation, anchor, scorer, population, split, or migration marker is absent.

Expected emitted state:

- Completeness state: partial when current-run marker is missing; complete may remain possible when only baseline-comparison marker is missing.
- Current-run computability state: current-run noncomputable if the missing marker is required for current-run semantics.
- Comparability state: comparison-blocked if the missing marker is required for baseline comparison.
- Noncomputability reasons: missing marker or comparison marker missing.

Expected detector behavior:

- Report missing marker.
- Do not infer marker from artifact name, prompt text, generated text, or historical report shape.
- Block comparison when comparability marker is absent.

Expected reconciliation behavior:

- Numeric reconciliation may pass diagnostically.
- Governed semantic or comparison reconciliation fails for missing marker.

Acceptance criteria:

- Fixture passes only if marker absence changes state as expected.
- Fixture fails if detector treats marker absence as harmless.

### WP8B-CS-007: Current-Run Computable And Comparison-Blocked

Purpose:

- Prove that current-run computability and historical comparison eligibility remain separate.

Required inputs:

- Governed concept has complete current-run facts.
- Count, denominator, and rate reconcile.
- Required migration status is absent or explicitly comparison-blocked.

Expected emitted state:

- Completeness state: complete.
- Current-run computability state: current-run computable.
- Comparability state: comparison-blocked.
- Noncomputability reasons: none for current run; comparison-block reason present.

Expected detector behavior:

- Permit current-run evaluation where applicable.
- Block historical comparison and deltas.
- Do not infer comparison eligibility.

Expected reconciliation behavior:

- Current-run reconciliation passes.
- Baseline reconciliation is blocked by comparison status.

Acceptance criteria:

- Fixture fails if current-run computability automatically permits comparison.
- Fixture fails if comparison-blocked state suppresses valid current-run facts.

### WP8B-CS-008: Current-Run Noncomputable And Comparison-Blocked

Purpose:

- Prove that a noncomputable current run also blocks comparison for the affected concept.

Required inputs:

- Governed concept is active.
- At least one current-run required family, sub-slice, denominator, source fact, scorer fact, or marker is missing.
- Historical baseline may be present.

Expected emitted state:

- Completeness state: missing or partial, depending on available facts.
- Current-run computability state: current-run noncomputable.
- Comparability state: comparison-blocked.
- Noncomputability reasons: current-run missing fact and comparison blocked.

Expected detector behavior:

- Block current-run governed evaluation for affected concept.
- Block historical comparison.
- Preserve conservative noncomputability behavior.

Expected reconciliation behavior:

- Current-run reconciliation is blocked at the missing item.
- Baseline reconciliation is not attempted for the affected concept.

Acceptance criteria:

- Fixture passes only if both current-run and comparison paths are blocked.
- Fixture fails if historical baseline is used to repair current-run noncomputability.

### WP8B-CS-009: Comparison-Allowed

Purpose:

- Prove that detector comparison runs only when concept-level migration status allows it.

Required inputs:

- Governed concept has complete current-run facts.
- Current-run facts reconcile.
- Historical baseline facts exist for the same governed concept.
- Migration review emits comparison-allowed for that specific concept.
- Population, denominator, scorer, taxonomy or subpopulation, split, row-set, and exclusion markers are compatible or approved by bridge.

Expected emitted state:

- Completeness state: complete.
- Current-run computability state: current-run computable.
- Comparability state: comparison-allowed.
- Noncomputability reasons: none for comparison.

Expected detector behavior:

- Run comparison only for the approved concept.
- Do not apply approval to sibling concepts or sub-slices unless separately approved.

Expected reconciliation behavior:

- Current-run reconciliation passes.
- Baseline comparability reconciliation passes for approved markers.

Acceptance criteria:

- Fixture passes only if comparison is concept-scoped.
- Fixture fails if family-level approval automatically approves sub-slices.

### WP8B-CS-010: Bridge-Required

Purpose:

- Prove that related historical evidence remains blocked until bridge review approves comparability.

Required inputs:

- Governed concept has complete current-run facts.
- Historical value appears related but differs in taxonomy, subpopulation, denominator, scorer semantics, split, or provenance.
- Migration status is bridge-required.

Expected emitted state:

- Completeness state: complete.
- Current-run computability state: current-run computable.
- Comparability state: bridge-required.
- Noncomputability reasons: none for current run; bridge required for comparison.

Expected detector behavior:

- Permit current-run evaluation where applicable.
- Block historical comparison.
- Report bridge-required status.

Expected reconciliation behavior:

- Current-run reconciliation passes.
- Baseline comparison reconciliation remains unresolved.

Acceptance criteria:

- Fixture fails if detector runs comparison before bridge approval.
- Fixture fails if related historical evidence is treated as equivalent by resemblance.

### WP8B-CS-011: Reference-Only

Purpose:

- Prove that historical values can remain available to human review without supporting detector comparison.

Required inputs:

- Governed concept has complete current-run facts.
- Historical value exists but lacks sufficient denominator, marker, population, scorer, taxonomy, split, or provenance evidence.
- Migration status is reference-only.

Expected emitted state:

- Completeness state: complete.
- Current-run computability state: current-run computable.
- Comparability state: reference-only.
- Noncomputability reasons: none for current run; reference-only reason present for baseline.

Expected detector behavior:

- Do not run comparative rules or deltas.
- Preserve current-run facts.
- Report reference-only status.

Expected reconciliation behavior:

- Current-run reconciliation passes.
- Historical comparison reconciliation is not allowed.

Acceptance criteria:

- Fixture fails if reference-only historical values affect detector outcome.
- Fixture passes only if reference evidence remains non-comparative.

### WP8B-CS-012: Parent Computable And Sub-Slice Noncomputable

Purpose:

- Prove that a computable parent family does not repair a noncomputable required sub-slice.

Required inputs:

- Parent family aggregate is complete and current-run computable.
- Governed sub-slice is active.
- Governed sub-slice is missing a required membership, denominator, marker, or summary.

Expected emitted state:

- Parent completeness state: complete.
- Parent current-run computability state: current-run computable.
- Sub-slice completeness state: partial or missing.
- Sub-slice current-run computability state: current-run noncomputable.
- Sub-slice comparability state: comparison-blocked.

Expected detector behavior:

- Permit parent-level current-run review only where independent.
- Block sub-slice governed evaluation.
- Do not substitute parent aggregate for sub-slice.

Expected reconciliation behavior:

- Parent reconciliation passes.
- Sub-slice reconciliation fails or remains blocked.

Acceptance criteria:

- Fixture fails if sub-slice passes through parent aggregate substitution.
- Fixture passes only if parent and sub-slice states are independently represented.

### WP8B-CS-013: Missing Source Row Fact

Purpose:

- Prove that missing row-level source facts block downstream governed aggregation.

Required inputs:

- Governed concept is active.
- Required source row fact is absent, such as family eligibility, sub-slice membership, anchor category, row identity, split membership, or exclusion state.

Expected emitted state:

- Completeness state: missing or partial.
- Current-run computability state: current-run noncomputable.
- Comparability state: comparison-blocked.
- Noncomputability reasons: missing source row fact.

Expected detector behavior:

- Report missing source row fact.
- Do not inspect raw rows or prompt text to infer the missing fact.

Expected reconciliation behavior:

- Dependent denominator and coverage reconciliation are blocked.

Acceptance criteria:

- Fixture fails if aggregation proceeds using inferred source facts.
- Fixture passes only if dependent governed concept remains noncomputable.

### WP8B-CS-014: Missing Scorer Fact

Purpose:

- Prove that missing scorer facts block exact-valid rates or subtype aggregates.

Required inputs:

- Governed concept is active.
- Required scorer fact is absent, such as exact-valid outcome, primary outcome, or failure subtype.

Expected emitted state:

- Completeness state: missing or partial.
- Current-run computability state: current-run noncomputable.
- Comparability state: comparison-blocked.
- Noncomputability reasons: missing scorer fact.

Expected detector behavior:

- Report missing scorer fact.
- Do not infer scorer outcome from generated text, parse state, or other metrics.

Expected reconciliation behavior:

- Numerator, exact/non-exact partition, or subtype distribution reconciliation is blocked.

Acceptance criteria:

- Fixture fails if detector or evaluator repairs missing scorer fact from generated output.
- Fixture passes only if affected concept remains noncomputable.

### WP8B-CS-015: Conflicting Ownership Marker

Purpose:

- Prove that conflicting metadata ownership blocks governed use instead of letting the detector choose a source.

Required inputs:

- Governed concept is active.
- Two or more emitted ownership markers conflict for a taxonomy, subpopulation, anchor category, or source fact.
- No approved conflict-resolution marker is emitted.

Expected emitted state:

- Completeness state: partial.
- Current-run computability state: current-run noncomputable for affected concept.
- Comparability state: comparison-blocked.
- Noncomputability reasons: conflicting ownership marker.

Expected detector behavior:

- Report ownership conflict.
- Do not pick one ownership source.
- Do not infer a resolved marker.

Expected reconciliation behavior:

- Numeric reconciliation may be present but is not governed-valid while ownership conflict remains.

Acceptance criteria:

- Fixture fails if detector resolves conflict by preference order.
- Fixture passes only if affected governed concept is blocked.

### WP8B-NI-001: Detector Non-Inference Negative, Alternate Denominator

Purpose:

- Prove that detector does not use another population's denominator when the governed denominator is missing.

Required inputs:

- Governed count is present.
- Governed denominator is missing.
- A related parent, sibling, mixed-tool, or historical denominator is present.

Expected emitted state:

- Completeness state: partial.
- Current-run computability state: current-run noncomputable.
- Comparability state: comparison-blocked.
- Noncomputability reasons: missing denominator.

Expected detector behavior:

- Reject alternate denominator.
- Do not compute rate.
- Report missing governed denominator.

Expected reconciliation behavior:

- Governed rate reconciliation is blocked.
- Alternate denominator is not considered a valid reconciliation input.

Acceptance criteria:

- Fixture fails if any alternate denominator produces a rate.
- Fixture passes only if affected governed concept remains noncomputable.

### WP8B-NI-002: Detector Non-Inference Negative, Historical Report-Layer Value

Purpose:

- Prove that detector does not treat report-layer historical values as comparable facts without migration status.

Required inputs:

- Current-run governed concept is complete and computable.
- Historical report-layer value exists.
- Concept-level migration status is absent, bridge-required, or reference-only.

Expected emitted state:

- Completeness state: complete.
- Current-run computability state: current-run computable.
- Comparability state: comparison-blocked, bridge-required, or reference-only according to emitted migration status.
- Noncomputability reasons: none for current run; comparison reason present.

Expected detector behavior:

- Do not run comparison unless status is comparison-allowed.
- Do not infer comparability from artifact name, path, or metric resemblance.

Expected reconciliation behavior:

- Current-run reconciliation passes.
- Historical comparison reconciliation is blocked or unavailable.

Acceptance criteria:

- Fixture fails if historical value affects detector outcome without comparison-allowed status.
- Fixture passes only if current-run and comparison states remain separate.

### WP8B-NI-003: Detector Non-Inference Negative, Prompt Or Generated-Text Classification

Purpose:

- Prove that detector does not classify missing subtypes, sub-slices, or anchor categories from text.

Required inputs:

- Prompt text or generated text appears to imply a subtype, symbol-name membership, no-anchor membership, or another governed label.
- Required emitted label or marker is absent.

Expected emitted state:

- Completeness state: missing or partial.
- Current-run computability state: current-run noncomputable for affected concept.
- Comparability state: comparison-blocked.
- Noncomputability reasons: missing emitted label or marker.

Expected detector behavior:

- Do not inspect prompt text or generated text to repair missing label.
- Report missing emitted label or marker.

Expected reconciliation behavior:

- Subtype, sub-slice, or anchor denominator reconciliation is blocked.

Acceptance criteria:

- Fixture fails if detector classifies from text.
- Fixture passes only if affected concept remains noncomputable.

## Coverage Mapping

| Required Coverage | Fixture IDs |
|---|---|
| Complete state | WP8B-CS-001 |
| Partial state | WP8B-CS-002, WP8B-CS-005, WP8B-CS-006, WP8B-CS-012, WP8B-CS-015 |
| Missing state | WP8B-CS-003, WP8B-CS-004, WP8B-CS-013, WP8B-CS-014, WP8B-NI-003 |
| Current-run computable | WP8B-CS-001, WP8B-CS-007, WP8B-CS-009, WP8B-CS-010, WP8B-CS-011, WP8B-NI-002 |
| Current-run noncomputable | WP8B-CS-002, WP8B-CS-003, WP8B-CS-004, WP8B-CS-005, WP8B-CS-006, WP8B-CS-008, WP8B-CS-012, WP8B-CS-013, WP8B-CS-014, WP8B-CS-015, WP8B-NI-001, WP8B-NI-003 |
| Comparison-allowed | WP8B-CS-009 |
| Bridge-required | WP8B-CS-010 |
| Reference-only | WP8B-CS-011 |
| Comparison-blocked | WP8B-CS-003, WP8B-CS-004, WP8B-CS-005, WP8B-CS-006, WP8B-CS-007, WP8B-CS-008, WP8B-CS-012, WP8B-CS-013, WP8B-CS-014, WP8B-CS-015, WP8B-NI-001, WP8B-NI-002, WP8B-NI-003 |
| Denominator-missing | WP8B-CS-005, WP8B-NI-001 |
| Marker-missing | WP8B-CS-006, WP8B-NI-003 |
| Parent computable and sub-slice noncomputable | WP8B-CS-012 |
| Detector non-inference negatives | WP8B-NI-001, WP8B-NI-002, WP8B-NI-003 |

## Acceptance Gates For WP8-B

WP8-B is complete when:

- Every required common state has at least one fixture-ready definition.
- Each definition lists purpose, required inputs, expected emitted state, expected detector behavior, expected reconciliation behavior, and acceptance criteria.
- Detector non-inference negatives are explicit.
- No fixture definition requires schema field names or runtime implementation.
- No fixture definition permits proxy, inferred, reconstructed, or parent-aggregate substitution.

## Recommendation For WP8-C Readiness

WP8-C should not begin as fixture-file authoring until Family A subtype boundaries are approved.

WP8-C may begin as planning when:

- WP8-B common state definitions are accepted.
- The Family A scenarios in `STAGE_B_WP8A_SCENARIO_CATALOG.md` are accepted as the scenario baseline.
- The direct-answer substitution governed subtype remains required.
- The subtype list and boundary rules are ready for review.

Recommended WP8-C first step:

- Produce a Family A subtype boundary table that maps each planned Family A scenario to an approved subtype, required scorer fact, missing-state behavior, and detector non-inference expectation.

WP8-C should still avoid fixture files, validator implementation, schema implementation, and code changes until implementation authorization is explicit.
