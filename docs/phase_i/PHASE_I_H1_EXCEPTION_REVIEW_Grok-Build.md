# Phase I H1 Exception Review

**Reviewer:** Grok-Build (independent governance review)  
**Date:** 2026-06-11  
**Scope:** One-time diagnostic exception for `H1_diversity_patch` despite Phase I run-level stop ceiling  
**Constraint:** Prior Phase H, Phase I, and stop-rule decisions are assumed correct. No experiment redesign.

---

## Executive Summary

Phase I is formally closed under the attribution `inconclusive_external_first`. Both `H0_control_i3_micro` and `H2_commitment_patch` tripped Phase H kill metrics (adversarial no-call for H0; wrapper leakage plus no-call/adversarial regressions for H2). The published run-level stop ceiling was therefore activated and correctly prevented execution of `H1_diversity_patch`.

`H2_commitment_patch` produced a clear, large-magnitude commitment-dominant signal: tool-holdout exact-valid rose from 0.0 to 0.525, no-anchor exact-valid from 0.0 to 0.844, and tool-name/argument accuracy improved by approximately +0.70 and +0.63 points respectively. These movements align with the failure profile observed in H0 (heavy near-canonical wrapper/envelope drift and direct-answer substitution). However, H2 also introduced wrapper leakage (0.005) and regressed adversarial no-call correctness from 0.75 (already a kill) to 0.4.

**Determination: Do not grant H1 exception.**

`H1_diversity_patch` would complete the minimum viable first-screen pair specified in the Phase H design, but the remaining attribution value is marginal and does not justify overriding a correctly applied stop ceiling after formal closure. H2 already supplies sufficient directional evidence that commitment—not tail-tool diversity restoration—is the binding internal lever on this training surface. A third kill-likely run would not convert the official `inconclusive_external_first` state, would not enable a formal A/B/C winner under the published thresholds, and would undermine the explicit anti-loop purpose of the ceiling. The higher-value path remains external-first remediation that preserves the observed commitment gains while addressing the safety regression.

**Choice: A — No exception. Phase I remains closed.**

---

## Evidence Reviewed

### Authoritative Phase I closure and checkpoint artifacts

| Artifact | Relevance |
|---|---|
| `docs/phase_i/PHASE_I_FINAL_COMPLETION_REPORT.md` | Formal closure with `inconclusive_external_first`; H1 explicitly blocked by ceiling after two kills; provisional B signal noted but not formal |
| `docs/phase_i/BOTTLENECK_ATTRIBUTION_DECISION.md` | Records that H0+H2 produced strong commitment signal but first-screen pair incomplete; official state `inconclusive_external_first` |
| `docs/phase_i/RUN_COMPARISON_MATRIX.md` | Detailed H0/H2 metrics, deltas, and stop-rule outcomes; H1 row marked "Blocked by run-level stop ceiling" |
| `docs/phase_i/H2_CHECKPOINT_REPORT.md` | Full H2 results, kill-metric trips (wrapper leakage, no-call correctness, adversarial), tool-holdout/no-anchor lifts, diagnostic profile (direct-answer substitution reduced to 9 rows) |
| `docs/phase_i/H0_CHECKPOINT_REPORT.md` | H0 baseline metrics and kill on adversarial no-call (0.75); dominant failure modes (102 wrapper/envelope drift, 18 direct-answer) |
| `docs/phase_i/CONTINUATION_AUTHORITY_RECORD.md` | Prior authorization for H2 and H1 as diagnostic/report-only probes (pre-H2 execution); explicitly does not preempt later run-level ceiling |
| `docs/phase_i/PHASE_H_GATE_REVIEW_AND_PHASE_I_CONTINUATION_DETERMINATION.md` | Gate review that authorized the prepared first-screen pair after H0 hard-stop; notes that authorization was diagnostic-only and that two kills would still trigger ceiling |

### Authoritative Phase H design and stop-rule artifacts

