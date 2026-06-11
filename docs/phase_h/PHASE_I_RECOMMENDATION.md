# Phase I Recommendation

## Recommendation

**H1: Internal proving experiment only**

## Why H1

This is the most defensible next action after Phase G and Phase H.

### Why not H2 now

`H2` would combine proving with bounded implementation, but the point of the next phase is to discover which intervention class deserves implementation effort.

The current evidence is still not specific enough to justify building the wrong thing.

### Why not H3 now

Proceeding directly to Dataset v1.1 would skip the exact causal question Phase G raised:

- how much of the remaining deficit is still internal and fixable,
- and which internal lever is worth carrying forward.

That question is not answered by Phase F or Phase G alone.

### Why not H4

No alternative path currently has better evidence than one bounded internal-first proving experiment with hard stop rules.

## Recommended Next Action

Execute the Phase H minimum viable run set:

1. fresh bounded control repro on i3 recovery bytes
2. commitment-only bounded patch
3. diversity-only bounded patch

Then:

- stop early if a clear winner emerges,
- run the schema split only if commitment wins or ties,
- run the methodology-only probe only if content probes remain inconclusive,
- stop internal-only iteration if the matrix does not produce informative lift.

## Support

This recommendation is supported by:

1. Phase G's conclusion that internal recovery helped but did not solve the deficit.
2. Phase G's conclusion that commitment and schema dominate the residual failure profile more than wrong-tool selection.
3. The Phase F and Grok-Build evidence that full Dataset v1.1 work should not begin until the project knows which internal lever actually matters most.

## Confidence

**Medium**

Confidence is not high because the internal source pool remains thin.

Confidence is sufficient because the proposed experiment is cheap, bounded, and likely to answer the most important unresolved question before larger implementation begins.

## Sources Used

- `docs/Phase_H_Work_packages.md`
- `docs/phase_g/COUNTERFACTUAL_ASSESSMENT.md`
- `docs/phase_g/FAILURE_ATTRIBUTION_ANALYSIS.md`
- `docs/phase_g/INTERNAL_VS_EXTERNAL_STRATEGY_ASSESSMENT.md`
