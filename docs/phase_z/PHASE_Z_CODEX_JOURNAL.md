# Phase Z Codex Journal

## Work Log

1. Promoted the control-arm execution assets:
   - [configs/lora/stage_b_llama31_8b_base_v1_phase_z_control.config.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_z_control.config.json)
   - [manifests/runs/stage_b_llama31_8b_base_v1_phase_z_control.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_z_control.run_manifest.json)
2. Ran `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_z_control.run_manifest.json` successfully.
3. Launched governed training on the control arm only.
4. Trained to completion on the Phase Y control dataset.
5. Launched the frozen canonical evaluation contract with the explicit local mirror override.
6. Polled the long evaluation run at a two-minute interval until completion.
7. Captured the evaluation summary and comparison bundle.

## Validation

- `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_z_control.run_manifest.json`: PASS
- Training: PASS
- Canonical evaluation: PASS
- `git diff --check`: PASS

## Commit And Push

- Commit: `39c4534` - `feat: execute phase z control arm`
- Push: `git push origin main` succeeded
- Remote update: `origin/main` advanced from `fe98746` to `39c4534`
- Packaging note: the initial artifact-heavy push was rejected by GitHub size limits, so the published commit excludes the oversized checkpoint blobs under `artifacts/stage_b_llama31_8b_base_v1_phase_z_control/checkpoints/`.

## Runtime Notes

- Training runtime: `165.6615s`
- Canonical evaluation runtime: `30.5152s`
- Evaluation run name: `phase_z_control_eval_20260613T002335Z`
- Local base-model override used for canonical evaluation:

```text
--model-name-or-path /mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base
```

## Current Determination

- Promotion determination: `Do Not Promote`
- Next action: `Proceed next to Treatment A`

## Boundary Confirmation

- No Treatment A, Treatment B, or Treatment C run was launched.
- No evaluator logic changed.
- No scoring logic changed.
- No governance or threshold changes were made.
- The control arm remained contamination-clean.
