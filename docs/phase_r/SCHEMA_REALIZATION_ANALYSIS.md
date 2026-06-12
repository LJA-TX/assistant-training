# Schema Realization Analysis

## Question

Why did H1/H2 produce strong exact-JSON and tool-call metrics while `v1.1` and `v1.2` did not?

## Evidence Summary

H1/H2 reached:

- exact JSON validity `0.44` / `0.48`
- tool-name accuracy `0.7143` / `0.7714`
- argument accuracy `0.6286` / `0.6929`
- heldout-validation exact-valid `0.64` / `0.75`

Phase Q on `v1.2` only reached:

- exact JSON validity `0.03`
- tool-name accuracy `0.0714`
- argument accuracy `0.0429`
- heldout-validation exact-valid `0.06`

Sources:

- [H1 checkpoint](/opt/ai-stack/assistant-training/docs/phase_ix/H1_EXCEPTION_CHECKPOINT_REPORT.md)
- [H2 checkpoint](/opt/ai-stack/assistant-training/docs/phase_i/H2_CHECKPOINT_REPORT.md)
- [Phase Q execution review](/opt/ai-stack/assistant-training/docs/phase_q/PHASE_Q_EXECUTION_REVIEW.md)

## What H1/H2 Taught

H1/H2 taught the model a narrow realization regime:

- the positive rows are single-call `tool_calls` examples;
- the system prompt repeatedly demands exact tool output;
- the tool-call surface is concentrated on a small set of anchors;
- the non-tool rows stay frozen on the same control scaffold.

That combination makes the model practice the same output contract over and over.

## What v1.1/v1.2 Taught Instead

The later datasets broadened the realization regime:

- v1.1 spreads tool positives across 8 evenly balanced prompt styles;
- v1.2 does the same, even though it restores some anchor weighting;
- both datasets include more explicit safety calibration than the H1/H2 patch runs;
- both move away from the narrow exact-envelope cue that H1/H2 reinforced.

This matters because the evaluation contract is not asking for "some JSON-like function object." It is asking for a strict `tool_calls` envelope.

## Why This Looks Like Schema Realization, Not Just Semantics

Phase Q shows the failure mode clearly:

- `94` failures were classified as near-canonical wrapper or envelope drift.
- `77` of those parsed as bare JSON objects with top-level keys `function` and `type`.
- `7` parsed as `enabled_tools` objects.
- `4` even contained a `tool_calls` key but still failed schema.

That means the model is not merely selecting the wrong tool. It is often choosing the correct tool semantics but realizing the wrong outer schema.

The drift is concentrated on the core anchors:

- `rg_search`
- `read_file`
- `find_files`
- `debug_tools`
- `run_command`

Those five account for `59/94` of the wrapper-drift failures.

## Interpretation

The strongest reading is:

- H1/H2 provided stronger realization training because they repeatedly enforced the exact envelope on a narrow control surface.
- v1.1/v1.2 diluted that realization signal by broadening prompt styles and composition, which increased semantic coverage but weakened exact schema commitment.
- The later datasets therefore know more about tool semantics in the abstract, but less about the strict outer wrapper required by the frozen evaluator.

## Practical Implication

If the next experiment wants exact JSON recovery, it should train schema realization directly:

- fewer prompt styles,
- more repeated canonical `tool_calls` examples,
- tighter anchor concentration,
- and a frozen control scaffold.

The current evidence does not support another broad hybrid before that narrower problem is fixed.
