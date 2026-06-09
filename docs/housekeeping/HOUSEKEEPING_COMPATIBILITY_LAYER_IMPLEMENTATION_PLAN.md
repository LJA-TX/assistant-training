# Repository Compatibility Layer Implementation Plan

## Work Package

- ID: `H-05`
- Title: `Compatibility Layer Implementation Plan`
- Repository: `/opt/ai-stack/assistant-training`
- Scope: compatibility-layer implementation planning only
- Governing authority:
  - `docs/housekeeping/HOUSEKEEPING_PRESERVATION_INDEX.md`
  - `docs/housekeeping/HOUSEKEEPING_ARCHITECTURE_AND_MIGRATION_PLAN.md`
  - `docs/housekeeping/HOUSEKEEPING_PATH_DECOUPLING_AND_COMPATIBILITY_STRATEGY.md`
  - `docs/current/housekeeping_status.md`
- Out of scope:
  - code changes
  - test changes
  - file moves
  - directory restructuring
  - fixture extraction
  - compatibility implementation
  - archival actions

## Current State Basis

- Stage B complete.
- Stage C blocker-oriented branch complete.
- Runtime-output / corpus-behavior investigation family defined and parked.
- Housekeeping phase active.
- H-04 established the navigation layer and confirmed that structural migration remains gated.

## Planning Principles

1. The first compatibility implementation must be smaller than the eventual migration.
2. The first slice should target the highest-value active couplings, not the whole repository.
3. In-place resolution is preferable to early file movement.
4. Historical provenance records must remain intact even when active call sites stop depending on old paths.
5. The compatibility layer should live inside the current layout, not presuppose the future `regimen/` layout.

## A. Resolver Architecture

## 1. Resolver Scope

The minimum viable resolver should cover four classes of active dependency:

- repository root resolution
- artifact resolution
- fixture resolution
- sample-artifact resolution

It should not try to solve all historical or external-runtime references in the first slice.

## 2. Repository Root Resolution

Minimum viable design:

- a single helper module in the existing `scripts/` surface
- proposed file name: `scripts/repo_paths.py`

Repository root resolution should use this precedence:

1. explicit environment override for the repository root
2. deterministic sentinel-based parent walk from the helper module or caller path
3. hard failure with a clear error if no repository root can be proven

Recommended sentinel set:

- `AGENTS.md`
- `docs/goal_charter_v5a.md`
- `scripts/`
- `evals/`

Design requirements:

- must not depend on the current working directory
- must return a canonical `Path`
- should cache the resolved root after first success

## 3. Artifact Resolution

Artifact resolution should use stable role names rather than concrete absolute paths.

Minimum role categories:

- `script`
- `artifact`
- `fixture_root`
- `sample_artifact`
- `output_artifact_dir`

Minimum artifact roles for the first implementation slice:

- `canonical_eval_manifest`
- `stage_c1_foundation_script`
- `stage_c2_foundation_script`
- `stage_c3_runtime_integration_script`
- `stage_c4_output_ingestion_script`
- `stage_c5_scoring_path_script`
- `stage_c6_scoring_report_script`
- `stage_c8_projection_adapter_script`
- `wp8_fixture_root`
- `stage_b_v1_threshold_profile`
- `stage_c4_sample_output_records`
- `stage_c5_sample_output_records`
- `stage_c6_sample_output_records`
- `stage_c3_baseline_artifacts_dir`
- `stage_c4_contract_artifacts_dir`
- `stage_c5_contract_artifacts_dir`
- `stage_c6_reporting_artifacts_dir`
- `stage_c8_projection_artifacts_dir`

The role map should stay code-local in the first slice.

Reason:

- this is smaller and less fragile than introducing a new configuration file format before the path model has stabilized
- it avoids coupling live resolution to frozen provenance manifests

## 4. Fixture Resolution

Fixture resolution should be layered on top of artifact resolution.

Minimum interface:

- resolve fixture family root by stable role
- optionally look up individual fixture documents by existing `fixture_id`

The first slice should preserve the current Stage C1 loading model:

- scan the current WP8 fixture root
- continue using the existing `fixture_id` values inside fixture payloads

This avoids a full fixture extraction or fixture-item rekeying phase.

## 5. Sample-Artifact Resolution

Sample-artifact resolution is required because tracked `reports/stage_c*` currently serve as active inputs.

Minimum sample roles:

- `stage_c4_sample_output_records`
- `stage_c5_sample_output_records`
- `stage_c6_sample_output_records`

