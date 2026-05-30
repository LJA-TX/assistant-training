# Stage B WP8 Execution Plan

## Scope

This document defines the first executable fixture-authoring slice for WP8 Validation Fixtures.

This is execution planning for fixture creation. It is not architecture planning and it does not create fixture files, implement validators, implement schemas, modify runtime behavior, modify detectors, modify scorers, modify evaluators, modify thresholds, modify governance rules, modify mappings, or modify manifests.

Reference inputs:

- `STAGE_B_IMPLEMENTATION_WORKPACKETS.md`
- `STAGE_B_IMPLEMENTATION_READINESS_REVIEW.md`
- `STAGE_B_VALIDATION_FIXTURE_MATRIX_PLAN.md`
- `STAGE_B_WP8A_SCENARIO_CATALOG.md`
- `STAGE_B_WP8B_COMMON_STATE_FIXTURES.md`
- `STAGE_B_WP8C_FAMILY_A_SUBTYPE_BOUNDARY_REVIEW.md`
- `STAGE_B_WP8C_SCENARIO_TO_SUBTYPE_MAPPING.md`
- `STAGE_B_WP3_FAMILY_A_SCORER_EVIDENCE_CONTRACT.md`
- `STAGE_B_WP3_SCORER_EVIDENCE_OUTPUT_DESIGN_REVIEW.md`

Execution premise:

- WP8 is the only Stage B packet currently ready for bounded execution.
- The first execution slice must author fixtures only.
- Common-state and Family A fixtures can begin before Family B1 and Family B2 ownership decisions are complete.
- Validator implementation remains a later packet.

## 1. WP8 Execution Scope

### Included In WP8 Phase 1

WP8 Phase 1 includes authoring fixture files for:

- Common state fixtures from `STAGE_B_WP8B_COMMON_STATE_FIXTURES.md`.
- Family A scenario fixtures from `STAGE_B_WP8A_SCENARIO_CATALOG.md`.
- Family A subtype mapping expectations from `STAGE_B_WP8C_SCENARIO_TO_SUBTYPE_MAPPING.md`.
- Detector non-inference negatives that apply to common-state and Family A scenarios.
- Reconciliation expectations that apply to common-state and Family A scenarios.

WP8 Phase 1 fixture files should be self-contained enough for later validator work to consume, but they must not require validator implementation in this slice.

### Excluded From WP8 Phase 1

WP8 Phase 1 excludes:

- Validator implementation.
- Schema implementation.
- Runtime implementation.
- Detector implementation.
- Scorer implementation.
- Evaluator implementation.
- Threshold changes.
- Family B1 fixture files that require final symbol-name ownership.
- Family B2 fixture files that require final anchor taxonomy or anchor ownership.
- Migration execution beyond common comparability-state fixtures.

### First Execution Slice

First execution slice: WP8 Phase 1A, Common-State Fixture Files.

Rationale:

- Common-state fixtures are family-neutral.
- They exercise complete, partial, missing, denominator-missing, marker-missing, current-run computable, current-run noncomputable, comparison-allowed, bridge-required, reference-only, comparison-blocked, parent/sub-slice divergence, and detector non-inference states.
- They do not depend on unresolved Family B1 or Family B2 ownership.
- They create the expected-state vocabulary needed before Family A fixture files are authored.

## 2. Initial Fixture Files

The proposed fixture root for WP8 Phase 1 is:

- `manifests/reports/stage_b_wp8_validation/fixtures/`

This root follows the repository's existing pattern for validation fixture artifacts under `manifests/reports/phase4_validation/fixtures/` while keeping Stage B redesign fixtures isolated.

### Common-State Fixture File Set

Initial common-state fixture files:

