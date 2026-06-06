# W1-11 Wave 1 Merge Readiness Remediation

## Work Package

- ID: `W1-11`
- Title: `Wave 1 Merge Readiness Remediation`
- Repository: `/opt/ai-stack/assistant-training`
- Raw execution branch: `housekeeping/w1-execution`
- Isolated merge-candidate branch: `housekeeping/w1-merge-candidate`
- Scope: remediation only
- Authority basis:
  - `W1-09` executed Wave 1 branch state
  - `docs/housekeeping/W1-10_WAVE_1_POST_EXECUTION_VERIFICATION_AND_MERGE_READINESS_REVIEW.md`
- Out of scope:
  - Wave 2 work
  - archive formation
  - pruning
  - additional structural migration
  - merge
  - push

## Corrective Action Summary

The minimum safe corrective action was:

1. preserve `housekeeping/w1-execution` unchanged as the raw execution branch
2. create a clean isolated merge-candidate branch from `main`
3. copy only the authorized Wave 1 payload and its minimum referenced support surfaces
4. normalize repo-facing wording from branch-local execution phrasing to merged repository-state phrasing
5. preserve rollback evidence inside the repository

This avoids rewriting the raw execution branch in place and removes the merge-governance contamination identified by `W1-10`.

## A. Merge Payload Isolation

### Affected Files

The resulting merge payload contains only:

1. `AGENTS.md`
2. `README.md`
3. `docs/current/*`
4. `docs/framework/*`
5. `docs/process_infrastructure/*` Wave 1 aliases and pointer page
6. `docs/lineages/*` Wave 1 aliases
7. `docs/convergence/README.md` plus the `11` authorized Wave 1 convergence aliases
8. `docs/housekeeping/README.md`
9. accepted housekeeping authority docs needed by repo-facing links:
   - `HOUSEKEEPING_PRESERVATION_INDEX.md`
   - `HOUSEKEEPING_ARCHITECTURE_AND_MIGRATION_PLAN.md`
   - `HOUSEKEEPING_PATH_DECOUPLING_AND_COMPATIBILITY_STRATEGY.md`
   - `HOUSEKEEPING_COMPATIBILITY_LAYER_IMPLEMENTATION_PLAN.md`
10. Wave 1 review and execution-governance docs:
   - `W1-01` through `W1-10`
11. index infrastructure under `docs/housekeeping/indexes/`
12. `scripts/validate_housekeeping_indexes.py`
13. the new W1-11 remediation and rollback-evidence records

### Retained Files

The following remain outside the merge payload and are not changed by this branch:

1. all executable compatibility-layer script changes from CL-01/CL-02
2. all test changes from CL-01/CL-02
3. unrelated housekeeping assessments outside the Wave 1 and required authority surfaces
4. runtime, fixture, sample, manifest, report, and broader convergence-history surfaces outside Wave 1

### Excluded Files

Explicitly excluded from the merge payload:

1. `repo_paths.py`
2. `scripts/repo_paths.py`
3. modified training/evaluator scripts from CL-01/CL-02
4. modified tests from CL-01/CL-02
5. `docs/convergence/HOUSEKEEPING_ASSESSMENT_Grok-Build.md`
6. `docs/convergence/HOUSEKEEPING_REPOSITORY_WIDE_ASSESSMENT_Codex.md`
7. `docs/housekeeping_assessment_v1.md`
8. `docs/using_the_regimen.md`
9. non-required earlier housekeeping planning families outside the accepted authority and Wave 1 review surface

### Resulting Merge Scope

The merge scope is now limited to:

1. the executed Wave 1 structural migration
2. its compatibility alias layer
3. the repo-facing wording normalization required for merged-state clarity
4. the reviewable index and rollback evidence required to assess that migration

## B. Repository-State Wording Normalization

Normalized repo-facing files:

1. `README.md`
2. `docs/current/current_status.md`
3. `docs/current/framework_vs_history.md`
4. `docs/current/housekeeping_status.md`
5. `docs/housekeeping/README.md`

Normalization was limited to:

1. removing branch-local execution phrasing such as "on this branch"
2. describing the Wave 1 state as repository state
3. updating housekeeping navigation text so it no longer describes the pre-Wave-1 boundary as current

## C. Rollback Evidence Preservation

Repository-resident rollback evidence created:

1. `docs/housekeeping/W1-11_WAVE_1_MOVE_MANIFEST.txt`
2. `docs/housekeeping/W1-11_WAVE_1_HASH_BASELINE.sha256`
3. `docs/housekeeping/W1-11_WAVE_1_ROLLBACK_VERIFICATION_INPUTS.md`

These preserve:

1. the original Wave 1 move inventory input list
2. the pre-move content-hash baseline captured during execution
3. the validation inputs needed to review rollback readiness without executing rollback

## D. Validation

Validation was re-run on `housekeeping/w1-merge-candidate`:

1. alias validation
2. `AGENTS.md` validation
3. convergence-index validation
4. exhaustive in-scope historical citation validation
5. rollback-readiness validation
6. merge-scope isolation checks

## E. Merge Readiness Assessment

### Determination

`3. Ready For Final Merge Authorization Review`

### Why

The blockers from `W1-10` are remediated:

1. the merge payload is isolated from unrelated CL-01/CL-02 work
2. repo-facing wording now describes merged repository state rather than branch-local execution state
3. rollback evidence is preserved inside the repository

This does not authorize merge.

It produces a clean Wave 1 merge candidate for final authorization review.
