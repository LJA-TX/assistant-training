# Stage B Successor Probe Scientific Assessment

## Scope
Post-run assessment of the completed Stage B successor live geometry probe:

- training: completed
- sampler validation: completed
- canonical eval: completed
- collapse detector: completed

No training reruns, eval reruns, detector reruns, dataset changes, or threshold changes were performed for this assessment.

## Artifacts Analyzed
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_lh/training_summary.json`
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_lh/exposure_ledger_realized.json`
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_lh/exposure_ledger_drift.json`
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_lh/sampler_determinism_report.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_successor_probe_weights_sidecar.json`
- `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_geometry_probe_lh_eval/summary.json`
- `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_geometry_probe_lh_eval/comparison_rows.jsonl`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_successor_probe_collapse_watch_interpretation.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_successor_probe_gate_assessment.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_counterbalanced_probe_canonical_eval_summary.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_scientific_assessment.md`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_behavior_interpretation.json`

## Part A Findings

### 1. Sampler Validity vs Behavioral Measurement
- The L/H training run remains sampler-valid.
- The weighted sidecar concentrated exposure on `13` of `1982` train rows with declared units `10/10/10/0`.
- Runtime capture recorded `401` sampled rows and `13` unique sampled indices.
- The previously observed `1881` drift remains a raw-count comparison artifact between full-train declared counts and the weighted sampled subset; it is not evidence of execution failure.

Assessment:
- Sampler validity is not the open question anymore.
- This phase answers behavioral and governance questions only.

### 2. Behavioral Outcomes
#### No-Call Preservation
Live (adapter):
- no_call aggregate correctness: `44 / 60 = 0.7333`
- no_call adversarial correctness: `13 / 20 = 0.6500`
- no_call split correctness: `14 / 20 = 0.7000`
- direct-answer split correctness: `17 / 20 = 0.8500`

Baseline:
- no_call aggregate correctness: `0.9667`
- no_call adversarial correctness: `1.0000`

Prior M/H live probe:
- no_call aggregate correctness: `0.9333`
- no_call adversarial correctness: `1.0000`

Delta (L/H - baseline):
- aggregate: `-0.2333`
- adversarial: `-0.3500`

Delta (L/H - M/H):
- aggregate: `-0.2000`
- adversarial: `-0.3500`

Assessment:
- Lowering no-call pressure from `medium` to `low` did not preserve no-call behavior.
- The successor probe violated both no-call hard invariants.

#### Read-File Preservation
Live (adapter):
- read_file exact_valid: `6 / 27 = 0.2222`
- read_file symbol_name exact_valid: `6 / 13 = 0.4615`

By source case:
- `p0_read_file_1` (first function name): `0 / 7 = 0.0000`
- `p0_read_file_2` (symbol name): `6 / 13 = 0.4615`
- `p0_read_file_3` (boolean presence): `0 / 7 = 0.0000`

Baseline:
- read_file exact_valid: `0.7037`
- read_file symbol_name exact_valid: `0.9231`

Prior M/H live probe:
- read_file exact_valid: `0.3704`
- read_file symbol_name exact_valid: `0.6923`

Delta (L/H - baseline):
- read_file exact_valid: `-0.4815`
- symbol_name exact_valid: `-0.4615`

Delta (L/H - M/H):
- read_file exact_valid: `-0.1481`
- symbol_name exact_valid: `-0.2308`

Assessment:
- The successor probe did not restore read_file preservation.
- Read_file exact-valid behavior worsened materially relative to both baseline and M/H.
- Symbol-name rows stayed above the catastrophic `0.40` floor, but the broader read_file surface collapsed harder than M/H because the other two read_file archetypes dropped to `0 / 14`.

#### Wrapper Leakage
Live (adapter):
- wrapper leakage: `0.0000`

Baseline:
- wrapper leakage: `0.0000`

Prior M/H live probe:
- wrapper leakage: `0.0150`

Assessment:
- Wrapper leakage recovered to the baseline floor.
- This is a genuine positive outcome, but it is not enough to offset the no-call and read_file failures.

