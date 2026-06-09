# Repository Path Decoupling and Compatibility Strategy

## Work Package

- ID: `H-03`
- Title: `Path Decoupling and Compatibility Strategy`
- Repository: `/opt/ai-stack/assistant-training`
- Scope: compatibility design and migration-safety planning only
- Governing authority:
  - `docs/housekeeping/HOUSEKEEPING_PRESERVATION_INDEX.md`
  - `docs/housekeeping/HOUSEKEEPING_ARCHITECTURE_AND_MIGRATION_PLAN.md`
- Out of scope:
  - file movement
  - directory creation
  - code modification
  - doctrine modification
  - migration implementation
  - archival actions

## Current State Basis

- Stage B complete.
- Stage C blocker-oriented branch complete.
- Runtime-output / corpus-behavior investigation family defined and parked.
- Housekeeping phase active.
- H-01 governs classification and preservation.
- H-02 governs target architecture and migration-family planning.

## Inspection Basis

Direct inspection for H-03 covered:

- governing H-01 and H-02 housekeeping artifacts
- `AGENTS.md`
- core scripts and Stage C integration scripts
- core tests and migration-coupled Stage C tests
- canonical eval manifest
- selected docs with path-coupled links
- data intake docs
- representative historical and fixture-bearing report surfaces

Observed repository facts relevant to path decoupling:

- `32` script files contain absolute `/opt/ai-stack/assistant-training/...` path references.
- `18` test files contain absolute `/opt/ai-stack/assistant-training/...` path references.
- `21` docs contain absolute `/opt/ai-stack/assistant-training/...` path references.
- `9` script files use `importlib.util.spec_from_file_location(...)`.
- `18` test files use `importlib.util.spec_from_file_location(...)`.
- `8` script files and `7` test files directly reference the WP8 fixture corpus or threshold profile.
- `5` script files and `2` test files directly reference tracked `reports/stage_c*` sample paths.
- `train_lora_sft.py` already contains one repo-root discovery pattern based on `Path(__file__).resolve().parents[1]`, which is the strongest current precedent for future decoupling.

## Planning Principles

1. Decoupling must separate executable dependencies from provenance records.
2. No compatibility design is acceptable if it rewrites or weakens pinned historical evidence.
3. Future moves must preserve both runnable surfaces and historical citation surfaces.
4. Paths should become late-bound through stable roles or identifiers, not early-bound through absolute literals.
5. Historical records may retain original paths as provenance even after active infrastructure moves.

## A. Path Dependency Inventory

## Dependency Legend

- `High`: move blocker for future structural housekeeping
- `Medium`: coordinated updates required, but not an immediate move blocker
- `Low`: mostly navigation or pointer maintenance
- `None`: not a real migration dependency

## 1. Hard-Coded Path Assumptions

| Dependency class | Representative locations | Current behavior | Migration risk |
|---|---|---|---:|
| Absolute repo-root defaults in active integration scripts | `scripts/stage_c3_evaluator_runtime_integration.py`, `stage_c4_real_output_ingestion.py`, `stage_c5_scoring_path_integration.py`, `stage_c6_scoring_report_integration.py`, `stage_c8_non_authoritative_detector_projection_adapter.py` | Scripts assume fixed locations for fixtures, sample output records, and output artifact directories under `/opt/ai-stack/assistant-training/...` | High |
| Absolute repo-root defaults in historical builders and validators | `scripts/build_stage_b_recovery_*.py`, `validate_stage_b_recovery_*.py`, `build_stage_b_v1_*_family_concentration_review.py` | Scripts hard-code `data/v1_0/`, `evals/data/canonical_v1/`, `configs/lora/`, `manifests/runs/`, and `manifests/reports/` | High |
| Absolute repo-root defaults in tests | `tests/test_eval_canonical_manifest.py`, `test_stage_c1_evaluator_foundation.py`, `test_stage_c3_evaluator_runtime_integration.py`, `test_stage_c6_scoring_report_integration.py`, `test_stage_c8_non_authoritative_detector_projection_adapter.py` | Tests target exact current script and fixture paths rather than path roles | High |
| Absolute repo-root references in documents | `AGENTS.md`, `docs/assistant_training_goal_documents_and_artifacts_index.md`, multiple `docs/convergence/*.md`, doctrine and deprecated doctrine docs | Documents encode current directory layout directly into links and references | Medium |
| External runtime-repo paths in active tests and intake docs | `tests/test_dataset_contract.py`, `data/README.md`, `data/README (data-intake).md`, `evals/canonical_eval_manifest_v1.json` | Some surfaces depend on `/opt/ai-stack/runtimes/assistant-runtime/...` or record it as canonical provenance | Medium |

