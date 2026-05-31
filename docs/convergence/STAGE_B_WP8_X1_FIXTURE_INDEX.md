# Stage B WP8 X1 Fixture Index

## Scope

This document indexes the completed first cross-family execution slice for WP8.

This is documentation-only and does not implement validators, schemas, runtime behavior, detectors, scorers, evaluators, thresholds, governance rules, mappings, or manifests.

Reference inputs:

- `STAGE_B_WP8A_SCENARIO_CATALOG.md`
- `STAGE_B_VALIDATION_FIXTURE_MATRIX_PLAN.md`
- `STAGE_B_WP8_CROSS_FAMILY_EXECUTION_PLAN_REVIEW.md`
- `STAGE_B_WP8_CROSS_FAMILY_READINESS_CONFIRMATION.md`
- `STAGE_B_WP8_B2_EXIT_REVIEW.md`
- `STAGE_B_B1_NI_SCENARIO_RECONCILIATION_REVIEW.md`
- `STAGE_B_B2_READINESS_CLOSURE_ASSESSMENT.md`

## Index Totals

| Category | Fixture Count |
|---|---:|
| Complete emission | 1 |
| Partial emission | 1 |
| Missing emission | 1 |
| Noncomputability state | 2 |
| Comparability (`X-CMP`) | 0 |
| Detector non-inference (`X-NI`) | 0 |
| Reconciliation (`X-REC`) | 0 |
| Total indexed cross-family fixtures in this slice | 5 |

## Cross-Family Slice 1 Fixture Index

| Fixture ID | Filename | Category | Governed Concept | Intended State | Expected State |
|---|---|---|---|---|---|
| `X-C-001` | `x_c_001_complete_all_active_families.json` | Complete emission | All active families and governed sub-slices | Family A, B1, and B2 complete emissions present together | `complete` / `current-run computable` / `comparison-blocked` |
| `X-P-001` | `x_p_001_mixed_complete_partial_missing_families.json` | Partial emission | Active family package | One family complete, one family partial, one family missing | `partial` / `current-run noncomputable` / `comparison-blocked` |
| `X-M-001` | `x_m_001_missing_shared_source_row_fact.json` | Missing emission | Source fact dependency | Shared required row-level source fact missing for an active concept | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `X-NC-001` | `x_nc_001_count_without_governed_denominator.json` | Noncomputability state | Count-only governed evidence | Count emitted without required denominator for a governed rate | `partial` / `current-run noncomputable` / `comparison-blocked` |
| `X-NC-002` | `x_nc_002_parent_computable_subslice_noncomputable.json` | Noncomputability state | Parent and governed sub-slice relationship | Parent family computable and governed sub-slice noncomputable | `partial` / `current-run noncomputable` / `comparison-blocked` |

## Index Review Notes

- All approved Slice 1 scenario IDs are represented by one fixture file each.
- All fixtures are classified as `Required`.
- All fixtures preserve detector consumption-only behavior and reject substitution, reconstruction, and inference.
- Parent and governed sub-slice state divergence remains explicit and unresolved unless required governed facts are emitted.
- Comparability (`X-CMP`), detector non-inference (`X-NI`), and reconciliation (`X-REC`) scenarios remain out of this execution slice.