| Planned File | Source Definition | Primary Coverage |
|---|---|---|
| `common_state/wp8b_cs_001_complete_state.json` | `WP8B-CS-001` | Complete state and current-run computable. |
| `common_state/wp8b_cs_002_partial_state.json` | `WP8B-CS-002` | Partial state. |
| `common_state/wp8b_cs_003_missing_family.json` | `WP8B-CS-003` | Missing family. |
| `common_state/wp8b_cs_004_missing_governed_subslice.json` | `WP8B-CS-004` | Missing governed sub-slice. |
| `common_state/wp8b_cs_005_denominator_missing.json` | `WP8B-CS-005` | Denominator missing. |
| `common_state/wp8b_cs_006_marker_missing.json` | `WP8B-CS-006` | Marker missing. |
| `common_state/wp8b_cs_007_computable_comparison_blocked.json` | `WP8B-CS-007` | Current-run computable and comparison-blocked. |
| `common_state/wp8b_cs_008_noncomputable_comparison_blocked.json` | `WP8B-CS-008` | Current-run noncomputable and comparison-blocked. |
| `common_state/wp8b_cs_009_comparison_allowed.json` | `WP8B-CS-009` | Comparison-allowed. |
| `common_state/wp8b_cs_010_bridge_required.json` | `WP8B-CS-010` | Bridge-required. |
| `common_state/wp8b_cs_011_reference_only.json` | `WP8B-CS-011` | Reference-only. |
| `common_state/wp8b_cs_012_parent_computable_subslice_noncomputable.json` | `WP8B-CS-012` | Parent computable and governed sub-slice noncomputable. |
| `common_state/wp8b_cs_013_missing_source_row_fact.json` | `WP8B-CS-013` | Missing source row fact. |
| `common_state/wp8b_cs_014_missing_scorer_fact.json` | `WP8B-CS-014` | Missing scorer fact. |
| `common_state/wp8b_cs_015_conflicting_ownership_marker.json` | `WP8B-CS-015` | Conflicting ownership marker. |
| `common_state/wp8b_ni_001_alternate_denominator_rejected.json` | `WP8B-NI-001` | Detector non-inference: alternate denominator. |
| `common_state/wp8b_ni_002_historical_report_layer_rejected.json` | `WP8B-NI-002` | Detector non-inference: historical report-layer value. |
| `common_state/wp8b_ni_003_prompt_or_generated_text_classification_rejected.json` | `WP8B-NI-003` | Detector non-inference: prompt or generated-text classification. |

Recommended first fixture file for authoring:

- `manifests/reports/stage_b_wp8_validation/fixtures/common_state/wp8b_cs_001_complete_state.json`

Rationale:

- It is the lowest-risk executable fixture.
- It establishes the basic complete/current-run-computable/comparison-blocked baseline.
- Every later partial, missing, and non-inference fixture can be reviewed against it.

### Family A Fixture File Set

Initial Family A fixture files:

