# Repository Architecture and Migration Plan

## Work Package

- ID: `H-02`
- Title: `Repository Architecture and Migration Plan`
- Repository: `/opt/ai-stack/assistant-training`
- Scope: planning and migration design only
- Governing classification input: `docs/housekeeping/HOUSEKEEPING_PRESERVATION_INDEX.md`
- Additional authority inputs:
  - accepted housekeeping assessments
  - current repository state
- Out of scope:
  - file moves
  - directory creation
  - archival actions
  - deletions
  - doctrine modifications
  - migration commits

## Current State Basis

- Stage B complete.
- Stage C blocker-oriented branch complete.
- Runtime-output / corpus-behavior investigation family defined and parked.
- Housekeeping phase active.
- H-01 is treated as the governing classification map for all architecture and migration recommendations in this document.

## Planning Principles

1. Preservation comes before simplification.
2. Future navigation must separate framework from project history.
3. Current executable and test dependencies take precedence over aesthetic restructuring.
4. Structural moves must follow path-decoupling work where hard-coded references exist.
5. No proposed move is valid if it weakens doctrine, reproducibility, provenance, or methodology extraction.

## A. Target Repository Architecture

### 1. Primary Navigation Surfaces

Proposed future primary navigation surfaces:

- `README.md`
- `AGENTS.md`
- `docs/current/`
- `docs/doctrine/`
- `docs/framework/`
- `regimen/`
- `examples/`

Rationale:

- These surfaces should answer four first-order questions quickly:
  - what this repository is
  - what governs it
  - how to use the reusable regimen
  - where project history lives
- The current repository mixes those concerns across `docs/convergence/`, `manifests/reports/`, `reports/`, and flat `scripts/`, which creates high navigation cost for future reuse.

### 2. Doctrine Surfaces

Proposed future doctrine area:

- `docs/doctrine/`

Contents intended for this area:

- charter
- operational appendix
- metric specification
- doctrine version pointers and compatibility notes

Rationale:

- Doctrine is binding authority and should be isolated from both implementation details and project history.
- H-01 identifies these surfaces as critical and never-removable.

### 3. Framework / Regimen Surfaces

Proposed future framework area:

- `regimen/`
- `docs/framework/`

Recommended split:

- `regimen/`
  - executable reusable core
  - contracts
  - evaluation package
  - dataset and preflight tooling
  - process assets that must remain close to execution
- `docs/framework/`
  - lineages
  - reusable methodology syntheses
  - process infrastructure guides
  - current framework maps and operator guidance

Rationale:

- The repo now contains a real reusable product, not just execution history.
- The reusable product is partly documentary and partly executable; separating those layers makes extraction and reuse easier.

### 4. History Surfaces

Proposed future history area:

- `history/`
- `history/projects/llama31_8b_base/`
- `history/reports/`

Contents intended for this area:

- bulk convergence package history
- per-run configs and run manifests
- project-specific dataset lineage
- bootstrap and establishment documents
- continuity snapshots
- deprecated doctrine versions
- historical run-report inventories

Rationale:

- The repository should preserve the full Llama-centered research record, but that record should not dominate future primary navigation.
- History remains essential for provenance, but it is not the same thing as the reusable framework.

### 5. Archive Surfaces

Proposed future archive area:

- `history/archive/`
- `history/archive/convergence/`
- `history/archive/review_bundles/`

Contents intended for this area:

- companion acceptance assessments
- implementation summaries
- review bundles
- dormant proposals
- superseded bootstrap indexes

Rationale:

- Some material should remain preserved but no longer appear as live framework or active history.
- Archive should be explicit so later users do not confuse retained evidence with active guidance.

### 6. Fixture Surfaces

Proposed future fixture area:

- `fixtures/`
- or `regimen/fixtures/`

Contents intended for this area:

- WP8 validation fixture corpus
- threshold profile
- stable sample output records currently embedded in `reports/stage_c*`
- canonical reusable sample artifact bundles

Rationale:

- Fixtures are framework inputs, not historical reports.
- Today, key fixtures live inside `manifests/reports/` and `reports/stage_c*`, which obscures their role and increases migration risk.

### 7. Examples Surfaces

Proposed future examples area:

- `examples/minimal/`
- `examples/reference/`

Contents intended for this area:

- minimal serious-run example
- reference config and manifest examples
- reference dataset and leakage metadata examples
- reference eval-manifest instance examples

Rationale:

- Current examples are embedded inside project-specific history.
- A reusable regimen needs a first-class example path that does not require reading Stage B or Stage C history.