These should resolve to the current in-place files during the first implementation slice.

That is enough to decouple call sites without moving the sample files yet.

## 6. Module Loading Support

The resolver should provide one additional helper for dynamic script loading.

Minimum viable loader support:

- resolve script by stable role
- load module from that resolved path

Reason:

- the active Stage C chain currently depends on sibling-path `spec_from_file_location(...)`
- future script moves are blocked until those loads stop assuming file adjacency

## 7. Minimum Viable Resolver Design

The smallest practical design is:

1. one helper module under `scripts/`
2. one static role map in that helper
3. one loader helper for script roles
4. no external config file
5. no attempt to solve historical provenance rewriting

This is sufficient to materially reduce the highest-risk active path coupling without creating a new packaging system first.

## B. Fixture Registry Architecture

## 1. Registry Scope

The first fixture registry should cover only active fixtures and active sample artifacts that are still used by scripts or tests.

In scope for the first registry:

- WP8 fixture family root
- Stage B v1 threshold profile
- Stage C4 sample output records
- Stage C5 sample output records
- Stage C6 sample output records

Out of scope for the first registry:

- bulk historical `manifests/reports/`
- bulk historical `reports/stage_c*`
- project-wide lineage datasets
- bootstrap and continuity materials

## 2. Fixture Identity Model

Use a two-level identity model.

Family-level identity:

- stable registry key for a fixture family or sample artifact

Item-level identity:

- existing `fixture_id` inside WP8 fixture payloads
- file identity for singular artifacts such as threshold profiles or sample JSONL files

Recommended family-level keys:

- `fixture_family/wp8_validation`
- `threshold_profile/stage_b_v1`
- `sample_output/stage_c4_v1`
- `sample_output/stage_c5_v1`
- `sample_output/stage_c6_v1`

This is smaller than trying to register every single WP8 JSON fixture as an independent first-slice registry row.

## 3. Fixture Metadata Model

Minimum registry fields:

- `artifact_id`
- `kind`
- `active_surface`
- `current_path`
- `sha256_mode`
- `source_origin_path`
- `historical_source_kind`
- `consumer_scripts`
- `consumer_tests`
- `notes`

Field intent:

- `kind`: `fixture_family`, `threshold_profile`, or `sample_artifact`
- `active_surface`: distinguishes active dependencies from preserved history
- `sha256_mode`: `tree` for fixture families, `file` for singular artifacts
- `source_origin_path`: current provenance anchor
- `historical_source_kind`: identifies whether the item currently lives in a report path, fixture path, or mixed path

## 4. Provenance Linkage Model

The first registry must preserve provenance without moving anything.

Minimum provenance linkage fields:

- `current_path`
- `recorded_source_path`
- `recorded_source_kind`
- `preservation_reason`

For the first slice, `current_path` and `recorded_source_path` will usually be the same.

That is acceptable because the registry is being introduced before physical migration.

## 5. Threshold-Profile Handling

The threshold profile should not be treated as an ordinary historical report.

It should be registered as:

- its own first-class `threshold_profile` artifact kind
- active infrastructure
- provenance-preserved

This matters because the threshold profile is both:

- a current active dependency
- a future migration target out of `manifests/reports/`

## 6. Active Fixtures Versus Historical Reports

Distinguish them explicitly:

- `active fixtures`
  - currently consumed by scripts or tests
  - registered by stable role
  - migration-relevant
- `historical reports`
  - preserved for provenance
  - not consumed by active code paths
  - not part of the first registry unless promoted into a sample-artifact role

This distinction is the core boundary that lets future housekeeping move safely without erasing history.

## 7. Minimum Viable Registry Design

The smallest practical design is:

1. one small registry module under `scripts/`
2. static metadata for the five active fixture/sample families listed above
3. no extraction
4. no directory changes
5. no rekeying of existing WP8 fixture item identities

## C. Compatibility Shim Strategy

## 1. Script Compatibility Approach

First implementation principle:

- reduce path coupling before introducing file-move wrappers

That means the first slice should prefer:

- resolver-based defaults
- resolver-based module loading

before adding legacy wrappers.

Script surfaces that will require compatibility shims once moves begin:

