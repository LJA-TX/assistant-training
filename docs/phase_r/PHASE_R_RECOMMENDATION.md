# Phase R Recommendation

## Recommended Next Direction

Focus next on **schema realization first**, implemented through a **control-preserving, anchor-weighted patch** rather than another broad full-dataset rebuild.

## Why

The evidence ranks the causes this way:

1. **Schema realization / envelope normalization**
2. **Anchor concentration**
3. **Control-surface preservation / dataset composition**
4. **Prompt-style distribution**
5. **Safety calibration**
6. **Trainer interaction**

The highest-confidence signal is the envelope failure in Phase Q:

- the model often emits the correct inner function object,
- but not the required outer `tool_calls` wrapper.

That is a schema-realization problem.

## What the Next Experiment Should Preserve

- The frozen control scaffold from the Stage B recovery line.
- The exact `tool_calls` envelope as the dominant positive target.
- High repetition on the core anchors:
  - `rg_search`
  - `read_file`
  - `find_files`
  - `debug_tools`
  - `run_command`
- A low-entropy prompt regime centered on the exact canonical tool-call instruction.

## What It Should Avoid

- another broad balancing pass across many prompt styles,
- another large safety expansion that changes the positive-to-negative ratio too aggressively,
- another full-corpus rematerialization that abandons the frozen scaffold.

## Recommended Shape

A more defensible follow-on would be:

- a compact patch on the existing control surface,
- exact `tool_calls` realization as the explicit objective,
- anchor-heavy rows for the core tools,
- and only minimal safety calibration needed to keep the refusal surface intact.

## Why Not Dataset Composition Alone

`v1.2` already improved composition relative to `v1.1`:

- tool-positive density increased,
- core-anchor share increased,
- `rg_search + read_file` share increased,
- contamination stayed clean.

But capability still did not recover. That means composition alone is not enough.

The missing ingredient is the exact outer schema.

## Final Recommendation

If the project wants to recover H1/H2-level capability, the next experiment should be framed as:

**schema-realization repair on a frozen control scaffold, with anchor-heavy repetition and a narrow canonical prompt regime.**
