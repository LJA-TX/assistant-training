# PUBLIC_ALPHA_01_ALPHA_REPOSITORY_ASSEMBLY_MANIFEST

Assessment and documentation creation authorized.

This document defines the exact local alpha candidate for the future curated/public repository `LJA-TX/assistant-training`.
It is a planning artifact only. It does not assemble, move, copy, or publish anything.

## 1. Executive Summary

The alpha repository should be a lean, method-first package.
It should teach a reader three things quickly:

1. what the project is for,
2. how the regimen is governed and evaluated,
3. how the current method evolved without exposing the full canonical archive.

The correct alpha story is not "everything in the canonical repository."
It is:

- a disciplined runtime-oriented training and evaluation regimen,
- a small public front door with explicit doctrine and current-state guidance,
- a bounded curated historical evidence spine,
- and a narrow support layer for reproducibility and inspection.

The alpha candidate is sufficiently defined to build locally.
It is not yet publication-ready as-is because several included documents and tests still need minor adaptation to remove hardcoded local-path assumptions or references to canonical-only support surfaces.

## 2. Alpha Repository Scope

### Scope statement

The alpha repository should present the methodology, doctrine, evaluation contract, and a curated evidence trail.
It should not try to mirror the canonical repository.
It should not expose bulk data, run dumps, archive-like history, or internal publication planning noise.

### What the first-time visitor should learn

- The project builds a reproducible runtime-oriented assistant regimen.
- The public package is intentionally selective.
- Current-state guidance is available up front.
- The method evolved through real decisions, reviews, and closures.

### What a Codex-for-OSS reviewer should learn

- The repository is maintained deliberately, not assembled opportunistically.
- Governance exists and is documented.
- Reproducibility is backed by scripts, tests, and a pinned canonical evaluation contract.
- The historical trail is bounded and decision-bearing rather than archival.

## 3. Inclusion Manifest

### Public Core

| Path | Transform | Why it belongs |
| --- | --- | --- |
| `README.md` | Include with minor adaptation | Public front door; should explain the curated/public boundary and the inspection path. |
| `AGENTS.md` | Include unchanged | Agent routing and authority-order skeleton; useful for automated and human inspection. |
| `pyproject.toml` | Include unchanged | Packaging and project metadata. |
| `.gitignore` | Include unchanged | Basic hygiene and noise suppression. |
| `repo_paths.py` | Include unchanged | Compatibility shim for the repository-root helper. |
| `evals/canonical_eval_manifest_v1.json` | Include with minor adaptation | Pinned canonical evaluation contract; should remain the public reproducibility anchor. |
| `docs/goal_charter_v5a.md` | Include with minor adaptation | Core doctrine; current absolute-path references should be normalized for the public copy. |
| `docs/appendix_a_operational_execution_contract_v3a.md` | Include with minor adaptation | Binding operational authority; path literals should be normalized. |
| `docs/metric_specification_v1a.md` | Include unchanged | Canonical scoring semantics; compact and foundational. |
| `docs/current/start_here.md` | Include with minor adaptation | Reader entry point; should point cleanly into the curated alpha package. |
| `docs/current/current_status.md` | Include with minor adaptation | Current-state summary; should be trimmed to the alpha boundary and not rely on excluded closure files. |
| `docs/current/framework_vs_history.md` | Include with minor adaptation | Boundary map between current method and curated history; should reflect the alpha set. |
| `docs/current/housekeeping_status.md` | Include with minor adaptation | Boundary summary for housekeeping and current structure; should align with the alpha package. |

### Public Supporting

