# Gen-2 Scope Boundary Assessment

Date: 2026-06-21

## Scope

This document provides a documentation-only scope assessment for a prospective Gen-2 program.

Its purpose is to define what an explanatory-comparability and observability Gen-2 program is and is not.

This document does **not** authorize:

- D2 planning;
- experiment design;
- treatment-arm design;
- run planning;
- manifests;
- preregistrations;
- execution;
- governance reinterpretation.

`Gen-2` remains a strategic program label only.
It does not replace the repository's existing stage, blocker, or family terminology.

## Inputs

- [GEN2_PROSPECTIVE_EVIDENCE_PROGRAM_ASSESSMENT.md](./GEN2_PROSPECTIVE_EVIDENCE_PROGRAM_ASSESSMENT.md)
- [GEN2_STRATEGIC_DIRECTION_OPTIONS_ASSESSMENT.md](./GEN2_STRATEGIC_DIRECTION_OPTIONS_ASSESSMENT.md)
- [D1_CLOSURE_AND_D2_READINESS_ASSESSMENT.md](./D1_CLOSURE_AND_D2_READINESS_ASSESSMENT.md)
- [../current_status.md](../current_status.md)
- [../project_outcomes_to_date.md](../project_outcomes_to_date.md)
- [../../continuity/D0_TO_CURRENT_TREE_MECHANISM_ISOLATION_GOVERNANCE.md](../../continuity/D0_TO_CURRENT_TREE_MECHANISM_ISOLATION_GOVERNANCE.md)
- [../../continuity/D1_GOVERNANCE_FOUNDATION_PACKAGE.md](../../continuity/D1_GOVERNANCE_FOUNDATION_PACKAGE.md)
- [../../continuity/STAGE_C_CLOSURE_CONTINUITY_PACKAGE.md](../../continuity/STAGE_C_CLOSURE_CONTINUITY_PACKAGE.md)
- [../../goal_charter_v5a.md](../../goal_charter_v5a.md)
- [../../appendix_a_operational_execution_contract_v3a.md](../../appendix_a_operational_execution_contract_v3a.md)
- [../../metric_specification_v1a.md](../../metric_specification_v1a.md)

## Executive Determination

If explanatory-comparability and observability are the preferred Gen-2 identity, then Gen-2 is not defined by execution, optimization, reconstruction, or replay.

It is defined by:

- disciplined comparison between current-tree behavior and preserved reference evidence;
- explicit evidence framing and claim-tier discipline;
- provenance and observability preservation at source; and
- tradeoff-aware explanation of strong structured tool-calling behavior.

The necessary scope model is therefore three-part:

1. work that belongs inside the Gen-2 identity;
2. work that may support Gen-2 but should remain outside its identity;
3. work that directly conflicts with the Gen-2 identity and must remain excluded.

## Why Scope Boundaries Are Necessary

These boundaries exist for four reasons:

1. to prevent Gen-2 from collapsing into H1/H2 replay, D0 reconstruction, or benchmark-maximization by inertia;
2. to preserve the D1 governance boundary and frozen-contract discipline;
3. to keep explanation and evidence quality primary over output volume or local metric gains; and
4. to preserve the repository's long-term aim of a reusable methodology rather than a one-off historical reconstruction story.

## 1. Work That Naturally Belongs Inside Gen-2

The following categories of work belong inside an explanatory-comparability Gen-2 identity.

### 1.1 Core explanatory work

- explanatory analysis of strong structured tool-calling behavior and its tradeoffs;
- compare-and-contrast reasoning across current-tree baselines, frozen controls, and observational reference regimes;
- interpretation of which observed differences are descriptive, associative, or plausibly mechanistic;
- explicit treatment of capability, safety, no-call, runtime-discipline, and wrapper-behavior tradeoffs as one explanatory surface.

### 1.2 Core comparability work

- preservation and clarification of comparison classes, control classes, and fixed surfaces;
- analysis of what can and cannot be compared legitimately under the frozen evaluation contract;
- boundary-setting around what historical surfaces mean for current-tree interpretation;
- identification of where interpretations are regime-specific versus method-general.

### 1.3 Core observability work

