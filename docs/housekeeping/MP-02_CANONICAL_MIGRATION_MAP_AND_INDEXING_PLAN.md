# Canonical Migration Map and Indexing Plan

## Work Package

- ID: `MP-02`
- Title: `Canonical Migration Map and Indexing Plan`
- Repository: `/opt/ai-stack/assistant-training`
- Scope: migration mapping and indexing design only
- Authority basis:
  - `docs/housekeeping/HOUSEKEEPING_PRESERVATION_INDEX.md`
  - `docs/housekeeping/HOUSEKEEPING_ARCHITECTURE_AND_MIGRATION_PLAN.md`
  - `docs/housekeeping/HOUSEKEEPING_PATH_DECOUPLING_AND_COMPATIBILITY_STRATEGY.md`
  - `docs/housekeeping/HOUSEKEEPING_COMPATIBILITY_LAYER_IMPLEMENTATION_PLAN.md`
  - `docs/housekeeping/MP-01_MIGRATION_PREPARATION_BOUNDARY_ASSESSMENT.md`
  - CL-01 implementation artifacts
  - CL-02 implementation artifacts
  - post-CL-02 migration readiness reassessment
- Out of scope:
  - file moves
  - archive creation
  - restructuring
  - code changes
  - doctrine changes
  - deletions
  - migration commits

## Current State Basis

- Stage B is complete.
- Stage C blocker-oriented branch is complete.
- Runtime-output / corpus-behavior investigation is defined but parked.
- Housekeeping phase is active.
- CL-01 reduced the active evaluator-chain path-coupling surface.
- CL-02 reduced default-path coupling in the core framework entrypoints.
- MP-01 established movement classes and the pre-move boundary.
- The repository is ready for migration preparation, but not ready for structural migration.

## Planning Principles

1. Index before move.
2. Preserve provenance before separation.
3. Keep executable compatibility and historical reference treatment distinct.
4. Do not rewrite frozen history to match future layout.
5. Structural movement is only authorized after canonical indexes, aliases, and validation coverage exist.

## A. Canonical Migration Map

### Movement Legend

- `Moveable`: could move in the next structural phase without major prerequisite work
- `Moveable With Preconditions`: may move later, but only after indexing, shims, or registry work
- `Archive Candidate`: should be preserved, but should leave the future primary path
- `Preserve In Place`: should remain where it is for the foreseeable future
- `Do Not Move`: movement would damage authority, provenance, or reusable framework value

### Major Repository Families

