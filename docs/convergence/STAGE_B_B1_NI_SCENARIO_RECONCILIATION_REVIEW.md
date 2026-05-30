# Stage B B1 NI Scenario Reconciliation Review

## Scope

This document resolves the B1 detector non-inference scenario mapping contradiction encountered before B1-NI fixture authoring.

This is documentation-only reconciliation. It does not author fixtures, implement validators, implement schemas, modify runtime behavior, modify detectors, modify scorers, modify evaluators, modify thresholds, modify governance rules, modify mappings, or modify manifests.

Reference inputs:

- `STAGE_B_WP8A_SCENARIO_CATALOG.md`
- `STAGE_B_VALIDATION_FIXTURE_MATRIX_PLAN.md`
- `STAGE_B_B1_SYMBOL_NAME_OWNERSHIP_REVIEW.md`
- `STAGE_B_B1_PARENT_CONTEXT_AND_DENOMINATOR_REVIEW.md`
- `STAGE_B_B1_READINESS_CLOSURE_ASSESSMENT.md`
- `STAGE_B_WP8_MIDPOINT_ASSESSMENT.md`

## Summary Determination

The approved scenario catalog is authoritative as-is for B1-NI fixture authoring.

No repository planning artifact requires correction. The contradiction was introduced by the later execution prompt that remapped B1-NI scenario IDs to different coverage concepts.

Additional planning is not required before B1-NI fixture authoring resumes, provided fixture authoring follows the catalog definitions documented here.

## 1. Approved B1-NI Scenario IDs From Source Catalog

| Scenario ID | Governed Concept Or Sub-Slice | Approved Input Condition | Expected Completeness | Expected Computability | Expected Comparability | Expected Detector Treatment | Expected Reconciliation |
|---|---|---|---|---|---|---|---|
| `B1-NI-001` | Read-file aggregate | Mixed-tool exact-valid aggregate exists; read-file aggregate absent. | `missing` | `current-run noncomputable` | `comparison-blocked` | Do not substitute mixed-tool aggregate. | Read-file denominator and numerator absent. |
| `B1-NI-002` | Symbol-name governed sub-slice | Read-file aggregate exists; symbol-name sub-slice absent. | `missing` | `current-run noncomputable` | `comparison-blocked` | Do not substitute parent aggregate for sub-slice. | Symbol-name reconciliation impossible. |
| `B1-NI-003` | Symbol-name governed sub-slice | Prompt contains symbol-like text; symbol-name marker missing. | `missing` | `current-run noncomputable` | `comparison-blocked` | Do not infer symbol-name from prompt text. | Symbol-name denominator blocked. |
| `B1-NI-004` | Symbol-name governed sub-slice | Historical symbol-name rate exists; current subpopulation marker missing. | `partial` | `current-run noncomputable` | `bridge-required` | Block comparison; do not use historical rate as emitted current fact. | Current subpopulation denominator blocked. |

## 2. Alternate B1-NI Interpretations Found

The conflicting execution prompt defined the requested B1-NI coverage as:

| Scenario ID | Alternate Interpretation |
|---|---|
| `B1-NI-001` | Symbol-looking content without emitted symbol-name membership must not create symbol-name membership. |
| `B1-NI-002` | Historical symbol-name counts must not become current-run symbol-name evidence. |
| `B1-NI-003` | Read-file-looking artifact without emitted eligibility markers must not become read-file eligible. |
| `B1-NI-004` | Parent aggregate presence must not reconstruct missing symbol-name membership. |

Repository planning artifacts do include related governance concepts, but not with those IDs:

- Symbol-like prompt text maps to `B1-NI-003`, not `B1-NI-001`.
- Historical symbol-name evidence maps to `B1-NI-004`, not `B1-NI-002`.
- Parent aggregate substitution maps to `B1-NI-002`, not `B1-NI-004`.
- Mixed-tool aggregate substitution maps to `B1-NI-001`.
- Read-file eligibility marker absence is already covered by `B1-M-002`, not a B1-NI scenario in the source catalog.

## 3. Mismatches

| Scenario ID | Catalog Definition | Alternate Definition | Classification |
|---|---|---|---|
| `B1-NI-001` | Mixed-tool aggregate must not substitute for read-file aggregate. | Symbol-looking content must not create symbol-name membership. | ID mismatch |
| `B1-NI-002` | Parent read-file aggregate must not substitute for symbol-name sub-slice. | Historical symbol-name counts must not become current-run evidence. | ID mismatch |
| `B1-NI-003` | Prompt contains symbol-like text; do not infer symbol-name from prompt text. | Read-file-looking artifact without eligibility markers must not become read-file eligible. | Concept mismatch |
| `B1-NI-004` | Historical symbol-name rate exists; current subpopulation marker missing; bridge required. | Parent aggregate must not reconstruct symbol-name membership. | ID mismatch |

