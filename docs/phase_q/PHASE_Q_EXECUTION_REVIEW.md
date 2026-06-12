# Phase Q Execution Review

## Executive Summary

The governed Dataset v1.2 run completed successfully from an execution standpoint. Training ran to completion, the frozen canonical evaluation contract completed, and contamination remained zero.

The run is **not promotable**. It recovered a small amount of exact JSON behavior relative to Phase L v1.1, but capability remains far below H1/H2 and safety regressed sharply on the no-call surfaces.

## Promoted Assets

| Asset | Path | Notes |
|---|---|---|
| Promoted config | [configs/lora/stage_b_llama31_8b_base_v1_phase_q_v1_2_anchor_weighted_hybrid.config.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_q_v1_2_anchor_weighted_hybrid.config.json) | Approved-to-run v1.2 execution asset |
| Promoted manifest | [manifests/runs/stage_b_llama31_8b_base_v1_phase_q_v1_2_anchor_weighted_hybrid.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_q_v1_2_anchor_weighted_hybrid.run_manifest.json) | Prepared-not-started manifest with approval gate opened |
| Training summary | [artifacts/stage_b_llama31_8b_base_v1_phase_q_v1_2_anchor_weighted_hybrid/training_summary.json](/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_q_v1_2_anchor_weighted_hybrid/training_summary.json) | Training runtime and exposure evidence |
| Canonical eval summary | [evals/runs/phase_q_v1_2_anchor_weighted_hybrid_eval_20260612T101256Z/summary.json](/opt/ai-stack/assistant-training/evals/runs/phase_q_v1_2_anchor_weighted_hybrid_eval_20260612T101256Z/summary.json) | Frozen evaluator output |
| Canonical comparison rows | [evals/runs/phase_q_v1_2_anchor_weighted_hybrid_eval_20260612T101256Z/comparison_rows.jsonl](/opt/ai-stack/assistant-training/evals/runs/phase_q_v1_2_anchor_weighted_hybrid_eval_20260612T101256Z/comparison_rows.jsonl) | Row-level frozen comparison evidence |
| Scorer evidence | [evals/runs/phase_q_v1_2_anchor_weighted_hybrid_eval_20260612T101256Z/stage_c_family_a_scorer_evidence_artifact.json](/opt/ai-stack/assistant-training/evals/runs/phase_q_v1_2_anchor_weighted_hybrid_eval_20260612T101256Z/stage_c_family_a_scorer_evidence_artifact.json) | Family-A scorer evidence artifact |
| Runtime contract summary | [evals/runs/phase_q_v1_2_anchor_weighted_hybrid_eval_20260612T101256Z/stage_c_runtime_contract_summary_artifact.json](/opt/ai-stack/assistant-training/evals/runs/phase_q_v1_2_anchor_weighted_hybrid_eval_20260612T101256Z/stage_c_runtime_contract_summary_artifact.json) | Frozen runtime-contract evidence |

## Validation Results

- `git diff --check`: PASS
- `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_q_v1_2_anchor_weighted_hybrid.run_manifest.json`: PASS

## Training Summary

| Item | Value |
|---|---|
| Base model | `/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base` |
| Dataset | `data/v1_2/dataset_v1_2_train.jsonl` and `data/v1_2/dataset_v1_2_val.jsonl` |
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
| Train runtime | `161.7761s` |
| Train loss | `0.7323995166354709` |
| Eval loss | `0.43417230248451233` |
| Train samples / second | `2.67` |
| Train steps / second | `0.167` |
| Sampler path | `geometry_sampling_disabled_default_sampler_path` |
| Exposure drift | Exact match on all dimensions |
| Row identity digest | `15ef009449d5afff81745c2e458e1cf3540358854bffa802c677087195a229a4` |

## Canonical Evaluation Summary

The canonical evaluator ran against the frozen manifest. The evaluator needed an explicit local mirror override for the base model path:

```text
--model-name-or-path /mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base
```

That override resolved the same frozen base model without changing the evaluator or the manifest.

### Aggregate Adapter Metrics

| Metric | Candidate |
|---|---:|
| exact JSON validity | `0.03` |
| invalid JSON rate | `0.2` |
| tool-name accuracy | `0.07142857142857142` |
| argument accuracy | `0.04285714285714286` |
| wrapper leakage | `0.0` |
| no-call correctness | `0.7666666666666667` |
| adversarial no-call correctness | `0.3` |

### Diagnostic Metrics

| Metric | Candidate |
|---|---:|
| heldout-validation exact-valid | `0.06` |
| tool-holdout exact-valid | `0.0` |
| read-file exact-valid | `0.0` |
| read-file symbol-name exact-valid | `0.0` |
| no-anchor exact-valid share | `0.0` |

### Failure Profile

| Failure mode | Candidate count |
|---|---:|
| direct-answer substitution | `37` |
| scalar substitution | `0` |
| malformed partial JSON | `3` |
| near-canonical wrapper or envelope drift | `94` |

## Contamination Status

Contamination remained zero throughout the slice.

- `data/v1_2/dataset_v1_2_leakage_report.json` reports zero overlap for heldout validation, tool holdout, no-call, adversarial, and direct-answer splits.
- The training run did not mutate the dataset.
- The canonical evaluation used the frozen contract only.

## Runtime Feasibility

The existing Phase L framework remained operationally valid for Dataset v1.2.

The only runtime adjustment required was the explicit local base-model mirror override for canonical evaluation, because `evals/canonical_eval_manifest_v1.json` stores the tokenizer path as `llama-3.1-8b-base` rather than a local filesystem path in this workspace.

No trainer geometry, LoRA topology, optimizer settings, evaluator logic, scoring logic, governance, or thresholds were changed.
