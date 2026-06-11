# Success And Failure Criteria

## Purpose

These criteria are not promotion rules for the model.

They are decision rules for determining which bottleneck is dominant after the Phase I proving experiment runs.

## Primary Metrics

Evaluate each treatment against `H0_control_i3_micro` using:

1. tool-expected exact JSON validity
2. tool-holdout exact JSON validity
3. tool-name accuracy
4. argument accuracy
5. tool-expected invalid JSON rate

These are the main attribution metrics because they map directly onto the competing hypotheses.

## Secondary Metrics

Use these to refine interpretation:

1. heldout exact JSON validity
2. no-anchor exact-valid share
3. read_file exact-valid rate
4. read_file symbol-name exact-valid rate
5. aggregate exact JSON validity

## Diagnostic Metrics

These identify *why* a run moved:

1. direct-answer substitution share
2. scalar substitution share
3. invalid-schema share
4. `missing_tool_calls` share
5. `payload_not_object` share
6. `payload_not_parsed` share
7. no-call correctness on `no_call`
8. no-call correctness on `adversarial`

## Kill Metrics

These are hard stop metrics for continuation and interpretation:

1. any heldout or tool-holdout contamination overlap greater than zero
2. wrapper leakage greater than zero
3. `no_call` or `adversarial` correctness below `1.0`
4. aggregate no-call correctness below `0.95`
5. aggregate invalid JSON greater than `0.30`
6. any drift in canonical eval manifest, decode defaults, or scoring semantics

Runs that trip kill metrics may still be documented as evidence, but they do not authorize continued internal-only iteration.

## Promotion Metrics

Promotion remains governed by Appendix A, not by Phase H.

Unexpectedly strong runs must still be judged against:

- exact JSON validity improvement requirements,
- tool-name accuracy improvement requirements,
- wrapper leakage constraints,
- no-call regression constraints.

Even if a Phase I run clears Appendix A thresholds, it should still be treated as experiment evidence first and escalated for explicit review before any broader advancement.

## Hypothesis Decision Thresholds

### Hypothesis A: diversity-dominant

Favor `A` if all are true:

1. `H1_diversity_patch` beats `H0` by at least `+5` percentage points on tool-holdout exact-valid or tool-name accuracy.
2. `H1` outperforms `H2` by at least `+5` points on tool-holdout exact-valid.
3. `H2` does not produce a clearly larger reduction in commitment-failure share.

### Hypothesis B: commitment-dominant

Favor `B` if all are true:

1. `H2_commitment_patch` reduces direct-answer plus scalar substitution share by at least `15` points versus `H0`.
2. `H2` improves no-anchor exact-valid share by at least `10` points versus `H0`.
3. `H1` does not outperform `H2` on tool-holdout exact-valid by more than `5` points.
4. `H3` is either unnecessary or fails to add a larger schema-specific gain.

### Hypothesis C: schema-dominant

Favor `C` if all are true:

1. `H3_schema_patch` reduces invalid-schema share by at least `15` points versus `H0`.
2. `H3` reduces `missing_tool_calls` plus `payload_not_object` by at least `20` points versus `H0`.
3. `H3` changes direct-answer plus scalar substitution share by no more than `5` points versus `H2`.

### Hypothesis D: methodology-dominant

Favor `D` if all are true:

1. `H4_methodology_only` improves a primary metric by at least `10` points versus `H0`.
2. `H4` is within `5` points of, or better than, the best content probe on tool-expected exact-valid.
3. The gain occurs with exact control dataset bytes.

### Hypothesis E: combined

Favor `E` if:

1. more than one treatment wins a different metric family,
2. no single probe dominates cleanly,
3. or the best explanatory pattern requires both content and methodology movement.

## Success Definition For The Experiment

The experiment is successful if it produces one of these outcomes:

1. a single leading hypothesis under the thresholds above, or
2. a clear combined-bottleneck determination under `E`, or
3. a justified stop into external-first work because internal-only probes failed to generate informative lift.

## Failure Definition For The Experiment

The experiment fails if:

1. the control run is not trustworthy,
2. kill metrics are triggered across most runs,
3. all treatments remain within the inconclusive band,
4. or the results can only be made interpretable by changing the thresholds after the fact.

## Inconclusive Band

Treat results as inconclusive when:

- all treatment deltas on primary metrics are within `+/-5` percentage points of one another,
- and no treatment cleanly wins its targeted diagnostic metric family,
- and no run produces nonzero tool-holdout exact-valid where the control had none.

Inconclusive results end internal-only iteration unless a predeclared conditional follow-up run remains available inside the Phase H matrix.

## Sources Used

- `docs/appendix_a_operational_execution_contract_v3a.md`
- `docs/phase_g/FAILURE_ATTRIBUTION_ANALYSIS.md`
- `docs/phase_g/COUNTERFACTUAL_ASSESSMENT.md`
- `manifests/reports/stage_b_v1_geometry_risk_assessment.json`
- `manifests/reports/stage_b_v1_i10r_microprobe_canonical_eval_summary.json`
- `manifests/reports/stage_b_v1_i10r_counterbalanced_probe_canonical_eval_summary.json`
- `manifests/reports/stage_b_v1_i10r_nocall_probe_canonical_eval_summary.json`
