# W1-11 Wave 1 Rollback Verification Inputs

## Scope

This record preserves the reviewable rollback-verification inputs for the isolated Wave 1 merge candidate.

It does not execute rollback.

## Canonical Evidence Files

- Move manifest: `docs/housekeeping/W1-11_WAVE_1_MOVE_MANIFEST.txt`
- Hash baseline: `docs/housekeeping/W1-11_WAVE_1_HASH_BASELINE.sha256`

## Source And Candidate Branches

- Raw execution branch: `housekeeping/w1-execution`
- Isolated merge-candidate branch: `housekeeping/w1-merge-candidate`

## Verification Inputs

### Critical Canonical Targets

Validate the presence of:

1. `docs/framework/process_infrastructure/`
2. `docs/framework/lineages/`
3. `docs/framework/methodology/`
4. `docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md`
5. `docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md`

### Critical Compatibility Surfaces

Validate the presence of:

1. `docs/process_infrastructure/README.md`
2. `docs/lineages/README.md`
3. `docs/convergence/README.md`
4. all `40` exact-file aliases named by the Wave 1 alias families

### Critical Governance And Index Surfaces

Validate the presence and consistency of:

1. `AGENTS.md`
2. `docs/housekeeping/indexes/index_registry.json`
3. `docs/housekeeping/indexes/convergence_history_index.json`
4. `scripts/validate_housekeeping_indexes.py`

## Expected Validation Checks

Run:

1. `python scripts/validate_housekeeping_indexes.py`
2. exact-file alias completeness validation
3. `AGENTS.md` canonical route-asset validation
4. exhaustive in-scope historical citation validation
5. `git diff --check`

## Hash-Comparison Rule

For moved files whose content should remain identical after canonical relocation:

1. compare the current canonical target hash against `docs/housekeeping/W1-11_WAVE_1_HASH_BASELINE.sha256`
2. expect exact preservation

For the reconciled methodology record:

1. `docs/framework/methodology/STAGE_BC_PHASE1_PROCESS_INFRASTRUCTURE_CLOSURE_DETERMINATION.md`
2. expect a content change relative to the baseline because W1-07 required narrow factual reconciliation

## Rollback Success Standard

Rollback would be considered ready for verification only if:

1. original source paths remain fully known through the move manifest
2. pre-move hashes remain reviewable through the baseline file
3. old exact paths and new canonical paths can both be validated from repository-resident evidence
