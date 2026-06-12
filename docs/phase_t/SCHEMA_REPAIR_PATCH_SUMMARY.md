# Schema Repair Patch Summary

## Patch Assets

- [Patch JSONL](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_t_schema_repair_patch_train.jsonl)
- [Patch summary JSON](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_t_schema_repair_patch_summary.json)
- [Patch contamination report JSON](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_t_schema_repair_patch_leakage_report.json)
- [Patch readiness assessment JSON](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_phase_t_schema_repair_patch_readiness_assessment.json)

## Row Counts

| Split | Rows |
|---|---:|
| Train / patch | 60 |
| Val | 0 |
| Total | 60 |

## Tool Distribution

| Tool | Rows |
|---|---:|
| `rg_search` | 12 |
| `read_file` | 12 |
| `find_files` | 12 |
| `debug_tools` | 12 |
| `run_command` | 12 |

## Schema Targets

The patch is built to reinforce the exact contract that Phase Q failed to recover:

- canonical `tool_calls` envelope;
- single-call assistant structure;
- no alternate wrapper shapes;
- one tool-positive row per example.

## Lineage

This patch is a Phase S micro-intervention for the frozen Stage B recovery scaffold.

The patch metadata records:

- `dataset_v1_2` as the parent dataset;
- `frozen_stage_b_recovery_scaffold` as the control surface;
- `H1`, `H2`, and `Phase_Q` as the comparison basis;
- `schema_repair` as the treatment component;
- `strict_json` as the prompt regime.

## Interpretation

This is intentionally small and narrow.

It does not attempt to solve long-tail coverage or full dataset redesign. It exists to test whether exact envelope realization can move when the five core anchors are trained under the same strict schema contract.

