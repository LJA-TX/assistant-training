Assessment only. No repository changes were made as part of the assessment itself.

# PUBLIC_REPO_01_INITIAL_CONTENT_MANIFEST

## 1. Executive Summary

Version 1 of the curated/public repository should be a lean, method-first package with a bounded evidence spine.

The public repo should:
- explain the project purpose and current doctrine
- expose the reproducible training and evaluation core
- show a small number of carefully selected historical documents that prove the method evolved through real decisions and reviews
- exclude bulk data, reports, manifests, generated artifacts, and research/archive surfaces

The right story for `LJA-TX/assistant-training` is not "everything the canonical repo contains." It is:
- a disciplined runtime-assistant regimen
- with clear governance
- reproducible tooling
- and a small, reviewer-friendly historical trail showing contamination discipline, methodology pivots, closure decisions, and public-front-door refinement

## 2. Public Core Candidates

Public Core should contain the minimum stable surface needed for a technically competent newcomer to understand and inspect the regimen.

### Core file families
- [README.md](/opt/ai-stack/assistant-training/README.md)
- Root doctrine:
  - [docs/goal_charter_v5a.md](/opt/ai-stack/assistant-training/docs/goal_charter_v5a.md)
  - [docs/appendix_a_operational_execution_contract_v3a.md](/opt/ai-stack/assistant-training/docs/appendix_a_operational_execution_contract_v3a.md)
  - [docs/metric_specification_v1a.md](/opt/ai-stack/assistant-training/docs/metric_specification_v1a.md)
  - [docs/evaluation_manifest_v1.md](/opt/ai-stack/assistant-training/docs/evaluation_manifest_v1.md)
- Current-state orientation:
  - [docs/current/start_here.md](/opt/ai-stack/assistant-training/docs/current/start_here.md)
  - [docs/current/current_status.md](/opt/ai-stack/assistant-training/docs/current/current_status.md)
  - [docs/current/framework_vs_history.md](/opt/ai-stack/assistant-training/docs/current/framework_vs_history.md)
  - [docs/current/housekeeping_status.md](/opt/ai-stack/assistant-training/docs/current/housekeeping_status.md)
- Executable regimen:
  - `scripts/` core training, preflight, dataset, eval, and path-resolution entrypoints
  - `tests/` core contract and regression tests
- Packaging and configuration:
  - [pyproject.toml](/opt/ai-stack/assistant-training/pyproject.toml)
  - [repo_paths.py](/opt/ai-stack/assistant-training/repo_paths.py)
  - [evals/canonical_eval_manifest_v1.json](/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json)
- Rights package:
  - [LICENSE](/opt/ai-stack/assistant-training/LICENSE) once the Apache-2.0 publication gate is finalized
  - [NOTICE](/opt/ai-stack/assistant-training/NOTICE) only if retained third-party notice material requires it

### Rationale
- These are the files that most directly answer:
  - what the repository is
  - why it exists
  - what makes it different
  - and what can be inspected quickly
- They preserve the public method without dragging the archive into the front door
- The canonical evaluation manifest is essential because it is the public reproducibility anchor

## 3. Public Supporting Candidates

Public Supporting should include files that improve reviewability and maintainability, but are not required to understand the method on first pass.

### Supporting file families
- [AGENTS.md](/opt/ai-stack/assistant-training/AGENTS.md)
- [docs/framework/process_infrastructure/](/opt/ai-stack/assistant-training/docs/framework/process_infrastructure/)
- [docs/process_infrastructure/](/opt/ai-stack/assistant-training/docs/process_infrastructure/) as a preserved compatibility pointer only
- [docs/repo_layout.md](/opt/ai-stack/assistant-training/docs/repo_layout.md)
- [docs/evaluation_manifest_v1.md](/opt/ai-stack/assistant-training/docs/evaluation_manifest_v1.md)
- [.gitignore](/opt/ai-stack/assistant-training/.gitignore)

### Rationale
- These files help a serious reader understand the repository's working conventions and navigation
- They are useful support, but not the public thesis itself
- They are lightweight enough to include without turning the public repo into an archive

