# Phase H — Controlled Experimental Design

## Mission

Design the next experiment.

Do NOT implement it.

Do NOT modify datasets.

Do NOT launch training.

Do NOT create Dataset v1.1.

The purpose of Phase H is to design a bounded experiment that can be executed later by GPT-5.4-Mini with minimal ambiguity.

This is an experimental-design phase.

---

## Context

Phase E established:

* reproducible baseline,
* reconciled evaluation contract,
* trustworthy evaluation framework.

Phase F established:

* severe Dataset v1.0 collapse,
* strong candidates for future external augmentation.

Grok-Build independently confirmed:

* collapse was real,
* collapse was pipeline-caused,
* collapse alone does not explain the full i3 deficit.

Phase G established:

* internal signal recovery restored substantial diversity,
* collapse repair is necessary but not sufficient,
* dominant residual failure is tool-call commitment and schema realization,
* wrong-tool selection is not currently the primary bottleneck.

The project now requires a carefully designed proving experiment before Dataset v1.1 implementation.

---

## Authority

Use:

* Goal Charter v5a
* Appendix A
* Metric Specification v1a
* Phase D artifacts
* Phase E artifacts
* Phase E remediation artifacts
* Phase F artifacts
* Grok-Build assessment
* Phase G artifacts

as authoritative.

---

# Primary Question

Design an experiment capable of distinguishing between:

### Hypothesis A

Dataset diversity remains the dominant bottleneck.

### Hypothesis B

Tool-call commitment is the dominant bottleneck.

### Hypothesis C

Schema realization is the dominant bottleneck.

### Hypothesis D

Training methodology is the dominant bottleneck.

### Hypothesis E

A combination of the above.

---

# Work Package H-01

## Experimental Objectives

Define:

* primary objective
* secondary objectives
* measurable outcomes
* failure conditions

Produce:

### EXPERIMENTAL_OBJECTIVES.md

---

# Work Package H-02

## Candidate Intervention Analysis

Identify the smallest interventions capable of isolating:

### Diversity effects

### Commitment effects

### Schema effects

### Methodology effects

Determine:

* which variables should change
* which variables must remain frozen

Produce:

### CANDIDATE_INTERVENTION_ANALYSIS.md

---

# Work Package H-03

## Experimental Matrix

Design a bounded experiment matrix.

For each candidate run specify:

* dataset variant
* training variant
* control relationship
* expected learning value

Include:

### Control run(s)

### Treatment run(s)

### Minimum viable run set

### Preferred run set

The matrix must be realistic for local execution.

Produce:

### EXPERIMENTAL_MATRIX.md

---

# Work Package H-04

## Success Metrics

Define:

### Primary metrics

### Secondary metrics

### Diagnostic metrics

### Kill metrics

### Promotion metrics

Explicitly state:

* what constitutes success,
* what constitutes failure,
* what constitutes inconclusive results.

Produce:

### SUCCESS_AND_FAILURE_CRITERIA.md

---

# Work Package H-05

## Stop Rules

Design strict stop rules.

Prevent:

* endless internal-only iteration,
* uncontrolled dataset expansion,
* ambiguous outcomes,
* post-hoc reinterpretation.

Produce:

### STOP_RULES_AND_DECISION_GATES.md

---

# Work Package H-06

## GPT-5.4-Mini Execution Package

This is the most important deliverable.

Produce a Mini-executable plan.

Assume the future execution agent:

* has repository access,
* can inspect files,
* can run commands,
* can create documentation,
* can commit and push,

but should not be required to invent methodology.

Provide:

### exact execution sequence

### required validations

### expected outputs

### escalation triggers

### completion criteria

Produce:

### MINI_EXECUTION_PACKAGE.md

The goal is that GPT-5.4-Mini can execute the experiment without needing to redesign it.

---

# Work Package H-07

## Recommendation

Recommend:

### H1

Internal proving experiment only

### H2

Internal proving experiment plus bounded implementation

### H3

Proceed directly to Dataset v1.1

### H4

Other

Support the recommendation.

Produce:

### PHASE_I_RECOMMENDATION.md

---

# Required Final Deliverable

Produce:

## PHASE_H_CONTROLLED_EXPERIMENT_DESIGN.md

Include:

### Executive Summary

### Competing Hypotheses

### Proposed Experiment

### Why This Experiment

### Expected Learning Value

### Risks

### Stop Rules

### Recommended Next Action

### Confidence Assessment

---

# Boundaries

Do NOT:

* implement Dataset v1.1
* modify datasets
* launch training
* modify evaluation semantics
* modify scoring semantics
* redesign project governance

This phase ends with an experiment design.

---

# Success Criteria

Success is achieved when:

* the next experiment is fully specified,
* competing explanations are distinguishable,
* success criteria are objective,
* stop rules exist,
* GPT-5.4-Mini can execute the experiment without needing to redesign it.

The objective is not to improve the model.

The objective is to determine the most informative next experiment before implementation begins.
