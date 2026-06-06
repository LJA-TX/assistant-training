# W1-03 Wave 1 Execution Readiness And Independent Risk Review

## Work Package

- ID: `W1-03`
- Title: `Wave 1 Execution Readiness And Independent Risk Review`
- Repository: `/opt/ai-stack/assistant-training`
- Scope: assessment only
- Review posture: skeptical, false-negative-biased, execution-denial unless the plan survives direct challenge
- Authority basis:
  - `docs/housekeeping/HOUSEKEEPING_PRESERVATION_INDEX.md`
  - `docs/housekeeping/HOUSEKEEPING_ARCHITECTURE_AND_MIGRATION_PLAN.md`
  - `docs/housekeeping/HOUSEKEEPING_PATH_DECOUPLING_AND_COMPATIBILITY_STRATEGY.md`
  - `docs/housekeeping/HOUSEKEEPING_COMPATIBILITY_LAYER_IMPLEMENTATION_PLAN.md`
  - CL-01 implementation artifacts
  - CL-02 implementation artifacts
  - `docs/housekeeping/MP-01_MIGRATION_PREPARATION_BOUNDARY_ASSESSMENT.md`
  - `docs/housekeeping/MP-02_CANONICAL_MIGRATION_MAP_AND_INDEXING_PLAN.md`
  - `docs/housekeeping/W0-01_CANONICAL_INDEX_FRAMEWORK_DESIGN.md`
  - `docs/housekeeping/W0-02_CANONICAL_INDEX_INFRASTRUCTURE_IMPLEMENTATION.md`
  - `docs/housekeeping/W0-03_INDEX_POPULATION_STRATEGY_AND_SCOPE_DETERMINATION.md`
  - `docs/housekeeping/W1-01_FRAMEWORK_HISTORY_SEPARATION_ASSESSMENT.md`
  - `docs/housekeeping/W1-02_MINIMAL_FRAMEWORK_SEPARATION_IMPLEMENTATION_PLAN.md`
- Out of scope:
  - implementation
  - file movement
  - restructuring
  - archive creation
  - code changes
  - doctrine changes

## Inspection Basis

Repository review for this package included:

- direct review of W1-02 against H-01 through H-05, MP-01, MP-02, W0-01 through W0-04, and W1-01
- repository-wide path-consumer search for the proposed move targets
- review of the current index registry, convergence-history index, and validator behavior
- review of active navigation, `AGENTS.md`, and preserved historical/report surfaces that cite the proposed move targets

Observed citation density relevant to W1-02:

- about `80` tracked references to `docs/process_infrastructure/`
- about `46` tracked references to `docs/lineages/`
- about `151` tracked references to the selected convergence records W1-02 proposes to move

Observed index coverage relevant to W1-02:

- W1-02 proposes moving `13` convergence records
- the current `convergence_history_index.json` covers only `5` of those physical records
- at least `8` proposed moved convergence records currently lack index entries

## Executive Conclusion

W1-02 does not survive independent execution-readiness review.

The plan is directionally aligned with the housekeeping program, but it is not safe to authorize as written because it understates live path consumers, overstates the adequacy of directory-level redirects, and broadens the primary-path move set beyond what H-01 classifies as future-primary material.

## A. Plan Integrity Review

### Alignment With Prior Authority

W1-02 is broadly aligned with the idea of a minimal framework-first separation, but it is not tightly aligned with the narrower controls established earlier:

1. H-01 classifies `docs/process_infrastructure/`, `docs/lineages/`, and a selected subset of convergence records as future-primary material.
2. MP-01 and MP-02 allow those families to move only with preconditions, especially citation treatment, canonical indexes, and preservation crosswalks.
3. H-03 explicitly treats documentation and citation coupling as a separate migration problem and names `AGENTS.md` as a migration-sensitive path consumer.

### Integrity Findings

1. W1-02 omits `AGENTS.md` from the move plan, redirect plan, validation plan, and rollback plan even though H-03 already identifies it as a direct consumer of `docs/process_infrastructure/...` paths.
2. W1-02 moves the launch-plan companion documents
   - `STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN_ACCEPTANCE_ASSESSMENT.md`
   - `STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN_IMPLEMENTATION_SUMMARY.md`
   into `docs/current/roadmap/`, but H-01 classifies companion acceptance and implementation summaries as archive/reference material once the canonical primary record exists.