- definition of what evidence must be captured at source so later interpretation is possible;
- prompt-surface observability rules when prompt construction affects interpretation;
- provenance framing for claim-bearing artifacts;
- preservation of evidence-creation machinery when it is part of the reproducibility boundary.

### 1.4 Core evidence-quality work

- claim-tier discipline;
- explicit confound handling;
- evidence-role separation;
- overclaim prevention;
- contamination and drift awareness as interpretive constraints.

### 1.5 Core methodological inheritance work

- carrying forward durable lessons from Stage C and D1;
- refining what future families should inherit as evidence discipline;
- clarifying what kinds of lessons are ready to be generalized and what remains local.

## 2. Work Adjacent To Gen-2 But Outside Its Identity

The following categories may support Gen-2 or be informed by it, but they should remain outside the Gen-2 identity itself.

### 2.1 General repository support work

- public-package front-door maintenance;
- publication architecture refinement;
- housekeeping, path compatibility, and documentation discoverability work;
- generic infrastructure maintenance.

These may improve readability or durability, but they are not Gen-2's scientific identity.

### 2.2 General execution-preparation work

- future D2 governance packaging;
- future study-design governance templates;
- generic validation tooling;
- generic reporting scaffolds.

These may later support separately authorized work, but they are not themselves explanatory-comparability work.

### 2.3 Broad capability-development work

- model-improvement efforts aimed primarily at raising metrics;
- broad dataset redesign not anchored to an explanatory question;
- training optimization work;
- deployment-oriented or productization-oriented refinements.

These may be future adjacent programs, but they should not define Gen-2.

## 3. Work That Actively Conflicts With The Gen-2 Identity

The following categories conflict with the Gen-2 identity and should remain excluded from it.

### 3.1 Replay and reconstruction identity

- historical replay framing;
- byte-perfect reconstruction as the main scientific agenda;
- treating H1/H2 as targets to be recovered;
- using current-tree outputs as proof of blocked canonical-byte continuity.

### 3.2 Capability-chasing identity

- benchmark-maximization as the primary success criterion;
- execution-first optimization sweeps;
- treating exact JSON gains as sufficient without tradeoff interpretation;
- allowing output volume to substitute for explanatory clarity.

### 3.3 Revisionist evidence practices

- heuristic repair of missing evidence;
- silent contract drift;
- implicit evidence-tier mixing;
- post-hoc reinterpretation that weakens provenance discipline.

### 3.4 Boundary-breaking governance behavior

- D0 blocker downgrades;
- reclassification of H1/H2 into replay targets;
- manifest or hash-claim edits without separate authority;
- design or execution drift under the cover of strategic framing.

## 4. In-Scope Question Classes

The following classes of questions are in-scope for Gen-2.

1. Which strong structured tool-calling behaviors are actually comparable across current-tree and preserved reference surfaces?
2. Which differences appear explanatory, which are merely descriptive, and which remain too confounded to interpret strongly?
3. What provenance and observability are required for later explanation to be trustworthy?
4. Which tradeoffs are structural, which are incidental, and which remain unresolved?
5. Which lessons appear regime-specific and which appear candidates for broader methodological inheritance?
6. How should historical reference regimes constrain present interpretation without becoming replay mandates?

## 5. Out-Of-Scope Question Classes

The following classes of questions are out-of-scope for Gen-2 as such.

1. Which exact treatment arm should be launched?
2. Which run should be executed next?
3. Which manifests or preregistrations should be authored?
4. How should H1/H2 be replayed or reproduced operationally?
5. How can the repository recover or replace blocked canonical bytes?
6. What is the fastest path to a better benchmark score independent of explanation quality?
7. Which deployment or productization path should be pursued?

## 6. Foundational Prerequisites Versus Optional Extensions

### 6.1 Foundational prerequisites

The following are foundational prerequisites for any future Gen-2 activity that claims to belong inside the identity:

- preserved authority order;
- preserved D0 blocker and D1 boundary;
- frozen-contract discipline;
- explicit separation between current-tree baseline and historical reference surfaces;
- H1/H2 compare-only treatment;
- explicit evidence-role framing;
- explicit claim-tier discipline;
- observability at source;
- provenance preservation;
- tradeoff-aware interpretation.

