# Stage C10-A Non-Authoritative Adapter Integration Plan

## Scope

This plan defines the smallest safe non-authoritative integration path for C9 contract and disposition outcomes into the detector projection adapter path.

Route selected from `AGENTS.md`: `migration_gate`.

This is planning only. It does not implement evaluator behavior, modify detector behavior, modify threshold profiles, authorize detector migration, or authorize threshold-profile migration.

## Authoritative Inputs Reviewed

1. `AGENTS.md`
2. `docs/convergence/STAGE_C9A_ADVERSARIAL_NO_CALL_SUBSET_MAPPING_REVIEW.md`
3. `docs/convergence/STAGE_C9A_ADVERSARIAL_NO_CALL_SUBSET_CLOSURE_DETERMINATION.md`
4. `docs/convergence/STAGE_C9B_NO_ANCHOR_SEMANTIC_EQUIVALENCE_BRIDGE_REVIEW.md`
5. `docs/convergence/STAGE_C9B_NO_ANCHOR_SEMANTIC_EQUIVALENCE_CLOSURE_DETERMINATION.md`
6. `docs/convergence/STAGE_C9C_BASELINE_DELTA_COMPARABILITY_GATE_REVIEW.md`
7. `docs/convergence/STAGE_C9C_BASELINE_DELTA_COMPARABILITY_CLOSURE_DETERMINATION.md`
8. `docs/convergence/STAGE_C9D_NO_ANCHOR_METRIC_DISPOSITION_REVIEW.md`
9. `docs/convergence/STAGE_C9D_NO_ANCHOR_METRIC_DISPOSITION_CLOSURE_DETERMINATION.md`
10. `docs/convergence/STAGE_C9_POST_BLOCKER_REASSESSMENT.md`
11. `docs/convergence/STAGE_C9_POST_BLOCKER_MIGRATION_READINESS_DETERMINATION.md`
12. `docs/convergence/STAGE_C8_NON_AUTHORITATIVE_DETECTOR_PROJECTION_ADAPTER.md`
13. `docs/convergence/STAGE_C8_DETECTOR_PROJECTION_ADAPTER_CONFORMANCE_REPORT.md`
14. `scripts/stage_c8_non_authoritative_detector_projection_adapter.py`
15. `tests/test_stage_c8_non_authoritative_detector_projection_adapter.py`
16. `manifests/reports/stage_b_v1_threshold_profile.json`

## C9 Outcome Set

### C9-A Adversarial No-Call Subset Mapping Contract

C9-A determined:

1. A legacy adversarial no-call source subset exists in the Stage B canonical evaluation/probe topology.
2. Stage C emitted detector-projection surfaces did not already provide an explicit adversarial no-call subset marker.
3. The mapping contract can be defined without doctrine redesign.
4. Computation is allowed only from explicit adversarial subset evidence plus explicit no-call expectation and scoring evidence.
5. Aggregate no-call correctness, prompt text, source-case naming, report paths, and historical metric values cannot substitute for explicit subset membership.
6. The blocker is partially resolved because the contract exists, but emitted evidence and adapter behavior remain incomplete.

### C9-B No-Anchor Semantic-Equivalence Finding

C9-B determined:

1. Legacy `no_anchor_exact_valid_share` maps to `failure_profile.anchor_exact_share.no_anchor_phrase`.
2. The legacy metric is a share of exact-valid rows in a historical no-anchor prompt bucket.
3. Stage C B2 no-anchor governed-rate denominator is eligible rows in the declared no-anchor category.
4. The denominator semantics are not equivalent.
5. Semantic equivalence cannot be established from current authority.
6. Stage C B2 governed-rate evidence cannot be substituted into the legacy metric.

### C9-C Baseline-Delta Comparability Gate Contract

C9-C determined:

1. The legacy threshold profile has one active delta-vs-baseline rule: `direct_answer_substitution_delta_gt_3`.
2. Delta evaluation requires current and baseline metric values under the threshold profile, with `missing_baseline_policy=fail_fast`.
3. Stage C comparability is concept-scoped and independent from completeness and current-run computability.
4. Delta evaluation is allowed only when the affected concept is current-run computable and has concept-scoped `comparison-allowed` evidence with denominator, provenance, migration, and reconciliation evidence present.
5. Compatibility-only same-run baselines must not become approved comparable baselines.
6. The gate is resolved at contract-definition level, but not implemented in the adapter path.

### C9-D No-Anchor Metric Disposition

C9-D selected authoritative noncomputable preservation:

1. `no_anchor_exact_valid_share` remains visible as a legacy detector metric identity.
2. The metric remains `projection_status=noncomputable_blocked`.
3. The metric value remains absent/null.
4. The reason code remains `blocked_no_anchor_share_semantic_mismatch`.
5. Stage C B2 no-anchor governed-rate evidence must not be substituted into the metric.
6. Replacement, retirement, threshold migration, or computation requires later authority.

