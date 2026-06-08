# assistant-training

This repository is the curated public package for a runtime-oriented assistant-training regimen. It is intentionally lean: it explains the doctrine, evaluation contract, current-state guidance, and a bounded historical evidence spine without turning the repository into an archive.

## What This Repository Shows

- the regimen and its governing doctrine
- the pinned canonical evaluation contract
- the scripts and tests that make the contract inspectable
- the curated historical evidence that explains how the method evolved

## Quick Orientation

| Question | Read first |
| --- | --- |
| What is this repository? | [docs/current/current_status.md](docs/current/current_status.md) |
| Why does it exist? | [docs/goal_charter_v5a.md](docs/goal_charter_v5a.md) and [docs/appendix_a_operational_execution_contract_v3a.md](docs/appendix_a_operational_execution_contract_v3a.md) |
| How do current method and history differ? | [docs/current/framework_vs_history.md](docs/current/framework_vs_history.md) |
| Where do I start? | [docs/current/start_here.md](docs/current/start_here.md) |
| What is the evidence spine? | [docs/framework/lineages/README.md](docs/framework/lineages/README.md) |

## First Inspection Path

1. [docs/current/start_here.md](docs/current/start_here.md)
2. [docs/current/current_status.md](docs/current/current_status.md)
3. [docs/current/framework_vs_history.md](docs/current/framework_vs_history.md)
4. [docs/framework/lineages/README.md](docs/framework/lineages/README.md)
5. [docs/goal_charter_v5a.md](docs/goal_charter_v5a.md)
6. [docs/appendix_a_operational_execution_contract_v3a.md](docs/appendix_a_operational_execution_contract_v3a.md)

## Core Inspection Targets

- [docs/metric_specification_v1a.md](docs/metric_specification_v1a.md)
- [evals/canonical_eval_manifest_v1.json](evals/canonical_eval_manifest_v1.json)
- [scripts/build_dataset_v1.py](scripts/build_dataset_v1.py)
- [scripts/preflight_lora_run.py](scripts/preflight_lora_run.py)
- [scripts/train_lora_sft.py](scripts/train_lora_sft.py)
- [scripts/eval_canonical_manifest.py](scripts/eval_canonical_manifest.py)
- [scripts/stage_c1_evaluator_foundation.py](scripts/stage_c1_evaluator_foundation.py)
- [scripts/repo_paths.py](scripts/repo_paths.py)
- [tests/test_dataset_contract.py](tests/test_dataset_contract.py)
- [tests/test_masking_behavior.py](tests/test_masking_behavior.py)
- [tests/test_eval_canonical_manifest.py](tests/test_eval_canonical_manifest.py)
- [tests/test_eval_adapter_toolcalls.py](tests/test_eval_adapter_toolcalls.py)
- [tests/test_repo_paths.py](tests/test_repo_paths.py)
- [tests/test_compatibility_path_resolution.py](tests/test_compatibility_path_resolution.py)

## Curated Historical Evidence

- [docs/framework/lineages/README.md](docs/framework/lineages/README.md)
- [docs/framework/methodology/](docs/framework/methodology/)
- [docs/current/status/](docs/current/status/)
- [docs/current/roadmap/](docs/current/roadmap/)
- [docs/housekeeping/OSS_01_INDEPENDENT_REVIEW_AND_RECONCILIATION_GROK.md](docs/housekeeping/OSS_01_INDEPENDENT_REVIEW_AND_RECONCILIATION_GROK.md)
- [docs/housekeeping/OSS_05_PUBLIC_FRONT_DOOR_IMPLEMENTATION_SUMMARY.md](docs/housekeeping/OSS_05_PUBLIC_FRONT_DOOR_IMPLEMENTATION_SUMMARY.md)

## Boundary

This repository is not a bulk archive.

Keep the public surface focused on:

- doctrine
- current-state guidance
- reproducibility contracts
- scripts and tests
- curated historical evidence

Leave bulk data, bulk report surfaces, and internal planning noise out of the public package unless a later authorization says otherwise.
