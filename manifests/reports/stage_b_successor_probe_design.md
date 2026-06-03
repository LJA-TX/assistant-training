# Stage B Successor Live Geometry Probe Design

## Scope
Design-only construction package for the successor Stage B live geometry probe.

Hard constraints:
- No training in this step.
- No eval execution in this step.
- No probe execution in this step.
- No dataset generation or mutation in this step.

## 1. Probe Purpose
### Hypothesis
A low-pressure no-call geometry cell with high read_file counterweight provides the smallest informative follow-up to the completed `M_H` live probe. It should test whether the observed read_file collapse was pressure-threshold driven while minimizing additional training cost.

### What This Probe Must Clarify
- Whether lowering no-call pressure from `medium` to `low` materially restores read_file procedural commitment.
- Whether adversarial no-call correctness can remain at ceiling under the lower-pressure cell.
- Whether restored detector-facing metric surfaces keep governance fully computable for the successor package.

### Why This Is Not A Repeat
- `cell_live_mh_nocall_medium_readfile_high_v1` must not be relaunched unchanged.
- The successor changes the primary pressure axis only:
  - previous: `no_call_pressure=medium`
  - successor: `no_call_pressure=low`
- Read_file counterweight remains `high` to preserve causal readability against the strongest prior failure mode.

## 2. Cell Selection
Recommended successor cell:

- `sweep_id`: `stage_b_v1_geometry_successor_probe`
- `cell_id`: `cell_live_lh_nocall_low_readfile_high_v1`
- `axis_levels`:
  - `no_call_pressure`: `low`
  - `read_file_counterweight`: `high`
  - `rg_search_contrastive`: `low`
  - `uncertainty_conditioning`: `zero`

Justification:
- `low/high` is the missing lower-pressure anchor from the approved bracketed sweep.
- It addresses the highest-value unresolved question without broadening to a multi-cell launch.
- It preserves the counterweight that best protects the dependent variable while testing the no-call threshold edge.

## 3. Exposure Plan
### Weighting Strategy
Primary strategy:
- deterministic weighted sampler (`geometry_sampling.enabled=true`),
- replacement sampling,
- explicit sampler seed,
- sidecar-overlay weight provisioning with `default_weight=0.0`.

### Declared Exposure (Successor Target)
From the approved sweep matrix for `L_H`:
- no-call adversarial family exposure units: `10`
- read_file symbol-name exposure units: `10`
- valid rg_search contrastive exposure units: `10`
- uncertainty-conditioning exposure units: `0`

Relative declared shares (over 30 total units):
- no-call: `33.3%`
- read_file symbol-name: `33.3%`
- rg_search contrastive: `33.3%`
- uncertainty: `0%`

### Expected Realized Exposure Range
For sampled stream total `N` in the realized ledger:
- no-call realized share expected: `27%` to `39%`
- read_file symbol-name share expected: `27%` to `39%`
- rg_search contrastive share expected: `27%` to `39%`
- uncertainty-conditioning share expected: `0%`

Declared-vs-realized drift expectation:
- `max_abs_delta_any_dimension <= 3`: acceptable
- `4-6`: watch/escalate
- `>6`: attribution degraded; halt progression

## 4. Evaluation Plan
### Required Eval Suite
Use the existing canonical Stage B eval topology:
- canonical eval manifest: `/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json`
- restored detector-facing metric surfaces required in raw `summary.json`:
  - `metrics.aggregate.no_call_correctness`
  - `metrics.probes.no_call_adversarial.no_call_correctness`
  - `metrics.aggregate.wrapper_leakage`
  - `metrics.aggregate.invalid_json`
  - `failure_profile.read_file_exact_valid.rate`
  - `failure_profile.read_file_symbol_name_exact_valid.rate`
  - `failure_profile.failure_categories_non_exact_tool_rows.direct_answer_substitution`
  - `failure_profile.anchor_exact_share.no_anchor_phrase`

### Required Baseline
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_counterbalanced_probe_canonical_eval_summary.json`

### Decision Metrics
- `no_call_correctness_aggregate`
- `no_call_correctness_adversarial`
- `read_file_exact_valid_rate`
- `read_file_symbol_name_exact_valid_rate`
- `invalid_json_overall`
- `wrapper_leakage_overall`
- `direct_answer_substitution_count`
- `no_anchor_exact_valid_share`

## 5. Governance Plan
Threshold profile source:
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_threshold_profile.json`
- profile id: `stage_b_v1_geometry_mapping_collapse_profile`

Successor package policy:
- keep hard invariants and catastrophic thresholds unchanged,
- use restored metric surfaces directly with no detector or threshold-profile aliases,
- require explicit human launch authorization before any training command is run.

## Final Recommendation
`CONSTRUCT_SUCCESSOR_PACKAGE_AND_REVIEW_READINESS`

Rationale:
- Metric observability restoration is complete.
- The successor cell changes the minimum necessary axis to answer the next empirical question.
- Package construction should proceed, followed by a bounded launch-readiness review before any execution.
