# Stage B i10r Counterbalanced Remediation Design (Rollback-First)

## Scope
- Phase type: design/scaffold only.
- No dataset mutation, no training, no eval reruns.
- This design is report-only until separately authorized.

## Authoritative Parent Constraint
- Required parent checkpoint for any follow-on probe: `stage_b_llama31_8b_base_v1_i10r_microprobe`.
- Explicitly forbidden parent: `stage_b_llama31_8b_base_v1_i10r_nocall_probe`.

## Problem Being Solved
The prior localized no-call restoration probe fixed adversarial no-call integrity but destabilized tool-expected behavior:
- no_call correctness recovered to `1.0` (aggregate and adversarial)
- read_file exact-valid collapsed (`0.703704 -> 0.259259`)
- read_file symbol-name collapsed (`11/13 -> 0/13`)
- direct-answer substitution rebounded (`0.226415 -> 0.439394`)

Interpretation: calibration bifurcation, not shell collapse, not anchor collapse, not global parseability catastrophe.

## Design Objective
Restore malformed-regex adversarial no-call boundary while preserving read_file symbol-name procedural commitment and maintaining i10r anti-scalar/no-anchor gains.

## Safest Counterbalanced Footprint (Recommended)
- Operation mode: additions-only.
- Total new rows: `16`.
- Replacements: `0`.
- Thinning: `0`.

Row budget:
- No-call boundary contrastive rows: `10` total
  - `5` malformed/underspecified regex no-call refusal rows
  - `5` matched valid canonical `rg_search` rows
- Read-file symbol-name commitment-preservation rows: `6` total
  - exact failing archetype only (`read_file_symbol_name`)
  - matched path/line envelopes (`server/agent.py`, line window around 1080-1104, both `/opt/...` and `/mnt/...` forms)
  - small paraphrastic spread without changing procedural target
- Uncertainty-conditioning support rows: `0` (removed)

## Why This Footprint
- Previous 16-row package was not primarily too large; it was misbalanced (all pressure on no-call boundary family without explicit read_file commitment preservation).
- Keeping the total at 16 preserves small-footprint discipline while correcting directional imbalance.
- Removing uncertainty-conditioning-only rows reduces global caution spill risk.

## Required Immutability
- Keep i10r conversion families unchanged.
- Keep all non-target no-call rows unchanged.
- Keep direct-answer rows outside the target family unchanged.
- Keep canonical eval topology, decode defaults, and thresholds unchanged.
- Keep ambiguity/contamination governance unchanged.

## Pairing Strategy
- No-call side: malformed regex vs valid regex matched semantic pairing (same intent token, opposite boundary validity).
- Read-file side: commitment-preservation rows are strictly procedural call emissions for symbol-name extraction, aligned to exact failing envelopes.

## Preventing Re-break of No-Call Integrity
- Retain valid-search commitment pairs (do not train pure refusal-only signal).
- Keep restoration strictly family-localized.
- Remove unpaired uncertainty-conditioning refusals.
- Require post-run dual pass: no-call hard gates + read_file anti-regression gates.

## Explicit Answers
1. Minimum viable no-call restoration rows after rollback: `10` (5 contrastive pairs).
2. Minimum viable read_file symbol-name counterbalance rows: `6`.
3. Prior 16-row package issue: misbalanced and missing counterbalance; not purely oversized.
4. Uncertainty-conditioning support rows: remove in this next pass (`4 -> 0`).
5. Read-file counterbalance form: exact failing archetype with matched path/line envelopes, plus limited paraphrastic variants.
6. Valid-search pairs: keep.
7. Bounded continuation justified after rollback-first design: yes, with strict post-run gates.

## Go/No-Go (Design Stage)
- Recommendation: `GO` for bounded counterbalanced dataset-generation planning review (not execution).
