# Gen-2 Strategic Direction Options Assessment

Date: 2026-06-19

## Scope

This document is a documentation-only follow-on assessment of the current Gen-2 framing.

Its purpose is to:

- critique the current Gen-2 assessment where the framing is too tightly coupled to H1/H2 history;
- refine the strategic framing where needed;
- compare plausible Gen-2 program shapes at a conceptual level; and
- recommend which strategic direction should be explored next.

This document does **not** authorize D2 planning, experiment design, treatment-arm design, run planning, preregistration creation, manifests, execution, or governance reinterpretation.

## Inputs

- [GEN2_PROSPECTIVE_EVIDENCE_PROGRAM_ASSESSMENT.md](./GEN2_PROSPECTIVE_EVIDENCE_PROGRAM_ASSESSMENT.md)
- [../current_status.md](../current_status.md)
- [../project_outcomes_to_date.md](../project_outcomes_to_date.md)
- [D1_CLOSURE_AND_D2_READINESS_ASSESSMENT.md](./D1_CLOSURE_AND_D2_READINESS_ASSESSMENT.md)
- [../../continuity/STAGE_D_D1_CLOSURE_AND_D2_READINESS_HANDOFF_2026-06-16.md](../../continuity/STAGE_D_D1_CLOSURE_AND_D2_READINESS_HANDOFF_2026-06-16.md)
- [../../continuity/D0_TO_CURRENT_TREE_MECHANISM_ISOLATION_GOVERNANCE.md](../../continuity/D0_TO_CURRENT_TREE_MECHANISM_ISOLATION_GOVERNANCE.md)
- [../../continuity/D1_GOVERNANCE_FOUNDATION_PACKAGE.md](../../continuity/D1_GOVERNANCE_FOUNDATION_PACKAGE.md)
- [../../goal_charter_v5a.md](../../goal_charter_v5a.md)
- [../../appendix_a_operational_execution_contract_v3a.md](../../appendix_a_operational_execution_contract_v3a.md)
- [../../metric_specification_v1a.md](../../metric_specification_v1a.md)

## Executive Determination

The current Gen-2 assessment is broadly directionally correct.

Its strongest move is the shift from reconstruction or execution language toward mechanism, observability, comparability, and evidence quality.

Its main weakness is not explicit replay authorization.
The main weakness is subtler: several objectives, uncertainties, and success criteria still let H1/H2 function as the de facto definition of Gen-2 rather than as the highest-signal current reference regimes inside a broader charter.

The framing should therefore be generalized.
H1/H2 should remain anchor comparators and foundational inputs, but they should not define the entire program's scientific identity.

## 1. Critical Review Of The Current Framing

### 1.1 What already works

The current assessment correctly states that Gen-2 should:

- avoid reconstruction-completion framing;
- avoid replay-target framing;
- avoid pure capability chasing;
- foreground observability and provenance;
- preserve the D0 blocker and D1 boundary; and
- treat Gen-1 as a completed first-generation evidence program.

Those elements align with the current authority surfaces and should be retained.

### 1.2 Where the framing is too historically narrow

The following elements should be treated as candidates for refinement:

| Current framing element | Concern | Recommended refinement |
|---|---|---|
| `Clarify the minimal explanatory surfaces behind H1/H2-class exact tool-call realization...` | Makes one historical reference regime the nominal scientific object of Gen-2. | Reframe around strong tool-calling behavior and its tradeoffs, with H1/H2 as anchor comparators. |
| `Which minimal factors actually drive H1/H2-class exact tool-call gains.` | Risks narrowing the uncertainty set to one observed regime rather than the broader explanatory problem. | Reframe around which factors drive strong exact tool-call behavior under the frozen contract, and which are H1/H2-specific versus more general. |
| `How much of the observed H1/H2 behavior is family-specific...` | Useful, but still assumes the program is defined by H1/H2 first and generalization second. | Reframe around which explanatory lessons are regime-specific versus method-general, with H1/H2 as the current best reference case. |
| `H1/H2 are treated as well-understood scientific comparators rather than as mysterious exceptions...` | Appropriate as a success condition, but too specific to stand as a program-level success definition. | Expand to historical reference regimes are interpretable comparators, with H1/H2 as the present highest-signal examples. |
| `...focus on identifying which current-tree conditions actually produce strong exact tool-call behavior...` | Better than replay language, but still capability-centered if left alone. | Pair it explicitly with tradeoff interpretation, evidence-tier discipline, and generalization boundaries. |

