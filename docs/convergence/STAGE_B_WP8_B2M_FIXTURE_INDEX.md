# Stage B WP8 B2-M Fixture Index

## Scope

This document indexes the completed Family B2 missing-emission fixture slice for WP8.

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
- `STAGE_B_WP8_B2P_FIXTURE_INDEX.md`

## Index Totals

| Category | Fixture Count |
|---|---:|
| Complete emission | 0 |
| Partial emission | 0 |
| Missing emission | 6 |
| Detector non-inference | 0 |
| Total indexed Family B2 fixtures in this slice | 6 |

## Family B2 Missing-Emission Fixture Index

| Fixture ID | Filename | Category | Governed Concept | Intended Sub-slice Or State | Expected State |
|---|---|---|---|---|---|
| `B2-M-001` | `b2_m_001_missing_anchor_family.json` | Missing emission | Anchor-generalization aggregate | Anchor family missing while registered active | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `B2-M-002` | `b2_m_002_missing_anchor_taxonomy.json` | Missing emission | Anchor taxonomy | Anchor taxonomy marker missing | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `B2-M-003` | `b2_m_003_missing_anchor_assignment_ownership.json` | Missing emission | Anchor assignment ownership | Anchor assignment ownership marker missing | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `B2-M-004` | `b2_m_004_missing_anchor_category_for_eligible_row.json` | Missing emission | Anchor category | Anchor category missing for eligible row | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `B2-M-005` | `b2_m_005_missing_no_anchor_subslice.json` | Missing emission | No-anchor governed sub-slice | No-anchor sub-slice missing | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `B2-M-006` | `b2_m_006_missing_exact_valid_scorer_fact_anchor_eligible_row.json` | Missing emission | Exact-valid fact | Exact-valid scorer fact missing for anchor-eligible row | `missing` / `current-run noncomputable` / `comparison-blocked` |

## Index Review Notes

- All `B2-M-001` through `B2-M-006` scenario IDs are represented by one fixture file each.
- All fixtures in this slice are classified as `Required`.
- Missing-state fixtures preserve missing and noncomputable status; none repair or infer absent facts.
- Detector non-inference boundaries remain explicit: no prompt/generated-text category inference, no ownership inference, no denominator substitution, and no scorer-fact defaulting.
- Complete-emission (`B2-C`) and partial-emission (`B2-P`) fixtures are unchanged and remain referenced as prior-slice baseline.
- Detector non-inference B2 scenarios remain out of this execution slice.
