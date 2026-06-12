# Phase Q Codex Journal

Purpose: record the Dataset v1.2 governed run, validation, commit, and push status.

## 2026-06-12

- Reviewed the controlling evidence from Phase L, Phase M, Phase N, Phase O, Phase I, and Phase IX before executing Phase Q.
- Promoted the approved Phase L run assets into the v1.2 execution pair:
  - `configs/lora/stage_b_llama31_8b_base_v1_phase_q_v1_2_anchor_weighted_hybrid.config.json`
  - `manifests/runs/stage_b_llama31_8b_base_v1_phase_q_v1_2_anchor_weighted_hybrid.run_manifest.json`
- Ran `git diff --check` successfully before execution.
- Ran `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_q_v1_2_anchor_weighted_hybrid.run_manifest.json` successfully.
- Executed the governed training run with:
  - `python scripts/train_lora_sft.py --config configs/lora/stage_b_llama31_8b_base_v1_phase_q_v1_2_anchor_weighted_hybrid.config.json`
- Training completed successfully.
  - `train_runtime = 161.7761s`
  - `train_loss = 0.7323995166354709`
  - `eval_loss = 0.43417230248451233`
- Executed the frozen canonical evaluation contract with the local mirror override required by this workspace:
  - `python scripts/eval_canonical_manifest.py --manifest evals/canonical_eval_manifest_v1.json --model-name-or-path /mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base --adapter-dir artifacts/adapters/stage_b_llama31_8b_base_v1_phase_q_v1_2_anchor_weighted_hybrid --out-dir evals/runs/phase_q_v1_2_anchor_weighted_hybrid_eval_20260612T101256Z`
- Canonical evaluation completed successfully.
  - `exact_json_validity = 0.03`
  - `invalid_json_rate = 0.2`
  - `tool_name_accuracy = 0.07142857142857142`
  - `argument_accuracy = 0.04285714285714286`
  - `wrapper_leakage = 0.0`
  - `no_call_correctness = 0.7666666666666667`
  - `adversarial_no_call_correctness = 0.3`
- Contamination remained zero in the dataset and in the frozen eval contract.
- Determination: `Do Not Promote`
- Substantive milestone commit:
  - `e4fec73` - `Phase Q: add governed v1.2 execution review`
- Push result:
  - `git push origin main` succeeded
  - `origin/main` advanced from `51af394` to `e4fec73`
- Validation outcomes:
  - `git diff --check`: PASS
  - `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_q_v1_2_anchor_weighted_hybrid.run_manifest.json`: PASS
  - training: PASS
  - canonical evaluation: PASS
- Current focus:
  - The governed v1.2 run is complete.
  - The evidence supports another design pass rather than promotion.
  - No evaluator, scoring, governance, or dataset modifications were made during execution.