## 2. Dynamic Module-Loading Assumptions

| Dependency class | Representative locations | Current behavior | Migration risk |
|---|---|---|---:|
| Sibling-script dynamic loading in evaluator chain | `scripts/eval_canonical_manifest.py` -> `stage_c1_evaluator_foundation.py` | Evaluator loads foundation by current sibling path | High |
| Sibling-script dynamic loading in Stage C integration chain | `scripts/stage_c3_evaluator_runtime_integration.py`, `stage_c4_real_output_ingestion.py`, `stage_c5_scoring_path_integration.py`, `stage_c6_scoring_report_integration.py`, `stage_c8_non_authoritative_detector_projection_adapter.py` | Each script loads prior-stage module from the same directory using `spec_from_file_location` | High |
| Dynamic loading of evaluator from historical methodology scripts | `scripts/stage_c_runtime_output_forensics_direct_answer_missing_evidence.py`, `stage_c_legacy_surface_validity_direct_answer_assessment.py`, `stage_c_technical_spike_direct_answer_probe.py` | Historical investigation scripts depend on current `eval_canonical_manifest.py` path | High |
| Test-side dynamic loading of current script files | `18` test files under `tests/` | Tests import scripts by exact on-disk file path rather than package import or resolved role | High |

## 3. Fixture-Location Assumptions

| Dependency class | Representative locations | Current behavior | Migration risk |
|---|---|---|---:|
| WP8 fixture corpus path | `scripts/stage_c1_evaluator_foundation.py`, `stage_c3...stage_c8`, `tests/test_stage_c1_evaluator_foundation.py`, `test_stage_c4_real_output_ingestion.py`, `test_stage_c8_non_authoritative_detector_projection_adapter.py` | Assumes canonical fixture root is `manifests/reports/stage_b_wp8_validation/fixtures/` | High |
| Threshold profile path | `scripts/stage_c8_non_authoritative_detector_projection_adapter.py`, `scripts/stage_c_package2a_gate_evidence_bundle.py`, `scripts/stage_c_package5b_direct_answer_blocker_persistence.py`, `tests/test_eval_canonical_manifest.py`, `tests/test_stage_c8_non_authoritative_detector_projection_adapter.py` | Assumes threshold profile remains at `manifests/reports/stage_b_v1_threshold_profile.json` | High |
| Eval dataset paths | `build_dataset_v1.py`, multiple Stage B recovery builders and validators, `evals/canonical_eval_manifest_v1.json` | Assumes canonical eval datasets remain in `evals/data/canonical_v1/` | Medium |

## 4. Report-Location Assumptions

| Dependency class | Representative locations | Current behavior | Migration risk |
|---|---|---|---:|
| `reports/stage_c4/input/` sample JSONL | `scripts/stage_c4_real_output_ingestion.py` | Uses tracked report input as the default sample output source | High |
| `reports/stage_c5/input/` sample JSONL | `scripts/stage_c5_scoring_path_integration.py`, `tests/test_stage_c6_scoring_report_integration.py` | Report tree doubles as active sample input location | High |
| `reports/stage_c6/input/` sample JSONL | `scripts/stage_c6_scoring_report_integration.py`, `scripts/stage_c8_non_authoritative_detector_projection_adapter.py`, `tests/test_stage_c8_non_authoritative_detector_projection_adapter.py` | Same mixed fixture/history role | High |
| `reports/stage_c3-6/contract_artifacts` and `reporting_artifacts` | Stage C integration scripts and downstream tests | Tracked report bundles act as reusable baseline artifacts | High |
| Historical report outputs referenced from docs | multiple `docs/convergence/*.md` | Documentation expects report artifacts at current `manifests/reports/` locations | Medium |

## 5. Test-Location Assumptions

