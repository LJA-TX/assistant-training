# Phase F — Dataset Evolution Reconnaissance

## Mission

Execute Phase F of the assistant-training roadmap.

The purpose of Phase F is to determine what dataset changes are most likely to improve tool-calling performance beyond the current i3 baseline.

This is a reconnaissance, assessment, and recommendation phase.

It is not a training phase.

It is not an implementation phase.

It is not a dataset-ingestion phase.

The objective is to establish an evidence-based Dataset Evolution Strategy.

---

## Context

Phase E established:

* A reproducible baseline.
* A reconciled evaluation contract.
* A trustworthy evaluation framework.
* A measurable but insufficient improvement from the i3 adapter.

Current evidence indicates:

* Invalid JSON improved substantially.
* Exact JSON validity remains poor.
* Tool-name accuracy remains poor.
* Argument accuracy remains poor.
* No-call correctness remains strong.

The question is now:

> What dataset changes are most likely to improve the weak metrics while preserving the strong ones?

---

## Authority

Use:

* Goal Charter v5a
* Appendix A
* Metric Specification v1a
* Canonical Evaluation Manifest
* Phase D artifacts
* Phase E artifacts
* Phase E remediation artifacts

as authoritative.

Do not reinterpret prior accepted findings.

---

## Boundaries

You may:

* investigate
* assess
* inventory
* compare
* document
* recommend
* create reports
* commit documentation
* push documentation

You may NOT:

* download datasets
* modify datasets
* build datasets
* ingest datasets
* launch training
* modify evaluation semantics
* modify scoring semantics
* modify promotion gates

This phase is planning and evidence only.

---

# Work Package F-01

## Current Dataset Assessment

Review the current Dataset v1.0 composition.

Determine:

* current provenance sources
* current category distribution
* current strengths
* current weaknesses
* likely causes of the observed i3 performance profile

Produce:

### CURRENT_DATASET_ASSESSMENT.md

---

# Work Package F-02

## External Dataset Survey

Investigate major tool-calling and function-calling dataset families.

At minimum evaluate:

* xLAM
* APIGen
* APIGen-MT
* ToolACE
* Glaive
* BFCL-related public datasets
* any other high-quality candidates discovered during research

For each:

* purpose
* size
* provenance
* maintenance status
* licensing
* quality signals
* known strengths
* known weaknesses

Produce:

### EXTERNAL_DATASET_SURVEY.md

---

# Work Package F-03

## Compatibility Assessment

For each candidate dataset family:

Determine:

* compatibility with the charter
* compatibility with Appendix A
* compatibility with the canonical evaluation framework
* compatibility with runtime-oriented assistant behavior

Classify:

### HIGH FIT

### MEDIUM FIT

### LOW FIT

Provide evidence.

Produce:

### DATASET_COMPATIBILITY_ASSESSMENT.md

---

# Work Package F-04

## Behavioral Gap Mapping

Map candidate datasets against the specific weaknesses identified in Phase E.

Assess expected impact on:

### Exact JSON validity

### Tool-name accuracy

### Argument accuracy

### Wrapper leakage

### No-call correctness

### Runtime alignment

Identify:

* likely improvements
* likely regressions
* unknowns

Produce:

### BEHAVIORAL_GAP_MAPPING.md

---

# Work Package F-05

## Risk Assessment

Assess risks of incorporating each candidate.

Include:

* data contamination risk
* schema mismatch risk
* quality risk
* licensing risk
* behavioral-regression risk
* overfitting risk

Produce:

### DATASET_RISK_ASSESSMENT.md

---

# Work Package F-06

## Dataset Evolution Strategy

Recommend one of:

### Strategy A

Incremental Dataset v1.1 expansion

### Strategy B

Dataset v2.0 redesign

### Strategy C

Targeted augmentation only

### Strategy D

Other

Support the recommendation with evidence.

Produce:

### DATASET_EVOLUTION_STRATEGY.md

---

# Work Package F-07

## Phase G Readiness Recommendation

Based on all evidence collected:

Recommend:

### Proceed directly to Dataset Implementation

or

### Additional research required

or

### Training-ready after implementation

Provide rationale.

Produce:

### PHASE_G_READINESS_RECOMMENDATION.md

---

# Required Final Deliverable

Produce:

## PHASE_F_CLOSURE_AND_DATASET_EVOLUTION_ASSESSMENT.md

Include:

### Executive Summary

### Current Dataset Findings

### External Dataset Findings

### Compatibility Findings

### Behavioral Impact Findings

### Risk Findings

### Recommended Dataset Strategy

### Recommended Next Action

### Go / No-Go Recommendation

for Dataset Evolution Implementation work.

---

# Execution Style

Operate autonomously.

Prefer evidence over intuition.

Prefer documented dataset characteristics over assumptions.

Prefer practical recommendations over theoretical possibilities.

Avoid governance expansion.

Avoid methodology expansion unless directly relevant.

The objective is to identify the highest-value dataset evolution path for improving tool-calling behavior.

---

# Validation Requirements

Document sources used.

Clearly separate:

* observed facts
* project-specific interpretation
* recommendations

Perform normal repository hygiene checks.

---

# Success Criteria

Success is achieved when:

* candidate dataset families have been assessed
* behavioral gaps have been mapped
* risks have been identified
* a dataset evolution strategy has been selected
* a clear implementation direction exists for the next phase

When complete:

* commit
* push
* provide exact artifact paths
* identify unresolved questions
* identify recommended next-phase scope

The objective is to determine what data should be added before the next serious training attempt.
