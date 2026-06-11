# Phase K Contamination Validation Report

## Outcome

**PASS**

The Dataset v1.1 candidate has zero overlap with the frozen canonical evaluation splits on prompt, target, and source case ID.

## Checked Splits

| Split | Prompt overlap | Target overlap | Case-ID overlap | Result |
|---|---:|---:|---:|---|
| `heldout_validation` | `0` | `0` | `0` | PASS |
| `tool_holdout` | `0` | `0` | `0` | PASS |
| `no_call` | `0` | `0` | `0` | PASS |
| `adversarial` | `0` | `0` | `0` | PASS |
| `direct_answer` | `0` | `0` | `0` | PASS |

## Validation Notes

- The builder checked the candidate against the frozen canonical eval files in `evals/data/canonical_v1/`.
- No prompt text from the candidate matched the frozen heldout or tool-holdout prompts.
- No assistant target JSON from the candidate matched the frozen heldout or tool-holdout tool-call targets.
- No candidate source case IDs collided with the frozen eval case IDs.
- The same zero-overlap result also held for the no-call, adversarial, and direct-answer eval splits, which is extra margin beyond the requested minimum.

## Evidence Files

- [Candidate train split](/opt/ai-stack/assistant-training/data/v1_1/dataset_v1_1_train.jsonl)
- [Candidate val split](/opt/ai-stack/assistant-training/data/v1_1/dataset_v1_1_val.jsonl)
- [Contamination report JSON](/opt/ai-stack/assistant-training/data/v1_1/dataset_v1_1_leakage_report.json)
- [Canonical heldout validation](/opt/ai-stack/assistant-training/evals/data/canonical_v1/heldout_validation.jsonl)
- [Canonical tool holdout](/opt/ai-stack/assistant-training/evals/data/canonical_v1/tool_holdout.jsonl)

