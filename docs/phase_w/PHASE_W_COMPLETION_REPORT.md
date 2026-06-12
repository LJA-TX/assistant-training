# Phase W Completion Report

## Executive Summary

Phase W defines the smallest controlled experiment capable of testing the Phase V preservation model.

The preserved factors from H1/H2 are now isolated into a single remaining question:

> how much anchor concentration is needed, with scaffold and exact cue held fixed, to recover H1/H2-style capability?

## Key Findings

- H1/H2 succeeded on a frozen scaffold with a small patch and a majority of exact-tool-request prompts on positive rows.
- v1.1 failed after flattening the tool family distribution and losing the exact-tool-request cue on tool rows.
- v1.2 restored some anchor mass but still failed to recover exact JSON behavior.
- Phase Q showed envelope drift.
- Phase U showed that schema-only repair preserves safety but does not recover capability.

## Experimental Design

The recommended experiment is a controlled anchor-concentration bracket:

- Control: `0.5212`
- Treatment A: `0.5879`
- Treatment B: `0.6546`
- Treatment C: `0.7258`

All arms keep:

- the frozen scaffold,
- the exact-tool-request cue,
- the patch-local shape,
- and the canonical `tool_calls` contract.

## Attribution Logic

Because cue and scaffold are held fixed, any between-arm change can be attributed to anchor concentration.

If the arm response is monotonic or thresholded across the bracket, the preservation model is supported.
If all arms fail together, anchor concentration alone is not sufficient.

## Stop Rules

Do not interpret any run if:

- contamination overlap is nonzero,
- wrapper leakage is nonzero,
- no-call or adversarial no-call correctness drops below `1.0`,
- aggregate invalid JSON exceeds `0.30`,
- or the canonical eval contract drifts.

## Recommended Next Action

Proceed later, if authorized, with the bracketed anchor-concentration experiment rather than a full-corpus redesign.

That is the highest-information way to test the remaining unresolved variable.

## Confidence Assessment

**Medium-high**

The evidence is strong enough to justify the ablation, but not strong enough to name the exact minimum anchor share before execution.
