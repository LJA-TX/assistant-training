# CA-02 Compatibility Adoption Implementation Slice

## Work Package

- ID: `CA-02`
- Title: `Compatibility Adoption Implementation Slice`
- Repository: `/opt/ai-stack/assistant-training`
- Branch: `compatibility/ca-02`
- Scope: approved CL-01 / CL-02 compatibility adoption only
- Authority basis:
  - `CA-01 Compatibility Adoption Extraction And Refinement Plan`
  - `H-03 Path Decoupling And Compatibility Strategy`
  - `H-05 Compatibility Layer Implementation Plan`
  - merged Wave 1 baseline on `main`

## A. Implementation Summary

Implemented compatibility adoption on a clean branch from the merged Wave 1 baseline.

Adopted script assets:

1. `scripts/repo_paths.py`
2. `scripts/eval_canonical_manifest.py`
3. `scripts/stage_c1_evaluator_foundation.py`
4. `scripts/stage_c3_evaluator_runtime_integration.py`
5. `scripts/stage_c4_real_output_ingestion.py`
6. `scripts/stage_c5_scoring_path_integration.py`
7. `scripts/stage_c6_scoring_report_integration.py`
8. `scripts/stage_c8_non_authoritative_detector_projection_adapter.py`
9. `scripts/train_lora_sft.py`
10. `scripts/preflight_lora_run.py`
11. `scripts/build_dataset_v1.py`

Adopted and directly affected tests:

1. `tests/test_eval_canonical_manifest.py`
2. `tests/test_stage_c1_evaluator_foundation.py`
3. `tests/test_stage_c2_family_state_reconciliation_foundation.py`
4. `tests/test_stage_c3_evaluator_runtime_integration.py`
5. `tests/test_stage_c4_real_output_ingestion.py`
6. `tests/test_stage_c5_scoring_path_integration.py`
7. `tests/test_stage_c6_scoring_report_integration.py`
8. `tests/test_stage_c8_non_authoritative_detector_projection_adapter.py`
9. `tests/test_masking_behavior.py`
10. `tests/test_repo_paths.py`
11. `tests/test_compatibility_path_resolution.py`

Applied CA-01 refinements:

1. excluded root-level `repo_paths.py`
2. tightened `scripts/repo_paths.py` to the active resolver and registry surface
3. added explicit role-map validation and fixture-registry validation
4. converted `build_dataset_v1.py` defaults to lazy repo-root resolution
5. made `preflight_lora_run.py` repo-root-relative semantics explicit for manifest and config paths
6. made `train_lora_sft.py` config-path resolution repo-root-relative for relative CLI values
7. classified Stage C8 convergence-document references as provenance metadata through `_convergence_metadata_source_paths()`
8. codified resolver and entrypoint path-regression coverage in dedicated tests

## B. Validation Results

Validation executed on `compatibility/ca-02`:

1. `python -m py_compile scripts/repo_paths.py ... tests/test_masking_behavior.py` -> PASS
2. `pytest -q tests/test_repo_paths.py tests/test_compatibility_path_resolution.py tests/test_eval_canonical_manifest.py tests/test_stage_c1_evaluator_foundation.py tests/test_stage_c2_family_state_reconciliation_foundation.py tests/test_stage_c3_evaluator_runtime_integration.py tests/test_stage_c4_real_output_ingestion.py tests/test_stage_c5_scoring_path_integration.py tests/test_stage_c6_scoring_report_integration.py tests/test_stage_c8_non_authoritative_detector_projection_adapter.py tests/test_masking_behavior.py` -> PASS (`72 passed`)
3. resolver validation -> PASS
   - `repo_root=/opt/ai-stack/assistant-training-ca-02`
4. role-map validation -> PASS
   - `role_count=20`
5. fixture-registry validation -> PASS
   - `registry_count=5`
6. targeted compatibility scan over the adopted slice -> PASS
   - no remaining absolute `/opt/ai-stack/assistant-training/...` literals in the adopted script surface
7. `git diff --check` -> PASS

## C. Remaining Coupling Assessment

Remaining coupling after CA-02 is limited but not eliminated.

Inside the adopted slice:

1. test bootstrap still uses `Path(__file__).resolve().parents[1] / "scripts"` in the updated tests so direct script loading can import `scripts/repo_paths.py` without a root shim
2. `tests/test_masking_behavior.py` still loads `train_lora_sft.py` by direct file path, but it is now repo-relative rather than hard-coded to `/opt/ai-stack/assistant-training/...`
3. Stage C8 still records convergence-document references in emitted metadata, but those references are now explicitly provenance metadata and resolved from the live repo root rather than fixed repo-root literals

Outside the adopted slice:

1. repository-wide `scripts/` and `tests/` still contain `255` absolute `/opt/ai-stack/assistant-training/...` literals
2. repository-wide `scripts/` and `tests/` still contain `28` `spec_from_file_location(...)` call sites
3. the remaining path-coupled surfaces are predominantly historical Stage B recovery builders, validators, legacy Stage C packages, and tests outside the CA-02 scope

## D. Readiness Assessment

CA-02 is ready for merge review.

Why:

1. the approved compatibility surface was adopted onto the merged Wave 1 baseline without bringing forward raw `housekeeping/w1-execution` branch clutter
2. the root shim was excluded as directed
3. the required refinements were implemented
4. bounded validation passed cleanly
5. the remaining coupling is known and mostly outside the adopted slice

Known review focus areas:

1. whether the test bootstrap pattern using `SCRIPTS_DIR` is the preferred long-term no-shim import model
2. whether any future compatibility wave should package the resolver more formally rather than continuing direct script loading
3. whether the broader historical path-coupled surfaces should be left in place or addressed in a later compatibility or migration phase
