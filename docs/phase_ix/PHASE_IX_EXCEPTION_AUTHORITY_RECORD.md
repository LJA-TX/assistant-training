# Phase IX Exception Authority Record

## Purpose

Record the operator-authorized, post-closure exception for a single H1 diversity probe.

## Basis For Execution

- Operator authorization explicitly allows one run of `H1_diversity_patch`.
- The run is a scientific follow-up activity after formal Phase I closure.
- The goal is to acquire the missing diversity-intervention datapoint without reopening Phase I.

## Governance Status

- Phase I remains formally closed.
- The official Phase I determination remains unchanged.
- This exception does not reopen Phase I and does not authorize any additional H-series runs.

## Exception Scope

Authorized activity:

- execute `H1_diversity_patch` once
- run canonical evaluation immediately after training
- document the result against H0 and H2
- record scientific interpretation and supplemental closure

Unauthorized activity:

- reopening Phase I
- altering Phase I conclusions
- authorizing H3 or H4
- authorizing any additional internal runs
- redesigning governance, stop rules, datasets, masking, optimizer, LoRA topology, or evaluation methodology

## Execution Boundaries

- use the already-approved H1 assets
- keep the dataset, config, optimizer, masking, LoRA topology, and evaluation methodology unchanged
- maintain existing validation controls
- treat the run as diagnostic, report-only, non-promotional, and post-closure

## Reviewed H1 Exception Evidence

The following supporting reviews were inspected and recorded:

- `docs/phase_i/PHASE_I_H1_EXCEPTION_REVIEW_Grok-Build.md`
- `docs/phase_i/PHASE_I_H1_EXCEPTION_REVIEW_GB-Composer.md`

These reviews are supporting evidence only. They do not override operator authorization.

## Official Phase I Determination

Official Phase I determination remains unchanged.

## Resulting Paths

- Config: `/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.config.json`
- Run manifest: `/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.run_manifest.json`
- Train data: `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_train.jsonl`
- Val data: `/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_val.jsonl`
- Run root: `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch`
- Adapter output dir: `/opt/ai-stack/assistant-training/artifacts/adapters/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch`
- Logs dir: `/opt/ai-stack/assistant-training/artifacts/logs/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch`

## Status

Ready for the single authorized exception run.
