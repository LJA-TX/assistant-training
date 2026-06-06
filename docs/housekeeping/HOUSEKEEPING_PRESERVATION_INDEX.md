# Repository Classification and Preservation Index

## Work Package

- ID: `H-01`
- Title: `Repository Classification and Preservation Index`
- Repository: `/opt/ai-stack/assistant-training`
- Scope: classification and preservation mapping only
- Out of scope: file moves, renames, directory reorganization, doctrine changes, archival actions, deletions, migration commits

## Current State Verified During Inspection

- Stage B complete.
- Stage C blocker-oriented branch complete.
- Runtime-output / corpus-behavior investigation family defined but parked.
- Housekeeping phase active.

## Authority Basis

Classification precedence used for this package:

1. authoritative catalogs and planning artifacts
2. doctrine and governance artifacts
3. accepted readiness, closure, and milestone determinations
4. current executable and test dependencies
5. local repository layout and retained evidence surfaces

## Inspection Notes

- Direct inspection covered repository structure, tracked files, selected ignored local surfaces, doctrine, process infrastructure, convergence records, scripts, tests, data, manifests, and reports.
- The repository currently contains `1110` tracked files.
- High-volume tracked evidence surfaces include:
  - `docs/convergence/`: `257` files visible in the current worktree
  - `manifests/reports/`: `529` tracked files
  - `reports/`: `98` tracked files
  - `data/v1_0/`: `49` tracked files
- Ignored local-only surfaces remain materially large:
  - `artifacts/`: about `6.9G`
  - `local_review_bundles/`: about `756K`
- Local uncommitted housekeeping work was observed in the worktree. It was read only to avoid collisions and is not treated as accepted authority for this index.

## Classification Legend

- `Doctrine`: binding rules, contracts, scoring semantics, and governance authority
- `Framework Assets`: reusable artifacts intended to support future post-training work across projects
- `Reusable Methodology`: distilled lessons, repeatable process patterns, and generalizable assessment structures
- `Active Infrastructure`: code, tests, fixtures, and support artifacts still used by the current core tooling
- `Historical Evidence`: project-specific execution records needed for provenance, reproducibility, or later interpretation
- `Project History`: setup history, continuity handoff, deprecated versions, and bootstrap records
- `Archive Candidates`: should be preserved, but should leave the future primary navigation path
- `Cleanup Candidates`: low-value or local-only material that may later be removed or ignored with low preservation risk

Navigation roles used below:

- `Primary`: should remain on the future main navigation path
- `Reference`: should remain preserved and easy to find, but not headline navigation
- `Historical`: should remain preserved as project history or evidence
- `Archive`: should be retained but moved off the main path in a future housekeeping phase
- `Local-only`: not part of future tracked primary structure; preserve only if needed operationally

Preservation priorities used below:

- `Critical`: loss would materially damage provenance, doctrine, or reusable framework extraction
- `High`: loss would materially reduce reproducibility or methodology transfer
- `Medium`: preserve unless later superseded by an explicit replacement
- `Low`: low-value clutter or local-only operational residue

## A. Preservation Index

