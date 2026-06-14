# Phase ZJ Treatment C Execution Review

## Executive Summary

Phase ZJ executed the final topology-ablation arm, Treatment C, under the frozen Phase L governed framework.

The run was scientifically valid, contamination-clean, and operationally successful. The result is **Do Not Promote**.

Treatment C does not recover H1/H2-style tool-call capability. It improves some surface behavior relative to ZI, but it remains far below the H1/H2 capability floor and does not justify promotion.

## Promoted Assets

- [Config](/opt/ai-stack/assistant-training/configs/lora/stage_b_llama31_8b_base_v1_phase_zj_treatment_c.config.json)
- [Run manifest](/opt/ai-stack/assistant-training/manifests/runs/stage_b_llama31_8b_base_v1_phase_zj_treatment_c.run_manifest.json)
- [Training run output](/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_phase_zj_treatment_c/)
- [Canonical eval output](/opt/ai-stack/assistant-training/evals/runs/phase_zj_treatment_c_eval_20260614T114650Z/)

## Validation Results

- Preflight manifest validation: PASS
- Dataset hash verification: PASS
- Frozen-surface verification: PASS
- Training: PASS
- Canonical evaluation: PASS
- Contamination verification: PASS
- `git diff --check`: PASS

## Dataset Summary

| Item | Value |
|---|---|
| Topology label | `fully_dispersed` |
| Train rows | `2160` |
| Val rows | `240` |
| Anchor rows | `726` |
| Long-tail rows | `667` |
| Tool-positive rows | `1393` |
| Safety rows | `767` |
| Tool families represented | `26` |

## ZJ Metrics

| Metric | ZJ |
|---|---:|
| Exact JSON validity | `0.04` |
| Tool-name accuracy | `0.17142857142857143` |
| Argument accuracy | `0.09285714285714286` |
| Wrapper leakage | `0.0` |
| No-call correctness | `0.6833333333333333` |
| Adversarial no-call correctness | `0.05` |

## Delta Summary

Compared with ZG control, ZJ is:

- slightly lower on exact JSON validity
- lower on tool-name accuracy
- lower on argument accuracy
- slightly lower on no-call correctness
- lower on adversarial no-call correctness

Compared with ZH and ZI, ZJ:

- matches the same exact JSON ceiling of `0.04`
- improves tool-name accuracy over ZH and ZI
- matches ZI on argument accuracy
- improves no-call correctness slightly over ZH and ZI
- still remains far below H1/H2

## Contamination Result

The Phase ZF Treatment C dataset reports zero overlap on all frozen evaluation surfaces, and the ZJ run did not mutate the dataset or the evaluation contract.

## Determination

**Do Not Promote**

The run is valid for analysis, but it does not demonstrate recovery of the target capability.
