Assessment and documentation creation authorized.

# PUBLIC_REPO_02_CURATED_REPOSITORY_ASSEMBLY_PLAN

## 1. Executive Summary

The curated/public repository should be assembled as a selective derivative of the canonical/private repository, not as a mirror and not as a second authority center.

The assembly plan should therefore treat publication as a gated packaging process:
- canonical/private remains the source of truth
- curated/public is derived from approved canonical material
- publication is selective, reviewable, and bounded
- bulk archive, data-bearing, report-heavy, and provenance-heavy surfaces remain canonical-only by default
- a small, intentional Curated Historical Evidence layer is allowed, but it must stay narrow

The most important operational rule is that the public repository should be built from a frozen canonical baseline after boundary review, validation, and license/rights gating. It should not accrete by ad hoc copying or independent public-only edits.

## 2. Recommended Repository Structure

### Root files
The public repository root should contain:
- [README.md](/opt/ai-stack/assistant-training/README.md)
- [AGENTS.md](/opt/ai-stack/assistant-training/AGENTS.md) as a public-supporting process aid
- [LICENSE](/opt/ai-stack/assistant-training/LICENSE) once the Apache-2.0 gate is finalized
- [NOTICE](/opt/ai-stack/assistant-training/NOTICE) only if retained notice material requires it
- [pyproject.toml](/opt/ai-stack/assistant-training/pyproject.toml)
- [repo_paths.py](/opt/ai-stack/assistant-training/repo_paths.py)

### docs/
The public `docs/` tree should organize content by reader function:
- `docs/current/` for orientation and current state
- `docs/framework/` for doctrine, methodology, and process infrastructure
- `docs/framework/lineages/` for the curated historical evidence spine
- `docs/framework/methodology/` for selected methodology transition records
- `docs/process_infrastructure/` only as a preserved compatibility pointer if link continuity is worth keeping

### scripts/
This should hold the executable regimen:
- training helpers
- dataset construction helpers
- evaluation helpers
- preflight and hygiene helpers
- path resolution helpers

### tests/
This should hold the public contract and regression tests that support reproducibility and inspection.

### Historical evidence location
The evidence spine should live in the existing thematic locations rather than in a new archive-like top-level area. The main entry point should be a curated index under `docs/framework/lineages/README.md`, with selected evidence files distributed across:
- `docs/framework/lineages/`
- `docs/framework/methodology/`
- `docs/current/`
- a small number of governance/publication documents if they are directly decision-bearing

This preserves the historical signal without creating a second archive.

## 3. Public Reader Journey

### First-time visitor
Recommended path:
1. `README.md`
2. `docs/current/start_here.md`
3. `docs/current/current_status.md`
4. `docs/current/framework_vs_history.md`
5. `docs/framework/lineages/README.md`

Goal:
- understand what the project is
- identify what is current
- learn how the public method differs from the historical record
- find the smallest useful evidence trail

### Technical reviewer
Recommended path:
1. `README.md`
2. `docs/framework/lineages/README.md`
3. selected lineage and methodology docs
4. `docs/evaluation_manifest_v1.md`
5. `evals/canonical_eval_manifest_v1.json`
6. `scripts/`
7. `tests/`

Goal:
- inspect the method
- inspect the evidence spine
- verify reproducibility anchors
- evaluate whether the repo is disciplined and technically credible

### Codex-for-OSS reviewer
Recommended path:
1. `README.md`
2. `docs/current/framework_vs_history.md`
3. `docs/framework/lineages/README.md`
4. selected methodology and governance-transition documents
5. `docs/housekeeping/` only for the few selected evidence items, if those are included in version 1
6. `scripts/` and `tests/`

Goal:
- assess seriousness
- assess maintenance discipline
- assess methodology evolution
- assess governance maturity

### Future maintainer
Recommended path:
1. `README.md`
2. `docs/current/start_here.md`
3. `docs/current/current_status.md`
4. `docs/framework/process_infrastructure/`
5. `scripts/`
6. `tests/`
7. `pyproject.toml`
8. `repo_paths.py`

Goal:
- understand the current operating model
- understand where execution and validation live
- understand how to extend without breaking the curated boundary

## 4. Historical Evidence Presentation Strategy

The 12-artifact evidence spine should be presented as a curated index with thematic grouping.

Recommended approach:
- keep the evidence in its natural thematic locations
- surface it through one small index page
- group evidence by theme rather than by raw chronology alone

Recommended themes:
- lineage and inflection points
- methodology transitions
- current-state milestones
- governance and publication-history decisions

