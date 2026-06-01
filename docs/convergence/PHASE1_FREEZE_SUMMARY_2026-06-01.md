# Phase 1 Freeze Summary (2026-06-01)

## Final Architecture

1. OpenClaw (local) is the operator-facing agent layer.
2. assistant-runtime (local) is the policy, tool-validation, and execution middleware.
3. Nemotron-3-Nano-30B-A3B-FP8 (`inferserv`) is the upstream model endpoint used by assistant-runtime.

## Alias Inventory (Authoritative for Phase 1)

| OpenClaw Canonical Name | assistant-runtime Tool | Status |
|---|---|---|
| `read` | `read_file` | mapped |
| `write` | `write_file` | intentionally unmapped (no alias) |
| `edit` | *(no direct `edit_file` schema)* | no equivalent |
| `bash` | `run_command` | intentionally unmapped (no alias) |
| `ls` | `list_dir` | observed but unmapped |
| `find` | `find_files` | intentionally unmapped |
| `grep` | `rg_search` | intentionally unmapped |
| `search` | `rg_search` | intentionally unmapped |

Phase 1 explicit alias map remains narrow:

- `read -> read_file`

## Read/Write Policy Model

1. assistant-runtime `allowed_roots` controls write-capable paths.
2. assistant-runtime `read_only_extra_roots` includes `/opt/ai-stack/assistant-training` for observer read access without write expansion.
3. assistant-runtime validation enforces tool schema and path policy before execution.
4. OpenClaw observer profile remains read-only by instruction/policy intent; hard write denial is enforced at assistant-runtime path policy.

## Regression Gates (Phase 1C)

1. Verified observer read execution gate:
   - requires `tool_call_outcome`, `execution_status=OK`, `tool_name=read_file`, and path under `/opt/ai-stack/assistant-training`.
2. Explicit observer write-policy denial gate:
   - requires parseable `write_file` attempt, runtime execution attempt, and denial containing `outside allowed_roots policy`.
3. Main-agent write-policy denial gate:
   - requires `write_file` attempt denial with the same path-policy error and no file creation.

## Known Limitations

1. Only `read` alias is promoted in Phase 1; other capability-style names are intentionally not auto-mapped.
2. Observer usability is currently terminal/OpenClaw-interface driven; external chat integration is deferred.
3. Observer conclusions are considered valid only when telemetry-backed tool execution is present.

## Deferred Phase 2 Items

1. Telegram (or alternate chat channel) integration.
2. OpenAI-compatible gateway/API surface hardening for Open WebUI integration workflow.
3. Optional evidence-driven alias expansion for additional read-only capability names.
4. Observer utility evaluation and UX refinements after baseline freeze.
