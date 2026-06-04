# Stage C Package 1D Migration-Readiness Taxonomy Rationale

## Scope

This artifact records the rationale for the first passive migration-readiness assessment surface over authoritative Stage C artifacts and the Package 1C passive reconciliation output.

This is an assessment-only slice.

It does not:

1. migrate detector authority;
2. migrate threshold authority;
3. alter comparability policy;
4. create replacement metrics;
5. authorize migration.

## Assessment Question

For the four active compatibility-bearing legacy surfaces, does the current authoritative Stage C evidence support:

1. `migration-ready`;
2. `migration-blocked`;
3. `not-comparable`;
4. `insufficient-evidence`?

## Why Package 1C Statuses Alone Are Not Enough

Package 1C established reconciliation statuses:

1. `aligned`
2. `requires_future_migration`
3. `not_comparable`

Those statuses are necessary inputs, but they are not yet migration-readiness judgments.

Reasons:

1. `aligned` shows that a current run reconciles, but readiness still depends on guardrails and legacy-surface preservation.
2. `requires_future_migration` is too coarse:
   - some surfaces are blocked by explicit authoritative evidence;
   - some surfaces simply do not yet have enough governed evidence for a stronger judgment.
3. `not_comparable` is already an assessment-grade status and can carry forward unchanged.

## Selected Readiness Taxonomy

### `migration-ready`

Use when:

1. Package 1C reports direct reconciliation alignment;
2. Stage C guardrails remain clear;
3. legacy surface policy remains unchanged;
4. no current authoritative blocker is visible in emitted evidence.

### `migration-blocked`

Use when:

1. the surface is conceptually comparable;
2. current authoritative evidence exposes an explicit blocker;
3. the blocker is visible in emitted authoritative artifacts or inherited reconciliation evidence.

Example blocker classes:

1. missing scorer subtype evidence preserved as missing evidence;
2. missing row linkage or explicit completeness failures;
3. guardrail or legacy-policy violations.

### `not-comparable`

Use when:

1. current authority already establishes semantic non-equivalence between the authoritative Stage C surface and the historical legacy surface.

This carries forward Package 1C `not_comparable` directly.

### `insufficient-evidence`

Use when:

1. current authoritative artifacts do not yet provide enough governed evidence to classify the surface as ready or explicitly blocked;
2. the absence is visible and preserved rather than repaired.

## Why This Taxonomy Is Minimal

This taxonomy adds only the distinction that Package 1C lacked:

1. `requires_future_migration` splits into:
   - `migration-blocked`
   - `insufficient-evidence`
2. `aligned` refines into:
   - `migration-ready`, but only when guardrails and legacy-surface policy remain clear

No new metric semantics are introduced.

No detector or threshold projection is introduced.

## Surface-Level Application

The four active compatibility-bearing surfaces remain:

1. `read_file_exact_valid_rate`
2. `read_file_symbol_name_exact_valid_rate`
3. `no_anchor_exact_valid_share`
4. `direct_answer_substitution_count`

Authority for this surface set:

1. `manifests/reports/stage_b_v1_threshold_profile.json`
2. `docs/convergence/STAGE_B_EVAL_REDESIGN_METRIC_INVENTORY.md`

Expected readiness interpretations under current doctrine:

1. `read_file_exact_valid_rate`
   - eligible for `migration-ready` if direct reconciliation holds.
2. `read_file_symbol_name_exact_valid_rate`
   - may remain `insufficient-evidence` when declared governed membership is absent.
3. `direct_answer_substitution_count`
   - may be `migration-blocked` when scorer-owned subtype evidence preserves explicit missingness.
4. `no_anchor_exact_valid_share`
   - remains `not-comparable` under current no-anchor semantic disposition.

## Ownership Preservation

Package 1D consumes:

1. authoritative Stage C row-fact metadata;
2. authoritative Stage C Family A scorer evidence;
3. authoritative Stage C guardrail and runtime-contract artifacts;
4. Package 1C reconciliation output.

Package 1D does not:

1. reconstruct governed membership;
2. infer scorer subtype;
3. project detector outputs;
4. project threshold outcomes;
5. synthesize replacement metrics.

## Boundary Confirmation

This rationale does not authorize:

1. detector migration;
2. threshold migration;
3. comparability cutover;
4. historical metric replacement;
5. detector-cutover preparation work.