### 8. Proposed High-Level Target Layout

This is a planning model only:

```text
/
  README.md
  AGENTS.md
  regimen/
  fixtures/
  examples/
  docs/
    current/
    doctrine/
    framework/
    housekeeping/
  history/
    projects/
    reports/
    archive/
```

## B. Migration Map

| Current family | Proposed future location | Preservation rationale | Migration complexity | Dependency considerations |
|---|---|---|---|---|
| `README.md` | `README.md` plus links into `docs/current/` and `docs/framework/` | Primary front door should remain stable | Low | Mostly documentation references |
| `AGENTS.md` | `AGENTS.md` | Keep stable as top-level dispatcher and authority surface | Low | Referenced by process work, not runtime code |
| `docs/goal_charter_v5a.md`, `docs/appendix_a_operational_execution_contract_v3a.md`, `docs/metric_specification_v1a.md` | `docs/doctrine/` | Critical doctrine authority should be isolated | Medium | Docs and some manifests refer to current paths |
| `docs/process_infrastructure/` | `docs/framework/process_infrastructure/` or `regimen/process/` | Reusable process assets should stay prominent | Medium | `AGENTS.md` references current paths; route table would need coordinated update later |
| `docs/lineages/` | `docs/framework/lineages/` | Distilled methodology should remain primary framework guidance | Low | Mostly docs references |
| Selected synthesis docs in `docs/convergence/` | `docs/framework/methodology/` or `docs/current/status/` | These are reusable methodology and current-state records | Medium | Many internal doc links would need remapping |
| Bulk `docs/convergence/` | `history/projects/llama31_8b_base/convergence/` | Preserve evidence chain while removing it from primary navigation | Medium | Cross-linked docs; needs canonical-record index first |
| `docs/continuity/` | `history/projects/llama31_8b_base/continuity/` | Preserve handoff state as project history | Low | Mostly documentation references |
| `docs/history/` | `history/archive/deprecated_doctrine/` | Preserve governance evolution without primary-path clutter | Low | Low executable coupling |
| Bootstrap docs such as `docs/assistant_training_initial_ChatGPT_thread_summary.md`, `docs/repository_establishment_plan_v1.md`, `docs/evaluation_manifest_v1.md`, `docs/migration_checklist.md` | `history/archive/bootstrap/` | Useful for provenance, not active navigation | Low | Minimal code coupling |
| `docs/potential_skills/` | `history/archive/proposals/` or `docs/framework/proposals/` | Preserve reusable seeds without keeping them on the main path | Low | Low coupling |
| `evals/canonical_eval_manifest_v1.json` and `evals/data/canonical_v1/` | `regimen/contracts/` plus `fixtures/canonical_eval/` or remain in place with framework aliasing | Critical framework contract and pinned corpora | Medium | Scripts, docs, validators, and examples rely on current location |
| Core scripts: `train_lora_sft.py`, `preflight_lora_run.py`, `build_dataset_v1.py`, `eval_canonical_manifest.py` | `regimen/core/` and `regimen/eval/` | Core reusable executable value | High | Hard-coded paths, docs references, manifests, and test expectations |
| `scripts/stage_c1_evaluator_foundation.py` | `regimen/eval/foundations/` | Active evaluator dependency, framework-grade logic | High | Dynamically loaded by `eval_canonical_manifest.py` using sibling path |
| `scripts/stage_c2...stage_c8` integration scripts and direct tests | `regimen/eval/integration/` or `regimen/runtime_surfaces/` | Still active infrastructure and reusable reporting logic | High | Direct use of `reports/stage_c*` and fixture paths |
| Stage C blocker-branch package scripts and tests | `history/projects/llama31_8b_base/stage_c_blocker_branch/` | Preserve methodology execution history | Medium | Some are self-contained; some depend on shared artifacts |
| `manifests/environment/` | `regimen/contracts/environment/` or `history/reference/environment/` | Reproducibility and serious-run pinning | Low | Mostly referenced in docs and manifests |
| `manifests/reports/stage_b_wp8_validation/fixtures/` | `fixtures/wp8_validation/` | Framework fixture corpus; should become an explicit fixture surface | High | Directly referenced by scripts and tests using hard-coded absolute paths |
| `manifests/reports/stage_b_v1_threshold_profile.json` | `fixtures/threshold_profiles/stage_b_v1_threshold_profile.json` | Active threshold contract and fixture dependency | High | Referenced by tests, docs, and migration-preparation logic |
| Bulk `manifests/reports/` outside fixtures/profile | `history/reports/` | Preserve run evidence and gate bundles | Medium | Some scripts and docs reference specific report outputs |
| `reports/stage_c1-6/` | `fixtures/stage_c_samples/` and `history/reports/stage_c/` split | These are both sample fixtures and historical integration outputs | High | Direct script and test dependencies on current paths |
| `configs/lora/` | `history/projects/llama31_8b_base/configs/` plus `examples/reference/configs/` subset | Preserve historical configs and expose reusable examples separately | Medium | Docs and manifests refer to existing paths |
| `manifests/runs/` | `history/projects/llama31_8b_base/run_manifests/` plus `examples/reference/run_manifests/` subset | Preserve run intent and serious-run examples | Medium | Docs and workflow examples refer to them |
| `data/v1_0/` | `history/projects/llama31_8b_base/data/v1_0/` plus curated `examples/reference/data/` subset | Preserve dataset lineage while exposing only needed examples | Medium | Builder scripts and docs reference current paths |
| `data/tool_ft_allaliases_20260525_from_qual_reports*` | `history/projects/llama31_8b_base/data/intake/` | Preserve provenance of dataset intake | Low | Low executable coupling |
| `local_review_bundles/` | `history/archive/review_bundles/` or external archive | Preserve only if later judged necessary | Low | Ignored local-only surface |
| `artifacts/`, `evals/runs/`, caches, empty `staging/assistant-runtime/` | not migrated into tracked architecture | Low-value local-only residue | None | No future tracked architecture role |

