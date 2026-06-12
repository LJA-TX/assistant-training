# Phase V Recommendation

## Recommended Next Experiment

The highest-information next experiment is a **controlled preservation ablation** that keeps the frozen scaffold and exact tool-call contract fixed while varying only anchor concentration around the H1/H2 range.

## Why This Is the Next Question

The current evidence already separates three possibilities:

- **Schema-only repair** is not enough. Phase U failed.
- **Anchor-weighted hybrid without the H1/H2 cue structure** is not enough. Phase Q failed.
- **Broad full-dataset balancing** is not enough. Phase L failed.

What remains unresolved is the interaction:

> Is H1/H2 success mainly due to anchor concentration, or due to anchor concentration plus the exact-tool-request cue on a frozen scaffold?

## What the Next Experiment Should Test

The next experiment should answer one question:

**If the exact tool-call envelope is held constant, how much anchor concentration is required to recover H1/H2-level capability?**

That question is higher value than another broad redesign because it isolates the remaining uncertainty instead of changing multiple dimensions at once.

## What Not to Do Yet

- Do not broaden prompt styles again before the preservation question is settled.
- Do not return to a full-corpus rebuild unless the preservation ablation fails.
- Do not treat strict JSON wording alone as a sufficient fix.

## Rationale

The repo already contains three instructive failures:

- v1.1: too flat, too broad, capability collapses.
- v1.2: more anchors, still not enough.
- Phase U: exact envelope on a tiny patch, still not enough.

That leaves one dominant unresolved factor: the **coupling between exact envelope realization and anchor density under the frozen scaffold**.

## Confidence

**Medium-high**

The recommendation is evidence-backed, but the exact minimal anchor level is still unknown.
