# Corrective Action Analysis

## Executive Summary

The evidence most strongly supports **dataset redesign and dataset rebalancing**.

Not evaluator review.
Not scoring review.
Not trainer-geometry change.

The frozen evaluation contract is behaving consistently.
The model is failing because the training signal is not producing tool-call realization at the required density.

## Options Assessed

| Option | Support level | Reason |
|---|---|---|
| Dataset redesign | Strongest support | The training mix is the only major surface that changed relative to the H1/H2 baseline shape. |
| Dataset rebalancing | Strongest support | Tool-positive density fell, safety density rose, and tool families were flattened across the same small budget. |
| Training-configuration adjustment | Secondary support | Geometry was stable, so config changes are not the primary fix, but more exposure to the right examples could help after a dataset fix. |
| Evaluation review | Weak support | The frozen manifest and row-level outputs are internally consistent. |
| Methodology review | Weak support | No evidence of scoring drift or evaluator inconsistency appears in the repository. |
| Another intervention | Moderate support | A staged safety-calibration design or a two-phase curriculum could be justified if it preserves tool-call density better. |

## Why Dataset Redesign Is The Primary Fix

The dataset is the only major control surface that changed in a way that lines up with the failure:

- tool-positive rows decreased,
- safety-calibration rows increased,
- tool distribution became flatter,
- the model learned safety exactly and capability not at all.

This is a dataset-shape problem first.

## Why Rebalancing Is The Primary Subtype

The problem is not simply "too much data" or "bad data."
It is the mixture:

- Phase L preserved safety by adding or emphasizing safety rows,
- but it reduced repeated positive tool-call pressure,
- and that appears to have erased the schema skill.

The corrective move is therefore to rebalance toward stronger tool-positive density while keeping the safety rows exact and auditable.

## What Not To Do

- Do not change evaluators to chase a better score.
- Do not change scoring to make the run look promotable.
- Do not alter the frozen canonical manifest.
- Do not treat the current failure as evidence that the safety rows were useless; they clearly worked.

## Recommended Direction

The most evidence-backed next move is a new dataset-design pass that:

- restores more repeated tool-call supervision,
- keeps explicit safety-calibration rows,
- preserves the contamination-safe split discipline,
- and avoids flattening the tool distribution so far that the model underfits the core envelope.

If a training-configuration adjustment is later considered, it should be a follow-on to the dataset redesign, not a substitute for it.

## Sources Used

- `docs/phase_l/PHASE_L_EXECUTION_REVIEW.md`
- `docs/phase_k/DATASET_V1_1_COMPOSITION_ANALYSIS.md`
- `docs/phase_k/CONTAMINATION_VALIDATION_REPORT.md`
- `docs/phase_j/DATASET_V1_1_DESIGN_REQUIREMENTS.md`
- `evals/runs/phase_l_v1_1_external_first_eval_20260611T153900Z/summary.json`
