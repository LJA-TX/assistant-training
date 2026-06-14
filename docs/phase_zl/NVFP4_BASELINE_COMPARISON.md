# NVFP4 Baseline Comparison

## Comparison Table

| Regime | Representative run | exact JSON | tool-name | arg | no-call | adversarial no-call | Reading |
|---|---|---:|---:|---:|---:|---:|---|
| Base Llama-3.1-8B-Base | Base model revalidation | `0.0` | `0.0` | `0.0` | `1.0` | `n/a` | Non-tool baseline; only no-call behavior is intact |
| H0 | `stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro` | `0.045` | `0.07142857142857142` | `0.06428571428571428` | `0.9166666666666666` | `0.75` | Low control baseline |
| H1 | `stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch` | `0.44` | `0.7142857142857143` | `0.6285714285714286` | `0.9` | `0.7` | Diversity-lift regime |
| H2 | `stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch` | `0.48` | `0.7714285714285715` | `0.6928571428571428` | `0.8` | `0.4` | Strongest exact-call regime in the repo |
| Phase Q | `stage_b_llama31_8b_base_v1_phase_q_v1_2_anchor_weighted_hybrid` | `0.03` | `0.07142857142857142` | `0.04285714285714286` | `0.7666666666666667` | `0.3` | Partial recovery, but below H0/H1/H2 and safety regresses |
| Phase U | `stage_b_llama31_8b_base_v1_phase_u_schema_repair_micro_patch` | `0.0` | `0.0` | `0.0` | `1.0` | `1.0` | Safety-preserving collapse of capability |
| Anchor sweep | `stage_b_llama31_8b_base_v1_phase_zc_treatment_c` | `0.085` | `0.2857142857142857` | `0.18571428571428572` | `0.6666666666666666` | `0.0` | Anchor concentration helps exact-call realization, but not enough |
| Topology sweep | `stage_b_llama31_8b_base_v1_phase_zj_treatment_c` | `0.04` | `0.17142857142857143` | `0.09285714285714286` | `0.6833333333333333` | `0.05` | Topology is weakened; no arm reaches the H1/H2 floor |
| NVFP4 external reference | `llama-3.1-8b-instruct-nvfp4` service-backed benchmark | `0.0` | `0.0` | `0.0` | `1.0` | `1.0` | Production-speed reference; it sits below the project-trained adapters on tool-call capability |

## What NVFP4 Adds

- It confirms that a production-speed reference model can be benchmarked on the frozen contract through the vLLM service path.
- It does not change the project ordering: H1/H2 still dominate exact tool-call recovery.
- It behaves much closer to the base-model floor than to any project-trained adapter on exact JSON, tool-name, and argument accuracy.

## Key Deltas

- Compared with H1, NVFP4 is down `0.44` on exact JSON, `0.7142857142857143` on tool-name accuracy, and `0.6285714285714286` on argument accuracy.
- Compared with H2, NVFP4 is down `0.48` on exact JSON, `0.7714285714285715` on tool-name accuracy, and `0.6928571428571428` on argument accuracy.
- Compared with Phase U, NVFP4 reaches the same aggregate exact/tool/argument floor, but its failure profile is different: it substitutes direct answers on tool-expected rows rather than collapsing into pure refusal-only behavior.

## Bottom Line

NVFP4 is a useful external reference for runtime context, but it is clearly below the project-trained adapters for tool-call capability. It does not threaten the conclusion that H1/H2 are the only high-capability regimes in the repository.

