# Phase V Completion Report

## Executive Summary

Phase V identifies the preserved properties that made H1/H2 successful and shows what later interventions lost.

The key conclusion is that H1/H2 preserved a **joint control surface**:

- frozen scaffold,
- exact-tool-request cue,
- high anchor concentration,
- and a small patch budget.

Later work separated those properties. The result was safety without capability in v1.1/v1.2, envelope drift in Phase Q, and direct-answer collapse in Phase U.

## Key Findings

- H1/H2 kept `1404` tool-positive rows on a fixed `2160`-row train surface.
- H1/H2 kept core-anchor share at `0.6546` and `0.7258`.
- H1/H2 kept `rg_search + read_file` share at `0.4409` and `0.5121`.
- H1/H2 kept the exact-tool-request cue on most tool-positive rows.
- v1.1 flattened tool families to near-uniform coverage and lost the exact-tool-request cue on tool rows.
- v1.2 restored some anchor mass but still did not recreate the H1/H2 cue structure.
- Phase Q failed mostly through wrapper/envelope drift.
- Phase U showed that canonical schema text alone does not recover tool-call capability.

## Preservation Model

The most defensible model is conjunctive:

1. frozen scaffold,
2. exact-tool-request cue,
3. anchor concentration.

The evidence does not support any single-factor explanation.

## Recommended Next Experiment

Run a controlled preservation ablation that keeps the exact tool-call contract fixed and varies only anchor concentration on the frozen scaffold.

That is the highest-information unresolved question remaining after H1/H2, v1.1, v1.2, Phase Q, and Phase U.

## Confidence Assessment

**Medium-high**

The evidence strongly supports the preservation model, but the minimal sufficient anchor level and the exact role of patch scale remain unmeasured.
