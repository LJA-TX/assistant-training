# Phase J Candidate Remediation Strategies

## Evaluation Frame

The evidence does not support a single-lever answer.
The safest reading is that Dataset v1.1 should be a combined-bottleneck remedy with explicit safety calibration.

## Strategy Comparison

| Strategy | Expected benefits | Expected risks | Evidence basis |
|---|---|---|---|
| Diversity-heavy | Best chance to keep the H1 tool-holdout lift and improve tail-tool coverage. | May underperform on heldout validation, tool-name accuracy, and argument accuracy; may not solve safety. | H1 outperforms H2 on tool-holdout exact-valid, no-anchor exact-valid, wrapper leakage, and no-call/adversarial safety. |
| Commitment-heavy | Best chance to keep the H2 heldout-validation, tool-name, and argument gains. | Highest risk of wrapper leakage and no-call/adversarial regression. | H2 outperforms H1 on heldout validation, tool-name accuracy, argument accuracy, and direct-answer suppression, but fails safety invariants. |
| Balanced hybrid | Best chance to explain the combined bottleneck by preserving both families of gains. | Can dilute the signal if the mix is not disciplined; may become ambiguous if it is not validated carefully. | H1 and H2 split metric families rather than producing one clean winner. |
| Safety-calibrated hybrid | Best chance to keep capability gains while forcing no-call and adversarial correctness back to `1.0`. | May reduce the raw capability lift if the refusal surface is overconstrained. | All observed runs fail at least one safety invariant, so any usable v1.1 must solve safety explicitly. |
| External-first hybrid | Best chance to escape the internal ceiling while still using the H1/H2 lesson set. | Higher contamination, license, and style-drift review cost. | The formal project determination remains `inconclusive_external_first`, so the repository already points toward external-first remediation. |

## Strategy Notes

### Diversity-heavy

This strategy is useful if the main concern is that the current internal corpus is too thin on tail tools and underrepresented tasks.
It is the strongest way to preserve the H1-style tool-holdout signal.

Its limitation is that it does not directly explain the H2 heldout-validation gains, and it does not solve the safety gap by itself.

### Commitment-heavy

This strategy is useful if the main concern is that the model still fails to enter canonical tool-call mode under less literal prompts.
It is the strongest way to preserve the H2 tool-name and argument gains.

Its limitation is that it visibly worsens safety in the observed run and does not explain why H1 wins tool-holdout and safety slices.

### Balanced hybrid

This is the best pure internal interpretation of the combined bottleneck.
It respects the fact that H1 and H2 split the metric families.

Its limitation is that a naive blend can hide which component is actually doing the work unless the validation plan is strict.

### Safety-calibrated hybrid

This is the strongest practical variant of the balanced strategy.
It is the only one that explicitly treats no-call and adversarial correctness as first-class requirements rather than side effects.

Its limitation is that the tighter the safety calibration, the more likely it is to suppress the raw capability gain.

### External-first hybrid

This is the strongest strategy if the next phase is defined by the formal project determination rather than by the internal scientific interpretation alone.
It is the cleanest way to expand breadth while reusing the H1/H2 lesson set.

Its limitation is the overhead of decontamination, licensing review, and style normalization.

## Evidence-Weighted Ranking

1. External-first hybrid.
2. Safety-calibrated hybrid.
3. Balanced hybrid.
4. Commitment-heavy.
5. Diversity-heavy.

The ranking is not a claim that the top item is already proven.
It is the smallest set of strategies that stays consistent with both the combined-bottleneck reading and the `inconclusive_external_first` formal determination.
If the external-first constraint is ignored, the internal evidence alone would favor the safety-calibrated hybrid as the cleanest combined-bottleneck design.

## Sources Used

- `docs/phase_i/H0_CHECKPOINT_REPORT.md`
- `docs/phase_i/H2_CHECKPOINT_REPORT.md`
- `docs/phase_ix/H1_EXCEPTION_CHECKPOINT_REPORT.md`
- `docs/phase_ix/H1_EXCEPTION_SCIENTIFIC_INTERPRETATION.md`
- `docs/phase_i/PHASE_I_FINAL_COMPLETION_REPORT.md`
- `docs/phase_i/BOTTLENECK_ATTRIBUTION_DECISION.md`
