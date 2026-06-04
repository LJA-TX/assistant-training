# Stage C Package 5B Acceptance Assessment

## Scope

Stage C Package 5B covers direct-answer substitution blocker-persistence assessment for:

- `direct_answer_substitution_count`

This package includes repeated full-run runtime evidence and read-only blocker bundling.

Explicit exclusions:

1. readiness reassessment;
2. gate reassessment;
3. detector behavior changes;
4. threshold behavior changes;
5. migration-flag changes;
6. replacement metrics;
7. migration planning.

## Inputs

Reviewed artifacts:

1. `docs/convergence/STAGE_C_PACKAGE_1C_RUNTIME_VALIDATION_REPORT.md`
2. `docs/convergence/STAGE_C_PACKAGE_1D_RUNTIME_VALIDATION_REPORT.md`
3. `docs/convergence/STAGE_C_PACKAGE_1E_CURRENT_SURFACE_GATE_ASSESSMENT.md`
4. `docs/convergence/STAGE_C_PACKAGE_5A_DIRECT_ANSWER_SUBSTITUTION_SURFACE_ENTRY_ASSESSMENT.md`
5. `docs/convergence/STAGE_C_PACKAGE_5A_ACCEPTANCE_ASSESSMENT.md`
6. `docs/convergence/STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
7. `docs/convergence/STAGE_B_WP3_FAMILY_A_SCORER_EVIDENCE_CONTRACT.md`
8. `docs/convergence/STAGE_B_WP8C_FAMILY_A_SUBTYPE_BOUNDARY_REVIEW.md`
9. `docs/convergence/STAGE_C9C_BASELINE_DELTA_COMPARABILITY_CLOSURE_DETERMINATION.md`
10. `docs/convergence/STAGE_C10C_REFRESHED_DETECTOR_MIGRATION_GATE_DETERMINATION.md`
11. `scripts/stage_c_package1b_passive_governance_consumer.py`
12. `scripts/stage_c_package1c_passive_reconciliation_surface.py`
13. `scripts/stage_c_package1d_migration_readiness_assessment.py`
14. `scripts/stage_c_package5b_direct_answer_blocker_persistence.py`
15. `tests/test_stage_c_package5b_direct_answer_blocker_persistence.py`
16. `evals/canonical_eval_manifest_v1.json`
17. `manifests/reports/stage_c_package5b_direct_answer_blocker_bundle_run_a.json`
18. `manifests/reports/stage_c_package5b_direct_answer_blocker_bundle_run_b.json`
19. `manifests/reports/stage_c_package5b_direct_answer_blocker_persistence_assessment.json`
20. `docs/convergence/STAGE_C_PACKAGE_5B_DIRECT_ANSWER_SUBSTITUTION_BLOCKER_PERSISTENCE_ASSESSMENT.md`

## Determinations

1. Package 5B stays within the bounded migration-gate assessment scope.
2. The direct-answer blocker persists across repeated full canonical runs.
3. The blocker-supporting row sets and blocker reasons are stable across repeated full runs.
4. Reproducibility is `strongly reproducible`.
5. The current blocker should be treated as a stable governed property of the frozen corpus plus current authoritative scorer-evidence behavior.
6. Subtype-completeness investigation is now the next logical blocker-focused follow-up.
7. Package 5B does not change readiness, gate, or planning state.

## Basis

### Determinations 1-2 Basis

The package executes the full repeated-run evidence requested without expanding into reassessment or migration work.

Across runs A and B:

1. `tool_expected_population_count = 140`
2. `non_exact_tool_expected_count = 140`
3. `subtype_assigned_count = 6`
4. `direct_answer_substitution_count = 0`
5. `missing_evidence_count = 134`
6. legacy direct-answer count = `125`

This reproduces the blocked authoritative posture on the full manifest rather than on a bounded sample.

### Determinations 3-4 Basis

The comparison artifact reports all critical blocker-stability checks as passing, including:

1. row identity stability;
2. tool-expected row identity stability;
3. non-exact row identity stability;
4. subtype-assigned row-id stability;
5. direct-answer row-id stability;
6. missing-evidence row-id stability;
7. missing-evidence reason stability;
8. reconciliation stability;
9. readiness stability;
10. legacy direct-answer surface stability;
11. guardrail stability.

The comparison classifier therefore correctly lands on `strongly reproducible`.

### Determination 5 Basis

The evidence now shows that the blocker is not transient:

1. repeated full runs reproduced the same authoritative blocker shape;
2. the blocker exists on the same frozen row identities;
3. the same missing-evidence reason accounts for the same blocker rows;
4. no drift toward direct-answer subtype assignment was observed.

That is enough to treat the blocker as a stable governed property of the current corpus plus current scorer-evidence behavior.

### Determination 6 Basis

Package 5A already established that lifecycle entry is possible on the current frozen corpus.

Package 5B now establishes that the blocker itself is stable.

So the next meaningful question is no longer:

1. whether the blocker exists;
2. whether the blocker is reproducible.

It is now:

1. why direct-answer/scalar subtype completeness remains missing for `134` rows;
2. whether that incompleteness is structurally expected under current scorer doctrine and evaluator implementation.

### Determination 7 Basis

Package 5B is explicitly blocker-persistence work only.

It does not alter:

1. current reconciliation status;
2. current readiness status;
3. current gate status;
4. detector authority;
5. threshold authority;
6. migration flags.

## Validation Results

Validation executed:

1. `python -m py_compile scripts/stage_c_package5b_direct_answer_blocker_persistence.py tests/test_stage_c_package5b_direct_answer_blocker_persistence.py` -> pass
2. `pytest -q tests/test_stage_c_package5b_direct_answer_blocker_persistence.py tests/test_stage_c_package2a_gate_evidence_bundle.py tests/test_stage_c_package1d_migration_readiness_assessment.py tests/test_stage_c_package1c_passive_reconciliation_surface.py tests/test_stage_c_package1b_passive_governance_consumer.py` -> pass (`17 passed`)
3. full canonical run A on frozen manifest -> pass
4. full canonical run B on frozen manifest -> pass
5. Package 1B/1C/1D on both runs -> pass
6. Package 5B blocker bundle build for both runs -> pass
7. Package 5B blocker comparison -> pass
8. `git diff --check` -> pass

## Known Limitations

1. Package 5B does not explain the blocker; it only proves persistence.
2. Package 5B does not determine whether the blocker can be reduced or resolved under current scorer/evaluator behavior.
3. Package 5B does not perform readiness or gate reassessment, even though the blocker evidence now has stronger full-run support.

## Recommendation

Recommended post-Package-5B interpretation:

1. treat the current direct-answer blocker as stable and governed, not transient;
2. preserve the current `migration-blocked` and `gate-blocked` posture unchanged;
3. focus future surface work on subtype-completeness investigation rather than on further blocker-existence validation.

## Boundary Confirmation

Confirmed unchanged:

1. detector authority;
2. threshold authority;
3. migration flags;
4. current readiness state;
5. current gate state;
6. current planning-authorization state;
7. runtime evaluator behavior.
