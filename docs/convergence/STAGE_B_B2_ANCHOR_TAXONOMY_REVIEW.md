# Stage B B2 Anchor Taxonomy Review

## Scope

This document closes the Family B2 anchor taxonomy approval question required before B2 fixture authoring.

This is documentation-only readiness closure. It does not implement fixtures, validators, schemas, runtime behavior, detectors, scorers, evaluators, thresholds, governance rules, mappings, or manifests.

Reference inputs:

- `STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
- `STAGE_B_EVAL_REDESIGN_EMISSION_DESIGN.md`
- `STAGE_B_EVAL_REDESIGN_IMPLEMENTATION_READINESS.md`
- `STAGE_B_EVAL_REDESIGN_SCHEMA_PROPOSAL.md`
- `STAGE_B_VALIDATION_FIXTURE_MATRIX_PLAN.md`
- `STAGE_B_WP8A_SCENARIO_CATALOG.md`
- `STAGE_B_WP8_MIDPOINT_ASSESSMENT.md`
- `STAGE_B_THREAD_TRANSITION_ASSESSMENT.md`

## Summary Determination

Family B2 anchor taxonomy is approved for fixture authoring readiness at the planning level.

The approved taxonomy rule is:

- Anchor-generalization uses an explicit declared category set.
- The no-anchor category is required as a governed sub-slice concept.
- At least one sibling anchored category is required for contextual distribution.
- Every eligible row must carry a declared approved anchor category before aggregation.

No detector-side prompt or generated-text classification is allowed.

## Taxonomy Contract

### Required Taxonomy Properties

- Taxonomy is explicit, finite, and declared before aggregation.
- Taxonomy identity is versioned or marker-addressable for comparability review.
- No-anchor category is declared as a first-class approved category.
- Sibling anchored categories are declared under the same taxonomy.
- Unsupported categories cannot be silently coerced into no-anchor.

### Required Row-Level Facts

For every anchor-eligible row:

- anchor-generalization eligibility;
- approved anchor category;
- tool-expected eligibility status (under existing family doctrine);
- exact-valid scorer outcome;
- exclusion status.

### Required Aggregate Facts

- family denominator across anchor-eligible population;
- anchor-category denominators, numerators, and rates;
- no-anchor denominator, numerator, and rate;
- split-scoped anchor summaries when split governance is active;
- taxonomy and comparability markers.

### Detector Non-Inference Boundaries

Detector must not infer:

- anchor category from prompt text;
- no-anchor membership from absence of cue words;
- denominator membership from raw rows;
- taxonomy identity from artifact naming or path conventions.

## Comparability And Migration Implications

- No-anchor comparison is blocked unless taxonomy and assignment ownership are stable or explicitly bridged.
- Historical "share of exact-valid rows that are no-anchor" is denominator-incompatible with the approved no-anchor rate and cannot substitute for current-run no-anchor rate.
- Taxonomy changes require explicit migration status before comparison.

## Scenario-Catalog Coverage Alignment

The approved taxonomy contract aligns with these Family B2 scenarios:

- complete taxonomy-bearing coverage: `B2-C-001` through `B2-C-008`;
- incomplete taxonomy distribution or marker coverage: `B2-P-004`;
- missing taxonomy: `B2-M-002`;
- missing category for eligible row: `B2-M-004`;
- taxonomy-change comparison block: `B2-NI-004`.

## Closure Determination

The Family B2 anchor taxonomy blocker is resolved for fixture authoring readiness.

B2 fixture execution may rely on explicit declared taxonomy, with no detector inference and no denominator reinterpretation.
