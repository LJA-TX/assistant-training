# Stage C Package 5B Direct Answer Substitution Blocker Persistence Assessment

## Scope

This package evaluates whether the current authoritative blocker for:

- `direct_answer_substitution_count`

persists reproducibly across repeated full canonical runs on the frozen manifest.

This is blocker-persistence assessment only.

It does not:

1. perform readiness reassessment;
2. perform gate reassessment;
3. modify detector behavior;
4. modify threshold behavior;
5. alter migration flags;
6. create replacement metrics;
7. begin migration planning.

## Inputs

Existing surface-state and doctrine inputs:

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

Runtime and evidence inputs:

1. `evals/canonical_eval_manifest_v1.json`
2. `/tmp/stage_c_package5b_full_run_a/*`
3. `/tmp/stage_c_package5b_full_run_b/*`
4. `manifests/reports/stage_c_package5b_direct_answer_blocker_bundle_run_a.json`
5. `manifests/reports/stage_c_package5b_direct_answer_blocker_bundle_run_b.json`
6. `manifests/reports/stage_c_package5b_direct_answer_blocker_persistence_assessment.json`

Read-only helper and consumer inputs:

1. `scripts/stage_c_package1b_passive_governance_consumer.py`
2. `scripts/stage_c_package1c_passive_reconciliation_surface.py`
3. `scripts/stage_c_package1d_migration_readiness_assessment.py`
4. `scripts/stage_c_package5b_direct_answer_blocker_persistence.py`

## Current Blocker Shape

Current direct-answer blocker shape from existing authoritative evidence:

1. reconciliation status: `requires_future_migration`
2. readiness status: `migration-blocked`
3. gate status: `gate-blocked`
4. blocker reason code: `authoritative_family_a_subtype_surface_incomplete`

The blocker is authoritative rather than merely informational because the current Stage C Family A artifact already preserves:

1. tool-expected eligibility;
2. non-exact eligibility;
3. subtype assignment when supportable;
4. explicit missing-evidence state when subtype evidence is insufficient.

The question in Package 5B is whether that blocker shape is stable on the frozen corpus.

## Runtime Commands

Full canonical evaluator run A:

```bash
python scripts/eval_canonical_manifest.py \
  --manifest evals/canonical_eval_manifest_v1.json \
  --out-dir /tmp/stage_c_package5b_full_run_a
```

Full canonical evaluator run B:

```bash
python scripts/eval_canonical_manifest.py \
  --manifest evals/canonical_eval_manifest_v1.json \
  --out-dir /tmp/stage_c_package5b_full_run_b
```

Passive consumers and blocker bundles:

```bash
python scripts/stage_c_package1b_passive_governance_consumer.py --run-dir /tmp/stage_c_package5b_full_run_a
python scripts/stage_c_package1c_passive_reconciliation_surface.py --run-dir /tmp/stage_c_package5b_full_run_a
python scripts/stage_c_package1d_migration_readiness_assessment.py --run-dir /tmp/stage_c_package5b_full_run_a
python scripts/stage_c_package5b_direct_answer_blocker_persistence.py build \
  --run-dir /tmp/stage_c_package5b_full_run_a \
  --bundle-label run_a \
  --output-path manifests/reports/stage_c_package5b_direct_answer_blocker_bundle_run_a.json

python scripts/stage_c_package1b_passive_governance_consumer.py --run-dir /tmp/stage_c_package5b_full_run_b
python scripts/stage_c_package1c_passive_reconciliation_surface.py --run-dir /tmp/stage_c_package5b_full_run_b
python scripts/stage_c_package1d_migration_readiness_assessment.py --run-dir /tmp/stage_c_package5b_full_run_b
python scripts/stage_c_package5b_direct_answer_blocker_persistence.py build \
  --run-dir /tmp/stage_c_package5b_full_run_b \
  --bundle-label run_b \
  --output-path manifests/reports/stage_c_package5b_direct_answer_blocker_bundle_run_b.json

python scripts/stage_c_package5b_direct_answer_blocker_persistence.py compare \
  --left-bundle-path manifests/reports/stage_c_package5b_direct_answer_blocker_bundle_run_a.json \
  --right-bundle-path manifests/reports/stage_c_package5b_direct_answer_blocker_bundle_run_b.json \
  --output-path manifests/reports/stage_c_package5b_direct_answer_blocker_persistence_assessment.json
```

All commands exited `0`.

## Repeated Full-Run Assessment

### Run Summary Table

| Run | Tool-expected population | Non-exact population | Subtype-assigned population | Direct-answer subtype population | Missing-evidence population | Legacy direct-answer count |
|---|---:|---:|---:|---:|---:|---:|
| `run_a` | 140 | 140 | 6 | 0 | 134 | 125 |
| `run_b` | 140 | 140 | 6 | 0 | 134 | 125 |

### Subtype Shape

Observed authoritative subtype distribution for both runs:

1. `malformed output`: `6`
2. `direct-answer substitution`: `0`
3. `scalar substitution`: `0`
4. all other approved emitted subtypes: `0`