## 4. Curated Historical Evidence Candidates

This is the bounded reviewer-facing evidence spine for version 1. Target: approximately 6-12 artifacts. The set below is 12 and is intentionally compact.

### A. Minimal lineage spine
These files show the major methodology inflections without exposing the whole archive:
- [docs/framework/lineages/README.md](/opt/ai-stack/assistant-training/docs/framework/lineages/README.md)
- [docs/framework/lineages/i2_contamination_event.md](/opt/ai-stack/assistant-training/docs/framework/lineages/i2_contamination_event.md)
- [docs/framework/lineages/i4_i5_overconstraint_collapse.md](/opt/ai-stack/assistant-training/docs/framework/lineages/i4_i5_overconstraint_collapse.md)
- [docs/framework/lineages/i6_isolated_variable_pivot.md](/opt/ai-stack/assistant-training/docs/framework/lineages/i6_isolated_variable_pivot.md)
- [docs/framework/lineages/i7_coupled_schema_dynamics.md](/opt/ai-stack/assistant-training/docs/framework/lineages/i7_coupled_schema_dynamics.md)
- [docs/framework/lineages/i8_pre_training_governance_snapshot.md](/opt/ai-stack/assistant-training/docs/framework/lineages/i8_pre_training_governance_snapshot.md)

### B. Methodology transition records
These show how the regimen and its process architecture matured:
- [docs/framework/methodology/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md](/opt/ai-stack/assistant-training/docs/framework/methodology/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md)
- [docs/framework/methodology/STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/framework/methodology/STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md)

### C. Current-state milestone records
These show accepted milestone closure and the next investigative direction:
- [docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md](/opt/ai-stack/assistant-training/docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md)
- [docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md](/opt/ai-stack/assistant-training/docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md)

### D. Governance and publication-history records
These show independent review and public-front-door refinement:
- [docs/housekeeping/OSS_01_INDEPENDENT_REVIEW_AND_RECONCILIATION_GROK.md](/opt/ai-stack/assistant-training/docs/housekeeping/OSS_01_INDEPENDENT_REVIEW_AND_RECONCILIATION_GROK.md)
- [docs/housekeeping/OSS_05_PUBLIC_FRONT_DOOR_IMPLEMENTATION_SUMMARY.md](/opt/ai-stack/assistant-training/docs/housekeeping/OSS_05_PUBLIC_FRONT_DOOR_IMPLEMENTATION_SUMMARY.md)

### Rationale
- This set proves the repository is not just a clean shell; it shows real evolution
- It demonstrates contamination discipline, isolated-variable methodology, governance gating, process extraction, milestone closure, and public-facing refinement
- It is bounded enough to avoid archive creep

## 5. Canonical Only Categories

These categories should remain in `assistant-training-private` by default.

### Major canonical-only families
- [docs/research/](/opt/ai-stack/assistant-training/docs/research/)
- [data/](/opt/ai-stack/assistant-training/data/)
- [evals/data/](/opt/ai-stack/assistant-training/evals/data/)
- [evals/runs/](/opt/ai-stack/assistant-training/evals/runs/)
- [reports/](/opt/ai-stack/assistant-training/reports/)
- [manifests/runs/](/opt/ai-stack/assistant-training/manifests/runs/)
- [manifests/reports/](/opt/ai-stack/assistant-training/manifests/reports/)
- [manifests/environment/](/opt/ai-stack/assistant-training/manifests/environment/)
- [artifacts/](/opt/ai-stack/assistant-training/artifacts/)
- [local_review_bundles/](/opt/ai-stack/assistant-training/local_review_bundles/)
- [configs/](/opt/ai-stack/assistant-training/configs/)
- [docs/history/](/opt/ai-stack/assistant-training/docs/history/)
- bulk [docs/convergence/](/opt/ai-stack/assistant-training/docs/convergence/) outside the curated evidence spine
- bulk [docs/housekeeping/](/opt/ai-stack/assistant-training/docs/housekeeping/) outside the curated evidence spine
- [docs/continuity/](/opt/ai-stack/assistant-training/docs/continuity/) for version 1, because the evidence spine already captures the needed evolution signal more compactly
- later lineage docs not selected for version 1, such as the more detailed `i9*` and `i10*` surfaces