| Path | Transform | Why it belongs |
| --- | --- | --- |
| `scripts/repo_paths.py` | Include unchanged | Shared path resolver; central to portability and path discipline. |
| `scripts/build_dataset_v1.py` | Include with minor adaptation | Core dataset builder; may need path normalization for the public copy. |
| `scripts/preflight_lora_run.py` | Include with minor adaptation | Preflight / readiness gate helper for the training pipeline. |
| `scripts/train_lora_sft.py` | Include with minor adaptation | Primary training entry point; should remain inspectable in the public package. |
| `scripts/eval_canonical_manifest.py` | Include with minor adaptation | Canonical evaluation harness; should remain close to the pinned eval contract. |
| `scripts/eval_adapter_toolcalls.py` | Include unchanged | Legacy/direct evaluation harness; useful as a compatibility and comparison surface. |
| `scripts/post_eval_collapse_detector.py` | Include unchanged | Post-eval detector support; small and self-contained. |
| `scripts/stage_c1_evaluator_foundation.py` | Include with minor adaptation | Current evaluator foundation; should be kept, but its fixture dependency must be reviewed for the public copy. |
| `tests/test_dataset_contract.py` | Include with minor adaptation | Core dataset contract coverage; currently references an external runtime dataset path. |
| `tests/test_masking_behavior.py` | Include unchanged | Core masking regression coverage. |
| `tests/test_eval_canonical_manifest.py` | Include with minor adaptation | Canonical eval contract coverage; currently coupled to canonical-only threshold/fixture surfaces. |
| `tests/test_eval_adapter_toolcalls.py` | Include with minor adaptation | Legacy eval harness coverage; currently hardcodes the current repo path. |
| `tests/test_repo_paths.py` | Include with minor adaptation | Path-resolution contract coverage; should be narrowed to the public alpha boundary. |
| `tests/test_compatibility_path_resolution.py` | Include unchanged | Good public-facing compatibility regression coverage. |
| `tests/test_stage_c1_evaluator_foundation.py` | Include with minor adaptation | Evaluator-foundation regression coverage; currently coupled to the WP8 fixture root. |
| `docs/framework/process_infrastructure/checklists/git_ignore_verification_checklist.md` | Include unchanged | Lightweight reusable hygiene checklist. |
| `docs/framework/process_infrastructure/checklists/governance_boundary_verification_checklist.md` | Include unchanged | Reusable boundary-verification checklist. |
| `docs/framework/process_infrastructure/checklists/hygiene_review_checklist.md` | Include unchanged | Reusable hygiene checklist. |
| `docs/framework/process_infrastructure/checklists/publication_readiness_checklist.md` | Include unchanged | Publication readiness gate checklist. |
| `docs/framework/process_infrastructure/checklists/push_readiness_checklist.md` | Include unchanged | Push readiness gate checklist. |
| `docs/framework/process_infrastructure/checklists/review_package_completeness_checklist.md` | Include unchanged | Review completeness checklist. |
| `docs/framework/process_infrastructure/checklists/validation_evidence_checklist.md` | Include unchanged | Validation evidence checklist. |
| `docs/framework/process_infrastructure/checklists/zip_workflow_checklist.md` | Include unchanged | Zip / package workflow checklist. |
| `docs/framework/process_infrastructure/templates/closure_determination_template.md` | Include unchanged | Reusable closure template. |
| `docs/framework/process_infrastructure/templates/conformance_report_template.md` | Include unchanged | Reusable conformance template. |
| `docs/framework/process_infrastructure/templates/coverage_summary_template.md` | Include unchanged | Reusable coverage summary template. |
| `docs/framework/process_infrastructure/templates/implementation_summary_template.md` | Include unchanged | Reusable implementation summary template. |
| `docs/framework/process_infrastructure/templates/milestone_determination_template.md` | Include unchanged | Reusable milestone template. |
| `docs/framework/process_infrastructure/templates/package_review_template.md` | Include unchanged | Reusable package review template. |
| `docs/framework/process_infrastructure/templates/readiness_determination_template.md` | Include unchanged | Reusable readiness template. |
| `docs/framework/process_infrastructure/templates/reconciliation_summary_template.md` | Include unchanged | Reusable reconciliation summary template. |
| `docs/framework/process_infrastructure/templates/transition_readiness_assessment_template.md` | Include unchanged | Reusable transition readiness template. |

