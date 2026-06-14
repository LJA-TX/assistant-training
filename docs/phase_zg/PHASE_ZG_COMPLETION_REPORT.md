# Phase ZG Completion Report

## Executive Summary

Phase ZG executed the topology Control arm and completed the first governed execution point for the topology sweep.

The run is scientifically valid, contamination-clean, and operationally successful. It is **Do Not Promote**.

The control arm does not recover H1/H2-level capability. It is best treated as the baseline reference for the remaining topology arms.

## Key Findings

- The compact-local control executed successfully under the frozen Phase L framework.
- Preflight passed with no manifest or dataset resolution issues.
- Training completed on the validated Phase ZF control dataset.
- Canonical evaluation completed under the frozen manifest and explicit local model-path override.
- The candidate remained contamination-clean.

## Dataset Summary

| Item | Value |
|---|---|
| Topology label | `compact_local` |
| Train rows | `2160` |
| Val rows | `240` |
| Anchor rows | `726` |
| Long-tail rows | `667` |
| Tool-positive rows | `1393` |
| Safety rows | `767` |
| Tool families represented | `26` |

## Validation Results

- `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_zg_control.run_manifest.json`: PASS
- Training: PASS
- Canonical evaluation: PASS
- Contamination: PASS
- `git diff --check`: PASS

## Contamination Results

The Phase ZF control dataset reports zero overlap on all frozen eval surfaces, and the ZG training run did not mutate the dataset or the evaluator contract.

## Readiness Determination

**Scientifically admissible baseline, not promotable.**

The control point is valid for comparison, but it does not demonstrate recovery of the target capability.

## Risks

- Treatment A may move capability only marginally.
- The exact-call surface remains weak relative to H1/H2.
- The topology sweep is still needed before any causal conclusion can be drawn.

## Recommended Next Phase

Proceed to **Phase ZG Treatment A**.
