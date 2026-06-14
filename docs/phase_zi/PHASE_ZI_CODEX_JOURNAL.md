# Phase ZI Codex Journal

## Work Log

1. Reviewed the governing context for the topology sweep, including the validated Phase ZF Treatment B artifacts, the Phase ZG control run, and the Phase ZH Treatment A datapoint.
2. Promoted the Treatment B execution assets:
   - [configs/lora/stage_b_llama31_8b_base_v1_phase_zi_treatment_b.config.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_zi_treatment_b.config.json)
   - [manifests/runs/stage_b_llama31_8b_base_v1_phase_zi_treatment_b.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_zi_treatment_b.run_manifest.json)
3. Ran preflight validation:
   - `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_zi_treatment_b.run_manifest.json`
   - Result: PASS
4. Verified dataset hashes against the Phase ZF summary:
   - train SHA-256: `36c62e5ed8de6ba9e6a46029df34ae1c926b2802ff9535e5360ae9a9764754bd`
   - val SHA-256: `0afe69984c099e169ffbccbfa9a7fb010bbfbcd9409eb680dacd386be562e844`
   - Result: PASS
5. Executed governed training:
   - `python scripts/train_lora_sft.py --config configs/lora/stage_b_llama31_8b_base_v1_phase_zi_treatment_b.config.json`
   - Result: completed successfully
6. Executed frozen canonical evaluation with the explicit local base-model override:
   - `python scripts/eval_canonical_manifest.py --manifest evals/canonical_eval_manifest_v1.json --model-name-or-path /mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base --adapter-dir artifacts/adapters/stage_b_llama31_8b_base_v1_phase_zi_treatment_b --out-dir evals/runs/phase_zi_treatment_b_eval_20260614T111746Z`
   - Result: completed successfully
7. Recorded the final evaluation artifacts:
   - [eval summary](/opt/ai-stack/assistant-training/evals/runs/phase_zi_treatment_b_eval_20260614T111746Z/summary.json)
   - [comparison rows](/opt/ai-stack/assistant-training/evals/runs/phase_zi_treatment_b_eval_20260614T111746Z/comparison_rows.jsonl)
   - [family-a scorer evidence](/opt/ai-stack/assistant-training/evals/runs/phase_zi_treatment_b_eval_20260614T111746Z/stage_c_family_a_scorer_evidence_artifact.json)
   - [runtime contract summary](/opt/ai-stack/assistant-training/evals/runs/phase_zi_treatment_b_eval_20260614T111746Z/stage_c_runtime_contract_summary_artifact.json)

## Validation Notes

- Dataset resolution was clean.
- The treatment dataset remained contamination-clean.
- The canonical evaluation contract remained frozen.
- No other topology arm was executed in this phase.

## Recorded Outcome

- Promotion determination: `Do Not Promote`
- Operational status: `success`
- Attribution status: `negative relative to ZG; flat-to-negative relative to ZH; sweep continues`