3. W1-02 assumes that redirect stubs are sufficient provenance protection for moved convergence records. That is weaker than the preservation logic in MP-01 and MP-02, which requires preserved old-path discoverability without weakening the evidence chain.
4. W1-02 assumes rollback is available, but the core alias mechanism is unresolved. A rollback plan built on an unspecified alias model is not execution-grade.

### Integrity Conclusion

W1-02 is planning-complete enough for discussion, but not integrity-complete enough for authorization.

## B. Move Inventory Review

### 1. `docs/process_infrastructure/`

Hidden and overlooked consumers:

- `AGENTS.md` contains concrete route-asset paths for specific checklist and template files.
- tracked convergence and housekeeping docs cite specific nested checklist/template paths, not just the directory root.

Assessment:

- The proposed directory-level move is not inherently unsafe.
- The proposed compatibility treatment is unsafe because W1-02 does not define file-level preservation for the nested assets cited from `AGENTS.md` and historical docs.

Movement recommendation:

- Do not execute this move under the current plan.
- At minimum, this family should not move until exact path preservation for nested checklist/template files is specified.

### 2. `docs/lineages/`

Hidden and overlooked consumers:

- preserved report/manifests surfaces reference specific lineage files by exact path, including absolute repository paths
- examples include:
  - `manifests/reports/stage_b_v1_i10_semantic_commitment_reconnaissance.json`
  - `manifests/reports/stage_b_v1_i10_semantic_substitution_taxonomy.json`
  - `manifests/reports/stage_b_v1_i10r_microprobe_forensic_index.md`

Assessment:

- This family is more provenance-coupled than W1-02 treats it.
- A directory-level pointer page at `docs/lineages/` would not preserve exact-file discoverability for those preserved references.

Movement recommendation:

- Do not execute this move under the current plan.
- This family should remain in place until exact-file alias preservation is planned.

### 3. Selected `docs/convergence/` Methodology And Status Records

Hidden and overlooked consumers:

- the selected records are high-citation assets used across `docs/convergence/`, housekeeping docs, README/current navigation, and preserved report surfaces
- the current selected set has about `151` tracked references across the repository

Assessment:

- W1-02 correctly recognizes these records as future-primary, but it treats physical relocation as lower risk than the repository evidence supports.
- Several of these records are both current-path assets and historical anchors. That dual role is not fully resolved by the current crosswalk plan.
- The current convergence-history index covers only `5` of the `13` proposed moved convergence records.

Movement candidates that should remain in place under the current plan:

- `docs/convergence/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN_ACCEPTANCE_ASSESSMENT.md`
- `docs/convergence/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN_IMPLEMENTATION_SUMMARY.md`

Rationale:

- Those two are companion records, not primary framework/current-state records under H-01.
- Moving them to `docs/current/roadmap/` weakens the framework-history boundary rather than clarifying it.

### 4. `docs/current/` Navigation Repointing

Assessment:

- Repointing `README.md` and `docs/current/*.md` is expected.
- The risk is not in changing those navigation files.
- The risk is that W1-02 treats navigation updates as if they were the full consumer inventory. They are not.

## C. Redirect And Crosswalk Review

### Redirect Strategy Review

The redirect strategy is not execution-ready.

Key gaps:

1. W1-02 does not choose a redirect mechanism:
   - symlink-style alias
   - per-file stub
   - duplicate compatibility copy
   - some other filesystem-level alias
2. Directory-level pointer pages are insufficient for nested references like:
   - `docs/process_infrastructure/checklists/hygiene_review_checklist.md`
   - `docs/process_infrastructure/templates/milestone_determination_template.md`
   - `docs/lineages/i9_post_eval_checkpoint.md`
3. W1-02 does not distinguish between:
   - discoverability redirects for humans
   - exact-path preservation for preserved historical citations

### Stable-ID And Index Strategy Review

The crosswalk plan is incomplete.

Key gaps:

