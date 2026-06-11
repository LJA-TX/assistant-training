# Contamination Validation Report V1.2

## Outcome

**PASS**

Dataset v1.2 has zero overlap with every frozen canonical evaluation asset on prompt text, assistant target text, and source case ID.

## Frozen Evaluation Assets Checked

| Eval split | Train overlap | Val overlap | Combined overlap | Result |
|---|---:|---:|---:|---|
| `heldout_validation` | `0 / 0 / 0` | `0 / 0 / 0` | `0 / 0 / 0` | PASS |
| `tool_holdout` | `0 / 0 / 0` | `0 / 0 / 0` | `0 / 0 / 0` | PASS |
| `no_call` | `0 / 0 / 0` | `0 / 0 / 0` | `0 / 0 / 0` | PASS |
| `adversarial` | `0 / 0 / 0` | `0 / 0 / 0` | `0 / 0 / 0` | PASS |
| `direct_answer` | `0 / 0 / 0` | `0 / 0 / 0` | `0 / 0 / 0` | PASS |

## Validation Notes

- The candidate was checked against the frozen canonical eval splits under `evals/data/canonical_v1/`.
- The frozen canonical evaluation manifest remains unchanged at `evals/canonical_eval_manifest_v1.json`.
- The dataset builder enforced fail-fast zero-overlap behavior.
- The train split and val split were both independently clean.

## Evidence Files

- [Dataset train split](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_train.jsonl)
- [Dataset val split](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_val.jsonl)
- [Dataset summary](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_summary.json)
- [Dataset leakage report](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_leakage_report.json)
- [Canonical evaluation manifest](/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json)
- [Canonical heldout validation](/opt/ai-stack/assistant-training/evals/data/canonical_v1/heldout_validation.jsonl)
- [Canonical tool holdout](/opt/ai-stack/assistant-training/evals/data/canonical_v1/tool_holdout.jsonl)
 - [Canonical no-call split](/opt/ai-stack/assistant-training/evals/data/canonical_v1/no_call.jsonl)
 - [Canonical adversarial split](/opt/ai-stack/assistant-training/evals/data/canonical_v1/adversarial.jsonl)
 - [Canonical direct-answer split](/opt/ai-stack/assistant-training/evals/data/canonical_v1/direct_answer.jsonl)
