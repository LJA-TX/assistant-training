# Stage B i10r Counterbalanced Probe Residual No-Call Forensics

## Scope
Read-only forensic analysis of residual no-call failures after the rollback-first counterbalanced probe.

Inputs:
- `stage_b_v1_i10r_counterbalanced_probe_comparison_rows_raw.snapshot.jsonl`
- `stage_b_v1_i10r_microprobe_comparison_rows_raw.snapshot.jsonl`
- `stage_b_v1_i10r_nocall_probe_comparison_rows_raw.snapshot.jsonl`
- `stage_b_v1_i10r_counterbalanced_dataset_plan.json`
- `stage_b_v1_i10r_counterbalanced_localized_diff_verification.json`

## Residual Failure Count
- Expected no-call rows: 60
- Residual no-call failures: 2
- Residual failure rate: 3.33%
- Split location: adversarial only (2/2)

## Residual Cases
1. `adv_91008` (`adversarial` row 8)
- Prompt family: `Find TODOs in code but do not provide the project path.`
- Output: legacy wrapper with explicit `rg_search` name and hallucinated placeholder path.
- Class: `invalid_schema`
- Schema reason: `missing_tool_calls`

2. `adv_91016` (`adversarial` row 16)
- Prompt family: same as above.
- Output: `function_calls` legacy wrapper variant with explicit `rg_search` name and placeholder path.
- Class: `invalid_schema`
- Schema reason: `missing_tool_calls`

## Comparison vs Prior Runs
- In `i10r_microprobe`, both cases were correct no-call refusals.
- In failed `i10r_nocall_probe`, both cases were also correct no-call refusals.
- In counterbalanced probe, both flipped into pseudo-tool overcommitment wrappers.

## Relationship to Prior 5 Malformed-Regex Failures
- Prior failures (`adv_91003/07/11/15/19`) are fully recovered on no-call metric (0 remaining in that slice).
- Residual failures are **not** from the prior malformed-regex family.
- New residual family: underspecified-path TODO search prompts.

## Mapping to Counterbalanced Additions
Counterbalanced additions were limited to:
- `malformed_regex_underspecified_search_adversarial_boundary` (10 rows)
- `read_file_symbol_name_commitment_instability` (6 rows)

Residual TODO-no-path family was not explicitly included in additions.

## Causal Interpretation
Most supported interpretation:
- The package corrected the original malformed-regex boundary but undercorrected a neighboring adversarial no-call boundary.
- Residual behavior is semantically plausible overcommitment under underspecification, expressed through legacy wrapper drift (`function` / `function_calls` envelopes with explicit `rg_search`).

Not supported by evidence:
- scoring artifact as primary cause,
- read_file collapse,
- scalar-substitution rebound,
- wrapper leakage recurrence.

## Tiny-Remediation Justification
A tiny additional localized remediation is scientifically justified.

Recommended safe cap:
- 6 rows (ceiling 8)
- 3 no-call refusal rows + 3 matched valid `rg_search` contrastive rows
- additions-only, family-localized to underspecified-path TODO search
- no uncertainty-conditioning rows
- no read_file expansion
- no global no-call suppression

## Explicit Answers
1. How many no-call failures remain?
- 2.

2. Are they the same family as before?
- No. Prior family was malformed-regex unclosed-bracket; residual family is underspecified-path TODO search.

3. Were the prior five malformed-regex failures fully fixed?
- Yes for no-call scoring/gates (5/5 no-call-correct in counterbalanced probe).

4. Did any new no-call failure family appear?
- Yes. The underspecified-path TODO adversarial family (`adv_91008`, `adv_91016`).

5. What exact behavior caused the remaining failures?
- Over-eager pseudo-tool commitment: explicit `rg_search` intent in legacy non-canonical wrappers, with hallucinated placeholder path.

6. Is another tiny localized remediation justified?
- Yes.

7. If yes, what is the maximum safe footprint?
- Recommended 6 rows; hard ceiling 8.

8. What is the most dangerous next direction?
- Broad no-call suppression/global calibration shifts (especially unpaired uncertainty-conditioning), which risks eroding tool-expected procedural gains.
