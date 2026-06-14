# Phase ZH Completion Report

## Executive Summary

Phase ZH executed the topology Treatment A arm and completed the second governed execution point for the topology sweep.

The run is scientifically valid, contamination-clean, and operationally successful. It is **Do Not Promote**.

Treatment A does not improve on the ZG control baseline; it weakens capability and adversarial safety. The correct next step is to continue the sweep, not to promote.

## Key Findings

- The two-cluster treatment executed successfully under the frozen Phase L framework.
- Preflight passed with no manifest or dataset resolution issues.
- Training completed on the validated Phase ZF Treatment A dataset.
- Canonical evaluation completed under the frozen manifest and explicit local model-path override.
- The candidate remained contamination-clean.

## Dataset Summary

| Item | Value |
|---|---|
| Topology label | `two_cluster` |
| Train rows | `2160` |
| Val rows | `240` |
| Anchor rows | `726` |
| Long-tail rows | `667` |
| Tool-positive rows | `1393` |
| Safety rows | `767` |
| Tool families represented | `26` |

## Validation Results

- `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_zh_treatment_a.run_manifest.json`: PASS
- Training: PASS
- Canonical evaluation: PASS
- Contamination: PASS
- `git diff --check`: PASS

## Contamination Results

The Phase ZF Treatment A dataset reports zero overlap on all frozen eval surfaces, and the ZH training run did not mutate the dataset or the evaluator contract.

## Readiness Determination

**Scientifically admissible baseline, not promotable.**

The Treatment A point is valid for comparison, but it does not demonstrate recovery of the target capability.

## Risks

- The sweep may be heading toward a topology plateau rather than a recoverable capability region.
- Treatment A weakens both exact-call realization and adversarial safety relative to ZG control.
- The remaining arms are needed to rule in or out a topology effect.

## Recommended Next Phase

Proceed to **Phase ZH Treatment B**.
