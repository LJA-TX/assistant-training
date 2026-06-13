# Phase ZA Treatment A Execution Review

## Executive Summary

The governed Phase Y Treatment A arm completed end to end under the frozen Phase Z framework.

Training finished, the frozen canonical evaluation contract executed, and the Treatment A candidate remains contamination-clean. The run is scientifically valid as an ablation result, but it is **not promotable**.

Treatment A shows measurable movement away from the Control baseline on the main capability metrics and on no-call correctness. The response is positive, but modest, and still far below the H1/H2 capability floor.

## Promoted Assets

| Asset | Path | Notes |
|---|---|---|
| Promoted config | [configs/lora/stage_b_llama31_8b_base_v1_phase_za_treatment_a.config.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_za_treatment_a.config.json) | Approved-to-run Treatment A config |
| Promoted manifest | [manifests/runs/stage_b_llama31_8b_base_v1_phase_za_treatment_a.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_za_treatment_a.run_manifest.json) | Prepared-not-started run manifest with gate opened |
| Training summary | [artifacts/stage_b_llama31_8b_base_v1_phase_za_treatment_a/training_summary.json](/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_za_treatment_a/training_summary.json) | Training and exposure evidence |
| Canonical eval summary | [evals/runs/phase_za_treatment_a_eval_20260613T005031Z/summary.json](/opt/ai-stack/assistant-training/evals/runs/phase_za_treatment_a_eval_20260613T005031Z/summary.json) | Frozen evaluator output |
| Canonical comparison rows | [evals/runs/phase_za_treatment_a_eval_20260613T005031Z/comparison_rows.jsonl](/opt/ai-stack/assistant-training/evals/runs/phase_za_treatment_a_eval_20260613T005031Z/comparison_rows.jsonl) | Row-level frozen comparison evidence |
| Scorer evidence | [evals/runs/phase_za_treatment_a_eval_20260613T005031Z/stage_c_family_a_scorer_evidence_artifact.json](/opt/ai-stack/assistant-training/evals/runs/phase_za_treatment_a_eval_20260613T005031Z/stage_c_family_a_scorer_evidence_artifact.json) | Authoritative family-a evidence artifact |
| Runtime contract summary | [evals/runs/phase_za_treatment_a_eval_20260613T005031Z/stage_c_runtime_contract_summary_artifact.json](/opt/ai-stack/assistant-training/evals/runs/phase_za_treatment_a_eval_20260613T005031Z/stage_c_runtime_contract_summary_artifact.json) | Guardrail and contract summary |

## Validation Results

- `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_za_treatment_a.run_manifest.json`: PASS
- `git diff --check`: PASS
- Training run: PASS
- Canonical evaluation: PASS

## Training Summary

| Item | Value |
|---|---|
| Base model | `/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base` |
| Dataset | `data/v1_2/dataset_v1_2_phase_y_treatment_a_train.jsonl` and `data/v1_2/dataset_v1_2_phase_y_treatment_a_val.jsonl` |
| Format | `openai_messages_with_assistant_tool_calls` |
| Sequence length | `2048` |
| LoRA | `r=16`, `alpha=32`, `dropout=0.05`, target modules `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj` |
| Quantization | 4-bit NF4, double quant, bfloat16 compute |
| Optimization | `0.2` epochs, `1e-4` LR, cosine schedule, `gradient_accumulation_steps=16` |
| Loss policy | Assistant-only, fail-fast |
| Prompt template | `tokenizer_chat_template` with `generic_roles_v1` fallback |

| Item | Value |
|---|---|
| Training status | `completed` |
| Train rows | `2160` |
| Val rows | `240` |
| Train runtime | `165.8693s` |
| Train loss | `0.6619200176662869` |
| Eval loss | `0.5236577987670898` |
| Train samples / second | `2.604` |
| Train steps / second | `0.163` |
| Sampler path | `geometry_sampling_disabled_default_sampler_path` |
| Exposure drift | Exact match on all dimensions |

## Canonical Evaluation Summary

The canonical evaluator ran against the frozen manifest with the explicit local mirror override required by this workspace:

```text
--model-name-or-path /mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base
```

### Aggregate Adapter Metrics

| Metric | Candidate |
|---|---:|
| exact JSON validity | `0.07` |
| invalid JSON rate | `0.185` |
| tool-name accuracy | `0.21428571428571427` |
| argument accuracy | `0.15` |
| wrapper leakage | `0.005` |
| no-call correctness | `0.7333333333333333` |
| adversarial no-call correctness | `0.25` |

### Failure Profile

| Failure mode | Candidate count |
|---|---:|
| direct-answer substitution | `34` |
| scalar substitution | `39` |
| malformed partial JSON | `4` |
| near-canonical wrapper or envelope drift | `49` |
| other | `0` |

## Contamination Confirmation

The Treatment A arm remains contamination-clean.

- The Phase Y Treatment A readiness assessment reports zero overlap on heldout validation, tool holdout, no-call, adversarial, and direct-answer splits.
- The training run did not mutate the dataset.
- The canonical evaluation contract remained frozen.

Supporting artifacts:

- [Phase Y Treatment A readiness assessment](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_y_treatment_a_readiness_assessment.json)
- [Phase Y Treatment A leakage report](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_y_treatment_a_leakage_report.json)

## Readiness / Promotion Determination

**Do Not Promote**

Treatment A is a valid ablation result, but it does not preserve the H1/H2 capability floor and it still loses adversarial no-call safety relative to the ideal invariant.

## Scientific Interpretation

Treatment A indicates a positive anchor-concentration response relative to the Control arm:

- exact JSON validity improved;
- tool-name accuracy improved;
- argument accuracy improved;
- no-call correctness improved;
- adversarial no-call correctness improved from zero to `0.25`.

The response is real but small. It is not enough to claim the ablation is answered, and it does not justify a promotion.
