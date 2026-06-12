# Phase W Preservation Ablation Options

## Objective

Test the Phase V preservation model by varying only anchor concentration while holding fixed:

- the frozen Stage B recovery scaffold,
- the exact-tool-request cue on tool-positive rows,
- the patch-local intervention shape,
- and the canonical single-call `tool_calls` contract.

## Evidence Basis

Phase V concluded that H1/H2 preserved three properties together:

- frozen scaffold and low-delta patching,
- exact-tool-request cue on most tool-positive rows,
- high anchor concentration on the five core tools.

The measured corpus-level values that matter are:

| Dataset | Core anchor share | `rg_search + read_file` share | Tool-positive density | exact JSON | tool-name accuracy | argument accuracy |
|---|---:|---:|---:|---:|---:|---:|
| H1 | `0.6546` | `0.4409` | `0.65` | `0.44` | `0.7143` | `0.6286` |
| H2 | `0.7258` | `0.5121` | `0.65` | `0.48` | `0.7714` | `0.6929` |
| v1.2 | `0.5212` | `0.3116` | `0.6449` | `0.03` | `0.0714` | `0.0429` |
| Phase U | fixed 5-anchor patch | fixed 5-anchor patch | `1.0` on patch rows | `0.0` | `0.0` | `0.0` |

Sources:

- [Phase V control surface comparison](/opt/ai-stack/assistant-training/docs/phase_v/CONTROL_SURFACE_COMPARISON.md)
- [Phase V preservation model](/opt/ai-stack/assistant-training/docs/phase_v/PRESERVATION_MODEL_ANALYSIS.md)
- [Phase L execution review](/opt/ai-stack/assistant-training/docs/phase_l/PHASE_L_EXECUTION_REVIEW.md)
- [Phase Q execution review](/opt/ai-stack/assistant-training/docs/phase_q/PHASE_Q_EXECUTION_REVIEW.md)
- [Phase U execution review](/opt/ai-stack/assistant-training/docs/phase_u/PHASE_U_EXECUTION_REVIEW.md)

## Candidate Levels

Use one control and three treatment levels. Keep the non-anchor parts identical across all arms.

| Arm | Corpus-level anchor target | `rg_search + read_file` target | Meaning |
|---|---:|---:|---|
| Control | `0.5212` | `0.3116` | v1.2-like low anchor baseline on the frozen scaffold and exact cue |
| Treatment 1 | `0.5879` | `0.3762` | midpoint between v1.2 and H1 |
| Treatment 2 | `0.6546` | `0.4409` | H1-like anchor concentration |
| Treatment 3 | `0.7258` | `0.5121` | H2-like anchor concentration |

## Why These Levels

They bracket the observed success region without changing any other variable.

- The control sits at the failed v1.2 anchor level.
- Treatment 1 tests whether a moderate increase is already enough.
- Treatment 2 tests the H1 floor.
- Treatment 3 tests the H2 ceiling.

## What Must Stay Fixed

- Same frozen Stage B recovery scaffold.
- Same exact-tool-request cue on tool-positive rows.
- Same canonical single-call `tool_calls` envelope.
- Same patch-local shape and patch budget.
- Same safety block and no-call coverage.
- Same canonical evaluator contract.

## Expected Reading

- If only the anchor level changes and metrics improve monotonically, the preservation model is supported.
- If all levels fail together, anchor concentration alone is not sufficient.
- If the control already succeeds, the required anchor level is at or below the control.

## Why Not Another Full Redesign

A full redesign would move too many levers at once:

- prompt manifold breadth,
- safety calibration,
- family balance,
- and anchor mass.

That would lose the causal signal Phase V isolated. This ablation keeps the experiment one-dimensional.
