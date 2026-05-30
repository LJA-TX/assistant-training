# Stage B B2 Conflicting Ownership Review

## Scope

This document closes the Family B2 conflicting-ownership handling question required before B2 fixture authoring.

This is documentation-only readiness closure. It does not implement fixtures, validators, schemas, runtime behavior, detectors, scorers, evaluators, thresholds, governance rules, mappings, or manifests.

Reference inputs:

- `STAGE_B_IMPLEMENTATION_WORKPACKETS.md`
- `STAGE_B_VALIDATION_FIXTURE_MATRIX_PLAN.md`
- `STAGE_B_WP8B_COMMON_STATE_FIXTURES.md`
- `STAGE_B_WP8A_SCENARIO_CATALOG.md`
- `STAGE_B_EVAL_REDESIGN_EMISSION_DESIGN.md`
- `STAGE_B_EVAL_REDESIGN_IMPLEMENTATION_READINESS.md`
- `STAGE_B_EVAL_REDESIGN_SCHEMA_PROPOSAL.md`

## Summary Determination

Conflicting ownership markers must block governed use for the affected B2 concept.

Approved handling:

- current-run noncomputable for affected governed concept;
- comparison-blocked for affected governed concept;
- report ownership conflict;
- do not choose a preferred ownership source.

## Conflict Classes

Conflicting-ownership conditions include:

- conflicting anchor assignment ownership markers;
- conflicting taxonomy ownership markers;
- conflicting row-level source ownership for anchor category or eligibility.

If two or more ownership markers conflict and no approved conflict-resolution marker exists, governed interpretation is blocked.

## Required Behavior

### Evaluator Emission

- Emit explicit noncomputability reason: conflicting ownership marker.
- Do not collapse conflict into a silently resolved owner.
- Preserve any numeric facts as diagnostic only; numeric reconciliation does not clear ownership conflict.

### Detector Consumption

- Consume emitted conflict state.
- Do not apply precedence rules, heuristics, or fallback owner inference.
- Do not permit comparative interpretation while conflict remains unresolved.

## State Expectations

For affected concept:

- completeness state: `partial` (or `missing` if additional required facts are absent);
- current-run computability state: `current-run noncomputable`;
- comparability state: `comparison-blocked`.

## Scenario And Fixture Alignment

| Source | Coverage |
|---|---|
| `WP8B-CS-015` | Canonical cross-family conflicting ownership handling behavior. |
| `B2-P-003` | Anchor categories present without assignment ownership marker; blocks provenance validity. |
| `B2-M-003` | Missing ownership marker for anchor assignment blocks governed anchor use. |
| `B2-NI-004` | Taxonomy-change comparison remains blocked without approved migration status. |

## Disallowed Resolution Patterns

- Selecting dataset ownership by default when evaluator ownership is also emitted.
- Selecting evaluator ownership by default when dataset ownership is also emitted.
- Selecting owner based on numeric coherence alone.
- Selecting owner based on historical prevalence.
- Selecting owner based on prompt-text resemblance.

## Closure Determination

The Family B2 conflicting ownership handling blocker is resolved for fixture-readiness planning.

B2 fixture execution can treat conflicts as explicit noncomputability rather than detector-resolved ownership.
