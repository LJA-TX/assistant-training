# ASSISTANT-TRAINING CONTINUITY DOCUMENT

## Post-Publication H1/H2 Causal Mechanism Isolation Launch Plan

### Date: 2026-06-14

---

# Project Identity

Repository:

```text
https://github.com/LJA-TX/assistant-training
```

Canonical worktree:

```text
/opt/ai-stack/assistant-training
```

Current branch:

```text
main
```

Current published tip:

```text
f3a6101
```

Repository status:

```text
## main...origin/main
```

Clean.

Synchronized.

Publication milestone complete.

---

# Purpose Of This Continuity Note

This document preserves the approved planning state for the next research thread.

It is a planning and handoff artifact only.

It does not:

1. authorize training launch by itself
2. change evaluation semantics
3. change scoring semantics
4. reopen Stage C
5. modify repository structure

The intended next thread should begin from this document and the cited evidence surfaces.

---

# Current Scientific Position

The repository now has a published baseline evidence package for:

```text
Llama-3.1-8B-Base
Llama-3.1-8B-Instruct
Llama-3.1-8B-Instruct-NVFP4
```

All three published baselines sit at the canonical exact-tool floor:

```text
exact JSON = 0.0
tool-name = 0.0
argument = 0.0
no-call = 1.0
adversarial no-call = 1.0
```

H1 and H2 remain the only clear high-capability regimes in the repository:

```text
H1 exact JSON = 0.44
H1 tool-name = 0.7142857142857143
H1 argument = 0.6285714285714286

H2 exact JSON = 0.48
H2 tool-name = 0.7714285714285715
H2 argument = 0.6928571428571428
```

Interpretation:

1. the external baseline floor is now established and published
2. H1/H2 are real capability regimes, not baseline artifacts
3. later full-corpus, schema-only, anchor-only, and topology-only lines did not recover the H1/H2 regime
4. the highest-value remaining training-side question is the minimal reproducible mechanism behind H1/H2-class exact tool-call realization

---

# Naming Note

The user requested a "Stage D" launch plan for H1/H2 causal mechanism isolation.

Be aware that `docs/phase_d/` already exists in this repository and refers to the post-Stage-C roadmap reconciliation package.

For any later implementation package, avoid overloading the existing `phase_d` path family.

Use a distinct family name or path if new documentation is created.

---

# Starting Evidence Base

The new thread should treat the following as the primary evidence spine for this study:

## Published Baseline Package

- `docs/current/baselines/README.md`
- `docs/current/baselines/LLAMA31_PROJECT_WIDE_COMPARISON.md`
- `evals/baselines/llama31/README.md`
- `evals/baselines/llama31/canonical_baseline_index.json`
- `evals/baselines/llama31/project_wide_comparison_table.json`

## Current Run Ordering

- `docs/current/status/TRAINING_RUN_HISTORY.md`

## H1/H2 Mechanism And Preservation Analysis

- `docs/phase_r/PHASE_R_COMPLETION_REPORT.md`
- `docs/phase_r/SCHEMA_REALIZATION_ANALYSIS.md`
- `docs/phase_r/H1_H2_SUCCESS_FACTORS.md`
- `docs/phase_v/PRESERVATION_MODEL_ANALYSIS.md`
- `docs/phase_v/H1_H2_SUCCESS_PRESERVATION_FACTORS.md`
- `docs/phase_v/CONTROL_SURFACE_COMPARISON.md`

## Superseding Causal Recommendation

- `docs/phase_zk/NEXT_CAUSAL_TARGET_RECOMMENDATION.md`
- `docs/phase_zk/PHASE_ZK_COMPLETION_REPORT.md`

## Prior Controlled-Ablation Scaffolding

- `docs/phase_x/ARM_SPECIFICATIONS.md`
- `docs/phase_x/VALIDATION_CHECKLIST.md`
- `docs/phase_x/STOP_RULE_CLARIFICATION.md`

## Doctrine

