# Minimum Intervention Analysis

## Question

What is the smallest scientifically defensible experiment that can test whether schema realization is the dominant remaining bottleneck?

## Working Conclusion

The smallest defensible intervention is a **60-row schema-repair micro-patch** applied on top of the frozen Stage B recovery scaffold.

## Why 60 Rows

The row count needs to be small enough to preserve attribution, but large enough to make a non-trivial schema signal visible.

60 rows is the best compromise because:

- it is materially smaller than the 100-row H1 and H2 patches that produced the strongest schema-realization signals;
- it still gives repeated exposure to every failure-prone core anchor;
- it allows a balanced split of 12 rows each across `rg_search`, `read_file`, `find_files`, `debug_tools`, and `run_command`;
- it keeps the non-tool surface frozen, so any movement can be attributed to the schema patch rather than broad dataset redesign.

Below 60 rows, the design becomes hard to defend as anything other than a pilot, because the model may simply not receive enough repeated exact-envelope examples to move the needle.

## Why The Five Core Anchors

Phase Q shows that the wrapper/envelope drift failures are concentrated on the same five anchors:

- `rg_search`
- `read_file`
- `find_files`
- `debug_tools`
- `run_command`

Those five account for `59/94` of the near-canonical wrapper drift failures in Phase Q.

That makes them the most informative targets for a minimal schema patch.

Using only those anchors keeps the experiment focused on the envelope realization problem instead of mixing in long-tail tool coverage.

## Why The Non-Tool Surface Must Stay Frozen

The current question is not whether the model can learn more tools in general.

It is whether the `tool_calls` envelope can be repaired with a small schema-focused patch while preserving the existing scaffold.

Therefore the patch should leave unchanged:

- the refusal and no-call rows;
- the safety calibration rows;
- the runtime alignment rows;
- the underlying trainer geometry;
- the evaluator and scoring contract.

## Why Smaller Than A Full Redesign

A full redesign would confound the causal question.

It would change:

- density,
- anchor concentration,
- prompt regime,
- and safety calibration

all at once.

That makes it a remediation candidate, not a clean test of the schema-realization hypothesis.

## Minimum Intervention Definition

The minimum intervention is:

1. a 60-row tool-positive patch;
2. restricted to the five core anchors;
3. using one canonical tool-call per row;
4. serialized in the exact `tool_calls` envelope;
5. with the rest of the scaffold left frozen.

## Minimum Intervention Risk

The main risk is underpowering a negative result.

If the patch is too small to move exact JSON validity, that does not automatically falsify schema realization. It may simply mean the patch was too short to teach the envelope.

For that reason, the 60-row proposal should be treated as the smallest defensible test, not as a final production recipe.

