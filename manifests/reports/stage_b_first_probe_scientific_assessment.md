# Stage B First Live Probe Scientific Assessment

## Scope
Read-only post-run assessment of the completed first live Stage B geometry probe:

- training: completed
- canonical eval: completed
- collapse detector: completed after noncomputable-governance repair

No training/eval/detector reruns were performed for this assessment.

## Artifacts Analyzed
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_mh/exposure_ledger_declared.json`
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_mh/exposure_ledger_realized.json`
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_mh/exposure_ledger_drift.json`
- `/opt/ai-stack/assistant-training/artifacts/stage_b_llama31_8b_base_v1_geometry_probe_mh/exposure_row_identity_sidecar.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_weights_sidecar.json`
- `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_geometry_probe_mh_eval/summary.json`
- `/opt/ai-stack/assistant-training/evals/runs/stage_b_v1_geometry_probe_mh_eval/comparison_rows.jsonl`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_counterbalanced_probe_canonical_eval_summary.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_collapse_watch_interpretation.json`
- `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_gate_assessment.json`

## Part A Findings

### 1. Exposure Accounting
- Declared train rows: `1982`
- Realized sampled rows captured: `401`
- Unique sampled train indices: `13`
- Raw declared-vs-realized drift is large (`family total_abs_delta=2357`) because declared covers the full train split while realized captures a weighted sampled subset for a `0.2` epoch run.
- Realized family mix:
  - `malformed_regex_underspecified_search_adversarial_boundary`: `287` (`71.57%`)
  - `read_file_symbol_name_commitment_instability`: `114` (`28.43%`)
- Weighted-plan conformance (normalized): realized closely matches expected counts from sidecar weights:
  - expected malformed family: `289.61` vs realized `287`
  - expected read_file_symbol_name family: `111.39` vs realized `114`

Assessment:
- Exposure execution was deterministic and internally consistent with the weighted sidecar.
- Geometry-axis activation is partial/confounded: no independently labeled `valid_rg_search_contrastive_family` appears in realized family accounting, despite declared units for that axis.

### 2. No-Call Behavior
Live (adapter):
- no_call aggregate correctness: `0.9333`
- no_call adversarial correctness: `1.0000`
- no_call split correctness: `0.8000`

Baseline:
- no_call aggregate correctness: `0.9667`
- no_call adversarial correctness: `1.0000`

Delta (live - baseline):
- aggregate: `-0.0333`
- adversarial: `0.0000`

Assessment:
- Adversarial no-call target held at ceiling.
- Aggregate no-call regressed modestly, driven by non-adversarial no-call split weakness.

### 3. Read-File Behavior
Derived from `comparison_rows.jsonl` (expected tool includes `read_file`):
- read_file exact_valid: `10 / 27 = 0.3704`
- read_file symbol_name exact_valid (case family `p0_read_file_2`): `9 / 13 = 0.6923`

Baseline:
- read_file exact_valid: `0.7037`
- read_file symbol_name exact_valid: `0.9231`

Delta (live - baseline):
- read_file exact_valid: `-0.3333`
- symbol_name exact_valid: `-0.2308`

Additional read_file structure:
- `p0_read_file_2` (symbol name): `9/13`
- `p0_read_file_1` (first function name): `1/7`
- `p0_read_file_3` (contains check): `0/7`

Assessment:
- Read-file performance materially collapsed versus baseline.
- Targeted symbol-name archetype performed better than other read_file archetypes, but still below baseline.

### 4. Wrapper Leakage
- Live aggregate wrapper leakage: `0.015` (`3/200`)
- Baseline wrapper leakage: `0.0`
- Delta: `+0.015`

Assessment:
- Hard-invariant posture not met behaviorally (even though detector could not compute the stale rule directly against live schema).

### 5. Invalid JSON
- Live aggregate invalid_json: `0.23` (`46/200`)
- Baseline invalid_json: `0.14`
- Delta: `+0.09`

Assessment:
- Invalid JSON materially worsened relative to baseline.

### 6. Other Meaningful Observations
- Live aggregate exact_json_validity: `0.21`.
- Tool-expected primary failure classes are dominated by:
  - `invalid_json`: `42`
  - `wrong_tool_name`: `30`
  - `wrong_arguments`: `13`
  - `invalid_schema`: `10`
- Governance remains halted due schema noncomputability, not because of silent pass-through.

## Hypothesis Evaluation (Geometry Coupling)
Evidence supporting coupling:
- Adversarial no-call remains perfect while read_file quality drops strongly, indicating a tradeoff surface rather than uniform movement.
- Symbol-name read_file subset retains partial performance relative to other read_file archetypes, suggesting selective counterweight effects.

Evidence limiting confidence:
- The full intended 4-axis geometry was not cleanly exercised as independently labeled families in realized accounting.
- Detector schema mismatch leaves 8 metrics and 9 rules noncomputable, reducing governance observability.

## Scientific Usefulness
- This cell is scientifically useful as an instrumentation-valid live signal.
- It is not sufficient as a progression gate for multi-cell advancement without schema convergence and cleaner axis disentanglement.

## Repeat Guidance
- Repeat unchanged: `No`.
- Reason: unchanged rerun would likely reproduce the same governance noncomputability and the same axis confound, limiting incremental scientific value.

## Scientific Recommendation
`REPAIR_AND_REEVALUATE`
