# Stage B i10 Human Review Package

- Generated UTC: 2026-05-27T11:23:36Z
- Iteration: stage_b_llama31_8b_base_v1_i10
- Status: completed

## Selection
- Added rows total: 102
- Added train: 88
- Added val: 14

## Telemetry Highlights
- Top1 behavioral category share: 0.45098 (threshold=0.7)
- Anchor dominance ratio: 0.215686 (threshold=0.7)
- Scalar rebound proxy delta: 0.05098 (threshold=0.05)

## Risk Flags
- Diversity pass: True
- Anti-homogenization pass: True
- Generalization/recitation flags: {'top1_behavioral_category': 'scalar_substitution', 'top1_behavioral_category_share': 0.45098, 'top1_threshold': 0.7, 'top1_flag': False, 'prompt_uniqueness_ratio': 0.901961, 'top_prompt_shell_share': 0.029412, 'interpretation_hint': 'High top_prompt_shell_share + low uniqueness may indicate lexical-shell memorization risk.'}
- Anchor flags: {'literal_tool_calls_anchor_rows': 22, 'intervention_rows': 102, 'ratio': 0.215686, 'threshold': 0.7, 'flag': False, 'anchor_bucket_distribution': {'no_anchor_phrase': 76, 'literal_tool_calls': 22, 'paraphrastic_tool_call': 4}}

## Guidance
- Prefer small read_file exact-valid footholds with paraphrastic spread over narrow literal-shell gains.
- If top prompt shell share rises above threshold, treat as template coercion risk.
- If ambiguity hard blocks are non-zero, invalidate candidate package before training review.
- If scalar substitution rebound rises post-eval, halt forward progression.