## Incorporation Assessment

| C9 Outcome | Incorporation Into Non-Authoritative Adapter | Allowed Current Behavior | Required Guardrail |
|---|---|---|---|
| C9-A adversarial mapping contract | Yes, as optional explicit-evidence projection logic and richer blocked evidence. | Compute only if explicit adversarial subset, no-call expectation, denominator, and scoring evidence are present. Otherwise remain blocked. | Do not infer subset from prompt, case ID, path, filename, aggregate no-call metric, or historical report. |
| C9-B no-anchor non-equivalence | Yes, as guardrail evidence. | Preserve blocked status and prohibit B2 governed-rate substitution. | Do not compute legacy metric from Stage C B2 governed-rate surfaces. |
| C9-C baseline-delta gate | Yes, as a non-authoritative gate-reporting artifact or adapter evidence section. | Emit blocked delta-gate status unless all C9-C pass conditions are explicitly present. | Do not treat C8 compatibility baseline as authoritative comparison evidence. |
| C9-D no-anchor disposition | Yes, as explicit metric disposition evidence. | Keep `no_anchor_exact_valid_share` visible and `noncomputable_blocked`. | Do not retire, replace, or compute the metric without later authority. |

## Outputs That Must Remain Noncomputable, Blocked, Or Migration-Disabled

### Migration Flags

All later adapter integration outputs must keep:

1. `authoritative_detector_output=false`
2. `detector_migration_enabled=false`
3. `threshold_profile_migration_enabled=false`

### No-Anchor Metric

`no_anchor_exact_valid_share` must remain:

1. `projection_status=noncomputable_blocked`
2. `value=null`
3. reason code `blocked_no_anchor_share_semantic_mismatch`
4. source evidence referencing C9-B and C9-D authority

Blocked conditions:

1. Stage C B2 governed-rate evidence is present but legacy exact-valid-share evidence is absent.
2. only historical report-layer values are available.
3. denominator compatibility would require substitution.
4. threshold rule evaluation would require treating the metric as computed.

### Adversarial No-Call Metric

`no_call_correctness_adversarial` may become non-authoritatively computable only when all C9-A inclusion and computability evidence is explicit in the current input surfaces.

It must remain blocked when:

1. adversarial subset marker is absent;
2. no-call expectation evidence is absent;
3. no-call scoring evidence is absent;
4. denominator is zero;
5. only aggregate no-call correctness is available;
6. only legacy report-layer metric values are available;
7. subset membership would require inference from prompt text, source-case ID, path, report name, or absence of markers.

Allowed reason codes include:

1. `blocked_adversarial_subset_mapping_unavailable`
2. `source_adversarial_subset_marker_missing`
3. `source_no_call_expectation_missing`
4. `source_no_call_scoring_missing`
5. `source_adversarial_subset_denominator_zero`
6. `source_adversarial_subset_provenance_conflict`
7. `source_adversarial_subset_inference_prohibited`

### Baseline-Delta Gate

`direct_answer_substitution_delta_gt_3` must remain blocked unless C9-C pass conditions are explicit.

Blocked conditions include:

1. baseline summary missing;
2. current metric missing or noncomputable;
3. baseline metric missing or noncomputable;
4. comparability status missing;
5. comparability is `bridge-required`;
6. comparability is `reference-only`;
7. comparability is `comparison-blocked`;
8. migration status missing;
9. denominator compatibility missing;
10. denominator scope mismatch;
11. current or baseline provenance missing;
12. baseline is compatibility-only.

Allowed reason codes include:

1. `baseline_summary_missing`
2. `baseline_metric_missing`
3. `current_metric_missing`
4. `current_metric_noncomputable`
5. `baseline_metric_noncomputable`
6. `comparability_status_missing`
7. `comparability_bridge_required`
8. `comparability_reference_only`
9. `comparability_comparison_blocked`
10. `migration_status_missing`
11. `denominator_compatibility_missing`
12. `denominator_scope_mismatch`
13. `baseline_provenance_missing`
14. `current_provenance_missing`
15. `baseline_compatibility_only`

The C8 compatibility detector run may remain as a consumer-readability check, but it must stay labeled compatibility-only and non-authoritative.

## Smallest Safe Implementation Slice

Recommended next implementation slice:

**Stage C10-B Non-Authoritative Detector Projection Adapter Contract Integration**

Recommended objective:

- Update the existing non-authoritative adapter path to reflect C9-A, C9-C, and C9-D outcomes without enabling detector migration or threshold-profile migration.

Recommended implementation scope:

1. Add explicit C9 contract/disposition references to adapter output evidence.
2. Preserve C8 adapter flags exactly:
   - `authoritative_detector_output=false`
   - `detector_migration_enabled=false`
   - `threshold_profile_migration_enabled=false`
