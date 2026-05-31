# Stage C8 Detector Projection Adapter Conformance Report

## Scope

This report records contract-conformance findings for Stage C8 non-authoritative detector projection adapter implementation.

## Conformance Targets

Checked for:

1. non-authoritative projection flags remain enforced,
2. unambiguous mappings are emitted from explicit source artifacts,
3. blocked metrics remain explicitly noncomputable with reason codes,
4. detector-consumer compatibility checks are executable and auditable,
5. state-axis independence and evidence visibility are preserved,
6. no inference/substitution/reconstruction behavior is introduced.

## Findings

## 1. Non-Authoritative Control Flags

Status: conformant.

Evidence:

1. adapter emits:
   - `authoritative_detector_output=false`
   - `detector_migration_enabled=false`
   - `threshold_profile_migration_enabled=false`
2. validation includes explicit `migration_flags_disabled` check.

## 2. Unambiguous Mapping Projection

Status: conformant in implemented scope.

Evidence:

1. explicit mappings emitted for:
   - `no_call_correctness_aggregate`
   - `wrapper_leakage_overall`
   - `invalid_json_overall`
   - `direct_answer_substitution_count`
2. B1 rate mappings remain explicit and noncomputable when B1 source concepts are absent in the current sample run.

## 3. Noncomputable Handling

Status: conformant.

Evidence:

1. blocked metrics remain `noncomputable_blocked` with explicit reason codes:
   - `blocked_adversarial_subset_mapping_unavailable`
   - `blocked_no_anchor_share_semantic_mismatch`
2. absent-source cases use explicit noncomputable status with source-missing reason code.
3. unresolved metrics are not inferred or backfilled.

## 4. Detector Consumer Compatibility Harness

Status: conformant.

Evidence:

1. compatibility harness executes detector over projected summaries without enabling migration.
2. schema continuity and metric-catalog coverage checks pass.
3. axis-preservation and evidence-preservation checks pass.
4. compatibility artifacts include emitted collapse-watch and gate-assessment outputs for auditability.

## 5. Governance And Guardrails

Status: conformant in implemented scope.

Evidence:

1. projection validation confirms no collapsed-state behavior.
2. projection validation confirms no inference/substitution/reconstruction flags.
3. adapter preserves explicit non-authoritative status and does not alter threshold profile behavior.

## Validation Results

1. `pytest -q tests/test_stage_c8_non_authoritative_detector_projection_adapter.py` -> pass
2. `python -m py_compile scripts/stage_c8_non_authoritative_detector_projection_adapter.py` -> pass
3. compatibility harness detector execution -> pass (as asserted by test suite and artifact checks)

## Governance Concerns

No new governance conflicts introduced in this slice.

Known unresolved migration blockers remain unchanged from Stage C7:

1. adversarial no-call subset mapping contract gap,
2. no-anchor share semantic-equivalence gap,
3. baseline-delta comparability gate gap for authoritative migration.

## Determination

Stage C8 non-authoritative detector projection adapter is contract-conformant in declared scope and remains safely migration-disabled.
