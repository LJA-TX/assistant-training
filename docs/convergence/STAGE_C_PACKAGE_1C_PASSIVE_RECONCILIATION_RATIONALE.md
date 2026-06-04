# Stage C Package 1C Passive Reconciliation Rationale

## Scope

This artifact records the design rationale for the first passive reconciliation surface between authoritative Stage C facts and legacy detector-facing outputs.

This is a reconciliation-only slice. It does not migrate detector authority, threshold authority, comparability policy, or historical metrics.

## Candidate Reconciliation Scopes

### Candidate 1: Family A Internal Coverage Only

Question:

- Do authoritative Family A row-fact and scorer-evidence surfaces internally reconcile?

Why it is insufficient:

1. it does not compare authoritative Stage C facts to any legacy detector-facing surface;
2. it duplicates Package 1B governance-consumption coverage more than it advances migration-readiness evidence.

### Candidate 2: One Legacy Metric Only

Question:

- Does one selected legacy detector-facing metric reconcile directly with authoritative Stage C facts?

Why it is too narrow:

1. it would show only one point result rather than a surface-level migration-readiness picture;
2. it would not demonstrate blocked and unavailable cases alongside the aligned case.

### Candidate 3: The Four Active Compatibility-Bearing Legacy Surfaces

Question:

- For the four active legacy compatibility-bearing surfaces, which legacy outputs already reconcile directly with authoritative Stage C facts, and which remain unavailable or non-comparable without migration?

Why it is preferred:

1. the four surfaces are already explicitly named in the active threshold profile;
2. each surface is governance-relevant and historically compatibility-bearing;
3. the scope remains small while still producing actionable migration-readiness evidence;
4. the surface can be consumed directly from authoritative Stage C artifacts and the existing legacy summary without detector or threshold projection.

## Selected Scope

Selected passive reconciliation surfaces:

1. `read_file_exact_valid_rate`
2. `read_file_symbol_name_exact_valid_rate`
3. `no_anchor_exact_valid_share`
4. `direct_answer_substitution_count`

Source authority for the selection:

1. `manifests/reports/stage_b_v1_threshold_profile.json`
2. `docs/convergence/STAGE_B_EVAL_REDESIGN_METRIC_INVENTORY.md`

## Why This Scope Is Governance-Relevant

These surfaces capture the exact legacy metrics that remain active in detector/threshold policy while Stage C authoritative ownership remains partial:

1. one surface (`read_file_exact_valid_rate`) is directly consumable from current authoritative facts;
2. one surface (`read_file_symbol_name_exact_valid_rate`) depends on declared governed membership that may legitimately remain absent;
3. one surface (`direct_answer_substitution_count`) depends on scorer subtype coverage that currently preserves missing evidence rather than reconstructing it;
4. one surface (`no_anchor_exact_valid_share`) is already documented as semantically non-equivalent to the current authoritative B2 concept.

This produces the smallest reconciliation slice that can simultaneously show:

1. direct alignment,
2. authoritative unavailability,
3. explicit non-comparability,
4. future-migration requirements.

## Ownership Model Preserved

The passive reconciliation surface consumes:

1. authoritative Stage C row-fact metadata:
   - dataset-owned Family B1/B2 declared markers,
   - dataset-owned Family A tool-expected eligibility,
   - row identity and split identity;
2. authoritative Stage C Family A scorer evidence:
   - scorer-owned exact-valid state,
   - scorer-owned non-exact state,
   - scorer-owned subtype assignment,
   - scorer-owned missing-evidence state;
3. legacy summary output:
   - legacy `failure_profile` values only;
4. evaluator-emitted guardrail and runtime policy artifacts.

The consumer does not:

1. infer missing governed membership from prompt text;
2. infer missing subtype from generated text;
3. project detector metrics from Stage C artifacts;
4. project threshold outcomes from Stage C artifacts;
5. create authoritative replacement metrics.

## Reconciliation Status Semantics

Package 1C uses the following reconciliation statuses:

1. `aligned`
   - authoritative and legacy surfaces are directly consumable and match in the current run.
2. `unavailable`
   - required authoritative or legacy source facts are absent for the surface.
3. `not_comparable`
   - both sides exist as surfaces, but semantics are explicitly not equivalent under current authority.
4. `requires_future_migration`
   - direct consumption is possible or partially possible, but authoritative completeness or semantic readiness is insufficient for migration-safe alignment.

## Boundary Confirmation

This rationale does not authorize:

1. detector migration;
2. threshold migration;
3. comparability cutover;
4. historical metric replacement;
5. detector-cutover preparation work.