| Path family | Primary category | Future navigation role | Preservation priority | Classification notes |
|---|---|---:|---:|---|
| `AGENTS.md` | Framework Assets | Primary | Critical | Thin dispatcher, authority order, stop-and-escalate rules, and route map for recurring work. Preserve unchanged semantics. |
| `docs/goal_charter_v5a.md`, `docs/appendix_a_operational_execution_contract_v3a.md`, `docs/metric_specification_v1a.md` | Doctrine | Primary | Critical | Binding authority for project purpose, operational gates, and scoring semantics. These should never be removed. |
| `evals/canonical_eval_manifest_v1.json`, `evals/data/canonical_v1/` | Framework Assets | Primary | Critical | Canonical evaluation contract plus pinned eval corpora. Central to cross-run comparability and future reuse. |
| `scripts/train_lora_sft.py`, `scripts/preflight_lora_run.py`, `scripts/build_dataset_v1.py`, `scripts/eval_canonical_manifest.py` | Active Infrastructure | Primary | Critical | Current executable core of the reusable regimen. Preserve even if later refactored into a package. |
| `scripts/stage_c1_evaluator_foundation.py` and `tests/test_stage_c1_evaluator_foundation.py` | Active Infrastructure | Primary | Critical | Still loaded by the canonical evaluator. Not project history; this is now framework-grade core. |
| `docs/process_infrastructure/` | Framework Assets | Primary | High | Extracted checklists and templates for repeatable process work. Stable, reusable, and low-churn. |
| `manifests/environment/` | Framework Assets | Reference | High | Environment pinning and reproducibility snapshots. Important for serious-run provenance. |
| `manifests/reports/stage_b_wp8_validation/fixtures/` and `manifests/reports/stage_b_v1_threshold_profile.json` | Framework Assets | Primary | Critical | Fixture corpus and threshold contract still used by scripts, tests, and migration-preparation logic. Loss would damage both methodology and active infrastructure. |
| `docs/lineages/` | Reusable Methodology | Primary | High | Distilled lessons from contamination control, isolated-variable methodology, overconstraint collapse, and bounded implementation scaffolding. These are already compressed history and should stay close to the main path. |
| `docs/convergence/STAGE_B_COMPLETION_DETERMINATION.md`, `STAGE_BC_PROCESS_EXTRACTION_ASSESSMENT.md`, `STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md`, `STAGE_BC_PHASE1_PROCESS_INFRASTRUCTURE_CLOSURE_DETERMINATION.md`, `STAGE_C_PACKAGE_3C_REGIMEN_RETROSPECTIVE_AND_REUSABILITY_ASSESSMENT.md`, `STAGE_C_PACKAGE_5E_DIRECT_ANSWER_LIFECYCLE_RETROSPECTIVE_AND_REGIMEN_GENERALIZATION_ASSESSMENT.md`, `STAGE_C_PACKAGE_6A_FORMAL_BLOCKER_ORIENTED_REGIMEN_BRANCH_ADOPTION_ASSESSMENT.md`, `STAGE_C_PACKAGE_6B_CONDITIONAL_BLOCKER_ORIENTED_BRANCH_ADOPTION_DETERMINATION.md`, `STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md`, `STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md`, `STAGE_C10C_REFRESHED_DETECTOR_MIGRATION_GATE_DETERMINATION.md` | Reusable Methodology | Primary | Critical | These are the small subset of convergence documents that directly state current status or extract reusable regimen structure. Keep on the future primary path. |
| `scripts/stage_c2_family_state_reconciliation_foundation.py`, `stage_c3_evaluator_runtime_integration.py`, `stage_c4_real_output_ingestion.py`, `stage_c5_scoring_path_integration.py`, `stage_c6_scoring_report_integration.py`, `stage_c8_non_authoritative_detector_projection_adapter.py`, and their direct tests | Active Infrastructure | Reference | High | These are not just historical package scripts; they encode reusable integration and reporting logic and are still exercised by tests. Keep preserved until a deliberate extraction or refactor occurs. |
| `reports/stage_c1/` through `reports/stage_c6/` | Active Infrastructure | Reference | High | These tracked artifacts are used as sample inputs, integration fixtures, and validation baselines by current scripts and tests. They look duplicative but should not be removed casually. |
| `scripts/eval_adapter_toolcalls.py` and `tests/test_eval_adapter_toolcalls.py` | Framework Assets | Reference | Medium | Legacy direct tool-call harness. No longer the primary evaluator, but still useful as a compatibility and historical comparison surface. |
| `configs/lora/` and `manifests/runs/` | Historical Evidence | Reference | High | Serious-run configuration and intent records for completed lineage work. Useful as future examples, but the bulk is project-specific rather than primary framework navigation. |
| `data/v1_0/` | Historical Evidence | Reference | High | Versioned dataset lineage for Stage A/B execution history. Preserve for reproducibility and future example extraction. Not future primary navigation. |
| `data/tool_ft_allaliases_20260525_from_qual_reports*` | Historical Evidence | Historical | Medium | Rawer project-specific intake surfaces and summaries. Useful for provenance of data assembly, not central future navigation. |
| Bulk `manifests/reports/` run-specific artifacts outside the fixture corpus and threshold profile | Historical Evidence | Archive | High | Includes Stage B run reports, Stage C gate bundles, technical spike outputs, runtime forensics outputs, and probe records. Preserve for provenance, but move off the future main path. |
| Bulk `docs/convergence/` package-level assessments, package reviews, acceptance assessments, implementation summaries, runtime validation reports, and companion determinations not listed above | Historical Evidence | Archive | High | This is the main project execution log. Preserve because it contains the evidence chain, but it should become historical/reference material rather than future primary navigation. |
| `docs/continuity/` | Project History | Historical | Medium | Snapshot and handoff material. Preserve for orientation, but this is not the future reusable framework surface. |
| `docs/deprecated/` | Project History | Archive | High | Doctrine and charter version history. Not primary navigation, but should remain preserved for provenance and governance evolution. |
| `docs/assistant_training_initial_ChatGPT_thread_summary.md`, `docs/assistant_training_goal_documents_and_artifacts_index.md`, `docs/repository_establishment_plan_v1.md`, `docs/evaluation_manifest_v1.md`, `docs/migration_checklist.md` | Project History | Archive | Medium | Valuable for bootstrap provenance and early architecture intent, but no longer primary navigation. `docs/evaluation_manifest_v1.md` is a superseded precursor, not the live contract. |
| `docs/potential_skills/canonical_eval_stage_ab_skill.md` | Reusable Methodology | Archive | Medium | Seed material for later extraction into a reusable skill or operator guide. Preserve, but keep off the main path until formalized. |
| `scripts/build_stage_b_recovery_*.py`, `scripts/build_stage_b_v1_*_family_concentration_review.py`, `scripts/validate_stage_b_recovery_*.py`, `scripts/i8_diagnostics_scaffold.py`, `scripts/i9_diagnostics_scaffold.py`, `scripts/i10_diagnostics_scaffold.py`, `scripts/provision_geometry_probe_weights.py` | Historical Evidence | Archive | Medium | Encodes project-specific recovery interventions and diagnostics. Preserve as lineage evidence and future example material; do not keep on the main path. |
| `scripts/stage_c_package1b_passive_governance_consumer.py`, `stage_c_package1c_passive_reconciliation_surface.py`, `stage_c_package1d_migration_readiness_assessment.py`, `stage_c_package2a_gate_evidence_bundle.py`, `stage_c_package5b_direct_answer_blocker_persistence.py`, `stage_c_technical_spike_direct_answer_probe.py`, `stage_c_runtime_output_forensics_direct_answer_missing_evidence.py`, `stage_c_legacy_surface_validity_direct_answer_assessment.py`, and their tests | Reusable Methodology | Archive | High | These are the strongest project-specific methodology records for the blocker-oriented branch. They are not future primary runtime tooling, but they should be preserved because they explain how the blocker method was exercised. |
| `tests/test_dataset_contract.py`, `tests/test_masking_behavior.py`, `tests/test_eval_canonical_manifest.py` | Active Infrastructure | Primary | Critical | These tests protect current core contracts. They stay near the main path. |
| Remaining Stage C package and migration-preparation tests | Historical Evidence | Reference | High | These are methodology-protection tests. Preserve until equivalent framework-level tests exist. |
| `local_review_bundles/` | Cleanup Candidates | Local-only | Low | Operational review packets and zip bundles. Useful during execution, but not part of authoritative tracked framework history. Future cleanup can remove them after confirming corresponding tracked artifacts exist. |
| `artifacts/`, `evals/runs/`, `.pytest_cache/`, `__pycache__/`, empty `staging/assistant-runtime/` | Cleanup Candidates | Local-only | Low | Heavy generated outputs, caches, and empty staging residue. These do not belong on the future primary path and are the safest later cleanup targets. |