### Curated Historical Evidence

| Path | Transform | Why it belongs |
| --- | --- | --- |
| `docs/framework/lineages/README.md` | Include with minor adaptation | Primary curated evidence index; should point at the alpha evidence spine. |
| `docs/framework/lineages/i2_contamination_event.md` | Include unchanged | Shows an early contamination/discipline inflection point. |
| `docs/framework/lineages/i4_i5_overconstraint_collapse.md` | Include unchanged | Captures a major methodological failure and correction. |
| `docs/framework/lineages/i6_isolated_variable_pivot.md` | Include unchanged | Shows the isolated-variable pivot that improved method clarity. |
| `docs/framework/lineages/i7_coupled_schema_dynamics.md` | Include unchanged | Shows the next major schema/method coupling inflection. |
| `docs/framework/lineages/i8_pre_training_governance_snapshot.md` | Include unchanged | Compact governance snapshot showing the method approaching the public boundary. |
| `docs/framework/methodology/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md` | Include unchanged | Major methodology-architecture decision record. |
| `docs/framework/methodology/STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md` | Include unchanged | Major closure / transition record for the method. |
| `docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md` | Include unchanged | Accepted milestone record showing the current baseline emerging. |
| `docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md` | Include unchanged | Shows the next planned investigative direction after the baseline. |
| `docs/housekeeping/OSS_01_INDEPENDENT_REVIEW_AND_RECONCILIATION_GROK.md` | Include unchanged | Independent review and reconciliation evidence. |
| `docs/housekeeping/OSS_05_PUBLIC_FRONT_DOOR_IMPLEMENTATION_SUMMARY.md` | Include unchanged | Public-front-door refinement evidence. |

## 4. Exclusion Manifest

The following families should remain canonical-only for the alpha package:

- `docs/convergence/`
- `docs/continuity/`
- `docs/history/`
- `docs/research/`
- `docs/process_infrastructure/` compatibility-pointer subtree
- `data/`
- `evals/data/`
- `evals/runs/`
- `reports/`
- `manifests/`
- `configs/`
- `artifacts/`
- `local_review_bundles/`

The following individual documents should also remain canonical-only for the alpha package:

- `docs/assistant_training_goal_documents_and_artifacts_index.md`
- `docs/repository_establishment_plan_v1.md`
- `docs/migration_checklist.md`
- `docs/evaluation_manifest_v1.md`
- `docs/repo_layout.md`
- `docs/framework/lineages/i8_bounded_implementation_scaffold.md`
- `docs/framework/lineages/i9_commitment_conversion_implementation.md`
- `docs/framework/lineages/i9_post_eval_checkpoint.md`
- `docs/framework/lineages/i10_semantic_commitment_implementation.md`
- `docs/framework/lineages/i10r_microprobe_checkpoint.md`
- `docs/framework/lineages/i10r_microprobe_checkpoint_lineage_note.md`
- `docs/framework/methodology/STAGE_BC_PROCESS_EXTRACTION_ASSESSMENT.md`
- `docs/framework/methodology/STAGE_BC_PHASE1_PROCESS_INFRASTRUCTURE_CLOSURE_DETERMINATION.md`
- `docs/framework/methodology/STAGE_C_PACKAGE_3C_REGIMEN_RETROSPECTIVE_AND_REUSABILITY_ASSESSMENT.md`
- `docs/framework/methodology/STAGE_C_PACKAGE_5E_DIRECT_ANSWER_LIFECYCLE_RETROSPECTIVE_AND_REGIMEN_GENERALIZATION_ASSESSMENT.md`
- `docs/framework/methodology/STAGE_C_PACKAGE_6A_FORMAL_BLOCKER_ORIENTED_REGIMEN_BRANCH_ADOPTION_ASSESSMENT.md`
- `docs/framework/methodology/STAGE_C_PACKAGE_6B_CONDITIONAL_BLOCKER_ORIENTED_BRANCH_ADOPTION_DETERMINATION.md`
- `docs/framework/methodology/STAGE_C10C_REFRESHED_DETECTOR_MIGRATION_GATE_DETERMINATION.md`

