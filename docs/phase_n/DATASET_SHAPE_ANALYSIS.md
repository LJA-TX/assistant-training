# Dataset Shape Analysis

## Executive Summary

The Phase L collapse was driven by **both**:

1. reduced tool-positive density, and
2. excessive tool-family flattening under a fixed budget.

The evidence points to **C, combination of both**, with the flattening effect being the stronger proximate cause.

Why that is the best reading:

- tool-positive density fell from `65%` in H1/H2 train data to `60%` in Dataset v1.1 train data;
- the tool-call core was flattened from a few strongly repeated anchor tools into a near-uniform 26-tool spread;
- safety rows increased, especially adversarial no-call calibration, and the model learned the refusal boundary perfectly while losing tool-call realization.

## Train-Split Density Comparison

| Dataset | Train rows | Tool-positive rows | Tool-positive density | Safety rows |
|---|---:|---:|---:|---:|
| H1 | `2160` | `1404` | `0.65` | `756` |
| H2 | `2160` | `1404` | `0.65` | `756` |
| Dataset v1.1 | `2160` | `1296` | `0.60` | `864` |

## Train-Split Delta

| Comparison | Tool-positive delta | Safety delta | Interpretation |
|---|---:|---:|---|
| v1.1 vs H1/H2 | `-108` | `+108` | The dataset traded positive tool-call signal for extra safety calibration. |

The safety increase is concentrated in the adversarial no-call slice:

- runtime_alignment stayed at `324`
- no_call_direct_calibration stayed at `216`
- refusal_calibration rose from `151` to `162`
- adversarial_no_call_calibration rose from `65` to `162`

That means most of the extra safety budget went into adversarial no-call calibration, not into the ordinary no-call or runtime-alignment slices.

## Why This Matters

The Phase L model did not just get "more safe."
It got more selective about refusing and less capable of producing the canonical tool-call envelope.

That pattern is consistent with a dataset that is:

- too safety-heavy for the fixed budget,
- too evenly spread across tool families,
- and too light on repeated canonical tool-call anchors.

## Bottom-Line Answer

The correct answer is **C**.

If forced to rank the two components:

- **B is the stronger proximate cause** of the exact-validity collapse.
- **A is the enabling cause** that reduced the tool-call signal floor.

## Sources Used

- `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_summary.json`
- `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_summary.json`
- `data/v1_1/dataset_v1_1_summary.json`
- `docs/phase_l/PHASE_L_EXECUTION_REVIEW.md`
- `docs/phase_m/FAILURE_CHARACTERIZATION.md`
