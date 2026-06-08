# PUBLIC_ALPHA_03_ALPHA_PREPARATION_REMEDIATION_PLAN

Assessment and documentation creation authorized.

This document converts the accepted `PUBLIC_ALPHA_02` preparation assessment into an executable remediation plan for the alpha-preparation phase.
It does not implement remediation.
It does not assemble the alpha repository.
It does not widen the alpha scope.

## 1. Executive Summary

`PUBLIC_ALPHA_02` established that the alpha candidate is **ready after preparation** rather than ready as-is.

The remaining work is narrow and operational:

- rewrite the public front door and current-state docs so they speak only to the accepted alpha surface;
- normalize the doctrine and eval manifest path contract so they do not leak canonical-only or machine-specific assumptions;
- align the evidence-spine index to the accepted curated history set;
- decouple the stage-C evaluator and its path-sensitive tests from excluded fixture/report surfaces;
- then run targeted validation before any alpha assembly step is authorized.

This plan groups that work into packages, identifies dependencies, and defines exit criteria for the preparation phase.

Readiness outcome:

- **PUBLIC_ALPHA_03:** preparation plan
- **PUBLIC_ALPHA_04:** remediation execution boundary
- **Alpha assembly:** after preparation only

## 2. Work Package Structure

| Work package | Purpose | Primary files | Dependency notes |
| --- | --- | --- | --- |
| Front Door Package | Rewrite the public entry path and current-state navigation so the alpha package reads cleanly on its own. | `README.md`, `docs/current/start_here.md`, `docs/current/current_status.md`, `docs/current/framework_vs_history.md`, `docs/current/housekeeping_status.md` | Depends on the final alpha surface inventory and the accepted evidence-spine order. |
| Doctrine and Manifest Normalization Package | Remove machine-specific or private-path assumptions from the public policy and pinned eval contract. | `docs/goal_charter_v5a.md`, `docs/appendix_a_operational_execution_contract_v3a.md`, `evals/canonical_eval_manifest_v1.json` | Critical path for all path-sensitive test and manifest work. |
| Evidence Spine Package | Reconcile the lineage index with the accepted curated evidence set. | `docs/framework/lineages/README.md` | Mostly independent, but its ordering must match the accepted 12-artifact spine. |
| Test and Evaluator Decoupling Package | Remove external runtime and excluded-surface coupling from the evaluator foundation and path-sensitive tests. | `scripts/stage_c1_evaluator_foundation.py`, `tests/test_dataset_contract.py`, `tests/test_eval_canonical_manifest.py`, `tests/test_eval_adapter_toolcalls.py`, `tests/test_repo_paths.py`, `tests/test_stage_c1_evaluator_foundation.py` | The main critical path. This package should be completed before final validation. |
| Support Revalidation Package | Re-run and confirm the supporting scripts/tests that should remain unchanged after the path-sensitive edits. | `scripts/build_dataset_v1.py`, `scripts/preflight_lora_run.py`, `scripts/train_lora_sft.py`, `scripts/eval_canonical_manifest.py`, `tests/test_compatibility_path_resolution.py` | Can proceed after the manifest and evaluator changes are settled. |
| Baseline Preservation Package | Confirm that stable support files, process assets, and the curated evidence set remain unchanged. | `AGENTS.md`, `pyproject.toml`, `.gitignore`, `repo_paths.py`, `scripts/repo_paths.py`, `scripts/eval_adapter_toolcalls.py`, `scripts/post_eval_collapse_detector.py`, `tests/test_masking_behavior.py`, process-infrastructure checklists/templates, selected evidence artifacts, `docs/metric_specification_v1a.md`, `docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md`, `docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md` | Verification only; no content changes expected. |

## 3. Dependency Analysis

### Work packages that can proceed independently

- `Evidence Spine Package` can proceed in parallel with the front-door rewrite, provided the accepted spine order remains fixed.
- `Baseline Preservation Package` is verification only and can be checked throughout the remediation pass.
- `Support Revalidation Package` can start once the direct remediation files it depends on are updated.

### Work packages with sequencing constraints

- `Doctrine and Manifest Normalization Package` should complete before the path-sensitive tests are finalized.
- `Test and Evaluator Decoupling Package` depends on the manifest and doctrine normalization because those files define the public contract the tests should enforce.
- `Front Door Package` should follow the accepted alpha surface list so the navigation text does not need repeated edits.

### Critical path

1. Normalize `evals/canonical_eval_manifest_v1.json`.
2. Decouple `scripts/stage_c1_evaluator_foundation.py` and the path-sensitive tests.
3. Rewrite the front door and current-state docs against the accepted alpha boundary.
4. Reconcile `docs/framework/lineages/README.md` with the accepted evidence spine.
5. Run the full alpha-preparation validation set.

