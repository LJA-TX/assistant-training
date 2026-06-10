# Baseline Delta Assessment

## Scope

Compare the fresh base-model revalidation against the fresh i3-adapter revalidation.
Do not evaluate promotion.
Do not recommend promotion.

## Inputs

- [evals/runs/phase_e_base_revalidation_20260610_r1/summary.json](../../evals/runs/phase_e_base_revalidation_20260610_r1/summary.json)
- [evals/runs/phase_e_i3_revalidation_20260610_r1/summary.json](../../evals/runs/phase_e_i3_revalidation_20260610_r1/summary.json)
- [docs/appendix_a_operational_execution_contract_v3a.md](../appendix_a_operational_execution_contract_v3a.md)

## Delta Results

| Metric | Base | i3 | Delta |
|---|---:|---:|---:|
| Exact JSON validity | 0.0 | 0.025 | +0.025 |
| Invalid JSON rate | 0.7 | 0.28 | -0.42 |
| Tool-name accuracy | 0.0 | 0.03571428571428571 | +0.03571428571428571 |
| Argument accuracy | 0.0 | 0.03571428571428571 | +0.03571428571428571 |
| Wrapper leakage rate | 0.0 | 0.0 | 0.0 |
| No-call correctness | 1.0 | 1.0 | 0.0 |

## Appendix A Gate Comparison

| Gate item | Threshold | Fresh delta | Result |
|---|---:|---:|---|
| Held-out exact JSON validity improvement | +10 percentage points | +2.5 percentage points | Fail |
| Held-out tool-name accuracy improvement | +5 percentage points | +3.57 percentage points | Fail |
| Invalid JSON decrease | Required | Yes | Pass |
| Wrapper leakage not worse by more than 5pp | Required | Yes | Pass |
| No-call correctness not degraded by more than 10pp | Required | Yes | Pass |

## Baseline Reality

The i3 adapter is better than the base model, but it does not meet the minimum-promising Appendix A thresholds.

The most important preserved property is that no-call correctness remains perfect.

## Determination

The fresh delta confirms a real improvement in structured-output behavior, but not enough improvement to change the baseline classification.

## Boundary Confirmation

This assessment does not recommend promotion.