- `scripts/eval_canonical_manifest.py`
- `scripts/stage_c1_evaluator_foundation.py`
- `scripts/stage_c2_family_state_reconciliation_foundation.py`
- `scripts/stage_c3_evaluator_runtime_integration.py`
- `scripts/stage_c4_real_output_ingestion.py`
- `scripts/stage_c5_scoring_path_integration.py`
- `scripts/stage_c6_scoring_report_integration.py`
- `scripts/stage_c8_non_authoritative_detector_projection_adapter.py`
- later, the core framework entrypoints if they move:
  - `scripts/train_lora_sft.py`
  - `scripts/preflight_lora_run.py`
  - `scripts/build_dataset_v1.py`

Script surfaces that do not need first-slice shims:

- historical Stage B recovery builders and validators
- historical blocker-branch methodology scripts
- bootstrap-only or deprecated documentation-linked scripts

Reason:

- these are preserved history, not the first active migration target

## 2. Test Compatibility Approach

The first test strategy should avoid adding test wrappers.

Instead:

- add one shared test-side path helper or reuse the resolver directly
- replace absolute `SCRIPT_PATH`, `FIXTURES_ROOT`, and sample-path constants in the directly affected tests

Tests that belong in the minimum slice:

- `tests/test_eval_canonical_manifest.py`
- `tests/test_stage_c1_evaluator_foundation.py`
- `tests/test_stage_c2_family_state_reconciliation_foundation.py`
- `tests/test_stage_c3_evaluator_runtime_integration.py`
- `tests/test_stage_c4_real_output_ingestion.py`
- `tests/test_stage_c5_scoring_path_integration.py`
- `tests/test_stage_c6_scoring_report_integration.py`
- `tests/test_stage_c8_non_authoritative_detector_projection_adapter.py`

Tests that do not need first-slice compatibility work:

- `tests/test_dataset_contract.py`
- historical blocker-branch and runtime-forensics tests
- legacy surfaces not required for the first migration unlock

Reason:

- the first slice should target the active move blockers, not all path references in the repository

## 3. Documentation Compatibility Approach

The first compatibility slice should not implement documentation shims broadly.

Recommended first documentation rule:

- no doc shims during compatibility slice zero
- use indexes and redirects only when a document family is actually scheduled to move

Documentation surfaces likely to require redirect-style treatment later:

- `docs/convergence/`
- `docs/process_infrastructure/`
- selected high-citation doctrine docs if their paths change

Documentation surfaces that do not need shims in the first implementation slice:

- `docs/current/`
- `docs/housekeeping/`
- low-citation historical materials not on the first structural-move path

## 4. Minimum Shim Posture

The smallest safe shim posture is:

- no wrapper files in the first compatibility implementation slice
- only resolver-based indirection and loader abstraction
- wrapper files introduced later, immediately before the first physical script moves

This keeps H-05 aligned with the goal of small, low-risk increments.

## D. Minimum Viable Implementation Slice

## 1. Implementation Slice Definition

Recommended first implementation package:

- `CL-01`
- title: `Active Evaluator And Fixture Path Decoupling`

## 2. In-Scope Work For `CL-01`

1. Add a repository resolver helper under the current `scripts/` surface.
2. Add a small in-place fixture/sample registry under the current `scripts/` surface.
3. Convert the active evaluator and Stage C integration chain to:
   - resolve script dependencies by role
   - resolve fixture roots by role
   - resolve sample artifacts by role
   - resolve threshold profile by role
4. Update the directly dependent tests listed in Section C to use the same role-based resolution pattern.
5. Add narrow validation for the resolver and registry plus targeted existing tests.

## 3. Explicitly Out Of Scope For `CL-01`

- structural file moves
- fixture extraction
- report extraction
- doc redirects
- historical script conversion
- bulk test conversion
- canonical manifest redesign
- external runtime path portability cleanup

## 4. Why `CL-01` Is The Smallest Practical Slice

`CL-01` materially reduces the strongest live couplings because it addresses:

- sibling-path dynamic script loading
- WP8 fixture root hard-coding
- threshold-profile hard-coding
- tracked `reports/stage_c*` sample-path hard-coding

At the same time, it avoids broad code churn because it does not touch:

- the full Stage B historical builder family
- the broad documentation corpus
- historical provenance artifacts
- directory structure

## 5. Immediate Migration Value

If `CL-01` succeeds, the repository gains four immediate benefits:

1. active code no longer identifies fixtures and samples by absolute path
2. future fixture/sample relocation becomes much smaller in scope
3. future script moves can use role-based loaders instead of sibling-path assumptions
4. the active migration blocker surface becomes isolated from the broader historical archive

## 6. Deferred Follow-On Slice

