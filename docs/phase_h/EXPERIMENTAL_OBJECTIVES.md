# Experimental Objectives

## Primary Objective

Design a bounded internal-first proving experiment that can distinguish which explanation best accounts for the remaining Phase E / Phase G deficit:

- `A`: diversity remains the dominant bottleneck
- `B`: tool-call commitment remains the dominant bottleneck
- `C`: schema realization remains the dominant bottleneck
- `D`: training methodology remains the dominant bottleneck
- `E`: no single factor dominates and the deficit is combined

The experiment must answer that question without:

- changing evaluation semantics,
- changing scoring semantics,
- importing external data,
- or beginning Dataset v1.1 implementation.

## Secondary Objectives

1. Preserve the frozen Phase E evaluation contract while testing bounded interventions.
2. Keep the experiment realistic for local execution using already-proven training and evaluation surfaces.
3. Prevent ambiguous "some improvement happened" conclusions by defining predeclared interpretation rules.
4. Provide a Mini-executable package so the next agent can run the experiment without redesigning it.

## Measurable Outcomes

The experiment is designed to measure differential movement in these outcomes versus a fresh bounded control run:

### Primary outcomes

- tool-expected exact JSON validity
- tool-holdout exact JSON validity
- tool-name accuracy
- argument accuracy
- tool-expected invalid JSON rate

### Secondary outcomes

- heldout exact JSON validity
- no-anchor exact-valid share
- read_file exact-valid rate
- read_file symbol-name exact-valid rate

### Diagnostic outcomes

- direct-answer substitution share
- scalar substitution share
- invalid-schema share
- `missing_tool_calls` share
- `payload_not_object` share
- `payload_not_parsed` share
- no-call correctness on both `no_call` and `adversarial`

## Success Conditions For The Design Phase

Phase H succeeds if all of the following are true:

1. The next experiment is fully specified.
2. The competing hypotheses are distinguishable by predeclared metrics and decision rules.
3. Frozen variables and allowed intervention variables are explicit.
4. Stop rules prevent open-ended internal-only iteration.
5. GPT-5.4-Mini can execute the plan without inventing methodology.

## Failure Conditions For The Future Experiment

The future execution should be treated as failed or inconclusive if any of the following occurs:

1. The control run cannot be reproduced on frozen surfaces.
2. A dataset variant cannot be built within the declared bounded patch budget.
3. Any run introduces contamination, wrapper leakage, or evaluation-contract drift.
4. All treatment runs stay within the predeclared inconclusive band.
5. The results require post-hoc reinterpretation to look meaningful.

## Design Principle

The experiment is not a promotion contest.

It is a bottleneck-disambiguation exercise:

- smallest useful interventions,
- fixed comparison surfaces,
- local execution cost kept bounded,
- and decisive stop conditions if internal-only evidence remains weak.

## Sources Used

- `docs/Phase_H_Work_packages.md`
- `docs/goal_charter_v5a.md`
- `docs/appendix_a_operational_execution_contract_v3a.md`
- `docs/metric_specification_v1a.md`
- `docs/phase_g/FAILURE_ATTRIBUTION_ANALYSIS.md`
- `docs/phase_g/COUNTERFACTUAL_ASSESSMENT.md`
- `docs/phase_g/INTERNAL_VS_EXTERNAL_STRATEGY_ASSESSMENT.md`
