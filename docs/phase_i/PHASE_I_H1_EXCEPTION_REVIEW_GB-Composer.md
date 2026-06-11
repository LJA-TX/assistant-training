# Phase I H1 Exception Review

**Reviewer:** Grok-Build (independent governance review)  
**Date:** 2026-06-11  
**Scope:** One-time diagnostic exception for `H1_diversity_patch` despite Phase I run-level stop ceiling  
**Constraint:** Prior Phase H, Phase I, and stop-rule decisions are assumed correct. No experiment redesign.

---

## Executive Summary

Phase I is formally closed with attribution `inconclusive_external_first`. `H0_control_i3_micro` and `H2_commitment_patch` each tripped Phase H kill metrics; the run-level stop ceiling correctly blocked `H1_diversity_patch`. `H2` produced a strong commitment-dominant signal on tool-holdout, no-anchor exact-valid, and tool-name/argument accuracy, but introduced wrapper leakage and sharp adversarial no-call regression.

**Determination: Do not grant H1 exception.**

`H1` would add marginal attribution value at this point. `H2` already supplies sufficient directional evidence that commitment intervention—not diversity restoration—is the binding internal lever on this surface. A third kill-likely run on the same frozen training surface would not materially improve confidence in A/B/C formal winners, would not convert the official `inconclusive_external_first` state under the published framework, and would weaken the anti-loop intent of the run-level stop ceiling. External-first remediation preserving commitment gains while fixing safety regression is the higher-value next step.

**Choice: A — No exception. Phase I remains closed.**

---

## Evidence Reviewed

### Authoritative Phase I closure artifacts

| Artifact | Relevance |
|---|---|
| `docs/phase_i/PHASE_I_FINAL_COMPLETION_REPORT.md` | Formal closure; `inconclusive_external_first`; H1 blocked |
| `docs/phase_i/BOTTLENECK_ATTRIBUTION_DECISION.md` | Provisional commitment signal; first-screen pair incomplete |
| `docs/phase_i/RUN_COMPARISON_MATRIX.md` | H0/H2 metrics and deltas; H1 not launched |
| `docs/phase_i/H2_CHECKPOINT_REPORT.md` | H2 kill metrics; commitment diagnostic profile |
| `docs/phase_i/H0_CHECKPOINT_REPORT.md` | H0 baseline and adversarial seam |
| `docs/phase_i/CONTINUATION_AUTHORITY_RECORD.md` | Prior H2/H1 diagnostic authorization scope |

### Authoritative Phase H design and stop rules

| Artifact | Relevance |
|---|---|
| `docs/phase_h/STOP_RULES_AND_DECISION_GATES.md` | Run-level ceiling after two kill trips |
| `docs/phase_h/SUCCESS_AND_FAILURE_CRITERIA.md` | Hypothesis A/B thresholds; kill metrics |
| `docs/phase_h/EXPERIMENTAL_MATRIX.md` | Minimum viable set; first-screen pair purpose |
| `docs/phase_h/CANDIDATE_INTERVENTION_ANALYSIS.md` | H1 vs H2 intervention semantics |
| `docs/phase_h/MINI_EXECUTION_PACKAGE.md` | Stop condition: two kill-metric trips |

### Execution assets (prepared but not run)

| Asset | Status |
|---|---|
| `configs/lora/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.config.json` | Ready |
| `manifests/runs/stage_b_llama31_8b_base_v1_phase_i_h1_diversity_patch.run_manifest.json` | Ready |
| `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_train.jsonl` | Built (+100 tail-tool rows) |
| `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_summary.json` | Validated |

### Key metrics (repository-recorded)

**H0 (control):**

- `exact_json_validity = 0.045`
- `tool_name_accuracy = 0.071`
- `argument_accuracy = 0.064`
- `tool_holdout_exact_valid = 0.0`
- `no_anchor_exact_valid = 0.0`
- `adversarial_no_call = 0.75` (kill)

**H2 (commitment patch):**

- `exact_json_validity = 0.48` (+0.435 vs H0)
- `tool_name_accuracy = 0.771` (+0.700)
- `argument_accuracy = 0.693` (+0.629)
- `tool_holdout_exact_valid = 0.525` (+0.525)
- `heldout_validation_exact_valid = 0.75` (+0.660)
- `no_anchor_exact_valid = 0.844` (+0.844)
- `wrapper_leakage = 0.005`, `no_call_correctness = 0.8`, `adversarial_no_call = 0.4` (kill)

**H1:** Not executed. Blocked by run-level stop ceiling.

---

## Attribution Value Assessment

### Question 1: Would H1 still provide meaningful attribution value?

**Partially, but not enough to justify an exception.**

H1 remains the designed discriminator for Hypothesis A (diversity-dominant). Running it would:

- Complete the formal first-screen pair that Phase H specified as minimum viable.
- Allow direct H1-vs-H2 comparison on tool-holdout exact-valid and tool-name/argument accuracy.
- Test whether tail-tool family restoration (`list_dir`, `list_models`, `move_path`, `git_diff`, etc.) produces a different capability/safety tradeoff than commitment paraphrase.

However, the *remaining* value is diminished because:

