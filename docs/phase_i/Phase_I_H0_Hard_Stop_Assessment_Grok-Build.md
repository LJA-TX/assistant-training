**Independent Assessment: Phase I H0 Hard Stop**

**Primary Question Answer**: Yes. Phase H (and its faithful execution under the declared rules in Phase I) optimized for preserving an absolute safety invariant (`no_call`/`adversarial` correctness = 1.0) at the direct expense of generating the comparative data needed to distinguish among the stated bottlenecks (dataset diversity, tool-call commitment, schema realization, training methodology, or combined).

The design and stop rule made attribution impossible once the control reproduced a known regression surface, even though the minimum viable diagnostic set (H0 + H2 + H1) had been prepared and the control run itself produced clean, internally consistent evidence of limited tool learning.

---

### Executive Summary

Phase H designed a bounded causal-attribution experiment (control repro on exact i3 recovery bytes + first-screen commitment and diversity patches + conditional follow-ups) to distinguish A/B/C/D/E hypotheses using predeclared primary, secondary, diagnostic, and kill metrics.

Phase I executed only `H0_control_i3_micro` (exact i3 recovery dataset bytes, frozen microprobe config clone at 0.2 epochs). The run completed successfully with positive but small tool-learning deltas versus base:

- Exact JSON validity: 0.045 (+0.045)
- Invalid JSON: 0.145 (–0.555)
- Tool-name accuracy: ~0.0714 (+0.0714)
- Argument accuracy: ~0.0643 (+0.0643)
- Wrapper leakage: 0.0
- No-call correctness (aggregate): 0.9167 (–0.0833)
- Adversarial no-call correctness: 0.75 (5/20 adversarial cases produced invalid_schema/tool behavior instead of refusal)

Per Phase H rules (SUCCESS_AND_FAILURE_CRITERIA.md), `no_call` or `adversarial` correctness below 1.0 is a hard-stop kill metric. H0 tripped it on adversarial. H2 and H1 (datasets and assets fully prepared and execution-gate approved) were never trained. Attribution was declared `inconclusive_external_first`.

The H0 result was not empirically invalid; it was policy-invalid under the absolute safety gate. The gate, while consistent with prior i10r lineage practice, prevented the comparative measurements the experiment existed to produce.

---

### Stop-Rule Assessment

**Classification: Defensible But Overly Conservative (Too Strict for a causal-attribution experiment).**

**Why**:

- The rule is well-motivated as a *safety and anti-looping* control. Phase H documents (STOP_RULES_AND_DECISION_GATES.md, SUCCESS_AND_FAILURE_CRITERIA.md, PHASE_H_CONTROLLED_EXPERIMENT_DESIGN.md) explicitly cite risks of "safety regressions masquerad[ing] as tool gains," endless internal iteration, and the need for decisive stops. Absolute 1.0 on no_call/adversarial (and wrapper leakage = 0) is a clean, predeclared, non-post-hoc line. It aligns with prior i10r hard-stop evaluations that treated `<1.0` as "halt_progression_report_only."
- It is overly conservative *for the declared purpose* of the experiment. The primary objective (EXPERIMENTAL_OBJECTIVES.md, EXPERIMENTAL_MATRIX.md) was bottleneck *disambiguation* via differential movement on tool-expected/holdout exact-valid, tool-name/arg accuracy, substitution shares, invalid-schema, and no-anchor exact-valid. The kill metrics were intended to bound the experiment, not to make the minimum viable diagnostic set (H0 + H2 + H1) unexecutable when the control reproduces the already-observed regression surface from the i10r microprobe template itself.
- Evidence that the regression is reproducible on the chosen surface: the i10r microprobe (heavily referenced as the template) also produced aggregate no_call_correctness = 0.9167 and triggered "no_call_correctness_lt_1". Later probes (counterbalanced, residual, nocall) showed adversarial varying (1.0 in some pressure conditions, 0.75/0.9/lower in others) and explicitly triggered "no_call_correctness_adversarial_lt_1_0". The i3 recovery data + microprobe recipe is known to be safety-sensitive when adding tool-positive signal. Requiring the H0 control to hit absolute 1.0 on this surface made informative attribution conditional on an outcome that prior work had already shown to be fragile or absent.
- Consequence: the rule functions as a promotion/safety gate overlaid on a diagnostic exercise. When the control itself fails, the experiment yields only the (pre-known) fact that this training recipe on i3 bytes does not preserve the invariant. It yields zero data on whether H1 or H2 patches move capability *and* safety metrics differently.

A defensible alternative would have been relative movement (or a pre-declared "characterization band" based on i10r observation) for diagnosis, with the absolute 1.0 retained strictly for any promotion or external handoff decision.

---

### H0 Evidence Assessment

**H0 generated meaningful experimental evidence. The run was not genuinely invalidated.**

