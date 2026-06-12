# Controlled Experiment Design

## Objective

Test whether exact `tool_calls` envelope realization can be repaired with a small schema-focused patch while preserving the current Stage B recovery scaffold.

## Control

The control is the frozen Phase Q / Dataset v1.2 scaffold baseline.

Use the existing baseline metrics as the comparison point:

- exact JSON validity `0.03`
- tool-name accuracy `0.07142857142857142`
- argument accuracy `0.04285714285714286`
- wrapper leakage `0.0`
- `94` near-canonical wrapper or envelope drift failures

## Primary Treatment

### Schema-Repair Micro-Patch

- 60 tool-positive rows
- 12 rows each on `rg_search`, `read_file`, `find_files`, `debug_tools`, and `run_command`
- narrow exact-tool / strict-JSON prompt regime
- single-call `tool_calls` envelope only
- no change to safety rows or the frozen scaffold

## Diagnostic Ablations

### Anchor-Only Patch

Keep the same 60-row core-anchor budget, but remove the explicit schema-repair emphasis.

This tests whether anchor concentration alone explains any improvement.

### Prompt-Regime Patch

Keep the same 60-row core-anchor budget and the same exact envelope target, but broaden the wording and prompt style.

This tests whether prompt style or instruction diversity is the dominant driver.

## Success Criteria

The schema-repair treatment is supported if it outperforms the ablations on the exact failure surface:

- exact JSON validity rises materially above control;
- wrapper drift falls materially below control;
- tool-name and argument accuracy rise together with exact JSON validity;
- safety surfaces remain at or above the frozen scaffold baseline.

Proposed minimum decision threshold:

- at least `+0.10` absolute gain in exact JSON validity over control, or a clearly non-null jump from the `0.03` Phase Q baseline;
- at least a substantial reduction in wrapper drift relative to the `94` Phase Q failures;
- no meaningful regression on no-call or adversarial no-call behavior relative to the control scaffold.

## Stop Rules

Stop the experiment and do not expand it if any of the following occurs:

- contamination appears in any frozen holdout;
- the schema patch fails to improve exact JSON validity at all;
- the schema patch improves tool selection but not envelope realization;
- safety metrics regress beyond the frozen scaffold tolerance;
- the ablations match or outperform the schema patch on exact JSON and wrapper drift.

## Attribution Logic

- If the schema-repair patch wins on exact JSON validity and wrapper drift, schema realization is the dominant bottleneck.
- If the anchor-only patch matches the schema patch, anchor concentration is the more likely driver.
- If the prompt-regime patch matches the schema patch, prompt style and instruction distribution are the more likely driver.
- If none of the small patches move the metrics, the bottleneck is probably larger than a schema-only issue and a broader redesign becomes more plausible.

## Experimental Order

To keep the experiment small:

1. Run the schema-repair micro-patch first.
2. Only if the result is ambiguous, run the anchor-only ablation.
3. Only if ambiguity remains, run the prompt-regime ablation.

This staged structure preserves the smallest possible first test while still allowing attribution if the initial result is not decisive.

