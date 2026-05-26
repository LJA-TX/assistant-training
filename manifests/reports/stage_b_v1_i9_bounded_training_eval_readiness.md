# Stage B i9 Bounded Training/Eval Readiness

## Current State
- i9 implementation scaffolding: complete
- i9 dataset package: pending generation/validation in this phase
- approvals: all closed (`approved_to_* = false`)

## Required Hard Passes Before Training Review
- Ambiguity hard blocks all false.
- Heldout/tool_holdout overlaps all zero.
- Forbidden-pattern hits equal zero.
- Diversity and anti-homogenization summaries pass.
- Anchor dominance ratio below threshold.
- Top-1 behavioral share below monoculture threshold.

## Collapse-Watch Conditions
Recommend halt if any emerge post-eval:
- payload_not_parsed rises materially while exact-valid stagnates/falls
- top-1 behavioral category share > 0.70
- scalar/direct-answer substitutions increase materially
- no-call correctness regresses
- wrapper leakage appears
- single-anchor dependence strengthens
- paraphrastic canonical success narrows

## Decision Policy
- Proceed: all hard passes true, warnings bounded.
- Revise dataset: hard passes true but concentration/anchor warnings trigger.
- Abort direction: hard block failure or strong collapse-watch proxy signal.

Approval remains closed until explicit human sign-off.