| Artifact | Relevance |
|---|---|
| `docs/phase_h/STOP_RULES_AND_DECISION_GATES.md` | Run-level stop rule (L39): do not continue internal-only after two kill trips; purpose is to avoid open-ended tradeoff chasing; external-first stop rules |
| `docs/phase_h/SUCCESS_AND_FAILURE_CRITERIA.md` | Kill metrics (wrapper leakage >0, no_call/adversarial correctness <1.0); Hypothesis A/B thresholds (including B.3 H1-vs-H2 tool-holdout comparison); report-only status for kill runs; inconclusive band definition |
| `docs/phase_h/EXPERIMENTAL_MATRIX.md` | Minimum viable set = H0 + H2 + H1 for first-screen diversity vs commitment; preferred order and interpretation table |
| `docs/phase_h/CANDIDATE_INTERVENTION_ANALYSIS.md` | H1 = bounded tail-tool / internal family diversity restoration; H2 = anchor-light paraphrastic commitment pressure; distinct target effects and expected evidence patterns |
| `docs/phase_h/MINI_EXECUTION_PACKAGE.md` | Explicit escalation trigger: "two runs trip kill metrics"; completion requires first-screen pair or external-first trigger |

### Execution assets (prepared but not run for H1)

| Asset | Status |
|---|---|
| `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.config.json` | Present (prepared) |
| `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.run_manifest.json` | Present (prepared) |
| `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_train.jsonl` | Present (built, +100 tail-tool rows, non-tool slices frozen, contamination clean per prior validation) |
| `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_summary.json` | Present (validated) |

### Key metrics (repository-recorded)

**H0 (control):**
- `exact_json_validity = 0.045`
- `tool_name_accuracy = 0.07142857142857142`
- `argument_accuracy = 0.06428571428571428`
- `tool_holdout_exact_valid = 0.0`
- `heldout_validation_exact_valid = 0.09`
- `no_anchor_exact_valid = 0.0`
- `wrapper_leakage = 0.0`
- `no_call_correctness = 0.9166666666666666`
- `adversarial_no_call_correctness = 0.75` (kill metric tripped)

