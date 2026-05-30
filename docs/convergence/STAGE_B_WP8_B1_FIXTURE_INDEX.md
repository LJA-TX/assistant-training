# Stage B WP8 B1 Fixture Index

## Scope

This document indexes the completed Family B1 fixture package for WP8.
It is documentation-only and does not implement validators, schemas, runtime behavior, detectors, scorers, evaluators, thresholds, governance rules, mappings, or manifests.

Reference inputs:

- `STAGE_B_WP8_EXECUTION_PLAN.md`
- `STAGE_B_WP8A_SCENARIO_CATALOG.md`
- `STAGE_B_VALIDATION_FIXTURE_MATRIX_PLAN.md`
- `STAGE_B_B1_SYMBOL_NAME_OWNERSHIP_REVIEW.md`
- `STAGE_B_B1_PARENT_CONTEXT_AND_DENOMINATOR_REVIEW.md`
- `STAGE_B_B1_READINESS_CLOSURE_ASSESSMENT.md`
- `STAGE_B_B1_NI_SCENARIO_RECONCILIATION_REVIEW.md`

## Index Totals

| Category | Fixture Count |
|---|---:|
| Complete emission | 9 |
| Partial emission | 5 |
| Missing emission | 6 |
| Detector non-inference | 4 |
| Total Family B1 fixtures | 24 |

## Family B1 Fixture Index

| Fixture ID | Filename | Category | Governed Concept | Intended Sub-slice Or State | Expected State |
|---|---|---|---|---|---|
| `B1-C-001` | `b1_c_001_exact_valid_read_file_row.json` | Complete emission | Read-file aggregate | Exact-valid read-file row | `complete` / `current-run computable` / `comparison-blocked` |
| `B1-C-002` | `b1_c_002_non_exact_read_file_row.json` | Complete emission | Read-file aggregate | Non-exact read-file row | `complete` / `current-run computable` / `comparison-blocked` |
| `B1-C-003` | `b1_c_003_exact_valid_symbol_name_row.json` | Complete emission | Symbol-name governed sub-slice | Exact-valid read-file symbol-name row | `complete` / `current-run computable` / `comparison-blocked` |
| `B1-C-004` | `b1_c_004_non_exact_symbol_name_row.json` | Complete emission | Symbol-name governed sub-slice | Non-exact read-file symbol-name row | `complete` / `current-run computable` / `comparison-blocked` |
| `B1-C-005` | `b1_c_005_read_file_outside_symbol_name.json` | Complete emission | Read-file aggregate and symbol-name sub-slice | Read-file row explicitly outside symbol-name sub-slice | `complete` / `current-run computable` / `comparison-blocked` |
| `B1-C-006` | `b1_c_006_non_read_file_tool_row.json` | Complete emission | Read-file aggregate | Non-read-file tool row | `complete` / `current-run computable` / `comparison-blocked` |
| `B1-C-007` | `b1_c_007_excluded_read_file_row.json` | Complete emission | Exclusion handling | Excluded read-file row | `complete` / `current-run computable` / `comparison-blocked` |
| `B1-C-008` | `b1_c_008_small_denominator_symbol_name.json` | Complete emission | Symbol-name governed sub-slice | Small-denominator symbol-name set | `complete` / `current-run computable` / `comparison-blocked` |
| `B1-C-009` | `b1_c_009_split_scoped_read_file_symbol_name.json` | Complete emission | Split-scoped read-file and symbol-name summaries | Complete split-scoped read-file and symbol-name coverage | `complete` / `current-run computable` / `comparison-blocked` |
| `B1-P-001` | `b1_p_001_missing_symbol_name_subslice.json` | Partial emission | Symbol-name governed sub-slice | Read-file aggregate present but symbol-name sub-slice missing | `partial` / `current-run noncomputable` / `comparison-blocked` |
| `B1-P-002` | `b1_p_002_symbol_name_count_without_denominator.json` | Partial emission | Symbol-name governed sub-slice | Symbol-name numerator present but denominator missing | `partial` / `current-run noncomputable` / `comparison-blocked` |
| `B1-P-003` | `b1_p_003_symbol_name_without_parent_context.json` | Partial emission | Symbol-name governed sub-slice | Symbol-name summary present without parent read-file context | `partial` / `current-run noncomputable` / `comparison-blocked` |
| `B1-P-004` | `b1_p_004_read_file_missing_expected_tool_marker.json` | Partial emission | Read-file aggregate | Read-file aggregate present without expected-tool marker | `partial` / `current-run noncomputable` / `comparison-blocked` |
| `B1-P-005` | `b1_p_005_missing_split_symbol_name_summary.json` | Partial emission | Split-scoped symbol-name summary | Aggregate symbol-name summary present but active split-scoped summary missing | `partial` / `current-run noncomputable` / `comparison-blocked` |
| `B1-M-001` | `b1_m_001_missing_read_file_family.json` | Missing emission | Read-file aggregate | Read-file family missing while registered active | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `B1-M-002` | `b1_m_002_missing_read_file_eligibility_marker.json` | Missing emission | Read-file aggregate | Read-file eligibility marker missing | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `B1-M-003` | `b1_m_003_missing_expected_tool_identity.json` | Missing emission | Read-file aggregate | Expected tool identity missing for eligible row | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `B1-M-004` | `b1_m_004_missing_symbol_name_membership_marker.json` | Missing emission | Symbol-name governed sub-slice | Symbol-name membership marker missing | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `B1-M-005` | `b1_m_005_missing_exact_valid_scorer_fact.json` | Missing emission | Read-file aggregate and symbol-name sub-slice | Exact-valid scorer fact missing | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `B1-M-006` | `b1_m_006_missing_read_file_denominator.json` | Missing emission | Read-file aggregate | Read-file denominator missing | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `B1-NI-001` | `b1_ni_001_mixed_tool_aggregate_rejected.json` | Detector non-inference | Read-file aggregate | Mixed-tool aggregate must not substitute for read-file aggregate | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `B1-NI-002` | `b1_ni_002_parent_read_file_aggregate_rejected.json` | Detector non-inference | Symbol-name governed sub-slice | Parent read-file aggregate must not substitute for symbol-name sub-slice | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `B1-NI-003` | `b1_ni_003_symbol_like_prompt_rejected.json` | Detector non-inference | Symbol-name governed sub-slice | Symbol-like prompt text must not create symbol-name membership | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `B1-NI-004` | `b1_ni_004_historical_symbol_name_rate_rejected.json` | Detector non-inference | Symbol-name governed sub-slice | Historical symbol-name rate must not become current-run evidence | `partial` / `current-run noncomputable` / `bridge-required` |

## Index Review Notes

- All approved Family B1 scenario IDs in the scenario catalog are represented by one fixture file.
- All fixtures are classified as `Required`.
- Complete-emission fixtures are current-run computable but comparison-blocked because current-run computability and baseline comparability remain separate concepts.
- Partial and missing fixtures preserve noncomputability when required parent context, denominators, ownership markers, or scorer facts are absent.
- Detector non-inference fixtures follow the authoritative mapping in `STAGE_B_B1_NI_SCENARIO_RECONCILIATION_REVIEW.md`.
- No planned Family B1 fixture remains unauthored.
