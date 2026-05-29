# Stage B Schema Convergence Recommendation

## Recommendation
`HYBRID_CONVERGENCE`

## Rationale
A single-layer fix does not cover the current 8 noncomputable metrics cleanly:

- 4 metrics have exact live-schema equivalents and are suitable for threshold-profile path updates:
  - `invalid_json_overall`
  - `no_call_correctness_adversarial`
  - `no_call_correctness_aggregate`
  - `wrapper_leakage_overall` (with candidate-path disambiguation)
- 4 metrics have no exact live-summary equivalent and require eval-summary emission expansion to preserve semantics:
  - `read_file_exact_valid_rate`
  - `read_file_symbol_name_exact_valid_rate`
  - `no_anchor_exact_valid_share`
  - `direct_answer_substitution_count`

## Proposed Convergence Sequence
1. Profile convergence pass (low-risk immediate)
- Update metric paths for exact-equivalent live metrics.
- Disambiguate wrapper leakage path selection explicitly by schema version.
- Keep noncomputable halt policy active.

2. Eval schema expansion pass (semantic restoration)
- Add explicit emission for missing semantic metrics in canonical eval summary.
- Keep additive schema design for backward compatibility.

3. Detector contract stabilization
- Keep alias usage limited to one-to-one exact mappings only, if needed for migration.
- Avoid proxy mappings that could hide real regressions.

## Governance Posture
- Maintain conservative `noncomputable_status` handling (`halt_progression`) until all critical metrics become computable.
- Do not convert missing metrics to inferred proxies for gate-critical decisions.

## Why Not the Other Single Options
- `PROFILE_UPDATE` only: leaves governance blind to key read_file/direct-answer/anchor metrics.
- `DETECTOR_ALIAS_LAYER` only: higher risk of semantic drift and harder auditability.
- `EVAL_SCHEMA_EXPANSION` only: strongest long-term fix, but slower to restore partial computability for currently exact-mappable metrics.

## Final Schema Recommendation
`HYBRID_CONVERGENCE`
