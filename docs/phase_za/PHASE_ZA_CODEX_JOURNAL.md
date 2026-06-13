# Phase ZA Codex Journal

## Work Log

1. Promoted the Treatment A execution assets:
   - [configs/lora/stage_b_llama31_8b_base_v1_phase_za_treatment_a.config.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_za_treatment_a.config.json)
   - [manifests/runs/stage_b_llama31_8b_base_v1_phase_za_treatment_a.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_za_treatment_a.run_manifest.json)
2. Ran `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_za_treatment_a.run_manifest.json` successfully.
3. Launched governed training on Treatment A only.
4. Trained to completion on the Phase Y Treatment A dataset.
5. Launched the frozen canonical evaluation contract with the explicit local mirror override.
6. Polled the long evaluation run at a two-minute interval until completion.
7. Captured the evaluation summary and comparison bundle.

## Validation

- `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_za_treatment_a.run_manifest.json`: PASS
- Training: PASS
- Canonical evaluation: PASS
- `git diff --check`: PASS

## Commit And Push

- Commit: `5b2ed90` - `feat: execute phase za treatment a arm`
- Push: `git push origin main` succeeded
- Remote update: `origin/main` advanced from `766d8fe` to `5b2ed90`
- Packaging note: the published commit excludes the oversized checkpoint blobs under `artifacts/stage_b_llama31_8b_base_v1_phase_za_treatment_a/checkpoints/`.

## Runtime Notes

- Training runtime: `165.8693s`
- Canonical evaluation runtime: `30.5104s`
- Evaluation run name: `phase_za_treatment_a_eval_20260613T005031Z`
- Local base-model override used for canonical evaluation:

```text
--model-name-or-path /mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base
```

## Current Determination

- Promotion determination: `Do Not Promote`
- Next action: `Proceed to Treatment B`

## Boundary Confirmation

- No Treatment B or Treatment C run was launched.
- No evaluator logic changed.
- No scoring logic changed.
- No governance or threshold changes were made.
- The Treatment A arm remained contamination-clean.
