# Stage B i8 Human Review Package

- Generated UTC: 2026-05-26T16:04:20Z
- Iteration: stage_b_llama31_8b_base_v1_i8
- Candidate train/val rows: 2160 / 240

## Contamination Audit (Blocking)
- train_overlap: heldout(p=0, t=0, c=0), tool_holdout(p=0, t=0, c=0)
- val_overlap: heldout(p=0, t=0, c=0), tool_holdout(p=0, t=0, c=0)
- combined_overlap: heldout(p=0, t=0, c=0), tool_holdout(p=0, t=0, c=0)

## Prompt Ambiguity Hard Blocks
- Counts: different_target=0, different_tool=0, prompt_tool_diff_args=0
- Hard-block flags: {'prompt_to_multiple_targets': False, 'prompt_to_multiple_tools': False, 'prompt_tool_to_multiple_arguments': False}

## Anchor Variant Distribution
- Train: {'append': 24, 'append_compact': 10, 'existing_anchor_signal': 629, 'prepend': 17, 'unchanged_diversity_preserve': 39}
- Val: {'append': 4, 'append_compact': 2, 'existing_anchor_signal': 69, 'prepend': 1, 'unchanged_diversity_preserve': 4}

## Top Skeleton Families (Targeted)
- 7bf04fd7509e: count=42 share=0.052566
- a195264dd90c: count=40 share=0.050063
- 49e8a004f19b: count=36 share=0.045056
- b5346fe71f24: count=32 share=0.04005
- 52c9c7295b06: count=30 share=0.037547
- 3d04e2e8f9fb: count=23 share=0.028786
- 4ea5a9d3e1aa: count=22 share=0.027534
- 4b6c95f32e2c: count=20 share=0.025031

## Dominant Style Buckets (Targeted)
- imperative_line_scoped: count=387 share=0.484355
- imperative_general: count=350 share=0.438048
- task_narrative: count=62 share=0.077597

## Prompt-Length Distribution
- Targeted delta: {'chars_mean_delta': 13.296621, 'chars_p95_delta': 17.0, 'words_mean_delta': 1.105131, 'words_p95_delta': 0.0}
- Targeted candidate stats: {'chars': {'count': 799.0, 'mean': 182.45682102628285, 'median': 165.0, 'p95': 273.0, 'max': 296.0}, 'words': {'count': 799.0, 'mean': 18.918648310387987, 'median': 17.0, 'p95': 31.0, 'max': 36.0}}

## Risk Flags
- Diversity: {'status': 'ok', 'style_bucket_count_targeted': 3, 'dominant_style_share_targeted': 0.484355, 'unique_skeletons_targeted': 54, 'top1_skeleton_share_targeted': 0.052566, 'risk_flags': [], 'pass': True}
- Anti-homogenization: {'status': 'ok', 'forbidden_hits_total': 0, 'targeted_top1_skeleton_share': 0.052566, 'targeted_top3_skeleton_share': 0.147685, 'dominant_style_share': 0.484355, 'risk_signals': [], 'pass': True}

## Interpretation Guidance
- If top1 targeted skeleton share rises while unique skeletons shrink, treat as local-template coercion risk.
- If targeted prompt-length deltas spike with stable tool distribution, inspect for anchor over-imprinting.
- If forbidden-pattern hits appear, invalidate candidate and revise intervention shaping.

## Targeted Prompt Samples
- read_file:
  - i3_adapt_p0_read_file_1 [imperative_line_scoped] chars=146: Read /opt/ai-stack/runtimes/assistant-runtime/server/service.py lines 1-25 and report the first function name. Return strict JSON tool_calls only.
  - i3_adapt_p0_read_file_1 [imperative_line_scoped] chars=146: Show /opt/ai-stack/runtimes/assistant-runtime/server/service.py lines 1-25 and report the first function name. Return strict JSON tool_calls only.
- rg_search:
  - i3_adapt_p0_rg_search_1 [imperative_general] chars=165: Use rg_search to find "def create_app" in /opt/ai-stack/runtimes/assistant-runtime/server/service.py and report match_count only. Return strict JSON tool_calls only.
  - i3_adapt_p0_rg_search_1 [imperative_general] chars=165: Use rg_search to find "def create_app" in /mnt/services/runtimes/assistant-runtime/server/service.py and report match_count only. Return strict JSON tool_calls only.
