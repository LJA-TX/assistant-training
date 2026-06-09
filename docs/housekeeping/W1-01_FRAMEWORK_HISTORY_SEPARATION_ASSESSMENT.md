# Framework History Separation Assessment

## Work Package

- ID: `W1-01`
- Title: `Framework-History Separation Planning Assessment`
- Repository: `/opt/ai-stack/assistant-training`
- Scope: Wave 1 planning only
- Authority basis:
  - `docs/housekeeping/HOUSEKEEPING_PRESERVATION_INDEX.md`
  - `docs/housekeeping/HOUSEKEEPING_ARCHITECTURE_AND_MIGRATION_PLAN.md`
  - `docs/housekeeping/HOUSEKEEPING_PATH_DECOUPLING_AND_COMPATIBILITY_STRATEGY.md`
  - `docs/housekeeping/HOUSEKEEPING_COMPATIBILITY_LAYER_IMPLEMENTATION_PLAN.md`
  - `docs/housekeeping/MP-01_MIGRATION_PREPARATION_BOUNDARY_ASSESSMENT.md`
  - `docs/housekeeping/MP-02_CANONICAL_MIGRATION_MAP_AND_INDEXING_PLAN.md`
  - `docs/housekeeping/W0-01_CANONICAL_INDEX_FRAMEWORK_DESIGN.md`
  - `docs/housekeeping/W0-02_CANONICAL_INDEX_INFRASTRUCTURE_IMPLEMENTATION.md`
  - `docs/housekeeping/W0-03_INDEX_POPULATION_STRATEGY_AND_SCOPE_DETERMINATION.md`
  - `docs/housekeeping/W0-04` anchor population artifacts
- Out of scope:
  - file moves
  - archive creation
  - restructuring
  - code changes
  - doctrine changes
  - migration execution

## Current State Basis

- Wave 0 objectives are substantially complete.
- Compatibility foundations exist.
- Migration boundaries are defined.
- Canonical migration mapping exists.
- Canonical indexes exist.
- Migration-critical anchors exist.
- No structural migration has occurred.

## Planning Principles

1. Separate the obvious framework surfaces first.
2. Keep provenance-heavy history out of the first wave unless it is structurally necessary.
3. Do not collapse ambiguous synthesis records into the same bucket as bulk history without a crosswalk.
4. The first wave should reduce confusion before it tries to reduce volume.
5. If a surface still feeds active consumers, treat it as active infrastructure until the consumer contract is decoupled.

## A. Framework-History Boundary Reassessment

### Framework Assets

These surfaces are already acting as reusable framework material or current navigation support:

- `AGENTS.md`
- `docs/goal_charter_v5a.md`
- `docs/appendix_a_operational_execution_contract_v3a.md`
- `docs/metric_specification_v1a.md`
- `evals/canonical_eval_manifest_v1.json`
- `evals/data/canonical_v1/`
- `docs/process_infrastructure/`
- `docs/lineages/`
- `docs/current/`
- `docs/housekeeping/`
- selected current-state and synthesis convergence records:
  - `docs/convergence/STAGE_B_COMPLETION_DETERMINATION.md`
  - `docs/convergence/STAGE_BC_PROCESS_EXTRACTION_ASSESSMENT.md`
  - `docs/convergence/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md`
  - `docs/convergence/STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md`
  - `docs/convergence/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md`

### History Assets

These surfaces are clearly historical evidence or provenance-heavy lineage records:

- bulk `docs/convergence/` package records outside the selected framework/current-state set
- `docs/continuity/`
- `docs/history/`
- `configs/lora/`
- `manifests/runs/`
- bulk `manifests/reports/`
- `data/v1_0/`
- `data/tool_ft_allaliases_*`
- blocker-branch methodology scripts and related tests:
  - `scripts/stage_c_package*`
  - `scripts/stage_c_technical_spike_*`
  - `scripts/stage_c_runtime_output_forensics_*`
  - `scripts/stage_c_legacy_surface_validity_*`

### Ambiguous Assets

These surfaces are mixed or transitional and should be treated cautiously:

- selected `docs/convergence/*` synthesis docs: they are history records that now function as framework guidance
- `reports/stage_c1/` through `reports/stage_c6/`: they are historical report families that still serve as active sample inputs and baseline artifacts
- `manifests/reports/stage_b_wp8_validation/fixtures/` and `manifests/reports/stage_b_v1_threshold_profile.json`: historically named, but active framework fixtures
- `docs/assistant_training_goal_documents_and_artifacts_index.md`: bootstrap/history surface with current navigational value
- `docs/process_infrastructure/`: framework asset, but still referenced by the current authority order and route logic

## B. Movement Candidate Assessment

### First Wave Candidate Families

