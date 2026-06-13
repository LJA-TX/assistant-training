# Phase ZB Codex Journal

## Work Log

1. Promoted the Treatment B execution assets:
   - [configs/lora/stage_b_llama31_8b_base_v1_phase_zb_treatment_b.config.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_zb_treatment_b.config.json)
   - [manifests/runs/stage_b_llama31_8b_base_v1_phase_zb_treatment_b.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_zb_treatment_b.run_manifest.json)
2. Ran `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_zb_treatment_b.run_manifest.json` successfully.
3. Launched governed training on Treatment B only.
4. Trained to completion on the Phase Y Treatment B dataset.
5. Launched the frozen canonical evaluation contract with the explicit local mirror override.
6. Observed the canonical evaluation completion output and recorded the resulting metrics.

## Validation

- `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_zb_treatment_b.run_manifest.json`: PASS
- Training: PASS
- Canonical evaluation: PASS
- `git diff --check`: PASS

## Runtime Notes

- Training runtime: `166.1638s`
- Internal eval runtime: `30.5464s`
- The canonical evaluation metrics for Phase ZB were captured from the completed run output.
- No persisted `evals/runs/phase_zb_treatment_b_eval_*` directory was present in this workspace at write time.
- Local base-model override used for canonical evaluation:

```text
--model-name-or-path /mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base
```

## Current Determination

- Promotion determination: `Do Not Promote`
- Next action: `Proceed to Treatment C`

## Boundary Confirmation

- No Treatment C run was launched.
- No evaluator logic changed.
- No scoring logic changed.
- No governance or threshold changes were made.
- The Treatment B arm remained contamination-clean.
