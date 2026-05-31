# Stage B WP8 X4 Fixture Index

## Scope

This document indexes the completed cross-family execution Slice 4 for reconciliation scenarios.

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
| Reconciliation (`X-REC`) | 10 |
| Complete emission | 0 |
| Partial emission | 0 |
| Missing emission | 0 |
| Noncomputability state (`X-NC`) | 0 |
| Comparability (`X-CMP`) | 0 |
| Detector non-inference (`X-NI`) | 0 |
| Total indexed cross-family fixtures in this slice | 10 |

## Cross-Family Slice 4 Fixture Index

| Fixture ID | Filename | Category | Governed Concept | Intended State | Expected State |
|---|---|---|---|---|---|
| `X-REC-001` | `x_rec_001_numerator_partition_equals_eligible_denominator.json` | Reconciliation | Aggregate reconciliation | Numerator and non-numerator partitions emitted for eligible denominator | `complete` / `current-run computable` / `comparison-blocked` |
| `X-REC-002` | `x_rec_002_subslice_denominator_bounded_by_parent.json` | Reconciliation | Sub-slice reconciliation | Governed sub-slice denominator emitted with parent denominator | `complete` / `current-run computable` / `comparison-blocked` |
| `X-REC-003` | `x_rec_003_exclusion_summary_reconciles_source_coverage.json` | Reconciliation | Exclusion reconciliation | Excluded rows emitted with exclusion summary | `complete` / `current-run computable` / `comparison-blocked` |
| `X-REC-004` | `x_rec_004_split_scoped_totals_reconcile_aggregate.json` | Reconciliation | Split reconciliation | Split-scoped summaries emitted for active split scope | `complete` / `current-run computable` / `comparison-blocked` |
| `X-REC-005` | `x_rec_005_row_fact_coverage_reconciles_governed_denominator.json` | Reconciliation | Coverage reconciliation | Row-fact coverage summary emitted for governed population | `complete` / `current-run computable` / `comparison-blocked` |
| `X-REC-006` | `x_rec_006_family_a_subtype_counts_reconcile_non_exact_denominator.json` | Reconciliation | Family A failure-subtype reconciliation | Family A subtype counts emitted for non-exact eligible denominator | `complete` / `current-run computable` / `comparison-blocked` |
| `X-REC-007` | `x_rec_007_family_b1_symbol_name_denominator_reconciles_parent_context.json` | Reconciliation | Family B1 symbol-name reconciliation | Symbol-name denominator and parent read-file denominator emitted | `complete` / `current-run computable` / `comparison-blocked` |
| `X-REC-008` | `x_rec_008_family_b2_anchor_category_counts_reconcile_family_denominator.json` | Reconciliation | Family B2 anchor-category reconciliation | Anchor category counts emitted for active taxonomy | `complete` / `current-run computable` / `comparison-blocked` |
| `X-REC-009` | `x_rec_009_count_denominator_rate_precision_reconciliation.json` | Reconciliation | Rate reconciliation | Count, denominator, and rate emitted for governed concept | `complete` / `current-run computable` / `comparison-blocked` |
| `X-REC-010` | `x_rec_010_small_denominator_visibility_preserved.json` | Reconciliation | Small-denominator visibility | Governed sub-slice has small denominator with visible count and denominator | `complete` / `current-run computable` / `comparison-blocked` |

## Index Review Notes

- All approved Slice 4 scenario IDs are represented by one fixture file each.
- All fixtures are classified as `Required`.
- Denominator substitution, historical reconstruction, migration-status inference, alternate-source replacement, and report-layer inference are explicitly disallowed.
- `X-REC-006` through `X-REC-008` preserve family-specific reconciliation doctrine in cross-family context.
