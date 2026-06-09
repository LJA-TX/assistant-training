# PUBLIC_ALPHA_02_ALPHA_ASSEMBLY_PREPARATION_ASSESSMENT

Assessment and documentation creation authorized.

This document identifies the preparation work required before a local alpha repository candidate can be assembled from the accepted `PUBLIC_ALPHA_01` baseline.
It does not assemble the repository.
It does not implement changes.

## 1. Executive Summary

`PUBLIC_ALPHA_01` is a valid assembly baseline, but it is not yet ready to be assembled as-is.

The main reason is not missing architecture.
The remaining work is preparation:

- several public-facing docs still reference canonical-only families or machine-specific paths,
- the canonical eval manifest still pins private/local locations,
- the lineage index still reflects an older evidence set shape,
- and a small but important cluster of scripts and tests still depend on excluded fixture/report surfaces or external runtime paths.

The alpha package therefore needs a preparation pass before assembly execution:

1. rewrite the public front door and current-state docs,
2. normalize the doctrine and eval manifest path references,
3. reconcile the evidence spine index with the accepted alpha evidence set,
4. decouple the stage-C evaluator and its tests from excluded fixture/report surfaces,
5. then validate the alpha candidate before any assembly or publication step.

Readiness outcome:

- **Assembly now:** no
- **Assembly after preparation:** yes

## 2. Inclusion Review

### Public Core

| Artifact | PUBLIC_ALPHA_01 classification | Preparation classification | Rationale |
|---|---|---|---|
| `README.md` | Public Core | Include with major adaptation | The front door still speaks from the canonical/private baseline and points at surfaces excluded from the alpha package. It needs a public-alpha rewrite. |
| `AGENTS.md` | Public Core | Include unchanged | Thin dispatcher, authority order, and route map. No alpha-specific rewrite is required. |
| `pyproject.toml` | Public Core | Include unchanged | Packaging metadata only. |
| `.gitignore` | Public Core | Include unchanged | Hygiene metadata only. |
| `repo_paths.py` | Public Core | Include unchanged | Compatibility shim; no machine-specific path literals. |
| `evals/canonical_eval_manifest_v1.json` | Public Core | Include with major adaptation | The manifest still pins absolute local paths and references excluded data/report surfaces. It needs path normalization or a public-alpha equivalent contract. |
| `docs/goal_charter_v5a.md` | Public Core | Include with major adaptation | Contains machine-specific mirror/runtime paths and private-repo references that are not public-alpha friendly. |
| `docs/appendix_a_operational_execution_contract_v3a.md` | Public Core | Include with major adaptation | Same issue set as the charter, plus pinned manifest/path references that need public-alpha cleanup. |
| `docs/metric_specification_v1a.md` | Public Core | Include unchanged | Compact scoring semantics; no alpha boundary issue. |
| `docs/current/start_here.md` | Public Core | Include with major adaptation | The reading path still points into the canonical repository’s broader historical surface set; it needs alpha-specific navigation. |
| `docs/current/current_status.md` | Public Core | Include with major adaptation | References closure artifacts and current-boundary statements that are not aligned to the alpha package boundary. |
| `docs/current/framework_vs_history.md` | Public Core | Include with major adaptation | Still enumerates excluded families and mixed surfaces; needs pruning to the alpha boundary. |
| `docs/current/housekeeping_status.md` | Public Core | Include with major adaptation | Still references closure reports and structural state not present in the alpha package. |

### Public Supporting

