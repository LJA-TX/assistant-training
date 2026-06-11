# Internal Signal Inventory

## Executive Summary

The repository's internal tool-positive signal was not absent. It was narrowed away by the v1.0 build path.

- The three upstream tool sources contain `1,592` normalized tool rows and `144` deduplicated tool-positive exemplars across `26` tools, `128` prompts, `44` case ids, and `68` distinct tool-call targets.
- The canonical v1.0 train slice preserved only `1` of those `26` tools, `1` of `128` prompts, `1` of `44` case ids, and `1` of `68` targets.
- The later i3 recovery corpus restored much of the lost surface diversity, but it did so through a thin and heavily resampled internal source pool rather than through a deep native corpus.

## Inputs

- `data/tool_ft_allaliases_20260525_from_qual_reports_freq.jsonl`
- `/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_aug_rebalanced_20260417T104659Z.jsonl`
- `/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_aug_focus_rebalanced_20260417T104747Z.jsonl`
- `scripts/build_dataset_v1.py`
- `data/v1_0/dataset_v1_0_summary.json`
- `data/v1_0/dataset_v1_0_train.jsonl`
- `data/v1_0/dataset_v1_0_val.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_train.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_val.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_summary.json`
- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl`

## Upstream Inventory

### Raw normalized upstream rows

| Source file | Normalized tool rows |
|---|---:|
| `tool_ft_allaliases_20260525_from_qual_reports_freq.jsonl` | 832 |
| `tool_sft_aug_rebalanced_20260417T104659Z.jsonl` | 456 |
| `tool_sft_aug_focus_rebalanced_20260417T104747Z.jsonl` | 304 |
| Total | 1,592 |

### Deduplicated upstream diversity

| Stage | Rows | Unique tools | Unique prompts | Unique case ids | Unique targets |
|---|---:|---:|---:|---:|---:|
| Raw normalized upstream | 1,592 | 26 | 128 | 45 | 68 |
| Deduplicated upstream pool | 144 | 26 | 128 | 44 | 68 |

The upstream signal was already concentrated in `rg_search` and `read_file`, but it still covered `26` tool families and `44` distinct source cases before the build path began excluding rows.

## v1.0 Collapse Path

The canonical collapse is reproducible from `scripts/build_dataset_v1.py` when the RNG is consumed in the same order as the build function.

| Build stage | Rows | Unique tools | Unique prompts | Unique case ids | Unique targets |
|---|---:|---:|---:|---:|---:|
| Deduplicated upstream pool | 144 | 26 | 128 | 44 | 68 |
| Tool-holdout pool | 8 | 8 | 8 | 8 | 8 |
| Non-holdout pool | 136 | 20 | 120 | 36 | 60 |
| Heldout validation draw | 100 | 17 | 90 | 29 | 49 |
| Remaining after eval exclusion | 36 | 8 | 32 | 15 | 25 |
| v1.0 validation tool-positive slice | 108 | 8 | 31 | 15 | 24 |
| v1.0 train tool pool survivors | 1 | 1 | 1 | 1 | 1 |
| v1.0 train tool-positive slice | 972 | 1 | 1 | 1 | 1 |
| Stage B train tool-positive slice | 1,404 | 1 | 1 | 1 | 1 |

### Survivor identity

The final v1.0 train survivor is the single case:

- `p0_rg_search_3`

The val draw removed the other `35` remaining fingerprints, leaving one trainable tool-positive fingerprint for both `dataset_v1_0_train.jsonl` and the later Stage B resample.

## Lost Diversity

### Loss from deduplicated upstream to v1.0 train

| Metric | Upstream | v1.0 train | Loss |
|---|---:|---:|---:|
| Unique tools | 26 | 1 | 25 lost (`96.2%`) |
| Unique prompts | 128 | 1 | 127 lost (`99.2%`) |
| Unique case ids | 44 | 1 | 43 lost (`97.7%`) |
| Unique targets | 68 | 1 | 67 lost (`98.5%`) |

### Tools lost entirely from the v1.0 train tool-positive slice

`apply_unified_diff`, `archive_create`, `archive_extract`, `check_service_health`, `copy_path`, `debug_tools`, `find_files`, `get_system_datetime`, `get_system_version`, `git_diff`, `git_status`, `http_request`, `json_edit`, `list_active_ports`, `list_dir`, `list_models`, `list_tools`, `move_path`, `read_file`, `run_command`, `service_control`, `sha256_file`, `stat_path`, `test_run`, `write_file`

The collapse is therefore not a minor skew. It is near-total elimination of upstream tool-positive diversity from the training path.

## Diversity Recovered For i3

### Recovery source pool

| Recovery source layer | Rows | Unique tools | Notes |
|---|---:|---:|---|
| Curated adapted internal rows | 122 | 20 | Directly transformed from internal tool sources |
| Synthetic recovery additions | 42 | 11 | Coverage, disambiguation, debug, and pressure rows |
| Total i3 source pool | 164 | 26 | Restores the full upstream tool set at source-pool level |

### Recovered i3 train slice

| Slice | Rows | Unique tools | Unique prompts | Unique case ids | Unique targets |
|---|---:|---:|---:|---:|---:|
| Stage B recovery i3 train tool-positive | 1,404 | 23 | 154 | 74 | 61 |

### Recovery detail

- Tools recovered from internal adapted rows: `get_system_version`, `git_diff`, `git_status`, `http_request`, `json_edit`, `list_active_ports`, `list_dir`, `list_models`, `list_tools`, `move_path`, `service_control`, `sha256_file`, `stat_path`, `test_run`, `write_file`
- Tools recovered only through synthetic internal additions: `apply_unified_diff`, `archive_create`, `archive_extract`, `copy_path`, `debug_tools`, `get_system_datetime`
- Tools present upstream but absent from the i3 training distribution: `list_dir`, `list_models`, `move_path`

That means i3 restored broad internal signal relative to collapsed v1.0 train, but not the entire upstream surface inside the final training distribution.

## Determination

The internal repository signal was substantial enough to support a much broader tool-positive training slice than v1.0 delivered.

The evidence supports three distinct conclusions:

1. The canonical v1.0 collapse was pipeline-caused, not source-caused.
2. Internal signal recovery can restore a large amount of lost surface diversity without external data.
3. The recovered internal corpus is still thin at source depth, so "recovered diversity" and "deep supervision" are not the same thing.

## Sources Used

- `scripts/build_dataset_v1.py`
- `data/v1_0/dataset_v1_0_summary.json`
- `data/v1_0/dataset_v1_0_train.jsonl`
- `data/v1_0/dataset_v1_0_val.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_train.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_val.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_summary.json`
- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl`
- `docs/phase_f/CURRENT_DATASET_ASSESSMENT.md`
- `docs/phase_f/INDEPENDENT_DATASET_COLLAPSE_ASSESSMENT_Grok-Build.md`
