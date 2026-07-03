# Current Status

This page records the accepted baseline and the current boundary for public-inspection work. Use it to tell at a glance whether a surface is active framework, preserved history, or still parked.

## Repository Objective

The repository objective is to create a reusable post-training and evaluation regimen that generalizes beyond the current model, dataset, repository state, or investigation family.

## Accepted Current State

- Stage B is complete.
- Stage C blocker-oriented branch is complete.
- The runtime-output / corpus-behavior investigation family is defined and parked.
- Wave 1 is complete and closed.
- Compatibility adoption is complete and closed.
- The merged `main` branch is the canonical repository baseline for future work.

## What Is Active Now

No structural housekeeping execution or Stage C investigation execution is active on this baseline. Current posture:

- preserve the merged baseline as the current canonical state
- authorize the next major phase separately before additional housekeeping or Stage C execution begins

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

Wave 1 and compatibility adoption are part of the accepted merged baseline. Closure records:

- `docs/housekeeping/W1-13_WAVE_1_CLOSURE_REPORT.md`
- `docs/housekeeping/CA-06_COMPATIBILITY_ADOPTION_CLOSURE_REPORT.md`

## Current Boundary

The completed Wave 1 migration and completed compatibility adoption slice are part of the current repository state.

Broader migration and Stage C runtime-output execution remain gated:

- no Wave 2 or later movement
- no archive formation
- no pruning or deletion work
- no fixture or sample extraction
- no Stage C runtime-output / corpus-behavior execution without separate reactivation authorization

Deletion and pruning remain out of scope.