## Observed Local Worktree Items Not Treated As Accepted Authority

The following visible local changes were not treated as accepted repository authority for this classification package:

- modified `README.md`
- untracked `docs/convergence/HOUSEKEEPING_ASSESSMENT_Grok-Build.md`
- untracked `docs/convergence/HOUSEKEEPING_REPOSITORY_WIDE_ASSESSMENT_Codex.md`
- untracked `docs/housekeeping_assessment_v1.md`
- untracked `docs/using_the_regimen.md`

They may become important later, but they are currently local worktree state, not accepted governance or established framework structure.

## B. Framework vs History Assessment

### What Should Remain On The Future Primary Navigation Path

- `README.md` as the front door for the reusable regimen
- `AGENTS.md`
- doctrine:
  - `docs/goal_charter_v5a.md`
  - `docs/appendix_a_operational_execution_contract_v3a.md`
  - `docs/metric_specification_v1a.md`
- canonical evaluation contract and pinned eval corpora:
  - `evals/canonical_eval_manifest_v1.json`
  - `evals/data/canonical_v1/`
- core executable infrastructure:
  - `scripts/train_lora_sft.py`
  - `scripts/preflight_lora_run.py`
  - `scripts/build_dataset_v1.py`
  - `scripts/eval_canonical_manifest.py`
  - `scripts/stage_c1_evaluator_foundation.py`
