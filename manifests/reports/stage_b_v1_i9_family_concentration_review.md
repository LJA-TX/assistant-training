# Stage B i9 Family Concentration Review

- Generated UTC: 2026-05-26T20:01:31Z
- Iteration: stage_b_llama31_8b_base_v1_i9
- Targeted rows: 870
- Material families: 27

## Method
- Effective diversity uses prompt entropy, effective prompt count, prompt uniqueness, and lexical Jaccard overlap.
- Risk flags are warnings only; no hard-block decisions are made in this artifact.

## Top Largest Families
- i3_adapt_p0_read_file_1: rows=95 pct_targeted=10.91954 eff_div_ratio=0.141028 risk=2.32186
- i3_adapt_p0_rg_search_4: rows=95 pct_targeted=10.91954 eff_div_ratio=0.10296 risk=2.148756
- i3_adapt_p0_read_file_2: rows=88 pct_targeted=10.114943 eff_div_ratio=0.168184 risk=1.85088
- i3_adapt_p0_rg_search_1: rows=87 pct_targeted=10.0 eff_div_ratio=0.129508 risk=1.968306
- i3_adapt_p0_rg_search_3: rows=81 pct_targeted=9.310345 eff_div_ratio=0.118193 risk=2.006025
- i3_adapt_p0_rg_search_2: rows=79 pct_targeted=9.08046 eff_div_ratio=0.113096 risk=2.023012
- i3_adapt_p0_read_file_3: rows=72 pct_targeted=8.275862 eff_div_ratio=0.123581 risk=1.988065
- i3_adapt_p0_rg_search_5: rows=70 pct_targeted=8.045977 eff_div_ratio=0.134481 risk=1.951729
- i9_conv_nmr_i3_adapt_p0_rg_search_5: rows=14 pct_targeted=1.609195 eff_div_ratio=0.905724 risk=0.85088
- i9_conv_ssc_i3_adapt_p0_rg_search_1: rows=14 pct_targeted=1.609195 eff_div_ratio=0.905724 risk=0.744974

## Top Lowest-Diversity Families
- i3_long_rg_002: rows=13 eff_div_ratio=0.076923 entropy=0.0 semantic_var=0.0
- i3_rg_readstyle_001: rows=13 eff_div_ratio=0.076923 entropy=0.0 semantic_var=0.0
- i3_read_literal_002: rows=12 eff_div_ratio=0.083333 entropy=0.0 semantic_var=0.0
- i3_rg_readstyle_004: rows=12 eff_div_ratio=0.083333 entropy=0.0 semantic_var=0.0
- i3_read_literal_003: rows=10 eff_div_ratio=0.1 entropy=0.0 semantic_var=0.0
- i3_rg_readstyle_003: rows=10 eff_div_ratio=0.1 entropy=0.0 semantic_var=0.0
- i3_adapt_p0_rg_search_4: rows=95 eff_div_ratio=0.10296 entropy=3.290005 semantic_var=0.0
- i3_adapt_p0_rg_search_2: rows=79 eff_div_ratio=0.113096 entropy=3.159405 semantic_var=0.0
- i3_adapt_p0_rg_search_3: rows=81 eff_div_ratio=0.118193 entropy=3.259061 semantic_var=0.0
- i3_adapt_p0_read_file_3: rows=72 eff_div_ratio=0.123581 entropy=3.15345 semantic_var=0.0