#### Invalid JSON and Control Metrics
Live (adapter):
- invalid_json: `0.3600`
- exact_json_validity: `0.1200`
- tool_name_accuracy: `0.3429`
- argument_accuracy: `0.3357`

Baseline:
- invalid_json: `0.1400`
- exact_json_validity: `0.7300`
- tool_name_accuracy: `0.6786`
- argument_accuracy: `0.6571`

Prior M/H live probe:
- invalid_json: `0.2300`
- exact_json_validity: `0.2100`
- tool_name_accuracy: `0.4000`
- argument_accuracy: `0.4857`

Assessment:
- Invalid JSON crossed the catastrophic threshold and worsened relative to both baseline and M/H.
- Scalar-control-adjacent quality indicators also degraded sharply.

#### Restored Gate-Critical Metrics
Live (adapter):
- direct_answer_substitution_count: `9`
- no_anchor_exact_valid_share: `0.7917`
- read_file_exact_valid_rate: `0.2222`
- read_file_symbol_name_exact_valid_rate: `0.4615`

Baseline:
- direct_answer_substitution_count: `11`
- no_anchor_exact_valid_share: `0.8370`

Assessment:
- All previously blocked gate-critical metrics are now computable.
- Direct-answer substitution improved slightly relative to baseline (`-2` cases).
- No-anchor exact-valid share remained above the `0.75` watch threshold.
- Scientific observability is restored, but the measured behavior is still unacceptable.

### 3. Governance Outcome
Detector result:
- status: `catastrophic_halt`
- progression_allowed: `false`
- halt_recommended: `true`
- noncomputable_metric_count: `0`
- noncomputable_rule_count: `0`

Triggered hard invariants:
- `no_call_correctness_aggregate_lt_1_0`
- `no_call_correctness_adversarial_lt_1_0`

Triggered catastrophic thresholds:
- `invalid_json_overall_gte_0_35`
- `read_file_exact_valid_rate_lt_0_40`

Triggered watch threshold:
- `read_file_exact_valid_rate_lt_0_70`

Assessment:
- Governance is no longer blocked by schema noncomputability.
- Governance now rejects the successor probe on substantive behavioral grounds.

## Hypothesis Evaluation
Declared L/H hypothesis:
- lowering no-call pressure from `M/H` to `L/H` would materially restore read_file procedural commitment while preserving adversarial no-call and keeping governance fully computable.

Supported:
- Restored metric surfaces do keep governance fully computable.
- Wrapper leakage can return to zero under this cell.
- Direct-answer substitution did not rebound upward.

Unsupported:
- Lowering no-call pressure restored neither aggregate nor adversarial no-call.
- Lowering no-call pressure did not restore read_file; it worsened both overall read_file exact-valid and read_file symbol-name exact-valid relative to M/H.
- The cell did not reduce overall invalid-json failure pressure.

Unexpected findings:
- The worst regression was on adversarial no-call, not only on the aggregate split.
- Read_file symbol-name stayed above the catastrophic floor while the other read_file archetypes collapsed to zero exact-valid.
- Wrapper leakage improved even as overall correctness and parseability worsened.

## Success Criteria Determination
Result: `failed`

Reasoning:
- The probe fails the declared successor success criteria on the decisive detector condition alone because detector status is `catastrophic_halt`.
- The run also fails the intended behavioral objective: read_file preservation did not improve, and no-call behavior regressed sharply.
- The literal drift clause in the package success criteria remains tripped by the known raw-count comparison artifact, but that is not the reason this probe fails.

## Scientific Recommendation
- Advance to additional geometry cells: `No`
- Advance this L/H adapter to promotion or broader sweep: `No`
- Next geometry cell recommendation: `None warranted from the current line`

Rationale:
- This probe is sampler-valid and scientifically useful as a decisive negative result.
- It is behaviorally unsuccessful and governance-rejected.
- The current evidence is sufficient for a no-go decision; no further geometry-cell recommendation is warranted from this slice.

## Final Determination
`L/H probe failed`

Interpretation:
- sampler validity: `pass`
- behavioral outcome: `fail`
- governance outcome: `fail`

The intended experimental question has been answered. Reducing no-call pressure from `M/H` to `L/H` did not improve read_file preservation without unacceptable regressions elsewhere.
