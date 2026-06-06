# Migration Preparation Boundary Assessment

## Work Package

- ID: `MP-01`
- Title: `Migration Preparation Boundary Definition`
- Repository: `/opt/ai-stack/assistant-training`
- Scope: migration boundary assessment and preservation planning only
- Authority basis:
  - `docs/housekeeping/HOUSEKEEPING_PRESERVATION_INDEX.md`
  - `docs/housekeeping/HOUSEKEEPING_ARCHITECTURE_AND_MIGRATION_PLAN.md`
  - `docs/housekeeping/HOUSEKEEPING_PATH_DECOUPLING_AND_COMPATIBILITY_STRATEGY.md`
  - `docs/housekeeping/HOUSEKEEPING_COMPATIBILITY_LAYER_IMPLEMENTATION_PLAN.md`
  - CL-01 implementation artifacts
  - CL-02 implementation artifacts
  - post-CL-02 migration readiness reassessment
- Out of scope:
  - file moves
  - directory creation
  - restructuring
  - archival actions
  - code changes

## Current State Basis

- CL-01 reduced the active evaluator-chain path-coupling surface.
- CL-02 reduced default-path coupling in the core framework entrypoints.
- Compatibility-layer expansion now has diminishing returns.
- The repository is ready for migration preparation, but not ready for structural migration.
- This document defines the boundary before any structural movement is authorized.

## Assessment Summary

The repository has three different move classes:

1. active framework surfaces that may eventually move, but only with compatibility and indexing preconditions
2. historical evidence surfaces that should be preserved and later archived, not treated as current framework
3. authoritative doctrine and canonical contracts that should stay fixed in place

The safest boundary is:

- do not move doctrine or canonical contracts
- do not move active fixtures or samples until a registry/index exists
- do not move active scripts/tests until shims or stable entrypoints exist
- archive historical evidence only after canonical indexes and citation maps exist

## A. Movement Classification

### Classification Legend

- `Moveable`: could move in the next structural phase without major prerequisite work
- `Moveable With Preconditions`: may move later, but only after indexing, shims, or registry work
- `Archive Candidate`: should be preserved, but should leave the future primary path
- `Preserve In Place`: should remain where it is for the foreseeable future
- `Do Not Move`: movement would damage authority, provenance, or reusable framework value

### Major Repository Families