- process scaffolding:
  - `docs/process_infrastructure/`
- distilled methodology:
  - `docs/lineages/`
- selected synthesis and status documents from `docs/convergence/`:
  - Stage B completion
  - Stage BC process extraction and architecture
  - Stage C reusable regimen extraction and blocker-branch closure
  - runtime-output / corpus-behavior launch plan
  - current migration-preparation determination

### What Should Become Historical Or Reference Material

- bulk Stage B and Stage C convergence package records
- run-specific configs and run manifests
- Stage A/B lineage datasets under `data/v1_0/`
- most run-specific `manifests/reports/`
- continuity snapshots
- repository bootstrap and establishment records
- non-primary evaluators and one-off probes

### What Should Be Archived

- companion acceptance assessments and implementation summaries once they are linked to a canonical primary record
- deprecated doctrine versions
- bulk convergence package history
- most project-specific builder, validator, and diagnostics scripts
- proposal-only documents such as `docs/potential_skills/canonical_eval_stage_ab_skill.md`

### What Should Never Be Removed

- doctrine authority documents
- canonical eval manifest and eval corpora
- current core scripts and their core contract tests
- process infrastructure checklists and templates
- Stage B fixture corpus and threshold profile
- `docs/lineages/`
- selected current-state and synthesis convergence docs listed in this index
- tracked `reports/stage_c1-6/` until tests and scripts stop depending on them

## C. Proposed Repository Architecture

This section recommends a future structure only. No structural changes are implemented by this package.

### Proposed Top-Level Categories

- `docs/current/`
  - purpose: current state, start-here navigation, and active housekeeping outputs
- `docs/doctrine/`
  - purpose: charter, appendix, metric spec, and stable authority pointers
- `docs/framework/`
  - purpose: reusable regimen guidance, lineages, process infrastructure, and selected methodology synthesis docs
- `regimen/` or `framework/`
  - purpose: extracted executable reusable core for training, evaluation, dataset building, and contract validation
- `examples/`
  - purpose: minimal example configs, manifests, sample datasets, and serious-run templates
- `history/`
  - purpose: archived convergence history, continuity snapshots, deprecated doctrine, bootstrap records, and lineage-specific execution evidence
- `history/reports/`
  - purpose: run-specific `manifests/reports/`, historical config and dataset snapshots, and bundled package evidence not needed on the main path
- `fixtures/` or `framework/fixtures/`
  - purpose: reusable WP8 validation fixtures and stable sample artifact bundles currently embedded in `manifests/reports/` and `reports/stage_c*`

### Rationale

- The repository now has two real products:
  - a reusable post-training and evaluation framework
  - a historical execution record for one large Llama-centered research effort
- The current structure mixes them in the same visible path, which makes onboarding and reuse harder than necessary.
- Future structure should separate:
  - binding doctrine
  - reusable executable core
  - reusable process and methodology
  - historical evidence and provenance
  - local-only operational residue

### Migration Considerations

- Hard-coded absolute paths exist across scripts, tests, configs, manifests, and documents. Structural housekeeping should not move those files until a path-migration plan or compatibility shim exists.
- `reports/stage_c1-6/` and `manifests/reports/stage_b_wp8_validation/fixtures/` are currently referenced directly by scripts and tests. Extract fixtures before moving or archiving them.
- `docs/convergence/` contains both reusable synthesis and historical package records. Create an index or canonical-record map before splitting that directory.
- `configs/lora/`, `manifests/runs/`, and `data/v1_0/` should remain intact until example/reference subsets are defined explicitly.
- Later structural housekeeping should be non-destructive first:
  - add new navigation layers
  - add pointers and indexes
  - only then move historical material
