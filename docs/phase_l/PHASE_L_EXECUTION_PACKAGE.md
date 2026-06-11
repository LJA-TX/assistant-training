# Phase L Execution Package

## Executive Summary

Phase L is the first governed training-and-evaluation package for Dataset v1.1.
It does not launch training in this phase. It prepares the draft configuration, run manifest, comparison method, and stop rules needed for a later authorized run.

The package is built around the external-first, safety-calibrated hybrid interpretation from Phase J and the validated Dataset v1.1 candidate from Phase K.

## Selected Execution Shape

| Item | Selection |
|---|---|
| Base model | `llama-3.1-8b-base` |
| Trainer | `scripts/train_lora_sft.py` |
| Evaluator | `scripts/eval_canonical_manifest.py` |
| Dataset | `data/v1_1/dataset_v1_1_train.jsonl` and `data/v1_1/dataset_v1_1_val.jsonl` |
| Canonical eval authority | `evals/canonical_eval_manifest_v1.json` |
| Config draft | `configs/lora/stage_b_llama31_8b_base_v1_phase_l_v1_1_external_first.config.draft.json` |
| Run manifest draft | `manifests/runs/stage_b_llama31_8b_base_v1_phase_l_v1_1_external_first.run_manifest.draft.json` |

## Package Invariants

1. No training is launched in this phase.
2. No evaluator or scorer behavior is changed.
3. No canonical eval manifest, decode default, or governance rule is changed.
4. The comparison target remains H0, H1, and H2 under the frozen canonical eval contract.
5. The run remains draft-not-started until explicit manual authorization is recorded.

## Package Contents

- Training configuration selection
- Baseline comparison method
- Contamination safeguards
- Promotion criteria
- Success and failure thresholds
- Stop rules
- Runtime requirements
- Expected outputs
- Readiness assessment

## Rationale

The Phase I evidence already showed that H1 and H2 split the metric families.
Dataset v1.1 is intended to test whether those gains can be retained together while also keeping the refusal surface exact.

This package therefore keeps the trainer geometry fixed and treats Dataset v1.1 as the controlled variable.