3. Add optional adversarial no-call projection logic that computes `no_call_correctness_adversarial` only from explicit C9-A-compliant evidence.
4. Preserve `no_call_correctness_adversarial` as `noncomputable_blocked` when explicit C9-A evidence is absent.
5. Preserve `no_anchor_exact_valid_share` as `noncomputable_blocked` with reason `blocked_no_anchor_share_semantic_mismatch` and C9-D disposition evidence.
6. Add a non-authoritative baseline-delta gate artifact or evidence section for `direct_answer_substitution_delta_gt_3`.
7. Mark the baseline-delta gate blocked when comparability, baseline, denominator, migration, provenance, or reconciliation evidence is missing.
8. Explicitly mark C8 same-run baseline output as compatibility-only and not sufficient for C9-C gate pass.
9. Preserve C8 detector-consumer compatibility harness behavior.
10. Do not change threshold-profile JSON, detector code, evaluator runtime behavior, catalogs, fixtures, or governance doctrine.

Recommended emitted artifact updates:

1. existing projection adapter artifact: add C9 contract references and per-metric disposition fields;
2. noncomputable metric artifact: include C9-A/C9-D reason-code coverage;
3. new or extended delta-gate artifact: emit rule-level C9-C gate result and blocked reasons;
4. projection validation artifact: add checks for C9 contract integration, no-anchor preservation, baseline compatibility-only blocking, and disabled migration flags;
5. compatibility harness artifact: preserve C8 consumer-readability checks and explicitly report non-authoritative status.

## Required Validation For Later Implementation

Required validations:

1. `pytest -q tests/test_stage_c8_non_authoritative_detector_projection_adapter.py`
2. `python -m py_compile scripts/stage_c8_non_authoritative_detector_projection_adapter.py`
3. adapter run over existing sample records with no explicit adversarial subset marker:
   - `no_call_correctness_adversarial` remains `noncomputable_blocked`
   - no inference from aggregate no-call metric occurs
4. synthetic or fixture-local adapter input with explicit C9-A-compliant adversarial subset evidence, if implementation authorizes a test-only input:
   - adversarial metric computes non-authoritatively from explicit evidence only
   - denominator and numerator evidence are preserved
5. no-anchor preservation check:
   - `no_anchor_exact_valid_share` remains `noncomputable_blocked`
   - reason code remains `blocked_no_anchor_share_semantic_mismatch`
   - B2 governed-rate evidence is not substituted
6. baseline-delta gate check:
   - compatibility-only baseline produces blocked gate status, not authoritative delta pass
   - missing comparability produces blocked status
   - `comparison-allowed` is required for any non-authoritative gate pass
7. migration flag check:
   - `authoritative_detector_output=false`
   - `detector_migration_enabled=false`
   - `threshold_profile_migration_enabled=false`
8. threshold-profile preservation check:
   - `manifests/reports/stage_b_v1_threshold_profile.json` remains unmodified
9. detector behavior preservation check:
   - `scripts/post_eval_collapse_detector.py` remains unmodified
10. C8 compatibility preservation:
   - schema continuity, required field presence, consumer readability, axis preservation, evidence preservation, and guardrail checks still pass.

## Governance Concerns

No new governance doctrine is introduced.

Active concerns for the next implementation slice:

1. adversarial computation must not infer subset membership from legacy paths, prompt text, case ID prefixes, or report names;
2. no-anchor noncomputable preservation must not be confused with metric retirement;
3. Stage C B2 no-anchor governed-rate evidence must remain separate from the legacy exact-valid-share metric;
4. compatibility-only baselines must not become authoritative baseline evidence;
5. baseline-delta gate reporting must not imply threshold-profile migration;
6. detector migration remains unauthorized until a refreshed migration gate approves it.

## Residual Ambiguities

No ambiguity blocks a non-authoritative adapter planning handoff.

Residual implementation choices for Stage C10-B:

1. whether to extend the existing C8 adapter artifact names or emit a new C10-specific artifact beside them;
2. whether adversarial explicit-evidence tests use a local test fixture or an existing real output record once explicit subset evidence exists;
3. how to name the baseline-delta gate artifact while avoiding authoritative detector-output language.

These are implementation-structure choices, not doctrine or migration blockers, provided all migration-disabled boundaries remain intact.

## Determination

Stage C10-A is closure-ready as a planning slice.

The smallest safe next implementation slice is Stage C10-B, limited to non-authoritative detector projection adapter contract integration.

Authoritative detector migration remains blocked.

Migration-disabled posture remains mandatory and unchanged.

## Boundary Confirmation

This plan did not modify evaluator runtime code, detector code, threshold profiles, fixture catalogs, fixture definitions, governance doctrine, or repository process infrastructure.

This plan does not authorize detector migration, threshold-profile migration, live inference, or replacement of existing detector outputs.
