# Stage B Lessons Learned Summary

## Scope

This document captures governance and execution lessons from Stage B planning, fixture authoring, readiness/exit review, and closure slices.

This is documentation-only summary. It does not author fixtures or implement schemas, validators, scorers, evaluators, runtimes, detectors, or governance redesign.

## Lessons Learned

## 1. Authority Control Must Stay Explicit

- The authoritative scenario catalog must remain the source of truth for scenario IDs, expected states, and detector treatment.
- Execution prompts can drift; they must not remap approved IDs without explicit planning authority.
- B1-NI reconciliation showed that contradiction handling should stop execution, reconcile authority, then resume.

## 2. Non-Inference Doctrine Must Be Fixture-Tested

- Detector behavior must consume emitted facts only.
- No inference from prompt text, path naming, report naming, historical artifacts, or marker absence should be allowed.
- Family-specific and cross-family NI slices materially reduced governance risk before implementation.

## 3. Missing Means Missing

- Missing-state scenarios must preserve noncomputability.
- Substitution, reconstruction, alternate-source replacement, and denominator backfill create governance drift and were correctly rejected.
- Partial versus missing distinction remained operationally important for validation design.

## 4. Comparability Requires Separate Governance

- Current-run computability does not imply baseline comparability.
- Explicit comparability states prevented collapse of `comparison-blocked`, `bridge-required`, and `reference-only` into a single status.
- Bridge requirements and reference-only constraints should remain first-class fields in future implementation contracts.

## 5. Reconciliation Integrity Is Denominator-Critical

- Count, denominator, and rate triads must be verified together.
- Parent-family and governed-sub-slice denominator relationships need explicit validation and visibility.
- Small-denominator visibility should remain mandatory to avoid silent volatility masking.

## 6. Slice-Based Closure Improves Control

- Bounded execution slices with package review and reconciliation checkpoints improved auditability and rollback clarity.
- Per-slice review ZIP bundles enabled fast external review without polluting git history.
- Documentation-only closure checkpoints prevented accidental scope expansion into implementation surfaces.

## Carry-Forward Recommendations

1. Keep authority-reconciliation checks mandatory when prompts and catalog appear misaligned.
2. Preserve non-inference and non-substitution requirements as hard implementation acceptance criteria.
3. Keep comparability-state distinctions explicit in schema and validator contracts.
4. Require denominator-provenance checks for every governed rate before declaring computability or comparability.
5. Continue bounded-slice closure packaging for future Stage B milestone and Stage C transition work.
