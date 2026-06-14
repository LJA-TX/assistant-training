# Phase ZG Codex Journal

## Work Log

1. Reviewed the governing context for the topology sweep, including Phase ZF dataset-readiness artifacts, the prior Z control review, and the repository-recorded H1/H2 results from Phase IX / Phase I.
2. Promoted the ZG control execution assets:
   - [configs/lora/stage_b_llama31_8b_base_v1_phase_zg_control.config.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_zg_control.config.json)
   - [manifests/runs/stage_b_llama31_8b_base_v1_phase_zg_control.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_zg_control.run_manifest.json)
3. Ran preflight validation:
   - `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_zg_control.run_manifest.json`
   - Result: PASS
4. Executed governed training:
   - `python scripts/train_lora_sft.py --config configs/lora/stage_b_llama31_8b_base_v1_phase_zg_control.config.json`
   - Result: completed successfully
5. Executed frozen canonical evaluation with the explicit local base-model override:
   - `python scripts/eval_canonical_manifest.py --manifest evals/canonical_eval_manifest_v1.json --model-name-or-path /mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base --adapter-dir artifacts/adapters/stage_b_llama31_8b_base_v1_phase_zg_control --out-dir evals/runs/phase_zg_control_eval_20260613T232145Z`
   - Result: completed successfully
6. Recorded the final evaluation artifacts:
   - [eval summary](/opt/ai-stack/assistant-training/evals/runs/phase_zg_control_eval_20260613T232145Z/summary.json)
   - [comparison rows](/opt/ai-stack/assistant-training/evals/runs/phase_zg_control_eval_20260613T232145Z/comparison_rows.jsonl)
   - [family-a scorer evidence](/opt/ai-stack/assistant-training/evals/runs/phase_zg_control_eval_20260613T232145Z/stage_c_family_a_scorer_evidence_artifact.json)
   - [runtime contract summary](/opt/ai-stack/assistant-training/evals/runs/phase_zg_control_eval_20260613T232145Z/stage_c_runtime_contract_summary_artifact.json)

## Validation Notes

- Dataset resolution was clean.
- The control dataset remained contamination-clean.
- The canonical evaluation contract remained frozen.
- No treatment arm was executed in this phase.

## Recorded Outcome

- Promotion determination: `Do Not Promote`
- Operational status: `success`
- Attribution status: `baseline established; topology conclusion pending`
