# Phase L Execution Review

## Executive Summary

The authorized Dataset v1.1 run completed end to end with the promoted config and run manifest, and the canonical evaluation contract executed successfully under the frozen manifest.

The run is **clean but not promotable**.

Promotion determination: **Do Not Promote**

The decisive reasons are:

1. The candidate misses every tool-call capability threshold by a wide margin.
2. Aggregate invalid JSON is `0.345`, which exceeds the Phase L hard-fail limit of `0.30`.
3. Direct-answer and scalar-substitution failure modes are worse than the H2 baseline.
4. The run preserves safety on no-call and adversarial no-call, but that is not enough to offset the capability failure.

## Promoted Execution Assets

| Asset | Path | Notes |
|---|---|---|
| Promoted config | [configs/lora/stage_b_llama31_8b_base_v1_phase_l_v1_1_external_first.config.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_l_v1_1_external_first.config.json) | Approved-to-run promoted asset |
| Promoted manifest | [manifests/runs/stage_b_llama31_8b_base_v1_phase_l_v1_1_external_first.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_l_v1_1_external_first.run_manifest.json) | Prepared-not-started run manifest with approval gate opened |
| Training summary | [artifacts/stage_b_llama31_8b_base_v1_phase_l_v1_1_external_first/training_summary.json](/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_l_v1_1_external_first/training_summary.json) | Training and exposure evidence |
| Canonical eval summary | [evals/runs/phase_l_v1_1_external_first_eval_20260611T153900Z/summary.json](/opt/ai-stack/assistant-training/evals/runs/phase_l_v1_1_external_first_eval_20260611T153900Z/summary.json) | Frozen evaluator output |
| Canonical comparison rows | [evals/runs/phase_l_v1_1_external_first_eval_20260611T153900Z/comparison_rows.jsonl](/opt/ai-stack/assistant-training/evals/runs/phase_l_v1_1_external_first_eval_20260611T153900Z/comparison_rows.jsonl) | Row-level frozen comparison evidence |
| Scorer evidence | [evals/runs/phase_l_v1_1_external_first_eval_20260611T153900Z/stage_c_family_a_scorer_evidence_artifact.json](/opt/ai-stack/assistant-training/evals/runs/phase_l_v1_1_external_first_eval_20260611T153900Z/stage_c_family_a_scorer_evidence_artifact.json) | Authoritative family-a evidence artifact |
| Runtime contract summary | [evals/runs/phase_l_v1_1_external_first_eval_20260611T153900Z/stage_c_runtime_contract_summary_artifact.json](/opt/ai-stack/assistant-training/evals/runs/phase_l_v1_1_external_first_eval_20260611T153900Z/stage_c_runtime_contract_summary_artifact.json) | Guardrail and contract summary |

## Training Summary

### Configuration

| Item | Value |
|---|---|
| Base model | `/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base` |
| Dataset | `data/v1_1/dataset_v1_1_train.jsonl` and `data/v1_1/dataset_v1_1_val.jsonl` |
| Format | `openai_messages_with_assistant_tool_calls` |
| Sequence length | `2048` |
| LoRA | `r=16`, `alpha=32`, `dropout=0.05`, target modules `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj` |
| Quantization | 4-bit NF4, double quant, bfloat16 compute |
| Optimization | `0.2` epochs, `1e-4` LR, cosine schedule, `gradient_accumulation_steps=16` |
| Loss policy | Assistant-only, fail-fast |
| Prompt template | `tokenizer_chat_template` with `generic_roles_v1` fallback |

### Run Outcome

| Item | Value |
|---|---|
| Training status | `completed` |
| Train rows | `2160` |
| Val rows | `240` |
| Train runtime | `159.0615s` |
| Train loss | `0.874854326248169` |
| Eval loss | `0.5422032475471497` |
| Train samples / second | `2.716` |
| Train steps / second | `0.17` |
| Sampler path | `geometry_sampling_disabled_default_sampler_path` |
| Exposure drift | Exact match on all dimensions |
| Row identity digest | `895590ed7cd396665b8054152254305194b4f7d56e320bd75441cfb5429e1603` |

The training artifact set was written under `artifacts/stage_b_llama31_8b_base_v1_phase_l_v1_1_external_first/` and `artifacts/adapters/stage_b_llama31_8b_base_v1_phase_l_v1_1_external_first/`.

## Evaluation Summary

The canonical evaluator ran against the frozen manifest:

- manifest: [evals/canonical_eval_manifest_v1.json](/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json)
- decode defaults: temperature `0.0`, top_p `1.0`, do_sample `false`, repetition_penalty `1.0`, max_new_tokens `64`, seed `1234`

### Aggregate Adapter Metrics

| Metric | Candidate |
|---|---:|
| exact JSON validity | `0.0` |
| invalid JSON rate | `0.345` |
| tool-name accuracy | `0.04285714285714286` |
| argument accuracy | `0.007142857142857143` |
| wrapper leakage | `0.0` |
| no-call correctness | `1.0` |
| adversarial no-call correctness | `1.0` |

### Per-Split Metrics

| Split | Candidate value | Notes |
|---|---:|---|
| heldout validation exact-valid | `0.0` | Capability failure on the main heldout slice |
| tool holdout exact-valid | `0.0` | No recovery on the tool-specific holdout |
| no-call correctness | `1.0` | Safety invariant preserved |
| adversarial no-call correctness | `1.0` | Safety invariant preserved |
| no-anchor exact-valid share | `0.0` | No recovery on the anchor-free diagnostic slice |

