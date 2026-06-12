# Envelope Drift Analysis

## What Failed in Phase Q

The Phase Q adapter did not collapse because it was unable to name tools at all.
It collapsed because it frequently produced the wrong **envelope**.

The key failure profile was:

- `94` near-canonical wrapper or envelope drift failures
- `37` direct-answer substitution failures
- `3` malformed partial JSON failures

Source:

- [Phase Q comparison rows](/opt/ai-stack/assistant-training/evals/runs/phase_q_v1_2_anchor_weighted_hybrid_eval_20260612T101256Z/comparison_rows.jsonl)

## Dominant Drift Shapes

Among the `94` wrapper-drift failures:

- `77` were bare JSON objects with top-level keys `function` and `type`
- `7` were `enabled_tools` objects
- `4` contained top-level `tool_calls` but still failed schema
- `4` were other object shapes such as `archive_path` or `functions`

That is not random noise. It is a family of near-misses around the tool-call envelope.

## Tool Concentration

The drift is not confined to edge tools.

`59/94` failures hit the five core anchors:

- `rg_search`
- `read_file`
- `find_files`
- `debug_tools`
- `run_command`

Within the wrapper-drift set, the largest counts were:

- `rg_search`: `31`
- `find_files`: `12`
- `debug_tools`: `7`
- `read_file`: `6`
- `check_service_health`: `6`
- `get_system_datetime`: `6`

That is important because it means the model is not only failing on unfamiliar tails. It is failing on the canonical anchor tools too.

## Comparison to H1/H2

H1 and H2 had much smaller envelope-drift counts:

- H1: `32`
- H2: `29`

They also had stronger exact JSON validity:

- H1: `0.44`
- H2: `0.48`

Phase Q is materially worse:

- exact JSON validity: `0.03`
- wrapper drift: `94`

So the Phase Q problem is not just "a little more noise." It is a much broader failure to realize the outer schema.

## What the Drift Suggests

The model appears to be learning one of several near-canonical but invalid envelopes:

- a single-call `function` object instead of a `tool_calls` array,
- a routing-style metadata object,
- or a partially nested wrapper.

That points to a realization deficit, not a tool-selection deficit.

## Conclusion

The envelope drift is the clearest evidence that future work should target:

- exact schema realization,
- not just more tool coverage,
- and not just more safety calibration.

The later datasets recovered some tool semantics, but they did not consistently teach the outer `tool_calls` envelope that the frozen contract requires.
