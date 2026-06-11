# H1 Exception Scientific Interpretation

## Did H1 materially move the target metrics?

**Yes.**

H1 materially improved the diversity-sensitive metrics relative to H0:

- tool-holdout exact-valid moved from `0.0` to `0.6`
- heldout-validation exact-valid moved from `0.09` to `0.64`
- tool-name accuracy moved from `0.07142857142857142` to `0.7142857142857143`
- argument accuracy moved from `0.06428571428571428` to `0.6285714285714286`
- no-anchor exact-valid moved from `0.0` to `0.8636363636363636`

Those are not marginal movements. They show that the diversity patch acquired real capability signal on the frozen surface.

## Did H1 outperform H2?

**Mixed.**

H1 outperformed H2 on:

- tool-holdout exact-valid: `0.6` vs `0.525`
- no-anchor exact-valid: `0.8636363636363636` vs `0.84375`
- wrapper leakage: `0.0` vs `0.005`
- no-call correctness: `0.9` vs `0.8`
- adversarial no-call correctness: `0.7` vs `0.4`

H2 outperformed H1 on:

- heldout-validation exact-valid: `0.75` vs `0.64`
- tool-name accuracy: `0.7714285714285715` vs `0.7142857142857143`
- argument accuracy: `0.6928571428571428` vs `0.6285714285714286`
- direct-answer suppression on non-exact tool rows: `9` vs `12`

No single run dominates cleanly across the full first-screen metric set.

## Did H1 support diversity dominance?

**Partially, but not formally.**

H1 clearly supports the idea that diversity restoration matters:

- it wins the tool-holdout exact-valid comparison against H2;
- it restores read-file coverage substantially;
- and it improves the tail-tool family metrics that H0 left collapsed.

However, the published A threshold is not satisfied cleanly because H2 still produces stronger commitment-side suppression and broader heldout accuracy movement.

## Did H1 support commitment dominance?

**No.**

H1 beats H2 on tool-holdout exact-valid and safety metrics, which means the commitment-only story is incomplete.
H2 remains stronger on heldout-validation exact-valid, tool-name accuracy, and argument accuracy, but that does not convert the evidence into a clean commitment-only winner.

## Did H1 support a combined explanation?

**Yes.**

The strongest scientific reading of the three-run set is a combined explanation:

- diversity repair contributes a meaningful lift on tool-holdout and tail-tool behavior;
- commitment repair contributes a meaningful lift on heldout validation, tool-name accuracy, and argument accuracy;
- neither lever alone explains the full pattern.

This is the closest fit to `E` in the Phase H hypothesis set.

## What new evidence was obtained?

The exception run adds three important facts:

1. Diversity-only intervention can beat commitment-only intervention on tool-holdout exact-valid.
2. The diversity patch preserves wrapper leakage at zero, but still does not satisfy the no-call/adversarial safety invariant.
3. The best explanation is no longer a single-lever dominance story; it is a split-family picture with both diversity and commitment contributing.

## Scientific Bottom Line

H1 does not overturn the official Phase I determination, but it materially strengthens the case that the residual bottleneck is combined rather than singular.

The most defensible research interpretation is `E`:

- more than one treatment wins a different metric family,
- no single probe dominates cleanly,
- and the evidence favors a combined bottleneck explanation.