| Family | Current location | Future target location | MP-01 classification | Required preconditions | Migration dependencies |
|---|---|---|---|---|---|
| Doctrine and canonical authority | `AGENTS.md`, `docs/goal_charter_v5a.md`, `docs/appendix_a_operational_execution_contract_v3a.md`, `docs/metric_specification_v1a.md`, `evals/canonical_eval_manifest_v1.json` | Preserve in place for now; future doctrine packaging would be `docs/doctrine/` and `regimen/contracts/` only if later explicitly authorized | `Do Not Move` | None for preservation; future packaging would require a citation map and alias plan | Docs, manifests, tests, and evaluator tooling depend on these records as binding authority |
| Current navigation and housekeeping surface | `README.md`, `docs/current/`, `docs/housekeeping/README.md`, `docs/current/*.md` | Remain primary navigation surfaces; no structural move required for MP-02 | `Preserve In Place` | None beyond keeping current pointers accurate | Used by humans, not by runtime code |
| Core framework entrypoints and path compatibility shim | `scripts/train_lora_sft.py`, `scripts/preflight_lora_run.py`, `scripts/build_dataset_v1.py`, `scripts/eval_canonical_manifest.py`, `scripts/repo_paths.py`, `repo_paths.py` | `regimen/core/`, `regimen/eval/`, `regimen/contracts/`, or equivalent extracted framework area | `Moveable With Preconditions` | Shared resolver, alias wrappers, stable module entrypoints, path-audit coverage, updated tests | Current scripts, direct tests, docs, and manifest references |
| Active evaluator chain | `scripts/stage_c1_evaluator_foundation.py`, `scripts/stage_c3_evaluator_runtime_integration.py`, `scripts/stage_c4_real_output_ingestion.py`, `scripts/stage_c5_scoring_path_integration.py`, `scripts/stage_c6_scoring_report_integration.py`, `scripts/stage_c8_non_authoritative_detector_projection_adapter.py`, and direct tests for those surfaces | `regimen/eval/foundations/`, `regimen/eval/integration/`, or equivalent extracted framework area | `Moveable With Preconditions` | Fixture/sample registry, stable sample IDs, loader shims or stable entrypoints, direct test updates, canonical sample-artifact index | Current report-tree inputs, WP8 fixture corpus, threshold profile, direct test coverage |
| Active fixtures and sample artifacts | `manifests/reports/stage_b_wp8_validation/fixtures/`, `manifests/reports/stage_b_v1_threshold_profile.json`, `reports/stage_c4/input/`, `reports/stage_c5/input/`, `reports/stage_c6/input/`, `reports/stage_c3-6/*_artifacts` | `fixtures/wp8_validation/`, `fixtures/threshold_profiles/`, `fixtures/stage_c_samples/`, with preserved historical originals in `history/reports/` | `Moveable With Preconditions` | Fixture registry, sample registry, provenance manifest, stable IDs, hash validation, active-consumer inventory | Active evaluator chain, Stage C tests, report consumers |
| Framework-process assets | `docs/process_infrastructure/`, `docs/lineages/`, selected `docs/convergence/*` synthesis and status docs | `docs/framework/process_infrastructure/`, `docs/framework/lineages/`, `docs/framework/methodology/`, and `docs/current/` for current-state pointers | `Moveable With Preconditions` | Canonical record index, navigation pointers, citation map, high-citation redirect plan | `AGENTS.md`, current navigation docs, selected convergence references |
| Historical convergence history | bulk `docs/convergence/` package records, acceptance assessments, implementation summaries, validation reports, and companion determinations not listed as selected framework synthesis | `history/projects/llama31_8b_base/convergence/` plus `history/archive/convergence/` as needed | `Archive Candidate` | Convergence canonical index, record IDs, old-path map, redirect stubs for high-citation records | Framework synthesis docs, current status docs, historical reference links |
| Historical run history and manifests | `configs/lora/`, `manifests/runs/`, bulk `manifests/reports/`, `data/v1_0/`, `data/tool_ft_allaliases_*` | `history/projects/llama31_8b_base/configs/`, `history/projects/llama31_8b_base/run_manifests/`, `history/projects/llama31_8b_base/data/v1_0/`, `history/reports/` | `Archive Candidate` | Run-history index, manifest index, provenance crosswalk, example-subset selection, no active consumer on moved-only path | Dataset contract tests, docs references, serious-run examples, reproducibility records |
| Blocker-branch methodology record | `scripts/stage_c_package*`, `scripts/stage_c_technical_spike_*`, `scripts/stage_c_runtime_output_forensics_*`, `scripts/stage_c_legacy_surface_validity_*`, related tests | `history/projects/llama31_8b_base/stage_c_blocker_branch/` or `history/archive/stage_c_blocker_branch/` | `Archive Candidate` | Package index, evidence map, dependency inventory, no active runtime callers | Historical methodology docs and evidence bundles |
| Local-only operational residue | `artifacts/`, `evals/runs/`, caches, `local_review_bundles/`, empty `staging/assistant-runtime/` | No tracked future target; keep local-only or remove later under separate cleanup | `Preserve In Place` | None for migration; cleanup decisions are separate | None for future tracked structure |

## B. Indexing Requirements

### Required Indexes