| Planned File | Scenario ID | Primary Coverage |
|---|---|---|
| `family_a/a_c_001_exact_valid_control.json` | `A-C-001` | Exact-valid tool-expected control. |
| `family_a/a_c_002_direct_answer_substitution.json` | `A-C-002` | Direct-answer governed subtype. |
| `family_a/a_c_003_scalar_substitution.json` | `A-C-003` | Scalar substitution sibling subtype. |
| `family_a/a_c_004_malformed_output.json` | `A-C-004` | Malformed output sibling subtype. |
| `family_a/a_c_005_wrapper_envelope_drift.json` | `A-C-005` | Wrapper/envelope drift sibling subtype. |
| `family_a/a_c_006_missing_tool_call.json` | `A-C-006` | Missing tool call sibling subtype. |
| `family_a/a_c_007_wrong_tool_name.json` | `A-C-007` | Wrong tool name sibling subtype. |
| `family_a/a_c_008_wrong_argument.json` | `A-C-008` | Wrong argument sibling subtype. |
| `family_a/a_c_009_excluded_row_control.json` | `A-C-009` | Exclusion handling. |
| `family_a/a_c_010_split_scoped_subtypes.json` | `A-C-010` | Split-scoped subtype summaries. |
| `family_a/a_p_001_missing_subtype_summary.json` | `A-P-001` | Partial aggregate with missing subtype summary. |
| `family_a/a_p_002_direct_answer_count_without_denominator.json` | `A-P-002` | Count-only direct-answer evidence. |
| `family_a/a_p_003_direct_answer_missing_taxonomy_marker.json` | `A-P-003` | Missing taxonomy marker. |
| `family_a/a_p_004_missing_split_summary.json` | `A-P-004` | Missing split-scoped subtype summary. |
| `family_a/a_p_005_missing_eligible_denominator.json` | `A-P-005` | Missing eligible tool-expected denominator. |
| `family_a/a_m_001_missing_family_a.json` | `A-M-001` | Missing active Family A aggregate. |
| `family_a/a_m_002_missing_direct_answer_subtype.json` | `A-M-002` | Missing governed direct-answer subtype. |
| `family_a/a_m_003_missing_failure_taxonomy.json` | `A-M-003` | Missing failure taxonomy. |
| `family_a/a_m_004_missing_primary_scorer_outcome.json` | `A-M-004` | Missing scorer primary outcome. |
| `family_a/a_m_005_missing_exact_valid_fact.json` | `A-M-005` | Missing exact-valid fact. |
| `family_a/a_m_006_missing_non_exact_subtype.json` | `A-M-006` | Missing approved subtype for non-exact row. |
| `family_a/a_ni_001_prose_without_subtype_rejected.json` | `A-NI-001` | Detector must not infer direct-answer from prose-like output. |
| `family_a/a_ni_002_scalar_without_subtype_rejected.json` | `A-NI-002` | Detector must not infer scalar or direct-answer from output shape. |
| `family_a/a_ni_003_historical_direct_answer_rejected.json` | `A-NI-003` | Historical direct-answer count remains bridge-required without current facts. |
| `family_a/a_ni_004_no_call_proxy_rejected.json` | `A-NI-004` | No-call correctness must not substitute for direct-answer subtype. |

### Fixture Index Files

Fixture authoring should include lightweight index files after the first common-state and Family A fixture batches are authored:

| Planned File | Purpose |
|---|---|
| `common_state/index.json` | List common-state fixture IDs, planned files, source definitions, and expected state categories. |
| `family_a/index.json` | List Family A scenario IDs, planned files, intended subtypes, and expected state categories. |
| `README.md` | State fixture root scope, non-runtime boundary, and validator-not-implemented status. |

The index files are fixture artifacts, not manifests for runtime behavior.

## 3. Fixture Authoring Sequence

### Phase 1A: Common-State Baseline

Authoring order:

1. `wp8b_cs_001_complete_state.json`
2. `wp8b_cs_007_computable_comparison_blocked.json`
3. `wp8b_cs_005_denominator_missing.json`
4. `wp8b_cs_006_marker_missing.json`
5. `wp8b_cs_002_partial_state.json`
6. `wp8b_cs_003_missing_family.json`
7. `wp8b_cs_004_missing_governed_subslice.json`
8. `wp8b_cs_008_noncomputable_comparison_blocked.json`
9. `wp8b_cs_009_comparison_allowed.json`
10. `wp8b_cs_010_bridge_required.json`
11. `wp8b_cs_011_reference_only.json`
12. `wp8b_cs_012_parent_computable_subslice_noncomputable.json`
13. `wp8b_cs_013_missing_source_row_fact.json`
14. `wp8b_cs_014_missing_scorer_fact.json`
15. `wp8b_cs_015_conflicting_ownership_marker.json`
16. `wp8b_ni_001_alternate_denominator_rejected.json`
17. `wp8b_ni_002_historical_report_layer_rejected.json`
18. `wp8b_ni_003_prompt_or_generated_text_classification_rejected.json`

Review checkpoint:

- Confirm every common-state fixture maps to its WP8-B definition.
- Confirm each fixture distinguishes completeness, current-run computability, and comparability.
- Confirm non-inference fixtures reject detector reconstruction.

### Phase 1B: Family A Complete-Emission Fixtures

Authoring order:

1. `a_c_001_exact_valid_control.json`
2. `a_c_002_direct_answer_substitution.json`
3. `a_c_003_scalar_substitution.json`
4. `a_c_004_malformed_output.json`
5. `a_c_005_wrapper_envelope_drift.json`
6. `a_c_006_missing_tool_call.json`
7. `a_c_007_wrong_tool_name.json`
8. `a_c_008_wrong_argument.json`
9. `a_c_009_excluded_row_control.json`
10. `a_c_010_split_scoped_subtypes.json`

