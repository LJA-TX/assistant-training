# Housekeeping Status

## Accepted Housekeeping Authorities

The following are accepted governing housekeeping documents:

- [../housekeeping/HOUSEKEEPING_PRESERVATION_INDEX.md](../housekeeping/HOUSEKEEPING_PRESERVATION_INDEX.md)
- [../housekeeping/HOUSEKEEPING_ARCHITECTURE_AND_MIGRATION_PLAN.md](../housekeeping/HOUSEKEEPING_ARCHITECTURE_AND_MIGRATION_PLAN.md)
- [../housekeeping/HOUSEKEEPING_PATH_DECOUPLING_AND_COMPATIBILITY_STRATEGY.md](../housekeeping/HOUSEKEEPING_PATH_DECOUPLING_AND_COMPATIBILITY_STRATEGY.md)

Their roles are:

- H-01: classification and preservation authority
- H-02: target architecture and migration authority
- H-03: path-decoupling and compatibility authority

Wave 1 execution is additionally governed by:

- `../housekeeping/W1-05_REVISED_MINIMAL_FRAMEWORK_SEPARATION_EXECUTION_PLAN.md`
- `../housekeeping/W1-07_WAVE_1_AUTHORIZATION_GAP_CLOSURE.md`
- `../housekeeping/W1-08_FINAL_WAVE_1_AUTHORIZATION_DECISION.md`

## Current Structural State

The authorized minimal Wave 1 framework-history separation is part of the current repository state.

Wave 1 changed only the approved surfaces:

- canonical process-infrastructure location is now `../framework/process_infrastructure/`
- canonical lineage location is now `../framework/lineages/`
- selected reusable methodology records now live under `../framework/methodology/`
- the Stage B completion marker now lives under `status/`
- the parked runtime-output planning anchor now lives under `roadmap/`

Compatibility aliases preserve the old exact file paths for Wave 1 records.

## Current Boundary

Wave 1 does not authorize:

- additional structural waves
- archival execution
- code changes
- test changes
- doctrine changes
- runtime, evaluator, scorer, detector, threshold, or training behavior changes

## Why Broader Migration Remains Gated

Broader structural work still depends on later migration-wave authorization and validation:

- archive formation planning
- fixture and sample-artifact separation
- broader convergence-history treatment
- later wave dependency review

Until those later waves are separately authorized, the repository should be treated as a bounded Wave 1 execution surface only.

## Next Permitted Phase

The next permitted phase is post-execution review, remediation if needed, and later separately authorized migration planning.

Deletion and pruning remain explicitly out of scope.