Why this works:
- direct exposure alone is too flat and makes the reader browse blindly
- a pure timeline can hide thematic meaning
- a curated index with themes preserves both discoverability and narrative clarity

Best practical presentation:
- `docs/framework/lineages/README.md` as the primary evidence index
- `docs/current/framework_vs_history.md` as the bridge between current method and historical evidence
- a short number of selected evidence documents from methodology, current-state, and housekeeping history

## 5. Navigation Strategy

### README responsibilities
The root `README.md` should:
- define the project in one pass
- explain the canonical/private vs curated/public relationship
- provide the main entry points
- point to the current-state docs and the evidence spine
- keep the front door concise

### start_here responsibilities
`docs/current/start_here.md` should:
- explain how to read the repository
- identify the current active surface
- point to the authoritative current-state and history bridge
- keep a newcomer from starting in the archive

### framework_vs_history responsibilities
`docs/current/framework_vs_history.md` should:
- explain the difference between current method and preserved history
- explain why the public repo is selective
- point to the historical evidence spine without overwhelming the reader

### evidence navigation responsibilities
`docs/framework/lineages/README.md` should:
- act as the curated evidence index
- explain the thematic grouping
- tell the reader which files are the minimum history spine
- keep the historical layer bounded

## 6. AGENTS.md Assessment

`AGENTS.md` belongs in **Public Supporting**, not Public Core.

Rationale:
- it is helpful for process routing and agentic inspection
- it supports maintainability and automation
- but it does not define the public method itself
- a human reader can understand the repository without it on first pass

If the public repository were extremely minimal and human-only, `AGENTS.md` could be omitted. But for an agent-friendly public repo, it is worth keeping as supporting material.

## 7. Readiness Gates

Before version 1 assembly approval, verify:
- the public inclusion boundary is frozen by category
- Public Core, Public Supporting, Curated Historical Evidence, and Canonical Only are assigned consistently
- no Canonical Only family has been accidentally promoted
- the evidence spine is bounded and decision-bearing
- rights and license posture are finalized
- the public repo links are coherent
- the reader journey works from README to current-state to evidence spine
- the public package remains readable without archive overload
- no machine-specific leak or provenance defect has been introduced into the included files
- no unresolved authority conflict exists between canonical and curated views

## 8. Risk Assessment

| Risk | Why it matters | Mitigation |
|---|---|---|
| Discoverability failure | A public repo can be technically correct but too hard to navigate | Use a strong README, start_here, and framework_vs_history bridge |
| Evidence overload | Too many historical files can turn the public repo into an archive | Keep the evidence spine capped and thematic |
| Evidence underexposure | Too little history can make the project look thin or unproven | Include the bounded 12-artifact spine |
| Navigation complexity | Multiple doc families can confuse new readers | Assign each doc family a narrow purpose and document the reading path |
| Reviewer confusion | Readers can mistake curated/public for a mirror of canonical/private | Make the authority model explicit in the front door and current-state docs |

## 9. Recommended Assembly Blueprint

### Root
- `README.md`
- `AGENTS.md`
- `LICENSE`
- `NOTICE` only if required
- `pyproject.toml`
- `repo_paths.py`

### docs/current/
- `start_here.md`
- `current_status.md`
- `framework_vs_history.md`
- `housekeeping_status.md`

### docs/framework/
- doctrine and methodology files
- `lineages/README.md`
- the bounded historical evidence spine
- `process_infrastructure/` as the canonical process-support library
- selected methodology transition docs

### scripts/
- core regimen scripts only

### tests/
- public contract and regression tests only

### Excluded from version 1
- `data/`
- `evals/data/`
- `evals/runs/`
- `reports/`
- `manifests/runs/`
- `manifests/reports/`
- `manifests/environment/`
- `artifacts/`
- `local_review_bundles/`
- `configs/`
- `docs/research/`
- `docs/history/`
- bulk `docs/convergence/`
- bulk `docs/housekeeping/`
- `docs/continuity/` unless a later version explicitly needs an extra continuity bridge

## 10. Final Recommendation

Use the assembly blueprint above as the starting point for the curated/public repository.

The public repo should remain:
- method-first
- bounded
- navigable
- evidence-backed
- and clearly derived from the canonical/private source of truth

The historical evidence should be surfaced through a curated index and a small thematic spine, not through archive duplication. `AGENTS.md` should be retained as Public Supporting. Version 1 should avoid archive creep and preserve clarity for both human reviewers and Codex-for-OSS evaluators.
