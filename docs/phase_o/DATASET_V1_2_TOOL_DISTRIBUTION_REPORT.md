# Dataset V1.2 Tool Distribution Report

## Executive Summary

The v1.2 train split restores anchor concentration without collapsing back to the H2 pattern.

Compared with v1.1, the core tool families are far more repeated. Compared with H1/H2, the distribution is still broader and better balanced across the long tail.

## Train-Split Comparison

| Metric | H1 | H2 | Dataset v1.1 | Dataset v1.2 |
|---|---:|---:|---:|---:|
| Tool-positive rows | `1404` | `1404` | `1296` | `1393` |
| Unique tools | `26` | `23` | `26` | `26` |
| Minimum per-tool count | `8` | `8` | `24` | `24` |
| Maximum per-tool count | `370` | `470` | `56` | `269` |
| Top-1 share | `0.2635` | `0.3348` | `0.0432` | `0.1931` |
| Top-5 share | `0.6546` | `0.7258` | `0.2060` | `0.5212` |
| Top-8 share | `0.7593` | `0.8291` | `0.3256` | `0.6131` |
| `rg_search + read_file` share | `0.4409` | `0.5121` | `0.0733` | `0.3116` |
| Core-5 share (`rg_search`, `read_file`, `find_files`, `debug_tools`, `run_command`) | `0.6546` | `0.7258` | `0.1937` | `0.5212` |

## Core Anchors

| Tool | Train rows |
|---|---:|
| `rg_search` | `269` |
| `read_file` | `165` |
| `find_files` | `111` |
| `debug_tools` | `88` |
| `run_command` | `93` |

The core five now account for just over half of tool-positive exposure, which is the Phase N target zone.

## Secondary Anchors

| Tool | Train rows |
|---|---:|
| `check_service_health` | `45` |
| `get_system_datetime` | `38` |
| `write_file` | `42` |
| `stat_path` | `41` |
| `archive_create` | `36` |
| `archive_extract` | `40` |

These tools remain meaningfully represented, but they no longer dominate the signal the way they did in the flat v1.1 candidate.

## Breadth Restoration Tools

| Tool | Train rows |
|---|---:|
| `list_dir` | `33` |
| `list_models` | `36` |
| `move_path` | `37` |

These are the H1 breadth-restoration tools that disappeared in H2. v1.2 keeps them visible and auditable.

## Long-Tail Tools

| Tool | Train rows |
|---|---:|
| `apply_unified_diff` | `26` |
| `copy_path` | `28` |
| `get_system_version` | `26` |
| `git_diff` | `27` |
| `git_status` | `29` |
| `http_request` | `27` |
| `json_edit` | `24` |
| `list_active_ports` | `26` |
| `list_tools` | `26` |
| `service_control` | `29` |
| `sha256_file` | `24` |
| `test_run` | `27` |

The long tail is no longer close to uniform, but it is still sufficiently present to remain auditable.

## Interpretation

The distribution answer is not "make the dataset flat again."

It is:

 - restore anchor repetition;
 - preserve breadth;
 - keep the explicit safety block;
 - avoid H2-style narrowness;
 - avoid v1.1-style flattening.

 That is exactly what v1.2 does.
