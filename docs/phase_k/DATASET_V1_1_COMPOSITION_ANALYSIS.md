# Phase K Dataset V1.1 Composition Analysis

## Dataset Size

| Split | Rows |
|---|---:|
| Train | `2160` |
| Val | `240` |
| Total | `2400` |

## Category Counts

| Category | Rows |
|---|---:|
| `tool_positive` | `1440` |
| `runtime_alignment` | `360` |
| `no_call_direct_calibration` | `240` |
| `refusal_calibration` | `180` |
| `adversarial_no_call_calibration` | `180` |

## Phase K Component Counts

| Component | Rows |
|---|---:|
| Diversity | `720` |
| Commitment | `720` |
| Safety | `600` |

## Tool-Family Counts

All `26` tool families are represented.

| Tool families with `56` rows | Tool families with `55` rows |
|---|---|
| `apply_unified_diff`, `archive_create`, `archive_extract`, `check_service_health`, `copy_path`, `debug_tools`, `find_files`, `get_system_datetime`, `get_system_version`, `git_diff` | `git_status`, `http_request`, `json_edit`, `list_active_ports`, `list_dir`, `list_models`, `list_tools`, `move_path`, `read_file`, `rg_search`, `run_command`, `service_control`, `sha256_file`, `stat_path`, `test_run`, `write_file` |

The tool-family distribution is intentionally tight:

- minimum tool-family count: `55`
- maximum tool-family count: `56`
- spread: `1`

This keeps the candidate balanced enough to preserve diversity without reintroducing the literal-anchor concentration that Phase G and Phase H were designed to reduce.

## Source-Lineage Counts

| Source lineage | Rows |
|---|---:|
| `canonical_case_template` | `720` |
| `contrastive_positive` | `540` |
| `contrastive_negative` | `180` |

This lineage mix is consistent with the Phase J guidance:

- canonical templates supply the diversity backbone;
- contrastive positives supply anchor-light commitment pressure;
- contrastive negatives keep the model from depending on one lexical shell.

## Verification Against Phase J Requirements

| Requirement | Result |
|---|---|
| Total row budget preserved | PASS |
| Diversity/commitment balance maintained | PASS |
| Explicit safety slices present | PASS |
| All tool families represented | PASS |
| Prompt/target/case-ID contamination against heldout and tool-holdout | PASS |
| Canonical eval semantics unchanged | PASS |

## Summary

The composition is balanced enough to test the combined bottleneck without making the candidate a narrow rewrite of the earlier Phase I slices.
The candidate is still large enough to be a realistic future training input, but the safety slices are now explicit and the tool-positive core is evenly spread across the full tool family set.

## Sources Used

- `data/v1_1/dataset_v1_1_summary.json`
- `data/v1_1/dataset_v1_1_leakage_report.json`
- `docs/phase_j/DATASET_V1_1_DESIGN_REQUIREMENTS.md`
- `docs/phase_j/PHASE_K_RECOMMENDATION.md`
