# Phase S Completion Report

## Executive Summary

Phase S is complete as a documentation-only design pass.

The evidence supports a narrow schema-realization hypothesis: H1 and H2 succeeded because they repeatedly trained the exact `tool_calls` envelope on a frozen scaffold, while Phase Q showed that v1.2 still drifted into bare `function/type` objects instead of the canonical wrapper.

The recommended next step is a 60-row schema-repair micro-patch, not a full dataset redesign.

## Key Findings

- H1 and H2 were small patch runs on the frozen 2160-row scaffold and reached exact JSON validity of `0.44` and `0.48`.
- Phase Q on Dataset v1.2 reached only `0.03` exact JSON validity and produced `94` near-canonical wrapper or envelope drift failures.
- The core anchors account for most of the wrapper drift in Phase Q, which makes them the right target set for a minimal patch.
- v1.1 flattened anchor concentration too aggressively.
- v1.2 restored some anchor concentration, but not the exact schema realization needed by the frozen evaluator.

## Minimum Intervention Assessment

The smallest defensible experiment is:

- 60 tool-positive rows;
- 12 rows each for `rg_search`, `read_file`, `find_files`, `debug_tools`, and `run_command`;
- strict `tool_calls` envelope targets;
- no change to safety rows or scaffold rows;
- no evaluator, scoring, or governance changes.

That design is small enough to preserve attribution and large enough to test whether envelope realization can move off the near-zero Phase Q baseline.

## Controlled Experiment Summary

The recommended controlled structure is staged:

1. schema-repair micro-patch first;
2. anchor-only ablation only if the first result is ambiguous;
3. prompt-regime ablation only if ambiguity remains.

Success is defined as a clear improvement in exact JSON validity and wrapper drift without safety regression.

## Recommended Next Phase

Proceed to a dedicated schema-repair execution phase if authorized.

Do not jump directly to a broad dataset redesign until the schema patch has been tested.

## Confidence Assessment

Confidence is high that schema realization remains the most plausible remaining bottleneck.

Confidence is moderate that a 60-row patch is the smallest defensible test.

Confidence is low that a broad redesign is the best first diagnostic move for this question.