The source catalog and fixture matrix agree with each other. The B1 readiness closure documents also agree with the source catalog:

- `B1-NI-002` is referenced as parent aggregate substitution rejection.
- `B1-NI-003` is referenced as prompt text not becoming symbol-name membership evidence.
- Historical symbol-name evidence is treated as not current-run evidence.

## 4. Authoritative Ownership

Authoritative source ownership for B1-NI fixture definitions:

| Artifact | Authority |
|---|---|
| `STAGE_B_WP8A_SCENARIO_CATALOG.md` | Primary authoritative source for scenario IDs, expected states, detector treatment, and reconciliation requirements. |
| `STAGE_B_VALIDATION_FIXTURE_MATRIX_PLAN.md` | Supporting source for scenario categories and validation expectations. |
| B1 readiness closure docs | Supporting doctrine for ownership, parent context, denominator rules, and non-inference boundaries. |
| Later execution prompt | Operational instruction only; not authoritative when it contradicts approved source definitions. |

The catalog is authoritative as-is. Later prompt wording should be treated as an execution-request mapping error, not a repository planning decision.

## 5. Correction Requirement

No repository planning artifact requires correction.

Required correction is procedural:

- B1-NI fixture authoring must use the catalog ID mapping.
- Future execution prompts should quote or preserve the approved B1-NI scenario mapping exactly.
- If additional B1-NI scenarios are desired, they should be proposed as new planning work rather than remapping approved IDs.

Additional planning is not required if the next execution prompt follows the catalog mapping.

## 6. Required Fixture Coverage

### B1-NI-001

Required fixture coverage:

- Mixed-tool exact-valid aggregate exists.
- Read-file aggregate is absent.
- Read-file denominator is absent.
- Read-file numerator is absent.
- Detector must not substitute mixed-tool aggregate for read-file aggregate.
- Expected state is `missing` / `current-run noncomputable` / `comparison-blocked`.

### B1-NI-002

Required fixture coverage:

- Parent read-file aggregate exists.
- Symbol-name governed sub-slice is absent.
- Detector must not substitute parent aggregate for symbol-name sub-slice.
- Detector must not use parent read-file count, denominator, or rate as symbol-name count, denominator, or rate.
- Expected state is `missing` / `current-run noncomputable` / `comparison-blocked`.

### B1-NI-003

Required fixture coverage:

- Prompt contains symbol-like text.
- Symbol-name marker is missing.
- Detector must not infer symbol-name membership from prompt text.
- Detector must not construct symbol-name denominator from prompt text.
- Expected state is `missing` / `current-run noncomputable` / `comparison-blocked`.

### B1-NI-004

Required fixture coverage:

- Historical symbol-name rate exists.
- Current subpopulation marker is missing.
- Detector must block comparison.
- Detector must not use historical rate as emitted current-run fact.
- Historical evidence may remain migration context only.
- Expected state is `partial` / `current-run noncomputable` / `bridge-required`.

## 7. Readiness For Fixture Authoring

B1-NI fixture authoring is ready to resume after review acceptance of this reconciliation document.

Readiness conditions:

- Use the catalog definitions from this document.
- Preserve detector-consumer-only ownership.
- Preserve no proxy, no inference, no reconstruction, and no historical substitution doctrine.
- Stop again if a future prompt remaps approved IDs or introduces new non-inference scenarios without planning approval.

Recommended next action:

- Author `B1-NI-001` through `B1-NI-004` using the catalog mapping.
- Do not create fixtures for the alternate prompt mapping unless those scenarios are first added through explicit planning.

## Reporting Summary

Contradictions found:

- The latest execution prompt remapped all four B1-NI IDs away from the approved catalog definitions.

Authoritative definitions:

- `STAGE_B_WP8A_SCENARIO_CATALOG.md` definitions for `B1-NI-001` through `B1-NI-004`.

Required corrections:

- No repository planning documents need correction.
- Future B1-NI execution should follow catalog definitions exactly.

Readiness conclusion:

- Ready for B1-NI fixture execution after review acceptance.

Recommendation:

- Resume B1-NI fixture execution using the authoritative mapping in this document.
