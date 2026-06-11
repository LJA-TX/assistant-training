# Phase E — Canonical Baseline Revalidation

## Mission

Execute Phase E of the assistant-training roadmap.

The purpose of Phase E is to establish the authoritative restart baseline for all future training work.

This is not a planning exercise.

This is not a documentation exercise.

This is an evidence-generation exercise.

You are expected to verify assumptions, execute validations, collect outputs, and produce a defensible baseline assessment.

---

## Authority

Use:

* Goal Charter v5a
* Appendix A
* Metric Specification v1a
* Canonical Eval Manifest
* Accepted continuity records
* Accepted Phase D artifacts

as authoritative.

Stage C remains closed history.

Do not reopen Stage C.

Do not reinterpret Stage C.

---

## Scope

You may:

* inspect
* validate
* execute evaluation runs
* verify manifests
* verify paths
* verify artifacts
* generate reports
* commit documentation
* push documentation

You may NOT:

* launch training
* alter datasets
* alter evaluation semantics
* alter scorer semantics
* alter promotion gates
* alter canonical manifest contents

---

# Work Package E-01

## Environment Verification

Verify:

### Repository State

* current branch
* HEAD
* origin alignment
* working tree cleanliness

### Canonical Model

Verify existence and accessibility of:

```text
/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base
```

### Adapter

Verify existence and accessibility of:

```text
artifacts/adapters/stage_b_llama31_8b_base_v1_i3
```

### Evaluation Assets

Verify:

* manifest exists
* scorer exists
* evaluation datasets exist
* hashes match expectations

Produce:

* ENVIRONMENT_AND_ASSET_VERIFICATION.md

---

# Work Package E-02

## Canonical Contract Verification

Verify:

* manifest integrity
* split integrity
* decode defaults
* scorer references
* dataset references
* model references

Determine whether:

> the canonical evaluation contract remains reproducible without modification

Produce:

* CANONICAL_CONTRACT_VERIFICATION.md

---

# Work Package E-03

## Base Model Revalidation

Execute the canonical evaluation process against:

```text
llama-3.1-8b-base
```

Capture:

* commands
* outputs
* summaries
* artifacts
* runtime notes
* failures
* warnings

Do not summarize from historical reports.

Generate fresh evidence.

Produce:

* BASE_MODEL_REVALIDATION_REPORT.md

---

# Work Package E-04

## Clean Restart Adapter Revalidation

Execute the canonical evaluation process against:

```text
stage_b_llama31_8b_base_v1_i3
```

Capture:

* commands
* outputs
* summaries
* artifacts
* runtime notes
* failures
* warnings

Generate fresh evidence.

Produce:

* I3_ADAPTER_REVALIDATION_REPORT.md

---

# Work Package E-05

## Baseline Delta Assessment

Compare:

### Base Model

vs

### i3 Adapter

Evaluate:

* JSON validity
* tool-name accuracy
* argument quality
* wrapper leakage
* no-call correctness
* Appendix A gate deltas

Produce:

* BASELINE_DELTA_ASSESSMENT.md

Do not evaluate promotion.

Do not recommend promotion.

Only establish baseline reality.

---

# Work Package E-06

## Readiness Determination

Determine:

### Is the canonical baseline reproducible?

### Is the i3 baseline reproducible?

### Is the evaluation contract stable?

### Is the repository ready for renewed training work?

Produce:

* PHASE_E_READINESS_DETERMINATION.md

Use:

* READY
* READY WITH CAVEATS
* NOT READY

with evidence.

---

# Work Package E-07

## Phase F Launch Recommendation

Based on actual evidence collected in this phase:

Recommend one of:

### Option A

Proceed directly to Dataset v1.x expansion work.

### Option B

Proceed directly to Stage A training.

### Option C

Perform remediation before either.

Produce:

* PHASE_F_LAUNCH_RECOMMENDATION.md

---

# Required Final Deliverable

Produce:

## PHASE_E_CLOSURE_AND_PHASE_F_TRANSITION_ASSESSMENT.md

Include:

### Executive Summary

### Environment Verification Results

### Contract Verification Results

### Base Model Results

### i3 Results

### Baseline Delta Results

### Risks

### Recommended Next Action

### Phase F Recommendation

### Go / No-Go Determination

---

# Validation Requirements

You must provide evidence.

Do not rely solely on historical artifacts.

Do not infer successful execution.

If execution fails:

* capture the failure
* diagnose it
* document it
* continue where possible

A documented failure is preferable to an undocumented assumption.

---

# Success Criteria

Success is achieved when:

* the canonical baseline has been freshly revalidated
* the i3 restart baseline has been freshly revalidated
* baseline deltas are documented
* repository readiness is determined
* the next training thread can begin from evidence rather than historical assumptions

When complete:

* perform hygiene checks
* commit
* push
* provide exact artifact paths
* identify unresolved blockers

The objective is to establish authoritative baseline reality, not to create additional governance.
