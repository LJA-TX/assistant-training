# Stage C9-A Adversarial No-Call Subset Closure Determination

## Scope

This determination closes the Stage C9-A contract-definition slice for the adversarial no-call subset mapping blocker.

Decision boundary:

1. Determine whether an authoritative adversarial no-call subset exists in Stage B/C artifacts.
2. Define ownership, inclusion/exclusion, provenance, computability, and noncomputable conditions when sufficient authority exists.
3. Identify missing authority where Stage C emitted surfaces remain incomplete.
4. Determine blocker status and Stage C9-A closure readiness.

This determination does not authorize detector migration or threshold-profile migration.

## Inputs

1. `AGENTS.md`
2. `docs/convergence/STAGE_C9A_ADVERSARIAL_NO_CALL_SUBSET_MAPPING_REVIEW.md`
3. `docs/convergence/STAGE_C9_BLOCKER_CLOSURE_PLANNING_ASSESSMENT.md`
4. `docs/convergence/STAGE_C9_BLOCKER_CLOSURE_READINESS_DETERMINATION.md`
5. `docs/convergence/STAGE_C7_DETECTOR_PROJECTION_MIGRATION_IMPLEMENTATION_GATE.md`
6. `docs/convergence/STAGE_C7_DETECTOR_PROJECTION_MIGRATION_GATE_DETERMINATION.md`
7. `docs/convergence/STAGE_C8_NON_AUTHORITATIVE_DETECTOR_PROJECTION_ADAPTER.md`
8. `docs/convergence/STAGE_C8_DETECTOR_PROJECTION_ADAPTER_CONFORMANCE_REPORT.md`
9. `manifests/reports/stage_b_v1_threshold_profile.json`
10. `manifests/reports/stage_b_first_probe_design.md`
11. `evals/data/canonical_v1/adversarial.jsonl`
12. Stage C4/C5/C6 emitted contract and reporting artifacts

## Determinations

1. An authoritative legacy adversarial no-call source subset exists in the Stage B canonical evaluation/probe topology.
2. An authoritative Stage C emitted detector-projection mapping for that subset did not exist before Stage C9-A.
3. Stage C9-A defines the required mapping contract at the evidence and computability level.
4. The adversarial no-call subset mapping blocker is partially resolved for the broader detector-migration path.
5. Stage C9-A is closure-ready as a contract-definition and evidence-mapping slice.
6. Detector migration remains unauthorized.
7. Threshold-profile migration remains unauthorized.

## Basis

### Determination 1 Basis

The legacy source subset exists because `evals/data/canonical_v1/adversarial.jsonl` contains 20 adversarial rows with explicit metadata category `adversarial_malformed` and source `synthetic_adversarial_malformed`. The Stage B threshold profile and first probe design identify `no_call_correctness_adversarial` as a required monitored metric/slice.

### Determination 2 Basis

Stage C4/C5/C6 artifacts preserve no-call and scoring evidence but do not emit an explicit adversarial subset marker. Stage C7 classified `no_call_correctness_adversarial` as blocked, and Stage C8 emitted it as `noncomputable_blocked` with reason code `blocked_adversarial_subset_mapping_unavailable`.

### Determination 3 Basis

`STAGE_C9A_ADVERSARIAL_NO_CALL_SUBSET_MAPPING_REVIEW.md` defines:

1. source subset ownership;
2. legacy metric ownership;
3. Stage C projection ownership;
4. governance ownership;
5. inclusion criteria;
6. exclusion criteria;
7. provenance requirements;
8. computability requirements;
9. noncomputable conditions;
10. permitted and disallowed mapping sources.

### Determination 4 Basis

The blocker is partially resolved because the contract/evidence mapping now exists, but implementation and migration-gate conditions remain incomplete:

1. the C8 adapter has not been modified to compute the metric from explicit subset evidence;
2. Stage C output/scoring artifacts do not yet emit the explicit adversarial subset marker required by the mapping;
3. remaining C9 blockers still prevent authoritative detector migration.

### Determination 5 Basis

Stage C9-A is closure-ready because it satisfied the requested contract-definition and evidence-mapping scope without expanding into implementation, doctrine redesign, threshold migration, or detector migration.

## Active Blockers

Active blockers after Stage C9-A:

1. no-anchor semantic-equivalence bridge;
2. baseline-delta comparability gate;
3. non-authoritative adapter implementation update for adversarial no-call subset mapping, if implementation of this contract is selected as the next controlled slice.

These blockers do not invalidate Stage C9-A closure. They continue to block authoritative detector migration.

## Recommendation

Recommended next controlled step depends on selected track:

1. For blocker-contract sequencing: proceed to the no-anchor semantic-equivalence bridge assessment.
2. For implementation sequencing: implement a bounded non-authoritative adapter update that consumes only explicit adversarial no-call subset evidence and preserves noncomputable status when that evidence is absent.

Neither path should authorize detector migration or threshold-profile migration.

## Boundary Confirmation

This determination does not expand authorized scope.

This determination does not authorize:

1. detector migration;
2. threshold-profile migration;
3. replacement of existing detector outputs;
4. evaluator runtime behavior changes;
5. fixture catalog changes;
6. governance doctrine redesign.
