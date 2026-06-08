# PUBLIC_ALPHA_04_EXECUTION_REPORT

Implementation authorized within the accepted `PUBLIC_ALPHA_03` remediation boundary.

This report records the preparation work performed to make the accepted alpha artifacts suitable for later assembly.
It does not assemble the alpha repository.
It does not publish anything.

## 1. Executive Summary

The alpha-preparation remediation pass is complete for the authorized scope.

The public front door, current-state guidance, doctrine, pinned manifest, lineage index, and evaluator/test surfaces were normalized so they now read as a coherent alpha package rather than a machine-specific or canonical-only working tree.

Validation passed:

- documentation hygiene checks passed
- path-hygiene checks on the modified surfaces passed
- targeted tests passed

Readiness outcome:

- **Ready for Alpha Assembly Validation**

## 2. Files Modified

### Front Door and Current-State Surfaces

- `README.md`
- `docs/current/start_here.md`
- `docs/current/current_status.md`
- `docs/current/framework_vs_history.md`
- `docs/current/housekeeping_status.md`

### Doctrine and Manifest Surfaces

- `docs/goal_charter_v5a.md`
- `docs/appendix_a_operational_execution_contract_v3a.md`
- `evals/canonical_eval_manifest_v1.json`

### Evidence-Spine Index

- `docs/framework/lineages/README.md`

### Evaluator and Test Decoupling Surfaces

- `scripts/stage_c1_evaluator_foundation.py`
- `tests/test_dataset_contract.py`
- `tests/test_eval_canonical_manifest.py`
- `tests/test_eval_adapter_toolcalls.py`
- `tests/test_repo_paths.py`
- `tests/test_stage_c1_evaluator_foundation.py`

### Preservation Report

- `docs/research/PUBLIC_ALPHA_04_EXECUTION_REPORT.md`

## 3. Remediation Performed

- Rewrote the public front door and current-state pages to point only at the accepted alpha surfaces and to stop advertising excluded archive-like families.
- Normalized the doctrine and execution-contract language so it uses repository-relative or logical references rather than machine-specific paths.
- Rebased the canonical evaluation manifest onto repo-relative and logical references for the runtime, tokenizer, datasets, scripts, and environment artifacts.
- Replaced the lineage index with the accepted curated spine and its follow-on context.
- Decoupled the Stage C1 evaluator default from the WP8 fixture corpus by making the default a repo-local placeholder path.
- Reworked the dataset, manifest, repo-path, and Stage C1 tests so they use self-contained temporary inputs and alpha-scoped role checks instead of external runtime checkouts or excluded report fixtures.

## 4. Validation Results

### Documentation Hygiene

- `git diff --check`: PASS

### Path Hygiene

- Targeted grep over the modified surfaces for absolute machine paths and excluded-family references: PASS

### Targeted Tests

Command:

```bash
pytest tests/test_dataset_contract.py tests/test_eval_canonical_manifest.py tests/test_eval_adapter_toolcalls.py tests/test_repo_paths.py tests/test_stage_c1_evaluator_foundation.py tests/test_compatibility_path_resolution.py tests/test_masking_behavior.py
```

Result:

- PASS, 40 passed

### Staging Note

- The remediation package is intended to be staged as a single preservation set after this report is written.
- No commit and no push were performed.

## 5. Remaining Issues

No blocking issues remain within the authorized remediation boundary.

One legacy roadmap record outside the remediation set still contains historical absolute links to convergence-era documents:

- `docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md`

That file was inspected but not modified because it was not included in the approved `PUBLIC_ALPHA_04` edit set.

## 6. Assembly Readiness Assessment

**Ready for Alpha Assembly Validation**

Rationale:

- the authorized alpha-preparation surfaces now read consistently as a curated package
- the manifest and path-sensitive code no longer depend on machine-specific absolute paths
- the evaluator and tests now run against self-contained or repo-root-relative inputs
- the targeted validation suite passed

## 7. Recommended Next Boundary

Proceed to **Alpha Assembly Validation**.

The next step is not a wider redesign.
It is the final review that confirms the accepted `PUBLIC_ALPHA_01` baseline can be assembled into the local alpha candidate without widening scope.
