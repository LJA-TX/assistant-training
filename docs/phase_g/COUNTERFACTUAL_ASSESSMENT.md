# Counterfactual Assessment

## Primary Answer

If Dataset v1.0 had never collapsed, the project would reasonably be expected to perform materially better than the canonical collapsed v1.0 / Stage B path, but not well enough by collapse repair alone to explain away the full Phase E deficit.

The closest observed internal counterfactual is the i3 recovery corpus:

- it bypassed the v1.0 collapse,
- it restored broad internal surface diversity,
- it reduced invalid JSON sharply,
- and it still produced only `2.5%` exact JSON validity and `3.57%` tool-name / argument accuracy.

That is the strongest evidence that collapse repair is necessary but not sufficient.

## Evidence Base

- `dataset_v1_0_train.jsonl` and `dataset_v1_0_stage_b_train.jsonl` are catastrophically collapsed.
- `dataset_v1_0_stage_b_recovery_i3_train.jsonl` restores `23` tools, `154` prompts, and `74` case ids.
- Phase E i3 still fails `135 / 140` tool-expected rows.
- Those failures are dominated by commitment loss and schema drift, not by a rich set of wrong-tool mistakes.

## Scenario Matrix

| Scenario | What changes | Closest evidence | Expected gain | Uncertainty | Gate outlook |
|---|---|---|---|---|---|
| A. v1.0 collapse fixed only | Preserve v1.0 balance but avoid the one-exemplar collapse | i3 is the nearest observed internal-only repair | Meaningful versus collapsed v1.0; limited versus the full Phase E deficit | Medium | Still unlikely to clear Appendix A minimum-promising gate by itself |
| B. Recovery corpus expanded without external data | Use more internal signal, more balanced internal recovery, and better diversity floors | Phase G inventory plus i3 source-depth limits | Moderate additional gain over i3-style recovery | Medium to high | Could improve heldout behavior, but gate success remains uncertain |
| C. Recovery corpus expanded plus external data | Internal repair plus curated external tool corpora | Phase F external survey and current internal depth limits | Highest expected gain | Medium to high | First scenario with a plausible path to minimum-promising thresholds |
| D. Training methodology unchanged but diversity increased | Keep model, LoRA, and eval contract fixed; only broaden tool-positive data | i3 already approximates this direction | Some gain, but a visible ceiling remains | Medium | Better than collapse, still not enough alone |

## Scenario Notes

### Scenario A: v1.0 collapse fixed only

This is the narrowest counterfactual and the easiest one to overstate.

What the evidence supports:

- training would almost certainly be better than a single repeated `rg_search` exemplar,
- parseability would likely improve,
- exact-valid outputs would likely become nonzero,
- but the result would still be far below the charter's target behavior unless other bottlenecks also improved.

Why: i3 already demonstrates what an internal collapse-repair path looks like under the current training regime, and that result remains weak.

### Scenario B: internal recovery expanded without external data

This is the best pure test of the causal question.

Potential internal gains still available:

- restore upstream tools that never entered the i3 distribution,
- reduce one- and two-example tool families,
- add more internal paraphrase and anchor variation,
- repair diversity floors directly in the build path.

Expected outcome:

- better than i3 on prompt-form generalization,
- probably better than zero on tool-holdout exact-valid rows,
- still constrained by thin native source depth for many tools.

### Scenario C: internal recovery plus external data

This is the highest-upside path because it attacks the weakest part of the current evidence base: low source depth per tool and per argument family.

Why it should help:

- current internal recovery still relies on many one-example tool families,
- holdout-tool exact-valid performance is `0 / 40`,
- Phase F already identified external families targeted at tool-name and argument accuracy rather than only no-call behavior.

This is also the highest-risk path for contamination, schema drift, and license review, so the upside is conditional on disciplined filtering and canonicalization.

### Scenario D: unchanged methodology, diversity increased

This is partly observed already.

What i3 shows:

- diversity alone can reduce invalid JSON and create some exact-valid behavior,
- diversity alone does not remove literal-anchor dependence,
- diversity alone does not solve the commitment-versus-schema problem.

This scenario should therefore be treated as necessary groundwork, not as a full explanation.

## Practical Counterfactual Bound

The strongest evidence-backed bound is:

- lower bound: collapsed v1.0 / Stage B train is structurally unfit and should be expected to perform worse than any repaired internal corpus;
- observed internal-only bound: i3-level behavior shows some real gains but remains far below Appendix A minimum-promising thresholds;
- plausible upper bound without external depth: better than i3, but still uncertain and still exposed to the same commitment / schema ceiling.

## Determination

The Phase G counterfactual answer is:

Dataset v1.0 not collapsing would have helped a lot relative to the broken canonical training path, but it would not reasonably be expected to solve the project on its own.

The most defensible interpretation is:

1. collapse repair explains a meaningful part of the deficit,
2. internal recovery already proves that part,
3. the remaining deficit is caused by other factors that persist even after internal recovery.

## Sources Used

- `data/v1_0/dataset_v1_0_train.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_train.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl`
- `evals/runs/phase_e_i3_revalidation_20260610_r1/summary.json`
- `docs/phase_e/I3_ADAPTER_REVALIDATION_REPORT.md`
- `docs/phase_f/INDEPENDENT_DATASET_COLLAPSE_ASSESSMENT_Grok-Build.md`
- `docs/phase_g/INTERNAL_SIGNAL_INVENTORY.md`
- `docs/phase_g/RECOVERY_CORPUS_ANALYSIS.md`
- `docs/phase_g/FAILURE_ATTRIBUTION_ANALYSIS.md`