| Dependency class | Representative locations | Current behavior | Migration risk |
|---|---|---|---:|
| Tests target current script file paths directly | `tests/test_masking_behavior.py`, `test_eval_adapter_toolcalls.py`, `test_eval_canonical_manifest.py`, Stage C tests | Test imports break immediately if scripts move without shims | High |
| Tests assume current fixture/report paths | `tests/test_stage_c3_evaluator_runtime_integration.py`, `test_stage_c4_real_output_ingestion.py`, `test_stage_c6_scoring_report_integration.py`, `test_stage_c8_non_authoritative_detector_projection_adapter.py` | Tests are tied to present report and fixture layout | High |
| Tests assume external dataset location | `tests/test_dataset_contract.py` | Depends on sibling runtime repo outputs, not this repo | Medium |

## 6. Documentation-Location Assumptions

| Dependency class | Representative locations | Current behavior | Migration risk |
|---|---|---|---:|
| Dispatcher references to process assets | `AGENTS.md` | References `docs/process_infrastructure/...` directly | Medium |
| Convergence cross-link density | `docs/convergence/*.md` | Documents heavily cite one another at current paths; `rg` found about `860` `docs/convergence/` references in docs and `AGENTS.md` | Medium |
| Absolute clickable repository links | `docs/assistant_training_goal_documents_and_artifacts_index.md`, implementation summaries, legacy transition docs | Documents will lose navigability if targets move without redirects or link rewrites | Medium |
| Current-path references in doctrine or historical doctrine | `docs/appendix_a_operational_execution_contract_v3a.md`, `docs/history/*.md`, `docs/evaluation_manifest_v1.md` | Some references are active guidance, others are frozen provenance | Medium |

## 7. Important Non-Dependencies That Must Not Be Mistaken For Location Coupling

| Surface | Why it contains paths | Migration risk | Handling rule |
|---|---|---:|---|
| `data/tool_ft_allaliases_20260525_from_qual_reports.jsonl` | Runtime file paths are part of training examples and prompt content | None | Preserve as data content; do not rewrite during housekeeping |
| `data/tool_ft_allaliases_20260525_from_qual_reports.summary.json` | Runtime report paths are provenance inputs | Low | Preserve as provenance record |
| `manifests/reports/*.json*` historical outputs | Paths appear inside recorded evidence | Low | Preserve original values; add relocation metadata separately if needed |
| `evals/canonical_eval_manifest_v1.json` absolute paths | Some fields are active executable references; some are pinned provenance | Medium | Split future runtime resolution from frozen provenance rather than rewriting blindly |

## Inventory Summary

The repository has three distinct path problems, not one:

1. executable location coupling
2. documentation and citation coupling
3. provenance records that contain path strings but should remain historically intact

Future migration work must treat those classes differently.

## B. Compatibility Strategy

## 1. Required Compatibility Model

Future structural moves should use a four-layer model:

1. `stable role`
   - examples: `core_evaluator`, `wp8_fixture_root`, `threshold_profile`, `canonical_eval_manifest`, `stage_c6_sample_outputs`
2. `resolver`
   - a single authoritative mechanism that maps a stable role to the current concrete path
3. `compatibility shim`
   - temporary wrapper or alias that preserves legacy callers while new locations are adopted
4. `provenance record`
   - historical artifacts retain their original path strings and are not rewritten merely to match the new layout

This model avoids the current failure mode where the concrete path is also the identity.

## 2. Script Compatibility Strategy

Future moves should preserve scripts by applying these rules:

- CLI arguments remain highest-precedence inputs.
- Default paths should be resolved through a shared repository resolver, not embedded as `/opt/ai-stack/assistant-training/...`.
- Dynamic `spec_from_file_location` chains should be replaced by stable module entrypoints or centralized loader helpers.
- When scripts move, legacy script paths should remain as thin compatibility wrappers until all tests, docs, and manifests are updated.
- Wrapper removal should be deferred until path-audit checks show no remaining live dependency on legacy script locations.

Recommended compatibility mechanisms:

- shared repo-root resolver
- named artifact resolver
- legacy script wrappers at original paths during transition
- explicit deprecation window for wrapper removal

## 3. Test Compatibility Strategy

Future moves should preserve tests by applying these rules:

- Tests should load executable surfaces through stable helpers, not absolute script paths.
- Path-coupled tests should be split into:
  - contract tests for behavior
  - compatibility tests for legacy entrypoints
