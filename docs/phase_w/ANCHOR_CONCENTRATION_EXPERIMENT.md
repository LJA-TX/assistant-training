# Phase W Anchor Concentration Experiment

## Experimental Question

If the frozen scaffold and exact-tool-request cue are preserved, how much anchor concentration is required to recover H1/H2-style capability?

## Design

This is a bracketing experiment with one control and three treatment levels.

### Invariants

All arms must preserve:

- the frozen Stage B recovery scaffold,
- the exact-tool-request cue on tool-positive rows,
- the same patch-local intervention shape,
- the canonical `tool_calls` envelope,
- the same train/val shell,
- the same safety block,
- the same canonical evaluator contract,
- and the same adapter/trainer geometry.

### Variable

Only anchor concentration varies.

The anchor block should scale the same five core tools in the same relative order:

- `rg_search`
- `read_file`
- `find_files`
- `debug_tools`
- `run_command`

The long tail remains represented and auditable, but only as a fixed residual mass.

## Treatment Levels

| Arm | Core anchor share | Expected qualitative role |
|---|---:|---|
| Control | `0.5212` | current failed anchor baseline |
| Treatment A | `0.5879` | moderate lift test |
| Treatment B | `0.6546` | H1-like threshold test |
| Treatment C | `0.7258` | H2-like threshold test |

## Patch-Local Shape

Use the same patch-local structure across all arms:

- same patch budget,
- same replacement topology,
- same positive-row envelope,
- same frozen non-tool surface.

Only the allocation of tool-positive mass across anchor vs tail tools changes.

## Sequential Execution Order

Use low-to-high ordering:

1. Control
2. Treatment A
3. Treatment B
4. Treatment C

This ordering is information-efficient because each step either narrows the threshold or stops the search early.

## Expected Outcomes

- If the control already recovers H1 floor metrics, the threshold is at or below `0.5212`.
- If Treatment A recovers and the control does not, the threshold lies between `0.5212` and `0.5879`.
- If Treatment B recovers and Treatment A does not, the threshold lies between `0.5879` and `0.6546`.
- If only Treatment C recovers, the threshold lies between `0.6546` and `0.7258`.
- If none recover, anchor concentration alone is not sufficient.

## Integrity Checks

Before execution, confirm:

- zero contamination overlap,
- 100 percent exact-tool-request cue retention on tool-positive rows,
- unchanged evaluator manifest and decode defaults,
- unchanged safety block,
- unchanged trainer geometry.

## Why This Is Controlled

The experiment changes exactly one axis. Everything else is frozen, so the result can be interpreted as an anchor-concentration effect rather than a prompt-regime or scaffold effect.