The first framework-history separation wave should include only the families that are already framework-facing or can be cleanly split without touching provenance-heavy evidence bundles:

1. `docs/process_infrastructure/`
2. `docs/lineages/`
3. selected `docs/convergence/` synthesis and status records
4. `docs/current/` navigation pointers, if they need to be repointed to the new framework/history layout

### Deferred But Related Families

These families should be part of later waves, not the first separation wave:

- `docs/continuity/`
- `docs/history/`
- `configs/lora/`
- `manifests/runs/`
- bulk `manifests/reports/`
- `data/v1_0/`
- `reports/stage_c1/` through `reports/stage_c6/`

### Not Good First-Wave Candidates

- blocker-branch methodology scripts and tests
- bulk convergence history
- local review bundles
- generated or cache-only surfaces

## C. Dependency Risk Assessment

| Candidate family | Active workflow risk | Active evaluator risk | Active training risk | Provenance risk | Rollback complexity |
|---|---|---|---|---|---|
| `docs/process_infrastructure/` | Low | None | None | Low | Low |
| `docs/lineages/` | Low | None | None | Low | Low |
| selected `docs/convergence/` synthesis/current-state docs | Low to medium | None | None | Medium | Medium |
| `docs/current/` navigation pointers | Low | None | None | Low | Low |
| `docs/continuity/` | None to low | None | None | Medium | Medium |
| `docs/history/` | None | None | None | Medium | Medium |
| `configs/lora/` | Low | None | Low | High | High |
| `manifests/runs/` | Low | None | Low | High | High |
| bulk `manifests/reports/` | Low | Low | Low | High | High |
| `data/v1_0/` | Low | None | High | High | High |
| `reports/stage_c1/` through `reports/stage_c6/` | Medium | Medium | Low | High | High |

### Risk Interpretation

- The low-risk surface is the documentation framework layer.
- The moderate-risk surface is the selected synthesis convergence layer.
- The high-risk surface is the provenance-heavy run/config/data/report layer.
- The first wave should avoid the high-risk surfaces unless a later implementation package explicitly needs them.

## D. Wave 1 Scope Options

### 1. Minimal Separation Wave

- Move or re-home only `docs/process_infrastructure/`, `docs/lineages/`, and selected `docs/convergence/` synthesis/current-state docs into the future framework-facing layout.
- Leave bulk history, run manifests, historical datasets, and report bundles in place.
- Add redirects or index pointers so the current navigation layer still resolves.

### 2. Moderate Separation Wave

- Do everything in the minimal wave.
- Also separate `docs/continuity/`, `docs/history/`, and bootstrap history docs into a history-oriented layout.
- Keep provenance-heavy configs, manifests, datasets, and report bundles in place for later waves.

### 3. Aggressive Separation Wave

- Do everything in the moderate wave.
- Also move `configs/lora/`, `manifests/runs/`, `data/v1_0/`, bulk `manifests/reports/`, and report families like `reports/stage_c1/` through `reports/stage_c6/`.
- This would touch the most provenance-sensitive material and has the highest rollback cost.

## E. Recommended Wave 1 Plan

### Recommendation

Use the minimal separation wave.

### Why This Is The Safest Practical Scope

- It separates the clearest framework assets first.
- It leaves the provenance-heavy history where it is until the framework boundary is proven stable.
- It avoids forcing early movement of run history, dataset lineage, or report bundles that still support active understanding.
- It keeps rollback small and mostly documentation-based.
- It creates a framework/history distinction that future waves can extend instead of re-litigating the whole repository.

### Practical Wave 1 Sequence

1. Repoint the current navigation layer to a framework-first and history-first split.
2. Separate `docs/process_infrastructure/` and `docs/lineages/` into a future framework surface.
3. Re-home selected `docs/convergence/` synthesis and status docs into a framework/current surface or a clearly indexed history-with-canonical-summary layout.
4. Add alias or redirect stubs for the old navigation paths.
5. Stop and validate before considering continuity, deprecated doctrine, or provenance-heavy evidence families.

## F. Readiness Determination

### Determination

The repository is ready for Wave 1 migration planning.

The repository is also ready for Wave 1 migration implementation planning, but only for the minimal separation wave.

The repository is not ready for direct Wave 1 structural execution.

### Why

- Wave 0 has already given the repository the classification, mapping, indexing, and anchor infrastructure needed to plan the first separation wave.
- The framework/history boundary is now clear enough to plan a first wave without guessing at the repository's role split.
- The provenance-heavy families are still too connected to the current evidence chain to include in an aggressive first wave.

### Boundary Statement

Wave 1 should be a framework-first documentation and navigation separation, not a broad history relocation exercise.

The safest practical scope is the minimal separation wave.