The next likely slice after `CL-01` should be narrow and optional:

- `CL-02`
- title: `Core Script Default Path Decoupling`

Likely scope:

- `scripts/build_dataset_v1.py`
- optionally `scripts/train_lora_sft.py`
- optionally `scripts/preflight_lora_run.py`

This should remain separate from `CL-01` unless validation shows the extra scope is truly low-cost.

## E. Migration Enablement Assessment

| H-02 migration family | Compatibility prerequisite satisfied by `CL-01` | Blockers that would remain |
|---|---|---|
| `README.md` and `AGENTS.md` | None required from compatibility layer | documentation and navigation updates only |
| Doctrine docs | None directly | future doc-path redirects or link rewrites if doctrine moves |
| `docs/process_infrastructure/`, `docs/lineages/`, selected synthesis docs | None directly | documentation citation and index work still required |
| Bulk `docs/convergence/` history | None directly | canonical record index, redirect strategy, and high-citation link handling still required |
| `docs/continuity/`, `docs/history/`, bootstrap docs, proposals | None directly | history indexes and archive-placement decisions still required |
| Canonical eval manifest and eval corpora | Partially: resolver pattern can later absorb manifest and dataset roles | frozen-manifest dual-path design and dataset-path portability still remain |
| Core scripts: `train_lora_sft.py`, `preflight_lora_run.py`, `build_dataset_v1.py`, `eval_canonical_manifest.py` | `eval_canonical_manifest.py` becomes materially less coupled; resolver architecture becomes available for the remaining core scripts | `train_lora_sft.py`, `preflight_lora_run.py`, and `build_dataset_v1.py` still need direct adoption or a follow-on slice |
| `scripts/stage_c1_evaluator_foundation.py` | yes: fixture root becomes role-based instead of absolute | future wrapper needed only once physical move begins |
| `scripts/stage_c2...stage_c8` integration scripts and direct tests | yes: dynamic loader chain, fixtures, samples, and threshold profile can be role-based | physical relocation still blocked until code and tests adopt the new layer and validate |
| Stage C blocker-branch package scripts and tests | Indirect only: they can reuse the same resolver pattern later | no direct blocker removal in the first slice |
| `manifests/environment/` | None directly | low-risk documentation and manifest reference work still required |
| WP8 fixture corpus and threshold profile | yes: both gain stable active identities without moving | actual extraction out of `manifests/reports/` still remains blocked until later validation |
| Bulk `manifests/reports/` outside active fixtures | Indirect only: active-versus-historical distinction becomes clearer | history indexing and archive movement strategy still required |
| `reports/stage_c1-6/` | yes for the active sample-input subset | full split between active samples and historical reports still remains |
| `configs/lora/`, `manifests/runs/`, `data/v1_0/` | None directly | example extraction, historical separation, and path cleanup in historical builders still required |
| `data/tool_ft_allaliases_20260525_from_qual_reports*` | None required | preserved as provenance-bearing historical data |
| Local-only cleanup surfaces | None required | later cleanup remains a separate decision |

## Summary

`CL-01` does not unblock every H-02 migration family.

It does unblock the highest-value active families first:

- active evaluator chain
- active fixture root
- threshold profile
- active Stage C sample inputs

That is enough to make later structural moves safer without dragging the whole repository into the first implementation slice.

## F. Implementation Readiness Determination

## Determination

After H-05, the repository is ready for actual compatibility-layer implementation in a small, validation-driven slice.

It is not ready for broad compatibility rollout or structural migration in the same phase.

## What Is Ready

Ready after H-05:

- implement `CL-01`
- keep implementation within the existing `scripts/` and `tests/` surfaces
- validate only the directly affected active chain first
- use registry-in-place rather than extraction

## What Is Not Ready

Not ready after H-05:

- repository-wide resolver adoption
- fixture extraction
- history/report relocation
- documentation-family relocation
- pruning or deletion
- coupling the compatibility implementation to the full future repository architecture

## Required Guardrails For Implementation

Actual implementation should proceed only if it follows these guardrails:

1. no structural moves in the same package as `CL-01`
2. no provenance record rewriting
3. no doctrine changes
4. targeted tests only for the directly affected chain first
5. explicit rollback criteria for resolver and registry adoption

## Final Readiness Answer

Yes, conditionally.

H-05 provides sufficient authority and design clarity to begin actual compatibility-layer implementation, but only as the narrow `CL-01` slice defined in this document.