| Artifact | PUBLIC_ALPHA_01 classification | Preparation classification | Rationale |
|---|---|---|---|
| `scripts/repo_paths.py` | Public Supporting | Include unchanged | Shared resolver and role map. |
| `scripts/build_dataset_v1.py` | Public Supporting | Include unchanged | No direct machine-specific path literal issue in the script body. |
| `scripts/preflight_lora_run.py` | Public Supporting | Include unchanged | Path handling is already repo-root-driven. |
| `scripts/train_lora_sft.py` | Public Supporting | Include unchanged | Same. |
| `scripts/eval_canonical_manifest.py` | Public Supporting | Include unchanged | Depends on the manifest, but does not itself hardcode the blocked paths. |
| `scripts/eval_adapter_toolcalls.py` | Public Supporting | Include unchanged | Useful legacy comparison surface. |
| `scripts/post_eval_collapse_detector.py` | Public Supporting | Include unchanged | Small, self-contained support module. |
| `scripts/stage_c1_evaluator_foundation.py` | Public Supporting | Include with major adaptation | The fixture root still resolves to the WP8 corpus under excluded report surfaces. That dependency must be decoupled or replaced. |
| `tests/test_dataset_contract.py` | Public Supporting | Include with major adaptation | It hardcodes the external runtime repo path and therefore is not public-alpha clean. |
| `tests/test_masking_behavior.py` | Public Supporting | Include unchanged | Core masking regression coverage. |
| `tests/test_eval_canonical_manifest.py` | Public Supporting | Include with major adaptation | It depends on threshold/profile and detector artifacts that live in excluded `manifests/` / `reports/` surfaces. |
| `tests/test_eval_adapter_toolcalls.py` | Public Supporting | Include with minor adaptation | It hardcodes the current repo path instead of resolving through the repo helper. |
| `tests/test_repo_paths.py` | Public Supporting | Include with major adaptation | It expects registry entries for excluded fixture and sample-output roles; those assumptions do not match the alpha boundary. |
| `tests/test_compatibility_path_resolution.py` | Public Supporting | Include unchanged | Good public-facing path-resolution regression coverage. |
| `tests/test_stage_c1_evaluator_foundation.py` | Public Supporting | Include with major adaptation | It still depends on the excluded WP8 fixture root through the evaluator foundation. |

### Public Supporting: Process Infrastructure Families

All selected files in these families can be included unchanged:

#### Checklists

- `docs/framework/process_infrastructure/checklists/git_ignore_verification_checklist.md`
- `docs/framework/process_infrastructure/checklists/governance_boundary_verification_checklist.md`
- `docs/framework/process_infrastructure/checklists/hygiene_review_checklist.md`
- `docs/framework/process_infrastructure/checklists/publication_readiness_checklist.md`
- `docs/framework/process_infrastructure/checklists/push_readiness_checklist.md`
- `docs/framework/process_infrastructure/checklists/review_package_completeness_checklist.md`
- `docs/framework/process_infrastructure/checklists/validation_evidence_checklist.md`
- `docs/framework/process_infrastructure/checklists/zip_workflow_checklist.md`

#### Templates

- `docs/framework/process_infrastructure/templates/closure_determination_template.md`
- `docs/framework/process_infrastructure/templates/conformance_report_template.md`
- `docs/framework/process_infrastructure/templates/coverage_summary_template.md`
- `docs/framework/process_infrastructure/templates/implementation_summary_template.md`
- `docs/framework/process_infrastructure/templates/milestone_determination_template.md`
- `docs/framework/process_infrastructure/templates/package_review_template.md`
- `docs/framework/process_infrastructure/templates/readiness_determination_template.md`
- `docs/framework/process_infrastructure/templates/reconciliation_summary_template.md`
- `docs/framework/process_infrastructure/templates/transition_readiness_assessment_template.md`

These files are reusable process assets and do not require content changes for alpha assembly.

### Curated Historical Evidence

