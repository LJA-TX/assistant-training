# Stage B v1 i9 Commitment-Conversion Reconnaissance

- Generated (UTC): 2026-05-26T19:38:10Z
- Phase type: reconnaissance + bounded intervention design (no training, no eval reruns, no dataset mutation).
- Focus: convert semantic substitution and near-canonical outputs into strict canonical `tool_calls` commitment.

## Inputs Analyzed
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i8_parseability_behavioral_analysis.md`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i8_parseability_behavioral_analysis.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i8_near_miss_taxonomy.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i8_tool_failure_clusters.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i3_semantic_recovery_gate_assessment.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i6_canonical_eval_summary.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i7_canonical_eval_summary.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i8_canonical_eval_summary.json`
- `/opt/ai-stack/assistant-training/evals/runs/canonical_eval_20260526T172855Z/comparison_rows.jsonl`

## Trajectory Context (i3/i6/i7/i8)
- Heldout `invalid_json`: i3=0.43, i6=0.39, i7=0.66, i8=0.57.
- `payload_not_parsed` counts: i3=55, i6=51, i7=81, i8=82.
- Spill composite (`payload_not_object + missing_tool_calls`) counts: i3=80, i6=88, i7=57, i8=54.
- Interpretation: spill pressure improved by i8, but parseability commitment remained unstable and sub-baseline to i3/i6.

## Commitment-Conversion Taxonomy
- `semantic_textual_substitution`: 58 / 136 (42.6%)
- `direct_scalar_answer_substitution`: 25 / 136 (18.4%)
- `wrapper_key_drift`: 19 / 136 (14.0%)
- `envelope_omission`: 16 / 136 (11.8%)
- `token_scalar_substitution`: 11 / 136 (8.1%)
- `malformed_nonjson_other`: 5 / 136 (3.7%)
- `object_missing_commitment_envelope`: 2 / 136 (1.5%)

- Semantic substitution family: 94/136 (69.1%) non-exact rows.
- Near-canonical structure family: 37/136 (27.2%) non-exact rows.
- Semantic substitution on-task marker rate: 55.3%.
- Near-canonical high latent-structure rate (`score>=0.6`): 89.2%.
- Distinction: semantic competence is frequently present; canonical commitment competence is the bottleneck.

## Near-Miss Repairability
- `semantic_textual_substitution`: tier=moderate_to_hard, count=58, latent_structure=0.01, on_task=89.7%
- `direct_scalar_answer_substitution`: tier=moderate_to_hard, count=25, latent_structure=0.00, on_task=0.0%
- `wrapper_key_drift`: tier=easiest, count=19, latent_structure=0.92, on_task=100.0%
- `envelope_omission`: tier=easiest, count=16, latent_structure=0.74, on_task=100.0%
- `token_scalar_substitution`: tier=moderate_to_hard, count=11, latent_structure=0.00, on_task=0.0%
- `malformed_nonjson_other`: tier=uncertain, count=5, latent_structure=0.00, on_task=0.0%
- `object_missing_commitment_envelope`: tier=moderate, count=2, latent_structure=0.10, on_task=0.0%

## Lexical Anchor Investigation
- Anchor dependence detected: **True**.
- Exact-valid outputs were confined to `rg_search` prompts with literal `pattern="tool_calls"` signature.
- Assessment: current canonical success appears token-triggered/brittle, not generalized schema commitment.
- i9 implication: broaden commitment activation through bounded, diverse conversion pairs rather than hard-coding single-token anchors.

## Commitment-Conditioned Curriculum Concepts (Bounded)
- Near-miss -> canonical repair pairs for wrapper/envelope classes (high-repairability, low collapse risk).
- Semantic substitution -> canonical conversion pairs for answer-content fallbacks (highest leverage, moderate risk).
- Uncertainty-conditioned canonical fallback exemplars (teach canonical call emission under uncertainty).
- Wrapper normalization repair pairs (`tool_function(s)`/`function` object to strict `tool_calls`).
- No negation-heavy policing, no blacklist flooding, no global imperative template collapse.

## Risk Analysis
- Most promising intervention family: `near_miss_wrapper_envelope_repair_pairs`.
- Most dangerous intervention family: `negation_heavy_global_policing`.
- Primary collapse risks: renewed overconstraint, hidden template homogenization, lexical overfitting to anchor tokens, no-call regression if global coercion leaks.
- Safe bounded pattern: local conversion pairs + diversity preservation + spill/no-call co-primary monitoring.
- Early collapse signals to watch:
  - rapid rise in payload_not_parsed/invalid_json with simultaneous drop in exact_valid over first bounded eval slice
  - collapse of behavior diversity: top-1 behavioral category share > 0.70 in targeted tools
  - sharp increase in scalar/direct-answer substitutions while near-canonical repairs do not rise
  - drop in no-call correctness below established invariant or any wrapper leakage > 0
  - new dominance of single lexical anchor family with loss of paraphrastic canonical success

## Required Explicit Conclusions
- **1_primary_bottleneck**: canonical serialization generalization + commitment behavior under uncertainty (not task semantics).
- **2_near_miss_repair_gain_likelihood**: high for wrapper/envelope classes; moderate overall because semantic substitution dominates volume.
- **3_semantic_substitution_vs_hygiene**: semantic-substitution conversion likely yields higher marginal gains than further hygiene tuning.
- **4_intervention_magnitude**: evidence supports low-magnitude targeted intervention before any redesign.
- **5_most_promising_family**: near_miss_wrapper_envelope_repair_pairs
- **6_most_dangerous_family**: negation_heavy_global_policing
- **7_early_i4_i5_collapse_signals**: ['rapid rise in payload_not_parsed/invalid_json with simultaneous drop in exact_valid over first bounded eval slice', 'collapse of behavior diversity: top-1 behavioral category share > 0.70 in targeted tools', 'sharp increase in scalar/direct-answer substitutions while near-canonical repairs do not rise', 'drop in no-call correctness below established invariant or any wrapper leakage > 0', 'new dominance of single lexical anchor family with loss of paraphrastic canonical success']

## i9 Recommendation
- **i9 should exist** as a bounded commitment-conversion run, provided intervention remains localized, diversity-preserving, and explicitly guarded against i4/i5 collapse signatures.
