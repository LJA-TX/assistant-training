# Stage B Evaluator Implementation Readiness Assessment

## Scope

This document determines what must be implemented to execute the Stage B evaluation framework against real model outputs after Stage B closure.

This is assessment-only documentation. It does not implement evaluator code, scorer code, detector code, runtime code, fixtures, schema files, or governance redesign.

## Reviewed Inputs

Planning and doctrine artifacts reviewed:

- `STAGE_B_IMPLEMENTATION_WORKPACKETS.md`
- `STAGE_B_EVAL_REDESIGN_METRIC_INVENTORY.md`
- `STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
- `STAGE_B_EVAL_REDESIGN_EMISSION_DESIGN.md`
- `STAGE_B_EVAL_REDESIGN_IMPLEMENTATION_READINESS.md`
- `STAGE_B_EVAL_REDESIGN_SCHEMA_READINESS.md`
- `STAGE_B_EVAL_REDESIGN_SCHEMA_PROPOSAL.md`
- `STAGE_B_VALIDATION_FIXTURE_MATRIX_PLAN.md`
- `STAGE_B_WP8A_SCENARIO_CATALOG.md`
- `STAGE_B_WP3_FAMILY_A_SCORER_EVIDENCE_CONTRACT.md`
- `STAGE_B_WP3_SCORER_EVIDENCE_OUTPUT_DESIGN_REVIEW.md`

Readiness, exit, and closure artifacts reviewed:

- `STAGE_B_IMPLEMENTATION_READINESS_REVIEW.md`
- `STAGE_B_WP8_B2_EXIT_REVIEW.md`
- `STAGE_B_WP8_CROSS_FAMILY_EXECUTION_READINESS_ASSESSMENT.md`
- `STAGE_B_WP8_CROSS_FAMILY_CLOSURE_ASSESSMENT.md`
- `STAGE_B_CLOSURE_ASSESSMENT.md`
- `STAGE_B_COMPLETION_DETERMINATION.md`
- `STAGE_B_LESSONS_LEARNED_SUMMARY.md`
- `STAGE_B_TRANSITION_READINESS_ASSESSMENT.md`
- `STAGE_B_B1_NI_SCENARIO_RECONCILIATION_REVIEW.md`

Fixture corpus reviewed:

- `manifests/reports/stage_b_wp8_validation/fixtures/common_state/*`
- `manifests/reports/stage_b_wp8_validation/fixtures/family_a/*`
- `manifests/reports/stage_b_wp8_validation/fixtures/family_b1/*`
- `manifests/reports/stage_b_wp8_validation/fixtures/family_b2/*`
- `manifests/reports/stage_b_wp8_validation/fixtures/cross_family/*`

Current executable surfaces reviewed:

- `scripts/eval_canonical_manifest.py`
- `scripts/eval_adapter_toolcalls.py`
- `scripts/post_eval_collapse_detector.py`
- `manifests/reports/stage_b_v1_threshold_profile.json`

Grok advisory input:

- No repository-captured Grok review artifact was found by filename or content search.

## Evidence Snapshot

Scenario and fixture reconciliation status:

- Planned catalog scenarios (`A`, `B1`, `B2`, `X`): `99`
- Authored catalog fixtures: `99`
- Missing scenario IDs: `0`
- Extra scenario IDs: `0`
- Expected-state mismatches: `0`
- `fixture_id` vs `source_definition_id` mismatches: `0`

WP8 fixture corpus size:

- Common-state fixtures (`WP8B-*`): `18`
- Catalog fixtures (`A/B1/B2/X`): `99`
- Total visible fixture artifacts: `117`

Current implementation state:

- No code path currently consumes `stage_b_wp8_validation` fixtures.
- Current evaluator (`eval_canonical_manifest.py`) emits legacy aggregate class metrics, not Stage B family envelopes or comparability/noncomputability state.
- Current detector (`post_eval_collapse_detector.py`) is profile-driven against metric-path catalogs and does not consume Stage B family/state outputs.

## Implementation Requirements

The following capabilities are required before the Stage B framework can run on real outputs.

### 1. Required Evaluator Inputs

Mandatory input families:

1. Row identity and split membership.
2. Tool-expected eligibility and expected tool behavior.
3. Exclusion state before aggregation.
4. Family B1 membership facts:
   - read-file eligibility,
   - symbol-name sub-slice membership,
   - parent read-file context linkage.
5. Family B2 membership facts:
   - anchor-generalization eligibility,
   - anchor category assignment,
   - assignment ownership marker,
   - taxonomy marker.
6. Scorer outputs:
   - exact-valid status,
   - primary outcome,
   - Family A subtype assignment or missing-evidence state,
   - scorer semantics and taxonomy markers.
7. Migration/comparability markers at concept level (family and governed sub-slice).

### 2. Required Evaluator Outputs

Mandatory output groups:

1. Family summaries for `Family A`, `Family B1`, `Family B2`.
2. Governed sub-slice summaries:
   - direct-answer substitution subtype (A),
   - symbol-name sub-slice (B1),
   - no-anchor sub-slice (B2).
3. Count/denominator/rate triads for governed rate-like concepts.
4. Split-scoped summaries when activated by emitted split-scope markers.
5. Coverage summaries and reconciliation statuses.
6. State outputs per concept:
   - completeness (`complete|partial|missing`),
   - current-run computability (`current-run computable|current-run noncomputable`),
   - comparability (`comparison-allowed|bridge-required|reference-only|comparison-blocked`),
   - explicit noncomputability/comparison-block reasons.
7. Detector-consumption projection that contains only emitted aggregate/state facts (no reconstruction inputs).

### 3. Required Fixture-Loading Behavior

Loader and validator behavior required by corpus structure:

1. Must parse all `117` fixture files and preserve order determinism.
2. Must enforce universal required top-level keys present in all fixtures:
   - `fixture_id`,
   - `source_definition_id`,
   - `source_documents`,
   - `classification`,
   - `required_inputs`,
   - `expected_state`,
   - `expected_detector_treatment`,
   - `expected_reconciliation_behavior`,
   - `acceptance_criteria`,
   - `rationale`.
3. Must support family/common-state optional keys without normalization loss:
   - `family`, `scenario_type`, `governed_concept`,
   - `scorer_evidence_expectations`,
   - `ownership_expectations`,
   - `intended_subtype`/`intended_subslice_or_state`,
   - `precedence_expectations`, `control_status`, `primary_coverage`.
4. Must validate `expected_state` axes and maintain separability of:
   - completeness,
   - current-run computability,
   - comparability.
5. Must reject fixture interpretation logic that infers missing facts from prompts, names, paths, or historical reports.

### 4. Required Scoring Behavior

Required scorer implementation behavior:

1. Deterministic exact-valid partition for tool-expected rows.
2. Deterministic Family A subtype assignment for eligible non-exact rows, or explicit missing-evidence state.
3. No generic implicit `other` subtype assignment.
4. Explicit precedence handling between neighboring subtype classes.
5. Marker emission:
   - failure taxonomy marker,
   - scorer semantics marker.
6. No detector-time or evaluator-time subtype reconstruction from generated text.

### 5. Required Reconciliation Behavior

Required reconciliation checks:

1. Denominator partition and subtype-sum reconciliation for Family A.
2. Parent/sub-slice boundedness reconciliation for Family B1 symbol-name.
3. Anchor-category distribution reconciliation for Family B2.
4. Coverage reconciliation (`covered + uncovered = governed denominator`) where required.
5. Split-to-aggregate reconciliation when split-scoped summaries are active.
6. Reconciliation failure must not silently downgrade to pass; it must produce explicit noncomputability/blocked states.

### 6. Required Comparability Behavior

Required comparability behavior:

1. Concept-level comparability statuses must be emitted explicitly.
2. Family-level comparison approval must not auto-propagate to governed sub-slices.
3. Historical values must stay `reference-only` or `bridge-required` unless explicit comparison-allowed evidence is emitted.
4. Missing migration markers must block comparison even with computable current-run values.
5. Denominator incompatibility must block comparison and block substitution.

### 7. Required Non-Inference Enforcement Behavior

Required doctrine enforcement:

1. No prompt-text inference for membership, taxonomy, ownership, denominator, subtype, or comparability.
2. No generated-text inference for subtype or membership.
3. No report-name/path-convention inference.
4. No historical reconstruction as current-run evidence.
5. No denominator substitution across parent/sibling/mixed-tool/historical populations.
6. No ownership auto-resolution for missing or conflicting markers.

### 8. Required Reporting Behavior

Minimum reporting artifacts for production runs:

1. Family-level and governed-sub-slice summaries with state and reconciliation outputs.
2. Noncomputability and comparison-block reason inventory.
3. Coverage and exclusion accounting.
4. Detector-ready projection plus provenance markers.
5. Run-level audit metadata:
   - input paths/hashes,
   - schema/version markers,
   - taxonomy/marker versions,
   - baseline/migration references.

## Readiness Determination

Overall readiness: partially implementation-ready.

Rationale:

1. Architecture and doctrine are sufficiently specified for implementation planning and subsystem decomposition.
2. Fixture corpus is complete, reconciled, and governance-rich (`117` fixtures with full state coverage).
3. Critical runtime implementation surfaces are still absent:
   - no Stage B family-output evaluator implementation,
   - no fixture-driven validator harness wired to runtime outputs,
   - no implemented metadata/scorer/evaluator pipeline for Family A/B1/B2 contracts,
   - no detector consumption path for Stage B family-state outputs.
4. Existing live evaluator/detector surfaces are still legacy-profile oriented and structurally incompatible with Stage B family output requirements.

Therefore the project is ready to start implementation work under controlled milestones, but not ready to execute the full Stage B framework against real outputs today.

## Recommended Next Implementation Milestone

Recommended next milestone: `WP1+WP2+WP3 implementation-entry gate and contract lock`.

Milestone objective:

1. Freeze concrete schema contract for Stage B family outputs (field-level, enum-level, artifact-level).
2. Implement row-fact metadata emitter/adapter for required ownership markers and memberships.
3. Implement Family A scorer evidence outputs (exact-valid partition plus subtype/missing-evidence markers).
4. Add fixture-runner skeleton capable of loading all `117` fixtures and validating output schema/state surfaces.

Exit criteria for this milestone:

1. Stage B output schema contract approved and executable.
2. Metadata/scorer outputs satisfy fixture-required input availability for at least common-state + Family A.
3. Fixture runner validates structural and state invariants without inference behavior.
4. No doctrine violations in non-inference, ownership, denominator, or comparability handling.
