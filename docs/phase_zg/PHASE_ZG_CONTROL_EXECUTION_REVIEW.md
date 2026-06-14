# Phase ZG Control Execution Review

## Executive Summary

The topology-ablation Control arm completed end to end under the frozen Phase L framework using the validated Phase ZF compact-local dataset.

Training finished, the frozen canonical evaluation contract executed, and the dataset remained contamination-clean. The run is scientifically valid as a baseline point for the topology sweep, but it is **Do Not Promote**.

Relative to the earlier Z-series control arm, the ZG control is slightly weaker on exact-call realization and slightly stronger on the no-call surfaces. Relative to H1/H2, it remains far below the capability floor.

## Promoted Assets

| Asset | Path | Notes |
|---|---|---|
| Promoted config | [configs/lora/stage_b_llama31_8b_base_v1_phase_zg_control.config.json](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_zg_control.config.json) | Approved-to-run topology-control config |
| Promoted manifest | [manifests/runs/stage_b_llama31_8b_base_v1_phase_zg_control.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_zg_control.run_manifest.json) | Prepared-not-started run manifest with gate opened |
| Training summary | [artifacts/stage_b_llama31_8b_base_v1_phase_zg_control/training_summary.json](/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_zg_control/training_summary.json) | Training and exposure evidence |
| Canonical eval summary | [evals/runs/phase_zg_control_eval_20260613T232145Z/summary.json](/opt/ai-stack/assistant-training/evals/runs/phase_zg_control_eval_20260613T232145Z/summary.json) | Frozen evaluator output |
| Canonical comparison rows | [evals/runs/phase_zg_control_eval_20260613T232145Z/comparison_rows.jsonl](/opt/ai-stack/assistant-training/evals/runs/phase_zg_control_eval_20260613T232145Z/comparison_rows.jsonl) | Row-level frozen comparison evidence |
| Scorer evidence | [evals/runs/phase_zg_control_eval_20260613T232145Z/stage_c_family_a_scorer_evidence_artifact.json](/opt/ai-stack/assistant-training/evals/runs/phase_zg_control_eval_20260613T232145Z/stage_c_family_a_scorer_evidence_artifact.json) | Authoritative family-a evidence artifact |
| Runtime contract summary | [evals/runs/phase_zg_control_eval_20260613T232145Z/stage_c_runtime_contract_summary_artifact.json](/opt/ai-stack/assistant-training/evals/runs/phase_zg_control_eval_20260613T232145Z/stage_c_runtime_contract_summary_artifact.json) | Frozen runtime-contract evidence |

## Validation Results

- `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_zg_control.run_manifest.json`: PASS
- `git diff --check`: PASS
- Training run: PASS
- Canonical evaluation: PASS

## Dataset And Training Summary

| Item | Value |
|---|---|
| Topology label | `compact_local` |
| Topology pattern | `minimal_span_window_of_100_rg_search_rows` |
| Train rows | `2160` |
| Val rows | `240` |
| Anchor rows | `726` |
| Long-tail rows | `667` |
| Tool-positive rows | `1393` |
| Safety rows | `767` |
| Tool families represented | `26` |
| Patch rows | `100` |
| Patch family mix | `20 rg_search`, `20 read_file`, `20 find_files`, `20 debug_tools`, `20 run_command` |

| Item | Value |
|---|---|
| Training status | `completed` |
| Train runtime | `164.7839s` |
| Train loss | `0.7300845958568432` |
| Eval loss | `0.5198308825492859` |
| Train samples / second | `2.622` |
| Train steps / second | `0.164` |
| Sampler path | `geometry_sampling_disabled_default_sampler_path` |
| Exposure drift | Exact match on all dimensions |

## Canonical Evaluation Summary

| Metric | Candidate |
|---|---:|
| exact JSON validity | `0.05` |
| invalid JSON rate | `0.195` |
| tool-name accuracy | `0.18571428571428572` |
| argument accuracy | `0.12857142857142856` |
| wrapper leakage | `0.0` |
| no-call correctness | `0.7` |
| adversarial no-call correctness | `0.1` |

## Failure Profile

| Failure mode | Candidate count |
|---|---:|
| direct-answer substitution | `37` |
| scalar substitution | `36` |
| malformed partial JSON | `4` |
| near-canonical wrapper or envelope drift | `53` |

## Contamination Confirmation

The control arm remains contamination-clean.

- The Phase ZF readiness assessment reports zero overlap on heldout validation, tool holdout, no-call, adversarial, and direct-answer splits.
- The training run did not mutate the dataset.
- The canonical evaluation contract remained frozen.

Supporting artifacts:

- [Phase ZF control readiness assessment](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_zf_control_readiness_assessment.json)
- [Phase ZF control leakage report](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_zf_control_leakage_report.json)

## Readiness / Promotion Determination

**Do Not Promote**

The run is valid baseline evidence for the topology sweep, but it does not recover H1/H2-level tool-call capability and does not establish a promotable endpoint.

## Scientific Interpretation

The compact-local control confirms that the Phase ZF sweep can be executed under the frozen Phase L framework.

Relative to the earlier Z-series control arm, this control is slightly worse on exact-call realization and slightly better on refusal/no-call behavior. Relative to H1/H2, it remains far below the capability floor. The result is therefore a valid baseline, not a topology conclusion.
