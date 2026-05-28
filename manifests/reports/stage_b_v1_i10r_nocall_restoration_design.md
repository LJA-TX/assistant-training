# i10r No-Call Boundary Restoration Design

## Objective
Restore no-call integrity for the localized i10r adversarial failure family without degrading:
- `read_file` exact-valid foothold,
- anti-scalar-substitution gains,
- no-anchor procedural generalization,
- wrapper leakage invariants.

## Scope and Boundaries
- Design/scaffold only.
- No dataset mutation in this phase.
- No training, no eval reruns, no approval-gate changes.
- Intervention remains failure-family-localized to malformed-regex adversarial search prompts (`adv_91003/07/11/15/19` archetype).

## Failure Localization Summary
- Expected no-call failures: `5/60`.
- Split localization: `5/5` failures are in `adversarial` split.
- Prompt family localization: `100%` in one normalized family (`search for pattern [a-z ... and proceed`).
- Output signature localization: `100%` legacy pseudo-wrapper (`{"function":...}`) with `schema_reason=missing_tool_calls`.
- Interpretation: procedural over-eagerness under adversarial uncertainty, not semantic misunderstanding.

## Minimum Viable Corrective Footprint
Additions-only, capped, localized package:
- Total proposed new rows: `16`.
- Total altered existing rows: `0`.
- Total replacements/thinning: `0`.

Composition:
1. `12` rows targeted no-call contrastive restoration.
   - `6` malformed/underspecified adversarial search prompts -> expected refusal/no-call.
   - `6` matched valid-search boundary prompts -> expected canonical `rg_search` tool call.
2. `4` rows small adversarial uncertainty conditioning support.
   - Ambiguous/improperly constrained search requests -> calibrated refusal/no-call.

Rationale: footprint is only ~`0.73%` of current i10r train size (`16/2202`), reducing global drift risk while directly addressing the localized failure signature.

## Data-Operation Mode
- Mode: **additions only**.
- Existing i10r conversion families: untouched.
- Existing no-call and direct-answer rows outside this failure slice: unchanged.
- Canonical eval topology and decode defaults: unchanged.

## Boundary Pair Design Rules
For each contrastive pair, enforce:
- Same task semantics (search intent), differing boundary validity.
- Malformed/underspecified variant: refusal/no-call target.
- Valid and sufficiently specified variant: canonical `tool_calls` `rg_search` target.
- No negation-heavy style, no blacklist language, no global anti-tool instructions.
- Maintain paraphrastic diversity and no-anchor predominance.

## Anti-Regression Gates (Post-Run Interpretation)
Hard gates:
- `no_call_correctness == 1.0` (aggregate expected no-call rows).
- `adversarial no_call_correctness == 1.0`.
- `wrapper_leakage == 0.0`.

Co-primary anti-regression gates:
- `read_file exact-valid` must not drop materially from i10r baseline (`0.703704`):
  - floor `>= 0.65` and delta `>= -0.05`.
- `scalar substitution share` must not rebound materially from i10r (`0.0`):
  - absolute `<= 0.05`.
- `no-anchor exact-valid share` must remain high (i10r baseline `0.862069`):
  - floor `>= 0.75` and delta `>= -0.10`.

## How Valid Search Commitment Is Preserved
- Every refusal-boundary addition is paired with a valid-search commitment counterpart.
- Preservation of commitment pressure is explicit: no broad anti-tool suppression rows are introduced.
- The intervention teaches boundary discrimination, not global caution.

## How Global Caution Drift Is Prevented
- Strict locality: one failure family only.
- Strict cap: 16 rows total.
- Additions-only avoids reweighting legacy/procedural datasets by deletion.
- Explicit prohibition of broad refusal flooding and confidence calibration campaigns.

## Telemetry Required to Prove Success
Required evidence after bounded run:
- No-call recovery: aggregate + adversarial no-call return to `1.0`.
- No procedural rollback: read_file exact-valid remains above gate floor.
- No scalar rebound: scalar/direct substitution shares remain low.
- No anchor relapse: no-anchor exact-valid remains dominant.
- No wrapper leakage recurrence.

## Explicit Answers
1. Minimum viable corrective footprint: `16` localized additions.
2. New/altered rows justified: `16` new, `0` altered.
3. Additions/replacements/thinning: additions only; no replacements; no thinning.
4. Preserve valid commitment while malformed refuses: paired boundary examples with matched semantics and opposite boundary validity.
5. Prevent global caution drift: strict family-local cap + paired valid commitments + prohibition of broad negative restoration.
6. Proof telemetry: no-call aggregate/adversarial restoration plus read_file/scalar/no-anchor/wrapper anti-regression gates.
7. Next step after design: **bounded dataset generation** (localized remediation package), not further broad forensics and not halt.
