# Training Run History

Status: living log.

This document records completed training runs from the beginning of the project onward.
It is intended to be updated at the end of each completed training run.
External reference baselines are tracked separately and do not count toward the canonical-eval/probe totals.

## Split Definition

- Canonical-eval runs are scored on the frozen canonical evaluation contract, or on an explicitly documented canonical completion report when the persisted `evals/runs/` summary is absent.
- Probe-only runs are diagnostic runs whose published result is not scored on the frozen canonical contract.
- Run names containing `probe` are not automatically probe-only.

## Split Summary

| Split | Count | Best exact JSON | Best run |
|---|---:|---:|---|
| Canonical-eval | 30 | 48.0% | **stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch** |
| Probe-only | 1 | 5.0% | `lora_probe_llama_3_2_3b_instruct_toolcall_v0_1` |

## Most Successful

Most successful overall by the ranking rule below:

- **stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch**
- exact JSON validity: `48.0%`
- tool-name accuracy: `77.1%`
- argument accuracy: `69.3%`
- no-call correctness: `80.0%`

Ranking rule:

1. Highest exact JSON validity.
2. Then highest argument accuracy.
3. Then highest tool-name accuracy.
4. Then lower eval loss.

## Canonical-Eval Runs

| Date (UTC) | Run | Train/Val | Train loss | Eval loss | Exact JSON | Tool name | Arg | No-call | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 2026-05-26 01:28:38 UTC | `stage_a_llama31_8b_base_v1_i1` | 2160/240 | 0.308 | 0.138 | 1.5% | 5.7% | 2.1% | 100.0% | Stage A baseline. |
| 2026-05-26 01:51:53 UTC | `stage_b_llama31_8b_base_v1_i1` | 2160/240 | 0.273 | 0.620 | 1.0% | 2.9% | 5.7% | 100.0% | Early stage-B iteration. |
| 2026-05-26 02:41:10 UTC | `stage_b_llama31_8b_base_v1_i2` | 2160/240 | 0.238 | 0.055 | 35.0% | 50.0% | 50.0% | 100.0% | Early stage-B iteration. |
| 2026-05-26 10:20:31 UTC | `stage_b_llama31_8b_base_v1_i4` | 2160/240 | 0.210 | 0.020 | 0.0% | 0.0% | 0.0% | 100.0% | Early stage-B iteration. |
| 2026-05-26 11:03:58 UTC | `stage_b_llama31_8b_base_v1_i5` | 2160/240 | 0.287 | 0.020 | 0.0% | 0.0% | 0.0% | 100.0% | Early stage-B iteration. |
| 2026-05-26 11:35:32 UTC | `stage_b_llama31_8b_base_v1_i6` | 2160/240 | 0.293 | 0.025 | 0.5% | 0.7% | 0.7% | 100.0% | Early stage-B iteration. |
| 2026-05-26 12:06:02 UTC | `stage_b_llama31_8b_base_v1_i7` | 2160/240 | 0.288 | 0.025 | 0.0% | 0.0% | 0.0% | 100.0% | Early stage-B iteration. |
| 2026-05-26 17:41:01 UTC | `stage_b_llama31_8b_base_v1_i8` | 2129/240 | 0.271 | 0.041 | 2.0% | 2.9% | 2.9% | 100.0% | Early stage-B iteration. |
| 2026-05-26 23:33:54 UTC | `stage_b_llama31_8b_base_v1_i9` | 2217/254 | 0.275 | 0.018 | 7.5% | 12.9% | 10.7% | 100.0% | Early stage-B iteration. |
| 2026-05-27 13:55:05 UTC | `stage_b_llama31_8b_base_v1_i10r_microprobe` | 1969/233 | 0.538 | 0.357 | 43.5% | 70.0% | 65.0% | 91.7% | High-capability probe run that still used the frozen canonical contract. |
| 2026-05-27 18:52:27 UTC | `stage_b_llama31_8b_base_v1_i10r_nocall_probe` | 1983/235 | 0.566 | 0.384 | 37.0% | 62.1% | 52.9% | 100.0% | Canonical-eval probe variant. |
| 2026-05-28 16:03:07 UTC | `stage_b_llama31_8b_base_v1_i10r_counterbalanced_probe` | 1982/236 | 0.573 | 0.429 | 46.0% | 67.9% | 65.7% | 96.7% | Canonical-eval probe variant. |
| 2026-05-28 17:10:14 UTC | `stage_b_llama31_8b_base_v1_i10r_residual_nocall_probe` | 1986/238 | 0.529 | 0.522 | 40.5% | 69.3% | 59.3% | 100.0% | Canonical-eval probe variant. |
| 2026-05-29 16:36:15 UTC | `stage_b_llama31_8b_base_v1_geometry_probe_mh` | 1982/236 | 0.345 | 1.731 | 21.0% | 40.0% | 48.6% | 93.3% | Geometry probe run. |
| 2026-06-03 13:01:50 UTC | `stage_b_llama31_8b_base_v1_geometry_probe_lh` | 1982/236 | 0.355 | 1.767 | 12.0% | 34.3% | 33.6% | 73.3% | Geometry probe run. |
| 2026-06-10 22:02:25 UTC | `stage_b_llama31_8b_base_v1_i3` | 2160/240 | 0.301 | 0.026 | 2.5% | 3.6% | 3.6% | 100.0% | Early stage-B iteration. |
| 2026-06-11 10:30:53 UTC | `stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro` | 2160/240 | 0.519 | 0.393 | 4.5% | 7.1% | 6.4% | 91.7% | Phase I hypothesis sweep. |
| 2026-06-11 12:02:39 UTC | **stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch** | 2160/240 | 0.595 | 0.429 | 48.0% | 77.1% | 69.3% | 80.0% | Most successful run. |
| 2026-06-11 13:02:09 UTC | `stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch` | 2160/240 | 0.526 | 0.413 | 44.0% | 71.4% | 62.9% | 90.0% | Phase I hypothesis sweep. |
| 2026-06-11 15:41:45 UTC | `stage_b_llama31_8b_base_v1_phase_l_v1_1_external_first` | 2160/240 | 0.875 | 0.542 | 0.0% | 4.3% | 0.7% | 100.0% | Strong training fit, but poor canonical exact-tool performance. |
| 2026-06-12 10:13:26 UTC | `stage_b_llama31_8b_base_v1_phase_q_v1_2_anchor_weighted_hybrid` | 2160/240 | 0.732 | 0.434 | 3.0% | 7.1% | 4.3% | 76.7% | First governed dataset v1.2 run. |
| 2026-06-12 11:19:54 UTC | `stage_b_llama31_8b_base_v1_phase_u_schema_repair_micro_patch` | 60/240 | 2.057 | 2.576 | 0.0% | 0.0% | 0.0% | 100.0% | Schema repair collapsed tool-call capability. |
| 2026-06-13 00:23:44 UTC | `stage_b_llama31_8b_base_v1_phase_z_control` | 2160/240 | 0.719 | 0.528 | 5.5% | 20.0% | 13.6% | 66.7% | Topology sweep run. |
| 2026-06-13 00:50:40 UTC | `stage_b_llama31_8b_base_v1_phase_za_treatment_a` | 2160/240 | 0.662 | 0.524 | 7.0% | 21.4% | 15.0% | 73.3% | Topology sweep run. |
| 2026-06-13 21:02:28 UTC | `stage_b_llama31_8b_base_v1_phase_zb_treatment_b` | 2160/240 | 0.663 | 0.536 | 7.0% | 21.4% | 15.0% | 73.3% | Recorded date comes from the run manifest; canonical-eval metrics are recorded in the Phase ZB completion report because no persisted `evals/runs/` summary was present. |
| 2026-06-13 21:31:32 UTC | `stage_b_llama31_8b_base_v1_phase_zc_treatment_c` | 2160/240 | 0.658 | 0.584 | 8.5% | 28.6% | 18.6% | 66.7% | Topology sweep run. |
| 2026-06-13 23:21:53 UTC | `stage_b_llama31_8b_base_v1_phase_zg_control` | 2160/240 | 0.730 | 0.520 | 5.0% | 18.6% | 12.9% | 70.0% | Topology sweep run. |
| 2026-06-13 23:49:17 UTC | `stage_b_llama31_8b_base_v1_phase_zh_treatment_a` | 2160/240 | 0.717 | 0.514 | 4.0% | 15.0% | 10.7% | 66.7% | Topology sweep run. |
| 2026-06-14 11:17:54 UTC | `stage_b_llama31_8b_base_v1_phase_zi_treatment_b` | 2160/240 | 0.717 | 0.496 | 4.0% | 12.1% | 9.3% | 66.7% | Topology sweep run. |
| 2026-06-14 11:51:11 UTC | `stage_b_llama31_8b_base_v1_phase_zj_treatment_c` | 2160/240 | 0.730 | 0.518 | 4.0% | 17.1% | 9.3% | 68.3% | Topology sweep run. |

