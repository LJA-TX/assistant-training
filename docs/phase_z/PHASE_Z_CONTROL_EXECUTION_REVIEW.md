# Phase Z Control Execution Review

## Executive Summary

The governed Phase Y control arm completed end to end under the frozen Phase L framework.

Training finished, the frozen canonical evaluation contract executed, and the control candidate remains contamination-clean. The run is scientifically valid as an ablation result, but it is **not promotable**.

The main outcome is mixed:

- capability improved relative to Phase Q on exact JSON, tool-name accuracy, and argument accuracy;
- safety regressed relative to Phase Q and Phase U on adversarial no-call;
- the result remains far below the H1/H2 capability floor.

## Promoted Assets

| Asset | Path | Notes |
|---|---|---|
| Promoted config | [configs/lora/stage_b_llama31_8b_base_v1_phase_z_control.config.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_z_control.config.json) | Approved-to-run control-arm config |
| Promoted manifest | [manifests/runs/stage_b_llama31_8b_base_v1_phase_z_control.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_z_control.run_manifest.json) | Prepared-not-started run manifest with gate opened |
| Training summary | [artifacts/stage_b_llama31_8b_base_v1_phase_z_control/training_summary.json](/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_z_control/training_summary.json) | Training and exposure evidence |
| Canonical eval summary | [evals/runs/phase_z_control_eval_20260613T002335Z/summary.json](/opt/ai-stack/assistant-training/evals/runs/phase_z_control_eval_20260613T002335Z/summary.json) | Frozen evaluator output |
| Canonical comparison rows | [evals/runs/phase_z_control_eval_20260613T002335Z/comparison_rows.jsonl](/opt/ai-stack/assistant-training/evals/runs/phase_z_control_eval_20260613T002335Z/comparison_rows.jsonl) | Row-level frozen comparison evidence |
| Scorer evidence | [evals/runs/phase_z_control_eval_20260613T002335Z/stage_c_family_a_scorer_evidence_artifact.json](/opt/ai-stack/assistant-training/evals/runs/phase_z_control_eval_20260613T002335Z/stage_c_family_a_scorer_evidence_artifact.json) | Authoritative family-a evidence artifact |
| Runtime contract summary | [evals/runs/phase_z_control_eval_20260613T002335Z/stage_c_runtime_contract_summary_artifact.json](/opt/ai-stack/assistant-training/evals/runs/phase_z_control_eval_20260613T002335Z/stage_c_runtime_contract_summary_artifact.json) | Guardrail and contract summary |

## Validation Results

- `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_z_control.run_manifest.json`: PASS
- `git diff --check`: PASS
- Training run: PASS
- Canonical evaluation: PASS

## Training Summary

| Item | Value |
|---|---|
| Base model | `/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base` |
| Dataset | `data/v1_2/dataset_v1_2_phase_y_control_train.jsonl` and `data/v1_2/dataset_v1_2_phase_y_control_val.jsonl` |
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
| Train runtime | `165.6615s` |
| Train loss | `0.7193721665276421` |
| Eval loss | `0.5284086465835571` |
| Train samples / second | `2.608` |
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
| exact JSON validity | `0.055` |
| invalid JSON rate | `0.2` |
| tool-name accuracy | `0.2` |
| argument accuracy | `0.1357142857142857` |
| wrapper leakage | `0.0` |
| no-call correctness | `0.6666666666666666` |
| adversarial no-call correctness | `0.0` |

### Failure Profile

| Failure mode | Candidate count |
|---|---:|
| direct-answer substitution | `38` |
| scalar substitution | `38` |
| malformed partial JSON | `3` |
| near-canonical wrapper or envelope drift | `50` |
| other | `0` |

## Contamination Confirmation

The control arm remains contamination-clean.

- The Phase Y control readiness assessment reports zero overlap on heldout validation, tool holdout, no-call, adversarial, and direct-answer splits.
- The training run did not mutate the dataset.
- The canonical evaluation contract remained frozen.

Supporting artifacts:

- [Phase Y control readiness assessment](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_y_control_readiness_assessment.json)
- [Phase Y control leakage report](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_y_control_leakage_report.json)

## Readiness / Promotion Determination

**Do Not Promote**

The run is valid evidence for the control arm, but it does not preserve the H1/H2 capability floor and it regresses adversarial no-call safety to `0.0`.

## Scientific Interpretation

The control arm indicates that the Phase Y scaffold can recover some exact tool-call structure relative to Phase Q, but the recovered signal is still too weak and too unstable to close the capability gap.

This is a valid ablation result, not a setup failure.