## C. Dependency Impact Assessment

### Dependency Severity Legend

- `none`: no meaningful move blocker
- `low`: mostly documentation or pointer updates
- `medium`: multiple references, but no hard runtime coupling
- `high`: direct script/test path coupling, dynamic loading, fixture dependency, or current executable reliance

### 1. Scripts That Reference Candidate Migration Targets

| Script family | Candidate target referenced | Impact | Notes |
|---|---|---:|---|
| `scripts/eval_canonical_manifest.py` | `scripts/stage_c1_evaluator_foundation.py` | High | Uses dynamic sibling-path loading. Any move requires loader redesign or shim. |
| `scripts/stage_c1_evaluator_foundation.py` | `manifests/reports/stage_b_wp8_validation/fixtures/` | High | Uses current absolute path for fixture root. |
| `scripts/stage_c5_scoring_path_integration.py` | `scripts/stage_c4_real_output_ingestion.py`, `reports/stage_c5/input/`, `reports/stage_c5/contract_artifacts/` | High | Integration script depends on current report paths and sibling script location. |
| `scripts/stage_c6_scoring_report_integration.py` | `manifests/reports/stage_b_wp8_validation/fixtures/`, `reports/stage_c6/input/`, `reports/stage_c6/reporting_artifacts/` | High | Direct absolute path defaults make this a move blocker. |
| `scripts/stage_c8_non_authoritative_detector_projection_adapter.py` | `scripts/stage_c6_scoring_report_integration.py`, `reports/stage_c6/input/`, `reports/stage_c8/projection_artifacts/` | High | Direct dynamic load plus absolute report-path assumptions. |
| Stage B recovery builders and validators | `data/v1_0/`, `manifests/reports/`, `evals/canonical_eval_manifest_v1.json` | Medium | Heavy path coupling, but these are historical rather than core runtime dependencies. |
| `scripts/train_lora_sft.py`, `preflight_lora_run.py`, `build_dataset_v1.py` | configs, manifests, data, eval manifest | Medium | Core scripts can move, but only with coordinated path-resolution updates. |

### 2. Tests That Reference Candidate Migration Targets

| Test family | Candidate target referenced | Impact | Notes |
|---|---|---:|---|
| `tests/test_eval_canonical_manifest.py` | `scripts/eval_canonical_manifest.py`, `scripts/stage_c1_evaluator_foundation.py` | High | Protects core evaluator plus foundation linkage. |
| `tests/test_stage_c1_evaluator_foundation.py` | `scripts/stage_c1_evaluator_foundation.py` | High | Core path-coupled foundation test. |
| `tests/test_stage_c4_real_output_ingestion.py` | `manifests/reports/stage_b_wp8_validation/fixtures/` | High | Direct absolute fixture-root dependency. |
| `tests/test_stage_c6_scoring_report_integration.py` | `reports/stage_c5/input/stage_c5_sample_output_records.jsonl` | High | Depends on tracked reports as sample inputs. |
| `tests/test_stage_c8_non_authoritative_detector_projection_adapter.py` | WP8 fixtures, threshold profile, `reports/stage_c6/input/` | High | Multiple fixture and report path dependencies. |
| Stage C package tests | matching package scripts plus historical report bundles | Medium | Historical methodology tests; still coupled, but not part of the minimal reusable path. |
| `tests/test_dataset_contract.py`, `tests/test_masking_behavior.py` | data paths and core script signatures | Medium | Core contract tests; path abstraction must preserve them. |

