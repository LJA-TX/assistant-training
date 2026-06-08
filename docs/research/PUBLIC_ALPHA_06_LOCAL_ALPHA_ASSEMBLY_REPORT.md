# PUBLIC_ALPHA_06_LOCAL_ALPHA_ASSEMBLY_REPORT

## 1. Executive Summary

The local alpha repository candidate was assembled successfully in a temporary review workspace:

- `/opt/ai-stack/local_review_bundles/assistant-training-public-alpha/`

The workspace contains exactly the 57 files defined by `PUBLIC_ALPHA_01`, with no missing paths and no extra paths.

Overall assessment: **yes**, the assembled alpha repository successfully communicates the project's purpose, methodology, and evidence story.

What it does well:

- presents a lean public front door;
- explains the doctrine and current-state boundary clearly;
- exposes a bounded reproducibility contract through scripts, tests, and the pinned eval manifest;
- preserves a concise historical evidence spine without turning the package into an archive.

Residual complexity remains in the preserved historical records, which still reference excluded canonical-only families such as `docs/convergence/`. That is expected for curated history and did not prevent the alpha candidate from being understandable.

## 2. Assembly Actions Performed

The alpha workspace was created outside the canonical repository so the review build would not contaminate the tracked tree.

Assembly actions:

- created a temporary local workspace directory;
- copied the approved Public Core artifacts into the workspace;
- copied the approved Public Supporting artifacts into the workspace;
- copied the approved Curated Historical Evidence artifacts into the workspace;
- validated that the workspace file set matches the approved manifest exactly;
- reviewed the assembled navigation flow from the front door through the evidence spine.

No GitHub repository was created.
No commits were made.
No pushes were made.
No public-repository population occurred.
No accepted alpha baseline files were modified.

## 3. Included Artifacts

The assembled workspace includes the exact manifest-driven set of 57 files:

### Public Core

The root front door, doctrine, current-state guidance, pinned evaluation contract, and repository metadata:

- `README.md`
- `AGENTS.md`
- `pyproject.toml`
- `.gitignore`
- `repo_paths.py`
- `evals/canonical_eval_manifest_v1.json`
- `docs/goal_charter_v5a.md`
- `docs/appendix_a_operational_execution_contract_v3a.md`
- `docs/metric_specification_v1a.md`
- `docs/current/start_here.md`
- `docs/current/current_status.md`
- `docs/current/framework_vs_history.md`
- `docs/current/housekeeping_status.md`

### Public Supporting

The reusable scripts, tests, and process-infrastructure docs selected by the alpha manifest:

- `scripts/repo_paths.py`
- `scripts/build_dataset_v1.py`
- `scripts/preflight_lora_run.py`
- `scripts/train_lora_sft.py`
- `scripts/eval_canonical_manifest.py`
- `scripts/eval_adapter_toolcalls.py`
- `scripts/post_eval_collapse_detector.py`
- `scripts/stage_c1_evaluator_foundation.py`
- `tests/test_dataset_contract.py`
- `tests/test_masking_behavior.py`
- `tests/test_eval_canonical_manifest.py`
- `tests/test_eval_adapter_toolcalls.py`
- `tests/test_repo_paths.py`
- `tests/test_compatibility_path_resolution.py`
- `tests/test_stage_c1_evaluator_foundation.py`
- `docs/framework/process_infrastructure/checklists/*.md` selected by the manifest
- `docs/framework/process_infrastructure/templates/*.md` selected by the manifest

### Curated Historical Evidence

The bounded evidence spine and its follow-on context:

- `docs/framework/lineages/README.md`
- `docs/framework/lineages/i2_contamination_event.md`
- `docs/framework/lineages/i4_i5_overconstraint_collapse.md`
- `docs/framework/lineages/i6_isolated_variable_pivot.md`
- `docs/framework/lineages/i7_coupled_schema_dynamics.md`
- `docs/framework/lineages/i8_pre_training_governance_snapshot.md`
- `docs/framework/methodology/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md`
- `docs/framework/methodology/STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md`
- `docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md`
- `docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md`
- `docs/housekeeping/OSS_01_INDEPENDENT_REVIEW_AND_RECONCILIATION_GROK.md`
- `docs/housekeeping/OSS_05_PUBLIC_FRONT_DOOR_IMPLEMENTATION_SUMMARY.md`

