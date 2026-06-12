# Phase X Stop-Rule Clarification

## Purpose

Separate three different outcomes that can happen during the ablation.

## Definitions

### Promotion failure

The arm is scientifically valid, but it does not meet the promotable capability/safety thresholds.

Examples:

- exact JSON stays below the Phase W target,
- tool-name accuracy does not reach the H1/H2 floor,
- or safety is preserved but capability remains too weak.

Promotion failure does not invalidate the evidence.

### Attribution failure

The result can no longer be interpreted as an anchor-concentration effect because a declared fixed factor drifted.

Examples:

- contamination is nonzero,
- the exact-tool-request cue changes between arms,
- the scaffold changes,
- the canonical `tool_calls` contract changes,
- the validation/eval contract changes,
- or the safety block is rebuilt instead of preserved.

Attribution failure invalidates the experiment as a causal test.

### Operational failure

The construction or run cannot be executed cleanly.

Examples:

- a dataset synthesis script fails,
- a path does not resolve,
- preflight validation fails,
- or an arm cannot be materialized as specified.

Operational failure is a build problem, not an inference result.

## Safety Regression Rule

Safety regression alone makes an arm non-promotable, but it can still leave the capability evidence scientifically useful.

That remains true unless the regression violates a declared attribution boundary.

In other words:

- if safety drops but the scaffold, cue, contract, and contamination bounds remain fixed, the run is still informative for attribution;
- if safety drops because the fixed boundaries changed, attribution fails.

## Practical Interpretation

For Phase X:

- nonzero contamination is a hard stop and an attribution failure,
- cue or scaffold drift is a hard stop and an attribution failure,
- safety regression without boundary drift is a promotion failure,
- and build-time problems are operational failures.

This distinction matters because the experiment can still teach us something even if an arm is not promotable.

## Reference Floors

Use these frozen comparison floors when interpreting the arms:

### H1 floor

- exact JSON validity: `0.44`
- tool-name accuracy: `0.7142857142857143`
- argument accuracy: `0.6285714285714286`
- wrapper leakage: `0.0`
- no-call correctness: `1.0`
- adversarial no-call correctness: `1.0`

### H2 floor

- exact JSON validity: `0.48`
- tool-name accuracy: `0.7714285714285715`
- argument accuracy: `0.6928571428571428`
- wrapper leakage: `0.0`
- no-call correctness: `1.0`
- adversarial no-call correctness: `1.0`
