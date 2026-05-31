# Stage B WP8 X2A Fixture Index

## Scope

This document indexes the completed cross-family execution Slice 2A for the first half of comparability scenarios.

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

## Cross-Family Slice 2A Fixture Index

| Fixture ID | Filename | Category | Governed Concept | Intended State | Expected State |
|---|---|---|---|---|---|
| `X-CMP-001` | `x_cmp_001_comparison_allowed_approved_migration_scope.json` | Comparability | Baseline comparison | Current-run facts computable; migration approved at same concept level | `complete` / `current-run computable` / `comparison-allowed` |
| `X-CMP-002` | `x_cmp_002_bridge_required_related_historical_concept.json` | Comparability | Baseline comparison | Current-run facts computable; related historical concept; bridge not approved | `complete` / `current-run computable` / `bridge-required` |
| `X-CMP-003` | `x_cmp_003_reference_only_historical_value.json` | Comparability | Baseline comparison | Current-run facts computable; historical value retained for reference only | `complete` / `current-run computable` / `reference-only` |
| `X-CMP-004` | `x_cmp_004_missing_migration_status_comparison_blocked.json` | Comparability | Baseline comparison | Current-run facts computable; migration status missing | `complete` / `current-run computable` / `comparison-blocked` |
| `X-CMP-005` | `x_cmp_005_noncomputable_current_run_with_baseline_present.json` | Comparability | Baseline comparison | Current-run facts noncomputable; baseline present | `missing` / `current-run noncomputable` / `comparison-blocked` |

## Index Review Notes

- All approved Slice 2A scenario IDs are represented by one fixture file each.
- All fixtures are classified as `Required`.
- Comparability-state distinctions remain explicit and separate: `comparison-allowed`, `bridge-required`, `reference-only`, and `comparison-blocked`.
- Current-run computability and comparability remain separate state axes.
- `X-CMP-006` through `X-CMP-010`, `X-NI`, and `X-REC` scenarios remain out of this execution slice.
