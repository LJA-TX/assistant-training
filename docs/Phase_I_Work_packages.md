# Phase I — Controlled Internal Proving Experiment

## Mission

Execute Phase I exactly as designed in the published Phase H bundle.

This is an execution phase.

Do not redesign the experiment.

Do not create a new methodology.

Do not revisit Phase H conclusions.

The purpose is to execute the bounded proving experiment and determine which bottleneck hypothesis survives contact with empirical evidence.

---

## Authority

Treat the following as authoritative:

### Phase H Bundle

* `docs/phase_h/README.md`
* `docs/phase_h/EXPERIMENTAL_OBJECTIVES.md`
* `docs/phase_h/EXPERIMENTAL_MATRIX.md`
* `docs/phase_h/SUCCESS_AND_FAILURE_CRITERIA.md`
* `docs/phase_h/STOP_RULES_AND_DECISION_GATES.md`
* `docs/phase_h/MINI_EXECUTION_PACKAGE.md`
* `docs/phase_h/PHASE_H_CONTROLLED_EXPERIMENT_DESIGN.md`
* `docs/phase_h/PHASE_I_RECOMMENDATION.md`

Phase H is the design authority.

You are executing it.

Not revising it.

---

## Primary Objective

Determine whether the dominant remaining bottleneck is:

### A

Dataset diversity

### B

Tool-call commitment

### C

Schema realization

### D

Training methodology

### E

Combined bottleneck

using the predeclared Phase H criteria.

---

## Required Execution Mode

Follow:

```text
docs/phase_h/MINI_EXECUTION_PACKAGE.md
```

exactly.

If a conflict exists:

```text
MINI_EXECUTION_PACKAGE
    >
EXPERIMENTAL_MATRIX
    >
other Phase H artifacts
```

---

# Work Package I-01

## Phase I Journal

Create:

```text
docs/phase_i/PHASE_I_CODEX_JOURNAL.md
```

Record:

* actions taken
* commands executed
* validations performed
* stop-rule decisions
* escalation decisions

Maintain throughout execution.

---

# Work Package I-02

## Control Surface Verification

Verify all frozen surfaces specified by Phase H.

Produce:

```text
docs/phase_i/CONTROL_SURFACE_VERIFICATION.md
```

Do not proceed if frozen-surface validation fails.

Apply Phase H stop rules.

---

# Work Package I-03

## Dataset Variant Construction

Construct the variants exactly as specified by Phase H:

### H0_control_i3_micro

### H2_commitment_patch

### H1_diversity_patch

Apply all Phase H constraints:

* bounded patch size
* frozen non-tool slices
* contamination checks
* validation artifacts

Produce:

```text
docs/phase_i/DATASET_VARIANT_VALIDATION.md
```

---

# Work Package I-04

## Execute First-Screen Runs

Run:

### H0

### H2

### H1

in the Phase H execution order.

After each run:

* evaluate immediately
* apply kill metrics
* update comparison artifacts

Do not proceed blindly.

---

# Work Package I-05

## Apply Phase H Decision Gates

Use:

```text
docs/phase_h/SUCCESS_AND_FAILURE_CRITERIA.md
```

and

```text
docs/phase_h/STOP_RULES_AND_DECISION_GATES.md
```

exactly.

Determine:

* stop in favor of diversity
* stop in favor of commitment
* continue to schema probe
* continue to methodology probe
* external-first stop rule

Document the rationale.

---

# Work Package I-06

## Conditional Runs

Run:

### H3_schema_patch

only if Phase H requires it.

Run:

### H4_methodology_only

only if Phase H requires it.

Do not execute conditional runs merely because they exist.

---

# Work Package I-07

## Attribution Decision

Produce:

```text
docs/phase_i/BOTTLENECK_ATTRIBUTION_DECISION.md
```

Determine:

### A

### B

### C

### D

### E

or

### inconclusive_external_first

using the published thresholds.

Do not invent new categories.

---

# Work Package I-08

## Final Comparison Bundle

Produce:

```text
docs/phase_i/RUN_COMPARISON_MATRIX.md
```

and

```text
docs/phase_i/PHASE_I_COMPLETION_AND_NEXT_STEP_RECOMMENDATION.md
```

Include:

* run summaries
* metric deltas
* threshold outcomes
* stop-rule outcomes
* recommendation

---

# Required Validation

Perform all validations required by:

```text
docs/phase_h/MINI_EXECUTION_PACKAGE.md
```

and record results.

---

# Escalation Rules

Escalate immediately if:

* frozen surfaces drift
* contamination cannot be cleared
* bounded variants cannot be constructed
* methodology probe requires trainer redesign
* Phase H stop rules trigger escalation

Do not improvise around those conditions.

---

# Commit / Push

Commit logical milestones.

Push to:

```text
origin/main
```

Provide:

* staged inventory
* validation results
* commit hashes
* push result
* final git status

---

# Success Criteria

Success is achieved when:

1. Phase H has been executed faithfully.
2. The first-screen runs are complete.
3. Any required conditional runs are complete.
4. One of:

   * A
   * B
   * C
   * D
   * E
   * inconclusive_external_first

   has been determined using the published rules.
5. A next-step recommendation is documented.

The objective is not to achieve a better score.

The objective is to identify the dominant bottleneck with the highest confidence achievable from a bounded internal experiment.

