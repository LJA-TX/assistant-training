# Phase X Validation Checklist

## 1. Contamination

Verify zero overlap against the frozen canonical evaluation assets:

- heldout validation
- tool holdout
- no-call
- adversarial no-call
- direct-answer

Checks:

- prompt overlap = 0
- target overlap = 0
- case-id overlap = 0

Failure:

- any nonzero overlap is an attribution failure and a hard stop.

## 2. Anchor Concentration

Verify the realized anchor counts for each arm:

- Control: `726`
- Treatment A: `819`
- Treatment B: `912`
- Treatment C: `1011`

Checks:

- core anchor share matches the target arm band,
- all 26 tool families remain represented,
- long-tail mass decreases only as anchor mass increases,
- the change is monotonic across the arms.

Failure:

- anchor counts off target by construction or non-monotonic family allocation.

## 3. Exact-Tool-Request Cue Retention

Verify that every tool-positive row uses the fixed exact-tool-request system prompt template.

Checks:

- 100 percent of tool-positive rows contain the exact cue,
- no alternate cue variants are introduced between arms,
- no arm-specific cue mutation appears in metadata or content.

Failure:

- any tool-positive row without the fixed cue.

## 4. Scaffold Invariance

Verify that the frozen Stage B recovery scaffold is unchanged.

Checks:

- non-tool rows match the frozen scaffold bit-for-bit,
- train and validation row counts remain fixed,
- the same row topology is used across arms,
- the canonical evaluation contract remains unchanged.

Failure:

- any non-tool slice mutation or validation-split drift.

## 5. `tool_calls` Envelope Validity

Verify that every tool-positive assistant row uses the canonical single-call `tool_calls` structure.

Checks:

- exactly one assistant tool call per positive row,
- `tool_calls` is the top-level assistant output envelope,
- no alternative wrapper shape appears,
- no bare `function` or `type` object appears in place of `tool_calls`.

Failure:

- any alternate envelope shape or multi-call structure.

## 6. Safety Block Preservation

Verify that the safety block stays fixed.

Checks:

- train safety rows remain `767`,
- runtime-alignment rows remain `324`,
- no-call-direct-calibration rows remain `216`,
- refusal-calibration rows remain `162`,
- adversarial-no-call-calibration rows remain `65`.

Failure:

- any safety category count changes or any no-call slice is rebuilt.

## 7. Operational Readiness

Verify the standard construction prerequisites:

- all paths resolve,
- the output directory is clean,
- the dataset builder writes the intended arm files only,
- no governance or evaluator files are modified.

Failure:

- any build or path failure before dataset creation.

## Decision Rule

Proceed to training only if all six validation groups pass.

If contamination, cue retention, scaffold invariance, or envelope validity fails, the arm is not scientifically admissible for attribution.
