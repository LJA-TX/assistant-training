# assistant-training

This repository develops a reusable post-training and evaluation regimen for runtime-oriented assistant models. It contains reusable doctrine, contracts, evaluation surfaces, training and dataset tooling, process infrastructure, and preserved project history from the Llama-3.1-8B-Base effort.

The repository is now on the merged post-Wave-1, post-compatibility-adoption baseline. Wave 1 framework-history separation and the bounded compatibility adoption slice are complete and closed. Broader history separation, archive formation, and pruning remain out of scope until later authorized work.

## Start Here

- Navigation entrypoint: [docs/current/start_here.md](docs/current/start_here.md)
- Current state: [docs/current/current_status.md](docs/current/current_status.md)
- Framework versus history map: [docs/current/framework_vs_history.md](docs/current/framework_vs_history.md)
- Housekeeping status and boundaries: [docs/current/housekeeping_status.md](docs/current/housekeeping_status.md)
- Housekeeping authorities: [docs/housekeeping/README.md](docs/housekeeping/README.md)

## Repository Identity

This repository now has five distinct value surfaces:

- Reusable regimen and framework:
  - doctrine
  - canonical evaluation contract
  - core training, dataset, and evaluation scripts
  - process infrastructure
  - distilled methodology
- Active infrastructure:
  - current executable scripts
  - current contract tests
  - active fixtures and threshold profiles still used by scripts and tests
- Doctrine and governance:
  - charter
  - operational execution contract
  - metric specification
- Project history and provenance:
  - convergence records
  - continuity records
  - run manifests
  - configs
  - historical reports
  - lineage datasets
- Parked investigation family:
  - runtime-output / corpus-behavior investigation planning is defined but not active

## Primary Framework Surfaces

- Doctrine:
  - [docs/goal_charter_v5a.md](docs/goal_charter_v5a.md)
  - [docs/appendix_a_operational_execution_contract_v3a.md](docs/appendix_a_operational_execution_contract_v3a.md)
  - [docs/metric_specification_v1a.md](docs/metric_specification_v1a.md)
- Canonical evaluation contract:
  - [evals/canonical_eval_manifest_v1.json](evals/canonical_eval_manifest_v1.json)
  - [evals/data/canonical_v1/](evals/data/canonical_v1/)
- Core executable infrastructure:
  - [scripts/train_lora_sft.py](scripts/train_lora_sft.py)
  - [scripts/preflight_lora_run.py](scripts/preflight_lora_run.py)
  - [scripts/build_dataset_v1.py](scripts/build_dataset_v1.py)
  - [scripts/eval_canonical_manifest.py](scripts/eval_canonical_manifest.py)
  - [scripts/stage_c1_evaluator_foundation.py](scripts/stage_c1_evaluator_foundation.py)
  - [scripts/repo_paths.py](scripts/repo_paths.py)
- Active validation and support surfaces:
  - `tests/test_dataset_contract.py`
  - `tests/test_masking_behavior.py`
  - `tests/test_eval_canonical_manifest.py`
  - `manifests/reports/stage_b_wp8_validation/fixtures/`
  - `manifests/reports/stage_b_v1_threshold_profile.json`
- Process and methodology:
  - [AGENTS.md](AGENTS.md)
  - [docs/framework/process_infrastructure/](docs/framework/process_infrastructure/)
  - [docs/framework/lineages/](docs/framework/lineages/)
  - [docs/framework/methodology/](docs/framework/methodology/)

## Project History And Provenance

The reusable framework is now minimally separated from bulk project history. Preserved historical material remains in its retained locations, including:

- `docs/convergence/`
- `docs/continuity/`
- `docs/deprecated/`
- `configs/lora/`
- `manifests/runs/`
- `manifests/reports/`
- `data/v1_0/`
- `reports/stage_c1/` through `reports/stage_c6/`

The old exact paths for moved Wave 1 records remain preserved through compatibility aliases.

## Parked Investigation Family

The runtime-output / corpus-behavior investigation family is defined but intentionally parked. The planning anchor for that family is:

- [docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md](docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md)

It is part of the preserved project trajectory, but it is not active execution work on the current baseline.

## Housekeeping Authority

Accepted housekeeping authorities are documented in [docs/housekeeping/README.md](docs/housekeeping/README.md).

Current governing housekeeping documents:

- [docs/housekeeping/HOUSEKEEPING_PRESERVATION_INDEX.md](docs/housekeeping/HOUSEKEEPING_PRESERVATION_INDEX.md)
- [docs/housekeeping/HOUSEKEEPING_ARCHITECTURE_AND_MIGRATION_PLAN.md](docs/housekeeping/HOUSEKEEPING_ARCHITECTURE_AND_MIGRATION_PLAN.md)
- [docs/housekeeping/HOUSEKEEPING_PATH_DECOUPLING_AND_COMPATIBILITY_STRATEGY.md](docs/housekeeping/HOUSEKEEPING_PATH_DECOUPLING_AND_COMPATIBILITY_STRATEGY.md)

## Current Boundary

This repository includes the completed Wave 1 structural migration and the completed compatibility adoption slice.

Still not authorized on this baseline:

- Wave 2 or later structural work
- archive formation
- deletions or pruning
- fixture or sample extraction
- Stage C runtime-output / corpus-behavior execution
- additional convergence-history cleanup beyond the completed Wave 1 move set

Broader migration and Stage C reactivation remain gated until later packages are separately authorized.