### Failure Profile

| Failure mode | Candidate count |
|---|---:|
| direct-answer substitution | `55` |
| scalar substitution | `1` |
| malformed partial JSON | `14` |
| near-canonical wrapper or envelope drift | `70` |
| other | `0` |

The candidate improves wrapper drift relative to the earlier commitment-heavy probe, but it regresses direct-answer substitution materially and leaves the overall JSON-forming capability near zero.

## Baseline Comparison

| Metric | Candidate | H0 | H1 | H2 | Interpretation |
|---|---:|---:|---:|---:|---|
| exact JSON validity | `0.0` | `0.045` | `0.44` | `0.48` | Below every baseline |
| tool-holdout exact-valid | `0.0` | `0.0` | `0.6` | `0.525` | No lift over the control; far below H1/H2 |
| heldout-validation exact-valid | `0.0` | `0.09` | `0.64` | `0.75` | Below every baseline |
| tool-name accuracy | `0.04285714285714286` | `0.07142857142857142` | `0.7142857142857143` | `0.7714285714285715` | Below every baseline |
| argument accuracy | `0.007142857142857143` | `0.06428571428571428` | `0.6285714285714286` | `0.6928571428571428` | Below every baseline |
| no-anchor exact-valid | `0.0` | `0.0` | `0.8636363636363636` | `0.84375` | No improvement over control; far below H1/H2 |
| wrapper leakage | `0.0` | `0.0` | `0.0` | `0.005` | Safety remains clean |
| no-call correctness | `1.0` | `0.9166666666666666` | `0.9` | `0.8` | Better than all baselines |
| adversarial no-call correctness | `1.0` | `0.75` | `0.7` | `0.4` | Better than all baselines |

### H2 Failure-Mode Comparison

H2 reported `direct-answer_substitution = 9` and `scalar_substitution = 0` on the non-exact tool rows.

This candidate reports `direct-answer_substitution = 55` and `scalar_substitution = 1`.

That is a clear regression versus H2 on the exact failure modes Phase L required to avoid worsening.

## Contamination Confirmation

The dataset candidate remains contamination-clean and the execution phase did not mutate the dataset.

Evidence:

- Phase K contamination validation passed on `heldout_validation`, `tool_holdout`, `no_call`, `adversarial`, and `direct_answer`.
- The dataset summary still reports zero overlap on all frozen canonical eval splits.
- The Phase L run used the promoted config and manifest only; it did not rebuild the dataset.

Supporting artifacts:

- [Dataset leakage report](/opt/ai-stack/assistant-training/data/v1_1/dataset_v1_1_leakage_report.json)
- [Dataset readiness assessment](/opt/ai-stack/assistant-training/data/v1_1/dataset_v1_1_readiness_assessment.json)
- [Phase K contamination report](/opt/ai-stack/assistant-training/docs/phase_k/CONTAMINATION_VALIDATION_REPORT.md)

## Stop-Rule Review

### Passed

1. The promoted config and manifest resolved.
2. The model and tokenizer mirrors resolved.
3. The train and val JSONL paths resolved.
4. Loss policy remained fail-fast.
5. The adapter output directory did not pre-exist.
6. Training completed without NaN, infinite loss, hidden retry, or auto-chain behavior.
7. Canonical evaluation used the frozen manifest and frozen decode defaults.
8. Wrapper leakage remained `0.0`.
9. No-call and adversarial no-call correctness remained `1.0`.

### Failed

1. Aggregate invalid JSON is `0.345`, which exceeds the `0.30` hard-fail limit.
2. Exact JSON validity is `0.0`, far below the `0.48` success threshold.
3. Tool-holdout exact-valid is `0.0`, below the `0.60` threshold.
4. Heldout-validation exact-valid is `0.0`, below the `0.75` threshold.
5. Tool-name accuracy is `0.04285714285714286`, below the `0.7714285714285715` threshold.
6. Argument accuracy is `0.007142857142857143`, below the `0.6928571428571428` threshold.
7. No-anchor exact-valid is `0.0`, below the `0.8636363636363636` threshold.
8. Direct-answer and scalar-substitution behavior worsened versus H2.

## Promotion Determination

**Do Not Promote**

This is not an ambiguous case. The run is safety-clean, but it does not preserve the H1/H2 capability gains and it fails the Phase L hard-fail quality gate on aggregate invalid JSON.

## Scientific Interpretation

The run does not support a combined-bottleneck closure.

What it shows is narrower:

- the external-first safety calibration successfully preserved refusal behavior on the no-call surfaces;
- the candidate still cannot reliably produce exact JSON tool-call structure;
- the commitment-side gains seen in H2 are not retained in a usable form;
- the diversity/commitment hybrid, as instantiated here, does not yet resolve the bottleneck.

The evidence therefore supports another design iteration, not promotion.

## References

- [Phase L execution package](/opt/ai-stack/assistant-training/docs/phase_l/PHASE_L_EXECUTION_PACKAGE.md)
- [Phase L readiness assessment](/opt/ai-stack/assistant-training/docs/phase_l/PHASE_L_READINESS_ASSESSMENT.md)
- [Phase L completion report](/opt/ai-stack/assistant-training/docs/phase_l/PHASE_L_COMPLETION_REPORT.md)
