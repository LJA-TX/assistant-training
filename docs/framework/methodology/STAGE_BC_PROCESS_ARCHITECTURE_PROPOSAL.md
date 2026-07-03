# Stage B/C Process Architecture Proposal

## Scope

This document proposes a concrete architecture for extracting stable workflow mechanics identified during Stage B/C process analysis.

This is a design artifact only. It does not create or modify `AGENTS.md`, protocol files, templates, checklists, repository structure, evaluator code, or governance doctrine.

## Inputs

Primary inputs:

- `docs/convergence/STAGE_BC_PROCESS_EXTRACTION_ASSESSMENT.md`
- Stage B closure/readiness/exit artifacts in `docs/convergence/STAGE_B_*.md`
- Stage C0-C8 implementation, conformance, migration-gate, and review artifacts in `docs/convergence/STAGE_C*.md`
- Existing review-bundle and publication hygiene workflow patterns

## 1. AGENTS.md Dispatcher Architecture

## Objective

Define a minimal dispatcher that routes execution requests to the right reusable process components while preserving governance boundaries.

## Responsibilities

`AGENTS.md` should:

1. classify request type into process families,
2. enforce pre-flight governance checks before work starts,
3. route to the correct protocol/template/checklist references,
4. define override hierarchy for authority artifacts,
5. enforce "stop and escalate" conditions when contradictions are detected.

## Routing Behavior

Minimal routing domains:

1. slice execution,
2. readiness/transition review,
3. closure/exit review,
4. migration gate,
5. publication/push checkpoint,
6. architecture/review-only assessment.

Each route should specify:

1. required inputs,
2. required outputs,
3. required checks,
4. prohibited actions.

## Trigger Concepts

Trigger concepts should be intent-driven, not filename-driven:

1. "author fixtures" -> slice execution route,
2. "assess readiness/closure" -> gate-review route,
3. "publish/push" -> publication route,
4. "migration safety" -> migration-gate route,
5. "review architecture/process" -> assessment route.

## Reference Model

Dispatcher reference order:

1. authoritative catalogs and planning artifacts,
2. doctrine/governance artifacts,
3. stage-level closure/readiness determinations,
4. route-specific protocol,
5. output templates/checklists.

## Boundaries

`AGENTS.md` should remain thin. It must not embed:

1. family-specific doctrine interpretations,
2. scenario catalogs or scenario-level mappings,
3. migration-semantic resolution logic,
4. large report templates,
5. command-by-command operational scripts.

## 2. Protocol Library Architecture

## Structure

Proposed protocol classes:

1. readiness gate protocol,
2. closure gate protocol,
3. migration gate protocol,
4. publication checkpoint protocol,
5. push checkpoint protocol,
6. implementation-slice conformance protocol.

## Protocol Class Definitions

| Protocol Class | Purpose | Scope | Stability | Extraction Readiness |
|---|---|---|---|---|
| Readiness Gate | Determine if a new execution phase/slice may begin | Inputs completeness, authority alignment, unresolved blockers | mostly stable | ready (Phase 2) |
| Closure Gate | Determine if a package/family/stage is complete and internally reconciled | coverage, reconciliation, doctrine consistency, unresolved concerns | mostly stable | ready (Phase 2) |
| Migration Gate | Decide if bounded migration can proceed safely | inventory, mapping, blocker classification, safety determination | still evolving | partial (Phase 3) |
| Publication Checkpoint | Verify repository publication hygiene before push authorization | clean tree, unintended files, artifact leakage, documentation consistency | stable | ready (Phase 1/2) |
| Push Checkpoint | Verify and execute bounded push operation safely | reviewed head, sync checks, push verification, anomaly detection | stable | ready (Phase 1/2) |
| Implementation-Slice Conformance | Normalize C-stage conformance decision process | conformance targets, validations, guardrails, determination | mostly stable | ready (Phase 2) |

## Protocol Boundaries

Protocols should define decision sequences and required evidence classes, but not:

1. family/scenario policy semantics,
2. dynamic implementation details for evolving migration blockers,
3. doctrine changes.

## 3. Template Library Architecture

## Template Categories

Proposed categories:

1. coverage summary template,
2. reconciliation summary template,
3. package review template,
4. conformance report template,
5. implementation-slice report template,
6. closure determination template,
7. readiness determination template.

## Ownership Model

1. Process owner: maintains structure and mandatory sections.
2. Domain owner: validates doctrine consistency of populated content.
3. Execution owner: fills run-specific evidence and determinations.

## Intended Use

Templates should be used for high-repeat reporting patterns only, especially where section heading recurrence is high (`Scope`, `Summary Determination`, `Boundary Confirmation`, `Validation Results`).

## Lifecycle

1. versioned baseline templates,
2. low-frequency controlled updates,
3. compatibility notes when section contracts change,
4. periodic drift review against produced artifacts.

## Boundaries

Templates should not encode policy outcomes; they only structure evidence and decisions.

## 4. Checklist Library Architecture

## Checklist Categories