Review checkpoint:

- Confirm every approved Family A subtype has positive fixture coverage.
- Confirm direct-answer substitution is a governed subtype and scalar substitution is a sibling subtype.
- Confirm exact-valid rows exit subtype assignment.
- Confirm excluded rows do not enter governed denominators.

### Phase 1C: Family A Partial And Missing Fixtures

Authoring order:

1. `a_p_001_missing_subtype_summary.json`
2. `a_p_002_direct_answer_count_without_denominator.json`
3. `a_p_003_direct_answer_missing_taxonomy_marker.json`
4. `a_p_004_missing_split_summary.json`
5. `a_p_005_missing_eligible_denominator.json`
6. `a_m_001_missing_family_a.json`
7. `a_m_002_missing_direct_answer_subtype.json`
8. `a_m_003_missing_failure_taxonomy.json`
9. `a_m_004_missing_primary_scorer_outcome.json`
10. `a_m_005_missing_exact_valid_fact.json`
11. `a_m_006_missing_non_exact_subtype.json`

Review checkpoint:

- Confirm missing facts produce noncomputability rather than zero values.
- Confirm missing subtype does not create an `other` subtype.
- Confirm missing denominator blocks rates even when counts exist.
- Confirm missing taxonomy marker blocks governed Family A interpretation.

### Phase 1D: Family A Detector Non-Inference Fixtures

Authoring order:

1. `a_ni_001_prose_without_subtype_rejected.json`
2. `a_ni_002_scalar_without_subtype_rejected.json`
3. `a_ni_003_historical_direct_answer_rejected.json`
4. `a_ni_004_no_call_proxy_rejected.json`

Review checkpoint:

- Confirm generated text does not become detector-owned subtype evidence.
- Confirm no-call correctness does not substitute for direct-answer subtype.
- Confirm historical direct-answer count does not become a current-run fact.
- Confirm comparison remains blocked or bridge-required as defined by the source scenario.

### Phase 1E: Fixture Index And Package Review

Authoring order:

1. `common_state/index.json`
2. `family_a/index.json`
3. `README.md`

Review checkpoint:

- Confirm every Phase 1 fixture is indexed.
- Confirm source planning documents are referenced.
- Confirm runtime non-implementation boundary is visible.
- Confirm unresolved Family B1 and Family B2 blockers are explicitly out of scope.

## 4. Acceptance Criteria

WP8 Phase 1 execution is complete when:

- Common-state fixture files exist for all 18 WP8-B fixture definitions.
- Family A fixture files exist for all 25 Family A scenarios from WP8-A.
- Each fixture identifies its source scenario or source definition.
- Each fixture identifies expected completeness state.
- Each fixture identifies expected current-run computability state.
- Each fixture identifies expected comparability state.
- Each fixture identifies expected detector treatment.
- Each fixture identifies expected reconciliation behavior.
- Each fixture identifies whether it is required, optional diagnostic, or future reserved.
- Family A fixtures identify intended subtype or no-subtype control status.
- Missing-evidence fixtures identify the missing evidence class and expected noncomputability behavior.
- Detector non-inference fixtures explicitly state the prohibited detector behavior.
- Index files reconcile fixture count to source scenario count.
- No fixture uses a proxy, alias, inferred metric, reconstructed metric, parent aggregate substitute, or historical report-layer substitute as governed evidence.
- No validator, schema, runtime, scorer, evaluator, detector, threshold, governance, mapping, or manifest behavior is modified.

Expected Phase 1 fixture count:

| Fixture Group | Expected Count |
|---|---:|
| Common-state fixtures | 18 |
| Family A fixtures | 25 |
| Index or README files | 3 |
| Total planned files | 46 |

## 5. Review Requirements

### Required Reviewers

Validation owner:

- Approves fixture shape, scenario coverage, and acceptance criteria.

Governance owner:

- Confirms fixtures preserve no-proxy, no-inference, no-detector-reconstruction, and no-governance-relaxation doctrine.