1. **H2 already moved the decisive metrics off zero.** Tool-holdout exact-valid rose from `0.0` to `0.525`; no-anchor exact-valid rose from `0.0` to `0.844`. These are not marginal deltas inside the ±5 pp inconclusive band—they are large, directional movements on the metrics H1 was designed to compete on.

2. **Hypothesis A winning now requires an implausible H1 outcome.** Per `SUCCESS_AND_FAILURE_CRITERIA.md`, favoring A requires H1 to beat H0 by ≥5 pp on tool-holdout or tool-name accuracy *and* outperform H2 by ≥5 pp on tool-holdout. H1 would need tool-holdout ≥ `0.575` while H2 already sits at `0.525`. Given H1's intervention targets underrepresented tail tools rather than the dominant H0 failure modes (near-canonical wrapper/envelope drift, direct-answer substitution on `read_file`/`rg_search`), overturning H2's signal is unlikely.

3. **H1 is unlikely to be safety-clean.** H0 tripped adversarial at `0.75`; H2 worsened adversarial to `0.4` and introduced wrapper leakage. H1 shares the same frozen microprobe surface, non-tool slices, and adversarial eval contract. A third run is more likely to extend the safety-regression pattern than to resolve it.

4. **Formal winner declaration would remain blocked.** Kill-metric runs may be documented as report-only evidence but do not authorize continued internal iteration (`SUCCESS_AND_FAILURE_CRITERIA.md`). Even with H1 data, all three first-screen runs would be kill-dirty, so the official state would still fall to `inconclusive_external_first` or procedural inconclusive—not a formal A/B/C winner.

**Conclusion:** H1 would provide completeness of the designed matrix, but not meaningful *decision-changing* attribution value given observed H2 results.

---

### Question 2: Has H2 already supplied enough evidence to make H1 unnecessary?

**Yes, for practical attribution and next-step guidance. No, for formal threshold completeness.**

**Why H2 is sufficient for the actionable question:**

