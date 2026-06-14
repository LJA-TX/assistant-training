# Phase ZL Completion Report

## Executive Summary

The NVFP4 external reference model was benchmarked against the frozen canonical evaluation contract using the production vLLM service path. The frozen manifest, prompt serialization, decode defaults, and scoring logic were preserved. The service-backed benchmark completed cleanly and produced a stable external reference baseline.

## Key Findings

- The model is service-available through the production vLLM stack at `http://127.0.0.1:8012`.
- The local Transformers load path is not usable for this checkpoint in the frozen canonical evaluator.
- The benchmark outcome is weak on every positive tool-call metric: exact JSON validity, tool-name accuracy, and argument accuracy are all `0.0`.
- Safety-style no-call behavior is intact at `1.0`, but that is not a tool-use recovery signal.
- The dominant failure mode is direct-answer substitution on tool-expected rows.

## External Reference Assessment

Classification: **below project-trained adapters**

This result is consistent with NVFP4 being a production-speed reference model rather than a tool-use specialist. It sits near the base-model floor on exact-call metrics and remains far below H1/H2.

## Project Context

- H1 and H2 remain the only clear high-capability regimes for exact tool-call recovery.
- Phase Q, Phase U, the anchor sweep, and the topology sweep all remain below H1/H2.
- NVFP4 adds runtime context, but it does not change the causal interpretation of the project-trained adapters.

## Recommended Next Action

Treat NVFP4 as an external reference only. Do not fold it into the causal intervention chain. Continue project reasoning from the H1/H2 adapter regimes and the later ablation results.

## Confidence Assessment

High confidence on the classification. The benchmark used the frozen contract and persisted artifacts, and the aggregate metrics are unambiguous.

