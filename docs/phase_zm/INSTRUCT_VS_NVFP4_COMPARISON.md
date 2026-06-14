# Instruct vs NVFP4 Comparison

## Comparison Table

| Regime | Representative run | exact JSON | tool-name | arg | invalid JSON | wrapper leakage | no-call | adversarial no-call | Reading |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| Base Llama-3.1-8B-Base | Base model revalidation | `0.0` | `0.0` | `0.0` | `0.7` | `0.0` | `1.0` | `n/a` | Non-tool baseline; only no-call behavior is intact |
| Instruct external reference | `llama-3.1-8b-instruct` canonical run | `0.0` | `0.0` | `0.0` | `0.69` | `0.0` | `1.0` | `1.0` | Direct-load baseline; same exact-call floor as NVFP4 |
| NVFP4 external reference | `llama-3.1-8b-instruct-nvfp4` service-backed benchmark | `0.0` | `0.0` | `0.0` | `0.695` | `0.0` | `1.0` | `1.0` | Production-speed reference; same exact-call floor as Instruct |
| H0 | `stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro` | `0.045` | `0.07142857142857142` | `0.06428571428571428` | `n/a` | `n/a` | `0.9166666666666666` | `0.75` | Low control baseline |
| H1 | `stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch` | `0.44` | `0.7142857142857143` | `0.6285714285714286` | `n/a` | `n/a` | `0.9` | `0.7` | Diversity-lift regime |
| H2 | `stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch` | `0.48` | `0.7714285714285715` | `0.6928571428571428` | `n/a` | `n/a` | `0.8` | `0.4` | Strongest exact-call regime in the repo |
| Phase Q | `stage_b_llama31_8b_base_v1_phase_q_v1_2_anchor_weighted_hybrid` | `0.03` | `0.07142857142857142` | `0.04285714285714286` | `n/a` | `n/a` | `0.7666666666666667` | `0.3` | Partial recovery, but below H0/H1/H2 and safety regresses |
| Phase U | `stage_b_llama31_8b_base_v1_phase_u_schema_repair_micro_patch` | `0.0` | `0.0` | `0.0` | `n/a` | `n/a` | `1.0` | `1.0` | Safety-preserving collapse of capability |
| Anchor sweep | `stage_b_llama31_8b_base_v1_phase_zc_treatment_c` | `0.085` | `0.2857142857142857` | `0.18571428571428572` | `n/a` | `n/a` | `0.6666666666666666` | `0.0` | Anchor concentration helps exact-call realization, but not enough |
| Topology sweep | `stage_b_llama31_8b_base_v1_phase_zj_treatment_c` | `0.04` | `0.17142857142857143` | `0.09285714285714286` | `n/a` | `n/a` | `0.6833333333333333` | `0.05` | Topology is weakened; no arm reaches the H1/H2 floor |

## Interpretation

The Instruct and NVFP4 baselines are behaviorally indistinguishable at the aggregate level that matters for the frozen contract:

- both have `0.0` exact JSON validity
- both have `0.0` tool-name accuracy
- both have `0.0` argument accuracy
- both have `1.0` no-call correctness
- both have `1.0` adversarial no-call correctness

The only differences are minor row-level failure-count variations:

- Instruct: `invalid_json=0.69`, `malformed_partial_json=5`, `near_canonical_wrapper_or_envelope_drift=2`
- NVFP4: `invalid_json=0.695`, `malformed_partial_json=6`, `near_canonical_wrapper_or_envelope_drift=1`

Those deltas are too small to support a meaningful behavior ranking.

## Conclusion

Classification: **behaviorally equivalent**

The evidence points to the NVFP4 result reflecting the underlying Instruct model behavior on this frozen contract, not a material quantization effect. Backend differences may still affect minor failure counts, but they do not change the aggregate conclusion.

