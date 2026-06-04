# Stage C Package 1A Implementation Summary

## Scope

This artifact records Stage C Package 1A implementation for authoritative row-identity instantiation in the live canonical evaluator Stage C artifact path.

Implemented scope only:

1. contract clarification for canonical row identity;
2. authoritative `row_id` instantiation for emitted Stage C row-fact and Family A scorer-evidence artifacts;
3. targeted validation coverage for duplicate provenance labels, identical duplicated rows, and repeated frozen-rowset stability;
4. representative runtime validation against the frozen canonical evaluator manifest.

Out of scope:

1. detector migration;
2. threshold-profile migration;
3. comparability cutover;
4. historical metric identity replacement;
5. Package 2 work.

## Authoritative Inputs

Implementation aligned to:

- `STAGE_C_PACKAGE_1A_CANONICAL_ROW_IDENTITY_CONTRACT_CLARIFICATION.md`
- `STAGE_B_EVAL_REDESIGN_CONTRACTS.md`
- `STAGE_B_EVAL_REDESIGN_EMISSION_DESIGN.md`
- `STAGE_B_WP3_FAMILY_A_SCORER_EVIDENCE_CONTRACT.md`
- `STAGE_B_WP3_SCORER_EVIDENCE_OUTPUT_DESIGN_REVIEW.md`
- `STAGE_C0_EVALUATOR_IMPLEMENTATION_ENTRY_CONTRACT_LOCK.md`
- `scripts/build_dataset_v1.py`
- `scripts/eval_canonical_manifest.py`
- `tests/test_eval_canonical_manifest.py`

## Implemented Artifacts

Changed implementation surfaces:

1. `scripts/eval_canonical_manifest.py`
2. `tests/test_eval_canonical_manifest.py`

Created documentation artifacts:

1. `docs/convergence/STAGE_C_PACKAGE_1A_CANONICAL_ROW_IDENTITY_CONTRACT_CLARIFICATION.md`
2. `docs/convergence/STAGE_C_PACKAGE_1A_RUNTIME_VALIDATION_REPORT.md`
3. `docs/convergence/STAGE_C_PACKAGE_1A_ACCEPTANCE_ASSESSMENT.md`

## Implemented Behavior

### 1. Authoritative Row Identity Instantiation

Stage C emitted `row_id` now uses:

- `"{split_id}:{row_index_1based}"`

This replaces the prior `source_case_id`-first behavior in Stage C artifact emission only.

Preserved surfaces:

1. `split_id` remains emitted separately;
2. `source_case_id` remains preserved in emitted evidence payloads as provenance;
3. existing Stage C artifact filenames remain unchanged;
4. legacy `summary.json`, `comparison_rows.jsonl`, detector-facing metrics, and failure-profile behavior remain unchanged.

### 2. Validation Coverage

Added test coverage for:

1. unique emitted `row_id` values for Stage C row-fact records;
2. duplicate `source_case_id` rows producing distinct Stage C `row_id` values;
3. exact duplicated rows producing distinct Stage C `row_id` values;
4. repeated emission over the same frozen row set preserving the same `row_id` values;
5. additive artifact behavior and unchanged legacy surfaces after Stage C artifact emission.

## Validation Executed

1. `python -m py_compile scripts/eval_canonical_manifest.py tests/test_eval_canonical_manifest.py` -> pass
2. `pytest -q tests/test_eval_canonical_manifest.py tests/test_stage_c1_evaluator_foundation.py` -> pass (`16 passed`)
3. `python scripts/eval_canonical_manifest.py --manifest evals/canonical_eval_manifest_v1.json --out-dir /tmp/stage_c_package1a_runtime_validation_run --max-samples-per-split 3` -> pass

Runtime-validation details are recorded in:

- `docs/convergence/STAGE_C_PACKAGE_1A_RUNTIME_VALIDATION_REPORT.md`

## Boundary Confirmation

Confirmed unchanged in this slice:

1. detector authority;
2. threshold authority;
3. comparability policy;
4. historical metric identities;
5. legacy detector-facing output shapes;
6. Family B1 and Family B2 ownership behavior outside the row-identity instantiation rule.

## Remaining Known Limitations

1. The canonical corpus still does not ship an explicit dataset-authored `row_id` field; Package 1A instantiates authoritative row identity from split-plus-ordinal under manifest-pinned row-set identity.
2. Stability is defined for repeated evaluation of the same frozen row set. If row ordering changes, row-set identity review remains required.
3. The bounded runtime validation sample exercised only one approved Family A subtype-assignment path because the sampled model outputs were predominantly `invalid_json` or no-call refusals.
