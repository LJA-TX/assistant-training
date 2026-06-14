# Topology Sweep Closure Report

## Scope

This report closes the topology-ablation branch using the reviewed evidence from:

- [Phase ZG](/opt/ai-stack/assistant-training/docs/phase_zg/PHASE_ZG_CONTROL_EXECUTION_REVIEW.md)
- [Phase ZH](/opt/ai-stack/assistant-training/docs/phase_zh/PHASE_ZH_TREATMENT_A_EXECUTION_REVIEW.md)
- [Phase ZI](/opt/ai-stack/assistant-training/docs/phase_zi/PHASE_ZI_TREATMENT_B_EXECUTION_REVIEW.md)
- [Phase ZJ](/opt/ai-stack/assistant-training/docs/phase_zj/PHASE_ZJ_TREATMENT_C_EXECUTION_REVIEW.md)
- [Phase ZD](/opt/ai-stack/assistant-training/docs/phase_zd/PHASE_ZD_COMPLETION_REPORT.md)
- [Phase ZE](/opt/ai-stack/assistant-training/docs/phase_ze/PHASE_ZE_COMPLETION_REPORT.md)
- [Phase ZF](/opt/ai-stack/assistant-training/docs/phase_zf/PHASE_ZF_COMPLETION_REPORT.md)

## Sweep Record

| Arm | exact JSON | tool-name | arg | no-call | adversarial no-call | Reading |
|---|---:|---:|---:|---:|---:|---|
| ZG Control | `0.05` | `0.18571428571428572` | `0.12857142857142856` | `0.7` | `0.1` | Baseline control point |
| ZH Treatment A | `0.04` | `0.15` | `0.10714285714285714` | `0.6666666666666666` | `0.0` | Lower exact-call and safety than ZG |
| ZI Treatment B | `0.04` | `0.12142857142857143` | `0.09285714285714286` | `0.6666666666666666` | `0.0` | Further capability loss vs ZG |
| ZJ Treatment C | `0.04` | `0.17142857142857143` | `0.09285714285714286` | `0.6833333333333333` | `0.05` | Best tool-name recovery in topology sweep, but still far below H1/H2 |

## Unified Readout

The topology sweep never enters the H1/H2 regime.

- Exact JSON stays pinned near `0.04-0.05`.
- Tool-name accuracy remains in the low teens to high teens.
- Argument accuracy remains below `0.13`.
- No-call correctness never exceeds the ZG baseline.
- Adversarial no-call correctness remains weak and unstable.

The best exact-JSON point in the topology branch is ZG Control at `0.05`.
The best tool-name point is ZJ Treatment C at `0.17142857142857143`.
Neither is close to H1 or H2.

## Final Determination

**Topology is Weakened**

Topology clearly moves the metrics, but the effect is too small, too non-monotonic, and too far below H1/H2 to serve as the primary explanation for the successful H1/H2 runs.

## Rationale

1. H1/H2 remain an order of magnitude stronger on exact-call realization.
2. The topology sweep does not produce a stable monotone improvement.
3. Safety does not improve in a way that preserves a promotable tradeoff.
4. The evidence is consistent with topology being a contributor, not a sufficient cause.

## Closure Statement

The topology branch is closed.
No additional topology arm is justified by the evidence in this cycle.
