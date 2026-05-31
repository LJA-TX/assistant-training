# Stage B WP8 B2-P Fixture Index

## Scope

This document indexes the completed Family B2 partial-emission fixture slice for WP8.

This is documentation-only and does not implement validators, schemas, runtime behavior, detectors, scorers, evaluators, thresholds, governance rules, mappings, or manifests.

Reference inputs:

- `STAGE_B_WP8_EXECUTION_PLAN.md`
- `STAGE_B_WP8A_SCENARIO_CATALOG.md`
- `STAGE_B_VALIDATION_FIXTURE_MATRIX_PLAN.md`
- `STAGE_B_B2_ANCHOR_TAXONOMY_REVIEW.md`
- `STAGE_B_B2_ANCHOR_OWNERSHIP_REVIEW.md`
- `STAGE_B_B2_NO_ANCHOR_MEMBERSHIP_REVIEW.md`
- `STAGE_B_B2_CONFLICTING_OWNERSHIP_REVIEW.md`
- `STAGE_B_B2_READINESS_CLOSURE_ASSESSMENT.md`
- `STAGE_B_WP8_B2C_FIXTURE_INDEX.md`

## Index Totals

| Category | Fixture Count |
|---|---:|
| Complete emission | 0 |
| Partial emission | 5 |
| Missing emission | 0 |
| Detector non-inference | 0 |
| Total indexed Family B2 fixtures in this slice | 5 |

## Family B2 Partial-Emission Fixture Index

| Fixture ID | Filename | Category | Governed Concept | Intended Sub-slice Or State | Expected State |
|---|---|---|---|---|---|
| `B2-P-001` | `b2_p_001_missing_no_anchor_subslice.json` | Partial emission | No-anchor governed sub-slice | Anchor family aggregate emitted but no-anchor sub-slice absent | `partial` / `current-run noncomputable` / `comparison-blocked` |
| `B2-P-002` | `b2_p_002_no_anchor_count_without_denominator.json` | Partial emission | No-anchor governed sub-slice | No-anchor count emitted without denominator | `partial` / `current-run noncomputable` / `comparison-blocked` |
| `B2-P-003` | `b2_p_003_anchor_categories_without_assignment_ownership.json` | Partial emission | Anchor-generalization aggregate | Anchor categories emitted without assignment ownership marker | `partial` / `current-run noncomputable` / `comparison-blocked` |
| `B2-P-004` | `b2_p_004_incomplete_anchor_category_distribution.json` | Partial emission | Anchor-category distribution | Taxonomy marker emitted with incomplete category distribution | `partial` / `current-run noncomputable` / `comparison-blocked` |
| `B2-P-005` | `b2_p_005_missing_split_scoped_no_anchor_summary.json` | Partial emission | Split-scoped no-anchor summary | Aggregate no-anchor summary emitted but active split-scoped no-anchor summary missing | `partial` / `current-run noncomputable` / `comparison-blocked` |

## Index Review Notes

- All `B2-P-001` through `B2-P-005` scenario IDs are represented by one fixture file each.
- All fixtures in this slice are classified as `Required`.
- All fixtures preserve noncomputability for missing no-anchor sub-slice, missing denominator, missing ownership marker, incomplete category distribution, or missing split-scoped no-anchor summary.
- Detector non-inference boundaries remain explicit: no prompt/generated-text classification, no denominator borrowing, no ownership inference, and no synthesized split summaries.
- Complete-emission `B2-C` fixtures are unchanged and remain referenced as prior-slice baseline.
- Missing-emission and detector non-inference B2 scenarios remain out of this execution slice.
