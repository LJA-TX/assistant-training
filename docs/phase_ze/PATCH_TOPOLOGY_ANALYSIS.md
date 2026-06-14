# Patch Topology Analysis

## Question

What remains untested after Phase ZD?

## Answer

The remaining untested property is the **patch-local replacement topology** of the successful H1/H2-style patch: how a fixed positive-row budget is distributed across the frozen scaffold.

Phase ZD eliminated schema-only repair and weakened anchor concentration as a sole explanation. What is still plausible is that H1/H2 depended on the geometry of a small positive patch, not just on its anchor share.

## Evidence

### H1 and H2 were small patches, not full rewrites

Both successful runs modified only `100` tool-positive rows on top of a frozen Stage B recovery scaffold.

| Run | Patch rows | Train rows | Patch / train | Non-tool slices |
|---|---:|---:|---:|---|
| H1 | `100` | `2160` | `4.63%` | Frozen |
| H2 | `100` | `2160` | `4.63%` | Frozen |

### Their row-placement footprint was compact

The patched rows were not spread across the full corpus.

| Run | Min position | Max position | Span | Span / train | Mean gap | Median gap |
|---|---:|---:|---:|---:|---:|---:|
| H1 | `2` | `467` | `466` | `21.6%` | `4.7` | `4` |
| H2 | `3` | `430` | `428` | `19.8%` | `4.31` | `4` |

That is the topology signal: a small patch, confined to a bounded span, on a frozen scaffold.

### The patch composition was also anchored, but composition has already been tested

The successful patches already showed:

- exact-tool-request cue retention on the positive rows,
- a fixed small patch budget,
- anchor-heavy positive composition,
- and a frozen validation contract.

Phase ZD and the completed anchor sweep showed that anchor concentration alone is not sufficient.

## What Later Interventions Changed

- Phase L rebuilt a full v1.1 corpus and lost capability.
- Phase Q rebuilt v1.2 with anchor weighting and still failed on the frozen contract.
- Phase U fixed schema realization locally and still collapsed into direct answers.
- The Z-series anchor sweep varied anchor concentration but not the patch-local topology question.

## Conclusion

Patch-local replacement topology remains the last unresolved causal variable because the successful H1/H2 runs preserved a small positive patch on a frozen scaffold, while the later interventions changed the topology of the intervention in broader ways.

The next experiment should therefore vary **only** footprint geometry while holding the rest fixed.