If any of the first two steps are incomplete, alpha assembly will remain brittle or internally inconsistent.

## 4. File-Level Remediation Plan

### A. Direct remediation files

| Path | Work package | Required action | Complexity | Validation required | Completion criteria |
| --- | --- | --- | --- | --- | --- |
| `README.md` | Front Door Package | Rewrite the front door so it points only at the alpha-approved surface set and no longer advertises excluded canonical-only surfaces. | Medium | `git diff --check`; path grep for excluded families; manual reading-path review. | The README explains the curated/public boundary, the reader path, and the alpha evidence spine without canonical-only leakage. |
| `docs/goal_charter_v5a.md` | Doctrine and Manifest Normalization Package | Normalize machine-specific and private-path references. | Medium | `git diff --check`; grep for `/opt/ai-stack`, `/mnt/mirrors`, and private-repo path literals. | No public-facing path literal remains unless it is explicitly marked as canonical/private provenance. |
| `docs/appendix_a_operational_execution_contract_v3a.md` | Doctrine and Manifest Normalization Package | Normalize pinned references and remove or fence private/local path assumptions. | Medium | `git diff --check`; grep for path literals and excluded family references. | The contract can be read in the alpha repository without implying a local deployment location. |
| `evals/canonical_eval_manifest_v1.json` | Doctrine and Manifest Normalization Package | Convert the manifest into a public-alpha-safe contract or fence unresolved paths explicitly. | High | `jq .`; `git diff --check`; grep for absolute paths and excluded surface names. | The manifest is valid JSON, no longer leaks private/local paths, and no longer implies that excluded data/report surfaces are part of the assembled package. |
| `docs/current/start_here.md` | Front Door Package | Rewrite the navigation path so it only leads through alpha-approved files. | Medium | `git diff --check`; manual path walk from README to evidence spine. | The reader journey stays entirely inside the accepted alpha boundary. |
| `docs/current/current_status.md` | Front Door Package | Replace closure references and boundary language with the accepted alpha baseline. | Medium | `git diff --check`; grep for closure-only artifacts and excluded families. | The status summary reflects the accepted alpha package and no longer depends on missing closure docs. |
| `docs/current/framework_vs_history.md` | Front Door Package | Prune excluded-family references and restate the history/current split around the accepted public package. | Medium | `git diff --check`; grep for `docs/convergence/`, `docs/continuity/`, `docs/deprecated/`, `data/`, `reports/`, `manifests/`. | The page explains the current method versus curated history without enumerating excluded surfaces as public navigation. |
| `docs/current/housekeeping_status.md` | Front Door Package | Remove closure-report references and align the housekeeping narrative to the accepted alpha boundary. | Medium | `git diff --check`; grep for missing closure-only document names. | The page can be read without requiring non-alpha artifacts. |
| `docs/framework/lineages/README.md` | Evidence Spine Package | Rewrite the index so it reflects the accepted curated evidence spine and reading order. | High | `git diff --check`; verify the listed evidence set matches the accepted 12-artifact spine. | The index points to the correct bounded spine and does not imply an archive. |
| `scripts/stage_c1_evaluator_foundation.py` | Test and Evaluator Decoupling Package | Decouple the evaluator foundation from the WP8 fixture corpus and excluded report surfaces. | High | Targeted test run plus path grep for excluded fixture/report roots. | The evaluator no longer depends on excluded WP8 fixture surfaces. |
| `tests/test_dataset_contract.py` | Test and Evaluator Decoupling Package | Replace the external runtime checkout path with repo-root-relative or helper-driven resolution. | High | Targeted test run; grep for `/opt/ai-stack/runtimes/assistant-runtime`. | The test no longer reaches outside the repository. |
| `tests/test_eval_canonical_manifest.py` | Test and Evaluator Decoupling Package | Remove the dependency on excluded `manifests/` and `reports/` artifacts. | High | Targeted test run; grep for excluded manifest/report fixture names. | The test validates the public-alpha manifest without needing excluded surfaces. |
| `tests/test_eval_adapter_toolcalls.py` | Test and Evaluator Decoupling Package | Replace the hardcoded repository path with repo-root resolution. | Low | Targeted test run; grep for absolute checkout paths. | The test resolves paths portably and no longer depends on the current checkout location. |
| `tests/test_repo_paths.py` | Test and Evaluator Decoupling Package | Narrow expectations to alpha-scoped roles only. | High | Targeted test run; review expected role set. | The registry test no longer expects excluded fixture or sample-output roles. |
| `tests/test_stage_c1_evaluator_foundation.py` | Test and Evaluator Decoupling Package | Repoint the test away from excluded WP8 fixture surfaces. | High | Targeted test run; grep for WP8 fixture root references. | The test covers the evaluator foundation without relying on excluded fixtures. |

