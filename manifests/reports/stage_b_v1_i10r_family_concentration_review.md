# Stage B i10 Family Concentration Review

- Generated UTC: 2026-05-27T13:13:22Z
- Iteration: stage_b_llama31_8b_base_v1_i10r
- Targeted rows: 601
- Material families: 27

## Method
- Effective diversity uses prompt entropy, effective prompt count, prompt uniqueness, and lexical Jaccard overlap.
- Risk flags are warnings only; no hard-block decisions are made in this artifact.

## Top Largest Families
- i3_adapt_p0_read_file_1: rows=52 pct_targeted=8.652246 eff_div_ratio=0.240489 risk=1.893975
- i3_adapt_p0_rg_search_4: rows=52 pct_targeted=8.652246 eff_div_ratio=0.18231 risk=1.7923
- i3_adapt_p0_read_file_2: rows=48 pct_targeted=7.986689 eff_div_ratio=0.290307 risk=1.427901
- i3_adapt_p0_rg_search_1: rows=48 pct_targeted=7.986689 eff_div_ratio=0.205527 risk=1.71005
- i3_adapt_p0_rg_search_3: rows=45 pct_targeted=7.487521 eff_div_ratio=0.209468 risk=1.701774
- i3_adapt_p0_rg_search_2: rows=43 pct_targeted=7.154742 eff_div_ratio=0.18657 risk=1.767862
- i3_adapt_p0_read_file_3: rows=40 pct_targeted=6.655574 eff_div_ratio=0.228125 risk=1.634293
- i3_adapt_p0_rg_search_5: rows=39 pct_targeted=6.489185 eff_div_ratio=0.237046 risk=1.609847
- i9_conv_nmr_i3_adapt_p0_rg_search_5: rows=14 pct_targeted=2.329451 eff_div_ratio=0.905724 risk=0.85088
- i9_conv_ssc_i3_adapt_p0_rg_search_1: rows=14 pct_targeted=2.329451 eff_div_ratio=0.905724 risk=0.744974

## Top Lowest-Diversity Families
- i3_adapt_p0_rg_search_4: rows=52 eff_div_ratio=0.18231 entropy=3.244904 semantic_var=0.0
- i3_adapt_p0_rg_search_2: rows=43 eff_div_ratio=0.18657 entropy=3.004056 semantic_var=0.003583
- i3_adapt_p0_rg_search_1: rows=48 eff_div_ratio=0.205527 entropy=3.302361 semantic_var=0.001701
- i3_adapt_p0_rg_search_3: rows=45 eff_div_ratio=0.209468 entropy=3.236654 semantic_var=0.0
- i3_adapt_p0_read_file_3: rows=40 eff_div_ratio=0.228125 entropy=3.189823 semantic_var=0.001852
- i3_adapt_p0_rg_search_5: rows=39 eff_div_ratio=0.237046 entropy=3.20864 semantic_var=0.0
- i3_adapt_p0_read_file_1: rows=52 eff_div_ratio=0.240489 entropy=3.644481 semantic_var=0.001538
- i3_adapt_p0_read_file_2: rows=48 eff_div_ratio=0.290307 entropy=3.800614 semantic_var=0.001543
- i10_conv_ssc_rf_i9_conv_ssc_i3_adapt_p0_read_file_1: rows=5 eff_div_ratio=0.757858 entropy=1.921928 semantic_var=0.144516
- i9_conv_ssc_i3_adapt_p0_rg_search_3: rows=11 eff_div_ratio=0.777203 entropy=3.095795 semantic_var=0.162734

