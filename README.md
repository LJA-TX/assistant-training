# assistant-training

This repository documents an ongoing effort to develop, validate, and document a reproducible training and evaluation methodology for tool-calling assistants built from open-weight language models.

The current experimental platform is Llama-3.1-8B-Base, but the long-term goal is a model-agnostic regimen that can be applied across future open-weight models.

This repository is presented as a curated public package rather than a complete project archive. It focuses on methodology, evaluation contracts, tooling, current-state guidance, and selected historical evidence that explains how the approach evolved.

## Public Snapshot Identity

This repository is published under Publication Lineage Version 2. The package is living and curated; the record below identifies one historical frozen publication point rather than a promise that future repository heads remain unchanged.

| Field | Value |
| --- | --- |
| Snapshot ID | `publication-lineage-v2-snapshot-v1` |
| Snapshot version | `v1` |
| Publication date | `2026-07-11` |
| Status | living curated package with a frozen historical publication snapshot |
| Public snapshot commit | `05634b6a3f47dfd6cf5656d4ab8da7997bf894d1` |
| Private lineage commit | `9d88798c506328635200b95b5aff9234dc127079` |

Machine-readable record: [docs/publication/public_snapshot.json](docs/publication/public_snapshot.json)

This snapshot identifies a historical publication point in a related public/private lineage, not an identical mirror. Future commits do not invalidate the snapshot, and private engineering work continues independently.

## Project Status & Philosophy

The overall project remains active.
This public repository is maintained as a bounded curated package of the current framework, evidence spine, baselines, and status documents rather than an open-ended working archive.

### What Has Been Achieved So Far

The project has developed and documented a repeatable regimen covering:

- Definition of target assistant behaviors
- Dataset construction and curation strategies
- Evaluation contracts and automated validation
- Detection of contamination, overfitting, and subtle failure modes
- Governed and reproducible iteration cycles

### Key Insights

The work has surfaced several important failure modes that conventional benchmarks often fail to reveal:

- Evaluation/runtime divergence
- Overconstraint collapse
- Wrapper-behavior persistence
- Schema-coupling effects
- Tool-selection and restraint failures

The project has also developed practical methods for detecting, measuring, and mitigating these issues.

### Current Focus

The overall project remains in active development.

Current project-level work remains focused on understanding the relationship between offline evaluation results and real-world runtime behavior and on maintaining a reusable training and evaluation framework. This bounded public repository preserves the current framework, baselines, evidence spine, and status surfaces; it does not imply active Stage C execution or open-ended structural work.

### Why This Repository Exists

This repository exists to share the methodology, tooling, evaluation surfaces, evidence trail, and lessons learned throughout that process.

The long-term goal is not merely to produce a single strong adapter. The larger objective is to develop a reusable training and evaluation framework that can help improve future generations of open-weight tool-calling models.

## Repository History

**July 2026 — Publication Lineage Version 2**

This repository has been under active development for considerably longer than the visible commit history on the `main` branch may suggest.

In July 2026, the project underwent a deliberate repository-topology remediation after a workflow issue caused content that was not intended for this repository to be committed directly to it for several weeks.

Once the issue was discovered, the repository was intentionally rebuilt beginning with **Publication Lineage Version 2**. As a result, the commit history visible on this branch begins with this reconstructed lineage rather than with the repository's original published history.

This reconstruction preserved the project's intended content while establishing a durable and safe publication workflow. Future commits will continue incrementally from this publication lineage.

## What This Repository Shows

- the regimen and its governing doctrine
- the pinned canonical evaluation contract
- a curated Llama 3.1 baseline evidence package
- the scripts and tests that make the contract inspectable
- the curated historical evidence that explains how the method evolved

## Plain-English Overview

Casual readers who want a low-jargon introduction can start with [docs/current/plain_english_project_summary.md](docs/current/plain_english_project_summary.md).

This page is an informal overview, not an authority or governance document.

## Quick Orientation

