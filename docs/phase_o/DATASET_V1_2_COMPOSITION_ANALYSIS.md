# Dataset V1.2 Composition Analysis

## Dataset Size

| Split | Rows |
|---|---:|
| Train | `2160` |
| Val | `240` |
| Total | `2400` |

## Category Counts

| Category | Rows |
|---|---:|
| `tool_positive` | `1548` |
| `runtime_alignment` | `360` |
| `no_call_direct_calibration` | `240` |
| `refusal_calibration` | `180` |
| `adversarial_no_call_calibration` | `72` |

## Phase O Component Counts

| Component | Rows |
|---|---:|
| Diversity | `774` |
| Commitment | `774` |
| Safety component total | `492` |

The explicit safety-calibration block also includes the runtime-alignment slice:

| Guardrail slice | Rows |
|---|---:|
| Runtime alignment | `360` |
| Explicit safety-calibration block total | `852` |

## Tool-Family Coverage

All `26` tool families are represented.

### Tiered Distribution

| Tier | Tools | Combined rows |
|---|---|---:|
| Core anchors | `rg_search`, `read_file`, `find_files`, `debug_tools`, `run_command` | `805` |
| Secondary anchors | `check_service_health`, `get_system_datetime`, `write_file`, `stat_path`, `archive_create`, `archive_extract` | `278` |
| Breadth restoration | `list_dir`, `list_models`, `move_path` | `114` |
| Long tail | remaining 12 tools | `351` |

This is the desired shape for v1.2: the core is no longer flat, but the long tail remains present and auditable.

## Train-Split Exposure

| Metric | Value |
|---|---:|
| Train tool-positive rows | `1393` |
| Tool-positive density | `0.6449` |
| Core anchor share | `0.5212` |
| `rg_search + read_file` share | `0.3116` |
| Unique tools in train split | `26` |
| Minimum train per-tool count | `24` |
| Maximum train per-tool count | `269` |

## Verification Against Phase N Requirements

| Requirement | Result |
|---|---|
| Tool-positive density in target range | PASS |
| Core anchor share in target range | PASS |
| `rg_search + read_file` share in target range | PASS |
| All 26 tools represented | PASS |
| Explicit safety block preserved | PASS |
| Contamination validation zero | PASS |

## Summary

 Dataset v1.2 is meaningfully more concentrated than v1.1, but it is still broader than H2 and less extreme than the H1/H2 anchor-heavy patches.

 That makes it the best structural match for the Phase N remediation hypothesis.
