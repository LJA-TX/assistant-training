# Phase ZH Treatment A Execution Review

## Executive Summary

The topology-ablation Treatment A arm completed end to end under the frozen Phase L framework using the validated Phase ZF two-cluster dataset.

Training finished, the frozen canonical evaluation contract executed, and the dataset remained contamination-clean. The run is scientifically valid, but it is **Do Not Promote**.

Relative to the ZG control baseline, Treatment A is weaker on exact-call realization and weaker on refusal safety. It does not move the sweep toward the H1/H2 capability floor.

## Promoted Assets

| Asset | Path | Notes |
|---|---|---|
| Promoted config | [configs/lora/stage_b_llama31_8b_base_v1_phase_zh_treatment_a.config.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_zh_treatment_a.config.json) | Approved-to-run topology-treatment A config |
| Promoted manifest | [manifests/runs/stage_b_llama31_8b_base_v1_phase_zh_treatment_a.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_zh_treatment_a.run_manifest.json) | Prepared-not-started run manifest with gate opened |
| Training summary | [artifacts/stage_b_llama31_8b_base_v1_phase_zh_treatment_a/training_summary.json](/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_zh_treatment_a/training_summary.json) | Training and exposure evidence |
| Canonical eval summary | [evals/runs/phase_zh_treatment_a_eval_20260613T234909Z/summary.json](/opt/ai-stack/assistant-training/evals/runs/phase_zh_treatment_a_eval_20260613T234909Z/summary.json) | Frozen evaluator output |
| Canonical comparison rows | [evals/runs/phase_zh_treatment_a_eval_20260613T234909Z/comparison_rows.jsonl](/opt/ai-stack/assistant-training/evals/runs/phase_zh_treatment_a_eval_20260613T234909Z/comparison_rows.jsonl) | Row-level frozen comparison evidence |
| Scorer evidence | [evals/runs/phase_zh_treatment_a_eval_20260613T234909Z/stage_c_family_a_scorer_evidence_artifact.json](/opt/ai-stack/assistant-training/evals/runs/phase_zh_treatment_a_eval_20260613T234909Z/stage_c_family_a_scorer_evidence_artifact.json) | Authoritative family-a evidence artifact |
| Runtime contract summary | [evals/runs/phase_zh_treatment_a_eval_20260613T234909Z/stage_c_runtime_contract_summary_artifact.json](/opt/ai-stack/assistant-training/evals/runs/phase_zh_treatment_a_eval_20260613T234909Z/stage_c_runtime_contract_summary_artifact.json) | Frozen runtime-contract evidence |

## Validation Results

- `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_zh_treatment_a.run_manifest.json`: PASS
- Dataset hash verification against Phase ZF summary hashes: PASS
- Frozen-surface verification via Phase ZF summary: PASS
- Training run: PASS
- Canonical evaluation: PASS
- `git diff --check`: PASS

## Dataset And Training Summary

| Item | Value |
|---|---|
| Topology label | `two_cluster` |
| Topology pattern | `two_clusters_50_plus_50_rg_search_rows` |
| Train rows | `2160` |
| Val rows | `240` |
| Anchor rows | `726` |
| Long-tail rows | `667` |
| Tool-positive rows | `1393` |
| Safety rows | `767` |
| Tool families represented | `26` |

| Item | Value |
|---|---|
| Training status | `completed` |
| Train runtime | `164.8346s` |
| Train loss | `0.7169404824574789` |
| Eval loss | `0.5137714147567749` |
| Train samples / second | `2.621` |
| Train steps / second | `0.164` |
| Sampler path | `geometry_sampling_disabled_default_sampler_path` |
| Exposure drift | Exact match on all dimensions |

## Canonical Evaluation Summary

| Metric | Candidate |
|---|---:|
| exact JSON validity | `0.04` |
| invalid JSON rate | `0.295` |
| tool-name accuracy | `0.15` |
| argument accuracy | `0.10714285714285714` |
| wrapper leakage | `0.0` |
| no-call correctness | `0.6666666666666666` |
| adversarial no-call correctness | `0.0` |

## Delta Versus ZG Control

| Metric | Delta |
|---|---:|
| exact JSON validity | `-0.01` |
| tool-name accuracy | `-0.03571428571428571` |
| argument accuracy | `-0.021428571428571432` |
| wrapper leakage | `0.0` |
| no-call correctness | `-0.033333333333333326` |
| adversarial no-call correctness | `-0.1` |

## Failure Profile

| Failure mode | Candidate count |
|---|---:|
| direct-answer substitution | `50` |
| scalar substitution | `42` |
| malformed partial JSON | `9` |
| near-canonical wrapper or envelope drift | `31` |

## Contamination Confirmation

The Treatment A arm remains contamination-clean.

- The Phase ZF readiness assessment reports zero overlap on heldout validation, tool holdout, no-call, adversarial, and direct-answer splits.
- The training run did not mutate the dataset.
- The canonical evaluation contract remained frozen.

Supporting artifacts:

- [Phase ZF Treatment A readiness assessment](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_zf_treatment_a_readiness_assessment.json)
- [Phase ZF Treatment A leakage report](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_zf_treatment_a_leakage_report.json)

## Readiness / Promotion Determination

**Do Not Promote**

The run is valid evidence for the Treatment A arm, but it does not preserve or improve the ZG control capability floor.

## Scientific Interpretation

Treatment A does not recover H1/H2-level tool-call capability.

Relative to ZG control, the two-cluster topology shifts the failure mix toward direct-answer and scalar substitution, reduces exact-call realization, and drops adversarial no-call correctness to zero. That is a negative signal for this topology level, not evidence of recovery.