| Family | Classification | Rationale | Affected surfaces |
|---|---|---|---|
| Doctrine and canonical authority | `Do Not Move` | These are the binding rules and canonical contracts for the repository. Moving them would weaken authority and increase citation fragility. | `AGENTS.md`, `docs/goal_charter_v5a.md`, `docs/appendix_a_operational_execution_contract_v3a.md`, `docs/metric_specification_v1a.md`, `evals/canonical_eval_manifest_v1.json` |
| Current navigation and housekeeping surface | `Preserve In Place` | The navigation layer is intentionally the first stable front door. It should remain fixed while the migration boundary is defined. | `README.md`, `docs/current/`, `docs/housekeeping/README.md`, `docs/current/*.md` |
| Core framework entrypoints and compatibility shim | `Moveable With Preconditions` | These can eventually become a `regimen/` or equivalent extracted core, but only after path shims, package boundaries, and external references are stabilized. | `scripts/train_lora_sft.py`, `scripts/preflight_lora_run.py`, `scripts/build_dataset_v1.py`, `scripts/eval_canonical_manifest.py`, `scripts/repo_paths.py`, `repo_paths.py` |
| Active evaluator chain | `Moveable With Preconditions` | The active evaluator chain is now decoupled enough to plan movement, but it still depends on stable registries, sample-artifact indexes, and wrapper compatibility. | `scripts/stage_c1_evaluator_foundation.py`, `scripts/stage_c3_evaluator_runtime_integration.py`, `scripts/stage_c4_real_output_ingestion.py`, `scripts/stage_c5_scoring_path_integration.py`, `scripts/stage_c6_scoring_report_integration.py`, `scripts/stage_c8_non_authoritative_detector_projection_adapter.py`, direct tests for those surfaces |
| Active fixtures and sample artifacts | `Moveable With Preconditions` | These are active infrastructure, but they still serve as live inputs. They should move only after a fixture/sample registry and canonical IDs exist. | `manifests/reports/stage_b_wp8_validation/fixtures/`, `manifests/reports/stage_b_v1_threshold_profile.json`, `reports/stage_c4/input/`, `reports/stage_c5/input/`, `reports/stage_c6/input/`, `reports/stage_c3-6/*_artifacts` |
| Framework-process assets | `Moveable With Preconditions` | Reusable process material can move into framework surfaces, but only after the current doc and navigation indexes are in place. | `docs/process_infrastructure/`, `docs/lineages/` |
| Selected current-state and synthesis docs | `Moveable With Preconditions` | These are candidates for `docs/framework/` or `docs/current/` consolidation, but they need a canonical record map first. | selected `docs/convergence/*` synthesis and status documents |
| Historical convergence records | `Archive Candidate` | These preserve the project evidence chain and should be separated from future primary navigation once canonical indexes exist. | bulk `docs/convergence/` package records, acceptance assessments, implementation summaries, validation reports |
| Historical run intent and evidence | `Archive Candidate` | These are needed for provenance and reproducibility, but they are not primary framework surfaces. | `configs/lora/`, `manifests/runs/`, bulk `manifests/reports/`, `data/v1_0/`, `data/tool_ft_allaliases_*` |
| Blocker-branch methodology record | `Archive Candidate` | These documents and scripts explain how the blocker-oriented branch was exercised. They should be preserved, but not kept on the future main path. | `scripts/stage_c_package*`, `scripts/stage_c_technical_spike_*`, `scripts/stage_c_runtime_output_forensics_*`, `scripts/stage_c_legacy_surface_validity_*`, related tests |
| Local-only operational residue | `Preserve In Place` | These are not migration targets; they are local working artifacts or cache surfaces. | `artifacts/`, `evals/runs/`, caches, `local_review_bundles/`, empty staging residue |

## B. Provenance Protection Assessment

### Assets Whose Movement Could Damage Provenance

| Asset family | Why movement is risky | Required protections |
|---|---|---|
| Doctrine authority | They encode binding governance and scoring semantics. | Keep canonical copies fixed, preserve links, and add aliases or redirects before any move. |
| `configs/lora/`, `manifests/runs/` | They prove what was intended to run and how a run was parameterized. | Preserve original records, add relocation metadata rather than rewriting content, and avoid mass edits. |
| `data/v1_0/` | It is lineage evidence for Stage A/B. | Preserve original dataset snapshots, keep hashable references, and avoid rewriting content. |
| `manifests/reports/` bulk history | It contains the evidence chain for decisions, gates, and runtime outcomes. | Preserve source paths, create canonical indexes, and only move after reference maps exist. |
| `docs/convergence/` bulk history | It contains the project execution log and decision trail. | Preserve original file content and add a canonical record index before any separation. |
| `docs/continuity/` and `docs/deprecated/` | They preserve handoff history and doctrine evolution. | Keep immutable history references and avoid reinterpreting old path strings as current targets. |
| `data/tool_ft_allaliases_*` | Runtime paths inside the data are part of the training evidence. | Treat path strings as data content, not as migration instructions. |

### Required Protections

1. Preserve original path strings in historical evidence.
2. Distinguish recorded provenance from current runtime resolution.
3. Keep canonical indexes for moved or archived families.
4. Use redirects, wrappers, or alias files for any moved active surface.
5. Do not rewrite historical records merely to match the future layout.

## C. Fixture And Sample Boundary Assessment

### Active Fixtures

