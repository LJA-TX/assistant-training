# Phase ZM Completion Report

## Executive Summary

The non-quantized Llama-3.1-8B-Instruct model was benchmarked directly against the frozen canonical evaluation contract. The model loaded successfully through the frozen project evaluator, so no fallback service path was required.

## Key Findings

- The model path is compatible with the frozen canonical evaluator.
- The benchmark completed on the local harness with preserved manifest, prompt rendering, decode defaults, scorer logic, and thresholds.
- Aggregate tool-call performance is at the frozen floor: exact JSON validity, tool-name accuracy, and argument accuracy are all `0.0`.
- No-call behavior is intact at `1.0`, including adversarial no-call correctness.
- The dominant failure mode is direct-answer substitution.

## Comparison to NVFP4

The Instruct and NVFP4 external references are behaviorally equivalent at the aggregate level. The NVFP4 result therefore appears to reflect the underlying Instruct behavior, not a meaningful quantization-induced shift.

## Project Context

- Both external references sit far below H1/H2 and do not enter the causal intervention chain.
- The project-trained adapter regimes remain the only high-capability tool-call results.

## Recommended Next Action

Treat both Instruct and NVFP4 as external reference baselines only. Continue project analysis from the adapter and ablation results rather than from the raw base-family models.