### Why these exclusions matter

- The excluded families are either bulk archive surfaces, research/planning surfaces, or mixed-provenance data/report surfaces.
- They create disproportionate publication-hygiene burden relative to their value in a public alpha repository.
- They belong in the canonical/private repository unless a later package explicitly promotes a subset of them.

## 5. Evidence Spine Mapping

The curated historical evidence should be surfaced as a single bounded spine, not as an archive.

| Evidence artifact | Theme | Alpha location | Navigation role |
| --- | --- | --- | --- |
| `docs/framework/lineages/README.md` | Index / orientation | `docs/framework/lineages/` | Primary evidence entry point. |
| `docs/framework/lineages/i2_contamination_event.md` | Lineage and inflection points | `docs/framework/lineages/` | Shows the first major discipline/contamination correction. |
| `docs/framework/lineages/i4_i5_overconstraint_collapse.md` | Lineage and inflection points | `docs/framework/lineages/` | Shows the overconstraint collapse and recovery lesson. |
| `docs/framework/lineages/i6_isolated_variable_pivot.md` | Lineage and inflection points | `docs/framework/lineages/` | Shows the isolated-variable pivot that improved method clarity. |
| `docs/framework/lineages/i7_coupled_schema_dynamics.md` | Lineage and inflection points | `docs/framework/lineages/` | Shows the next method-shaping coupling lesson. |
| `docs/framework/lineages/i8_pre_training_governance_snapshot.md` | Governance evolution | `docs/framework/lineages/` | Shows the method approaching a stronger governance posture. |
| `docs/framework/methodology/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md` | Methodology transition | `docs/framework/methodology/` | Explains the architecture shift in the regimen. |
| `docs/framework/methodology/STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md` | Methodology transition | `docs/framework/methodology/` | Explains the blocker-branch closure and runtime-output transition. |
| `docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md` | Current-state milestone | `docs/current/status/` | Confirms the accepted baseline and Stage B completion. |
| `docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md` | Current-state milestone | `docs/current/roadmap/` | Shows the next planned investigative direction. |
| `docs/housekeeping/OSS_01_INDEPENDENT_REVIEW_AND_RECONCILIATION_GROK.md` | Governance and publication history | `docs/housekeeping/` | Shows independent review and reconciliation. |
| `docs/housekeeping/OSS_05_PUBLIC_FRONT_DOOR_IMPLEMENTATION_SUMMARY.md` | Governance and publication history | `docs/housekeeping/` | Shows the public-front-door refinement step. |

### Evidence spine rule

The evidence spine should stay at approximately twelve artifacts total, counting the index page as the entry point and not expanding into a second archive.

## 6. Transform Requirements

### Include unchanged

- `AGENTS.md`
- `pyproject.toml`
- `.gitignore`
- `repo_paths.py`
- `scripts/repo_paths.py`
- `scripts/eval_adapter_toolcalls.py`
- `scripts/post_eval_collapse_detector.py`
- `docs/framework/process_infrastructure/checklists/*.md`
- `docs/framework/process_infrastructure/templates/*.md`
- the curated historical evidence artifacts listed above

### Include with minor adaptation

- `README.md`
- `evals/canonical_eval_manifest_v1.json`
- `docs/goal_charter_v5a.md`
- `docs/appendix_a_operational_execution_contract_v3a.md`
- `docs/current/start_here.md`
- `docs/current/current_status.md`
- `docs/current/framework_vs_history.md`
- `docs/current/housekeeping_status.md`
- `docs/framework/lineages/README.md`
- `scripts/build_dataset_v1.py`
- `scripts/preflight_lora_run.py`
- `scripts/train_lora_sft.py`
- `scripts/eval_canonical_manifest.py`
- `scripts/stage_c1_evaluator_foundation.py`
- `tests/test_dataset_contract.py`
- `tests/test_eval_canonical_manifest.py`
- `tests/test_eval_adapter_toolcalls.py`
- `tests/test_repo_paths.py`
- `tests/test_compatibility_path_resolution.py`
- `tests/test_stage_c1_evaluator_foundation.py`