- `manifests/reports/stage_b_wp8_validation/fixtures/`
- `manifests/reports/stage_b_v1_threshold_profile.json`
- `reports/stage_c4/input/stage_c4_sample_output_records.jsonl`
- `reports/stage_c5/input/stage_c5_sample_output_records.jsonl`
- `reports/stage_c6/input/stage_c6_sample_output_records.jsonl`

These are active infrastructure, not mere history, because they still feed active scripts and tests.

### Historical Fixtures Or Historical Evidence

- bulk `manifests/reports/` outputs outside the active fixture/profile surfaces
- `reports/stage_c3/contract_artifacts`
- `reports/stage_c4/contract_artifacts`
- `reports/stage_c5/contract_artifacts`
- `reports/stage_c6/reporting_artifacts`
- `reports/stage_c8/projection_artifacts`

These should be preserved as evidence until a canonical sample-artifact registry exists.

### Boundary Requirement Before Movement

Before any fixture or sample artifact is moved:

- a fixture registry must exist
- sample artifacts must have stable IDs
- the active evaluator chain must resolve by role, not by path literal
- historical sample outputs must be indexed separately from reusable fixtures
- tests must be able to distinguish active sample inputs from historical report bundles

## D. Manifest And Report Boundary Assessment

### What May Eventually Move

- selected active sample artifacts currently living in `reports/stage_c4/input/`, `reports/stage_c5/input/`, and `reports/stage_c6/input/`
- selected reusable fixtures currently embedded in `manifests/reports/`
- selected canonical examples extracted from `configs/lora/`, `manifests/runs/`, and `data/v1_0/`

### What Should Remain Authoritative

- doctrine docs
- canonical eval manifest
- pinned eval corpora
- current navigation and housekeeping docs
- current compatibility helper surfaces

### What Requires Compatibility Treatment

- Stage C active scripts and tests
- direct module-loading wrappers
- any script or test that still consumes `reports/stage_c*` as if it were an active source of truth
- any run manifest or config that still hard-codes the present layout

### What Requires Historical Preservation Treatment

- bulk convergence reports
- run-specific manifests and report bundles
- continuity and deprecated doctrine records
- Stage B builder and validator history
- blocker-branch evidence packages

## E. Migration Sequencing Recommendations

### Recommended Sequence

1. Navigation moves
   - create or refine canonical entrypoints and index pages
   - make current-state, framework, and history navigation obvious

2. Framework/history separation
   - split reusable framework guidance from project history
   - create canonical indexes for convergence, reports, and history families

3. Fixture/sample separation
   - assign stable IDs to active fixtures and sample outputs
   - move active sample data only after registry/index support exists

4. Archive formation
   - move bulk evidence, history, and superseded materials into archive surfaces
   - preserve links and provenance references from the old locations

### Why This Order

- navigation first reduces user confusion without altering evidence
- framework/history separation reduces clutter before bulk moves
- fixture/sample separation is required before moving active evaluator inputs
- archive formation should happen last because it depends on stable indexes and compatibility boundaries

## F. Structural Migration Readiness Assessment

### What Must Still Happen Before The First Structural Move Can Be Authorized

- a canonical migration map for moveable families
- a fixture/sample registry for active evaluator inputs
- canonical indexes for convergence, reports, and history families
- compatibility shims or stable entrypoints for any moved executable surface
- a validated path for historical references so they remain discoverable after movement
- a clear rule for preserving provenance records without rewriting them

### Readiness Determination

- The repository is approaching readiness for migration planning.
- It is not ready to authorize the first structural move yet.
- Additional compatibility expansion now has diminishing returns; the next leverage point is boundary definition, indexing, and migration sequencing rather than more path-resolution work.

## Boundary Statement

MP-01 defines the boundary for future structural housekeeping.

It does not authorize any move, archive action, or restructuring step.

It establishes the rule that:

- doctrine stays fixed
- active evaluator inputs move only after registry/index support exists
- historical evidence stays preserved until canonical archive boundaries are defined
- compatibility work should stop expanding once it no longer materially reduces migration blockers