| Index | Scope | Minimum fields | Must exist before movement |
|---|---|---|---|
| Convergence history index | `docs/convergence/` package records and related transition material | `record_id`, `package_id`, `record_type`, `current_path`, `proposed_path`, `status`, `summary`, `primary_reference`, `related_records`, `preservation_note` | Yes, before any bulk convergence move or archive formation |
| Reports index | `manifests/reports/`, `reports/stage_c*`, historical report bundles | `report_id`, `run_id`, `family`, `current_path`, `future_path`, `role`, `hash`, `consumer`, `provenance_note` | Yes, before any report move, report split, or archive formation |
| Manifests index | `manifests/runs/`, `configs/lora/`, `evals/canonical_eval_manifest_v1.json`, related runtime manifests | `manifest_id`, `run_id`, `config_family`, `current_path`, `future_path`, `authority_level`, `hash`, `resolved_runtime_path`, `recorded_source_path` | Yes, before any manifest family move |
| Fixture index | `manifests/reports/stage_b_wp8_validation/fixtures/`, `manifests/reports/stage_b_v1_threshold_profile.json`, reusable fixture bundles | `fixture_id`, `current_path`, `hash`, `content_scope`, `active_consumer`, `source_path`, `canonical_path`, `provenance_link` | Yes, before any active fixture move |
| Sample-artifact index | `reports/stage_c4/input/`, `reports/stage_c5/input/`, `reports/stage_c6/input/`, promoted sample bundles | `sample_id`, `source_report_id`, `current_path`, `canonical_path`, `hash`, `consumer`, `promotion_reason`, `source_bundle` | Yes, before any sample-artifact move or promotion |
| Archive index | `history/archive/`, `history/reports/`, future archive surfaces | `archive_id`, `source_family`, `current_path`, `future_path`, `original_path`, `reason_for_archive`, `redirect_target`, `related_index_entries` | Yes, before archive creation begins |

### Index Coverage Rules

1. Every family classified as `Moveable With Preconditions` or `Archive Candidate` must have at least one canonical index entry before movement.
2. Every family with high-citation documents or direct runtime consumers must have a forward and backward crosswalk.
3. Every extracted fixture or sample artifact must retain a link back to its source artifact.
4. No archive entry is valid unless it names the preserved original path and the discoverability path.

## C. Redirect And Compatibility Requirements

| Surface class | Required treatment | Examples | Notes |
|---|---|---|---|
| Moved executable surfaces | Compatibility shims | `scripts/train_lora_sft.py`, `scripts/preflight_lora_run.py`, `scripts/build_dataset_v1.py`, `scripts/eval_canonical_manifest.py`, Stage C active scripts | Preserve CLI behavior and old entrypoints until direct callers are fully migrated |
| Moved active evaluator chain | Shims plus stable entrypoints | `scripts/stage_c1_evaluator_foundation.py`, `scripts/stage_c3...stage_c8` | Dynamic loader assumptions must be removed or isolated behind wrappers |
| Moved fixture/sample surfaces | Alias preservation plus registry lookup | WP8 fixtures, threshold profile, `reports/stage_c4-6` sample inputs | Active consumers should resolve by ID or registry entry, not by old path literal |
| Moved high-citation documentation | Redirects or alias pages | selected `docs/convergence/*`, `docs/process_infrastructure/*`, `docs/lineages/*` | Documentation must remain discoverable through old and new paths during transition |
| Moved archive/history surfaces | Alias preservation in indexes | bulk `docs/convergence/`, `manifests/reports/`, `configs/lora/`, `manifests/runs/`, `data/v1_0/` | Historical records should remain readable at original paths in provenance records, but not be the active navigation target |
| Surfaces that remain in place | No compatibility treatment | `README.md`, `AGENTS.md`, `docs/current/`, `docs/housekeeping/`, local-only residue | Keep simple; add pointers, not shims |

### Compatibility Rules

1. Scripts and tests keep CLI and behavior compatibility first, path compatibility second.
2. Historical records retain original path strings as evidence, not as runtime instructions.
3. Redirects are for discoverability; shims are for executable continuity; aliases are for registry continuity.
4. No compatibility treatment is required for surfaces that are intentionally preserved in place.

## D. Migration Wave Plan

### Wave 0: Navigation And Index Foundation

