# Phase X Arm Specifications

## Common Invariants

Every arm must preserve:

- `2160` training rows,
- `240` validation rows,
- `1393` training tool-positive rows,
- `767` training safety rows,
- the exact-tool-request cue on every tool-positive row,
- the canonical `tool_calls` envelope,
- the frozen scaffold,
- and the same canonical evaluation contract.

The validation split is frozen across arms and is not part of the ablation variable.

## Common Safety Block

Keep the train safety rows fixed to the v1.2 train baseline:

- `324` runtime-alignment rows,
- `216` no-call-direct-calibration rows,
- `162` refusal-calibration rows,
- `65` adversarial-no-call-calibration rows.

That preserves the safety scaffold while leaving anchor concentration as the only moving part.

## Arm Table

| Arm | Train rows | Tool-positive rows | Anchor rows | Long-tail rows | Safety rows | Exact cue preservation | Scaffold preservation |
|---|---:|---:|---:|---:|---:|---|---|
| Control | `2160` | `1393` | `726` | `667` | `767` | `100% of tool-positive rows` | Frozen Stage B recovery scaffold copied bit-for-bit for non-tool rows |
| Treatment A | `2160` | `1393` | `819` | `574` | `767` | `100% of tool-positive rows` | Same scaffold and same row topology |
| Treatment B | `2160` | `1393` | `912` | `481` | `767` | `100% of tool-positive rows` | Same scaffold and same row topology |
| Treatment C | `2160` | `1393` | `1011` | `382` | `767` | `100% of tool-positive rows` | Same scaffold and same row topology |

## Anchor Allocation Method

Use the same five anchor tools in every arm:

- `rg_search`
- `read_file`
- `find_files`
- `debug_tools`
- `run_command`

Within each arm:

- allocate the requested anchor rows across those five tools using the frozen anchor ordering from the Phase V control surface,
- preserve a nonzero floor for every long-tail tool family,
- and scale the 21 long-tail tool families proportionally from the v1.2 non-anchor histogram.

## Long-Tail Allocation Method

The long-tail block is the residual after anchor allocation.

Allocation rule:

- preserve all 21 non-anchor tool families,
- scale their relative frequencies from the v1.2 non-anchor distribution,
- apply largest-remainder rounding,
- and enforce a minimum floor of 1 row per family.

This keeps long-tail representation auditable while anchor concentration changes.

## Cue Preservation Method

Every tool-positive row should use the same fixed system prompt template:

`Use ONLY the exact tool requested. Keep final answer concise. If a tool result already answers the task, stop and finalize. Return only strict JSON tool calls when a tool is required. Do not add prose, markdown, or shell blocks.`

That string preserves the H1/H2 exact-tool-request cue while keeping the canonical `tool_calls` requirement explicit.

## Scaffold Preservation Method

The scaffold is preserved by leaving all non-tool rows unchanged relative to the frozen Stage B recovery surface.

Only the tool-positive slice is rebalanced.
No change is made to:

- the non-tool slice content,
- the validation split,
- the canonical evaluator,
- or the comparison contract.

## Why These Specs Are Executable

The counts are integerized and the fixed surfaces are named explicitly, so a later builder can translate this spec directly into train/validation JSONL without inventing new degrees of freedom.
