# Process Dispatcher Skeleton (Phase 1)

## Purpose

This file provides a minimal routing skeleton for recurring Stage B/C process work.
It is intentionally thin and route-oriented.

## Authority Order

Use this precedence order whenever inputs conflict:

1. Authoritative catalogs and planning artifacts
2. Governance/doctrine artifacts
3. Accepted stage/family readiness or closure determinations
4. Route-specific process assets (checklists/templates)
5. Prompt-local defaults

Lower levels must not override higher levels.

## Pre-Flight Checks (All Routes)

Run these checks before execution:

1. Confirm request classification and bounded scope.
2. Confirm ownership/authority inputs are identified.
3. Check for stop-and-escalate conditions.
4. Apply baseline hygiene checks:
   - `docs/process_infrastructure/checklists/hygiene_review_checklist.md`
   - `docs/process_infrastructure/checklists/governance_boundary_verification_checklist.md`
   - `docs/process_infrastructure/checklists/git_ignore_verification_checklist.md` (when temporary bundles/artifacts are created)

## Route Selection

| Route | Trigger Intent | Primary Assets |
|---|---|---|
| `slice_execution` | author bounded execution slice outputs | package review, coverage summary, reconciliation summary templates; review-package completeness, ZIP, and hygiene checklists |
| `readiness_or_closure_review` | readiness/exit/closure assessment requests | readiness determination, transition readiness assessment, closure determination templates; review-package completeness and hygiene checklists |
| `conformance_slice` | implementation conformance/reporting slice | conformance report and implementation summary templates; validation evidence and hygiene checklists |
| `publication_checkpoint` | publication-readiness verification | publication-readiness checklist; hygiene and governance-boundary checklists |
| `push_checkpoint` | authorized push operations | push-readiness checklist; git-ignore verification checklist |
| `milestone_determination` | milestone checkpoint determinations | milestone determination template; validation evidence and hygiene checklists |
| `architecture_or_process_assessment` | architecture/process-only assessments | implementation summary template (structure-only) plus hygiene checklist |

## Stop-And-Escalate Triggers

Stop and escalate when any of the following appears:

1. Authority conflict
2. Catalog contradiction
3. Undefined ownership
4. Scope expansion beyond authorized slice
5. Methodology redesign decision request
6. Repository anomaly

## Boundaries

This dispatcher must not contain:

1. Doctrine specifics
2. Scenario catalog content
3. Migration semantics or migration procedures
4. Protocol bodies
5. Template bodies
6. Checklist bodies

## Status

Phase 1 extraction provides dispatcher routing + references to checklists/templates only.
Protocol library extraction remains deferred to later phases.
