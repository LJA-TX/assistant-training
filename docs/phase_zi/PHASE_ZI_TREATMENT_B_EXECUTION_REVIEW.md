# Phase ZI Treatment B Execution Review

## Executive Summary

The topology-ablation Treatment B arm completed end to end under the frozen Phase L framework using the validated Phase ZF four-cluster dataset.

Training finished, the frozen canonical evaluation contract executed, and the dataset remained contamination-clean. The run is scientifically valid, but it is **Do Not Promote**.

Relative to the ZG control and ZH Treatment A baselines, Treatment B is weaker on exact-call realization and weaker on adversarial/no-call safety. It does not move the sweep toward the H1/H2 capability floor.

## Promoted Assets

| Asset | Path | Notes |
|---|---|---|
| Promoted config | [configs/lora/stage_b_llama31_8b_base_v1_phase_zi_treatment_b.config.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_zi_treatment_b.config.json) | Approved-to-run topology-treatment B config |
| Promoted manifest | [manifests/runs/stage_b_llama31_8b_base_v1_phase_zi_treatment_b.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_zi_treatment_b.run_manifest.json) | Prepared-not-started run manifest with gate opened |
| Training summary | [artifacts/stage_b_llama31_8b_base_v1_phase_zi_treatment_b/training_summary.json](/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_zi_treatment_b/training_summary.json) | Training and exposure evidence |
| Canonical eval summary | [evals/runs/phase_zi_treatment_b_eval_20260614T111746Z/summary.json](/opt/ai-stack/assistant-training/evals/runs/phase_zi_treatment_b_eval_20260614T111746Z/summary.json) | Frozen evaluator output |
| Canonical comparison rows | [evals/runs/phase_zi_treatment_b_eval_20260614T111746Z/comparison_rows.jsonl](/opt/ai-stack/assistant-training/evals/runs/phase_zi_treatment_b_eval_20260614T111746Z/comparison_rows.jsonl) | Row-level frozen comparison evidence |
| Scorer evidence | [evals/runs/phase_zi_treatment_b_eval_20260614T111746Z/stage_c_family_a_scorer_evidence_artifact.json](/opt/ai-stack/assistant-training/evals/runs/phase_zi_treatment_b_eval_20260614T111746Z/stage_c_family_a_scorer_evidence_artifact.json) | Authoritative family-a evidence artifact |
| Runtime contract summary | [evals/runs/phase_zi_treatment_b_eval_20260614T111746Z/stage_c_runtime_contract_summary_artifact.json](/opt/ai-stack/assistant-training/evals/runs/phase_zi_treatment_b_eval_20260614T111746Z/stage_c_runtime_contract_summary_artifact.json) | Frozen runtime-contract evidence |

## Validation Results

- `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_zi_treatment_b.run_manifest.json`: PASS
- Dataset hash verification against Phase ZF summary hashes: PASS
- Frozen-surface verification via Phase ZF summary: PASS
- Training run: PASS
- Canonical evaluation: PASS
- `git diff --check`: PASS

## Dataset And Training Summary

| Item | Value |
|---|---|
| Topology label | `four_cluster` |
| Topology pattern | `four_clusters_25_plus_25_plus_25_plus_25_rg_search_rows` |
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
| Train runtime | `164.9310s` |
| Train loss | `0.7171172212671351` |
| Eval loss | `0.4962088167667389` |
| Train samples / second | `2.619` |
| Train steps / second | `0.164` |
| Sampler path | `geometry_sampling_disabled_default_sampler_path` |
| Exposure drift | Exact match on all dimensions |

## Canonical Evaluation Summary

| Metric | Candidate |
|---|---:|
| exact JSON validity | `0.04` |
| invalid JSON rate | `0.33` |
| tool-name accuracy | `0.12142857142857143` |
| argument accuracy | `0.09285714285714286` |
| wrapper leakage | `0.0` |
| no-call correctness | `0.6666666666666666` |
| adversarial no-call correctness | `0.0` |

## Delta Versus ZG Control

| Metric | Delta |
|---|---:|
| exact JSON validity | `-0.01` |
| tool-name accuracy | `-0.06428571428571428` |
| argument accuracy | `-0.0357142857142857` |
| wrapper leakage | `0.0` |
| no-call correctness | `-0.033333333333333326` |
| adversarial no-call correctness | `-0.1` |

## Delta Versus ZH Treatment A

| Metric | Delta |
|---|---:|
| exact JSON validity | `0.0` |
| tool-name accuracy | `-0.02857142857142858` |
| argument accuracy | `-0.01428571428571429` |
| wrapper leakage | `0.0` |
| no-call correctness | `0.0` |
| adversarial no-call correctness | `0.0` |

## Failure Profile

| Failure mode | Candidate count |
|---|---:|
| direct-answer substitution | `53` |
| scalar substitution | `48` |
| malformed partial JSON | `2` |
| near-canonical wrapper or envelope drift | `29` |

## Contamination Confirmation

The Treatment B arm remains contamination-clean.

- The Phase ZF readiness assessment reports zero overlap on heldout validation, tool holdout, no-call, adversarial, and direct-answer splits.
- The training run did not mutate the dataset.
- The canonical evaluation contract remained frozen.

Supporting artifacts:

- [Phase ZF Treatment B readiness assessment](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_zf_treatment_b_readiness_assessment.json)
- [Phase ZF Treatment B leakage report](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_zf_treatment_b_leakage_report.json)

## Readiness / Promotion Determination

**Do Not Promote**

The run is valid evidence for the Treatment B arm, but it does not preserve or improve the ZG control capability floor.

## Scientific Interpretation

Treatment B does not recover H1/H2-level tool-call capability.

Relative to ZG control, the four-cluster topology lowers exact-call realization and tool-selection accuracy while also worsening the adversarial no-call surface. Relative to ZH Treatment A, it is mostly flat on exact JSON and no-call behavior, but it remains below Treatment A on tool selection and argument realization. That is a negative or flat signal for this topology level, not evidence of recovery.
