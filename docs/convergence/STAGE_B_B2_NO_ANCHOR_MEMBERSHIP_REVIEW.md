# Stage B B2 No-Anchor Membership Review

## Scope

This document closes Family B2 no-anchor membership declaration and denominator-scope questions required before B2 fixture authoring.

This is documentation-only readiness closure. It does not implement fixtures, validators, schemas, runtime behavior, detectors, scorers, evaluators, thresholds, governance rules, mappings, or manifests.

Reference inputs:

- `STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
- `STAGE_B_EVAL_REDESIGN_EMISSION_DESIGN.md`
- `STAGE_B_EVAL_REDESIGN_IMPLEMENTATION_READINESS.md`
- `STAGE_B_EVAL_REDESIGN_SCHEMA_PROPOSAL.md`
- `STAGE_B_VALIDATION_FIXTURE_MATRIX_PLAN.md`
- `STAGE_B_WP8A_SCENARIO_CATALOG.md`
- `STAGE_B_IMPLEMENTATION_WORKPACKETS.md`

## Summary Determination

No-anchor membership must be declared before aggregation and must remain non-detector-owned.

Approved denominator rule:

- no-anchor exact-valid rate denominator is eligible rows in the declared no-anchor category.

Historical "share of exact-valid rows that are no-anchor" is a different denominator concept and cannot be substituted.

## Membership Declaration Rules

- No-anchor membership must be explicit for eligible rows.
- No-anchor non-membership must be explicit for eligible rows assigned to sibling categories.
- Missing no-anchor membership or category declaration makes the affected no-anchor concept noncomputable.
- No-anchor membership cannot be inferred from prompt text, generated text, or absence of anchor words.
- Anchor-family aggregate behavior cannot substitute for missing no-anchor governed sub-slice facts.

## Denominator Rules

No-anchor denominator:

- includes only anchor-eligible rows explicitly declared in the no-anchor category;
- excludes sibling anchor categories;
- excludes rows outside anchor-generalization population;
- excludes pre-aggregation excluded rows.

Count-only no-anchor evidence is insufficient for governed rate interpretation when denominator is missing.

## Historical-Baseline Treatment

Historical no-anchor evidence may be compared only when:

- anchor taxonomy is known and stable or explicitly bridged;
- assignment ownership is known and comparable;
- no-anchor denominator is known and comparable;
- split and population scope are known and comparable.

Historical no-anchor values remain `bridge-required` or `reference-only` when denominator compatibility or ownership comparability is unresolved.

## Detector Non-Inference Boundaries

Detector must not:

- classify no-anchor from prompt wording;
- classify no-anchor from generated output style;
- use family aggregate rate as no-anchor substitute;
- reinterpret historical denominator-incompatible shares as current-run no-anchor rate.

## Scenario Alignment

| Scenario | Expected Membership Or Denominator Handling |
|---|---|
| `B2-C-001` | Exact-valid no-anchor row with full membership and denominator evidence. |
| `B2-C-002` | Non-exact no-anchor row preserves denominator partition behavior. |
| `B2-P-001` | Anchor family aggregate present without no-anchor sub-slice remains noncomputable for no-anchor concept. |
| `B2-P-002` | No-anchor count without denominator remains noncomputable. |
| `B2-M-005` | Missing no-anchor sub-slice blocks no-anchor governed evaluation. |
| `B2-NI-001` | Prompt text cue absence does not create no-anchor membership. |
| `B2-NI-002` | Historical no-anchor share cannot substitute for missing denominator-compatible no-anchor rate. |
| `B2-NI-003` | Family aggregate cannot substitute for no-anchor governed sub-slice. |

## Closure Determination

The Family B2 no-anchor membership and denominator blocker is resolved for readiness closure.

B2 fixture authoring can proceed with explicit no-anchor membership and denominator semantics while preserving detector non-inference.
