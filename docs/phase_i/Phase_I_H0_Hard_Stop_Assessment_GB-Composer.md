Gathering Phase H/I artifacts and the H0 checkpoint evidence to assess the hard-stop decision from first principles.
# Independent Assessment — Phase I H0 Hard Stop

## Executive Summary

Phase I halted after `H0_control_i3_micro` because `adversarial_no_call_correctness = 0.75` tripped a Phase H kill metric requiring exactly `1.0` on both `no_call` and `adversarial` splits. That halt was **procedurally faithful** to predeclared Phase H rules, but **scientifically costly**: it blocked the minimum viable attribution pair (`H2`, `H1`) that the experiment was designed to run.

H0 was not a broken run. Training and eval completed cleanly on frozen surfaces. The adversarial miss is **archetype-specific** (5/20 rows, one prompt family), **reproducible** (identical to `i10r_microprobe`), and **structurally aligned with Hypothesis B** (commitment bleed on malformed requests). The run produced usable primary and diagnostic metrics for tool-expected attribution; it failed a **promotion-grade safety gate**, not a **comparator-validity gate**.

**Primary question:** Yes — Phase H largely optimized for preserving a safety invariant at the expense of learning which bottleneck dominates. The stop rule conflated “do not promote / do not iterate blindly” with “control is unusable for causal comparison,” and that conflation foreclosed the experiment’s main learning value.

---

## A. Stop-Rule Assessment

### Classification: **Defensible But Overly Conservative**

(and, for this experiment’s stated purpose, bordering on **Too Strict**)

### Why

**What the rule does well**

- Predeclared, binary, hard to game post hoc (`SUCCESS_AND_FAILURE_CRITERIA.md`, `STOP_RULES_AND_DECISION_GATES.md`).
- Guards against safety regressions masquerading as tool gains — a real risk noted in Phase H design.
- Aligns with Appendix A’s safety-first posture and prior microprobe rollback doctrine.

**Where it misfires for a causal-attribution experiment**

1. **Wrong gate for the stated objective.** Phase H explicitly frames the work as bottleneck disambiguation, not promotion (`EXPERIMENTAL_OBJECTIVES.md`: “The experiment is not a promotion contest”). Kill metric #3 is a **safety/promotion invariant**, not a **comparator-trust invariant**.

2. **Diagnostic metric elevated to hard invalidation.** Adversarial no-call is listed under *diagnostic* metrics, while attribution decisions are driven by tool-expected exact-valid, tool-holdout, tool-name/argument accuracy, and commitment/schema diagnostics. Tripping adversarial `< 1.0` does not make H0’s primary-metric deltas uninterpretable.

3. **Internal contradiction in Phase H itself.** Kill metrics say tripped runs “may still be documented as evidence” but do not authorize continued iteration (`SUCCESS_AND_FAILURE_CRITERIA.md` L55). The H0 gate then labels the run “not trustworthy” and blocks all downstream runs (`STOP_RULES_AND_DECISION_GATES.md` L43–51). Same run, two incompatible statuses: report-only evidence vs. invalid control.

4. **Asymmetric strictness vs. prior practice.** `i10r_microprobe` had the **same** `adversarial = 0.75` and `aggregate no_call = 0.9167`, triggered hard-stop, and was marked report-only — yet was still cloned as the Phase I training template. H0’s adversarial failure was **predictable**, not a surprise infrastructure failure.

5. **The failure mode is the hypothesis under test.** All 5 adversarial misses are the same case: malformed bracket prompts where the model emits partial `rg_search` tool-call JSON (`invalid_schema` / `missing_tool_calls`) instead of refusing. That is commitment behavior bleeding into adversarial no-call — exactly what `H2_commitment_patch` was built to probe.

6. **Tiered kill metrics were already available but ignored.** Aggregate no-call `< 0.95` (H0: `0.9167`) is a softer guardrail. Per-split `= 1.0` is maximal strictness. Using the stricter rule as a **control invalidation** condition is conservative beyond what attribution requires.

**Verdict:** Appropriate for **promotion iteration control**; **not appropriate as a hard comparator-invalidity condition** for a bounded A/B attribution design where all treatments share the same frozen non-tool slices and eval contract.

---

## B. H0 Evidence Assessment

### Did H0 generate meaningful experimental evidence?

**Yes.** The run was not genuinely invalidated.

### Metric profile (adapter)

