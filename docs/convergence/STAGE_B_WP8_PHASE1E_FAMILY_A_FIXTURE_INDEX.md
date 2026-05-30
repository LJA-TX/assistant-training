# Stage B WP8 Phase 1E Family A Fixture Index

## Scope

This document indexes the completed Family A fixture package for WP8. It is documentation-only and does not implement validators, schemas, runtime behavior, detectors, scorers, evaluators, thresholds, governance rules, mappings, or manifests.

Reference inputs:

- `STAGE_B_WP8_EXECUTION_PLAN.md`
- `STAGE_B_WP8A_SCENARIO_CATALOG.md`
- `STAGE_B_WP8C_FAMILY_A_SUBTYPE_BOUNDARY_REVIEW.md`
- `STAGE_B_WP8C_SCENARIO_TO_SUBTYPE_MAPPING.md`
- `STAGE_B_WP3_FAMILY_A_SCORER_EVIDENCE_CONTRACT.md`
- `STAGE_B_WP3_SCORER_EVIDENCE_OUTPUT_DESIGN_REVIEW.md`

## Index Totals

| Category | Fixture Count |
|---|---:|
| Complete emission | 10 |
| Partial emission | 5 |
| Missing emission | 6 |
| Detector non-inference | 4 |
| Total Family A fixtures | 25 |

## Family A Fixture Index

| Fixture ID | Filename | Category | Intended Subtype Or State | Expected State |
|---|---|---|---|---|
| `A-C-001` | `a_c_001_exact_valid_control.json` | Complete emission | Exact-valid control; no subtype assignment | `complete` / `current-run computable` / `comparison-blocked` |
| `A-C-002` | `a_c_002_direct_answer_substitution.json` | Complete emission | `direct-answer substitution` | `complete` / `current-run computable` / `comparison-blocked` |
| `A-C-003` | `a_c_003_scalar_substitution.json` | Complete emission | `scalar substitution` | `complete` / `current-run computable` / `comparison-blocked` |
| `A-C-004` | `a_c_004_malformed_output.json` | Complete emission | `malformed output` | `complete` / `current-run computable` / `comparison-blocked` |
| `A-C-005` | `a_c_005_wrapper_envelope_drift.json` | Complete emission | `wrapper/envelope drift` | `complete` / `current-run computable` / `comparison-blocked` |
| `A-C-006` | `a_c_006_missing_tool_call.json` | Complete emission | `missing tool call` | `complete` / `current-run computable` / `comparison-blocked` |
| `A-C-007` | `a_c_007_wrong_tool_name.json` | Complete emission | `wrong tool name` | `complete` / `current-run computable` / `comparison-blocked` |
| `A-C-008` | `a_c_008_wrong_argument.json` | Complete emission | `wrong argument` | `complete` / `current-run computable` / `comparison-blocked` |
| `A-C-009` | `a_c_009_excluded_row_control.json` | Complete emission | Excluded-row control; no subtype assignment | `complete` / `current-run computable` / `comparison-blocked` |
| `A-C-010` | `a_c_010_split_scoped_subtypes.json` | Complete emission | `all approved subtypes, split-scoped` | `complete` / `current-run computable` / `comparison-blocked` |
| `A-P-001` | `a_p_001_missing_subtype_summary.json` | Partial emission | `affected approved subtype unknown or missing` | `partial` / `current-run noncomputable` / `comparison-blocked` |
| `A-P-002` | `a_p_002_direct_answer_count_without_denominator.json` | Partial emission | `direct-answer substitution` | `partial` / `current-run noncomputable` / `comparison-blocked` |
| `A-P-003` | `a_p_003_direct_answer_missing_taxonomy_marker.json` | Partial emission | `direct-answer substitution` | `partial` / `current-run noncomputable` / `comparison-blocked` |
| `A-P-004` | `a_p_004_missing_split_summary.json` | Partial emission | `direct-answer substitution, split-scoped` | `partial` / `current-run noncomputable` / `comparison-blocked` |
| `A-P-005` | `a_p_005_missing_eligible_denominator.json` | Partial emission | `all approved subtype rates` | `partial` / `current-run noncomputable` / `comparison-blocked` |
| `A-M-001` | `a_m_001_missing_family_a.json` | Missing emission | Missing active Family A aggregate | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `A-M-002` | `a_m_002_missing_direct_answer_subtype.json` | Missing emission | `direct-answer substitution` | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `A-M-003` | `a_m_003_missing_failure_taxonomy.json` | Missing emission | `all approved subtypes` | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `A-M-004` | `a_m_004_missing_primary_scorer_outcome.json` | Missing emission | `affected subtype unknown` | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `A-M-005` | `a_m_005_missing_exact_valid_fact.json` | Missing emission | `affected subtype unknown` | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `A-M-006` | `a_m_006_missing_non_exact_subtype.json` | Missing emission | `affected approved subtype missing` | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `A-NI-001` | `a_ni_001_prose_without_subtype_rejected.json` | Detector non-inference | `direct-answer substitution candidate, missing evidence` | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `A-NI-002` | `a_ni_002_scalar_without_subtype_rejected.json` | Detector non-inference | `scalar substitution candidate, missing evidence` | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `A-NI-003` | `a_ni_003_historical_direct_answer_rejected.json` | Detector non-inference | `direct-answer substitution, historical-only evidence` | `partial` / `current-run noncomputable` / `bridge-required` |
| `A-NI-004` | `a_ni_004_no_call_proxy_rejected.json` | Detector non-inference | `direct-answer substitution candidate, no-call proxy rejected` | `missing` / `current-run noncomputable` / `comparison-blocked` |

## Index Review Notes

- All Family A scenario IDs in the approved scenario catalog are represented by one fixture file.
- All fixtures are classified as `Required`.
- Complete-emission fixtures are current-run computable but comparison-blocked because baseline comparability remains separate from current-run computability.
- Partial, missing, and detector non-inference fixtures preserve noncomputability rather than substituting zero values, proxy metrics, historical facts, generated-text inspection, or inferred subtype assignments.