### 1.3 What could unintentionally narrow Gen-2 to replay-adjacent questions

The current assessment does not explicitly authorize replay.
However, the following framing pattern creates replay-adjacent pressure:

1. H1/H2 are repeatedly named as the leading object of explanation.
2. the strongest observed regime is repeatedly treated as the main success surface;
3. generalization appears later as an extension rather than as part of the core frame.

That pattern can unintentionally produce a working interpretation of:

`Gen-2 = explain H1/H2`

That is narrower than the broader charter, which is to build a reusable methodology for future generations of runtime-oriented tool-calling assistants.

The safer framing is:

`Gen-2 = explain strong tool-calling behavior and its tradeoffs in a reusable, evidence-disciplined way, using H1/H2 as the strongest current anchor comparators`

## 2. Assessment Of The Current Objective

Current objective under review:

`Clarify the minimal explanatory surfaces behind H1/H2-class exact tool-call realization and the associated safety/no-call regressions.`

## Determination

Yes.
A more general formulation would better align with the overall charter.

The current wording is scientifically understandable because H1/H2 are the strongest observed regimes in the repository.
But it is narrower than the charter in two ways:

1. it makes one historical regime the center of the objective rather than the broader problem of disciplined tool-calling behavior;
2. it emphasizes exact-tool realization more than the charter's wider behavioral frame, which also includes wrapper restraint, runtime obedience, no-call behavior, and safety discipline.

## Recommended General Formulation

Recommended replacement objective:

`Clarify the explanatory surfaces behind strong structured tool-calling behavior and its associated safety, no-call, and runtime-discipline tradeoffs, using H1/H2 as high-signal observational reference regimes rather than as replay targets or the sole definition of success.`

Why this is better:

- it preserves continuity with the strongest observed evidence;
- it aligns more directly with the charter's broader behavioral target;
- it keeps tradeoffs central;
- it avoids making H1/H2 the entire scientific identity of Gen-2; and
- it remains above the level of design or execution.

## 3. Plausible Gen-2 Program Shapes

Multiple plausible program shapes satisfy the current charter.
They are not all equally strong, and they optimize for different things.

### 3.1 Mechanism-Isolation-Oriented Program

**Central question**

What minimal explanatory surfaces best account for strong tool-calling behavior and its tradeoffs under the frozen contract?

**Optimizes for**

- explanatory sharpness;
- candidate-mechanism discrimination;
- high-value use of the D1 hypothesis inventory.

**Strengths**

- strong continuity with D0-to-D1 transition logic;
- uses the repository's strongest existing high-signal evidence;
- provides a clear scientific center of gravity.

**Risks**

- can collapse back into H1/H2-centered thinking;
- can invite premature causal ambition before broader generalization or observability questions are stabilized;
- can be misread as quasi-replay intent if the framing is not disciplined.

**Charter alignment**

High, but only if the program is framed as mechanism discovery about strong behavior in general rather than H1/H2 reenactment.

### 3.2 Observability-First Program

**Central question**

What evidence, provenance, and surface-capture rules must exist from the start so future findings are interpretable, reproducible, and not dependent on retrospective reconstruction?

**Optimizes for**

- evidence quality;
- interpretability;
- prevention of Stage C and D0-style observability failures.

**Strengths**

- directly carries forward one of the most durable Gen-1 lessons;
- produces method value even before any future explanatory claims are made;
- strongly aligned with the repository's governance and reproducibility posture.

**Risks**

- can become too procedural or instrumentation-centric;
- may leave the substantive explanation problem underspecified;
- may delay clarity on the actual behavioral questions Gen-2 exists to answer.

**Charter alignment**

Very high on methodology quality, but incomplete if treated as the whole Gen-2 identity rather than as a foundation.

### 3.3 Explanatory-Comparability Program

**Central question**

How should current-tree behavior, published baselines, and preserved historical reference regimes be compared so that explanations are informative, bounded, and non-revisionist?

