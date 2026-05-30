# Stage B WP8 B2-C Fixture Index

## Scope

This document indexes the completed Family B2 complete-emission fixture slice for WP8.

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

## Index Totals

| Category | Fixture Count |
|---|---:|
| Complete emission | 8 |
| Partial emission | 0 |
| Missing emission | 0 |
| Detector non-inference | 0 |
| Total indexed Family B2 fixtures in this slice | 8 |

## Family B2 Complete-Emission Fixture Index

| Fixture ID | Filename | Category | Governed Concept | Intended Sub-slice Or State | Expected State |
|---|---|---|---|---|---|
| `B2-C-001` | `b2_c_001_exact_valid_no_anchor_row.json` | Complete emission | No-anchor governed sub-slice | Exact-valid no-anchor row | `complete` / `current-run computable` / `comparison-blocked` |
| `B2-C-002` | `b2_c_002_non_exact_no_anchor_row.json` | Complete emission | No-anchor governed sub-slice | Non-exact no-anchor row | `complete` / `current-run computable` / `comparison-blocked` |
| `B2-C-003` | `b2_c_003_exact_valid_sibling_anchor_row.json` | Complete emission | Sibling anchor category | Exact-valid row in another approved anchor category | `complete` / `current-run computable` / `comparison-blocked` |
| `B2-C-004` | `b2_c_004_non_exact_sibling_anchor_row.json` | Complete emission | Sibling anchor category | Non-exact row in another approved anchor category | `complete` / `current-run computable` / `comparison-blocked` |
| `B2-C-005` | `b2_c_005_outside_anchor_population_row.json` | Complete emission | Anchor-generalization aggregate | Row outside anchor-generalization population | `complete` / `current-run computable` / `comparison-blocked` |
| `B2-C-006` | `b2_c_006_excluded_anchor_eligible_row.json` | Complete emission | Exclusion handling | Excluded anchor-eligible row | `complete` / `current-run computable` / `comparison-blocked` |
| `B2-C-007` | `b2_c_007_multi_category_anchor_distribution.json` | Complete emission | Anchor-category distribution | Multiple approved anchor categories with full markers | `complete` / `current-run computable` / `comparison-blocked` |
| `B2-C-008` | `b2_c_008_split_scoped_anchor_summaries.json` | Complete emission | Split-scoped anchor summaries | Complete split-scoped anchor summaries | `complete` / `current-run computable` / `comparison-blocked` |

## Index Review Notes

- All `B2-C-001` through `B2-C-008` scenario IDs are represented by one fixture file each.
- All fixtures in this slice are classified as `Required`.
- All fixtures preserve detector consumption-only behavior and reject prompt/generated-text inference for anchor classification.
- Ownership and taxonomy marker expectations are explicit in each fixture.
- Conflicting ownership markers are disallowed for complete-emission fixtures and are not auto-resolved by detector.
- Partial, missing, and detector non-inference B2 scenarios remain out of this execution slice.