| Artifact | PUBLIC_ALPHA_01 classification | Preparation classification | Rationale |
|---|---|---|---|
| `docs/framework/lineages/README.md` | Curated Historical Evidence | Include with major adaptation | The current index reflects an older five-item spine. It must be rewritten to match the accepted alpha evidence set and reading path. |
| `docs/framework/lineages/i2_contamination_event.md` | Curated Historical Evidence | Include unchanged | Bounded lineage evidence; no prep issue. |
| `docs/framework/lineages/i4_i5_overconstraint_collapse.md` | Curated Historical Evidence | Include unchanged | Same. |
| `docs/framework/lineages/i6_isolated_variable_pivot.md` | Curated Historical Evidence | Include unchanged | Same. |
| `docs/framework/lineages/i7_coupled_schema_dynamics.md` | Curated Historical Evidence | Include unchanged | Same. |
| `docs/framework/lineages/i8_pre_training_governance_snapshot.md` | Curated Historical Evidence | Include unchanged | Same. |
| `docs/framework/methodology/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md` | Curated Historical Evidence | Include unchanged | Decision-bearing methodology record. |
| `docs/framework/methodology/STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md` | Curated Historical Evidence | Include unchanged | Decision-bearing methodology record. |
| `docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md` | Curated Historical Evidence | Include unchanged | Accepted milestone record. |
| `docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md` | Curated Historical Evidence | Include unchanged | Accepted roadmap record. |
| `docs/housekeeping/OSS_01_INDEPENDENT_REVIEW_AND_RECONCILIATION_GROK.md` | Curated Historical Evidence | Include unchanged | Decision-lineage evidence. |
| `docs/housekeeping/OSS_05_PUBLIC_FRONT_DOOR_IMPLEMENTATION_SUMMARY.md` | Curated Historical Evidence | Include unchanged | Decision-lineage evidence. |

## 3. Adaptation Inventory

### High-priority adaptation items

| Artifact | Exact issue | Required preparation |
|---|---|---|
| `README.md` | Still narrates the canonical/private baseline and references excluded validation/history surfaces. | Rewrite the front door so it only points at the alpha-approved surface set. |
| `docs/goal_charter_v5a.md` | Hardcoded machine-specific and private-repo path references (`/opt/ai-stack/...`, `/mnt/mirrors/...`). | Normalize paths and remove public-facing dependence on local deployment locations. |
| `docs/appendix_a_operational_execution_contract_v3a.md` | Same machine-specific and private-path problem as the charter. | Normalize the pinned references or annotate them as canonical/private-only provenance. |
| `evals/canonical_eval_manifest_v1.json` | Pins absolute paths to private/local locations and references excluded data/report surfaces. | Convert to public-alpha-safe references or explicitly fence it as a pinned contract with unresolved external paths called out. |
| `docs/current/start_here.md` | Reading path still assumes a broader canonical repo than the alpha package. | Rewrite the navigation path so it only leads through alpha-approved files. |
| `docs/current/current_status.md` | Closure references and boundary language still point at non-alpha artifacts. | Replace closure references with the accepted alpha baseline and curated evidence spine. |
| `docs/current/framework_vs_history.md` | Enumerates excluded families (`docs/convergence/`, `docs/continuity/`, `docs/history/`, `configs/`, `manifests/`, `reports/`, `data/`) as if they were public navigation surfaces. | Prune to the alpha boundary and reframe the history/current split around the accepted public package. |
| `docs/current/housekeeping_status.md` | References closure-report artifacts that are not part of the alpha package. | Update to reference the accepted alpha boundary instead of missing closure docs. |
| `docs/framework/lineages/README.md` | Still reflects an older minimal spine, not the accepted alpha evidence set. | Rewrite the index to the accepted alpha spine and theme order. |
| `scripts/stage_c1_evaluator_foundation.py` | Depends on the WP8 fixture corpus in excluded report surfaces. | Decouple from the excluded fixture root or replace the dependency with a public-alpha fixture registry. |
| `tests/test_dataset_contract.py` | Hardcoded `/opt/ai-stack/runtimes/assistant-runtime` path to an external repository. | Replace with repo-root-relative indirection or move the assertion into a summary-only public contract note. |
| `tests/test_eval_canonical_manifest.py` | Depends on excluded threshold/profile and detector artifacts in `manifests/` and `reports/`. | Decouple from excluded surfaces or replace with a smaller public-alpha contract test. |
| `tests/test_eval_adapter_toolcalls.py` | Hardcoded absolute path to the current repository checkout. | Switch to repo-root resolution. |
| `tests/test_repo_paths.py` | Still expects registry entries for excluded fixture/sample-output roles. | Rewrite the expectations to alpha-only roles or make the registry explicitly alpha-scoped. |
| `tests/test_stage_c1_evaluator_foundation.py` | Depends on the excluded WP8 fixture root via the evaluator foundation helper. | Repoint to a public-alpha fixture surface or replace with a smaller public test. |