1. review ZIP workflow checklist,
2. git-ignore verification checklist,
3. publication-readiness checklist,
4. push-readiness checklist,
5. repository hygiene checklist,
6. governance boundary checklist,
7. validation evidence checklist.

## Scope and Trigger Conditions

| Checklist | Scope | Trigger Condition | Extraction Readiness |
|---|---|---|---|
| ZIP Workflow | bundle generation and containment path rules | any review/execution slice requiring bundle output | ready (Phase 1) |
| Git-Ignore Verification | ensure bundles/temp outputs are not tracked or staged | any bundle generation or temp-artifact run | ready (Phase 1) |
| Publication Readiness | pre-push hygiene and consistency checks | publication-readiness review requests | ready (Phase 1) |
| Push Readiness | pre/post push safety checks | authorized push operations | ready (Phase 1) |
| Hygiene Review | detect unintended tracked/staged artifacts | any closure or publication boundary | ready (Phase 1) |
| Governance Boundary | verify no prohibited workstream expansion | all execution slices | ready (Phase 1/2) |
| Validation Evidence | confirm required validations were executed and reported | implementation slices and conformance slices | ready (Phase 2) |

## Boundaries

Checklists should remain operational and binary; they should not contain doctrinal interpretation logic.

## 5. Interaction Model

## Invocation Flow

1. Request enters via dispatcher (`AGENTS.md`).
2. Dispatcher selects process route and required protocol.
3. Protocol defines decision sequence and evidence requirements.
4. Template defines output artifact structure.
5. Checklist enforces execution hygiene and boundary compliance.
6. Final determination emitted with explicit evidence trace.

## Decision Flow

1. Pre-flight authority and scope checks.
2. Route-specific protocol decision steps.
3. Structured reporting via template.
4. Operational verification via checklists.
5. Final governance gate: pass/hold/escalate.

## Override Behavior

Override order should be explicit:

1. authoritative catalog/planning artifacts,
2. doctrine/governance artifacts,
3. stage-level determinations,
4. protocol requirements,
5. template/checklist defaults.

If conflict occurs at any layer, lower layers cannot override higher layers.

## Governance Boundaries

Interaction model must enforce:

1. no inference/substitution/reconstruction beyond doctrine,
2. no collapsed-state behavior,
3. no scope expansion into unauthorized implementation families,
4. mandatory stop-and-escalate on authority contradictions.

## 6. Adoption Roadmap

## Phase 1: Lowest-Risk Extractions

1. checklist set:
   - ZIP workflow,
   - git-ignore verification,
   - publication readiness,
   - push readiness,
   - hygiene review.
2. template set:
   - coverage summary,
   - reconciliation summary,
   - package review.
3. minimal dispatcher route map (no deep protocol logic).

## Phase 2: Moderate-Risk Extractions

1. readiness gate protocol,
2. closure gate protocol,
3. implementation-slice conformance protocol,
4. readiness/closure/conformance template normalization.

## Phase 3: Deferred Extractions

1. migration gate protocol deepening for detector/threshold transition,
2. comparability migration decision protocol,
3. authoritative migration execution runbooks.

## Items That Should Remain Prompt-Driven (Now)

1. unresolved detector migration blocker resolution,
2. no-anchor share semantic-equivalence decisions,
3. baseline-delta comparability gating semantics,
4. any new doctrine interpretation not yet stabilized by accepted gates.

## 7. Risk Assessment And Mitigations

## Over-Centralization Risks

Risks:

1. single dispatcher becoming brittle bottleneck,
2. reduced adaptability for edge-case slices.

Mitigations:

1. keep dispatcher minimal and route-only,
2. keep domain decisions in protocols, not dispatcher,
3. allow explicit exception path with required rationale.

## Process Ossification Risks

Risks:

1. freezing currently evolving migration semantics,
2. template-driven behavior replacing critical judgment.

Mitigations:

1. defer evolving areas to prompt-driven handling,
2. add periodic stability reassessment gates,
3. require evidence-backed deviations when protocols are not yet mature.

## Governance Drift Risks

Risks:

1. omitted boundary checks in manual prompt variants,
2. inconsistent stop-condition enforcement.

Mitigations:

1. centralize boundary checklists early,
2. embed mandatory pre-flight and pre-close checks in each route,
3. require explicit unresolved-issue reporting in every determination artifact.

## Maintenance Burden Risks

Risks:

1. too many protocol/template versions,
2. divergence between process assets and actual practice.

Mitigations:

1. keep initial asset set small,
2. assign ownership per asset class,
3. run periodic drift audits against produced artifacts,
4. retire unused assets aggressively.

## Recommendation Summary

1. adopt a hybrid architecture with minimal dispatcher + bounded protocol set + lightweight templates/checklists,
2. prioritize Phase 1 extraction to reduce immediate prompt burden,
3. defer migration-semantic extraction until C7 blocker classes are resolved,
4. preserve authority/doctrine override hierarchy as a non-negotiable control surface.

## Governance Concerns

No new governance contradictions were found in this proposal slice.

Primary forward concern remains governance drift from repeated manual prompt boilerplate if stable controls are not extracted in Phase 1.
