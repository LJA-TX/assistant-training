# Stage B i10r Residual No-Call Human Review Package

- Generated UTC: 2026-05-28T16:34:48Z
- Iteration: stage_b_llama31_8b_base_v1_i10r_residual_nocall

## Composition
- Added rows total: 6
- Added rows train: 4
- Added rows val: 2
- Altered existing rows: 0

## Localization
- additions_exact_match: True
- existing_rows_unchanged: True
- localized_family_only: True
- contrastive_pairs_pass: True
- residual_block_pass: True

## Hygiene
- ambiguity_hard_blocks_clean: True
- heldout_overlap_zero: True
- tool_holdout_overlap_zero: True
- forbidden_pattern_hits_zero: True

## Anti-Regression
- additions_anchor_distribution: {'literal_tool_calls': 0, 'paraphrastic_tool_call': 0, 'no_anchor_phrase': 6}
- top1_skeleton_share_additions: 0.166667
- anti_regression_risk_pass: True
- risk_flags: {'literal_anchor_ratio_high': False, 'top1_skeleton_share_high': False, 'unexpected_tool_mix': False, 'unexpected_refusal_mix': False, 'read_file_additions_present': False}

## Recommendation
- suitable_for_one_final_bounded_residual_seam_probe_review_only_if_post_run_gates_hold

