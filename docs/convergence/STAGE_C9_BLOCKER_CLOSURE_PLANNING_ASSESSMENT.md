# Stage C9 Blocker Closure Planning Assessment

## Scope

This artifact assesses the remaining authoritative detector-migration blockers after Stage C8 and identifies the smallest safe next Stage C9 slice.

This is a planning and readiness artifact only. It does not implement blocker resolutions, modify evaluator runtime behavior, modify detector code, alter threshold profiles, redesign governance doctrine, or authorize migration.

## Route And Inputs

Dispatcher route: `migration_gate`.

Primary process assets:

1. `docs/process_infrastructure/templates/conformance_report_template.md`
2. `docs/process_infrastructure/templates/milestone_determination_template.md`
3. `docs/process_infrastructure/checklists/validation_evidence_checklist.md`
4. `docs/process_infrastructure/checklists/governance_boundary_verification_checklist.md`
5. `docs/process_infrastructure/checklists/hygiene_review_checklist.md`

Authoritative inputs reviewed:

1. `AGENTS.md`
2. `docs/convergence/STAGE_C7_DETECTOR_PROJECTION_MIGRATION_IMPLEMENTATION_GATE.md`
3. `docs/convergence/STAGE_C7_DETECTOR_PROJECTION_MIGRATION_GATE_DETERMINATION.md`
4. `docs/convergence/STAGE_C8_NON_AUTHORITATIVE_DETECTOR_PROJECTION_ADAPTER.md`
5. `docs/convergence/STAGE_C8_DETECTOR_PROJECTION_ADAPTER_CONFORMANCE_REPORT.md`
6. `docs/convergence/STAGE_C0_C8_IMPLEMENTATION_REVIEW.md`
7. `docs/convergence/STAGE_C0_C8_MILESTONE_DETERMINATION.md`
8. `docs/convergence/STAGE_C0_EVALUATOR_IMPLEMENTATION_ENTRY_CONTRACT_LOCK.md`
9. `docs/convergence/STAGE_B_CLOSURE_ASSESSMENT.md`
10. `docs/convergence/STAGE_B_COMPLETION_DETERMINATION.md`
11. `docs/convergence/STAGE_B_LESSONS_LEARNED_SUMMARY.md`

## Blocker Inventory

### Active Authoritative Migration Blockers

| Blocker | Current State | Evidence | Active Status |
|---|---|---|---|
| Adversarial no-call subset mapping | `no_call_correctness_adversarial` has no authoritative Stage C emitted subset mapping contract. | C7 mapping gate and C0-C8 milestone determination. | active |
| No-anchor semantic-equivalence bridge | `no_anchor_exact_valid_share` is not authoritatively equivalent to the current Stage C B2 no-anchor governed-rate surface. | C7 mapping gate and C8 noncomputable reason `blocked_no_anchor_share_semantic_mismatch`. | active |
| Baseline-delta comparability gate | Detector delta-vs-baseline rule lacks authoritative comparability gating for migration path. | C7 safety gate and C0-C8 milestone determination. | active |

### Previously Identified But Addressed In C8

| Prior Issue | Current State | Basis |
|---|---|---|
| Detector-output consumer compatibility harness absent | Addressed for non-authoritative adapter scope. | C8 implemented compatibility harness; C8 conformance reports schema continuity, metric-catalog coverage, axis preservation, evidence preservation, and detector execution pass. |

### Additional Non-Blocking Risks

| Risk | Classification | Basis |
|---|---|---|
| Family B1/B2 real-output sample coverage is limited in computed mode | readiness risk, not authoritative blocker | C0-C8 review notes sample output coverage is Family A-heavy and leaves some projected metrics noncomputable. |
| Stage script coupling and repeated status strings | technical debt, not blocker | C0-C8 implementation review. |
| Full comparability engine behavior remains constrained | implementation gap coupled to baseline-delta gate | C0-C8 review and C0 contract. |

## Dependency Analysis

### Blocker Dependencies

