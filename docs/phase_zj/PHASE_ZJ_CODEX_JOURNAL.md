# Phase ZJ Codex Journal

## Work Log

1. Reviewed the frozen Phase ZF Treatment C readiness and summary artifacts.
2. Promoted the ZJ run assets:
   - [stage_b_llama31_8b_base_v1_phase_zj_treatment_c.config.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_zj_treatment_c.config.json)
   - [stage_b_llama31_8b_base_v1_phase_zj_treatment_c.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_zj_treatment_c.run_manifest.json)
3. Ran preflight validation:
   - `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_zj_treatment_c.run_manifest.json`
   - Result: PASS
4. Verified dataset hashes against the Phase ZF summary:
   - train SHA-256: `78d394fe06217a6861b6a8531b90c4eb3325303273a354e372bb5147af59f193`
   - val SHA-256: `0afe69984c099e169ffbccbfa9a7fb010bbfbcd9409eb680dacd386be562e844`
   - Result: PASS
5. Executed governed training:
   - `python scripts/train_lora_sft.py --config configs/lora/stage_b_llama31_8b_base_v1_phase_zj_treatment_c.config.json`
   - Result: completed successfully
6. Executed frozen canonical evaluation:
   - `python scripts/eval_canonical_manifest.py --manifest evals/canonical_eval_manifest_v1.json --model-name-or-path /mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base --adapter-dir artifacts/adapters/stage_b_llama31_8b_base_v1_phase_zj_treatment_c --out-dir evals/runs/phase_zj_treatment_c_eval_20260614T114650Z`
   - Result: completed successfully
7. Recorded the final evaluation artifacts:
   - [summary](/opt/ai-stack/assistant-training/evals/runs/phase_zj_treatment_c_eval_20260614T114650Z/summary.json)
   - [comparison rows](/opt/ai-stack/assistant-training/evals/runs/phase_zj_treatment_c_eval_20260614T114650Z/comparison_rows.jsonl)
   - [family-a scorer evidence](/opt/ai-stack/assistant-training/evals/runs/phase_zj_treatment_c_eval_20260614T114650Z/stage_c_family_a_scorer_evidence_artifact.json)
   - [runtime contract summary](/opt/ai-stack/assistant-training/evals/runs/phase_zj_treatment_c_eval_20260614T114650Z/stage_c_runtime_contract_summary_artifact.json)
8. Updated `docs/current/status/TRAINING_RUN_HISTORY.md` with the completed ZJ canonical-eval row.

## Validation Notes

- Dataset resolution was clean.
- The treatment dataset remained contamination-clean.
- The canonical evaluation contract remained frozen.
- No additional topology arms were executed.

## Recorded Outcome

- Promotion determination: `Do Not Promote`
- Operational status: `success`
- Attribution status: `topology weakened; not a primary explanation for H1/H2 success`