### 3. Reports Used As Fixtures

| Report family | Current role | Impact | Notes |
|---|---|---:|---|
| `reports/stage_c1/stage_c1_fixture_harness_report.json` | baseline validation output | Medium | Historical plus potential reference fixture |
| `reports/stage_c2/stage_c2_foundation_report.json` | baseline validation output | Medium | Same pattern |
| `reports/stage_c3/baseline_contract_artifacts/*` | baseline artifact bundle | High | Downstream `stage_c4+` structure mirrors or reuses this bundle |
| `reports/stage_c4/input/stage_c4_sample_output_records.jsonl` | input fixture for ingestion | High | Executable dependency |
| `reports/stage_c5/input/stage_c5_sample_output_records.jsonl` | input fixture for reporting | High | Executable dependency |
| `reports/stage_c6/input/stage_c6_sample_output_records.jsonl` | input fixture for projection prep | High | Executable dependency |
| `reports/stage_c4-6/contract_artifacts` and `reporting_artifacts` | integration fixture bundles | High | Tests and scripts expect current paths and nested structure |

### 4. Path-Coupled Assets

| Asset family | Impact | Notes |
|---|---|---:|---|
| Absolute `/opt/ai-stack/assistant-training/...` defaults across scripts and tests | High | Main migration blocker for structural moves |
| Dynamic sibling-module loading in Stage C integration code | High | Prevents simple file relocation |
| WP8 fixture corpus inside `manifests/reports/` | High | Framework fixtures are stored in a historically named directory |
| Threshold profile inside `manifests/reports/` | High | Same issue as fixtures |
| `reports/stage_c*` used as sample fixtures | High | Historical report tree doubles as active input surface |
| Docs-only cross-links inside `docs/convergence/` | Medium | Many links, but mostly documentation-level remapping |
| Config and manifest references to data and report paths | Medium | Needs coordinated migration or compat layer |
| Ignored local-only surfaces | None | Not part of tracked migration design |

### 5. Migration Blockers

| Blocker | Impact | Why it blocks structural moves |
|---|---|---:|---|
| No shared path-resolution abstraction | High | Paths are embedded directly in scripts, tests, docs, configs, and reports |
| No canonical split between fixture assets and historical reports | High | `manifests/reports/` and `reports/stage_c*` mix framework and history |
| No canonical split between framework synthesis docs and historical convergence logs | Medium | `docs/convergence/` cannot be moved safely in bulk without a canonical-record map |
| Dynamic module loading tied to file adjacency | High | Prevents moving evaluator foundations independently |
| Current tests assert old locations | High | Structural moves would fail validation immediately |
| Dirty worktree with ongoing housekeeping edits | Low | Not a structural blocker, but implementation planning must avoid colliding with ongoing local documentation work |

## D. Housekeeping Execution Sequence

### 1. Prerequisite Work

These are required before any structural move phase begins:

1. Freeze the architecture blueprint and preservation map as accepted housekeeping authority.
2. Define canonical record sets:
   - selected synthesis records in `docs/convergence/`
   - fixture corpus roots
   - threshold profile
   - sample report fixtures
3. Introduce a path-resolution strategy for scripts and tests.
4. Define fixture extraction rules for `reports/stage_c*` and `manifests/reports/stage_b_wp8_validation/fixtures/`.
5. Define a documentation index for convergence history before splitting it.

### 2. Safe Early Moves

These should be done first during implementation planning because they are low-risk and preservation-safe:

- navigation-layer additions
  - add `docs/current/` style index and start-here materials
  - add framework-vs-history pointers
  - add canonical-record indexes
- documentation-only re-layering
  - create pointers to future doctrine/framework/history areas without moving underlying files yet
- archive-intent tagging
  - mark which families are planned for history or archive without physically relocating them

These are safe because they change navigation before changing structure.

### 3. Medium-Risk Structural Moves

These should follow after path-decoupling and canonical indexing:

