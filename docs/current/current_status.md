# Current Status

This page records the accepted alpha-package baseline for public inspection. Use it to tell at a glance whether a surface is active framework, curated historical evidence, or still parked.

## Repository Objective

The repository objective is to present a reproducible post-training and evaluation regimen that can be inspected without exposing a full archive of working history.

## Accepted Current State

- Stage B is complete.
- Wave 1 is complete and closed.
- Compatibility adoption is complete and closed.
- The curated public package has a defined alpha baseline.
- A curated Llama 3.1 baseline evidence package is published.
- The Stage C runtime-output / corpus-behavior family remains parked.

## What Is Active Now

No broader structural work is active on this baseline. Current posture:

- preserve the curated public package as the current presentation surface
- keep the published baseline package under `evals/baselines/llama31/` and `docs/current/baselines/` aligned with the front door
- keep the alpha-preparation boundary narrow and reviewable
- authorize any later structural work separately before additional expansion begins
- maintain the living training-run history log at [status/TRAINING_RUN_HISTORY.md](status/TRAINING_RUN_HISTORY.md) after each completed run

## What Is Preserved As Current Method

The following remain active framework or infrastructure surfaces in the current package:

- doctrine
- canonical evaluation contract
- curated Llama 3.1 baseline evidence under `evals/baselines/llama31/`
- core training, dataset, and evaluation scripts
- process infrastructure under `docs/framework/process_infrastructure/`
- distilled methodology under `docs/framework/methodology/`
- lineages under `docs/framework/lineages/`
- core contract tests
- active compatibility and path-resolution support

## What Is Preserved As Curated History

The following remain preserved as curated historical evidence:

- the bounded lineage spine
- selected methodology transition records
- selected current-state milestone records
- selected housekeeping and front-door review records

## Current Boundary

The curated public package remains intentionally bounded.

Still out of scope on this baseline:

- archive formation
- deletion or pruning work
- fixture or sample extraction beyond the accepted alpha package
- Stage C runtime-output / corpus-behavior execution
- broader structural expansion without separate authorization

The current boundary is a preparation boundary, not a publication boundary.