### B. Verification-only follow-up files

These files are not expected to need content edits, but they must be re-validated after the direct remediation files change.

| Path | Work package | Required action | Complexity | Validation required | Completion criteria |
| --- | --- | --- | --- | --- | --- |
| `scripts/build_dataset_v1.py` | Support Revalidation Package | Verify that defaults still match the final alpha manifest and repo-root layout. | Low | Targeted smoke check after manifest normalization. | No new path or boundary defect appears after the surrounding edits. |
| `scripts/preflight_lora_run.py` | Support Revalidation Package | Verify that preflight assumptions still match the final alpha boundary. | Low | Targeted smoke check after the surrounding edits. | The script remains alpha-compatible without further edits. |
| `scripts/train_lora_sft.py` | Support Revalidation Package | Verify that training entry-point assumptions still match the final alpha boundary. | Low | Targeted smoke check after the surrounding edits. | The script remains alpha-compatible without further edits. |
| `scripts/eval_canonical_manifest.py` | Support Revalidation Package | Verify the runner still matches the normalized manifest contract. | Low | Targeted smoke check after the manifest change. | The runner and manifest remain consistent. |
| `tests/test_compatibility_path_resolution.py` | Support Revalidation Package | Re-run after the path-sensitive edits to confirm no regression. | Low | Targeted test run after the surrounding edits. | Path resolution remains stable after normalization. |

### C. Baseline preservation inventory

These files are expected to remain unchanged. They still require a final spot check after the remediation pass so that the alpha package stays clean and bounded.

| Path set | Required action | Validation required | Completion criteria |
| --- | --- | --- | --- |
| `AGENTS.md`, `pyproject.toml`, `.gitignore`, `repo_paths.py`, `scripts/repo_paths.py`, `scripts/eval_adapter_toolcalls.py`, `scripts/post_eval_collapse_detector.py`, `tests/test_masking_behavior.py`, `docs/metric_specification_v1a.md` | Preserve unchanged. | Spot-check for accidental edits and confirm no new path leakage was introduced by the surrounding work. | The files remain byte-for-byte unchanged or otherwise still conform to the accepted alpha baseline. |
| `docs/framework/process_infrastructure/checklists/git_ignore_verification_checklist.md`, `docs/framework/process_infrastructure/checklists/governance_boundary_verification_checklist.md`, `docs/framework/process_infrastructure/checklists/hygiene_review_checklist.md`, `docs/framework/process_infrastructure/checklists/publication_readiness_checklist.md`, `docs/framework/process_infrastructure/checklists/push_readiness_checklist.md`, `docs/framework/process_infrastructure/checklists/review_package_completeness_checklist.md`, `docs/framework/process_infrastructure/checklists/validation_evidence_checklist.md`, `docs/framework/process_infrastructure/checklists/zip_workflow_checklist.md` | Preserve unchanged. | Spot-check that they still provide reusable process guidance and do not contain alpha-specific leakage. | The process checklist set remains reusable without modification. |
| `docs/framework/process_infrastructure/templates/closure_determination_template.md`, `docs/framework/process_infrastructure/templates/conformance_report_template.md`, `docs/framework/process_infrastructure/templates/coverage_summary_template.md`, `docs/framework/process_infrastructure/templates/implementation_summary_template.md`, `docs/framework/process_infrastructure/templates/milestone_determination_template.md`, `docs/framework/process_infrastructure/templates/package_review_template.md`, `docs/framework/process_infrastructure/templates/readiness_determination_template.md`, `docs/framework/process_infrastructure/templates/reconciliation_summary_template.md`, `docs/framework/process_infrastructure/templates/transition_readiness_assessment_template.md` | Preserve unchanged. | Spot-check that they still provide reusable process templates and do not contain alpha-specific leakage. | The template set remains reusable without modification. |
| `docs/framework/lineages/i2_contamination_event.md`, `docs/framework/lineages/i4_i5_overconstraint_collapse.md`, `docs/framework/lineages/i6_isolated_variable_pivot.md`, `docs/framework/lineages/i7_coupled_schema_dynamics.md`, `docs/framework/lineages/i8_pre_training_governance_snapshot.md`, `docs/framework/methodology/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md`, `docs/framework/methodology/STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md`, `docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md`, `docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md`, `docs/housekeeping/OSS_01_INDEPENDENT_REVIEW_AND_RECONCILIATION_GROK.md`, `docs/housekeeping/OSS_05_PUBLIC_FRONT_DOOR_IMPLEMENTATION_SUMMARY.md` | Preserve unchanged. | Spot-check that the accepted evidence spine still matches the curated history story. | The selected curated evidence artifacts remain unchanged and in scope. |

