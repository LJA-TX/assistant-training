# Phase Y Completion Report

## Executive Summary

Phase Y is complete.

The approved Phase X preservation ablation has been constructed as four contamination-clean arms:

- Control
- Treatment A
- Treatment B
- Treatment C

All four arms preserve the frozen scaffold, the exact-tool-request cue, the canonical `tool_calls` envelope, the safety block, and the frozen validation surface.

## Dataset Summary

| Arm | Anchor rows | Long-tail rows | Tool-positive rows | Safety rows | Status |
|---|---:|---:|---:|---:|---|
| Control | `726` | `667` | `1393` | `767` | Ready |
| Treatment A | `819` | `574` | `1393` | `767` | Ready |
| Treatment B | `912` | `481` | `1393` | `767` | Ready |
| Treatment C | `1011` | `382` | `1393` | `767` | Ready |

The validation split remains frozen at `240` rows for each arm.

## Validation Results

All four arms passed the required checks:

- contamination against heldout validation, tool holdout, no-call, adversarial, and direct-answer assets: zero overlap;
- exact tool-request cue retention: true;
- scaffold invariance: true;
- canonical `tool_calls` envelope validity: true;
- safety block preservation: true;
- all tool families represented: true.

Representative evidence is recorded in the arm readiness assessments and leakage reports under `data/v1_2/`.

## Contamination Results

No prompt overlap, target overlap, or case-id overlap was detected for train, validation, or combined splits against any frozen evaluation asset.

This means the Phase Y candidate datasets remain contamination-clean and suitable for governed execution review.

## Readiness Determination

All four arms are scientifically admissible and ready for governed execution under the existing Phase L framework.

## Risks

- The phase remains an ablation study, so capability recovery is not guaranteed by construction alone.
- The increasing anchor concentration reduces long-tail mass in the treatment arms, which may affect generalization even if capability improves.

## Recommended Next Phase

Proceed to governed execution review for the four Phase Y arms.

The evidence base is now sufficient to evaluate whether anchor concentration is the remaining bottleneck under the preserved scaffold and safety calibration.
