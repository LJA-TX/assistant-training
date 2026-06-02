# Stage C9-C Baseline-Delta Comparability Closure Determination

## Scope

This determination closes the Stage C9-C baseline-delta comparability gate review slice.

Decision boundary:

1. determine legacy detector baseline-delta requirements;
2. identify Stage C comparability concepts and emitted evidence surfaces relevant to baseline comparison;
3. determine whether an authoritative comparability gate can be established;
4. define gate ownership, evidence, comparability, computability, and noncomputable conditions;
5. assess blocker status and Stage C9-C closure readiness.

This determination does not authorize detector migration or threshold-profile migration.

## Inputs

1. `AGENTS.md`
2. `docs/convergence/STAGE_C9C_BASELINE_DELTA_COMPARABILITY_GATE_REVIEW.md`
3. `docs/convergence/STAGE_C9_BLOCKER_CLOSURE_PLANNING_ASSESSMENT.md`
4. `docs/convergence/STAGE_C7_DETECTOR_PROJECTION_MIGRATION_IMPLEMENTATION_GATE.md`
5. `docs/convergence/STAGE_C8_NON_AUTHORITATIVE_DETECTOR_PROJECTION_ADAPTER.md`
6. `docs/convergence/STAGE_C0_EVALUATOR_IMPLEMENTATION_ENTRY_CONTRACT_LOCK.md`
7. `docs/convergence/STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
8. `docs/convergence/STAGE_B_EVAL_REDESIGN_SCHEMA_PROPOSAL.md`
9. `docs/convergence/STAGE_B_WP8A_SCENARIO_CATALOG.md`
10. Cross-family `X-CMP` and `X-NI` fixtures
11. `manifests/reports/stage_b_v1_threshold_profile.json`
12. `scripts/post_eval_collapse_detector.py`
13. Stage C6 and C8 projection-related artifacts

## Determinations

1. The legacy detector path has one active delta-vs-baseline rule: `direct_answer_substitution_delta_gt_3`.
2. The current threshold profile requires a baseline summary for delta rules under `missing_baseline_policy=fail_fast`.
3. Stage C comparability doctrine is authoritative and concept-scoped.
4. An authoritative baseline-delta comparability gate can be established from current authority.
5. Delta evaluation is allowed only when the affected concept is current-run computable and concept-scoped `comparison-allowed` with denominator, provenance, migration, and reconciliation evidence present.
6. The baseline-delta comparability gate blocker is resolved at contract-definition and evidence-mapping level.
7. Stage C9-C is closure-ready.
8. Detector migration remains unauthorized.
9. Threshold-profile migration remains unauthorized.

## Basis

### Determination 1 Basis

`manifests/reports/stage_b_v1_threshold_profile.json` contains one `delta_vs_baseline` rule:

- `direct_answer_substitution_delta_gt_3`

The rule uses metric ID `direct_answer_substitution_count` and evaluates current minus baseline against threshold `3.0` with comparator `gt`.

### Determination 2 Basis

`missing_baseline_policy=fail_fast` is declared in the threshold profile. `scripts/post_eval_collapse_detector.py` raises when a baseline summary is absent and delta dependencies exist under `fail_fast`.

### Determination 3 Basis

Stage C0 locks independent state axes and allowed comparability states. Stage B schema doctrine defines `comparison-allowed`, `bridge-required`, `reference-only`, and `comparison-blocked` and requires detector comparison to remain blocked unless comparison status is explicitly `comparison-allowed`.

### Determination 4 Basis

The current authority includes sufficient comparability semantics:

1. C0 comparator/state-axis contract;
2. Stage B schema comparability definitions;
3. direct-answer delta-specific comparability requirements;
4. cross-family `X-CMP-001` through `X-CMP-010` fixture coverage;
5. C6 projection-preparation source surfaces for comparability axis, denominator provenance, scoring evidence, and guardrails.

### Determination 5 Basis

`X-CMP-001` permits comparison only when current-run facts are computable and concept-level migration approval exists. `X-CMP-002` through `X-CMP-010` prove bridge-required, reference-only, missing migration status, current-run noncomputability, family/sub-slice scope divergence, missing denominator, taxonomy change, subpopulation change, and report-layer provenance blocks.

### Determination 6 Basis

The C9-C review defines the gate contract, ownership model, required evidence, comparability requirements, computability requirements, blocked conditions, and validation matrix without requiring doctrine redesign.

## Active Blockers

The baseline-delta comparability gate blocker is resolved at contract level.

Remaining overall detector-migration blockers and constraints:

1. C9-A adversarial no-call mapping is contract-defined but still requires later implementation if selected.
2. C9-B no-anchor semantic equivalence remains unresolved for authoritative detector migration.
3. The non-authoritative adapter has not been updated to enforce the C9-C gate for authoritative detector projection.
4. A refreshed detector migration gate is required before any authoritative detector migration.

## Recommended Next Controlled Step

Recommended next controlled step:

- Stage C9 blocker-closure rollup and migration-gate refresh assessment.

Purpose:

1. reconcile C9-A, C9-B, and C9-C outcomes;
2. determine whether any non-authoritative implementation slice is safe;
3. preserve migration-disabled posture until all blockers are dispositioned.

If implementation resumes before rollup, the smallest safe implementation candidate is a non-authoritative adapter gate check that emits blocked delta status unless concept-scoped `comparison-allowed` evidence is present. That implementation is not authorized by this determination.

## Boundary Confirmation

This determination does not expand authorized scope.

This determination does not authorize:

1. detector migration;
2. threshold-profile migration;
3. replacement of existing detector outputs;
4. evaluator runtime behavior changes;
5. fixture catalog changes;
6. governance doctrine redesign;
7. detector code changes.
