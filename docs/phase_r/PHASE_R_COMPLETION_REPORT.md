# Phase R Completion Report

## Executive Summary

H1 and H2 succeeded because they were **small, controlled schema-realization patches** on a frozen recovery scaffold. They concentrated exact tool-call prompting, repeated a small set of anchor tools, and preserved the non-tool surface.

`v1.1` failed because it flattened the tool distribution and spread the prompt styles too widely.

`v1.2` recovered some anchor concentration, but it still spread the realization signal too broadly and did not recover the exact `tool_calls` envelope. Phase Q therefore shows a generalized schema drift, not a tool-selection problem.

## Key Findings

- H1/H2 were patch runs of `100` tool-positive rows on a frozen 2160-row control corpus.
- H1/H2 kept tool-positive density at `0.65`, with core-anchor share at `0.6546` and `0.7258`.
- `v1.1` flattened anchor share to `0.1937`.
- `v1.2` improved anchor share to `0.5212`, but still did not reach H1/H2 levels.
- H1/H2 used a narrow prompt regime centered on exact-tool-request and strict-JSON instructions.
- `v1.1` and `v1.2` spread positive rows across eight balanced prompt styles.
- Phase Q wrapper drift is dominated by bare `function/type` JSON objects, which points to envelope realization failure.

## Ranked Hypotheses

### 1. Schema realization deficit

Highest confidence.

The model often learns the inner function object but not the outer `tool_calls` wrapper. That exactly matches the Phase Q error profile.

### 2. Anchor concentration

High confidence.

H1/H2 keep `rg_search` and `read_file` much more dominant than `v1.1`, and still more dominant than `v1.2`.

### 3. Control-surface preservation / composition

High confidence.

The H1/H2 runs preserve the Stage B recovery scaffold and only patch 100 positive rows. The later datasets are full rebuilds.

### 4. Prompt-style distribution

Medium confidence.

Balanced prompt styles improve coverage but appear to dilute exact schema realization.

### 5. Safety calibration

Medium-low confidence.

Safety calibration matters, but it does not explain why Phase Q still failed after anchor weighting was restored.

### 6. Trainer interaction

Low confidence.

The same trainer family and LoRA geometry were used across phases; the response differences track data shape much more strongly than trainer changes.

## Confidence Assessment

Confidence is high that the decisive gap is not tool semantics in the abstract. The decisive gap is exact schema realization under a narrow control scaffold.

Confidence is moderate that future work should restore H1/H2-level anchor concentration and narrow the prompt regime.

Confidence is low that the answer lies in trainer changes.

## Recommended Next Action

Run a schema-realization-first design pass before authorizing any further governed training.

That pass should treat the `tool_calls` envelope as the primary target, not a secondary formatting detail.

## Recommended Next Phase

A controlled schema-repair phase should be the next experimental direction:

- preserve the frozen control surface,
- restore H1/H2-like anchor density,
- keep the prompt regime narrow,
- and validate whether exact JSON returns before broadening composition again.