### Medium-priority review items

| Artifact | Exact issue | Required preparation |
|---|---|---|
| `scripts/build_dataset_v1.py` | No hardcoded path defect, but its defaults should be checked after the manifest is rewritten. | Verify defaults still match the alpha boundary after the manifest and docs are updated. |
| `scripts/preflight_lora_run.py` | Same. | Validate against the final alpha manifest and repo-root layout. |
| `scripts/train_lora_sft.py` | Same. | Validate against the final alpha manifest and repo-root layout. |
| `scripts/eval_canonical_manifest.py` | Same. | Validate against the final manifest once its path contract is normalized. |
| `tests/test_compatibility_path_resolution.py` | No direct defect, but it should be re-run after path cleanup. | Re-validate after the path-sensitive files are updated. |

### No-prep items

These selected artifacts do not require preparation edits before alpha assembly:

- `AGENTS.md`
- `pyproject.toml`
- `.gitignore`
- `repo_paths.py`
- `scripts/repo_paths.py`
- `scripts/eval_adapter_toolcalls.py`
- `scripts/post_eval_collapse_detector.py`
- `tests/test_masking_behavior.py`
- all selected process-infrastructure checklist/template files
- the selected lineages, methodology transitions, current milestone/roadmap records, and housekeeping evidence documents
- `docs/metric_specification_v1a.md`
- `docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md`
- `docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md`

No selected artifact needs summary-only replacement at this stage.
The prep work is primarily adaptation, not substitution.

## 4. Remediation Checklist

Use this checklist as the preparation gate before assembly:

1. Rewrite [README.md](/opt/ai-stack/assistant-training/README.md) so the front door only points to alpha-approved files and no longer advertises excluded canonical-only surfaces.
2. Normalize path literals in [docs/goal_charter_v5a.md](/opt/ai-stack/assistant-training/docs/goal_charter_v5a.md) and [docs/appendix_a_operational_execution_contract_v3a.md](/opt/ai-stack/assistant-training/docs/appendix_a_operational_execution_contract_v3a.md).
3. Update [evals/canonical_eval_manifest_v1.json](/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json) so the manifest is public-alpha-safe and does not imply that excluded data/report surfaces are part of the assembled package.
4. Rewrite [docs/current/start_here.md](/opt/ai-stack/assistant-training/docs/current/start_here.md), [docs/current/current_status.md](/opt/ai-stack/assistant-training/docs/current/current_status.md), [docs/current/framework_vs_history.md](/opt/ai-stack/assistant-training/docs/current/framework_vs_history.md), and [docs/current/housekeeping_status.md](/opt/ai-stack/assistant-training/docs/current/housekeeping_status.md) to match the accepted alpha boundary.
5. Rewrite [docs/framework/lineages/README.md](/opt/ai-stack/assistant-training/docs/framework/lineages/README.md) so it reflects the accepted alpha evidence spine and reading order.
6. Decouple [scripts/stage_c1_evaluator_foundation.py](/opt/ai-stack/assistant-training/scripts/stage_c1_evaluator_foundation.py) from the excluded WP8 fixture corpus or replace that dependency with a public-alpha fixture registry.
7. Replace the hardcoded external runtime path in [tests/test_dataset_contract.py](/opt/ai-stack/assistant-training/tests/test_dataset_contract.py) with repo-root-relative or helper-driven resolution.
8. Rework [tests/test_eval_canonical_manifest.py](/opt/ai-stack/assistant-training/tests/test_eval_canonical_manifest.py) so it does not depend on excluded `manifests/` or `reports/` artifacts.
9. Replace the absolute path literal in [tests/test_eval_adapter_toolcalls.py](/opt/ai-stack/assistant-training/tests/test_eval_adapter_toolcalls.py) with repository-root resolution.
10. Rewrite [tests/test_repo_paths.py](/opt/ai-stack/assistant-training/tests/test_repo_paths.py) so it validates only alpha-scoped roles.
11. Repoint [tests/test_stage_c1_evaluator_foundation.py](/opt/ai-stack/assistant-training/tests/test_stage_c1_evaluator_foundation.py) away from excluded fixture surfaces.
12. Re-run `git diff --check` and the path-sensitive tests after the above edits.