## Top Concentration-Risk Families
- i3_long_rg_002: risk=2.74359 rows=13 flags=['low_effective_diversity_ratio', 'low_prompt_entropy', 'low_semantic_variation_estimate', 'high_nearest_neighbor_similarity']
- i3_rg_readstyle_001: risk=2.74359 rows=13 flags=['low_effective_diversity_ratio', 'low_prompt_entropy', 'low_semantic_variation_estimate', 'high_nearest_neighbor_similarity']
- i3_read_literal_002: risk=2.722222 rows=12 flags=['low_effective_diversity_ratio', 'low_prompt_entropy', 'low_semantic_variation_estimate', 'high_nearest_neighbor_similarity']
- i3_rg_readstyle_004: risk=2.722222 rows=12 flags=['low_effective_diversity_ratio', 'low_prompt_entropy', 'low_semantic_variation_estimate', 'high_nearest_neighbor_similarity']
- i3_read_literal_003: risk=2.666667 rows=10 flags=['low_effective_diversity_ratio', 'low_prompt_entropy', 'low_semantic_variation_estimate', 'high_nearest_neighbor_similarity']
- i3_rg_readstyle_003: risk=2.666667 rows=10 flags=['low_effective_diversity_ratio', 'low_prompt_entropy', 'low_semantic_variation_estimate', 'high_nearest_neighbor_similarity']
- i3_long_rg_001: risk=2.583333 rows=8 flags=['low_effective_diversity_ratio', 'low_prompt_entropy', 'low_semantic_variation_estimate', 'high_nearest_neighbor_similarity']
- i3_read_literal_001: risk=2.583333 rows=8 flags=['low_effective_diversity_ratio', 'low_prompt_entropy', 'low_semantic_variation_estimate', 'high_nearest_neighbor_similarity']
- i3_read_literal_004: risk=2.583333 rows=8 flags=['low_effective_diversity_ratio', 'low_prompt_entropy', 'low_semantic_variation_estimate', 'high_nearest_neighbor_similarity']
- i3_rg_readstyle_002: risk=2.52381 rows=7 flags=['low_effective_diversity_ratio', 'low_prompt_entropy', 'low_semantic_variation_estimate', 'high_nearest_neighbor_similarity']

## Memorization-Risk Interpretation
- i3_long_rg_002: memorization_prone=False semantically_diverse=False routing_diverse=False ambiguous_historically=False
  interpretation: concentration present but effective diversity indicates bounded memorization risk
- i3_rg_readstyle_001: memorization_prone=False semantically_diverse=False routing_diverse=False ambiguous_historically=False
  interpretation: concentration present but effective diversity indicates bounded memorization risk
- i3_read_literal_002: memorization_prone=False semantically_diverse=False routing_diverse=False ambiguous_historically=False
  interpretation: concentration present but effective diversity indicates bounded memorization risk
- i3_rg_readstyle_004: memorization_prone=False semantically_diverse=False routing_diverse=False ambiguous_historically=False
  interpretation: concentration present but effective diversity indicates bounded memorization risk
- i3_read_literal_003: memorization_prone=False semantically_diverse=False routing_diverse=False ambiguous_historically=False
  interpretation: concentration present but effective diversity indicates bounded memorization risk
- i3_rg_readstyle_003: memorization_prone=False semantically_diverse=False routing_diverse=False ambiguous_historically=False
  interpretation: concentration present but effective diversity indicates bounded memorization risk
- i3_long_rg_001: memorization_prone=False semantically_diverse=False routing_diverse=False ambiguous_historically=False
  interpretation: concentration present but effective diversity indicates bounded memorization risk
- i3_read_literal_001: memorization_prone=False semantically_diverse=False routing_diverse=False ambiguous_historically=False
  interpretation: concentration present but effective diversity indicates bounded memorization risk
- i3_read_literal_004: memorization_prone=False semantically_diverse=False routing_diverse=False ambiguous_historically=False
  interpretation: concentration present but effective diversity indicates bounded memorization risk
- i3_rg_readstyle_002: memorization_prone=False semantically_diverse=False routing_diverse=False ambiguous_historically=False
  interpretation: concentration present but effective diversity indicates bounded memorization risk

## Optional Cap Simulation (Read-Only)
- cap=0.20 removed=0 (0.0%) families_capped=0 entropy_delta=0.0 dilution_risk=low
- cap=0.15 removed=0 (0.0%) families_capped=0 entropy_delta=0.0 dilution_risk=low
- cap=0.12 removed=0 (0.0%) families_capped=0 entropy_delta=0.0 dilution_risk=low
- cap=0.10 removed=17 (1.954023%) families_capped=3 entropy_delta=0.016187 dilution_risk=low