- Tests that intentionally verify old-path compatibility should remain explicit and temporary.
- Tests that rely on report-tree sample inputs should switch to canonical fixture IDs once fixture extraction is complete.

Recommended compatibility mechanisms:

- single test helper for repository-root and artifact resolution
- transitional compatibility tests for wrapper entrypoints
- fixture registry lookups instead of direct `reports/stage_c*` paths

## 4. Fixture Compatibility Strategy

Future moves should preserve fixtures by applying these rules:

- Reusable fixtures receive stable fixture IDs.
- Fixture identity is defined by content hash plus fixture ID, not by current storage directory.
- Active scripts and tests resolve fixtures by ID through a canonical fixture registry.
- Original fixture-bearing historical paths remain preserved until the extracted fixture surfaces are validated.

Recommended compatibility mechanisms:

- fixture registry
- checksum manifest
- provenance manifest linking extracted fixture to original source path
- temporary dual-path support during transition

## 5. Report Compatibility Strategy

Future moves should preserve report consumers by applying these rules:

- Historical reports should stop acting as the default source of active sample inputs.
- Any report-derived sample that remains active should be promoted into a canonical sample-artifact surface.
- Historical report bundles should retain original structure for provenance.
- Code should consume active samples through fixture or artifact IDs, not `reports/stage_c*` paths.

Recommended compatibility mechanisms:

- canonical sample-artifact registry
- provenance manifest from sample artifact to source report
- historical copy retained until report-to-fixture migration validates cleanly

## 6. Manifest Compatibility Strategy

Future moves should preserve manifests by applying these rules:

- Pinned historical manifests should not be mass-rewritten to new paths because they serve provenance and comparability.
- Future runtime execution can use companion resolution metadata rather than editing frozen manifest records in place.
- Active manifests may need two path concepts:
  - recorded provenance path
  - current resolved path

Recommended compatibility mechanisms:

- companion relocation map for pinned manifests
- stable artifact IDs referenced by runtime tooling
- explicit distinction between `recorded_source_path` and `resolved_runtime_path`

## 7. Documentation Compatibility Strategy

Future moves should preserve navigation and citation by applying these rules:

- High-citation docs need redirect or alias treatment during transition.
- Bulk path rewrites should not happen without a canonical record index.
- Primary navigation docs should point to new framework/history surfaces first.
- Historical docs may retain old path mentions when those mentions are part of provenance or quoted record state.

Recommended compatibility mechanisms:

- current-to-future path map
- high-citation redirect stubs for moved documents
- `INDEX.md` or summary pages at family boundaries
- documentation link audit before legacy path removal

## 8. External Runtime Dependency Strategy

The sibling runtime repo dependency should be handled separately from internal restructuring:

- Internal repository migration should not silently rewrite runtime-file paths embedded in datasets, manifests, or evidence.
- Active tests or docs that require the runtime repo should declare that dependency explicitly.
- Reuse-oriented surfaces should prefer fixtureized local examples when possible, but provenance surfaces should continue recording the original runtime paths.

This is a portability issue and a compatibility issue, but it is not solved by repository moves alone.

## C. Fixture Extraction Strategy

## 1. Fixture Separation Model

Future fixture extraction should separate four artifact roles:

1. reusable fixtures
2. historical reports
3. sample artifacts
4. provenance records

Definitions:

- `reusable fixtures`: stable inputs required by active scripts or tests
- `historical reports`: execution outputs preserved as evidence
- `sample artifacts`: representative bundles promoted from history because they are needed for active integration coverage
- `provenance records`: metadata tying extracted fixtures or samples back to their original source artifacts

## 2. Promotion Rules

An artifact should be promoted from history into a reusable fixture surface only if at least one of the following is true:

- an active script depends on it
- an active test depends on it
- it is the canonical baseline needed to reproduce a current methodology claim
- it is the smallest stable sample that preserves the required behavior surface

Artifacts that are merely illustrative but not active should remain historical/reference material.

## 3. Recommended Future Fixture Split

