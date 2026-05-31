# Stage C0 Evaluator Implementation Entry Contract Lock

## Scope

This document freezes authoritative implementation-entry contracts required before Stage B evaluator implementation begins.

This is a contract-definition artifact, not implementation. It does not implement evaluator code, fixture harness code, scoring code, runtime code, schema code, or doctrine redesign.

## Authority Inputs

This contract lock reconciles and depends on:

- `STAGE_B_EVALUATOR_IMPLEMENTATION_READINESS_ASSESSMENT.md`
- `STAGE_B_EVALUATOR_ARCHITECTURE_DISCOVERY_AND_GAP_ANALYSIS.md`
- `STAGE_B_WP8A_SCENARIO_CATALOG.md`
- `STAGE_B_VALIDATION_FIXTURE_MATRIX_PLAN.md`
- `STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
- `STAGE_B_EVAL_REDESIGN_EMISSION_DESIGN.md`
- `STAGE_B_EVAL_REDESIGN_SCHEMA_PROPOSAL.md`
- `STAGE_B_WP3_FAMILY_A_SCORER_EVIDENCE_CONTRACT.md`
- `STAGE_B_WP3_SCORER_EVIDENCE_OUTPUT_DESIGN_REVIEW.md`
- `STAGE_B_B1_SYMBOL_NAME_OWNERSHIP_REVIEW.md`
- `STAGE_B_B2_ANCHOR_OWNERSHIP_REVIEW.md`
- `STAGE_B_B2_CONFLICTING_OWNERSHIP_REVIEW.md`
- `STAGE_B_B1_NI_SCENARIO_RECONCILIATION_REVIEW.md`
- `STAGE_B_CLOSURE_ASSESSMENT.md`
- `STAGE_B_COMPLETION_DETERMINATION.md`
- `STAGE_B_LESSONS_LEARNED_SUMMARY.md`
- `STAGE_B_TRANSITION_READINESS_ASSESSMENT.md`
- `manifests/reports/stage_b_wp8_validation/fixtures/*`

## Contract-Lock Determination

Contract-lock status: locked.

This document is the authoritative implementation-entry contract baseline for Stage C0 evaluator work.

## 1. State Model Contract

## 1.1 Canonical State Axes

Every governed concept MUST emit three independent axes:

1. `completeness`
2. `current_run_computability`
3. `comparability`

Allowed values:

- `completeness`: `complete | partial | missing`
- `current_run_computability`: `current-run computable | current-run noncomputable`
- `comparability`: `comparison-allowed | bridge-required | reference-only | comparison-blocked`

## 1.2 Required State Payload

Each governed concept state payload MUST include:

- `completeness`
- `current_run_computability`
- `comparability`
- `noncomputability_reasons` (array; empty allowed)
- `comparison_block_reasons` (array; required when comparability is not `comparison-allowed`, optional otherwise)

## 1.3 Axis Independence Rules

Implementations MUST preserve axis independence:

1. `current-run computable` does not imply `comparison-allowed`.
2. `partial` does not imply `current-run noncomputable` in all cases.
3. `comparison-allowed` can be false while current-run computation is true.
4. Family-level comparability MUST NOT auto-propagate to governed sub-slices.

## 1.4 Explicit Prohibition: Collapsed-State Implementations

The following are PROHIBITED:

1. Any single combined status replacing the three axes.
2. Mapping multiple axis combinations to one coarse label without preserving original values.
3. Deriving comparability directly from completeness or computability.
4. Inferring computability from comparability.

## 2. Schema Contract

This section defines required logical structures. Names MAY differ in code, but every required structure and field class MUST be represented.

## 2.1 Evaluator Input Structures

Required input structure classes:

1. `evaluation_context_input`:
   - run identity,
   - row-set identity,
   - split scope,
   - scorer semantics marker,
   - taxonomy markers,
   - baseline/migration references.
2. `row_fact_input`:
   - row identity,
   - split membership,
   - tool-expected eligibility,
   - expected tool behavior,
   - exclusion marker.
3. `family_membership_input`:
   - Family B1 read-file eligibility,
   - Family B1 symbol-name membership marker,
   - Family B1 parent-context linkage marker,
   - Family B2 anchor eligibility,
   - Family B2 anchor category,
   - Family B2 assignment ownership marker,
   - Family B2 taxonomy marker.
4. `scorer_evidence_input`:
   - exact-valid outcome,
   - primary scorer outcome,
   - Family A subtype or missing-evidence state,
   - failure taxonomy marker,
   - scorer semantics marker.
5. `comparability_input`:
   - concept-level migration/comparison markers,
   - denominator compatibility markers,
   - provenance markers for baseline use.

## 2.2 Evaluator Output Structures

Required output structure classes:

1. `family_summary_output`:
   - one envelope per governed family (`Family A`, `Family B1`, `Family B2`),
   - aggregate counts/denominators/rates,
   - governed sub-slice summaries.
2. `state_output`:
   - independent axis payload per governed concept.
3. `reconciliation_output`:
   - equation and boundedness checks,
   - pass/fail flags,
   - failure reasons.
4. `comparability_output`:
   - concept-scoped comparability states and reasons.
5. `noncomputability_output`:
   - explicit missing/blocked reasons keyed to governed concept.
6. `detector_projection_output`:
   - detector-consumable facts and states only, no raw reconstruction substrate.
7. `reporting_output`:
   - run summary and audit-ready metadata.

## 2.3 Row-Fact Structure Contract

Each row-fact record MUST support:

- row identity,
- split membership,
- governed-family eligibility markers,
- governed sub-slice membership markers where applicable,
- ownership markers where applicable,
- exclusion state and reason when excluded,
- provenance source reference.

Missing required row-fact fields MUST produce explicit noncomputability; they MUST NOT be inferred.

## 2.4 Family-Level Structure Contract

Each family envelope MUST contain:

1. family identity and activation state.
2. aggregate governed concept summary with count/denominator/rate.
3. governed sub-slice collection with per-sub-slice summaries.
4. per-concept state payloads.
5. comparability references.
6. noncomputability references.
7. reconciliation references.

## 2.5 Reconciliation Structure Contract

Reconciliation outputs MUST support:

1. Family A subtype partition reconciliation.
2. Family B1 parent/sub-slice denominator boundedness.
3. Family B2 category-to-family denominator reconciliation.
4. coverage-to-denominator reconciliation where emitted.
5. split-to-aggregate reconciliation where split scope is active.

Each check MUST include:

- check identifier,
- evaluated inputs,
- result (`pass|fail|blocked`),
- failure/block reason.

## 2.6 Reporting Structure Contract

Reporting structures MUST include:

- run metadata,
- family summaries,
- state distributions,
- reconciliation outcomes,
- comparability outcomes,
- noncomputability inventories,
- detector projection reference,
- provenance and version markers.

## 3. Artifact Contract

## 3.1 Required Emitted Artifacts

The implementation MUST emit, at minimum, the following artifact classes per run:

1. `evaluator_run_context_artifact`
2. `evaluator_row_fact_coverage_artifact`
3. `evaluator_family_summary_artifact`
4. `evaluator_state_artifact`
5. `evaluator_reconciliation_artifact`
6. `evaluator_comparability_artifact`
7. `evaluator_noncomputability_artifact`
8. `evaluator_detector_projection_artifact`
9. `evaluator_audit_artifact`

Physical filenames MAY vary, but each artifact class MUST exist and be addressable.

## 3.2 Required Evidence Fields

Required evidence fields across artifacts:

- governed concept identity,
- numerator/count evidence where applicable,
- denominator evidence where applicable,
- rate evidence where applicable,
- marker presence/absence evidence,
- reconciliation evidence,
- missing-evidence reasons where relevant.

## 3.3 Required Provenance Fields

Required provenance fields:

- run ID and timestamp,
- dataset/row-set identity,
- split scope identity,
- scorer/evaluator semantics markers,
- taxonomy marker versions,
- schema/contract version markers,
- baseline/migration reference identities.

## 3.4 Required Ownership Fields

Ownership fields MUST be explicit when ownership-governed concepts are involved:

- symbol-name membership ownership source,
- anchor assignment ownership source,
- taxonomy ownership markers where applicable,
- conflict markers when ownership evidence conflicts.

Missing/ambiguous/conflicting ownership MUST emit blocked/noncomputable state.

## 3.5 Required Denominator Fields

For each governed rate-like concept, artifacts MUST include:

- numerator/count,
- denominator,
- denominator scope identity,
- denominator provenance reference.

Cross-population denominator substitution is PROHIBITED.

## 3.6 Required Reconciliation Outputs

Artifacts MUST include:

- per-check reconciliation status,
- blocked/failure reasons,
- arithmetic inputs used,
- concept-level reconciliation summary.

Numeric consistency MUST NOT override marker/ownership failures.

## 4. Interface Boundary Contract

## 4.1 Subsystem Boundary Table

| Subsystem | Responsibilities | Required Inputs | Required Outputs |
|---|---|---|---|
| Ingestion | normalize run context and source handles | manifests, row sources, baseline refs | normalized context bundle |
| Row-fact metadata | emit declared eligibility/membership/ownership facts | normalized context + metadata sources | row-fact bundle + coverage summary |
| Scorer | emit exact-valid + Family A subtype/missing evidence | model outputs + expected behavior inputs | scorer evidence bundle |
| Family aggregation | compute family and sub-slice summaries | row-fact bundle + scorer evidence | family summary bundle |
| State engine | compute independent state axes per concept | family summaries + marker presence | state bundle |
| Reconciliation engine | execute arithmetic/scope checks | family summaries + states + coverage | reconciliation bundle |
| Comparability engine | classify concept-level baseline status | current-run outputs + migration markers + baseline refs | comparability bundle |
| Detector projection | expose consumer-only policy surface | family/state/reconciliation/comparability bundles | detector projection bundle |
| Fixture harness | validate outputs against WP8 fixture corpus | runtime bundles + fixture corpus | fixture validation report |
| Reporting | produce audit and execution reports | all bundles | run report package |

## 4.2 Boundary Rules

1. Subsystems MUST communicate via emitted bundles, not implicit shared inference.
2. Detector projection MUST be consumer-only and reconstruction-safe.
3. Fixture harness MUST validate emitted behavior; it MUST NOT reinterpret doctrine.
4. Comparability decisions MUST remain concept-scoped and marker-driven.

## 5. Governance Preservation Contract

## 5.1 Explicit Prohibitions

The following are PROHIBITED in implementation:

1. inference from prompt text for membership, taxonomy, ownership, subtype, denominator, or comparability.
2. inference from generated text for subtype or governed membership.
3. inference from report naming or path conventions.
4. inference from marker absence.
5. substitution of parent/sibling/mixed-tool/historical denominators.
6. reconstruction of missing facts from historical artifacts.
7. ownership auto-resolution for missing/conflicting markers.
8. migration-status inference by resemblance.
9. comparability-state collapse into binary comparable/non-comparable.
10. state-axis collapse into single composite status.

## 5.2 Conservative Failure Rules

Implementation MUST preserve conservative behavior:

1. missing required fact -> explicit noncomputability.
2. missing/invalid migration marker -> comparison blocked (or bridge/reference states as emitted).
3. ownership conflict -> governed concept blocked regardless of numeric reconciliation.
4. denominator missing -> governed rate blocked even when count exists.

## 6. Gap Resolution And Remaining Ambiguities

## 6.1 Blocking Ambiguity Assessment

Blocking contract ambiguities after this lock: none.

This contract lock resolves previously identified blocking ambiguity classes by freezing:

- state-axis independence,
- required logical schema structures,
- required artifact classes and field classes,
- subsystem boundaries and responsibilities,
- explicit governance prohibitions.

## 6.2 Non-Blocking Implementation Details

The following may be decided during implementation without violating this lock:

1. concrete file names/paths for required artifact classes.
2. concrete in-code type names.
3. serialization format details beyond required field classes.
4. operational packaging conventions for run reports.

These decisions MUST remain contract-conformant.

## 7. Implementation Readiness Determination

Implementation after contract lock: authorized to proceed.

Meaning:

- Contract-level blockers are closed.
- Implementation may begin under the locked contracts and established Stage B doctrine.
- Runtime implementation is still required before real-output execution is possible.

## 8. Recommended Next Milestone

Recommended next milestone: `Stage C1 - Evaluator Foundation Implementation`.

Entry objectives:

1. implement concrete schema/types for contract-locked structures.
2. implement ingestion + row-fact metadata + Family A scorer outputs.
3. implement initial family aggregation/state/reconciliation path.
4. implement fixture harness skeleton and validate common-state + Family A slices first.
5. produce first contract-conformance report against WP8 fixtures.