### Replace with index

- `docs/framework/lineages/README.md` is already the index for the curated evidence spine and should remain the navigation surface for that layer.
- No other included file should be replaced by a separate index in the alpha package.

### Defer from alpha

- bulk archive families
- research-planning families
- mixed-provenance report/data surfaces
- later lineage and methodology documents not selected for the evidence spine
- license artifacts until the rights gate is closed

## 7. Reader Journey Assessment

### First-time visitor

Recommended path:

1. `README.md`
2. `docs/current/start_here.md`
3. `docs/current/current_status.md`
4. `docs/current/framework_vs_history.md`
5. `docs/framework/lineages/README.md`

What this visitor should learn:

- what the repository is
- why the curated alpha exists
- where current-state guidance lives
- how the public method differs from the canonical archive
- how to reach the curated historical evidence spine

### Technically sophisticated reviewer

Recommended path:

1. `README.md`
2. `docs/goal_charter_v5a.md`
3. `docs/appendix_a_operational_execution_contract_v3a.md`
4. `docs/metric_specification_v1a.md`
5. `evals/canonical_eval_manifest_v1.json`
6. `scripts/`
7. `tests/`
8. `docs/framework/lineages/README.md`

What this reviewer should learn:

- the doctrine and scoring model
- the implementation and validation surfaces
- the curated historical trail
- whether the repository is disciplined and reproducible

### Codex-for-OSS reviewer

Recommended path:

1. `README.md`
2. `docs/current/framework_vs_history.md`
3. `docs/framework/lineages/README.md`
4. the curated historical evidence spine
5. `scripts/`
6. `tests/`

What this reviewer should learn:

- that the repository is intentionally curated
- that the method evolved through real decisions
- that the public boundary is bounded and reviewable
- that the repository is maintained with visible discipline

## 8. Alpha Repository Size Assessment

### Estimated size

- Public Core: about 13 files
- Public Supporting: about 25 to 30 files, depending on whether the public copy keeps all selected checklist/template files as individual tracked markdown files
- Curated Historical Evidence: 12 files
- Total: about 50 to 60 tracked files
- Directory count: about 10 top-level or second-level directories in the curated package

### Scope judgment

The alpha candidate is appropriately scoped for a version-1 public package.
It is not tiny, but it is still lean relative to the canonical repository because the bulk archive families stay excluded.

The only part that pushes it above "minimal" is the deliberate support layer for reproducibility and the curated evidence spine.
That is acceptable because this repository exists to be inspected, not merely to be glanced at.

## 9. Assembly Readiness Determination

### Determination

**Ready with minor adjustments.**

### Why not fully ready yet

- Several public-core docs still contain local absolute-path references that should be normalized for the public copy.
- Several included tests are still coupled to canonical-only fixture or report surfaces and should be revised before a public-facing alpha package is considered clean.
- The curated historical evidence index needs its selected i8 entry reflected consistently.

### Why it is still ready

- The public boundary is now concrete enough to assemble.
- The inclusion and exclusion sets are bounded.
- The evidence spine is narrow and decision-bearing.
- The remaining work is adaptation, not new architecture.

## 10. Final Recommendation

Use this manifest as the working alpha assembly target for `LJA-TX/assistant-training`.

Build the alpha package around:

- a small public front door,
- a bounded support layer,
- a curated historical evidence spine,
- and explicit canonical-only exclusions.

Do not let bulk convergence history, continuity records, data/report surfaces, or research/planning artifacts leak into the public package.

The right next step is controlled alpha assembly preparation, followed by a hygiene pass on the path-sensitive docs and tests before any public publication decision.
