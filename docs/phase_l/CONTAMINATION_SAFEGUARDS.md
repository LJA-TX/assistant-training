# Contamination Safeguards

## Scope

Phase L must preserve the contamination-clean state established in Phase K.

## Required Safeguards

1. Keep the Dataset v1.1 train and val splits fixed.
2. Use only the frozen canonical eval manifest and frozen canonical eval files.
3. Require zero prompt overlap, zero target overlap, and zero case-id overlap against `heldout_validation` and `tool_holdout`.
4. Preserve the extra zero-overlap margin already demonstrated against `no_call`, `adversarial`, and `direct_answer`.
5. Treat any reuse of canonical eval answers, prompts, or case IDs as a hard stop.
6. Do not use the strong-system-prompt override for promotion.
7. Do not change decode defaults, scorer semantics, or eval topology.
8. Do not silently rebuild the dataset under the same file names.

## Validated Evidence

The Phase K leakage report already shows zero overlap for every requested comparison set:

- `heldout_validation`
- `tool_holdout`
- `no_call`
- `adversarial`
- `direct_answer`

That evidence is the contamination baseline for Phase L.

## Operational Rules

1. Read canonical eval files as read-only inputs.
2. Compare by file identity and semantic content, not by label alone.
3. Preserve dataset provenance through the draft config and run manifest.
4. Stop immediately if any overlap becomes nonzero.

## Why This Matters

The whole Phase L claim depends on comparing a new training result to a frozen evaluation contract.
If the train split leaks into the eval splits, the comparison is invalid even if the metrics look strong.