- H2 is the commitment probe (Hypothesis B). It produced exactly the metric-family movement Phase H predicted for commitment dominance: large no-anchor lift, tool-holdout lift off zero, sharp tool-name/argument gains, and direct-answer substitution reduction (9 non-exact rows vs H0's 18).
- H0's failure profile was commitment-shaped (102 near-canonical wrapper/envelope drift, 18 direct-answer substitution, 0% no-anchor exact-valid). H2 targeted that profile and moved it dramatically.
- H1's intervention (tail-tool diversity restoration) addresses a different causal hypothesis. Nothing in H0 or H2 suggests diversity absence—not commitment failure—is the binding constraint on this surface.

**Why H2 alone cannot formally close Hypothesis B:**

- Threshold B.3 requires confirming that H1 does not outperform H2 on tool-holdout by >5 pp. That comparison is undefined without H1.
- The first-screen pair is formally incomplete per `EXPERIMENTAL_MATRIX.md` and `MINI_EXECUTION_PACKAGE.md`.

**Conclusion:** H2 supplies enough *directional* evidence to make H1 unnecessary for choosing the next remediation path. H2 does not supply enough *formal* evidence to declare Hypothesis B under the published thresholds—but that formal gap cannot be closed by a kill-likely H1 run on a surface where two prior runs already tripped kill metrics.

---

### Question 3: Would running H1 materially improve confidence in A / B / C?

| Hypothesis | Confidence improvement from H1 | Rationale |
|---|---|---|
| **A (diversity-dominant)** | **Low** | H2's large commitment lift makes A unlikely. H1 would mainly provide negative confirmation. |
| **B (commitment-dominant)** | **Low–Medium** | Provisional B signal is already strong. H1 failing to match H2 would strengthen B informally, but formal B remains blocked by kill metrics on all runs. |
| **C (combined)** | **Low** | H3 was never authorized and would not be authorized by an H1 exception. H1 cannot discriminate schema dominance. |

H1 could marginally help distinguish **B vs E** (combined) if H1 showed nonzero gains on a *different* metric family than H2. Given H2's breadth of gains across tool-holdout, no-anchor, and accuracy metrics, a combined determination would require H1 to win clearly on at least one primary family—which, per intervention design, is improbable.

**Conclusion:** H1 would not materially improve confidence on any formal winner. At best it would add low-cost negative evidence against A.

---

### Question 4: Scientific value of H1 today vs alternatives

| Option | Scientific value | Actionability |
|---|---|---|
| **H1 diagnostic run** | Low–Medium: completes matrix; mostly negative A confirmation; kill-likely | Does not advance promotion or external handoff |
| **One additional training run (external-first remediation)** | **High**: targets known safety regression while preserving H2 commitment gains | Directly actionable per `PHASE_I_FINAL_COMPLETION_REPORT.md` recommendation |
| **One additional canonical eval** | Low for attribution: re-baselines without new intervention signal | Useful for monitoring, not for A/B discrimination |

H1 costs ~170s training + ~35s eval—trivial in compute—but the governance and anti-loop cost of overriding a correctly-applied stop ceiling is not trivial. The scientific return per unit of authorized internal iteration is lower than external-first remediation.

---

## Governance Assessment

### Applicable rules (assumed correctly applied)

1. **Kill metrics** (`SUCCESS_AND_FAILURE_CRITERIA.md`): H0 and H2 tripped; both documented as report-only.
2. **Run-level stop ceiling** (`STOP_RULES_AND_DECISION_GATES.md` L39): "do not continue to another internal-only run if two runs have already tripped kill metrics."
3. **Mini stop condition** (`MINI_EXECUTION_PACKAGE.md`): "two runs trip kill metrics" is an explicit termination trigger.
4. **Phase I closure** (`PHASE_I_FINAL_COMPLETION_REPORT.md`): formal attribution `inconclusive_external_first`; no additional internal-only runs without new governance route.

### Exception request in context

A prior continuation determination (`PHASE_H_GATE_REVIEW_AND_PHASE_I_CONTINUATION_DETERMINATION.md`) authorized H2 and H1 together as diagnostic probes *before* H2 executed and tripped the second kill. That authorization did not preempt the run-level ceiling; the ceiling correctly activated after H2's kill trip. The exception now requested is not completion of an open authorization window—it is override of a correctly-applied stop rule after formal Phase I closure.

### Governance test

Under the narrow question—*does remaining attribution value justify a single diagnostic-only exception?*—the burden is on the requester to show that:

1. The exception recovers decision-critical evidence not available from H0+H2.
2. The exception does not reopen internal-only iteration or weaken anti-loop discipline.
3. The exception changes the recommended next action or formal attribution state.

**H1 fails all three tests:**

1. H0+H2 already discriminate commitment as the dominant internal lever on this surface.
2. Granting a third run after two kills directly contradicts the run-level ceiling's purpose ("avoid turning internal experimentation into open-ended tradeoff chasing," `STOP_RULES_AND_DECISION_GATES.md`).
3. Official attribution would remain `inconclusive_external_first`; next action remains external-first remediation regardless of H1 outcome in the plausible range.

### Options evaluated

| Option | Assessment |
|---|---|
| **A — No exception** | **Selected.** Preserves stop-ceiling integrity; H2 signal is sufficient for next-step guidance. |
| **B — One-time H1 diagnostic exception** | Rejected. Marginal attribution gain does not outweigh anti-loop governance cost. |
| **C — Reopen Phase I generally** | Rejected. Out of scope; would violate closure and invite scope expansion. |

---

## Risk Assessment

### Risks of granting the exception

| Risk | Severity |
|---|---|
| Precedent for overriding correctly-applied stop ceilings | **High** |
| Third kill trip reinforcing safety-regression pattern | **Medium–High** |
| Delaying external-first remediation | **Medium** |
| "Completeness chasing" without decision change | **Medium** |
| Post-hoc reinterpretation pressure if H1 shows any lift | **Medium** |

### Risks of denying the exception

| Risk | Severity |
|---|---|
| First-screen pair remains formally incomplete | **Low** (acknowledged in closure docs) |
| Hypothesis B threshold B.3 never formally verified | **Low** (formal B blocked by kill metrics regardless) |
| Uncertainty whether diversity could match commitment on tool-holdout | **Low–Medium** (H2's magnitude makes this unlikely) |

**Net risk posture:** Denying the exception is lower risk. The documented provisional commitment signal and external-first recommendation do not depend on H1.

---

## Determination

### Required answers

| Question | Answer |
|---|---|
| Q1: Meaningful H1 attribution value? | Partial only; not decision-changing |
| Q2: H2 sufficient to make H1 unnecessary? | Yes for practical guidance; no for formal threshold B.3 |
| Q3: Materially improve A/B/C confidence? | No |
| Q4: Scientific value vs alternatives? | Lower than external-first training run |
| Q5: Exception choice? | **A — No exception** |

### Final determination

**Do not grant H1 exception.**

Phase I remains closed with attribution `inconclusive_external_first`. The stop ceiling was correctly applied. `H2_commitment_patch` already provides the dominant actionable signal: commitment intervention produces large tool-side gains on this surface but at unacceptable safety cost. The next authorized workstream is external-first remediation—not a third internal-only diagnostic run on the same kill-sensitive surface.

---

## Confidence Level

**Medium (≈70%)**

**High confidence on:**

- H0 and H2 metric values and kill-metric status (canonical eval artifacts, checkpoint reports)
- Run-level stop ceiling was correctly applied (STOP_RULES, FINAL_COMPLETION_REPORT)
- H2's commitment-dominant signal magnitude (tool-holdout +0.525, no-anchor +0.844)
- H1 exception would not convert official attribution to formal B under published rules

**Moderate uncertainty on:**

- Exact H1 quantitative outcome (counterfactual; never run)
- Whether H1 could achieve a better safety profile than H2 (possible but insufficient to change governance outcome)

**Lower confidence on:**

- Whether stakeholders would accept provisional B without H1 formal comparison (organizational, not evidentiary)

---

## Direct Answer

```
Do not grant H1 exception
```

Phase I remains closed. Proceed to external-first work preserving commitment gains and eliminating safety regression, per `PHASE_I_FINAL_COMPLETION_REPORT.md`.