## Probe-Only Runs

| Date (UTC) | Run | Train/Val | Train loss | Eval loss | Exact JSON | Tool name | Arg | No-call | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 2026-05-05 00:17:53 UTC | `lora_probe_llama_3_2_3b_instruct_toolcall_v0_1` | 162/40 | 1.827 | 1.821 | 5.0% | 0.0% | 0.0% | n/a | Headline metric uses the strong-prompt validation eval. The earlier minimum and train40 evals were `0.0%` exact. |

## External Reference Baselines

| Date (UTC) | Reference | Train/Val | Train loss | Eval loss | Exact JSON | Tool name | Arg | No-call | Adversarial no-call | Notes |
|---|---|---|---|---|---:|---:|---:|---:|---:|---|
| 2026-06-14 13:10:06 UTC | `llama-3.1-8b-instruct-nvfp4` external reference | `n/a` | `n/a` | `n/a` | `0.0%` | `0.0%` | `0.0%` | `100.0%` | `100.0%` | Service-backed canonical-manifest benchmark; the HF Transformers load path failed, so the frozen contract was executed through the production vLLM stack. |
| 2026-06-14 13:34:54 UTC | `llama-3.1-8b-instruct` external reference | `n/a` | `n/a` | `n/a` | `0.0%` | `0.0%` | `0.0%` | `100.0%` | `100.0%` | Direct canonical-manifest benchmark on the frozen local harness; the non-quantized model loaded successfully with no fallback path. |

## Published Llama 3.1 Evidence Package

- Landing page: [../baselines/README.md](../baselines/README.md)
- Project-wide comparison: [../baselines/LLAMA31_PROJECT_WIDE_COMPARISON.md](../baselines/LLAMA31_PROJECT_WIDE_COMPARISON.md)
- Machine-readable package root: [../../../evals/baselines/llama31/README.md](../../../evals/baselines/llama31/README.md)
- The curated package includes the authoritative Base revalidation baseline, the Instruct and NVFP4 external references, and H1/H2 as internal reference regimes.

## Source Notes

- Canonical-eval source runs, the Phase ZB completion report, and probe-only artifact outputs are generated/private provenance intentionally omitted from this curated package; see the [public-reference disposition metadata](../../publication/public_reference_dispositions.json).

## Update Rule

1. Append new completed runs in chronological order.
2. Keep canonical and probe-only sections separate.
3. If a later canonical run overtakes the current leader on the ranking rule, bold it in the canonical section and update the split summary.
4. Use the canonical evaluation summary when present.
5. Use a phase completion report only when the persisted canonical eval summary is absent.