## 5. Validation Strategy

### Documentation validation

Run after the front-door and doctrine updates:

- `git diff --check`
- targeted path greps for:
  - `/opt/ai-stack`
  - `/mnt/mirrors`
  - `docs/convergence/`
  - `docs/continuity/`
  - `docs/deprecated/`
  - `data/`
  - `evals/data/`
  - `evals/runs/`
  - `reports/`
  - `manifests/`
  - `local_review_bundles/`

The documentation pass is complete only when the public-facing docs read cleanly and no longer imply that excluded surfaces are part of the alpha package.

### Path-hygiene validation

Run after manifest and evaluator changes:

- `jq . evals/canonical_eval_manifest_v1.json`
- targeted greps for hardcoded checkout paths
- targeted greps for excluded fixture/report roots

The path-hygiene pass is complete only when the manifest and path-sensitive code no longer pin the public alpha to a local machine layout.

### Test validation

Run after the evaluator and test changes:

- `pytest tests/test_dataset_contract.py`
- `pytest tests/test_eval_canonical_manifest.py`
- `pytest tests/test_eval_adapter_toolcalls.py`
- `pytest tests/test_repo_paths.py`
- `pytest tests/test_stage_c1_evaluator_foundation.py`
- `pytest tests/test_compatibility_path_resolution.py`
- `pytest tests/test_masking_behavior.py`

The test pass is complete only when the path-sensitive tests pass without relying on excluded surfaces.

### Alpha-boundary validation

Run after all edits:

- confirm that the accepted alpha package still matches `PUBLIC_ALPHA_01`
- confirm that no excluded canonical-only family has been imported into the alpha set
- confirm that the curated evidence set remains bounded and still reads as a spine rather than an archive

## 6. Execution Sequence

Recommended order:

1. Normalize `docs/goal_charter_v5a.md`, `docs/appendix_a_operational_execution_contract_v3a.md`, and `evals/canonical_eval_manifest_v1.json`.
2. Rewrite `README.md` and the current-state docs to match the accepted alpha boundary.
3. Rewrite `docs/framework/lineages/README.md` so the evidence spine matches the accepted curated set.
4. Decouple `scripts/stage_c1_evaluator_foundation.py` and the path-sensitive tests.
5. Re-run the support scripts/tests that should remain unchanged.
6. Spot-check the baseline preservation inventory and the curated evidence set.
7. Run the full validation strategy and confirm the alpha package is internally consistent.

This sequence minimizes rework because it resolves the contract and path issues before the surrounding narrative and test confirmations.

## 7. Alpha-Preparation Exit Criteria

`PUBLIC_ALPHA_04` may begin only when all of the following are true:

1. The direct remediation files are updated and reviewed.
2. The manifest is valid JSON and no longer leaks private/local path assumptions.
3. The front-door and current-state docs point only to the accepted alpha package.
4. The lineage index matches the accepted evidence spine.
5. The path-sensitive tests pass without relying on excluded fixtures or external runtime checkouts.
6. `git diff --check` passes.
7. The baseline preservation inventory remains unchanged.
8. No new files, scope expansions, or assembly steps were introduced during remediation.

## 8. Residual Risk Assessment

### High risk

- Hidden path literals could remain in the manifest or evaluator if the remediation is partial.
- `scripts/stage_c1_evaluator_foundation.py` could still carry an implicit fixture dependency if the decoupling is only superficial.
- `tests/test_repo_paths.py` could still encode excluded roles if the role set is not narrowed carefully.

### Medium risk

- The front-door rewrite could drift away from the actual alpha surface if the surrounding docs are edited independently.
- The evidence spine could become over- or under-described if the index changes without the reading path being updated.
- The support scripts may require a second review pass after the manifest normalization settles.

### Low risk

- The unchanged support files could pick up incidental edits during the remediation pass.
- The curated evidence set could be misread as archival if the index wording is not explicit enough.

## 9. Final Recommendation

Proceed with the preparation plan in the sequence above.

Treat the manifest, evaluator, and path-sensitive test work as the critical path.
Treat the front-door rewrite and evidence-spine alignment as the reader-facing cleanup that confirms the public alpha boundary.
Treat the remaining support files as verification-only guards.

If the exit criteria are satisfied, `PUBLIC_ALPHA_04` can authorize preparation execution and the alpha repository candidate can then be assembled from the accepted baseline.
