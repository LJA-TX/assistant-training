# Stage B First Live Geometry Probe Design

## Scope
Design-only plan for the first Stage B live geometry probe.

Hard constraints:
- No training in this step.
- No eval execution in this step.
- No probe execution in this step.
- No dataset generation or mutation in this step.

## 1. Probe Purpose
### Hypothesis
A single medium-pressure no-call geometry cell with high read_file counterweight can preserve read_file procedural commitment while testing whether no-call correctness can approach or reach the hard ceiling under live instrumentation.

### What Success Means
- Instrumentation is fully auditable in live mode:
  - typed digest lineage complete,
  - declared/realized/drift ledgers emitted,
  - weighted-sampler metadata and sampled stream captured.
- Behavioral outcome remains non-catastrophic:
  - no catastrophic collapse detector trigger,
  - no wrapper leakage,
  - read_file metrics remain above catastrophic floors,
  - no-call signal is directionally improved vs read_file-safe baseline.

### What Failure Means
- Instrumentation failure:
  - missing/misaligned typed digests,
  - missing realized/drift ledgers,
  - sampled stream not capturable when weighted sampling is enabled.
- Behavioral failure:
  - catastrophic collapse trigger,
  - hard-invariant violation,
  - severe declared-vs-realized exposure divergence that prevents attribution.

## 2. Cell Selection (Single Recommended Cell)
Recommended cell: `M_H` (first live probe cell)

Proposed cell identity:
- `sweep_id`: `stage_b_v1_geometry_first_live_probe`
- `cell_id`: `cell_live_mh_nocall_medium_readfile_high_v1`
- `axis_levels`:
  - `no_call_pressure`: `medium`
  - `read_file_counterweight`: `high`
  - `rg_search_contrastive`: `medium` (derived 1:1 with no-call exposure)
  - `uncertainty_conditioning`: `zero`

Justification:
- `no_call_pressure=medium`: enough pressure to test coupling, lower collapse risk than `high` for first live run.
- `read_file_counterweight=high`: protects the dependent variable while no-call pressure is applied.
- `rg_search_contrastive=medium`: maintains valid-tool procedural commitment pressure to avoid blanket refusal generalization.
- `uncertainty_conditioning=zero`: removes a known confound in first live attribution.

## 3. Exposure Plan
### Weighting Strategy
Primary strategy:
- deterministic weighted sampler (`geometry_sampling.enabled=true`),
- replacement sampling,
- explicit sampler seed,
- metadata-driven weights (no row duplication as first choice).

Fallback (only if blocked operationally):
- tightly capped row duplication (`<=2`) with explicit confound labeling.

### Declared Exposure (Design Target)
From Stage B geometry matrix for `M_H`:
- no-call adversarial family exposure units: `13`
- read_file symbol-name exposure units: `10`
- valid rg_search contrastive exposure units: `13`
- uncertainty-conditioning exposure units: `0`

Relative declared shares (over 36 total units):
- no-call: `36.1%`
- read_file symbol-name: `27.8%`
- rg_search contrastive: `36.1%`
- uncertainty: `0%`

### Expected Realized Exposure Range
For sampled stream total `N` in the realized ledger:
- no-call realized share expected: `30%` to `42%` (`0.30N` to `0.42N`)
- read_file symbol-name share expected: `22%` to `33%` (`0.22N` to `0.33N`)
- rg_search contrastive share expected: `30%` to `42%` (`0.30N` to `0.42N`)
- uncertainty-conditioning share expected: `0%`

Declared-vs-realized drift expectation (single-cell acceptance band):
- `max_abs_delta_any_dimension <= 3`: acceptable for first probe.
- `4-6`: watch/escalate.
- `>6`: attribution degraded; halt progression to additional cells.

## 4. Evaluation Plan
### Required Eval Suite
Use the existing canonical Stage B eval topology:
- canonical eval manifest: `/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json`
- required probe slices in summary:
  - no-call adversarial correctness,
  - aggregate no-call correctness,
  - read_file exact-valid,
  - read_file symbol-name exact-valid,
  - invalid_json,
  - wrapper_leakage,
  - direct_answer_substitution count,
  - no_anchor exact-valid share.

### Required Baseline
Primary baseline (single required baseline for detector delta rules):
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_counterbalanced_probe_canonical_eval_summary.json`
- generated: `2026-05-28T16:06:47Z`

Rationale:
- it is the latest read_file-preserving reference point and includes direct-answer substitution count for delta checks.

### Decision Metrics (Monitored for Governance)
- `no_call_correctness_aggregate`
- `no_call_correctness_adversarial`
- `read_file_exact_valid_rate`
- `read_file_symbol_name_exact_valid_rate`
- `invalid_json_overall`
- `wrapper_leakage_overall`
- `direct_answer_substitution_count` (delta vs baseline)
- `no_anchor_exact_valid_share`

### Observational Metrics (Non-gating for first probe)
- `exact_valid_overall`
- `scalar_substitution_share`
- `payload_not_parsed.rate`
- `tool_name_accuracy`
- `argument_accuracy`

## 5. Governance Plan
Threshold profile source:
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_threshold_profile.json`
- profile id: `stage_b_v1_geometry_mapping_collapse_profile`

Policy for first live probe:
- Keep existing hard invariants and catastrophic thresholds unchanged.
- Treat read_file metrics as dependent variables with watch/catastrophic interpretation (not immediate stop unless catastrophic).

Stop conditions:
- any `catastrophic_halt` status,
- any hard invariant violation (`halt_progression`),
- severe drift (`max_abs_delta_any_dimension > 6`),
- missing required typed digest/ledger artifacts.

Escalation conditions:
- detector status `watch`,
- realized drift in warning band (`4-6`),
- direct-answer substitution delta trigger,
- no-call underperformance without catastrophic collapse.

## 6. Interpretation Plan
### Outcomes Justifying `NOT_READY`
- instrumentation artifacts incomplete or non-reconstructable,
- hard invariants violated,
- catastrophic collapse triggered,
- drift too large for defensible attribution.

### Outcomes Justifying `CONTINUE_SINGLE_PROBES`
- instrumentation clean and reconstructable,
- no catastrophic collapse,
- at least one watch-level or attribution concern remains,
- outcome suggests nearby cell probing needed before sweep expansion.

### Outcomes Justifying `ADVANCE_TO_MULTI_CELL_SWEEP`
- instrumentation clean,
- no catastrophic/hard-invariant failure,
- no-call and read_file tradeoff is non-catastrophic and interpretable,
- drift within tolerance (`<=3`),
- clear directional learning signal that motivates 3-5 additional cells.

## Final Recommendation
`READY_TO_EXECUTE_FIRST_PROBE`

Rationale:
- Stage B typed-digest and exposure instrumentation stack is now validated synthetically,
- governance profile is available,
- `M_H` is the lowest-risk informative live geometry cell for first execution.