## 4. Excluded Artifacts

The following families were intentionally left out of the assembled workspace:

- `docs/convergence/`
- `docs/continuity/`
- `docs/deprecated/`
- `docs/research/`
- `data/`
- `evals/data/`
- `evals/runs/`
- `reports/`
- `manifests/`
- `configs/`
- `artifacts/`
- `local_review_bundles/`

Also excluded were the canonical-only individual docs named in `PUBLIC_ALPHA_01`, including the lineage notes and methodology records that were explicitly marked canonical-only.

Notably excluded from the alpha workspace:

- `docs/research/PUBLIC_ALPHA_04_EXECUTION_REPORT.md`
- `docs/research/PUBLIC_ALPHA_05_ALPHA_ASSEMBLY_VALIDATION.md`

Those remain canonical-repository process artifacts and were not part of the assembled public candidate.

## 5. Transformations Applied

The workspace was assembled from the post-preparation canonical tree, so most approved transformations were already present before copy time.

Applied by assembly:

- copied the accepted prepared versions of the public front door, doctrine, manifest, and current-state documents;
- copied the accepted prepared scripts and tests;
- copied the accepted curated evidence documents;
- copied the selected process-infrastructure checklists and templates exactly as accepted;
- preserved the bounded evidence model without adding archive-like surfaces.

No additional transformation was introduced during assembly beyond manifest-driven copying.

## 6. Navigation Assessment

### First-Time Visitor

The flow is understandable.

Recommended path:

1. `README.md`
2. `docs/current/start_here.md`
3. `docs/current/current_status.md`
4. `docs/current/framework_vs_history.md`
5. `docs/framework/lineages/README.md`
6. `docs/goal_charter_v5a.md`
7. `docs/appendix_a_operational_execution_contract_v3a.md`

This gives a new reader the project purpose, the present boundary, and the evidence spine without forcing archive traversal.

### Technical Reviewer

The technical path is also coherent:

- doctrine surfaces explain the regimen and its evaluation contract;
- `evals/canonical_eval_manifest_v1.json` pins the reproducibility contract;
- scripts and tests are visible and inspectable;
- curated historical evidence shows why the current boundary exists.

### Codex-for-OSS Reviewer

The assembled candidate reads as deliberate maintenance rather than opportunistic accumulation.

The reviewer can see:

- authority and boundary control;
- reproducibility and validation surfaces;
- a bounded historical spine;
- a curated package instead of a canonical dump.

### Navigation Gaps

No blocking navigation gaps were found.

Minor rough edge:

- some historical evidence records still contain absolute links to excluded canonical-only material, which is acceptable for preserved history but slightly noisier than the current front door surfaces.

## 7. Alpha Statistics

Measured workspace statistics:

- file count: 57
- directory count: 15
- evidence-artifact count: 12

Comparison against `PUBLIC_ALPHA_01`:

- file set: exact match
- evidence count: exact match
- boundedness: consistent with the lean alpha objective

## 8. Assembly Findings

### Missing Context

No major missing context was identified.

### Documentation Gaps

No blocking documentation gaps were found.

### Navigation Gaps

None blocking.

### Unexpected Complexity

Low.

The only meaningful complexity is the intentional residue of historical links inside preserved evidence documents. Those links point at excluded canonical-only families, but they remain confined to historical records rather than public-core surfaces.

### Assembly Surprises

None that change the readiness judgment.

The workspace was straightforward to assemble once the manifest boundary had been accepted.

## 9. Reviewer Experience Assessment

The assembled alpha repository is readable and purposeful.

What a reviewer sees:

- a concise public front door;
- a clear statement of purpose and boundary;
- a reproducibility contract via scripts, tests, and pinned eval manifest;
- a curated evidence spine that explains the method's evolution;
- no bulk archive noise.

Verdict:

- the assembled alpha repository successfully communicates the project's purpose, methodology, and evidence story.

## 10. Final Recommendation

Keep the assembled workspace as the local review candidate for further inspection.

No additional assembly changes are required before human review.

If a later phase wants to reduce residual historical-link noise, it should do so as an explicit archival-hygiene pass rather than as part of alpha assembly.
