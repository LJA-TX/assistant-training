# Recovery Corpus Analysis

## Executive Summary

The i3 recovery corpus is genuinely broader than collapsed v1.0 train, but its effective depth is much smaller than its row count suggests.

- The tool-positive slice contains `1,404` rows with `23` tools, `154` prompts, `74` case ids, `61` exact argument payloads, and `27` tool-plus-schema combinations.
- The same slice is still highly concentrated: the top `2` tools account for `51.2%` of all tool-positive rows and the top `5` tools account for `72.6%`.
- Most of the tail tools are learned from one or two source exemplars and then oversampled aggressively, which means the corpus looks diverse on paper but remains shallow as supervision.

## Inputs

- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_summary.json`
- `scripts/build_stage_b_recovery_i3_dataset.py`

## Headline Diversity Metrics

| Metric | Value |
|---|---:|
| Tool-positive rows | 1,404 |
| Unique tools | 23 |
| Unique prompts | 154 |
| Unique case ids | 74 |
| Unique targets | 61 |
| Unique exact argument payloads | 61 |
| Unique argument-key schemas | 22 |
| Unique tool-plus-schema combinations | 27 |
| Effective tool diversity | 6.03 |
| Effective prompt diversity | 85.34 |
| Effective case diversity | 29.38 |

The apparent tool diversity is `23`, but the effective tool diversity is only about `6`. That is the key gap between visible breadth and usable depth.

## Source Depth Versus Resampled Training Weight

### Overall concentration

| Measure | Source pool | Final i3 train slice |
|---|---:|---:|
| Unique source rows | 164 | 1,404 rows after resampling |
| Unique tools | 26 | 23 |
| Effective tool diversity | 4.41 | 6.03 |
| Top 2 tool share | 62.8% | 51.2% |
| Top 5 tool share | 82.3% | 72.6% |

The resampling plan somewhat flattens the heaviest source concentration, but it does not create new source depth. It only redistributes repetition.

### Oversampling by tool

| Tool | Unique source rows | Train rows | Oversample factor |
|---|---:|---:|---:|
| `rg_search` | 63 | 470 | 7.46 |
| `read_file` | 40 | 249 | 6.22 |
| `find_files` | 3 | 120 | 40.00 |
| `debug_tools` | 20 | 110 | 5.50 |
| `run_command` | 8 | 70 | 8.75 |
| `check_service_health` | 2 | 55 | 27.50 |
| `get_system_datetime` | 1 | 45 | 45.00 |
| `write_file` | 4 | 45 | 11.25 |
| `archive_create` | 1 | 35 | 35.00 |
| `stat_path` | 2 | 35 | 17.50 |
| `archive_extract` | 1 | 30 | 30.00 |
| `copy_path` | 1 | 30 | 30.00 |

The long tail is especially shallow:

- `15` tools are trained from exactly `1` source exemplar.
- `19` tools are trained from `2` source exemplars or fewer.

That means many tools are represented in the label space without having enough underlying variation to support robust heldout generalization.

## Prompt And Case Diversity

### Prompt concentration

- `154` unique prompts exist, but only `61` unique tool-call targets exist.
- `11` prompts appear at least `20` times.
- The top `10` prompts account for `26.1%` of all tool-positive rows.
- Only `1` prompt appears exactly once.

This is better than collapsed v1.0 train, but it still means many prompt variants map onto the same small target set.

### Case concentration

- `74` unique case ids exist.
- `18` case ids appear at least `20` times.
- The top `10` case ids account for `51.1%` of all tool-positive rows.

Case-level concentration is materially stronger than prompt-level concentration. The corpus therefore contains many prompt variants that still resolve back to a relatively small set of canonical cases.

## Argument And Schema Diversity

### Dominant schema shapes

| Argument-key schema | Rows |
|---|---:|
| `path, pattern` | 451 |
| `line_end, line_start, path` | 249 |
| empty arguments | 163 |
| `pattern, root` | 120 |
| `command` | 70 |
| `path` | 57 |
| `url` | 55 |

The top `4` schema shapes account for `983 / 1,404` rows (`70.0%`).

### Interpretation

- `rg_search` plus `read_file` alone supply almost half of all rows and almost half of all schema mass.
- Empty-argument tools (`debug_tools`, `get_system_datetime`) add surface tool diversity but contribute little argument-composition pressure.
- Only `61` exact argument payloads exist across `1,404` rows, so the tool-positive corpus is still heavily repetitive at the argument level.

## Source-Type Mix

| Source label | Train rows | Share |
|---|---:|---:|
| `adapted_source_i3` | 938 | 66.8% |
| `synthetic_coverage_i3` | 225 | 16.0% |
| `synthetic_debug_tools_i3` | 110 | 7.8% |
| `synthetic_disambiguation_i3` | 70 | 5.0% |
| `synthetic_run_command_i3` | 41 | 2.9% |
| `synthetic_length_pressure_i3` | 20 | 1.4% |

All tool-positive i3 rows are transformed or synthetic rows. Even the adapted-source rows are rewritten into the i3 schema form rather than preserved as untouched originals.

## Determination

The i3 recovery corpus has true diversity, but not deep diversity.

It materially repaired the single-example collapse, yet its effective supervision remains limited by:

1. a shallow source pool per tool,
2. heavy oversampling of one- and two-example tool families,
3. concentration in a few schema shapes, and
4. many prompt variants resolving to the same small target set.

That is enough to support some parseability gains. It is not enough to assume strong heldout tool generalization.

## Sources Used

- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_summary.json`
- `scripts/build_stage_b_recovery_i3_dataset.py`
- `docs/phase_f/INDEPENDENT_DATASET_COLLAPSE_ASSESSMENT_Grok-Build.md`