- Objective: establish canonical entry points and index surfaces before any file movement.
- Scope: `docs/current/`, `docs/housekeeping/`, canonical convergence/report/manifest/fixture/sample/archive indexes, and crosswalk documents.
- Prerequisites: MP-02 acceptance, current classification stable, no open ambiguity about source roles.
- Validation requirements:
  - link audit for navigation documents
  - index completeness check
  - sample crosswalk check for each major family
- Rollback considerations:
  - revert only the new navigation and index documents
  - no content movement to unwind

### Wave 1: Framework / History Separation

- Objective: separate reusable framework material from project history.
- Scope: `docs/process_infrastructure/`, `docs/lineages/`, selected `docs/convergence/*` synthesis and status docs, and top-level navigation pointers.
- Prerequisites:
  - canonical convergence index
  - redirect plan for high-citation docs
  - selected framework record set approved
- Validation requirements:
  - documentation link audit
  - current-state navigation check
  - high-citation reference check
- Rollback considerations:
  - restore original pointers and alias pages if any link check fails

### Wave 2: Fixture / Sample Separation

- Objective: move active fixtures and sample artifacts onto stable registry-driven surfaces.
- Scope: WP8 fixture corpus, threshold profile, `reports/stage_c4-6` sample inputs, and any promoted canonical sample bundles.
- Prerequisites:
  - fixture registry
  - sample-artifact registry
  - provenance manifest
  - active-consumer inventory
- Validation requirements:
  - checksum verification
  - consumer test pass
  - registry resolution pass
  - source-to-canonical equivalence check where exact copy is intended
- Rollback considerations:
  - restore original fixture/sample path bindings
  - keep historical originals intact

### Wave 3: Archive Formation

- Objective: move bulk historical evidence and superseded records off the primary path.
- Scope: bulk `docs/convergence/`, `manifests/reports/`, `configs/lora/`, `manifests/runs/`, `data/v1_0/`, blocker-branch scripts/tests, and archive candidates identified by MP-01.
- Prerequisites:
  - convergence, report, manifest, fixture, sample, and archive indexes
  - redirect or alias coverage for moved items with active references
  - no unresolved active consumer on a moved-only path
- Validation requirements:
  - provenance lookup
  - archived record discoverability
  - targeted test and path-audit pass for any still-active consumers
- Rollback considerations:
  - restore archive aliases and discoverability map
  - re-expose original locations if a preserved evidence chain becomes ambiguous

## E. Archive Formation Prerequisites

Archive creation can begin only when all of the following are true:

1. The canonical migration map is accepted and frozen for planning.
2. All archive candidates have stable IDs and index entries.
3. Convergence, report, manifest, fixture, sample, and archive indexes exist.
4. Redirects or aliases are defined for any preserved active consumer.
5. The source-to-target provenance crosswalk exists for every archive family.
6. Example subsets have been identified where a historical family also needs a reusable reference slice.
7. No archived-only path is required by an active evaluator, training script, or test without a compatibility layer.
8. Archive discoverability is documented from the future primary navigation path.

## F. Migration Planning Readiness Assessment

### Determination

After MP-02, the repository will be ready for the first migration-planning package.

### What This Means

- Ready for:
  - wave-by-wave migration planning
  - alias and redirect planning
  - index implementation planning
  - fixture/sample extraction planning
  - archive boundary planning
- Not ready for:
  - direct structural moves
  - archive creation
  - pruning or deletion
  - blanket path rewrites

### Why The Repository Is Ready For Planning

- MP-01 already defined the move classes and boundary rules.
- H-01 and H-02 define what must stay primary and what may become history.
- H-03 and H-05 define the compatibility preconditions.
- CL-01 and CL-02 reduced the active path-coupling surface enough to support a canonical migration map.
- The remaining blockers are now boundary and indexing problems, not unresolved compatibility design problems.

### Boundary Statement

MP-02 does not authorize any move.

It establishes the canonical migration map, the indexes required before movement, and the redirect/compatibility rules that future structural housekeeping must satisfy.
