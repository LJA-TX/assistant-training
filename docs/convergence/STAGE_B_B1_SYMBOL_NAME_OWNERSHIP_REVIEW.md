# Stage B B1 Symbol-Name Ownership Review

## Scope

This document closes the Family B1 symbol-name ownership and declaration-rule questions identified before B1 fixture authoring.

This is documentation-only readiness closure.

Boundary confirmations:

- It does not implement fixtures.
- It does not implement validators.
- It does not implement schemas.
- It does not implement runtime behavior.
- It does not modify detectors, scorers, evaluators, thresholds, governance rules, mappings, or manifests.

Reference inputs:

- `STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
- `STAGE_B_EVAL_REDESIGN_EMISSION_DESIGN.md`
- `STAGE_B_EVAL_REDESIGN_IMPLEMENTATION_READINESS.md`
- `STAGE_B_EVAL_REDESIGN_SCHEMA_PROPOSAL.md`
- `STAGE_B_WP8_EXECUTION_PLAN.md`
- `STAGE_B_WP8A_SCENARIO_CATALOG.md`
- `STAGE_B_VALIDATION_FIXTURE_MATRIX_PLAN.md`
- `STAGE_B_WP8_MIDPOINT_ASSESSMENT.md`

## Summary Determination

Symbol-name membership is a dataset/evaluation metadata declaration, not a detector-derived classification.

The symbol-name governed sub-slice remains a required governed sub-slice inside Family B1. It should not be retired, downgraded, inferred from prompt text, reconstructed from historical reports, or replaced by the aggregate read-file preservation metric.

This review resolves the following B1 fixture-readiness blockers at the planning level:

- symbol-name sub-slice declaration rule approval;
- symbol-name membership ownership approval;
- detector non-inference boundary for symbol-like prompt text;
- historical-baseline treatment for symbol-name evidence.

## Ownership Authority

| Fact Or Decision | Owner | Detector Role |
|---|---|---|
| Row identity | Dataset metadata | Consume only after emission |
| Split membership | Dataset metadata | Consume only after emission |
| Expected tool identity | Dataset metadata | Consume only after emission |
| Read-file family eligibility | Dataset metadata or evaluator-owned metadata preparation | Consume only after emission |
| Symbol-name sub-slice membership | Dataset metadata or evaluator-owned metadata preparation | Must not infer |
| Exact-valid scorer outcome | Scorer | Must not recompute |
| Aggregated counts, denominators, and rates | Evaluator | Consume only after emission |
| Comparability status | Evaluator, based on approved metadata and migration review | Must not infer |

Symbol-name membership may be prepared by evaluation data tooling, but its governance authority must remain upstream of the detector and explicit before aggregation.

## Declaration Rules

Required declaration rules:

- Symbol-name membership must be declared before aggregation.
- Symbol-name non-membership must also be representable for read-file rows outside the sub-slice.
- Symbol-name membership applies only within the eligible read-file family population.
- A symbol-name governed row must also carry the required read-file family context.
- Missing symbol-name membership makes the symbol-name governed sub-slice noncomputable for the affected row or summary.
- A prompt containing a symbol-like string is not a membership declaration.
- A generated answer containing a symbol-like string is not a membership declaration.
- Historical symbol-name classification is not current-run membership evidence.

These rules support the planned B1 scenarios:

- `B1-C-003` and `B1-C-004`, where symbol-name membership is present and computable;
- `B1-C-005`, where a read-file row is explicitly outside the symbol-name sub-slice;
- `B1-M-004`, where missing membership blocks symbol-name computation;
- `B1-NI-003`, where prompt text must not become membership evidence.

## Membership Determination

The approved source of symbol-name membership is explicit evaluation metadata, or an evaluator-owned preprocessing step that writes explicit metadata before aggregation.

Membership must not be determined by:

- detector inspection of prompt text;
- detector inspection of generated text;
- row filename or artifact path heuristics;
- aggregate read-file behavior;
- mixed-tool aggregate behavior;
- historical report-layer values;
- baseline rates;
- inferred relationship to neighboring rows.

If the membership source is absent, ambiguous, or contradictory, the affected symbol-name concept is noncomputable. The detector may report the missing or conflicting condition only if it is emitted as such; it must not repair it.

## Detector Non-Inference Boundaries

Detector must not infer:

- that a row is read-file eligible;
- that a row belongs to the symbol-name sub-slice;
- symbol-name denominator membership;
- symbol-name numerator membership;
- exact-valid status;
- split membership;
- exclusion status;
- baseline comparability status.

Detector may consume:

- emitted symbol-name count;
- emitted symbol-name denominator;
- emitted symbol-name rate;
- emitted parent read-file context;
- emitted current-run completeness and computability states;
- emitted comparability status;
- emitted noncomputability reasons.

## Historical-Baseline Treatment

Historical symbol-name rates may be used for comparison only when the current run emits sufficient current-run facts and an approved comparability or migration bridge exists.

Historical symbol-name values must remain reference-only or bridge-required when:

- current symbol-name membership is missing;
- current symbol-name denominator is missing;
- current parent read-file context is missing;
- symbol-name subpopulation definition changed without approved bridge;
- historical evidence is report-layer only;
- historical denominator is unknown;
- historical row-set or split scope is unknown.

Historical evidence must not become current-run membership, numerator, denominator, or rate evidence.

## Governance Implications

The symbol-name sub-slice exists to prevent aggregate read-file recovery from hiding a harder extraction-like subpopulation collapse. Removing explicit membership ownership would weaken this governance signal.

Governance implications:

- Symbol-name must remain visible as a governed sub-slice.
- Count and denominator must remain visible, especially for small denominators.
- Parent read-file aggregate cannot replace symbol-name sub-slice facts.
- Missing symbol-name membership must halt governed symbol-name computation.
- Detector-side inference would violate the no-proxy and no-reconstruction doctrines.

## Closure Determination

The symbol-name ownership blocker is resolved at the planning level.

Fixture authoring may proceed after review acceptance using these rules:

- symbol-name membership is explicit upstream metadata;
- detector does not infer membership;
- missing membership is noncomputable;
- historical symbol-name evidence is not current-run evidence;
- aggregate read-file evidence does not replace symbol-name sub-slice evidence.