| Current surface | Future role | Notes |
|---|---|---|
| `manifests/reports/stage_b_wp8_validation/fixtures/` | reusable fixtures | Promote as canonical fixture root with stable IDs |
| `manifests/reports/stage_b_v1_threshold_profile.json` | reusable fixture contract | Treat as threshold fixture, not as historical report clutter |
| `reports/stage_c4/input/stage_c4_sample_output_records.jsonl` | sample artifact | Active sample input currently living in report tree |
| `reports/stage_c5/input/stage_c5_sample_output_records.jsonl` | sample artifact | Same |
| `reports/stage_c6/input/stage_c6_sample_output_records.jsonl` | sample artifact | Same |
| `reports/stage_c3-6/contract_artifacts` and `reporting_artifacts` | mixed: sample artifact subset plus historical report | Split only the minimal reusable bundle; preserve full originals as history |
| bulk `manifests/reports/` | historical reports | Preserve as evidence unless an active dependency justifies promotion |

## 4. Extraction Method

The future extraction sequence should follow `copy -> hash -> register -> validate -> preserve original`.

Required outputs for each promoted fixture family:

- canonical fixture copy
- checksum record
- source-to-canonical provenance manifest
- validation note listing active consumers

This is intentionally preservation-first:

- original historical artifact remains intact
- extracted fixture becomes the new active dependency surface
- only later can duplication be reviewed

## 5. Reproducibility Rules

Future fixture extraction must not reduce reproducibility. That requires:

- content-hash equality between extracted fixture and source artifact where exact copying is intended
- explicit provenance mapping when a reduced sample is extracted from a larger report bundle
- retained historical originals for any promoted sample
- stable fixture IDs that remain valid across directory moves

## 6. Important Boundary

Do not rewrite scenario-content paths inside datasets merely because those strings look like filesystem references.

For example:

- runtime file paths inside training prompts
- runtime repo paths inside qualitative source summaries
- recorded artifact paths inside historical evaluation outputs

Those are part of the preserved record, not migration targets.

## D. Historical Reference Preservation Strategy

## 1. Convergence History

Future migration should preserve convergence history through a two-surface model:

- `framework-selected synthesis`
- `historical convergence archive`

Required preservation mechanisms:

- canonical convergence index
- old-path to new-path reference map
- primary/supporting/informational labels for key records
- redirect treatment for high-citation convergence records when moved

This is necessary because docs contain roughly `860` references to `docs/convergence/`.

## 2. Run History

Future migration should preserve run history through:

- stable run IDs
- run-manifest index
- report-bundle index
- config-to-run crosswalk
- provenance map for historical report locations

Run history remains discoverable if users can answer:

- what run existed
- what config and manifest governed it
- what reports belong to it
- where its preserved history now lives

## 3. Continuity History

Future migration should preserve continuity history through:

- a continuity landing index
- preserved snapshot ordering
- explicit link from current-state docs back to continuity snapshots

Continuity should move off the primary path without becoming invisible.

## 4. Archived Materials

Future archive surfaces should remain discoverable through:

- archive index
- reason-for-archive note
- original path record
- related active or canonical replacement record

Archive discoverability matters because many companion assessments look redundant but still explain the evidence chain around a primary record.

## 5. Recommended Historical Reference Artifacts

Future structural housekeeping should create, at minimum:

- migration path map
- convergence canonical record index
- run-history index
- continuity index
- archive index

These are not optional if large historical families move.

## E. Validation Strategy

The validation plan below groups the H-02 migration map into major migration families.