1. The current `convergence_history_index.json` covers only `5` of the `13` proposed moved convergence records.
2. W1-02 says `convergence_history_index.json` will be updated, but it does not explicitly include the matching `index_registry.json` `entry_count` updates required by the current validator.
3. W1-02 special-cases the launch-plan companion docs, but it does not spell out full stable-ID minting or entry creation for the other `8` currently unindexed moved convergence records.
4. No equivalent canonical index or citation crosswalk is defined for moved `docs/process_infrastructure/*` and `docs/lineages/*` files themselves.

### Crosswalk Conclusion

The redirect and crosswalk layer is the strongest reason not to execute W1-02 as written.

## D. Validation And Rollback Review

### Pre-Move Validation Critique

Missing safeguards:

1. No explicit `AGENTS.md` route-asset validation, even though H-03 names that exact check.
2. No repo-wide high-citation audit for moved documentation families.
3. No validation that every preserved absolute historical file reference still resolves to the original content or an exact-file compatibility target.
4. No requirement for a clean structural baseline beyond `git diff --check`; whitespace cleanliness is not execution-state cleanliness.

### Post-Move Validation Critique

Missing safeguards:

1. W1-02 checks existence of redirect stubs, not adequacy of those stubs.
2. There is no post-move comparison of target-file hashes against the pre-move baseline hashes.
3. There is no explicit validation that the index registry and family entry counts remain coherent after new convergence entries are added.
4. There is no explicit sampled audit of preserved historical documents that cite moved paths.

### Rollback Validation Critique

Missing safeguards:

1. No mechanism is defined for restoring exact-file compatibility aliases if the initial alias mechanism is itself unresolved.
2. No requirement exists to prove that old-path citations again resolve to the original content after rollback.
3. No baseline snapshot artifact, commit boundary, or frozen move manifest output is required beyond narrative planning.

### Rollback Trigger Critique

The rollback triggers are too narrow.

Missing triggers include:

- missing exact-file alias coverage for a cited historical path
- any unresolved `AGENTS.md` route-asset reference
- registry or index entry-count mismatch after entry creation
- any moved companion record appearing on the primary path contrary to H-01 classification

## E. Risk Assessment

| Risk category | Rating | Justification |
|---|---|---|
| Active workflow risk | `High` | `AGENTS.md` is a live process dispatcher surface with concrete `docs/process_infrastructure/...` file references. W1-02 does not include it in execution, validation, or rollback. |
| Provenance risk | `High` | preserved reports/manifests cite exact lineage files; selected convergence records are historical anchors; redirect notes are weaker than preserved original-path content for evidence-bearing records. |
| Discoverability risk | `High` | the proposed move touches families with about `80`, `46`, and `151` tracked references respectively; W1-02 validates only a narrow navigation subset. |
| Maintenance risk | `Medium` | the long-term moved layout is manageable, but only if the repository first defines a concrete alias model and complete crosswalk coverage. W1-02 does not. |
| Rollback risk | `High` | rollback depends on an unresolved alias mechanism, incomplete consumer inventory, and insufficient content-identity verification. |

## F. Execution Recommendation

### Recommendation

`1. Do Not Execute`

### Justification

W1-02 should not be executed as written because the plan fails three execution-readiness tests:

1. it misses live hard consumers such as `AGENTS.md`
2. it proposes a redirect model that is too weak for exact-file historical citations
3. it broadens the moved current-path set to include companion records that H-01 does not keep on the future primary path

This is not a minor polish issue. It is a boundary and safety issue.

## G. Authorization Readiness Determination

### Determination

`Not Ready`

### Why

The repository may be close to authorization for a very small first structural move, but W1-02 is not yet the package that should be authorized.

Current blockers to authorization of W1-02 include:

1. unresolved exact-path preservation for `docs/process_infrastructure/*` and `docs/lineages/*`
2. incomplete convergence index coverage for the proposed moved record set
3. missing treatment of `AGENTS.md` as a hard consumer
4. overbroad inclusion of launch-plan companion documents on the future current path
5. insufficient validation and rollback safeguards for a first structural migration

### Final Readiness Answer

Do not authorize the first structural migration package on the basis of W1-02 alone.

The current plan has not passed independent risk review.