Without these, the program is not explanatory-comparability in a meaningful sense.

### 6.2 Optional extensions

The following are reasonable extensions, but not prerequisites of the identity itself:

- broader cross-family generalization analysis;
- doctrine-elevation threshold analysis;
- expansion of the reference-regime set beyond H1/H2;
- outsider-facing summaries that explain the methodological position to new readers;
- broader comparative methodological synthesis across additional contracts or baselines.

These can strengthen Gen-2, but the identity does not depend on them from day one.

## 7. H1/H2 Treatment Within The Scope Model

H1/H2 should be treated as:

- high-signal observational reference regimes;
- anchor comparators for explanatory work;
- preserved historical evidence surfaces;
- scientific inputs, not scientific destiny.

H1/H2 should **not** be treated as:

- replay targets;
- success targets;
- canonical targets;
- the sole definition of Gen-2;
- substitute proof for current-tree or canonical-byte claims.

This boundary exists because H1/H2 are central evidence objects but not legitimate identity monopolists.

## 8. Identity-Drift Risks

The following future work types would create identity drift.

### 8.1 Mechanism-only narrowing

If Gen-2 is treated as nothing more than a mechanism-isolation hunt for H1/H2, its broader explanatory-comparability identity collapses into a local historical puzzle.

### 8.2 Scoreboard capture

If Gen-2 becomes a better-metrics program, a stronger-checkpoint program, or a benchmark-recovery program, the explanatory and observability core is displaced.

### 8.3 Observability bureaucratization

If Gen-2 becomes only a process or instrumentation program with no substantive explanatory center, its identity becomes procedural rather than scientific.

### 8.4 Historical exceptionalism

If all framing or success language is anchored to one historical regime, Gen-2 loses the reusable-methodology character that justified creating it.

## 9. Governance-Drift Risks

The following future work types would create governance drift.

### 9.1 Boundary erosion

- allowing strategic documents to imply execution authority;
- moving from interpretation into design or run planning without separate authorization;
- introducing operational specificity that belongs to a later governance layer.

### 9.2 Authority erosion

- weakening the D0 blocker;
- overriding frozen-contract discipline informally;
- treating lower-order planning language as if it supersedes current authority surfaces.

### 9.3 Evidence-discipline erosion

- mixing behavioral, provenance, governance, and continuity evidence as if they have equal claim weight;
- permitting post-hoc variables or silent drift in comparison surfaces;
- tolerating ambiguous or missing evidence instead of stopping and preserving the uncertainty boundary.

### 9.4 Labeling erosion

- describing H1/H2 as replay mandates;
- describing comparability work as historical reconstruction;
- describing strategic framing as if it were execution approval.

## 10. Necessary Scope Boundaries To Preserve Explanatory-Comparability Doctrine

To preserve the explanatory-comparability doctrine, the following boundaries are necessary:

1. comparison must remain distinct from replay;
2. explanation must remain distinct from optimization;
3. observability must be captured at source rather than reconstructed later;
4. provenance gaps must remain visible rather than repaired narratively;
5. evidence tiers must remain explicit;
6. tradeoffs must be interpreted jointly rather than selectively;
7. historical reference regimes must remain compare-only;
8. frozen measurement contracts must remain stable unless separately re-governed;
9. strategic framing must remain distinct from operational authorization.

## 11. Scope Summary

In short, Gen-2 is in-scope when the work improves the repository's ability to interpret strong structured tool-calling behavior and its tradeoffs under preserved comparability and preserved provenance.

Gen-2 is outside its identity when the work mainly supports packaging, infrastructure, or generic future execution preparation.

Gen-2 is out-of-bounds when the work turns into replay, reconstruction cleanup, capability chasing, execution planning, or governance boundary erosion.

## Boundary Confirmation

This assessment is documentation-only.

It does not authorize:

- D2 planning or D2 execution;
- experiment design;
- treatment-arm design;
- run planning;
- manifests;
- preregistrations;
- training or evaluation execution; or
- governance reinterpretation.
