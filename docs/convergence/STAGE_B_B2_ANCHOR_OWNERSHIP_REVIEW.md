# Stage B B2 Anchor Ownership Review

## Scope

This document closes the Family B2 anchor-assignment ownership question required before B2 fixture authoring.

This is documentation-only readiness closure. It does not implement fixtures, validators, schemas, runtime behavior, detectors, scorers, evaluators, thresholds, governance rules, mappings, or manifests.

Reference inputs:

- `STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
- `STAGE_B_EVAL_REDESIGN_EMISSION_DESIGN.md`
- `STAGE_B_EVAL_REDESIGN_IMPLEMENTATION_READINESS.md`
- `STAGE_B_EVAL_REDESIGN_SCHEMA_PROPOSAL.md`
- `STAGE_B_IMPLEMENTATION_WORKPACKETS.md`
- `STAGE_B_IMPLEMENTATION_READINESS_REVIEW.md`
- `STAGE_B_VALIDATION_FIXTURE_MATRIX_PLAN.md`
- `STAGE_B_WP8A_SCENARIO_CATALOG.md`

## Summary Determination

Anchor assignment ownership is approved as explicit non-detector ownership.

Approved ownership rule:

- Primary default owner: dataset metadata.
- Alternate owner path: evaluator-owned pre-aggregation assignment, only when explicitly approved and emitted with ownership marker.
- Detector remains consumption-only and cannot assign categories.

## Ownership Authority

| Fact Or Decision | Owner | Detector Role |
|---|---|---|
| Row identity and split membership | Dataset metadata | Consume only |
| Anchor-generalization eligibility | Dataset metadata | Consume only |
| Anchor category assignment (default) | Dataset metadata | Must not infer |
| Anchor category assignment (approved alternate path) | Evaluator pre-aggregation process with explicit owner marker | Must not infer |
| Exact-valid outcome | Scorer | Must not recompute |
| Anchor-category and no-anchor aggregation | Evaluator | Consume only |
| Comparability status | Evaluator and migration review | Must not infer |

## Ownership Rules

- Ownership marker must be emitted for anchor assignment.
- If evaluator-owned assignment is used, emitted ownership evidence must be explicit and unambiguous.
- Ownership changes across runs require explicit migration handling before comparison.
- Missing ownership marker blocks governed anchor interpretation for affected concept.

## Disallowed Behavior

- Detector prompt-text or generated-text anchor classification.
- Implicit owner selection from artifact names or path conventions.
- Silent fallback from missing ownership marker to guessed owner.
- Numeric reconciliation overriding missing or ambiguous ownership.

## Scenario Alignment

| Scenario | Ownership Implication |
|---|---|
| `B2-P-003` | Categories present without assignment ownership marker must remain noncomputable. |
| `B2-M-003` | Missing ownership marker blocks governed anchor-category provenance. |
| `B2-M-004` | Missing category for eligible row blocks governed aggregation. |
| `B2-NI-001` | Prompt text must not become substitute ownership or category evidence. |
| `B2-NI-004` | Taxonomy change plus missing approved migration status keeps comparison blocked. |

## Closure Determination

The Family B2 anchor assignment ownership blocker is resolved for planning and fixture-readiness purposes.

B2 fixture authoring can proceed under explicit ownership markers and detector non-inference boundaries.
