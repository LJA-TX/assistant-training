# Phase X Completion Report

## Executive Summary

Phase X turns the Phase W anchor-concentration ablation into a precise construction plan.

The controlled variable is now explicit:

- anchor concentration inside the tool-positive slice.

The fixed factors are explicit:

- frozen scaffold,
- exact-tool-request cue,
- patch-local shape,
- canonical `tool_calls` envelope,
- safety block,
- and canonical evaluation contract.

## Key Construction Decisions

- Train rows stay fixed at `2160`.
- Validation rows stay frozen at `240`.
- Tool-positive rows stay fixed at `1393`.
- Safety rows stay fixed at `767`.
- The control arm uses `726` anchor rows.
- Treatment A uses `819` anchor rows.
- Treatment B uses `912` anchor rows.
- Treatment C uses `1011` anchor rows.
- Long-tail rows are the residual mass, redistributed proportionally from the v1.2 non-anchor histogram.

## Stop-Rule Interpretation

- Promotion failure means the arm is not promotable but may still be scientifically useful.
- Attribution failure means a fixed boundary changed, so the causal test is invalid.
- Operational failure means the dataset/run asset could not be built cleanly.

Safety regression alone is a promotion failure, not an attribution failure, unless it comes with boundary drift.

## Validation Requirements

Before any later build or run, verify:

- contamination is zero,
- anchor concentration matches the arm target,
- the exact cue is retained on 100 percent of tool-positive rows,
- the frozen scaffold is unchanged,
- the canonical `tool_calls` envelope is valid,
- and the safety block is preserved.

## Execution Sequencing

Use low-to-high order:

1. Control
2. Treatment A
3. Treatment B
4. Treatment C

Stop early if:

- the control already reaches the H1 floor,
- Treatment A reaches the floor,
- Treatment B reaches the floor,
- or Treatment C is the first arm that reaches the floor.

If all four arms fail the H1 floor while remaining valid, anchor concentration within the tested range is insufficient.

## Recommendation

Proceed to dataset construction.

This is the highest-information next step because it preserves causal interpretability while isolating the last unresolved variable from Phase V.

## Confidence Assessment

**Medium-high**

The design is specific enough to build later without inventing new variables, but the exact empirical threshold still depends on execution.