- bootstrap and historical docs
- continuity docs
- deprecated doctrine versions
- dormant proposal docs
- bulk convergence history after synthesis docs are isolated
- bulk `manifests/reports/` history after fixture/profile exceptions are separated

Validation checkpoint after this phase:

- verify all canonical-record links resolve
- verify doctrine links remain stable
- verify no core script or test path breaks

### 4. High-Risk Structural Moves

These should occur only after dependency remediation:

- core scripts into `regimen/`
- stage_c1 foundation extraction
- stage_c2-c8 integration extraction
- fixture corpus move out of `manifests/reports/`
- threshold profile move
- `reports/stage_c1-6/` split into fixture and history roles
- configs, run manifests, and dataset lineage split into history plus examples

Validation checkpoint after each high-risk move:

- core contract tests
- evaluator tests
- fixture-dependent tests
- path-audit grep for old locations
- equivalence check for moved fixture contents

### 5. Archival Moves

These should happen only after primary navigation and structural moves are stable:

- local review bundle decisions
- companion acceptance and implementation summaries
- dormant stage package scripts and tests
- bootstrap archives

Validation checkpoint:

- provenance index still resolves every preserved record
- no H-01 critical or high-priority surface is lost

### 6. Future Pruning Candidates

Pruning is explicitly not part of H-02.

Future pruning should be deferred until:

1. framework/history separation is complete
2. dependency-coupled fixtures have canonical replacements
3. provenance indexes are in place
4. a narrower redundancy audit has been completed

Likely future pruning candidates after that point:

- ignored local-only heavy outputs
- duplicate operational review bundles
- duplicated historical sample reports after canonical fixture extraction
- superseded bootstrap docs with confirmed archival coverage

### 7. Execution Phases By Change Type

Explicit distinction for later implementation planning:

- navigation-layer changes
  - indexes
  - start-here docs
  - framework/history pointers
  - canonical-record maps
- structural moves
  - doctrine relocation
  - framework extraction
  - history relocation
  - fixture relocation
- archival moves
  - companion docs
  - dormant proposals
  - review packets
  - deprecated history
- future pruning candidates
  - only after structural stabilization and a separate redundancy review

## E. Preservation Compliance Assessment

### Compliance With H-01

This architecture remains compliant with H-01 because it preserves:

- doctrine as a protected top-level authority class
- framework assets as primary navigation material
- reusable methodology as an explicit framework surface
- active infrastructure as preserved until deliberate extraction or refactor
- historical evidence as retained history rather than discarded clutter
- project history as preserved archival material
- cleanup candidates as local-only and outside the tracked primary architecture

### H-01 Families Preserved Without Downgrade

- doctrine surfaces remain primary and never-removable
- WP8 fixtures and threshold profile remain critical framework fixtures
- core evaluator and training scripts remain critical reusable infrastructure
- `docs/lineages/` remains primary methodology
- selected synthesis convergence docs remain primary methodology/current-state records
- `reports/stage_c1-6/` are preserved until replacement fixture paths exist

### Areas Where H-01 Could Need Later Amendment

No H-01 amendment is required to proceed to structural implementation planning.

Potential future amendment points only after implementation evidence exists:

- if `reports/stage_c1-6/` are successfully split into canonical fixtures plus historical copies, H-01 may later downgrade some duplicated report surfaces from `Reference` to `Archive`
- if stage_c2-c8 integration code is fully absorbed into a stable `regimen/` package, H-01 may later reclassify some current script paths from `Reference` to `Historical`
- if a new doctrine packaging layout is accepted, H-01 may later update doctrine path names while preserving doctrine priority and never-remove status

These are path-level refinements, not classification reversals.

## F. Structural Housekeeping Readiness Determination

### Determination

After H-02, the repository is ready for structural housekeeping implementation planning.

### Scope Of Readiness

Ready:

- navigation-layer implementation planning
- path-decoupling implementation planning
- fixture extraction planning
- doctrine/framework/history split planning
- staged structural move planning

Not yet ready:

- bulk moves without dependency remediation
- archive execution without canonical-record indexes
- pruning or deletion work

### Readiness Conditions

Implementation planning may proceed if it treats the following as mandatory first-order work:

1. path abstraction and compatibility strategy
2. fixture-surface extraction design
3. convergence canonical-record mapping
4. validation checkpoints for every structural phase

### Final Readiness Answer

Yes: H-02 provides sufficient architecture and migration clarity for structural housekeeping implementation planning.

The next phase should be an implementation-planning package, not direct bulk migration execution.
