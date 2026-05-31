# Stage B WP8 X3 Fixture Index

## Scope

This document indexes the completed cross-family execution Slice 3 for detector non-inference scenarios.

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
| Detector non-inference (`X-NI`) | 2 |
| Complete emission | 0 |
| Partial emission | 0 |
| Missing emission | 0 |
| Noncomputability state (`X-NC`) | 0 |
| Comparability (`X-CMP`) | 0 |
| Reconciliation (`X-REC`) | 0 |
| Total indexed cross-family fixtures in this slice | 2 |

## Cross-Family Slice 3 Fixture Index

| Fixture ID | Filename | Category | Governed Concept | Intended State | Expected State |
|---|---|---|---|---|---|
| `X-NI-001` | `x_ni_001_historical_report_layer_without_migration_status.json` | Detector non-inference | Historical comparison | Historical report-layer value exists without migration status | `complete` / `current-run computable` / `comparison-blocked` |
| `X-NI-002` | `x_ni_002_required_denominator_missing_alternate_exists.json` | Detector non-inference | Denominator construction | Required denominator missing while another population denominator exists | `partial` / `current-run noncomputable` / `comparison-blocked` |

## Index Review Notes

- All approved Slice 3 scenario IDs are represented by one fixture file each.
- All fixtures are classified as `Required`.
- Detector non-inference constraints are explicit for prompt text, historical artifacts, report naming, path conventions, and marker absence.
- No alternate denominator substitution is permitted for governed rates.
- `X-REC` scenarios remain out of this execution slice.