- Execution was clean (160.9s training, 30.5s eval; loss values reported; no wrapper leakage; hashes and surfaces matched the frozen contract per CONTROL_SURFACE_VERIFICATION.md and EXECUTION_GATE_APPROVAL.md).
- Dataset preparation for the control (exact i3 bytes) and the two treatments succeeded with all required constraints (row counts frozen at 2160/240, non-tool slices byte-identical, zero new heldout/tool-holdout contamination — see DATASET_VARIANT_VALIDATION.md and PHASE_I_CODEX_JOURNAL.md).
- The adapter produced a small but real tool-learning signal on the i3 recovery distribution under the budgeted microprobe shape: +4.5pp exact JSON validity, substantial drop in invalid JSON, +7pp tool-name and +6.4pp argument accuracy on the aggregate tool-expected set. Tool-holdout exact-valid remained 0 (as expected for a "control" on recovery data). Failure profile showed heavy "near_canonical_wrapper_or_envelope_drift" + invalid_schema on tool rows and read_file exact-valid = 0.
- The safety regression is real and specific: aggregate no_call 0.9167 (55/60 correct), but all 5 errors were in the adversarial split (15/20 correct = 0.75; the 5 failures were classified invalid_schema, i.e., tool-call emission on refusal-expected adversarial prompts). Base model was 1.0 on no_call/adversarial/direct_answer splits. No_call split and direct_answer split for the adapter remained 1.0.
- This is consistent with (not an anomaly relative to) the i10r microprobe and geometry-probe lineage. It is evidence about the coupling between tool-positive fine-tuning on this data/recipe and over-generalization into adversarial refusal contexts.

The judgment "H0 is not trustworthy" and "control run is not trustworthy under Phase H" (H0_CHECKPOINT_REPORT.md, RUN_COMPARISON_MATRIX.md, BOTTLENECK_ATTRIBUTION_DECISION.md) is a *rule application*, not a finding that the metrics or run are scientifically unusable. The metrics are usable for characterizing what this control produces; they simply do not authorize further internal runs under the declared gates.

---

### Attribution Impact Assessment

**Substantial scientific value was lost by not running H2_commitment_patch and H1_diversity_patch.**

- The minimum viable set was explicitly H0 + H2 + H1 to answer the first causal question: is the next most informative internal move about broader diversity or about tool-call commitment (EXPERIMENTAL_MATRIX.md)?
- Both treatment datasets existed, were validated, and were execution-gate approved alongside H0 (EXECUTION_GATE_APPROVAL.md). They were small (+100 tool-positive rows only), preserved all frozen non-tool slices and total row counts, and introduced no new contamination.
- Even under safety regression, comparative data would have been informative:
  - Relative deltas on primary metrics (tool-expected/holdout exact-valid, tool-name/arg accuracy) vs H0.
  - Shifts in diagnostic profiles (direct-answer + scalar substitution for commitment; tool-holdout lift for diversity; invalid-schema share).
  - Degree and direction of any additional (or reduced) no_call/adversarial regression under each patch type.
  - Whether either patch could move tool-holdout off zero while the control could not.
- Prior i10r work already demonstrated that data interventions (nocall pressure, counterbalancing) *can* move adversarial_no_call (sometimes restoring toward 1.0 at capability cost; sometimes not). Phase I patches were different levers (diversity restoration of omitted families vs paraphrastic commitment on existing intents). Running them would have tested whether those specific levers interact with the safety surface differently from the base i3 control.
- What was learned instead: only that the chosen control surface + i3 bytes reproduces the prior regression. This was already visible in the i10r microprobe report (hard stop on no_call <1) and probe review packages. No new information on A vs B (or C/D/E) was obtained.
- The "inconclusive_external_first" determination is formally correct under the rules but shallow: the experiment was designed to reach even an inconclusive outcome *after* the first screen, not before any comparative data existed.

---

### Recommended Action

**Disagree — Continue H2/H1 (as diagnostic/report-only runs).**

Run the already-prepared first-screen pair (or re-execute them) under explicit "report-only; safety regression documented; not promotion candidates" labeling. Capture the full comparison matrix (tool metrics + safety deltas + failure profiles) versus H0. Then apply (or revise) the decision gates with the actual comparative evidence in hand.

Support:
- The datasets, configs, and manifests for H1/H2 are present and match the Phase H spec.
- The preparation slice (build, validation, gate approval, control execution) succeeded; only the training/eval of the treatments was blocked.
- Continuing internally for these two bounded runs does not violate the spirit of "maximum first-screen treatment runs = 2" once the control data point exists.
- If both also regress on adversarial, the matrix still distinguishes relative leverage and cost (capability gain per unit safety regression). If one regresses less while moving its targeted metric family more, that is directly actionable for bottleneck diagnosis and for any external handoff.
- The alternative (halt and escalate without the comparisons) leaves the core Phase H question (which bottleneck dominates) unanswered by construction.

If governance requires strict adherence to the current kill metric even for pure diagnostics, the honest outcome is "experiment design did not permit attribution on this surface" rather than a clean "inconclusive_external_first" that implies the matrix was attempted.

---

### Confidence Level

**Medium-High** on the assessment of the stop-rule impact and lost attribution value (direct from the Phase H design documents, H0 metrics, prior i10r reports, and Phase I execution artifacts).

**Medium** on the precise quantitative value of the specific H1/H2 patches (they were never run; their effects are inferred from design intent, patch construction details, and analogous prior probe movements on the same safety axis). The directional conclusion (material value was lost; the control regression was predictable from the chosen recipe) is robust.

All primary required artifacts were reviewed (Phase H bundle, Phase I bundle, H0 checkpoint report, RUN_COMPARISON_MATRIX.md, BOTTLENECK_ATTRIBUTION_DECISION.md, PHASE_I_COMPLETION_AND_NEXT_STEP_RECOMMENDATION.md, supporting evals, training summary, dataset validations, and relevant prior lineage reports).

The experiment as executed followed the Phase H rules exactly. The rules themselves, applied to a control that used the known-sensitive i10r microprobe shape on i3 recovery data, precluded the learning the experiment was chartered to produce.
