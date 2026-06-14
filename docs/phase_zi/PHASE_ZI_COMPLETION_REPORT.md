# Phase ZI Completion Report

## Executive Summary

Phase ZI executed the topology Treatment B arm and completed the third governed execution point for the topology sweep.

The run is scientifically valid, contamination-clean, and operationally successful. It is **Do Not Promote**.

Treatment B does not improve on the ZG control baseline and does not improve on ZH Treatment A. The correct next step is to continue the sweep to Treatment C, not to promote.

## Key Findings

- The four-cluster treatment executed successfully under the frozen Phase L framework.
- Preflight passed with no manifest or dataset resolution issues.
- Dataset hashes matched the Phase ZF summary exactly.
- Training completed on the validated Phase ZF Treatment B dataset.
- Canonical evaluation completed under the frozen manifest and explicit local model-path override.
- The candidate remained contamination-clean.

## Dataset Summary

| Item | Value |
|---|---|
| Topology label | `four_cluster` |
| Train rows | `2160` |
| Val rows | `240` |
| Anchor rows | `726` |
| Long-tail rows | `667` |
| Tool-positive rows | `1393` |
| Safety rows | `767` |
| Tool families represented | `26` |

## Validation Results

- `python scripts/preflight_lora_run.py manifests/runs/stage_b_llama31_8b_base_v1_phase_zi_treatment_b.run_manifest.json`: PASS
- Training: PASS
- Canonical evaluation: PASS
- Contamination: PASS
- `git diff --check`: PASS

## Contamination Results

The Phase ZF Treatment B dataset reports zero overlap on all frozen eval surfaces, and the ZI training run did not mutate the dataset or the evaluator contract.

## Readiness Determination

**Scientifically admissible baseline, not promotable.**

The Treatment B point is valid for comparison, but it does not demonstrate recovery of the target capability.

## Risks

- The sweep appears to be trending downward in tool-call quality as topology becomes less local.
- Safety remains unstable on the adversarial no-call surface.
- Treatment C is still required to determine whether there is any non-monotonic response.

## Recommended Next Phase

Proceed to **Phase ZI Treatment C**.