- `docs/goal_charter_v5a.md`
- `docs/appendix_a_operational_execution_contract_v3a.md`
- `docs/metric_specification_v1a.md`
- `evals/canonical_eval_manifest_v1.json`

---

# Goal

Define and later execute a bounded, preregistered, schema-realization-first control study that isolates the minimal reproducible mechanism behind H1/H2-class exact tool-call realization.

The study should prioritize causal interpretability over broad remediation.

The study should treat exact `tool_calls` envelope realization as the primary causal object.

---

# Study Scope

The study should:

1. reconstruct the frozen i3/H0 scaffold
2. reconstruct the H1 and H2 replacement surfaces from preserved repository artifacts
3. isolate the smallest plausible causal factors:
   - exact `tool_calls` envelope pressure
   - anchor concentration
   - cue phrasing
   - patch budget
   - non-tool/no-call balance
   - contamination bounds
4. keep non-tool rows, tool mix, patch budget, decode settings, and evaluator contract fixed wherever practical
5. include at least one H2-like treatment
6. include at least one matched semantic-control treatment with weaker outer-envelope enforcement

The study should not begin as a broad dataset redesign.

---

# Frozen Surfaces To Reconstruct

## Scaffold / Control Surface

- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_val.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_summary.json`
- `configs/lora/stage_b_llama31_8b_base_v1_i3.config.json`
- `manifests/runs/stage_b_llama31_8b_base_v1_i3.run_manifest.json`

## H0 / H1 / H2 Reference Surfaces

- `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.config.json`
- `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.config.json`
- `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.config.json`
- `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h0_control_i3_micro.run_manifest.json`
- `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.run_manifest.json`
- `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h2_commitment_patch.run_manifest.json`
- `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_train.jsonl`
- `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_val.jsonl`
- `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_summary.json`
- `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_train.jsonl`
- `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_val.jsonl`
- `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_summary.json`
- `evals/runs/stage_b_v1_phase_i_h0_control_i3_micro_eval_20260611T103048Z/summary.json`
- `evals/runs/stage_b_v1_phase_i_h1_diversity_patch_eval_20260611T125835Z/summary.json`
- `evals/runs/stage_b_v1_phase_i_h2_commitment_patch_eval_20260611T120228Z/summary.json`

## Eval Contract

- `evals/canonical_eval_manifest_v1.json`
- decode defaults pinned by Appendix A
- same scorer/evaluator path as the preserved H-series runs

---

# Preregistered Hypotheses

## Primary Hypothesis

H1/H2-class capability depends on a conjunctive surface:

1. frozen scaffold
2. low-delta patch-local replacement
3. strong exact `tool_calls` envelope pressure
4. high anchor concentration
5. narrow exact-tool-request cue regime

## Secondary Hypothesis

If semantics, tools, arguments, patch positions, and patch budget are held fixed, weakening the outer-envelope pressure should materially reduce exact JSON realization.

## Tertiary Hypothesis

If envelope pressure is preserved, reducing anchor concentration from H2-like levels should reduce exact realization, but not necessarily collapse it to the external baseline floor.

---

# Proposed Experiment Matrix

Use the historical H0/H1/H2 artifacts as frozen comparators.

The new execution slice should start with three new arms only.

## Historical References

- `R0` = historical H0 comparator only
- `R1` = historical H1 comparator only
- `R2` = historical H2 comparator only

No new training is required for these reference rows.

## New Arms

### A1 — H2-Like Positive Control

Purpose:

Reproduce the strongest known successful mechanism as closely as possible from preserved evidence.

Properties:

- frozen i3 scaffold
- same train/val row counts
- same non-tool/no-call block
- `100` tool-positive replacement rows
- H2-like patch-local replacement surface
- H2-like anchor concentration
- strong exact-tool-request cue
- strong explicit outer `tool_calls` envelope pressure

Expected reading:

If this arm cannot substantially reproduce H2-class behavior, the mechanism is not yet isolated at reconstruction fidelity.

### A2 — Matched Semantic Control With Weaker Outer-Envelope Enforcement

Purpose:

Directly test whether outer-envelope pressure matters when semantics are held fixed.

Properties:

- same scaffold as A1
- same patch positions as A1
- same tools and argument intents as A1
- same patch budget as A1
- same anchor concentration as A1
- weaker positive-row cue: generic tool-use / strict-JSON language without the strongest explicit `tool_calls` envelope emphasis

Expected reading:

If A2 materially underperforms A1, outer-envelope pressure remains a plausible causal factor.

### A3 — Anchor Step-Down Under Preserved Envelope

Purpose:

Test whether H2-like anchor mass is still required once envelope pressure is preserved.

Properties:

- same scaffold as A1
- same patch budget as A1
- same strong envelope/cue regime as A1
- reduced anchor concentration toward the v1.2 / H1 intermediate region

Expected reading:

If A3 drops materially below A1, anchor concentration remains contributory inside the preserved envelope regime.

## Conditional Extension

### A4 — Budget Step-Down

Only authorize if A1 is admissible and materially successful.

Purpose:

Test whether the H2 mechanism still works at a smaller patch budget.

Properties:

- same scaffold as A1
- same cue/envelope regime as A1
- same tool-family mix as A1
- reduced replacement budget, e.g. `60` rows

Expected reading:

This isolates minimum budget only after the primary positive-control reconstruction works.

---

# Fixed Factors

Hold fixed wherever practical:

1. canonical eval manifest
2. decode settings
3. non-tool scaffold bytes
4. validation split bytes
5. train row count
6. validation row count
7. safety/no-call category counts
8. patch budget across A1-A3
9. tool-family support set across A1-A3
10. evaluator/scorer scripts
11. masking and preflight rules

---

# Acceptance Criteria

## Reconstruction Acceptance

Before any new arm is launched:

1. the i3 scaffold is verified against preserved hashes or equivalent row-level integrity checks
2. H1 and H2 replacement surfaces are reconstructed mechanically from the preserved dataset summaries and train JSONL
3. reconstructed counts match published summaries for:
   - patch size
   - tool-positive counts
   - tool-family counts
   - frozen non-tool preservation

## Execution Acceptance

For the new study to count as scientifically successful:

1. A1 passes all admissibility gates
2. A1 reaches at least a strong directional reproduction band:
   - exact JSON `>= 0.40`
   - tool-name `>= 0.65`
   - argument `>= 0.60`
3. A1 materially outperforms A2 on exact JSON realization or envelope-drift reduction
4. A3 yields an interpretable anchor-effect delta relative to A1, even if not promotable

## Negative But Informative Outcomes

The study is still scientifically useful if:

1. A1 is admissible but fails to reproduce H2
2. A1 and A2 are close, weakening envelope pressure as a primary driver
3. A1 succeeds but A3 degrades, supporting anchor contribution

---

# Failure Taxonomy And Stop Rules

Use the prior causal-test distinction:

## Attribution Failure

Hard stop.

Any of:

1. contamination overlap becomes nonzero on heldout validation, tool holdout, no-call, adversarial, or direct-answer splits
2. scaffold bytes drift
3. eval contract drifts
4. cue template drifts outside preregistered allowance
5. safety block is rebuilt instead of preserved

## Operational Failure

Hard stop on that arm until repaired.

Any of:

1. builder failure
2. path resolution failure
3. preflight failure
4. artifact incompleteness
5. inability to reconstruct H2-like control surface faithfully

## Promotion Failure

Not a causal-test failure.

Safety regression alone makes the arm non-promotable, but it can still be scientifically informative if all fixed boundaries remained intact.

## Initial Run Budget

Keep the first execution slice to:

1. A1
2. A2
3. A3

Do not launch A4 unless A1 succeeds and the reconstruction logic is trusted.

---

# Required Artifact List

The later implementation thread should plan to emit:

1. experiment declaration JSON
2. frozen-surface hash snapshot
3. i3 scaffold verification report
4. H1 reconstruction fidelity report
5. H2 reconstruction fidelity report
6. arm-spec JSON for A1-A3
7. contamination report for each arm
8. dataset summary for each arm
9. draft config for each arm
10. draft run manifest for each arm
11. preflight validation report for each arm
12. training summary for each executed arm
13. canonical eval summary for each executed arm
14. `comparison_rows.jsonl` for each executed arm
15. post-run attribution report comparing A1-A3 to H0/H1/H2/Phase Q

---

# Validation Gates

## Gate 1 — Frozen Surface Verification

Verify:

1. i3 scaffold
2. canonical eval manifest
3. train script
4. eval script
5. model-path assumptions

## Gate 2 — Reconstruction Fidelity

Verify:

1. H1 patch size and tool counts
2. H2 patch size and tool counts
3. replacement positions or equivalent row-identity mapping
4. unchanged non-tool slices

## Gate 3 — Arm Admissibility

Verify for each arm:

1. zero contamination
2. fixed cue compliance
3. scaffold invariance
4. `tool_calls` envelope validity
5. fixed safety-block counts

## Gate 4 — Preflight Readiness

Verify:

1. config completeness
2. manifest completeness
3. masking/preflight pass
4. no unintended file modifications

## Gate 5 — Canonical Eval Completion

Verify:

1. frozen manifest used
2. full artifact set emitted
3. result comparability to H0/H1/H2/Phase Q

## Gate 6 — Attribution Review

Verify:

1. whether A1 reproduced enough of H2 to validate the reconstruction
2. whether A2 isolates envelope pressure
3. whether A3 isolates anchor contribution under preserved envelope pressure

---

# Risks And Mitigations

## Risk 1 — Name Collision With Existing Phase D

Mitigation:

Do not place later implementation docs under the existing `docs/phase_d/` family without an explicit rename decision.

## Risk 2 — False Negative From Bad Reconstruction

Mitigation:

Require reconstruction fidelity reports before any run.

## Risk 3 — Semantic-Control Confound

Mitigation:

Keep patch positions, tools, arguments, budget, scaffold, and counts fixed between A1 and A2.
Change only the outer-envelope / cue-pressure regime.

## Risk 4 — Underpowered Budget Interpretation

Mitigation:

Do not vary patch budget in the core slice.
Only test budget after a successful positive control.

## Risk 5 — Overclaiming Transferability

Mitigation:

Treat this study as mechanism isolation on the frozen i3/H-series surface.
Do not interpret success as cross-scaffold generalization.

## Risk 6 — Safety Regression Noise

Mitigation:

Separate promotability from causal informativeness.
Use the fixed-boundary attribution model.

---

# Recommended First Executable Task

The next thread should begin with a **reconstruction-verification package**, not a new training run.

That package should:

1. verify the frozen i3 scaffold against preserved evidence
2. reconstruct the H1 and H2 replacement surfaces from the preserved train JSONL plus summary artifacts
3. produce a row-level fidelity report showing:
   - patch size
   - replacement positions or equivalent mapping
   - tool-family allocation
   - cue regime
   - frozen non-tool preservation
4. define A1/A2/A3 mechanically from that reconstruction

Reason:

If the H1/H2 surfaces cannot be reconstructed cleanly from the repository's own preserved evidence, any later causal run will be ambiguous before training even starts.

---

# Bottom Line

The repository is now in a good state to pursue a bounded H1/H2 causal mechanism isolation study.

The highest-value next move is not another broad redesign.

It is a preregistered, control-preserving, schema-realization-first study that:

1. starts from the frozen i3 scaffold
2. treats H2-like reconstruction as the positive control
3. pairs it with a matched semantic control with weaker outer-envelope enforcement
4. keeps the rest of the study mechanically narrow enough to preserve attribution

This continuity note should be sufficient to start a new thread cleanly.