Scorer owner:

- Reviews Family A subtype fixture expectations and missing-evidence behavior.

Detector owner:

- Reviews detector non-inference fixtures and expected blocked behavior.

Evaluator owner:

- Reviews reconciliation expectations and denominator/rate behavior.

Schema owner:

- Reviews that fixture shape does not prematurely lock schema implementation details.

### Review Checkpoints

Checkpoint 1:

- After `wp8b_cs_001_complete_state.json`.
- Purpose: approve minimal fixture shape before authoring the full set.

Checkpoint 2:

- After all common-state fixtures.
- Purpose: confirm state model coverage and non-inference negatives.

Checkpoint 3:

- After Family A complete-emission fixtures.
- Purpose: confirm positive subtype coverage and exact-valid/exclusion controls.

Checkpoint 4:

- After Family A partial and missing fixtures.
- Purpose: confirm missing-evidence noncomputability and marker/denominator behavior.

Checkpoint 5:

- After Family A detector non-inference fixtures and indexes.
- Purpose: approve Phase 1 as complete and ready for later validator planning.

## 6. Rollback Boundaries

Independent rollback units:

- Individual common-state fixture files.
- Individual Family A fixture files.
- Common-state fixture batch.
- Family A complete-emission batch.
- Family A partial and missing batch.
- Family A detector non-inference batch.
- Fixture index files.

Rollback rules:

- If the first fixture shape is rejected, roll back only `wp8b_cs_001_complete_state.json` and revise the fixture-shape decision before authoring more files.
- If common-state semantics are rejected, roll back the common-state batch before Family A fixture authoring proceeds.
- If Family A subtype expectations are rejected, roll back Family A fixture files without changing common-state fixtures.
- If an index file is wrong, roll back the index file without changing fixture content.
- If a fixture accidentally encodes a schema implementation decision, roll back or revise that fixture before validator work begins.
- If a fixture implies detector reconstruction, remove or revise the fixture before it becomes an acceptance target.

Runtime rollback is not required for WP8 Phase 1 because no runtime behavior is changed.

## 7. Separation From Runtime Implementation

WP8 Phase 1 fixture files are acceptance artifacts only.

They must not:

- Add or modify validators.
- Add or modify schemas.
- Add or modify scorer logic.
- Add or modify evaluator aggregation.
- Add or modify detector logic.
- Add or modify thresholds.
- Add or modify governance rules.
- Add or modify runtime mappings.
- Change manifest interpretation.

They may:

- Encode source scenario ID or fixture definition ID.
- Encode expected completeness, computability, and comparability states.
- Encode expected detector treatment in prose or structured fixture metadata.
- Encode expected reconciliation behavior in fixture metadata.
- Encode missing-evidence and non-inference expectations.
- Reference source planning documents.

They must keep current-run computability and baseline comparability separate.

## Remaining Blockers Before Family B1 And Family B2 Fixture Execution

Family B1 blockers:

- Symbol-name sub-slice declaration rule approval.
- Symbol-name membership ownership approval.
- Parent read-file context rule approval.
- Small-denominator visibility acceptance.
- Validation-owner approval of B1 fixture scope.

Family B2 blockers:

- Anchor taxonomy approval.
- Anchor assignment ownership approval.
- No-anchor membership declaration rule approval.
- Conflicting ownership handling approval.
- Validation-owner approval of B2 fixture scope.

Shared B1/B2 blockers:

- Confirmation that fixture shape established by Phase 1 is accepted.
- Confirmation that family-specific fixtures do not require schema implementation first.
- Confirmation that detector non-inference negatives are sufficient for prompt-text and parent-aggregate rejection.

## Confidence Level

Confidence level: High.

Rationale:

- WP8 has already been classified as the first executable packet.
- Common-state fixture definitions and Family A scenarios are complete.
- Family A subtype mapping and scorer evidence planning are complete enough for fixture authoring.
- The first execution slice avoids unresolved Family B1 and Family B2 ownership decisions.
- The plan preserves the no-runtime, no-validator, no-schema, and no-governance-change boundaries.