| Migration family | Required validation checks | Rollback criteria | Migration success criteria |
|---|---|---|---|
| `README.md` and `AGENTS.md` | README navigation check; `AGENTS.md` route-asset links resolve; no broken primary entry links | any broken entry path or route-asset reference | front-door navigation resolves cleanly and authority surfaces remain reachable |
| Doctrine docs | doctrine link audit; manifest references reviewed; no authority ambiguity introduced | any missing doctrine path, any broken reference from primary navigation, any doctrine/provenance confusion | doctrine reachable from new location and any required old-path compatibility still resolves |
| `docs/process_infrastructure/`, `docs/lineages/`, selected synthesis docs | link audit; high-citation doc checks; primary-path navigation check | any broken path from `AGENTS.md`, any missing selected synthesis record | reusable methodology and process assets remain primary and discoverable |
| Bulk `docs/convergence/` history | canonical record index complete; sampled historical doc links resolve; old-to-new map complete | missing canonical record, broken high-citation links, missing historical package family | convergence history discoverable by package and by canonical record |
| `docs/continuity/`, `docs/history/`, bootstrap docs, dormant proposals | index coverage check; random-sample link check | missing index coverage or ambiguous archive placement | history remains discoverable without staying on primary path |
| Canonical eval manifest and eval corpora | manifest integrity check; dataset hash verification; evaluator smoke test against resolved paths | manifest no longer points to resolvable runtime paths, hash mismatch, evaluator failure | active evaluation still runs and pinned corpora/provenance remain intact |
| Core scripts and core tests | targeted `pytest` for `test_masking_behavior.py`, `test_eval_canonical_manifest.py`, `test_stage_c1_evaluator_foundation.py`; CLI smoke for core scripts; path-audit grep | any import failure, any core contract regression, any unresolved old-path dependency without shim | core tooling works from new structure and legacy callers remain supported if planned |
| Stage C integration scripts and direct tests | targeted `pytest` for Stage C integration tests; sample-artifact resolution checks; dynamic-loader checks | any failure in `stage_c3` through `stage_c8` chain, missing sample artifact, broken loader resolution | integration chain runs through canonical fixture/sample surfaces |
| WP8 fixtures and threshold profile | checksum verification; fixture inventory check; fixture-dependent tests; registry resolution check | any hash mismatch, missing fixture ID, any dependent test failure | fixtures resolve through canonical fixture surface with originals still preserved |
| `reports/stage_c1-6/` sample/report split | sample-artifact hash or content-equivalence check; downstream test pass; provenance manifest completeness | any active consumer still depends on historical path only, any missing provenance link | active samples use new fixture surface and full historical reports remain preserved |
| `manifests/environment/` | environment snapshot readability check; manifest references resolve | broken manifest path or unreadable snapshot | reproducibility snapshots remain accessible and cited correctly |
| Bulk `manifests/reports/` history | report index completeness; sampled historical links resolve; no active script still points at archived-only location | active dependency on moved historical-only path, missing bundle coverage, broken provenance references | history reports move off the primary path without losing evidence discoverability |
| `configs/lora/`, `manifests/runs/`, `data/v1_0/` | example subset identification; hash checks for preserved originals; docs/example link audit | any active script unexpectedly depends on moved historical location, any broken run-history reference | historical lineage preserved and example surfaces are explicit |
| Local-only cleanup candidates | ignore rules still valid; no tracked dependency | any tracked surface unexpectedly depended on local-only residue | local-only surfaces remain outside primary tracked architecture |

## Common Validation Gates

Regardless of migration family, every structural phase should also run:

1. path-audit grep for unresolved legacy assumptions
2. targeted test suite for the touched family
3. documentation link audit for the touched family
4. provenance completeness check
5. checksum or equivalence check where content was copied or promoted

## Common Rollback Rule

Rollback is required if any of the following occurs:

- a primary script or test stops resolving
- a canonical fixture or manifest can no longer be located
- a preserved historical record becomes undiscoverable
- a path-looking string that is actually preserved evidence is accidentally normalized or rewritten
- old-path compatibility was declared for the phase but does not hold

## F. Implementation Readiness Determination

## Determination

After H-03, the repository is ready for structural implementation of the compatibility layer and prerequisite migration scaffolding.

It is not yet ready for unrestricted bulk file movement.

## What H-03 Makes Ready

Ready after acceptance of H-03:

- implementation of a shared path-resolution mechanism
- implementation of fixture and sample-artifact registries
- implementation of compatibility wrappers or redirect shims
- implementation of convergence and history reference indexes
- staged migration execution planning tied to validation checkpoints

## What Remains Gated

Still gated after H-03:

- bulk moves of active scripts
- bulk moves of fixture-bearing surfaces
- bulk moves of `docs/convergence/`
- pruning or deletion
- any change that rewrites frozen provenance records without a preservation rationale

## Final Readiness Answer

Yes, conditionally.

H-03 provides sufficient compatibility design to begin structural implementation work, but that work must start with:

1. path resolver implementation
2. fixture/sample registry implementation
3. compatibility shim implementation
4. historical reference index implementation

Only after those prerequisites validate cleanly should physical structural migration begin.
