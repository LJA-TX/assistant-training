# Gen-2 Prospective Evidence Program Assessment

Date: 2026-06-19

## Scope

This document provides a documentation-only strategic assessment for a prospective second-generation evidence program ("Gen-2").

Its purpose is to define what Gen-2 should fundamentally be about, based on the repository's published Gen-1 state.

This document does **not** authorize D2 planning, training, evaluation execution, experiment design, treatment-arm design, run planning, preregistration creation, manifest edits, hash-claim edits, or governance reinterpretation.

`Gen-2` is used here as a strategic program label only.
It does not replace the repository's existing stage, family, or blocker terminology.

## Inputs

- [current_status.md](../current_status.md)
- [project_outcomes_to_date.md](../project_outcomes_to_date.md)
- [STAGE_B_COMPLETION_DETERMINATION.md](./STAGE_B_COMPLETION_DETERMINATION.md)
- [D1_CLOSURE_AND_D2_READINESS_ASSESSMENT.md](./D1_CLOSURE_AND_D2_READINESS_ASSESSMENT.md)
- [../../continuity/STAGE_C_CLOSURE_CONTINUITY_PACKAGE.md](../../continuity/STAGE_C_CLOSURE_CONTINUITY_PACKAGE.md)
- [../../convergence/STAGE_C_FINAL_DISPOSITION_AND_PUBLICATION_ASSESSMENT.md](../../convergence/STAGE_C_FINAL_DISPOSITION_AND_PUBLICATION_ASSESSMENT.md)
- [../../continuity/D0_TO_CURRENT_TREE_MECHANISM_ISOLATION_GOVERNANCE.md](../../continuity/D0_TO_CURRENT_TREE_MECHANISM_ISOLATION_GOVERNANCE.md)
- [../../continuity/D1_GOVERNANCE_FOUNDATION_PACKAGE.md](../../continuity/D1_GOVERNANCE_FOUNDATION_PACKAGE.md)
- [../../continuity/D1_MECHANISM_HYPOTHESIS_INVENTORY_SPECIFICATION.md](../../continuity/D1_MECHANISM_HYPOTHESIS_INVENTORY_SPECIFICATION.md)
- [../../continuity/D1_MECHANISM_HYPOTHESIS_INVENTORY.md](../../continuity/D1_MECHANISM_HYPOTHESIS_INVENTORY.md)
- [TRAINING_RUN_HISTORY.md](./TRAINING_RUN_HISTORY.md)
- [../baselines/README.md](../baselines/README.md)
- [../baselines/LLAMA31_PROJECT_WIDE_COMPARISON.md](../baselines/LLAMA31_PROJECT_WIDE_COMPARISON.md)
- [../../../evals/canonical_eval_manifest_v1.json](../../../evals/canonical_eval_manifest_v1.json)
- [../../goal_charter_v5a.md](../../goal_charter_v5a.md)
- [../../appendix_a_operational_execution_contract_v3a.md](../../appendix_a_operational_execution_contract_v3a.md)
- [../../metric_specification_v1a.md](../../metric_specification_v1a.md)

## Current Basis

The current repository-backed basis for this assessment is:

- Stage B is complete.
- Stage C is complete and closed as historical work with retained guidance.
- The curated Llama 3.1 baseline evidence package is published.
- D1 is complete and published.
- D0 blocker `D0-BLK-TRAINING-SCRIPT-PROVENANCE-001` remains active.
- D2 mechanism-isolation planning is not authorized.
- The public repository is currently a bounded curated package rather than an open-ended working archive.

## Determination

Gen-2 should be a mechanism-and-observability evidence program.

It should not be framed as:

- a reconstruction-completion program;
- a broad performance-chase program;
- a reopening of Stage C;
- a public-package expansion exercise; or
- an implicit D2 execution program.

The central strategic move for Gen-2 is to convert Gen-1's strongest outputs from descriptive and governance-rich evidence into durable explanatory knowledge with first-class provenance and observability.

## Purpose

Gen-2 should exist to answer the questions that Gen-1 deliberately left open:

- what actually explains the strongest observed tool-call capability regimes;
- which tradeoffs are intrinsic versus incidental;
- which lessons are family-specific versus method-general; and
- what evidence must be captured from day one so future conclusions do not depend on retrospective reconstruction.

## Objectives

