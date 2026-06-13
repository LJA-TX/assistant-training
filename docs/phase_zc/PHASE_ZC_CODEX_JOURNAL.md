# Phase ZC Codex Journal

## Work Log

1. Promoted the Treatment C execution assets:
   - [configs/lora/stage_b_llama31_8b_base_v1_phase_zc_treatment_c.config.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_zc_treatment_c.config.json)
   - [manifests/runs/stage_b_llama31_8b_base_v1_phase_zc_treatment_c.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_zc_treatment_c.run_manifest.json)
2. Ran `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_zc_treatment_c.run_manifest.json` successfully.
3. Launched governed training on Treatment C only.
4. Trained to completion on the Phase Y Treatment C dataset.
5. Launched the frozen canonical evaluation contract with the explicit local mirror override.
6. Polled the long evaluation run at a two-minute interval until completion.
7. Captured the evaluation summary and comparison bundle from the completed run.

## Validation

- `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_zc_treatment_c.run_manifest.json`: PASS
- Training: PASS
- Canonical evaluation: PASS
- `git diff --check`: PASS

## Runtime Notes

- Training runtime: `167.0348s`
- Canonical evaluation runtime: `30.5103s`
- Evaluation run name: `phase_zc_treatment_c_eval_20260613T212800Z`
- Local base-model override used for canonical evaluation:

```text
--model-name-or-path /mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base
```

## Current Determination

- Promotion determination: `Do Not Promote`
- Sweep conclusion: `Mixed response`
- Anchor concentration as sole explanation: `Not sufficient`

## Boundary Confirmation

- No additional treatment arm was launched.
- No evaluator logic changed.
- No scoring logic changed.
- No governance or threshold changes were made.
- The Treatment C arm remained contamination-clean.
