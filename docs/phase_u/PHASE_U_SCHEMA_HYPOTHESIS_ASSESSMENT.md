# Phase U Schema Hypothesis Assessment

## Determination

**Not Supported**

## Question

Does a small schema-focused intervention materially improve exact tool-call envelope realization relative to the Phase Q baseline?

## Evidence

Phase U used the smallest schema-repair treatment defined in Phase S:

- 60 tool-positive rows,
- 12 each on `rg_search`, `read_file`, `find_files`, `debug_tools`, and `run_command`,
- canonical single-call `tool_calls` envelope,
- frozen Stage B recovery scaffold preserved.

The outcome did not improve envelope realization:

- exact JSON validity: `0.0`
- tool-name accuracy: `0.0`
- argument accuracy: `0.0`
- wrapper leakage: `0.0`
- no-call correctness: `1.0`
- adversarial no-call correctness: `1.0`

Compared with Phase Q:

- exact JSON validity moved from `0.03` to `0.0`
- tool-name accuracy moved from `0.0714` to `0.0`
- argument accuracy moved from `0.0429` to `0.0`
- wrapper leakage stayed at `0.0`
- no-call correctness improved from `0.7667` to `1.0`
- adversarial no-call correctness improved from `0.3` to `1.0`

## Why This Is Not Schema Recovery

The failure surface changed shape:

- Phase Q was dominated by near-canonical wrapper or envelope drift.
- Phase U was dominated by direct-answer substitution.

That means the micro-patch did not teach the correct outer schema. It pushed the model away from wrapper-drift behavior and into direct answers on tool prompts.

## Confidence

High confidence in the negative result.

The experiment preserves safety, but it does not demonstrate that schema realization is the dominant remaining bottleneck.

## Interpretation

The evidence argues that a schema-only micro-patch is insufficient on its own.

If a future intervention is to recover tool-call capability, it likely needs broader composition changes than exact-envelope reinforcement alone.