| Question | Read first |
| --- | --- |
| What is this repository? | [docs/current/current_status.md](docs/current/current_status.md) |
| What has the project accomplished so far? | [docs/current/project_outcomes_to_date.md](docs/current/project_outcomes_to_date.md) |
| What defines the current Gen-2 framing? | [docs/current/status/GEN2_PROGRAM_CHARTER.md](docs/current/status/GEN2_PROGRAM_CHARTER.md), [docs/current/status/GEN2_PROSPECTIVE_EVIDENCE_PROGRAM_ASSESSMENT.md](docs/current/status/GEN2_PROSPECTIVE_EVIDENCE_PROGRAM_ASSESSMENT.md), [docs/current/status/GEN2_STRATEGIC_DIRECTION_OPTIONS_ASSESSMENT.md](docs/current/status/GEN2_STRATEGIC_DIRECTION_OPTIONS_ASSESSMENT.md), and [docs/current/status/GEN2_SCOPE_BOUNDARY_ASSESSMENT.md](docs/current/status/GEN2_SCOPE_BOUNDARY_ASSESSMENT.md) |
| Where are the published baseline artifacts? | [docs/current/baselines/README.md](docs/current/baselines/README.md) |
| What is the current closure and handoff posture? | [docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md](docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md), [docs/current/status/D1_CLOSURE_AND_D2_READINESS_ASSESSMENT.md](docs/current/status/D1_CLOSURE_AND_D2_READINESS_ASSESSMENT.md), and [docs/current/status/GEN2_PROGRAM_CHARTER.md](docs/current/status/GEN2_PROGRAM_CHARTER.md) |
| What is the current readiness baseline? | [docs/current/status/D1_CLOSURE_AND_D2_READINESS_ASSESSMENT.md](docs/current/status/D1_CLOSURE_AND_D2_READINESS_ASSESSMENT.md) and [docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md](docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md) |
| Why does it exist? | [docs/goal_charter_v5a.md](docs/goal_charter_v5a.md) and [docs/appendix_a_operational_execution_contract_v3a.md](docs/appendix_a_operational_execution_contract_v3a.md) |
| How do current method and history differ? | [docs/current/framework_vs_history.md](docs/current/framework_vs_history.md) |
| Where do I start? | [docs/current/start_here.md](docs/current/start_here.md) |
| What is the evidence spine? | [docs/framework/lineages/README.md](docs/framework/lineages/README.md) |

## First Inspection Path

1. [docs/current/start_here.md](docs/current/start_here.md)
2. [docs/current/current_status.md](docs/current/current_status.md)
3. [docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md](docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md)
4. [docs/current/status/D1_CLOSURE_AND_D2_READINESS_ASSESSMENT.md](docs/current/status/D1_CLOSURE_AND_D2_READINESS_ASSESSMENT.md)
5. [docs/current/status/GEN2_PROGRAM_CHARTER.md](docs/current/status/GEN2_PROGRAM_CHARTER.md)
6. [docs/framework/lineages/README.md](docs/framework/lineages/README.md)
7. [docs/framework/methodology/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md](docs/framework/methodology/STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md)
8. [docs/continuity/D0_TO_CURRENT_TREE_MECHANISM_ISOLATION_GOVERNANCE.md](docs/continuity/D0_TO_CURRENT_TREE_MECHANISM_ISOLATION_GOVERNANCE.md)
9. [docs/goal_charter_v5a.md](docs/goal_charter_v5a.md)
10. [docs/appendix_a_operational_execution_contract_v3a.md](docs/appendix_a_operational_execution_contract_v3a.md)

## Core Inspection Targets

- [docs/current/baselines/README.md](docs/current/baselines/README.md)
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
- [docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md](docs/current/status/STAGE_B_COMPLETION_DETERMINATION.md)
- [docs/framework/methodology/STAGE_BC_PROCESS_EXTRACTION_ASSESSMENT.md](docs/framework/methodology/STAGE_BC_PROCESS_EXTRACTION_ASSESSMENT.md)
- [docs/housekeeping/OSS_01_INDEPENDENT_REVIEW_AND_RECONCILIATION_GROK.md](docs/housekeeping/OSS_01_INDEPENDENT_REVIEW_AND_RECONCILIATION_GROK.md)
- [docs/housekeeping/OSS_05_PUBLIC_FRONT_DOOR_IMPLEMENTATION_SUMMARY.md](docs/housekeeping/OSS_05_PUBLIC_FRONT_DOOR_IMPLEMENTATION_SUMMARY.md)
