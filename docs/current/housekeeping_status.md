# Housekeeping Status

## Accepted Housekeeping Authorities

The following are accepted governing housekeeping documents:

- [../housekeeping/HOUSEKEEPING_PRESERVATION_INDEX.md](../housekeeping/HOUSEKEEPING_PRESERVATION_INDEX.md)
- [../housekeeping/HOUSEKEEPING_ARCHITECTURE_AND_MIGRATION_PLAN.md](../housekeeping/HOUSEKEEPING_ARCHITECTURE_AND_MIGRATION_PLAN.md)
- [../housekeeping/HOUSEKEEPING_PATH_DECOUPLING_AND_COMPATIBILITY_STRATEGY.md](../housekeeping/HOUSEKEEPING_PATH_DECOUPLING_AND_COMPATIBILITY_STRATEGY.md)
- [../housekeeping/HOUSEKEEPING_COMPATIBILITY_LAYER_IMPLEMENTATION_PLAN.md](../housekeeping/HOUSEKEEPING_COMPATIBILITY_LAYER_IMPLEMENTATION_PLAN.md)

Their roles are:

- H-01: classification and preservation authority
- H-02: target architecture and migration authority
- H-03: path-decoupling and compatibility authority
- H-05: compatibility-layer implementation authority

Wave 1 execution was governed by:

- `../housekeeping/W1-05_REVISED_MINIMAL_FRAMEWORK_SEPARATION_EXECUTION_PLAN.md`
- `../housekeeping/W1-07_WAVE_1_AUTHORIZATION_GAP_CLOSURE.md`
- `../housekeeping/W1-08_FINAL_WAVE_1_AUTHORIZATION_DECISION.md`

Compatibility adoption was governed by:

- `../housekeeping/CA-02_COMPATIBILITY_ADOPTION_IMPLEMENTATION_SLICE.md`
- `../housekeeping/CA-03_COMPATIBILITY_ADOPTION_MERGE_READINESS_AND_AUTHORIZATION_REVIEW.md`
- `../housekeeping/CA-05_FINAL_COMPATIBILITY_ADOPTION_AUTHORIZATION_DECISION.md`

## Current Structural State

The authorized minimal Wave 1 framework-history separation and the authorized compatibility adoption slice are part of the current repository state.

Wave 1 canonicalized:

- canonical process-infrastructure location is now `../framework/process_infrastructure/`
- canonical lineage location is now `../framework/lineages/`
- selected reusable methodology records now live under `../framework/methodology/`
- the Stage B completion marker now lives under `status/`
- the parked runtime-output planning anchor now lives under `roadmap/`

Compatibility aliases preserve the old exact file paths for Wave 1 records.

Compatibility adoption additionally established:

- resolver-based active path handling under `../../scripts/repo_paths.py`
- bounded active evaluator-chain adoption of resolver-based paths
- bounded core entrypoint path decoupling for training, preflight, and dataset building surfaces

## Current Boundary

The current merged baseline does not itself authorize:

- additional structural waves
- archival execution
- fixture or sample extraction
- pruning or deletion
- Stage C runtime-output / corpus-behavior execution
- methodology or doctrine redesign

## Why Broader Migration Remains Gated

Broader structural work still depends on later migration-wave authorization and validation:

- archive formation planning
- fixture and sample-artifact separation
- broader convergence-history treatment
- later wave dependency review

The parked Stage C runtime-output / corpus-behavior family also requires explicit reactivation before execution resumes.

Until those later phases are separately authorized, the repository should be treated as a closed post-Wave-1, post-compatibility baseline.

## Next Permitted Phase

The next permitted phase is either later-wave housekeeping planning or explicit Stage C reactivation planning.

Deletion and pruning remain explicitly out of scope.
