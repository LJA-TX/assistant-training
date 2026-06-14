# Remaining Causal Model

## Smallest Model Consistent With The Evidence

The smallest explanation that fits H1/H2 success, Phase L failure, Phase Q failure, Phase U failure, and the full Z / ZA / ZB / ZC sweep is:

> H1/H2 succeeded because they preserved a small, patch-local training surface on a frozen scaffold, with the exact-tool-request cue on the positive rows and a high concentration of the core anchor tools.

That model is conjunctive, not single-factor.

## Why This Is The Smallest Model

### 1. Schema alone is not enough

Phase U shows that canonical JSON wording by itself does not recover tool-call capability.

### 2. Anchor concentration helps, but it is not sufficient

The Z sweep shows a positive response to higher anchor concentration, but the response is non-monotonic and does not reach H1/H2.

### 3. The frozen scaffold and exact cue are necessary context, but not the full explanation

They are preserved across the successful patches and the later ablation arms, so they are background constraints rather than the differentiating signal.

### 4. The remaining untested property is the patch-local replacement topology

The H1/H2 runs were small, low-delta patches on top of the Stage B recovery scaffold.
The later v1.1/v1.2-style rebuilds and the Z-series ablation arms did not isolate that small-patch property.

That is the most plausible remaining factor after the completed anchor sweep.

## What The Model Explains

- Why H1/H2 reached exact JSON validity near `0.44` to `0.48`.
- Why Phase L and Phase Q fell far short.
- Why Phase U preserved safety but lost capability.
- Why the Z-series sweep improved capability but never reproduced H1/H2.
- Why the highest-anchor arm in ZC recovered some realization but not the full safety/capability balance.

## What The Model Does Not Yet Explain

- The precise division between patch scale and prompt-regime effects inside the H1/H2 success surface.
- Whether the exact-tool-request cue is merely necessary or a core causal multiplier.
- Whether a smaller patch-local experiment at fixed anchor concentration would recover the H1/H2 regime.

## Implication

The causal story is no longer "anchor concentration alone."

The evidence now points to a patch-local, cue-preserving, anchor-heavy positive slice as the remaining plausible explanation.
