# Stage B i10r No-Call Probe Failure Forensics

- Generated UTC: 2026-05-27T19:13:50Z
- Scope: read-only forensic analysis (no dataset mutation, no training, no eval reruns).

## Executive Findings
- No-call objective succeeded on target boundary: aggregate no-call `0.9167 -> 1.0000`, adversarial no-call `0.7500 -> 1.0000`, wrapper leakage remained `0.0`.
- Tool-expected performance regressed: overall exact-valid `0.4350 -> 0.3700`, invalid_json `0.0950 -> 0.1750`.
- Read_file collapsed on one archetype: exact-valid `0.7037 -> 0.2593` (net -12 exact rows).
- Direct-answer substitution rebounded: `0.2264 -> 0.4394` (+0.2130 share). Scalar substitution stayed controlled (`0.0 -> 0.0303`).
- Anchor/no-anchor profile stayed stable; this is not shell-ritual or anchor-collapse behavior.

## Row-Level Transition Summary
- Tool-expected rows: 140
- Hard regressions (exact->non-exact): 19
- Severity regressions: 24
- Dominant degraded transitions: exact_valid -> direct_answer_fallback (12), other_non_exact -> direct_answer_fallback (4), exact_valid -> other_non_exact (4), exact_valid -> scalar_substitution (2), exact_valid -> tool_commitment_suppression (1)
- Severity regressions by tool: {'read_file': 13, 'rg_search': 6, 'stat_path': 2, 'git_status': 1, 'git_diff': 1, 'get_system_version': 1}

## Read_File Collapse Localization
- `read_file_symbol_name`: microprobe exact 11/13 -> no-call probe exact 0/13.
- `read_file_first_function_name`: microprobe exact 1/7 -> no-call probe exact 0/7.
- `read_file_boolean_presence`: stable at 7/7 exact.
- Regressions are concentrated in source case family `p0_read_file_2` and mostly direct-answer fallback.

## Causal Interpretation
- The restoration package repaired the intended malformed-regex adversarial no-call boundary (5/5 fixed).
- The same update likely shifted calibration toward semantic closure under uncertainty-like extraction tasks: exact read_file tool calls became plain-text answers (identifier/file-token outputs).
- This is a regime bifurcation: no-call integrity improved while read_file commitment collapsed. It is not global parseability collapse, not wrapper leakage relapse, and not anchor ritualization.

## Why No-Call Recovery Coincided With Direct-Answer Rebound
- No-call correctness is scored as “no tool call emitted”; plain-text echo/refusal text satisfies that boundary.
- Read_file symbol-name prompts are shortcut-prone (model can emit plausible token-like answers); after restoration, this shortcut expanded in heldout.
- Scalar outputs remained constrained, but textual direct-answer substitution expanded, indicating substitution-style shift rather than full substitution elimination.

## Stability Assessment
- i10r gains are not fundamentally broken, but they are narrowly calibrated and sensitive to small boundary-restoration perturbations.
- Incremental continuation remains scientifically plausible, but not from the current no-call probe checkpoint.
- Safer next step: rollback to i10r microprobe and apply narrower remediation that explicitly protects read_file symbol-name commitment while restoring no-call boundary.

## Explicit Answers
1. What caused the read_file collapse?
   - Exact read_file symbol extraction rows transitioned to direct-answer fallback (11 exact->direct-answer flips in symbol-name, plus 1 first-function regression), indicating commitment calibration spillover, not task misunderstanding.
2. Why did no-call recovery coincide with direct-answer rebound?
   - The update improved “do not call tools” boundary behavior while increasing plain-text semantic closure on tool-expected extraction prompts.
3. Caution drift vs hesitation vs bifurcation?
   - Best fit is calibration bifurcation with procedural hesitation in read_file extraction slices; not broad global caution drift.
4. Are i10r gains fundamentally unstable?
   - No; they are narrowly calibrated and locally fragile.
5. Is incremental continuation justified?
   - Yes, with rollback-first and narrower remediation. No-go for direct continuation from this checkpoint.
6. Would further localized remediation help or hit diminishing returns?
   - Further localized remediation can help if archetype-matched and counterbalanced; broad no-call additions likely hit diminishing returns quickly.
7. Most likely safe next direction?
   - Rollback to i10r microprobe + ultra-narrow read_file symbol-name commitment-preservation remediation paired with no-call boundary examples.
8. Most dangerous next direction?
   - Additional no-call restoration expansion from the current checkpoint without read_file commitment safeguards.
