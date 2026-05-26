# Stage B i8 Surgical Rebalance Post-Remediation Review

- Iteration: `stage_b_llama31_8b_base_v1_i8`
- Generated: `2026-05-26T17:09:27Z`
- Proposal: `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i8_surgical_rebalance_proposal.json`

## Required Verification Answers
- `1_trim_executed_exactly_as_specified`: `True`
- `2_any_preservation_constraints_failed`: `False`
- `3_any_ambiguity_hard_blocks_regressed`: `False`
- `4_any_concentration_metrics_worsened_unexpectedly`: `False`
- `5_any_style_bucket_distribution_shift_material`: `False`
- `6_any_skeleton_concentration_metrics_regressed`: `False`
- `7_top_concentration_families_reached_intended_cap_equivalent_regime`: `True`
- `8_any_families_still_materially_memorization_prone`: `False`
- `9_dataset_suitable_for_bounded_training_execution_review`: `True`

## Before / After Comparison
| Metric | Before | After | Delta |
|---|---:|---:|---:|
| Targeted row count | 799 | 768 | -31 |
| Family entropy | 3.564487 | 3.592267 | 0.02778 |
| Prompt uniqueness ratio (targeted) | 0.128911 | 0.134115 | 0.005204 |
| Top-1 skeleton share (targeted) | 0.052566 | 0.050781 | -0.001785 |
| i3_adapt_p0_read_file_1 eff-div ratio | 0.115462 | 0.141028 | 0.025566 |
| i3_adapt_p0_rg_search_4 eff-div ratio | 0.097658 | 0.10296 | 0.005302 |

### Top Family Shares (Targeted)
- Before:
  - i3_adapt_p0_read_file_1: 122 rows (15.269086%)
  - i3_adapt_p0_rg_search_4: 99 rows (12.390488%)
  - i3_adapt_p0_read_file_2: 88 rows (11.013767%)
  - i3_adapt_p0_rg_search_1: 87 rows (10.888611%)
  - i3_adapt_p0_rg_search_3: 81 rows (10.137672%)
- After:
  - i3_adapt_p0_read_file_1: 95 rows (12.369792%)
  - i3_adapt_p0_rg_search_4: 95 rows (12.369792%)
  - i3_adapt_p0_read_file_2: 88 rows (11.458333%)
  - i3_adapt_p0_rg_search_1: 87 rows (11.328125%)
  - i3_adapt_p0_rg_search_3: 81 rows (10.546875%)

### Ambiguity Counts
- Before: {'duplicate_prompt_groups_different_target_count': 0, 'duplicate_prompt_groups_different_tool_count': 0, 'duplicate_prompt_tool_groups_different_arguments_count': 0}
- After: {'duplicate_prompt_groups_different_target_count': 0, 'duplicate_prompt_groups_different_tool_count': 0, 'duplicate_prompt_tool_groups_different_arguments_count': 0}

### Contamination Counts (Combined)
- Before: {'heldout_validation': {'prompt_overlap': 0, 'target_overlap': 0, 'source_case_id_overlap': 0}, 'tool_holdout': {'prompt_overlap': 0, 'target_overlap': 0, 'source_case_id_overlap': 0}, 'no_call': {'prompt_overlap': 0, 'target_overlap': 6, 'source_case_id_overlap': 0}, 'adversarial': {'prompt_overlap': 0, 'target_overlap': 4, 'source_case_id_overlap': 0}, 'direct_answer': {'prompt_overlap': 0, 'target_overlap': 0, 'source_case_id_overlap': 0}}
- After: {'heldout_validation': {'prompt_overlap': 0, 'target_overlap': 0, 'source_case_id_overlap': 0}, 'tool_holdout': {'prompt_overlap': 0, 'target_overlap': 0, 'source_case_id_overlap': 0}, 'no_call': {'prompt_overlap': 0, 'target_overlap': 6, 'source_case_id_overlap': 0}, 'adversarial': {'prompt_overlap': 0, 'target_overlap': 4, 'source_case_id_overlap': 0}, 'direct_answer': {'prompt_overlap': 0, 'target_overlap': 0, 'source_case_id_overlap': 0}}

### Style Bucket Deltas (Targeted)
- imperative_general: 350 -> 346 (delta -4)
- imperative_line_scoped: 387 -> 360 (delta -27)
- task_narrative: 62 -> 62 (delta 0)

## Recommendation
- Decision: `proceed_to_bounded_training_review`
- ambiguity hard blocks remain clean
- heldout and tool_holdout overlap remain zero
- anti-homogenization and diversity checks remain passing
