# Stage B WP8 X2B Fixture Index

## Scope

This document indexes the completed cross-family execution Slice 2B for the remaining comparability scenarios.

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
| Comparability (`X-CMP`) | 5 |
| Complete emission | 0 |
| Partial emission | 0 |
| Missing emission | 0 |
| Noncomputability state (`X-NC`) | 0 |
| Detector non-inference (`X-NI`) | 0 |
| Reconciliation (`X-REC`) | 0 |
| Total indexed cross-family fixtures in this slice | 5 |

## Cross-Family Slice 2B Fixture Index

| Fixture ID | Filename | Category | Governed Concept | Intended State | Expected State |
|---|---|---|---|---|---|
| `X-CMP-006` | `x_cmp_006_family_comparison_allowed_subslice_blocked.json` | Comparability | Family/sub-slice comparison | Family comparison allowed; governed sub-slice comparison blocked | `partial` / `current-run computable` / `comparison-blocked` |
| `X-CMP-007` | `x_cmp_007_historical_denominator_missing_reference_only.json` | Comparability | Historical denominator | Historical baseline present; historical denominator missing | `complete` / `current-run computable` / `reference-only` |
| `X-CMP-008` | `x_cmp_008_historical_taxonomy_change_bridge_required.json` | Comparability | Historical taxonomy | Historical baseline present; taxonomy changed without approved bridge | `complete` / `current-run computable` / `bridge-required` |
| `X-CMP-009` | `x_cmp_009_historical_subpopulation_change_bridge_required.json` | Comparability | Historical subpopulation | Historical baseline present; subpopulation definition changed | `complete` / `current-run computable` / `bridge-required` |
| `X-CMP-010` | `x_cmp_010_historical_report_layer_provenance_reference_only.json` | Comparability | Historical provenance | Historical baseline is report-layer only | `complete` / `current-run computable` / `reference-only` |

## Index Review Notes

- All approved Slice 2B scenario IDs are represented by one fixture file each.
- All fixtures are classified as `Required`.
- Comparability-state distinctions remain explicit and separate: `comparison-allowed`, `bridge-required`, `reference-only`, and `comparison-blocked`.
- `X-CMP-006` preserves family-versus-sub-slice comparison scope separation.
- `X-NI` and `X-REC` scenarios remain out of this execution slice.