Observed non-exact primary-outcome distribution for both runs:

1. `invalid_json`: `140`

Observed missing-evidence reason counts for both runs:

1. `current canonical evaluator does not emit approved direct-answer or scalar substitution evidence`: `134`

## Row-Level Persistence Review

### Row Identity Stability

The repeated full runs preserved row identity fully:

1. `row_fact_record_count = 200` in both runs;
2. `unique_row_id_count = 200` in both runs;
3. overall `row_id_digest` matched across runs;
4. `tool_expected_row_id_count = 140` in both runs;
5. `non_exact_row_id_count = 140` in both runs;
6. tool-expected and non-exact row-id digests matched across runs.

### Missing-Evidence Row Stability

The blocker-supporting missing-evidence row set was stable across runs:

1. `missing_evidence_count = 134` in both runs;
2. `missing_evidence_row_id_digest` matched across runs;
3. the comparison artifact reports `missing_evidence_row_ids_stable = true`.

Observed structure:

1. the missing-evidence rows span both `heldout_validation` and `tool_holdout`;
2. they include the large majority of the `140` non-exact tool-expected rows;
3. they are not a transient subset or a small-denominator anomaly.

### Subtype-Assigned Row Stability

The subtype-assigned row set was also stable:

1. `subtype_assigned_count = 6` in both runs;
2. `subtype_assigned_row_id_digest` matched across runs;
3. all assigned rows remained `malformed output`, not `direct-answer substitution`.

Representative stable assigned row ids from run A:

1. `heldout_validation:2`
2. `heldout_validation:32`
3. `heldout_validation:5`
4. `heldout_validation:62`
5. `heldout_validation:7`
6. `heldout_validation:90`

### Direct-Answer Row Stability

The direct-answer subtype row set was stably empty:

1. `direct_answer_substitution_count = 0` in both runs;
2. `direct_answer_row_ids = []` in both runs;
3. `direct_answer_row_id_digest` matched across runs.

## Blocker-Reason Persistence Review

The blocker reason structure remained stable across runs.

Observed reasons:

1. only one missing-evidence reason was present:
   - `current canonical evaluator does not emit approved direct-answer or scalar substitution evidence`
2. the reason count was `134` in both runs;
3. the reason-to-row-id mapping digest matched across runs;
4. the comparison artifact reports `missing_evidence_reasons_stable = true`.

This means the blocker is not only count-stable but explanation-stable.

No run-specific alternate missing-evidence reason appeared.

No drift toward:

1. direct-answer subtype assignment;
2. scalar-substitution subtype assignment;
3. a different Family A missing-evidence cause.

## Reproducibility Determination

Reproducibility classification:

- `strongly reproducible`

### Basis

The comparison artifact reports all of the following as `true`:

1. `manifest_identity_stable`
2. `runtime_configuration_stable`
3. `summary_semantic_digest_stable`
4. `row_fact_semantic_digest_stable`
5. `comparison_rows_hash_stable`
6. `row_identity_stable`
7. `tool_expected_row_identity_stable`
8. `non_exact_row_identity_stable`
9. `package1b_snapshot_stable`
10. `blocker_inventory_stable`
11. `subtype_assigned_row_ids_stable`
12. `direct_answer_row_ids_stable`
13. `missing_evidence_row_ids_stable`
14. `missing_evidence_reasons_stable`
15. `focus_reconciliation_stable`
16. `focus_reconciliation_requires_future_migration_both`
17. `focus_readiness_stable`
18. `focus_readiness_migration_blocked_both`
19. `guardrails_clear_both`
20. `legacy_surface_stable`

So the current direct-answer blocker behaves as a stable governed property of the frozen corpus plus current authoritative scorer-evidence emission, not as a transient artifact of one run.

## Regimen Impact Assessment

### Readiness Work

Future readiness work remains meaningful.

Why:

1. the current blocker is stable enough to support targeted follow-up review;
2. the blocked state is reproducible, not noisy;
3. a later readiness-focused slice can investigate blocker structure without first questioning whether the blocker itself is real.

### Gate Work

Future gate work also remains meaningful, but only after blocker-oriented evidence work.

Why:

1. gate state remains downstream of readiness and blocker structure;
2. current repeated-run evidence confirms the blocker is durable;
3. this makes premature gate work unjustified, but makes later gate work better scoped once subtype completeness questions are addressed.

### Next Logical Focus

Subtype-completeness investigation is now the logical next focus.

Why:

1. corpus coverage is already known to be sufficient for lifecycle entry;
2. ownership boundaries are already established;
3. blocker persistence is now demonstrated;
4. the remaining active question is why the scorer/evaluator path preserves `134` direct-answer-or-scalar missing-evidence rows and only `6` malformed-output assignments on the full frozen corpus.

## Boundary Confirmation

This assessment does not:

1. perform readiness reassessment;
2. perform gate reassessment;
3. modify detector behavior;
4. modify threshold behavior;
5. alter migration flags;
6. create replacement metrics;
7. begin migration planning.