| Metric | Value | Notes |
|---|---:|---|
| Exact JSON validity | 4.5% | Nonzero lift vs base (+4.5 pp) |
| Invalid JSON | 14.5% | Large improvement vs base (-55.5 pp) |
| Tool-name accuracy | 7.1% | Primary attribution metric populated |
| Argument accuracy | 6.4% | Primary attribution metric populated |
| Wrapper leakage | 0.0% | Clean |
| `no_call` split correctness | 1.0 | Clean on standard no-call |
| Adversarial correctness | 0.75 | 5/20 failures, single archetype |
| Aggregate no-call | 0.9167 | Driven entirely by adversarial subset |
| Tool-holdout exact-valid | 0.0 | Consistent with Phase G ceiling |

### Forensic characterization of the adversarial miss

- **5 failures**, all: “Search for pattern [a-z without closing bracket…”
- **Mechanism:** model emits `{"function":{"arguments":{"pattern":"[a-z"},"name":"rg_search"},"type":"function"}` — commitment/schema bleed, not successful tool execution or wrapper leakage.
- **15/20 adversarial rows correct** (refusal_expected).
- **`no_call` split perfect** at 1.0.

### Failure profile (tool-expected, diagnostic value)

- 131/140 tool rows non-exact.
- Dominant categories: near-canonical wrapper/envelope drift (102), direct-answer substitution (18).
- Anchor dependence: successes only from literal/paraphrastic anchors; **0% no-anchor exact-valid** — strong Phase G consistency.
- This is exactly the profile Phase H needed to compare against H1/H2.

### What “invalidated” would actually mean — and didn’t happen here

A genuinely invalidated control would show: contract drift, contamination, inconsistent eval, or irreproducible infrastructure failure. None of those occurred. Control surfaces were verified pre-run (`EXECUTION_GATE_APPROVAL.md`). H0 is a **valid within-matrix baseline** with a **known, bounded safety blemish** inherited from the microprobe training surface.

### Important contextual regression

- Phase E i3 revalidation: adversarial `1.0`, aggregate `1.0`.
- H0 (i3 bytes + microprobe config): adversarial `0.75`, aggregate `0.9167`.
- `i10r_microprobe`: adversarial `0.75` (identical to H0).
- `i10r_nocall_probe`: adversarial `1.0` (demonstrates fixability without abandoning the matrix).

So H0 did not “discover” a new failure; it **re-exposed a known microprobe-class adversarial seam** on i3 corpus bytes. That is evidence, not invalidation.

---

## C. Attribution Impact Assessment

### Scientific value lost by not running H2 and H1: **High**

The minimum viable Phase H set was exactly `{H0, H2, H1}`. Stopping at H0 eliminated the entire first-screen attribution mechanism.

| Run | Expected attribution value if run | Value despite H0 adversarial regression |
|---|---|---|
| **H2_commitment_patch** | Direct test of Hypothesis B; targets anchor-light / paraphrastic tool-expected rows; should reduce direct-answer/scalar substitution and no-anchor dependence | **Very high** — adversarial failures are commitment-shaped; H2 is the most informative next probe for that exact failure |
| **H1_diversity_patch** | Direct test of Hypothesis A; restores omitted internal tool families | **High** — diversity vs commitment contrast remains meaningful as relative deltas vs the same H0 baseline |

**Why relative comparison would still work**

- H1 and H2 share H0’s frozen non-tool slices, eval manifest, trainer surface, and patch envelope.
- Attribution thresholds are defined on **deltas vs H0** on primary and targeted diagnostic metrics, not on absolute adversarial perfection.
- Even if all three runs shared `adversarial = 0.75`, **differential movement** on tool-holdout, commitment-failure share, and no-anchor exact-valid would still discriminate A vs B.
- H2 improving adversarial while H1 does not (or vice versa) would itself be decisive evidence.

**What was preserved vs lost**

- Preserved: a documented control baseline, dataset variants, configs, gate artifacts.
- Lost: any empirical basis to choose A/B/C/D/E; forced fallback to `inconclusive_external_first` without running the designed discriminators.

Cost: ~2 training runs (~340s training + ~60s eval), trivial relative to the decision they were meant to inform.

---

## D. Alternative Decision Framework

### Choice: **Continued conditionally**, with **modified gates**

Not “continued fully” without guardrails; not “stopped immediately” as executed.

### Proposed framework

**Tier 1 — Hard stop (comparator invalidity / integrity)**  
Stop if any of:

- heldout/tool-holdout contamination > 0
- wrapper leakage > 0
- eval/scoring/decode contract drift
- training infrastructure failure before metrics exist

**Tier 2 — Attribution continuation gate (after H0)**  
Continue H2/H1 if:

- H0 completes on frozen surfaces
- primary attribution metrics are computable
- kill metrics are **documented** but do not void the control as a delta reference

**Tier 3 — Promotion / external-handoff gate**  
Block promotion and trigger `inconclusive_external_first` only if:

- post-screen treatments remain in the ±5 pp inconclusive band on primary metrics, **or**
- safety regressions **worsen materially vs H0** (e.g., adversarial drops further, wrapper leakage appears), **or**
- two **runs** trip Tier-3 kill metrics (consistent with `STOP_RULES` L39 intent)

**Conditional H0-specific rule I would apply here**

- `adversarial = 0.75` with `no_call = 1.0`, zero leakage, known archetype → **flag, do not halt attribution**
- Proceed to H2 first (per Phase H execution order), because the adversarial miss is commitment-shaped

This preserves Phase H’s anti-loop discipline while separating **“unsafe to promote”** from **“unsafe to compare.”**

---

## E. Recommendation

### **Agree With Caveats**

| Dimension | Position |
|---|---|
| Procedural halt under predeclared Phase H rules | Agree — rules were followed faithfully |
| Scientific appropriateness of the rule for this experiment | Disagree — rule class mismatch |
| Whether H0 should block H2/H1 | Disagree — H0 is usable as a delta baseline |
| Current `inconclusive_external_first` as final attribution state | Agree only as **procedural outcome**, not as **evidence-based attribution conclusion** |

### Recommended Action

1. **Reclassify H0** from “untrustworthy control” to **“valid report-only baseline with documented adversarial seam.”**
2. **Run `H2_commitment_patch` then `H1_diversity_patch`** against existing H0 metrics — do not retrain H0 unless infrastructure changed.
3. **Apply attribution thresholds** on primary/diagnostic deltas; treat adversarial as a **secondary safety monitor**, not a pre-screen veto.
4. **Record promotion ineligibility** for any run with adversarial `< 1.0` until remediated (e.g., nocall-probe-style non-tool rebalance), without conflating that with attribution failure.
5. **Amend Phase H gate taxonomy** for any future proving experiment: separate integrity kills, promotion kills, and attribution continuation rules.

Do **not** reinterpret H0 metrics post hoc to loosen thresholds retroactively; instead, acknowledge the rule was applied correctly but was the wrong class of gate for the experiment’s primary question.

---

## Confidence Level

**Medium–High (≈75%)**

**High confidence on:**

- H0 metric values and adversarial failure forensics (canonical eval artifacts)
- Identity of H0 adversarial pattern with `i10r_microprobe` (0.75, same 5-case archetype)
- Phase H internal contradiction between “report-only evidence” and “untrustworthy control”
- High value of the unrun H2/H1 pair for the stated A vs B question

**Moderate uncertainty on:**

- Whether Phase H authors intentionally accepted total experiment forfeiture vs. comparator continuation as a known tradeoff (not fully documented as such)
- Whether H2 would have improved or worsened adversarial (counterfactual; but that is precisely why the run should have proceeded)

---

## Direct Answer to the Primary Question

> Did Phase H accidentally optimize for preserving a safety invariant at the expense of learning which bottleneck actually exists?

**Yes — substantially.**

The evidence chain:

1. Phase H’s stated objective is causal bottleneck disambiguation, not promotion.
2. The hard stop applied a maximal safety invariant (`adversarial = 1.0`) as a **control-trust veto**.
3. H0’s adversarial failure is a **known, bounded, commitment-shaped** pattern already present in the template run — not a novel integrity breach.
4. The halted treatments (`H2`, `H1`) were the **designed discriminators** for the dominant Phase G residual (commitment + schema).
5. The resulting official state (`inconclusive_external_first`) reflects **procedure**, not **evidence that internal probes cannot discriminate bottlenecks**.

Phase I did not fail as an experiment because H0 broke. It failed to **complete** as an experiment because a promotion-style safety gate was installed at the control checkpoint of an attribution study — and that gate fired on a predictable, diagnostically informative signal instead of the tool-expected metrics the matrix was built to compare.
