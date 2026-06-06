# CA-03 Compatibility Adoption Merge Readiness And Authorization Review

## Work Package

- ID: `CA-03`
- Title: `Compatibility Adoption Merge Readiness And Authorization Review`
- Repository: `/opt/ai-stack/assistant-training`
- Review branch: `compatibility/ca-02`
- Scope: independent assessment only
- Authority basis:
  - `CA-01 Compatibility Adoption Extraction And Refinement Plan`
  - `CA-02 Compatibility Adoption Implementation Slice`
  - `H-03 Path Decoupling And Compatibility Strategy`
  - `H-05 Compatibility Layer Implementation Plan`
  - merged Wave 1 baseline

## Validation Basis

Independent review re-ran or verified the following on `compatibility/ca-02`:

1. `python -m py_compile ...` -> PASS
2. targeted `pytest` package -> PASS (`72 passed`)
3. resolver validation probe -> PASS
4. fixture-registry validation probe -> PASS
5. `git diff --check` -> PASS
6. direct inspection of `scripts/repo_paths.py`, `tests/test_repo_paths.py`, `tests/test_compatibility_path_resolution.py`, and the modified script/test surfaces
7. direct probe confirming `reports/stage_c8/projection_artifacts` is absent while `validate_role_maps()` still passes the corresponding role

## A. Scope Compliance

CA-02 remained largely inside its authorized slice.

Confirmed:

1. no Wave 2 work
2. no structural migration work
3. no Stage C methodology redesign
4. no root-level `repo_paths.py`
5. no branch restructuring, merge, or push

Observed scope edge:

1. `tests/test_masking_behavior.py` was not part of the original `20`-asset CA-01 inventory
2. however, it is a direct consumer of `scripts/train_lora_sft.py` and would fail after CA-02 unless its script-loading bootstrap was updated
3. treating it as a directly affected consumer is reasonable and does not amount to unauthorized compatibility expansion

Scope conclusion:

- compliant enough for merge review
- no scope blocker identified

## B. Resolver Architecture Review

### Strengths

1. `scripts/repo_paths.py` is appropriately small and script-local.
2. sentinel-based repo-root discovery matches H-05 intent.
3. the role maps cover the active evaluator chain and the three CL-02 core entrypoints without attempting repository-wide generalization.
4. exclusion of the root shim was correct and reduces long-term duplication.
5. Stage C8 now distinguishes provenance metadata references from executable dependency resolution.

### Maintenance Burden

Acceptable but non-zero:

1. static role maps must be maintained when active script or artifact paths move
2. fixture registry metadata is only lightly consumed today, so some fields are presently forward-looking maintenance overhead
3. direct script loading remains part of the operating model, so path roles reduce coupling but do not eliminate loader indirection

### Resolver / Validation Weakness

One concrete weakness prevents unconditional merge authorization:

1. `validate_role_maps()` reports all declared roles as valid even when `artifact:stage_c8_projection_artifacts_dir` resolves to a path that does not exist
2. current evidence:
   - resolved role path: `reports/stage_c8/projection_artifacts`
   - path existence: `False`
   - `validate_role_maps()` result: PASS
3. this happens because optional output artifact roles are treated as valid if their path is absolute and lexically under the repo root, not because the target actually exists or has been meaningfully validated

Assessment:

- the resolver itself is mergeable
- the validation claim is too strong as currently implemented

## C. Test Architecture Review

### Strengths

1. `tests/test_repo_paths.py` covers repo-root discovery, env override behavior, and registry/role validation entrypoints.
2. `tests/test_compatibility_path_resolution.py` codifies the new CL-02 path-handling behavior for dataset build, preflight, and train config resolution.
3. the previously modified evaluator-chain tests now consume scripts and artifacts through the resolver rather than fixed repo-root literals.
4. `tests/test_stage_c8_non_authoritative_detector_projection_adapter.py` now asserts the Stage C8 convergence-document references are treated as repo-root-resolved metadata.

### Weaknesses

1. `tests/test_repo_paths.py` does not detect the optional-output false-positive described above.
2. test bootstrap still depends on injecting `tests/../scripts` into `sys.path`; this is acceptable for the no-shim model but remains a test-only import convention that future work must preserve consciously.
3. the tests protect the bounded CA-02 slice well, but they do not protect the broader historical loader/path-coupled surfaces outside scope.

Assessment:

- sufficient for the adopted slice
- not yet sufficient to justify the current optional-output validation claim

## D. Remaining Coupling Assessment

### Acceptable Residual Coupling

1. test bootstrap through `SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"`
2. direct script loading via `spec_from_file_location(...)` where the loaded path is now role-resolved rather than hard-coded
3. Stage C8 convergence-document references emitted as provenance metadata using `_convergence_metadata_source_paths()`
4. continued in-place use of fixture and sample artifacts under `manifests/reports/` and `reports/stage_c*` pending later migration work

### Concerning Residual Coupling

1. validation overclaim for optional output roles
2. repository-wide historical and legacy path coupling remains extensive outside the adopted slice:
   - `255` absolute repo-root literals across `scripts/` and `tests/`
   - `28` `spec_from_file_location(...)` call sites across `scripts/` and `tests/`

Assessment:

- acceptable residual coupling remains inside the CA-02 slice
- the main concern is validation accuracy, not path-resolution correctness of the adopted code itself

## E. Merge Readiness Determination

Decision: `2. Authorize Merge After Specific Corrections`

Justification:

1. the implementation stayed within its bounded scope
2. the adopted compatibility behavior validated successfully
3. the remaining blocker is narrow and execution-adjacent
4. merge would otherwise bless a validation mechanism that currently marks at least one absent output role as successfully validated

## F. Minimum Required Corrections

Only the following corrections are required before merge authorization:

1. tighten `scripts/repo_paths.py` optional-output role validation so `validate_role_maps()` does not report non-existent output artifact roles as fully validated merely because they are lexically under the repo root
2. add or adjust a targeted test so the chosen optional-output validation rule is explicitly exercised and cannot regress silently
3. rerun the existing CA-02 validation package after that correction and refresh the implementation summary accordingly

No broader redesign is required.
No scope expansion is required.
