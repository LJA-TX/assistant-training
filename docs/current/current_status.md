# Current Status

## Repository Objective

The repository objective is to create a reusable post-training and evaluation regimen that generalizes beyond the current model, dataset, repository state, or investigation family.

## Accepted Current State

- Stage B is complete.
- Stage C blocker-oriented branch is complete.
- The runtime-output / corpus-behavior investigation family is defined and parked.
- Housekeeping is the active phase.
- The authorized minimal Wave 1 structural migration is complete.

## What Is Active Now

The active workstream is housekeeping for long-term framework reuse. Current focus:

- validating the executed Wave 1 separation
- preserving compatibility and rollback safety
- preparing only later, separately authorized migration waves

## What Is Preserved And Still Active

The following remain active framework or infrastructure surfaces in the current repository layout:

- doctrine
- canonical evaluation contract and pinned eval corpora
- core training, dataset, and evaluation scripts
- process infrastructure under `docs/framework/process_infrastructure/`
- distilled methodology under `docs/framework/methodology/`
- lineages under `docs/framework/lineages/`
- core contract tests
- active fixture and threshold surfaces used by scripts and tests

## What Is Preserved As History

The following remain preserved project history and provenance:

- bulk convergence records
- continuity snapshots
- deprecated doctrine versions
- historical configs and run manifests
- historical dataset lineage
- historical report bundles

## Housekeeping State

Housekeeping authorities H-01 through H-05 remain accepted.

Wave 1 structural execution is governed by:

- `docs/housekeeping/W1-05_REVISED_MINIMAL_FRAMEWORK_SEPARATION_EXECUTION_PLAN.md`
- `docs/housekeeping/W1-07_WAVE_1_AUTHORIZATION_GAP_CLOSURE.md`
- `docs/housekeeping/W1-08_FINAL_WAVE_1_AUTHORIZATION_DECISION.md`

## Current Boundary

The first bounded structural migration wave is part of the current repository state.

Broader migration remains gated:

- no Wave 2 or later movement
- no archive formation
- no pruning or deletion work
- no fixture or sample extraction in this wave

Deletion and pruning remain out of scope.
