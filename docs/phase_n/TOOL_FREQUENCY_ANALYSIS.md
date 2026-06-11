# Tool Frequency Analysis

## Executive Summary

The earlier H1/H2 datasets were anchor-heavy.
Dataset v1.1 is almost perfectly flat.

That flattening is large enough to matter:

- H1 and H2 both preserve a strong repeated core,
- v1.1 removes that repetition pressure while keeping all 26 tools present,
- and the result is capability collapse despite perfect safety.

## Tool-Positive Density

| Dataset | Tool-positive rows | Train rows | Density |
|---|---:|---:|---:|
| H1 | `1404` | `2160` | `0.65` |
| H2 | `1404` | `2160` | `0.65` |
| Dataset v1.1 | `1296` | `2160` | `0.60` |

The density reduction is modest by itself.
It is not large enough to explain a collapse to zero on its own.

## Tool-Family Distribution

| Dataset | Unique tools | Min per-tool count | Max per-tool count | Top-1 share | Top-5 share | Top-8 share |
|---|---:|---:|---:|---:|---:|---:|
| H1 | `26` | `8` | `370` | `0.2635` | `0.6546` | `0.7593` |
| H2 | `23` | `8` | `470` | `0.3348` | `0.7258` | `0.8291` |
| Dataset v1.1 | `26` | `46` | `56` | `0.0432` | `0.2060` | `0.3256` |

## Anchor Tools

The recurring anchor tools in the H1/H2 data are:

- `rg_search`
- `read_file`
- `find_files`
- `debug_tools`
- `run_command`
- `check_service_health`
- `get_system_datetime`
- `write_file`
- `stat_path`
- `archive_create`

These are the tools whose repetition most strongly encoded the canonical tool-call envelope.

### Anchor Concentration

| Dataset | `rg_search + read_file` share | Core-5 share (`rg_search`, `read_file`, `find_files`, `debug_tools`, `run_command`) |
|---|---:|---:|
| H1 | `0.4409` | `0.6546` |
| H2 | `0.5121` | `0.7258` |
| Dataset v1.1 | `0.0733` | `0.1937` |

The collapse is not subtle.
The canonical core fell from roughly two-thirds to less than one-fifth of tool-positive exposure.

## Exact Anchor Counts

| Tool | H1 | H2 | Dataset v1.1 |
|---|---:|---:|---:|
| `rg_search` | `370` | `470` | `47` |
| `read_file` | `249` | `249` | `48` |
| `find_files` | `120` | `120` | `53` |
| `debug_tools` | `110` | `110` | `51` |
| `run_command` | `70` | `70` | `52` |
| `check_service_health` | `55` | `55` | `51` |
| `get_system_datetime` | `45` | `45` | `48` |
| `write_file` | `47` | `45` | `47` |
| `stat_path` | `35` | `35` | `48` |
| `archive_create` | `35` | `35` | `49` |

## Breadth Restoration

H1 and H2 differ in breadth:

- H1 includes `list_dir`, `list_models`, and `move_path`.
- H2 drops those three tools entirely.
- Dataset v1.1 restores them, but in a flat distribution.

### H1-Only Relative To H2

- `list_dir`
- `list_models`
- `move_path`

### V1.1 Relative To H2

- `list_dir`
- `list_models`
- `move_path`

This means Dataset v1.1 successfully restored breadth.
It did not preserve the anchor concentration needed for capability.

## Concentration Interpretation

H1/H2 show that the model can learn strong tool-call behavior when a small anchor core is repeated heavily.
Dataset v1.1 shows that breadth without concentration is not enough.

The likely target for v1.2 is therefore neither H2-style narrowness nor v1.1-style uniformity.
It is a tiered distribution with:

- a repeated anchor core,
- a preserved long tail,
- and all 26 tools still represented.

## Sources Used

- `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_train.jsonl`
- `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_train.jsonl`
- `data/v1_1/dataset_v1_1_train.jsonl`
