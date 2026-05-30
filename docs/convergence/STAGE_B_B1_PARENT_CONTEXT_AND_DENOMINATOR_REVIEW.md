# Stage B B1 Parent Context And Denominator Review

## Scope

This document closes the Family B1 parent read-file context, denominator, and small-denominator visibility questions identified before B1 fixture authoring.

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

The symbol-name governed sub-slice is interpretable only inside its parent read-file family context.

The read-file aggregate and symbol-name sub-slice have related but distinct denominators. A complete parent aggregate may be reviewed independently where its own required facts are present, but it does not make a missing or incomplete symbol-name sub-slice computable.

This review resolves the following B1 fixture-readiness blockers at the planning level:

- parent read-file context rule approval;
- denominator relationship for read-file aggregate and symbol-name sub-slice;
- missing-parent behavior;
- small-denominator visibility acceptance.

## Parent Read-File Context

Family B1 has two governed levels:

| Level | Purpose | Required Context |
|---|---|---|
| Read-file aggregate | Protect exact-valid preservation for eligible read-file tool rows. | Expected tool identity, read-file eligibility, scorer exact-valid outcome, denominator, exclusions, split scope. |
| Symbol-name sub-slice | Protect a harder read-file subpopulation that can be hidden by aggregate recovery. | All read-file aggregate context plus explicit symbol-name membership, symbol-name denominator, symbol-name numerator, and sub-slice comparability context. |

The symbol-name sub-slice is not a separate top-level family. It is a governed sub-slice inside the read-file preservation family.

## Relationship Between Parent And Sub-Slice

Required relationship rules:

- Every symbol-name row must be a read-file eligible row.
- The symbol-name denominator must be bounded by the eligible read-file denominator.
- Symbol-name numerator and denominator must reconcile within the symbol-name sub-slice.
- The parent read-file context must be emitted for symbol-name interpretation.
- Parent aggregate facts may help interpret symbol-name behavior but must not substitute for missing symbol-name facts.
- Symbol-name comparison status may differ from parent read-file comparison status.
- Split-scoped symbol-name summaries must be emitted when split-scoped governance is active; aggregate symbol-name summaries do not substitute for missing split summaries.

These rules support the planned B1 scenarios:

- `B1-C-003` and `B1-C-004`, where symbol-name facts reconcile with parent context;
- `B1-C-005`, where a read-file row is outside the symbol-name denominator;
- `B1-P-001`, where parent aggregate is present but symbol-name is absent;
- `B1-P-003`, where symbol-name summary is present without parent context;
- `B1-P-005`, where split-scoped symbol-name summary is missing;
- `B1-NI-002`, where parent aggregate substitution is rejected.

## Inheritance Rules

Allowed inheritance:

- Symbol-name rows inherit read-file family eligibility only when both read-file eligibility and symbol-name membership are explicitly emitted.
- Symbol-name summaries may carry parent read-file context for interpretation and denominator-bounds reconciliation.
- Exclusion policy applies before governed denominator inclusion.

Disallowed inheritance:

- Parent read-file aggregate does not imply symbol-name membership.
- Parent read-file denominator does not become symbol-name denominator.
- Parent read-file exact-valid rate does not become symbol-name exact-valid rate.
- Parent read-file comparability status does not automatically become symbol-name comparability status.
- Mixed-tool denominator does not become read-file denominator.

## Missing-Parent Behavior

When parent read-file context is missing:

- symbol-name governed sub-slice is current-run noncomputable;
- parent-child denominator reconciliation is blocked;
- symbol-name rate is not governed-computable;
- baseline comparison is blocked unless an approved bridge explicitly covers the missing context;
- detector must not reconstruct parent context from aggregate labels, row text, or history.

When parent read-file aggregate is complete but symbol-name sub-slice is missing:

- parent read-file aggregate may remain computable for its own concept;
- symbol-name sub-slice remains noncomputable;
- parent aggregate cannot repair the missing sub-slice;
- detector may not use parent aggregate as symbol-name numerator, denominator, or rate.

## Denominator Rules

Read-file aggregate denominator:

- includes eligible read-file tool-expected rows;
- excludes non-read-file tool rows;
- excludes rows marked out before governed aggregation;
- requires expected tool identity and read-file eligibility facts.

Symbol-name denominator:

- includes only eligible read-file rows with explicit symbol-name membership;
- excludes read-file rows explicitly outside symbol-name membership;
- requires parent read-file context;
- requires visible denominator evidence;
- must not be reconstructed from symbol-like prompt text.

Count-only evidence is insufficient for either governed rate when the relevant denominator is missing.

## Small-Denominator Visibility

Small-denominator symbol-name cases must remain visible.

Reporting expectations:

- symbol-name count must be visible;
- symbol-name denominator must be visible;
- symbol-name rate may be emitted only when count and denominator are present and reconcile;
- small-denominator volatility must not be hidden by suppressing the denominator;
- aggregate read-file rate must not be used to smooth or mask symbol-name volatility.

Governance implications:

- Small denominators increase volatility but do not justify hiding counts or denominators.
- Visibility is required so reviewers can distinguish true collapse from small-population volatility.
- Threshold redesign is out of scope; this document does not set or adjust thresholds.

## Noncomputability Implications

The following conditions make the affected concept noncomputable:

- missing read-file eligibility marker;
- missing expected tool identity;
- missing read-file denominator;
- missing scorer exact-valid fact;
- missing symbol-name membership marker;
- missing symbol-name denominator;
- missing parent read-file context for symbol-name interpretation;
- missing split-scoped summary when split-scoped governance is active.

Detector behavior:

- report emitted noncomputability states;
- consume emitted facts only;
- do not infer missing denominators;
- do not use parent aggregate as sub-slice substitute;
- do not use mixed-tool denominator as read-file denominator.

## Closure Determination

The parent-context, denominator, and small-denominator visibility blockers are resolved at the planning level.

Fixture authoring may proceed after review acceptance using these rules:

- symbol-name is a governed sub-slice inside the read-file family;
- parent context is required for governed symbol-name interpretation;
- parent aggregate does not repair missing symbol-name evidence;
- small-denominator count and denominator visibility is required;
- missing parent, marker, denominator, or scorer facts create noncomputability.