## 5. Risk Assessment

### High-risk adaptations

- `evals/canonical_eval_manifest_v1.json`
- `scripts/stage_c1_evaluator_foundation.py`
- `tests/test_dataset_contract.py`
- `tests/test_eval_canonical_manifest.py`
- `tests/test_repo_paths.py`
- `tests/test_stage_c1_evaluator_foundation.py`

Why high risk:
- they are either path-coupled to excluded surfaces or externally anchored,
- they are necessary for reproducibility/validation,
- and they can block alpha assembly if left unresolved.

### Medium-risk adaptations

- `README.md`
- `docs/goal_charter_v5a.md`
- `docs/appendix_a_operational_execution_contract_v3a.md`
- `docs/current/start_here.md`
- `docs/current/current_status.md`
- `docs/current/framework_vs_history.md`
- `docs/current/housekeeping_status.md`
- `docs/framework/lineages/README.md`
- `tests/test_eval_adapter_toolcalls.py`

Why medium risk:
- they are mostly narrative/navigation edits,
- but they determine whether the public alpha reads cleanly and does not leak canonical-only assumptions.

### Low-risk items

- `AGENTS.md`
- `pyproject.toml`
- `.gitignore`
- `repo_paths.py`
- `scripts/repo_paths.py`
- `scripts/eval_adapter_toolcalls.py`
- `scripts/post_eval_collapse_detector.py`
- `tests/test_masking_behavior.py`
- all selected process-infrastructure checklists/templates
- all unchanged historical evidence artifacts
- `docs/metric_specification_v1a.md`
- `docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md`
- `docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md`
- `docs/housekeeping/OSS_01_INDEPENDENT_REVIEW_AND_RECONCILIATION_GROK.md`
- `docs/housekeeping/OSS_05_PUBLIC_FRONT_DOOR_IMPLEMENTATION_SUMMARY.md`

Why low risk:
- they are already aligned to the accepted alpha baseline or are stable reusable support material.

## 6. Effort Assessment

### Estimated files requiring direct work

- High-risk / direct edits: about 10 to 12 files
- Medium-risk / review-and-verify files: about 6 to 8 files
- Unchanged files: the remainder of the selected baseline

### Approximate preparation effort

- **Focused preparation effort:** one to two working days
- Most of that time is expected to go into:
  - front-door and current-state rewrite,
  - manifest path normalization,
  - and test/fixture decoupling.

### Likely blockers

1. The excluded WP8 fixture corpus is still the current dependency for `scripts/stage_c1_evaluator_foundation.py` and its test.
2. `tests/test_dataset_contract.py` reaches outside the repository to an external runtime checkout.
3. The canonical eval manifest still uses absolute paths and excluded support surfaces.
4. The lineage index still reflects the older five-artifact spine.

If those blockers are not resolved, alpha assembly will either be brittle or internally inconsistent.

## 7. Assembly Readiness Determination

### Determination

**Ready after preparation**

### Rationale

The alpha baseline is complete enough to assemble, but several selected artifacts are not yet in a public-alpha-safe shape.

The main blockers are not conceptual:

- they are path hygiene,
- fixture coupling,
- and front-door consistency.

Once those are resolved, the alpha repository can be assembled from the accepted baseline without revisiting the publication architecture itself.

## 8. Final Recommendation

Proceed with a narrow preparation pass before alpha assembly execution.

Do not assemble yet.
Do not widen the alpha scope.
Do not pull in excluded canonical-only families to avoid the prep work.

The correct order is:

1. prepare the selected alpha files,
2. validate the prepared candidate,
3. then assemble the local alpha repository candidate from the accepted baseline.