**H2 (commitment patch):**
- `exact_json_validity = 0.48` (+0.435 vs H0)
- `tool_name_accuracy = 0.7714285714285715` (+0.700)
- `argument_accuracy = 0.6928571428571428` (+0.629)
- `tool_holdout_exact_valid = 0.525` (+0.525)
- `heldout_validation_exact_valid = 0.75` (+0.660)
- `no_anchor_exact_valid = 0.84375` (+0.844)
- `wrapper_leakage = 0.005` (kill)
- `no_call_correctness = 0.8`
- `adversarial_no_call_correctness = 0.4` (kill)
- Direct-answer substitution on non-exact tool rows: 9 (vs H0's 18)

**H1:** Not executed. Blocked by run-level stop ceiling after H0 and H2 each tripped kill metrics. Assets prepared inside Phase H bounded-patch envelope.

---

## Attribution Value Assessment

### Question 1: Would H1 still provide meaningful attribution value?

**Partially — for formal completeness of the designed matrix — but not enough to justify an exception.**

H1 remains the designated probe for Hypothesis A (diversity-dominant). Executing it would:
- Finish the minimum viable first-screen set (H0 + H2 + H1) called out in `EXPERIMENTAL_MATRIX.md` and `MINI_EXECUTION_PACKAGE.md`.
- Permit direct numerical comparison of H1 versus H2 on tool-holdout exact-valid, tool-name accuracy, and argument accuracy.
- Test whether restoring omitted internal tool families (list_dir, list_models, move_path, git_diff, etc.) produces a meaningfully different capability/safety tradeoff surface than the commitment paraphrase used in H2.

The *remaining* value is substantially diminished for these reasons:

1. H2 already moved the primary attribution metrics far outside the inconclusive band. Tool-holdout exact-valid and no-anchor exact-valid both left zero by large margins. These are the exact metric families H1 was intended to compete on.

2. Per `SUCCESS_AND_FAILURE_CRITERIA.md`, favoring A requires H1 to (a) beat H0 by ≥5 pp on tool-holdout or tool-name accuracy *and* (b) outperform H2 by ≥5 pp on tool-holdout. With H2 already at 0.525 on tool-holdout, H1 would need >0.575. H1's intervention (bounded tail-tool diversity restoration on the same frozen non-tool slices and microprobe surface) targets a different residual category than H0's dominant failure modes (near-canonical wrapper/envelope drift and direct-answer substitution). Overturning H2's observed lead is therefore implausible on the published thresholds.

3. H1 is unlikely to be safety-clean. H0 already killed on adversarial (0.75). H2 worsened the regression (to 0.4) and introduced the first wrapper leakage. H1 uses the identical frozen training surface and eval contract. A third run is more likely to reproduce or extend the safety pattern than to invert it.

4. Even a successful H1 execution would not change the official attribution. All three first-screen runs would be kill-dirty. Per the kill-metric rules, such runs "may still be documented as evidence, but they do not authorize continued internal-only iteration." The state would remain `inconclusive_external_first` (or a procedural variant); no formal A/B/C/D/E winner could be declared.

**Conclusion:** H1 would deliver completeness and a negative confirmation on A, but it would not supply decision-changing attribution value given the magnitude and direction of the H2 signal already in hand.

### Question 2: Has H2 already supplied enough evidence to make H1 unnecessary?

**Yes for practical attribution and selection of the next remediation path. No for literal application of every published threshold clause.**

**Why H2 is sufficient for the actionable question:**
- H2 is the explicit Hypothesis B (commitment-dominant) probe. It produced precisely the metric-family movements Phase H predicted for commitment: large no-anchor lift, tool-holdout lift off zero, sharp tool-name/argument gains, and measurable reduction in direct-answer substitution.
- H0's failure profile was commitment-shaped (heavy direct-answer substitution + near-canonical wrapper drift on tool rows; 0% no-anchor exact-valid). H2 was designed against that profile and moved it dramatically.
- H1's intervention (per `CANDIDATE_INTERVENTION_ANALYSIS.md`) restores tool-family breadth rather than applying commitment/anti-direct-answer pressure. Nothing in the H0 or H2 results indicates that absence of tail-tool diversity — rather than commitment failure — is the binding constraint on this surface.

**Why H2 alone cannot formally close Hypothesis B:**
- Threshold B.3 requires confirming that "H1 does not outperform H2 on tool-holdout exact-valid by more than 5 points." That specific comparison is undefined without H1 data.
- The first-screen pair is therefore formally incomplete relative to `EXPERIMENTAL_MATRIX.md` and the minimum viable set.

**Conclusion:** H2 supplies enough *directional and diagnostic* evidence to make H1 unnecessary for choosing the next step (external-first remediation). It does not supply enough *formal threshold* evidence to declare B under the letter of the rules — but that formal gap cannot be closed productively by executing another kill-likely run on a surface where the ceiling has already terminated internal iteration.

### Question 3: Would running H1 materially improve confidence in A / B / C?

| Hypothesis | Confidence improvement from H1 | Rationale |
|---|---|---|
| **A (diversity-dominant)** | **Low** | H2 already produced large, clean lifts on the primary metrics H1 was built to contest. H1 would at best supply negative confirmation that diversity restoration is not competitive here. |
| **B (commitment-dominant)** | **Low–Medium** | The provisional B signal is already strong and internally consistent with H0's failure profile. H1 underperforming H2 would strengthen the informal case for B, but formal declaration of B remains blocked by kill metrics on the executed runs. |
| **C (schema-dominant)** | **Low** | H3 was never authorized under the continuation determination or the H1 exception request. H1's intervention does not target invalid-schema or missing_tool_calls / payload_not_object rates. |

H1 could in principle help discriminate B versus a combined (E) determination if it showed nonzero movement on a *different* primary metric family than H2. Given the breadth of H2's gains across tool-holdout, no-anchor, and accuracy families, a combined determination would still require H1 to win clearly on at least one primary family — an outcome that is improbable given the distinct intervention semantics.

**Conclusion:** H1 would not materially improve confidence in any formal winner. At best it would add low-cost negative evidence against A.

### Question 4: Scientific value of H1 today relative to one additional training run / one additional canonical eval?

| Option | Scientific value | Actionability |
|---|---|---|
| **H1 diagnostic run** | Low–Medium: completes the designed matrix; mostly negative confirmation on A; high probability of kill trip | Does not advance promotion eligibility or external handoff; does not change official attribution or recommended next workstream |
| **One additional training run (external-first remediation)** | **High**: targets the known safety regression while attempting to retain H2's commitment-side gains on tool-holdout, no-anchor, and accuracy | Directly actionable per the explicit recommendation in `PHASE_I_FINAL_COMPLETION_REPORT.md` |
| **One additional canonical eval** | Low for attribution: re-baselines the current surface without introducing a new intervention signal | Useful for monitoring drift or post-remediation comparison, not for A/B discrimination |

H1 training + eval cost is small (~170 s + ~35 s). The governance and precedent cost of overriding a correctly-applied run-level ceiling after formal closure is not trivial. The scientific return per unit of authorized internal iteration is lower than moving to external-first remediation.

---

## Governance Assessment

### Applicable rules (assumed correctly applied)

1. **Kill metrics** (`SUCCESS_AND_FAILURE_CRITERIA.md`): H0 tripped adversarial correctness <1.0; H2 tripped wrapper leakage >0, no_call correctness <1.0, and adversarial correctness <1.0. Both runs documented as report-only.
2. **Run-level stop ceiling** (`STOP_RULES_AND_DECISION_GATES.md` L39): "do not continue to another internal-only run if two runs have already tripped kill metrics." Explicit purpose: avoid turning internal experimentation into open-ended tradeoff chasing.
3. **Mini stop condition** (`MINI_EXECUTION_PACKAGE.md`): "two runs trip kill metrics" is listed as an explicit escalation trigger.
4. **Phase I closure** (`PHASE_I_FINAL_COMPLETION_REPORT.md`, `BOTTLENECK_ATTRIBUTION_DECISION.md`): formal attribution `inconclusive_external_first`; "No additional internal-only run should be launched unless a new governance route explicitly authorizes it."

### Exception request in context

The prior continuation determination (`PHASE_H_GATE_REVIEW_AND_PHASE_I_CONTINUATION_DETERMINATION.md` and `CONTINUATION_AUTHORITY_RECORD.md`) authorized H2 and H1 together as *diagnostic/report-only* probes *before* H2 executed and became the second kill. That authorization did not (and could not) preempt the run-level ceiling. Once H2 tripped its kills, the ceiling correctly activated and H1 was blocked. The current request is therefore not completion of an open authorization window; it is a request to override a correctly-applied stop rule after formal Phase I closure.

### Governance test

Under the narrow question — *does the remaining attribution value justify a single diagnostic-only exception?* — the burden is on the requester to demonstrate that the exception would:
1. Recover decision-critical evidence that is not already available from H0 + H2.
2. Not reopen internal-only iteration or weaken anti-loop discipline.
3. Change the recommended next action or the formal attribution state.

**H1 fails all three tests:**
1. H0 + H2 already discriminate commitment as the dominant internal lever on this surface (large, directional, threshold-exceeding movement on the exact metrics and diagnostic families the first screen was designed to contrast).
2. Granting a third run after two kills directly contradicts the ceiling's stated purpose.
3. Official attribution would remain `inconclusive_external_first`; the recommended next action remains external-first remediation regardless of any plausible H1 outcome.

### Options evaluated

| Option | Assessment |
|---|---|
| **A — No exception** | **Selected.** Preserves the integrity of the stop ceiling; H2 signal is sufficient for next-step guidance and external-first planning. |
| **B — One-time H1 diagnostic exception** | Rejected. Marginal attribution gain (completeness + negative A confirmation) does not outweigh the governance and anti-loop cost of overriding a correctly applied ceiling after closure. |
| **C — Reopen Phase I generally** | Rejected. Explicitly out of scope per the query constraints; would violate the formal closure determination and invite scope expansion beyond the authorized slice. |

---

## Risk Assessment

### Risks of granting the exception

| Risk | Severity |
|---|---|
| Precedent for overriding correctly-applied stop ceilings after formal closure | **High** |
| Third kill trip on the same surface, reinforcing the observed safety-regression pattern | **Medium–High** |
| Delaying higher-value external-first remediation work | **Medium** |
| "Completeness chasing" without any change to official attribution or recommended path | **Medium** |
| Post-hoc reinterpretation pressure if H1 produced any lift on secondary metrics | **Medium** |

### Risks of denying the exception

| Risk | Severity |
|---|---|
| First-screen pair remains formally incomplete | **Low** (already explicitly acknowledged in closure artifacts) |
| Hypothesis B threshold B.3 never formally verified | **Low** (formal B declaration is blocked by kill metrics on executed runs regardless) |
| Residual uncertainty whether a diversity patch could have matched or exceeded H2 on tool-holdout | **Low–Medium** (H2's magnitude on the targeted metrics makes this outcome unlikely) |

**Net risk posture:** Denying the exception is the lower-risk course. The documented provisional commitment signal, the H0/H2 comparison matrix, and the external-first recommendation do not depend on H1 data.

---

## Determination

### Required answers

| Question | Answer |
|---|---|
| Q1: Meaningful H1 attribution value? | Partial only (completeness + negative confirmation on A); not decision-changing |
| Q2: H2 sufficient to make H1 unnecessary? | Yes for practical guidance and next-step selection; no for literal formal threshold B.3 |
| Q3: Materially improve A/B/C confidence? | No |
| Q4: Scientific value vs alternatives? | Lower than one external-first training run; comparable to or below a re-baseline eval for attribution purposes |
| Q5: Exception choice? | **A — No exception** |

### Final determination

**Do not grant H1 exception.**

Phase I remains closed with attribution `inconclusive_external_first`. The run-level stop ceiling was applied correctly after two kill-metric trips. `H2_commitment_patch` already provides the dominant actionable signal on this surface: commitment intervention produces large tool-side gains (tool-holdout, no-anchor, tool-name/argument accuracy) but at unacceptable safety cost (wrapper leakage and adversarial regression). The next authorized workstream is external-first remediation that attempts to retain the commitment gains while eliminating the safety regression — not a third internal-only diagnostic run on the same kill-sensitive surface.

---

## Confidence Level

**Medium (≈70%)**

**High confidence on:**
- Recorded H0 and H2 metric values, deltas, and kill-metric status (directly from canonical eval summaries and checkpoint reports)
- Correct application of the run-level stop ceiling (STOP_RULES_AND_DECISION_GATES.md, MINI_EXECUTION_PACKAGE.md, FINAL_COMPLETION_REPORT.md, RUN_COMPARISON_MATRIX.md)
- Magnitude and direction of H2's commitment-dominant signal (tool-holdout +0.525, no-anchor +0.844, accuracy gains)
- That an H1 exception would not convert the official attribution state to a formal B (or any other winner) under the published rules

**Moderate uncertainty on:**
- Exact quantitative outcome H1 would have produced (counterfactual; the run was never executed)
- Whether H1 would have exhibited a materially better (or worse) safety profile than H2 on the same surface (possible in principle but insufficient to change the governance outcome)

**Lower confidence on:**
- Whether downstream stakeholders would accept a provisional B determination without the formal H1 comparison data (organizational judgment rather than pure evidentiary)

---

## Direct Answer

```
Do not grant H1 exception
```

Phase I remains closed. Proceed to external-first work that preserves the observed commitment gains on tool-holdout, no-anchor, and accuracy metrics while eliminating the safety regression, consistent with the recommendation in `PHASE_I_FINAL_COMPLETION_REPORT.md`.

---

## Boundary Confirmation

This review remained strictly inside the authorized slice:
- Request classification confirmed as bounded governance exception review on a closed phase.
- No redesign of Phase H, Phase I, experimental matrix, thresholds, or datasets.
- No new workstreams, training runs, or promotion recommendations introduced.
- All prior decisions (including the H0 hard stop, H2 execution, and subsequent closure) assumed correct per explicit constraint.
- Stop-and-escalate conditions checked: none triggered (no authority conflicts, catalog contradictions, undefined ownership, or scope expansion).
- Hygiene and governance-boundary checklists applied at the outset; only the expected deliverable artifact is untracked.
- Evidence drawn exclusively from authoritative in-repository artifacts listed above. No external data or reinterpretation of stop rules.

The determination rests solely on whether remaining attribution value justifies the requested one-time diagnostic exception. It does not.