## Top Concentration-Risk Families
- i3_adapt_p0_read_file_1: risk=1.893975 rows=52 flags=['low_effective_diversity_ratio', 'low_semantic_variation_estimate', 'high_nearest_neighbor_similarity', 'prior_ambiguity_involvement', 'multi_tool_lineage_history', 'ambiguity_remediation_applied']
- i3_adapt_p0_rg_search_4: risk=1.7923 rows=52 flags=['low_effective_diversity_ratio', 'low_semantic_variation_estimate', 'high_nearest_neighbor_similarity', 'prior_ambiguity_involvement']
- i3_adapt_p0_rg_search_2: risk=1.767862 rows=43 flags=['low_effective_diversity_ratio', 'low_semantic_variation_estimate', 'high_nearest_neighbor_similarity', 'prior_ambiguity_involvement']
- i3_adapt_p0_rg_search_1: risk=1.71005 rows=48 flags=['low_effective_diversity_ratio', 'low_semantic_variation_estimate', 'high_nearest_neighbor_similarity', 'prior_ambiguity_involvement']
- i3_adapt_p0_rg_search_3: risk=1.701774 rows=45 flags=['low_effective_diversity_ratio', 'low_semantic_variation_estimate', 'high_nearest_neighbor_similarity', 'prior_ambiguity_involvement']
- i3_adapt_p0_read_file_3: risk=1.634293 rows=40 flags=['low_effective_diversity_ratio', 'low_semantic_variation_estimate', 'high_nearest_neighbor_similarity', 'prior_ambiguity_involvement']
- i3_adapt_p0_rg_search_5: risk=1.609847 rows=39 flags=['low_effective_diversity_ratio', 'low_semantic_variation_estimate', 'high_nearest_neighbor_similarity', 'prior_ambiguity_involvement']
- i3_adapt_p0_read_file_2: risk=1.427901 rows=48 flags=['low_effective_diversity_ratio', 'low_semantic_variation_estimate', 'high_nearest_neighbor_similarity', 'prior_ambiguity_involvement']
- i9_conv_nmr_i3_adapt_p0_rg_search_5: risk=0.85088 rows=14 flags=['low_semantic_variation_estimate', 'high_nearest_neighbor_similarity']
- i9_conv_ucf_i3_adapt_p0_read_file_3: risk=0.790928 rows=10 flags=['low_semantic_variation_estimate', 'high_nearest_neighbor_similarity']

## Memorization-Risk Interpretation
- i3_adapt_p0_read_file_1: memorization_prone=False semantically_diverse=False routing_diverse=True ambiguous_historically=True
  interpretation: concentration present but effective diversity indicates bounded memorization risk
- i3_adapt_p0_rg_search_4: memorization_prone=False semantically_diverse=False routing_diverse=False ambiguous_historically=True
  interpretation: concentration present but effective diversity indicates bounded memorization risk
- i3_adapt_p0_rg_search_2: memorization_prone=False semantically_diverse=False routing_diverse=False ambiguous_historically=True
  interpretation: concentration present but effective diversity indicates bounded memorization risk
- i3_adapt_p0_rg_search_1: memorization_prone=False semantically_diverse=False routing_diverse=False ambiguous_historically=True
  interpretation: concentration present but effective diversity indicates bounded memorization risk
- i3_adapt_p0_rg_search_3: memorization_prone=False semantically_diverse=False routing_diverse=False ambiguous_historically=True
  interpretation: concentration present but effective diversity indicates bounded memorization risk
- i3_adapt_p0_read_file_3: memorization_prone=False semantically_diverse=False routing_diverse=False ambiguous_historically=True
  interpretation: concentration present but effective diversity indicates bounded memorization risk
- i3_adapt_p0_rg_search_5: memorization_prone=False semantically_diverse=False routing_diverse=False ambiguous_historically=True
  interpretation: concentration present but effective diversity indicates bounded memorization risk
- i3_adapt_p0_read_file_2: memorization_prone=False semantically_diverse=False routing_diverse=False ambiguous_historically=True
  interpretation: concentration present but effective diversity indicates bounded memorization risk
- i9_conv_nmr_i3_adapt_p0_rg_search_5: memorization_prone=False semantically_diverse=False routing_diverse=False ambiguous_historically=False
  interpretation: concentration present but effective diversity indicates bounded memorization risk
- i9_conv_ucf_i3_adapt_p0_read_file_3: memorization_prone=False semantically_diverse=False routing_diverse=False ambiguous_historically=False
  interpretation: concentration present but effective diversity indicates bounded memorization risk

## Optional Cap Simulation (Read-Only)
- cap=0.20 removed=0 (0.0%) families_capped=0 entropy_delta=0.0 dilution_risk=low
- cap=0.15 removed=0 (0.0%) families_capped=0 entropy_delta=0.0 dilution_risk=low
- cap=0.12 removed=0 (0.0%) families_capped=0 entropy_delta=0.0 dilution_risk=low
- cap=0.10 removed=0 (0.0%) families_capped=0 entropy_delta=0.0 dilution_risk=low

