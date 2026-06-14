# Project-Wide Baseline Comparison

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

## Best-Performing Runs

- Best exact JSON validity: H2 at `0.48`.
- Best tool-name accuracy: H2 at `0.7714285714285715`.
- Best argument accuracy: H2 at `0.6928571428571428`.
- Best no-call correctness: Base model and Phase U at `1.0`.
- Best adversarial no-call correctness: Phase U at `1.0`.

## Major Capability Regimes

### Raw base / collapse floor

The base model and Phase L show that the frozen canonical contract is not satisfied without specialized intervention.

### Diversity / commitment recovery

H1 and H2 establish the only clear high-capability regime in the repository.

### Anchor-weighted partial recovery

Phase Q, Phase ZC, and the Z-series show that anchor concentration helps, but it does not reproduce H1/H2 by itself.

### Schema-preserving collapse

Phase U preserves safety but loses capability completely.

### Topology refinement failure

The ZG-ZJ sweep changes the shape of the failure, but not enough to recreate H1/H2-level exact-call behavior.

## Bottom Line

The repository has one clear high-capability region:

- H1/H2 on the frozen recovery scaffold.

Everything else is either partial recovery, safety-preserving collapse, or a weakened variant of the same failure family.