- Do not couple structural housekeeping to doctrine revision. The classification is already sufficient without changing doctrine.

## D. Preservation Risk Assessment

### Loss Would Damage Provenance

- `configs/lora/` and `manifests/runs/`
- `data/v1_0/`
- run-specific `manifests/reports/`
- current closure and transition determinations in `docs/convergence/`
- `docs/continuity/`
- `docs/deprecated/`

These artifacts prove what was run, what was concluded, and under which assumptions the project moved between stages.

### Loss Would Damage Methodology Extraction

- `AGENTS.md`
- `docs/process_infrastructure/`
- `docs/lineages/`
- `evals/canonical_eval_manifest_v1.json` and eval corpora
- `scripts/train_lora_sft.py`, `scripts/preflight_lora_run.py`, `scripts/build_dataset_v1.py`, `scripts/eval_canonical_manifest.py`, `scripts/stage_c1_evaluator_foundation.py`
- `manifests/reports/stage_b_wp8_validation/fixtures/`
- `manifests/reports/stage_b_v1_threshold_profile.json`
- selected synthesis convergence docs:
  - Stage BC process extraction
  - Stage C regimen retrospective
  - blocker-branch closure
  - runtime-output launch plan

These artifacts contain the actual reusable regimen mechanics and the reasoning that extracted them from project history.

### Artifacts That Look Redundant But Should Be Preserved

- `reports/stage_c1-6/`
  - reason: they are still used as sample inputs and integration fixtures by scripts and tests
- paired run-bundle artifacts such as:
  - `manifests/reports/stage_c_package2a_*`
  - `manifests/reports/stage_c_package5b_*`
  - `manifests/reports/stage_c_technical_spike_*`
  - `manifests/reports/stage_c_runtime_output_forensics_*`
  - `manifests/reports/stage_c_legacy_surface_validity_*`
  - reason: they support repeated-run stability and evidence-chain claims
- companion convergence documents such as acceptance assessments and implementation summaries
  - reason: they often record packaging outcome, boundary confirmation, or decision framing even when they overlap with the main assessment
- tracked draft configs and draft run manifests
  - reason: they can capture pre-approval intent or interim execution boundaries that matter to provenance

### Artifacts That Appear Genuinely Disposable

- `artifacts/`
- `local_review_bundles/`
- `.pytest_cache/`
- `__pycache__/`
- empty `staging/assistant-runtime/`

These are local-only, generated, or operational residue surfaces. They may still be useful temporarily, but their long-term preservation value is low compared with tracked doctrine, fixtures, reports, and determinations.

### Artifacts That Are Better Treated As Cleanup Candidates Than Disposable

- duplicate `data/README.md` and `data/README (data-intake).md`
- top-level bootstrap and indexing docs that have been superseded but still carry early provenance
- proposal-only skills or establishment plans

These are low-priority on the future primary path, but they are still better handled by archive or consolidation rather than blunt deletion.

## E. Housekeeping Readiness Determination

### Determination

Housekeeping classification confidence is sufficient to begin structural housekeeping.

### Confidence Level

- High confidence at the path-family level
- Medium confidence at the individual-file level inside:
  - `docs/convergence/`
  - `manifests/reports/`
  - `reports/`

### What This Means Practically

- The repository is ready for non-destructive structural housekeeping:
  - adding new navigation layers
  - introducing future archive/reference boundaries
  - separating framework and history in planned destination structures
- The repository is not yet ready for bulk deletion.
- Any later deletion phase should require a narrower redundancy audit after structural separation is complete.

### Guardrails For The Next Phase

- preserve all doctrine, fixture, and current-core script surfaces unchanged
- treat selected synthesis docs as canonical records before moving bulk convergence history
- do not move test-dependent `reports/stage_c*` artifacts until replacement fixture paths exist
- do not archive `manifests/reports/stage_b_wp8_validation/fixtures/` or `stage_b_v1_threshold_profile.json`
- do not treat local ignored outputs as part of the future primary navigation model

### Final Readiness Answer

Yes: sufficient classification confidence exists to begin structural housekeeping, provided the next phase is preservation-first, non-destructive, and guided by this index.