**Optimizes for**

- correct interpretation;
- evidence-tier discipline;
- continuity between current-tree reasoning and preserved historical evidence.

**Strengths**

- matches the D1 boundary and D0 transition especially well;
- keeps H1/H2 important without making them replay targets;
- naturally supports both mechanism questions and generalization questions.

**Risks**

- can remain too abstract if not coupled to substantive behavioral questions;
- may produce careful framing without enough explanatory ambition if treated too defensively.

**Charter alignment**

Very high.
This shape is broad enough to support reusable methodology and narrow enough to remain evidence-disciplined.

### 3.4 Tradeoff-Characterization Program

**Central question**

Which capability, safety, no-call, and runtime-discipline tradeoffs are structural, which are incidental, and which are artifacts of specific regimes or contracts?

**Optimizes for**

- balanced behavioral interpretation;
- alignment with the charter's safety and restraint priorities;
- avoiding capability-only success framing.

**Strengths**

- directly addresses a recurring project-level concern;
- generalizes more naturally than a purely H1/H2-centric mechanism frame;
- keeps the repository from drifting back into pure metric maximization.

**Risks**

- can become descriptive rather than explanatory;
- may underweight provenance and observability if treated as a score-comparison exercise;
- may not produce a sharp enough program identity on its own.

**Charter alignment**

High.
It tracks the broader behavioral target better than a narrow exact-JSON framing does.

### 3.5 Cross-Family Generalization Program

**Central question**

Which explanatory lessons from Gen-1 and the current reference regimes generalize across additional families, contracts, or model baselines?

**Optimizes for**

- methodological durability;
- doctrine-readiness;
- future-generation usefulness.

**Strengths**

- best aligned with the long-term objective of a reusable methodology;
- most resistant to overfitting the program identity to one historical case;
- strongest route to durable lessons rather than local explanations only.

**Risks**

- may be premature while first-order explanatory uncertainty remains high;
- can broaden scope too early;
- can weaken focus if used before the initial explanatory frame is sharpened.

**Charter alignment**

High in the long term, but only medium-high as the primary immediate Gen-2 interpretation because it assumes more explanatory stability than the current corpus yet provides.

## 4. Comparative Assessment

No single pure program shape is sufficient on its own.

The weakest standalone interpretations are:

- a purely mechanism-isolation frame, because it risks over-centering H1/H2 history;
- a purely observability-first frame, because it risks becoming infrastructure without enough scientific identity;
- a purely cross-family-generalization frame, because it is likely too broad for the present evidence state.

The strongest current interpretation is a combined shape:

- primary identity: explanatory-comparability;
- required foundation: observability-first;
- explicit analytical lens: tradeoff-characterization;
- bounded sub-question: mechanism isolation.

That ordering matters.
It keeps mechanism questions inside a broader interpretive and methodological frame instead of letting them define the whole program.

## 5. Preferred Strategic Direction

The strategically preferable direction is:

**Gen-2 should be framed as an explanatory-comparability and observability program for strong tool-calling behavior and its tradeoffs, with mechanism-isolation questions treated as important sub-questions and H1/H2 treated as anchor reference regimes rather than as the program's sole scientific identity.**

This direction is preferable because it:

- aligns with the long-term charter objective of reusable methodology;
- preserves continuity with the D0-to-D1 transition;
- keeps H1/H2 scientifically important without making Gen-2 a historical replay surrogate;
- incorporates the strongest Stage C and D1 lessons about observability and evidence tiers; and
- leaves room for later authorized work without prematurely choosing one narrow scientific identity.

## 6. Recommended Strategic Exploration Boundary

The next strategic direction to explore should therefore be:

1. a generalized Gen-2 framing centered on strong tool-calling behavior, tradeoffs, and interpretability rather than on H1/H2-specific explanation alone;
2. an explicit statement that H1/H2 are anchor comparators and starting evidence, not the definition of the program;
3. a program identity built around explanatory comparability plus observability requirements;
4. success criteria stated in terms of explanatory quality, tradeoff understanding, and generalizable methodology rather than local reconstruction of one historical regime.

This remains a framing recommendation only.
It is not experiment design, arm design, run planning, or execution guidance.

## 7. Boundary Confirmation

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
