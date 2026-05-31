# Stage B Evaluator Architecture Discovery And Gap Analysis

## Scope

This document records architecture discovery findings and implementation-gap analysis for Stage B evaluator execution against real model outputs.

This is documentation-only analysis. It does not implement code, fixtures, schemas, or governance changes.

## Architecture Discovery

## 1. Major Subsystems

| Subsystem | Primary Responsibility | Required Inputs | Required Outputs | Doctrine Boundary |
|---|---|---|---|---|
| Run Ingestion | Load run context, manifest, split metadata, and row identity sources | run manifest, dataset metadata, model output artifacts | normalized run context and row references | No inference from paths/names |
| Row-Fact Metadata Layer | Emit declared eligibility/membership/ownership facts | dataset rows + approved ownership contracts | row facts with marker completeness | No detector-owned classification |
| Scoring Layer | Emit exact-valid and Family A subtype evidence | model outputs + expected behavior metadata | scorer outcomes, subtype or missing-evidence states, markers | No fallback subtype synthesis |
| Family Aggregation Layer | Build Family A/B1/B2 aggregates and governed sub-slices | row facts + scorer outputs | family summaries with count/denominator/rate | No parent/sibling substitution |
| State Engine | Compute completeness/computability/comparability states | family summaries + marker presence | explicit state triads and reasons | No collapsed state axes |
| Reconciliation Engine | Enforce arithmetic and scope consistency | aggregates, sub-slices, coverage summaries | pass/fail reconciliation records | No numeric override of missing markers |
| Comparability Engine | Classify concept-level baseline status | current-run facts + migration markers + baseline references | comparison-allowed/bridge-required/reference-only/comparison-blocked | No historical proxy promotion |
| Detector Projection Layer | Emit detector-consumable policy surface | family/state/reconciliation/comparability outputs | detector input artifact | Consumer-only payload; no raw reconstruction inputs |
| Fixture Validation Harness | Run WP8 fixtures against implementation outputs | fixture corpus + runtime outputs | structural/state/doctrine validation results | No fixture reinterpretation or inference |
| Reporting Layer | Emit audit, closure, and run reports | all subsystem outputs | governance report artifacts | Preserve reason-level traceability |

## 2. Proposed Module Boundaries

Recommended module boundaries for implementation planning:

1. `stage_b_inputs`:
   - ingest manifests, run metadata, baseline references, and source rows;
   - enforce deterministic run identity and split identity.
2. `stage_b_row_facts`:
   - construct declared row facts only;
   - validate ownership markers and conflict states.
3. `stage_b_scorer_family_a`:
   - produce exact-valid and subtype outputs with missing-evidence states.
4. `stage_b_aggregator`:
   - aggregate Family A/B1/B2 and governed sub-slices;
   - emit count/denominator/rate plus exclusions and split-scoped summaries.
5. `stage_b_state_machine`:
   - compute completeness/computability/comparability states per concept;
   - attach explicit reasons.
6. `stage_b_reconciliation`:
   - enforce denominator partition, boundedness, and coverage consistency.
7. `stage_b_comparability`:
   - evaluate baseline compatibility at concept scope.
8. `stage_b_detector_view`:
   - project consumer-only surface for policy logic.
9. `stage_b_fixture_runner`:
   - load fixtures and assert expected state/treatment/reconciliation behavior.
10. `stage_b_reports`:
   - emit structured audit and governance reports.

## 3. Major Data Flows

### Current-run flow

1. Real model outputs and row metadata enter `stage_b_inputs`.
2. `stage_b_row_facts` emits explicit eligibility/membership/ownership markers.
3. `stage_b_scorer_family_a` emits exact-valid + subtype evidence.
4. `stage_b_aggregator` emits family and sub-slice metrics.
5. `stage_b_state_machine` computes concept states and reasons.
6. `stage_b_reconciliation` validates arithmetic and scope integrity.
7. `stage_b_detector_view` publishes detector-consumable policy surface.
8. `stage_b_reports` emits run artifacts and audit traces.

### Baseline/comparison flow

1. Baseline references enter with migration markers.
2. `stage_b_comparability` classifies each concept-level comparison status.
3. Status is attached to detector view and reports.
4. Comparative rule execution is gated by emitted status only.

## 4. Doctrine Enforcement Points

Primary enforcement points:

1. `stage_b_row_facts`:
   - reject missing ownership markers where required;
   - represent conflicts as explicit noncomputable state.
2. `stage_b_scorer_family_a`:
   - forbid implicit `other` subtype;
   - emit missing-evidence states when subtype evidence is insufficient.
3. `stage_b_aggregator`:
   - forbid parent/sibling/mixed-tool denominator substitution.
4. `stage_b_comparability`:
   - forbid historical values as current-run substitutes;
   - enforce concept-scope comparison gating.
5. `stage_b_detector_view`:
   - expose emitted facts only;
   - exclude raw evidence that enables reconstruction.
6. `stage_b_fixture_runner`:
   - enforce no-inference expectations captured in `expected_detector_treatment`.

## State-Machine Requirements

## 1. Required State Axes

Each governed concept requires independent state axes:

1. completeness: `complete | partial | missing`
2. current-run computability: `current-run computable | current-run noncomputable`
3. comparability: `comparison-allowed | bridge-required | reference-only | comparison-blocked`

Each concept must also carry explicit reason lists:

- `noncomputability_reasons`
- `comparison_block_reasons` when applicable.

## 2. Required State Semantics

Required state semantics from fixture corpus:

1. `partial` does not always imply noncomputable for current-run (for example `X-CMP-006`).
2. current-run computable does not imply comparison-allowed.
3. missing denominator must block governed rate computation even when count exists.
4. family-level comparison-allowed must not auto-allow governed sub-slice comparison.
5. marker/ownership conflict must block governed use regardless of numeric consistency.

## 3. State Transition Requirements

Transition rules must be concept-local and evidence-driven:

1. Missing required facts transition concept to noncomputable without repair.
2. Addition of required facts can restore computability without changing comparison status.
3. Comparison status can transition only through explicit migration/marker evidence.
4. Conflict states must remain blocked until explicit resolution evidence exists.

## Reconciliation Engine Requirements

Required reconciliation checks:

1. Family A non-exact denominator equals sum of approved subtype counts when computable.
2. Direct-answer subtype remains independently visible and not merged with sibling counts.
3. Family B1 symbol-name denominator must be bounded by parent read-file context.
4. Family B2 anchor-category counts must reconcile to anchor-family denominator.
5. Coverage summaries must reconcile to governed denominators where emitted.
6. Split summaries must reconcile to aggregate summaries when active.
7. Reconciliation pass must be decoupled from comparability pass.
8. Reconciliation cannot clear ownership/taxonomy marker failures.

## Scoring Engine Requirements

Required scoring behavior:

1. Deterministic exact-valid partition on eligible tool-expected rows.
2. Deterministic subtype assignment for Family A eligible non-exact rows.
3. Explicit missing-evidence emission when subtype assignment cannot be made safely.
4. Precedence controls between direct-answer, scalar, malformed, wrapper drift, missing-tool-call, wrong tool name, wrong argument.
5. Marker outputs required for downstream governed interpretation:
   - failure taxonomy marker,
   - scorer semantics marker.

## Gap Analysis

## 1. Critical Gaps (Block Real Execution)

| Gap | Evidence | Impact |
|---|---|---|
| No Stage B family-output evaluator implementation | `scripts/eval_canonical_manifest.py` emits legacy aggregate metrics only | Cannot produce required family/sub-slice/state outputs |
| No Stage B fixture runner wired to runtime outputs | no script/test consumes `stage_b_wp8_validation` fixtures | Cannot validate implementation against authoritative corpus |
| No implemented row-fact ownership/membership emitter for B1/B2 | ownership contracts exist only in docs/fixtures | High risk of implicit inference or missing markers |
| No implemented Family A scorer subtype output path | WP3 contract/design are docs only | Family A governed subtype behavior unavailable |
| Detector consumes path-based legacy metric catalog, not Stage B family projection | `post_eval_collapse_detector.py` + `stage_b_v1_threshold_profile.json` | Detector cannot execute Stage B doctrine on real outputs |

## 2. High Gaps (Must Be Resolved During First Milestones)

| Gap | Evidence | Impact |
|---|---|---|
| Concrete executable schema not frozen | Stage B schema proposal remains conceptual and naming-flexible | Implementation drift risk across modules |
| Family-output threshold profile contract not migrated | current profile still references legacy `failure_profile.*` paths | Rule evaluation incompatible with Stage B family outputs |
| Baseline migration/comparability executable contract absent | comparability doctrine exists in fixtures/docs only | Risk of improper comparison enablement |
| Precision/rounding contract for rate reconciliation not fully codified | reconciliation fixtures require precision checks, code contract not present | Possible false pass/fail reconciliation outcomes |

## 3. Medium Gaps (Operational/Hygiene)

| Gap | Evidence | Impact |
|---|---|---|
| No standardized report schema for Stage B run outputs | reporting requirements documented but not implemented | Audit and downstream integration variability |
| No explicit implementation-time contract tests for doctrine guards | doctrine is fixture-encoded but runtime tests absent | Regression risk during iterative implementation |

## 4. Doctrine-To-Code Translation Risks

Primary translation risks:

1. Collapsing three-state axes into a single status field.
2. Reintroducing prompt/path/report-name inference in helper layers.
3. Allowing numeric reconciliation to override marker/ownership failures.
4. Enabling family-level comparability to leak into sub-slice comparability.
5. Treating optional diagnostics as governed evidence.

## Dependency Resolution Sequence

Recommended dependency sequence before full framework execution:

1. Freeze concrete Stage B output schema and enums.
2. Implement row-fact ownership/membership emitters.
3. Implement Family A scoring outputs.
4. Implement family aggregation/state/reconciliation engines.
5. Implement detector projection and Stage B-compatible threshold profile.
6. Wire fixture runner and execute full WP8 corpus validation.
7. Run controlled baseline migration classification before enabling comparative rule execution.

## Readiness Summary

Architecture discovery completeness: sufficient for implementation recommendation.

Gap posture: critical implementation gaps remain, but they are concrete and bounded. No governance redesign is required to proceed.
