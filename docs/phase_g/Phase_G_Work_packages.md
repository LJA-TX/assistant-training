# Phase G — Internal Signal Recovery and Causal Attribution Assessment

## Mission

Perform a deep investigation into the question raised by the independent Grok-Build review.

The purpose of this phase is NOT to build Dataset v1.1.

The purpose is to determine:

> How much of the observed performance deficit can be explained and potentially corrected using signal already present inside the repository?

This is a causal-attribution and recovery assessment.

---

## Context

Phase F identified a severe dataset-collapse defect.

Grok-Build independently verified:

* the collapse is real,
* the collapse is severe,
* the collapse is pipeline-caused,
* the upstream source pool contains substantially more diversity than survived into Dataset v1.0.

However, Grok-Build also found:

> The Phase E i3 adapter did not train on the collapsed corpus.

The i3 recovery corpus contained:

* meaningful tool diversity,
* multiple tools,
* multiple prompts,
* multiple case IDs,

yet still produced poor:

* exact JSON validity,
* tool-name accuracy,
* argument accuracy.

This creates an unresolved question:

> How much of the remaining performance deficit is caused by dataset construction versus other factors?

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
* Grok-Build independent assessment

as authoritative evidence.

Do not reinterpret accepted facts.

---

# Primary Question

Answer:

> If Dataset v1.0 had never collapsed, how much better would we reasonably expect the project to perform?

Support with evidence.

Do not guess.

---

# Work Package G-01

## Internal Signal Inventory

Determine:

* what tool-positive diversity existed upstream,
* what diversity survived,
* what diversity was lost,
* what diversity was later recovered for i3.

Produce:

### INTERNAL_SIGNAL_INVENTORY.md

Include quantitative tables.

---

# Work Package G-02

## Recovery-Corpus Analysis

Analyze:

```text
dataset_v1_0_stage_b_recovery_i3_train.jsonl
```

Determine:

* true tool diversity,
* true argument diversity,
* true schema diversity,
* oversampling patterns,
* prompt diversity,
* case diversity.

Assess whether apparent diversity differs materially from effective diversity.

Produce:

### RECOVERY_CORPUS_ANALYSIS.md

---

# Work Package G-03

## Failure Attribution Analysis

Using Phase E evaluation outputs:

Classify failures into categories such as:

* tool-call commitment failure
* wrong tool selection
* wrong arguments
* schema failure
* wrapper drift
* direct-answer substitution
* refusal substitution
* malformed JSON
* other

Determine which categories dominate.

Produce:

### FAILURE_ATTRIBUTION_ANALYSIS.md

---

# Work Package G-04

## Counterfactual Assessment

Construct evidence-based counterfactuals.

Examples:

### Scenario A

v1.0 collapse fixed only

### Scenario B

Recovery corpus expanded without external data

### Scenario C

Recovery corpus expanded plus external data

### Scenario D

Training methodology unchanged but diversity increased

Estimate:

* expected gains
* uncertainty
* supporting evidence

Do not fabricate precision.

Produce:

### COUNTERFACTUAL_ASSESSMENT.md

---

# Work Package G-05

## Internal-First vs External-First Strategy

Assess:

### Internal-first

Recover and exploit existing signal.

versus

### External-first

Import major external corpora.

Determine:

* expected effort
* expected risk
* expected upside
* expected learning value

Produce:

### INTERNAL_VS_EXTERNAL_STRATEGY_ASSESSMENT.md

---

# Work Package G-06

## Phase H Recommendation

Recommend one of:

### H1

Repair build pipeline first

### H2

Expand recovery corpus first

### H3

External augmentation first

### H4

Combined approach

Support the recommendation.

Produce:

### PHASE_H_RECOMMENDATION.md

---

# Required Final Deliverable

Produce:

## PHASE_G_CAUSAL_ATTRIBUTION_AND_SIGNAL_RECOVERY_ASSESSMENT.md

Include:

### Executive Summary

### What We Now Know

### What The Collapse Explains

### What The Collapse Does Not Explain

### Most Likely Remaining Bottlenecks

### Recommended Next Action

### Confidence Assessment

---

# Boundaries

Do NOT:

* build Dataset v1.1
* ingest external datasets
* launch training
* modify evaluation semantics
* modify scoring semantics
* modify promotion gates

This is an assessment phase only.

---

# Success Criteria

Success is achieved when we can answer:

> Is the project's primary bottleneck now:
>
> * dataset construction,
> * dataset diversity,
> * curriculum composition,
> * tool-call commitment,
> * training methodology,
> * model limitations,
> * or some combination?

with substantially greater confidence than we possess today.

The objective is to identify the highest-leverage intervention before implementing Dataset v1.1.
