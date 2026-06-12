# Phase U Completion Report

## Executive Summary

Phase U completed the controlled execution of the Phase T schema-repair micro-patch.

The run is scientifically useful because it cleanly separates safety from capability:

- safety improved and remained perfect on the no-call surfaces,
- tool-call capability collapsed,
- exact JSON stayed at zero,
- and the schema hypothesis was not supported by the treatment.

## Key Findings

- The promoted Phase U run assets resolved cleanly.
- Preflight passed before training.
- Training completed on the 60-row patch.
- Canonical evaluation completed under the frozen contract.
- Contamination stayed clean.
- The adapter did not recover exact JSON, tool-name accuracy, or argument accuracy.
- The failure mode moved from wrapper drift to direct-answer substitution.

## Combined Assessment

Phase U shows that a small schema-focused patch is not enough to recover envelope realization.

The run preserves the safety gains seen in Phase L better than the prior phases, but it does not restore H1/H2-style tool-call competence.

## Baseline Comparison

Relative to Phase Q:

- exact JSON validity: `0.0` vs `0.03`
- tool-name accuracy: `0.0` vs `0.0714`
- argument accuracy: `0.0` vs `0.0429`
- wrapper leakage: `0.0` vs `0.0`
- no-call correctness: `1.0` vs `0.7667`
- adversarial no-call correctness: `1.0` vs `0.3`

Relative to H1/H2:

- Phase U does not recover any capability metric.
- Phase U is safer than H1/H2 on the no-call surfaces.
- Phase U is much weaker than H1/H2 on tool-call realization.

## Readiness / Promotion Determination

**Do Not Promote**

This is not a promotable tool-call candidate because it does not produce exact tool-call outputs on the frozen canonical contract.

## Recommended Next Action

Do not iterate on schema-only patching as the next move.

The next analysis should revisit dataset composition, anchor density, and prompt-regime balance together, because the Phase U result suggests that schema realization alone is not the dominant factor.

## Confidence Assessment

High confidence in the safety result.

High confidence that the schema hypothesis is not supported by this experiment.

Moderate confidence that the next useful direction is broader dataset redesign rather than another micro-patch.