### Rationale
- These families are high-burden, high-provenance, or archive-heavy
- They do not materially improve the public front door
- They belong in the canonical/private repository unless separately promoted later

## 6. Public Repository Narrative

The public repository should tell a story of disciplined regimen development, not a record of every internal artifact.

The story is:
- the project exists to build a reproducible runtime-oriented assistant training regimen
- the method is governed by explicit doctrine and evaluation contracts
- the implementation is reproducible through scripts, tests, and pinned evaluation surfaces
- the method evolved through real constraints: contamination events, overconstraint collapse, isolated-variable pivots, coupled schema dynamics, blocker-branch closure, and public-front-door refinement
- the public package is intentionally selective, so readers can understand the method without being buried in the archive

This gives the public repo a clear identity:
- methodology
- governance
- rigor
- reproducibility
- and evolution

## 7. Codex-for-OSS Assessment

The proposed manifest should read well to a Codex-for-OSS reviewer.

### It demonstrates serious work
- The public core exposes the actual regimen, not marketing prose
- The evidence spine shows repeated closure, review, and correction cycles
- The repository appears engineered, not assembled casually

### It demonstrates maintenance discipline
- The manifest is selective
- Archive-heavy material stays canonical-only
- The public boundary is explicit rather than implied

### It demonstrates methodology evolution
- The lineage set and selected methodology/current/governance docs show how the project moved from early contamination discipline to isolated-variable methodology and then to blocker-branch closure and public-front-door refinement

### It remains approachable
- `README.md`, `start_here.md`, `current_status.md`, and `framework_vs_history.md` make the repo navigable
- The public evidence spine is small enough to read
- A technically competent newcomer can understand the project without first reconstructing the full history

## 8. Risk Assessment

| Risk | Why it matters | Mitigation |
|---|---|---|
| Over-disclosure | Bulk archive or data/report surfaces would make the public repo noisy and harder to license/review | Keep bulk history, data, reports, manifests, and research canonical-only |
| Under-disclosure | Removing all history would make the project look thin and reduce reviewer confidence | Keep the curated evidence spine of 12 artifacts |
| Archive creep | Historical evidence can slowly become a second archive | Cap the evidence set and require nomination review for additions |
| Insufficient evidence | A public repo with only core docs can hide serious maintenance history | Include the lineage, milestone, and governance evidence set |
| Discoverability issues | Too many categories or unclear boundaries can confuse new readers | Keep the public front door simple and explicitly map categories in the README |
| Provenance mistakes | Mixed-provenance families could be accidentally included | Treat the canonical-only boundary as default and require review for exceptions |

## 9. Recommended Version-1 Manifest

### Include by default
- Public Core:
  - README
  - doctrine
  - current-state docs
  - scripts
  - tests
  - packaging and configuration metadata
  - canonical eval manifest
  - LICENSE, once adopted
  - NOTICE only if required by retained third-party notice material
- Public Supporting:
  - AGENTS
  - process infrastructure
  - repo layout / evaluation-manifest narrative docs
  - ignore rules
- Curated Historical Evidence:
  - the 12-artifact spine listed above
- Canonical Only:
  - data, reports, manifests, artifacts, research, deprecated docs, continuity docs, and all bulk archive material not explicitly selected for the evidence spine

### Exclude from version 1
- training datasets
- evaluation datasets
- run manifests
- generated reports
- artifact bundles
- research memos
- bulk convergence history
- bulk housekeeping history
- local review bundles

## 10. Final Recommendation

Use the manifest above as the first public-release candidate for `LJA-TX/assistant-training`.

It is the best balance of:
- clarity
- public value
- reviewer credibility
- reproducibility
- and maintenance burden

Keep version 1 lean at the core, support it with a small historical evidence spine, and leave the rights-heavy archive families in the canonical/private repository.
