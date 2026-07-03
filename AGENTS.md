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
   - `docs/framework/process_infrastructure/checklists/hygiene_review_checklist.md`
   - `docs/framework/process_infrastructure/checklists/governance_boundary_verification_checklist.md`
   - `docs/framework/process_infrastructure/checklists/git_ignore_verification_checklist.md` (when temporary bundles/artifacts are created)

## Route Selection

| Route | Trigger Intent | Primary Assets |
|---|---|---|
| `slice_execution` | author bounded execution slice outputs | `docs/framework/process_infrastructure/templates/package_review_template.md`; `docs/framework/process_infrastructure/templates/coverage_summary_template.md`; `docs/framework/process_infrastructure/templates/reconciliation_summary_template.md`; `docs/framework/process_infrastructure/checklists/review_package_completeness_checklist.md`; `docs/framework/process_infrastructure/checklists/zip_workflow_checklist.md`; `docs/framework/process_infrastructure/checklists/hygiene_review_checklist.md` |
| `readiness_or_closure_review` | readiness/exit/closure assessment requests | `docs/framework/process_infrastructure/templates/readiness_determination_template.md`; `docs/framework/process_infrastructure/templates/transition_readiness_assessment_template.md`; `docs/framework/process_infrastructure/templates/closure_determination_template.md`; `docs/framework/process_infrastructure/checklists/review_package_completeness_checklist.md`; `docs/framework/process_infrastructure/checklists/hygiene_review_checklist.md` |
| `conformance_slice` | implementation conformance/reporting slice | `docs/framework/process_infrastructure/templates/conformance_report_template.md`; `docs/framework/process_infrastructure/templates/implementation_summary_template.md`; `docs/framework/process_infrastructure/checklists/validation_evidence_checklist.md`; `docs/framework/process_infrastructure/checklists/hygiene_review_checklist.md` |
| `migration_gate` | migration-readiness or migration-safety gate requests | `docs/framework/process_infrastructure/templates/conformance_report_template.md`; `docs/framework/process_infrastructure/templates/milestone_determination_template.md`; `docs/framework/process_infrastructure/checklists/validation_evidence_checklist.md`; `docs/framework/process_infrastructure/checklists/governance_boundary_verification_checklist.md`; `docs/framework/process_infrastructure/checklists/hygiene_review_checklist.md` |
| `publication_checkpoint` | publication-readiness verification | `docs/framework/process_infrastructure/checklists/publication_readiness_checklist.md`; `docs/framework/process_infrastructure/checklists/hygiene_review_checklist.md`; `docs/framework/process_infrastructure/checklists/governance_boundary_verification_checklist.md` |
| `push_checkpoint` | authorized push operations | `docs/framework/process_infrastructure/checklists/push_readiness_checklist.md`; `docs/framework/process_infrastructure/checklists/git_ignore_verification_checklist.md`; `docs/current/status/COMMIT_AND_PUSH_PROCEDURE.md` |
| `milestone_determination` | milestone checkpoint determinations | `docs/framework/process_infrastructure/templates/milestone_determination_template.md`; `docs/framework/process_infrastructure/checklists/validation_evidence_checklist.md`; `docs/framework/process_infrastructure/checklists/hygiene_review_checklist.md` |
| `architecture_or_process_assessment` | architecture/process-only assessments | `docs/framework/process_infrastructure/templates/implementation_summary_template.md`; `docs/framework/process_infrastructure/checklists/hygiene_review_checklist.md` |

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
After each completed canonical run or probe, update `docs/current/status/TRAINING_RUN_HISTORY.md` before closing out the work.
