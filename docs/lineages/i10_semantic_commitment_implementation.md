# i10 Semantic Commitment Implementation (Bounded Design Scaffold)

## Purpose
This document operationalizes i10 as a bounded continuation after i9.

Primary target:
- convert semantically-correct scalar/direct substitutions into canonical procedural commitment,
- with `read_file` as primary pathological slice,
- while preserving no-call/wrapper invariants and avoiding i4/i5-style collapse dynamics.

Out of scope in this phase:
- dataset emission,
- training,
- canonical eval execution,
- approval-gate opening.

## Implementation Philosophy
- Localize intervention pressure to behavior families and archetypes, not global policy text.
- Prefer positive procedural exemplars over prohibitive wording.
- Treat collapse-watch telemetry as co-primary with exact-valid improvement.
- Preserve prompt-style and paraphrastic diversity to avoid lexical-shell ritualization.
- Keep all execution approvals closed until preflight + human review pass.

## Intervention Topology (Planned)
- Primary: `read_file` semantic-substitution conversion
  - archetypes: boolean presence, symbol-name, first-function-name.
- Secondary: `rg_search` scalar substitution conversion
  - archetypes: match_count, zero/non-zero bypass.
- Tertiary: small uncertainty-conditioned procedural continuation overlays.

## Safeguards (Must Preserve)
- `no_call_correctness = 1.0`
- `wrapper_leakage = 0.0`
- contamination overlap zero on heldout/tool_holdout
- ambiguity hard blocks
- diversity and anti-monoculture controls
- collapse-watch enforcement

## Required Design Answers

1. How will i10 avoid brittle “always emit tool_calls” ritualization?
- By using archetype-conditioned conversion pairs (intent-preserving) rather than global imperative directives.
- By enforcing paraphrastic spread and top-shell concentration telemetry.
- By forbidding lexical-blacklist and global coercive pressure regimes.

2. How will i10 distinguish semantic closure from procedural completion?
- Semantic closure is defined as direct/scalar/pseudo result substitution output.
- Procedural completion is defined as canonical tool-call envelope emission with argument-bearing function payload.
- Telemetry tracks these as separate behavior channels, not aggregated invalid-json only.

3. How will i10 create a `read_file` exact-valid foothold?
- `read_file` is primary intervention family with explicit archetype coverage.
- Coverage is intentionally split across three read_file archetypes to avoid one-shell overfit.
- Success requires read_file exact-valid emergence with no invariant regressions.

4. How will scalar-substitution rebound be measured separately from wrapper/envelope regressions?
- Dedicated scalar/direct substitution rebound proxies are tracked independently.
- Wrapper/envelope channels are tracked via structural categories and spill composite telemetry.
- Collapse-watch can trigger on scalar rebound even when wrapper metrics look stable.

5. How will paraphrastic success diversity be preserved?
- Anchor-bucket telemetry (literal vs paraphrastic vs no-anchor) is mandatory.
- Prompt uniqueness, entropy, and top-shell share are explicit diagnostics.
- Readiness requires non-collapsed paraphrastic distribution.

6. What telemetry indicates healthy generalization vs lexical-shell memorization?
- Healthy generalization:
  - substitution shares decline,
  - read_file exact-valid emerges,
  - success spreads across multiple paraphrastic buckets,
  - shell concentration stays below threshold.
- Lexical-shell memorization:
  - exact-valid concentrates in one lexical shell,
  - top prompt-shell share rises,
  - paraphrastic success narrows.

7. Highest-risk collapse vector for i10?
- Local read_file template homogenization causing procedural recitation and benchmark-facing overfit while scalar substitution remains high in real slices.

## Planning Artifacts
- Builder scaffold: `scripts/build_stage_b_recovery_i10_dataset.py`
- Diagnostics scaffold: `scripts/i10_diagnostics_scaffold.py`
- Preflight validator: `scripts/validate_stage_b_recovery_i10_preflight.py`
- Draft config/manifest and governance templates under `configs/lora/` and `manifests/`.

## Decision Boundary
i10 remains scientifically justified as bounded continuation if:
- scalar/direct substitution channels are targeted directly,
- read_file foothold is treated as primary success objective,
- collapse-watch constraints remain strict and unchanged.
