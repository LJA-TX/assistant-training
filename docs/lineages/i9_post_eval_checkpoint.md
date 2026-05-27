# i9 Post-Eval Preservation Checkpoint

## 1) What i9 Successfully Achieved

- Iteration: `stage_b_llama31_8b_base_v1_i9`
- Objective focus: commitment-conversion repair (near-miss wrapper/envelope repair + semantic-substitution conversion) under bounded governance.
- Heldout exact-valid improved materially:
  - i8: `0.04`
  - i9: `0.15` (`+11pp`)
- Heldout tool-name/argument accuracy improved materially:
  - i8: `0.04 / 0.04`
  - i9: `0.15 / 0.15`
- Structural near-miss pressure dropped sharply:
  - i8 structural near-miss rate: `0.272059`
  - i9 structural near-miss rate: `0.056`
- Spill/no-call runtime invariants preserved:
  - no-call correctness: `1.0`
  - wrapper leakage: `0.0`
  - contamination blocking splits (`heldout_validation`, `tool_holdout`): overlap remains zero.
- Interpretation: commitment-conversion is a real leverage point for exact-valid/tool-accuracy recovery.

## 2) What Failed or Regressed

- Semantic/scalar substitution rebound became the active regression:
  - i8 scalar substitution share: `0.264706`
  - i9 scalar substitution share: `0.400000`
  - delta: `+0.135294` (collapse-watch trigger)
- Parseability remains weak in absolute terms:
  - heldout `invalid_json`: i8 `0.57` -> i9 `0.58` (not improved)
  - `payload_not_parsed` remains dominant (`75` tool-expected rows)
- Generalization remains incomplete:
  - exact-valid concentrated in specific slices despite broader non-anchor successes.
- `read_file` remains a major weakness:
  - tool-expected rows: `27`
  - exact-valid rows: `0`
  - `payload_not_parsed` rate: `1.0`

## 3) Most Important Behavioral Interpretation

- i9 evidence continues to support **commitment inhibition** more than task misunderstanding.
- The run shows **procedural commitment progress** (exact-valid lift + near-miss repair) without a return to catastrophic schema-spill behavior.
- Anchor behavior is mixed rather than pure lexical ritualization:
  - literal-anchor exact share: `0.266667`
  - paraphrastic-anchor exact share: `0.333333`
  - exact successes are present outside literal anchor prompts.
- i9 is still progress because it demonstrates controllable structural recovery under preserved invariants, while clearly exposing the next bottleneck (semantic/scalar substitution).

## 4) Why Execution Halted

- Halt trigger: `scalar_direct_substitution_rebound` (active collapse-watch condition).
- Halt decision was correct because rebound exceeded configured tolerance while parseability remained weak.
- This is **not** interpreted as i4/i5-style catastrophic collapse:
  - no-call remained perfect,
  - wrapper leakage remained zero,
  - top-1 behavioral share stayed below monoculture threshold,
  - no broad overconstraint signature reappeared.

## 5) Current Strategic Interpretation

- Wrapper/envelope repair appears partially solved in i9.
- Active bottleneck has shifted to semantic/scalar substitution under uncertainty.
- Next bounded work, if authorized, should prioritize semantic-substitution conversion (especially `read_file`) over additional generic hygiene.

## 6) Explicit Governance Status

- No promotion authorized.
- No canonization authorized.
- No threshold relaxation performed.
- No canonical eval topology mutation performed.
- Bounded experimentation posture remains in force.