1. Clarify the minimal explanatory surfaces behind H1/H2-class exact tool-call realization and the associated safety/no-call regressions.
2. Distinguish descriptive observations, associative findings, candidate mechanisms, and accepted mechanism claims at the correct evidentiary tier.
3. Determine which observability and provenance requirements are mandatory when prompt construction, render path, dataset composition, or evaluation contract materially affect interpretation.
4. Separate durable methodology lessons from one-family historical artifacts.
5. Strengthen the bridge between offline canonical evaluation findings and runtime-behavior interpretation without assuming they are interchangeable.

## Non-Goals

Gen-2 should explicitly **not** be defined by:

- clearing the D0 blocker or recovering missing canonical trainer bytes;
- replaying H1 or H2 as success targets;
- reopening Stage C as an active runtime-output investigation;
- broad dataset redesign without a bounded explanatory question;
- benchmark or leaderboard chasing detached from mechanism and safety interpretation;
- public-package front-door polish as a scientific objective;
- experiment design, treatment-arm design, run planning, preregistration, or execution authorization;
- governance rewrite, metric reinterpretation, or blocker weakening.

## Durable Lessons From Gen-1

The strongest durable lessons carried forward from Gen-1 are:

1. Strong offline evaluation gains do not, by themselves, explain runtime behavior or safety behavior.
2. Exact rendered prompts and their provenance are first-class evidence when prompt construction affects interpretation.
3. Missing evidence must remain missing; substitution, backfill, or inference-based repair damages credibility.
4. Capability improvement and safety/no-call regression must be interpreted together rather than as separate scoreboards.
5. Frozen contracts, pinned surfaces, structured validation, and append-only evidence history are part of the scientific method, not clerical overhead.
6. Candidate-mechanism work requires typed evidence roles and structured confounds or it will drift into narrative overclaim.
7. Evidence-creation mechanisms matter when they are the minimal reproducibility path and should be preserved alongside the resulting evidence objects.

## Foundational Gen-1 Inputs

The following Gen-1 outputs should be treated as foundational inputs to Gen-2.

### Measurement And Doctrine

- the goal charter, Appendix A execution contract, metric specification, and frozen canonical evaluation manifest;
- the published Llama 3.1 baseline package, including the project-wide comparison and machine-readable baseline bundle.

### Closure And Boundary Determinations

- Stage B completion determination;
- Stage C closure continuity package and final disposition assessment;
- D0-to-current-tree governance transition;
- D1 closure and D2 readiness assessment;
- Stage D continuity handoff and the D1 governance foundation.

### Explanatory Starting Corpus

- the living training run history as the empirical ordering surface;
- the D1 mechanism-hypothesis inventory specification;
- the D1 mechanism-hypothesis inventory itself, including its typed evidence roles, relationship metadata, and structured confounds.

These should be treated as the starting corpus for Gen-2, not as optional background.

## Gen-1 Assumptions To Challenge Or Discard

Gen-2 should challenge or discard the following Gen-1 assumptions:

1. That byte-perfect reconstruction is the right organizing scientific question for future explanatory work.
2. That exact-call improvement alone is enough to define success.
3. That single-family or single-regime evidence is sufficient for doctrine elevation or strong mechanism claims.
4. That H1/H2 should function as replay targets rather than observational reference regimes.
5. That broader or later modifications are automatically more informative than smaller preserved high-signal regimes.
6. That behavioral evidence, governance evidence, provenance evidence, and continuity context can be mixed interchangeably in support of a claim.

## Largest Remaining Uncertainties

The current evidence corpus still leaves several major uncertainties unresolved:

1. Which minimal factors actually drive H1/H2-class exact tool-call gains.
2. Which factors drive the corresponding safety and no-call regressions, and whether those regressions are separable from the capability gains.
3. How much of the observed H1/H2 behavior is family-specific, contract-specific, or method-general.
4. When offline canonical metrics are reliable predictors of runtime behavior and when they are not.
5. What the minimum acceptable observability package is for more complex prompt regimes than the Stage C exemplar.
6. What evidence threshold would justify elevating any current candidate mechanism or retained guidance beyond its present status.

## Valuable Gen-2 Question Classes

The highest-value question classes for Gen-2 appear to be:

1. Mechanism questions: what minimal current-tree surfaces plausibly explain strong exact tool-call realization and its tradeoffs.
2. Comparability questions: how preserved H1/H2 reference regimes should constrain present-day interpretation without becoming replay mandates.
3. Observability questions: what must be captured so prompt, dataset, configuration, and evaluation surfaces are interpretable from first principles.
4. Generalization questions: which Gen-1 lessons survive across additional families, render contracts, or model baselines.
5. Claim-quality questions: how evidence tiers, fixed-surface declarations, and confound handling should bound acceptable conclusions.

## Question Classes That Should Not Define Gen-2

The following classes should explicitly **not** define Gen-2:

1. Historical certification cleanup or provenance repair as the main scientific agenda.
2. Front-door, publication, or packaging refinement as a substitute for evidence generation.
3. Re-litigation of closed Stage C findings.
4. Unbounded optimization sweeps whose primary output is more runs rather than better explanations.
5. Any attempt to weaken the D0 blocker, relabel H1/H2, or bypass current boundary controls.
6. Any implicit transition from strategic framing into treatment-arm design, run planning, or execution.

## Recommended Conceptual Direction

The recommended conceptual direction is:

- treat Gen-1 as a completed first-generation evidence program;
- preserve its baselines, closures, governance, and hypothesis inventory as fixed starting inputs;
- orient Gen-2 around explanatory comparability, observability discipline, and mechanism-quality evidence;
- prefer questions that improve the interpretability of future findings over questions that merely add more output volume; and
- define success in terms of durable explanatory power, not just another local capability maximum.

In practical strategic terms, Gen-2 should be about understanding why the repository produced its strongest regimes, under what evidence conditions those interpretations are trustworthy, and which lessons generalize beyond the exact historical path that produced them.

## What Success Should Look Like

Success for Gen-2 should look like:

1. the repository can explain its strongest observed capability regime and its tradeoffs without depending on retrospective narrative repair;
2. future conclusions can be stated at the correct evidentiary tier with less ambiguity about what is descriptive, associative, or mechanistic;
3. observability failures like missing rendered prompts or unresolved provenance do not recur because the required evidence is captured at creation time;
4. H1/H2 are treated as well-understood scientific comparators rather than as mysterious exceptions or optimization targets; and
5. the resulting program definition is broad enough to support later authorized work without being captive to one historical anomaly.

## Day-One Observability, Provenance, And Evidence-Capture Requirements

From day one, any future Gen-2 work should require:

1. exact rendered prompt capture whenever prompt construction materially affects interpretation;
2. row identity, source provenance, render-path metadata, template identity, and hashes attached to prompt-surface evidence;
3. explicit recording of fixed surfaces, comparison class, control/reference class, and allowed-to-vary surfaces for every claim-bearing artifact;
4. preservation of configs, dataset versions, script identities, seeds, environment pinning, training summaries, and evaluation summaries for every serious run or evidence-creation slice;
5. strict separation of behavioral evidence from governance, provenance, contract, and continuity-context evidence;
6. structured confound records attached to claim-bearing artifacts rather than buried in narrative prose;
7. preservation of evidence-creation code and validation outputs whenever they are the minimal reproducibility path;
8. append-only history and explicit versioning for prompt, render, and evaluation-contract changes rather than silent semantic drift.

## Principal Risks Of Repeating Gen-1 Mistakes

The principal risks of repeating Gen-1 mistakes are:

1. allowing key observability gaps to be discovered only after interpretation has already begun;
2. collapsing descriptive correlation into mechanism claims;
3. confusing current-tree comparability with historical certification;
4. chasing capability gains without jointly accounting for safety and no-call regressions;
5. mixing evidence tiers or authority levels for convenience;
6. letting strategic framing drift into unauthorized design or execution work before separate authorization exists.

## Outsider Description

Gen-2 should be described to a technically sophisticated outsider as a second-generation evidence program for tool-calling assistants that moves beyond baseline publication and historical closure into explanation: it would use the repository's published baselines, Stage C observability lessons, D0/D1 governance boundaries, and D1 hypothesis inventory as fixed inputs, and focus on identifying which current-tree conditions actually produce strong exact tool-call behavior, which tradeoffs accompany those conditions, and what provenance and observability must be captured from the start so later conclusions are reproducible, inspectable, and not dependent on retrospective reconstruction.

## Boundary Confirmation

This assessment is documentation-only.

It does not authorize:

- D2 planning or D2 execution;
- experiment design;
- treatment-arm design;
- run planning;
- preregistration creation;
- manifest edits;
- hash-claim edits;
- training or evaluation execution; or
- governance reinterpretation.