| Blocker | Depends On | Notes |
|---|---|---|
| Adversarial no-call subset mapping | C4/C5 output record identity, no-call scoring evidence, explicit subset marker or fixture/source linkage, C8 non-authoritative projection evidence format | Does not require threshold migration or detector output replacement. |
| No-anchor semantic-equivalence bridge | B2 no-anchor doctrine, B2 anchor/no-anchor emitted surfaces, denominator provenance, comparability axis, C8 blocked metric handling | Coupled to denominator and semantic-equivalence proof. Higher risk than adversarial subset mapping. |
| Baseline-delta comparability gate | C0 comparability contract, current/baseline provenance, detector delta rule semantics, migration marker availability, no state-axis collapse | Cross-cutting and should be locked before any authoritative delta-rule migration. |

### Ordering

Recommended blocker-ordering sequence:

1. adversarial no-call subset mapping;
2. no-anchor semantic-equivalence bridge;
3. baseline-delta comparability gate;
4. re-run migration gate after all three blocker contracts are closed.

Rationale:

1. adversarial subset mapping is the smallest independently addressable blocker and has limited coupling to B2 denominator semantics;
2. no-anchor semantic equivalence depends on B2 doctrine, denominator provenance, and possibly bridge/reference comparability handling;
3. baseline-delta comparability is cross-cutting and should consume clarified concept mappings rather than precede them.

### Coupling Assessment

| Coupling | Determination |
|---|---|
| Adversarial subset mapping to no-anchor bridge | low |
| Adversarial subset mapping to baseline-delta gate | low to moderate; both must preserve comparability but adversarial mapping can remain current-run scoped. |
| No-anchor bridge to baseline-delta gate | moderate to high; bridge/equivalence outcomes may influence whether baseline comparisons are allowed, bridge-required, reference-only, or blocked. |
| All blockers to detector migration | high; authoritative detector migration remains blocked until all are closed and re-gated. |

## Slice Candidate Analysis

### Candidate 1: Adversarial No-Call Subset Mapping Contract

Objective:

Define the authoritative, non-inferential mapping contract for `no_call_correctness_adversarial` from Stage C emitted surfaces.

Scope:

1. inventory existing no-call/adversarial fixture and output-record markers;
2. define required explicit subset evidence;
3. define noncomputable behavior when subset evidence is absent;
4. define validation expectations for a later non-authoritative adapter update.

Expected artifacts:

1. Stage C9 adversarial no-call subset mapping contract;
2. conformance/readiness determination for non-authoritative implementation;
3. review ZIP.

Validation requirements:

1. confirm no prompt/path/report-name inference is used;
2. confirm subset membership must come from emitted fixture/source/record evidence;
3. confirm absent subset evidence remains noncomputable;
4. confirm migration flags remain disabled.

Governance risks:

1. accidentally deriving adversarial subset membership from fixture ID naming or prompt text;
2. converting absent subset evidence into an approximate aggregate;
3. allowing detector migration before validation.

Readiness:

Ready for bounded contract slice.

### Candidate 2: No-Anchor Semantic-Equivalence Bridge Contract

Objective:

Determine whether and how legacy `no_anchor_exact_valid_share` can be mapped to Stage C B2 no-anchor emitted surfaces without substitution or semantic collapse.

Scope:

1. review B2 no-anchor doctrine and emitted B2 surfaces;
2. compare legacy share semantics to Stage C governed-rate semantics;
3. define bridge-required, reference-only, comparison-blocked, or equivalence conditions;
4. define required denominator/provenance evidence.

Expected artifacts:

1. no-anchor semantic-equivalence/bridge assessment;
2. bridge-readiness determination;
3. validation checklist for future adapter behavior.

Validation requirements:

1. verify denominator scope identity;
2. verify numerator semantics;
3. verify ownership/taxonomy evidence;
4. verify missing/incompatible evidence remains noncomputable or comparison-blocked.

Governance risks:

1. denominator substitution;
2. collapsing legacy share and Stage C governed rate into one state without equivalence proof;
3. accidental doctrine redesign.

Readiness:

Partially ready; should follow adversarial mapping closure.

### Candidate 3: Baseline-Delta Comparability Gate Contract

Objective:

Define the authoritative comparability gate for detector delta-vs-baseline rule evaluation.

Scope:

1. specify required current/baseline provenance;
2. require concept-level comparability status before delta evaluation;
3. define blocked/reference-only/bridge-required behavior;
4. preserve status-axis independence.

Expected artifacts:

1. baseline-delta comparability gate contract;
2. delta-rule migration-readiness determination;
3. blocked-case validation matrix.

Validation requirements:

1. comparison cannot proceed without explicit `comparison-allowed`;
2. baseline absence or incompatible denominator blocks delta evaluation;
3. state axes remain independent;
4. detector migration remains disabled.

Governance risks:

1. historical denominator substitution;
2. migration-status inference by resemblance;
3. comparability collapse into binary comparable/non-comparable;
4. false pass from same-run compatibility-only baselines.

Readiness:

Partially ready; should follow or consume concept mapping closure.

### Candidate 4: Combined Blocker Closure Package

Objective:

Close all three active migration blockers in one package.

Scope:

1. adversarial subset mapping;
2. no-anchor bridge/equivalence;
3. baseline-delta comparability gate.

Expected artifacts:

1. combined blocker-closure assessment;
2. combined migration gate refresh;
3. readiness determination.

Validation requirements:

1. all individual blocker validations;
2. cross-blocker consistency checks;
3. detector migration remains disabled.

Governance risks:

1. scope too broad for safe first Stage C9 slice;
2. increased risk of conflating mapping, bridge, and comparability decisions;
3. harder review and rollback.

Readiness:

Not recommended as next slice.

## Recommended Next Slice

Recommended Stage C9 slice: **Stage C9-A Adversarial No-Call Subset Mapping Contract**.

Recommended objective:

Close the `no_call_correctness_adversarial` mapping blocker at the contract/evidence level, then determine whether a later non-authoritative adapter update is safe.

Recommended scope:

1. define the explicit source evidence that may classify an output record into the adversarial no-call subset;
2. define the exact emitted surfaces that may feed `no_call_correctness_adversarial`;
3. define blocked/noncomputable behavior when subset evidence is missing;
4. define validation requirements for any later C8-adapter extension;
5. preserve `authoritative_detector_output=false`, `detector_migration_enabled=false`, and `threshold_profile_migration_enabled=false`.

Out of scope:

1. detector migration;
2. threshold-profile migration;
3. detector output replacement;
4. no-anchor bridge closure;
5. baseline-delta gate closure;
6. doctrine redesign;
7. live inference or full benchmark execution.

Why this is the smallest safe slice:

1. it targets a single active blocker;
2. it is current-run scoped and does not require historical denominator or baseline comparability resolution;
3. it can preserve noncomputable behavior when explicit subset evidence is absent;
4. it can be reviewed independently before code changes.

## Stage C9 Entry Readiness

Stage C9 entry classification: **partially ready**.

Ready for:

1. bounded blocker-closure contract work;
2. non-authoritative mapping proofs;
3. validation design for explicit noncomputable behavior.

Not ready for:

1. authoritative detector migration;
2. threshold-profile migration;
3. baseline delta rule activation;
4. detector output replacement in manifest-linked flows.

## Governance Concerns

No new governance contradictions were found.

Active governance concerns to preserve:

1. no inference from prompt text, path naming, report naming, historical artifacts, or marker absence;
2. no denominator substitution;
3. no ownership or taxonomy auto-resolution;
4. no state-axis or comparability collapse;
5. no authoritative migration until all blockers are closed and a migration gate is re-run.

## Boundary Confirmation

This assessment did not modify evaluator code, detector code, threshold profiles, fixtures, catalogs, runtime behavior, or governance doctrine.
