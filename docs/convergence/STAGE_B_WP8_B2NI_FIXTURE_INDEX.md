# Stage B WP8 B2-NI Fixture Index

## Scope

This document indexes the completed Family B2 detector non-inference fixture slice for WP8.

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
- `STAGE_B_WP8_B2M_FIXTURE_INDEX.md`

## Index Totals

| Category | Fixture Count |
|---|---:|
| Complete emission | 0 |
| Partial emission | 0 |
| Missing emission | 0 |
| Detector non-inference | 4 |
| Total indexed Family B2 fixtures in this slice | 4 |

## Family B2 Detector Non-Inference Fixture Index

| Fixture ID | Filename | Category | Governed Concept | Intended Sub-slice Or State | Expected State |
|---|---|---|---|---|---|
| `B2-NI-001` | `b2_ni_001_prompt_without_no_anchor_marker_rejected.json` | Detector non-inference | No-anchor governed sub-slice | Prompt text lacks obvious anchor phrase; no-anchor marker missing | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `B2-NI-002` | `b2_ni_002_historical_no_anchor_share_denominator_incompatible.json` | Detector non-inference | No-anchor governed sub-slice | Historical denominator-incompatible no-anchor share exists; current denominator-based rate absent | `missing` / `current-run noncomputable` / `bridge-required` |
| `B2-NI-003` | `b2_ni_003_anchor_family_aggregate_substitution_rejected.json` | Detector non-inference | No-anchor governed sub-slice | Family aggregate exact-valid rate exists; no-anchor sub-slice absent | `missing` / `current-run noncomputable` / `comparison-blocked` |
| `B2-NI-004` | `b2_ni_004_taxonomy_change_without_migration_status_blocked.json` | Detector non-inference | No-anchor governed sub-slice | Taxonomy changed without approved migration status | `complete` / `current-run computable` / `comparison-blocked` |

## Index Review Notes

- All `B2-NI-001` through `B2-NI-004` scenario IDs are represented by one fixture file each.
- All fixtures in this slice are classified as `Required`.
- Prompt/no-anchor inference, ownership inference, denominator substitution, and family-aggregate substitution are explicitly rejected.
- Historical denominator-incompatible share substitution is explicitly rejected and bridge-required.
- Taxonomy-change scenario preserves current-run computability while blocking historical comparison without migration status.
