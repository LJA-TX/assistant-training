# Stage B First Probe Execution Review Checklist

## Scope
Reviewer checklist for authorization decision on:
- `sweep_id`: `stage_b_v1_geometry_first_live_probe`
- `cell_id`: `cell_live_mh_nocall_medium_readfile_high_v1`

## 1. Geometry Identity Verification
- [ ] `geometry_schema_version` present and expected.
- [ ] `sweep_id` and `cell_id` match approved probe design.
- [ ] Axis levels match approved cell:
  - `no_call_pressure=medium`
  - `read_file_counterweight=high`
  - `rg_search_contrastive=medium`
  - `uncertainty_conditioning=zero`
- [ ] `weighting_mode` matches sidecar-overlay probe mode.

## 2. Digest Verification
- [ ] `digest_contract_v1.json` link is present in resolved config.
- [ ] `geometry_mapping_identity_digest` is present and deterministic.
- [ ] `geometry_context_input_digest` is present and deterministic.
- [ ] Legacy alias fields are present and explicitly marked:
  - `geometry_context_digest`
  - `geometry_context_digest_alias_of`
- [ ] No workflow step incorrectly assumes typed digests must be equal.

## 3. Sidecar Weighting Verification
- [ ] `geometry_sampling.enabled=true`.
- [ ] `geometry_sampling.weight_source.kind=sidecar`.
- [ ] Sidecar path is present and intended:
  - `/opt/ai-stack/assistant-training/manifests/reports/stage_b_first_probe_weights_sidecar.json`
- [ ] Sidecar digest binding fields are present and consistent:
  - `geometry_mapping_identity_digest`
  - `geometry_context_input_digest`
  - `row_identity_reference.rows_digest_sha256`
- [ ] Expected sidecar payload digest verified:
  - `0553484014a19d51520321989f81eaedc28e2135756edfd0f7dc516d334446bf`
- [ ] Row identity digest match is expected and verified:
  - `1cb0a23a2038bb949b1e1be90b289eb02f1b05b776a8a2a11af44c961a993549`
- [ ] Positive-weight coverage is sufficient:
  - positive rows `>=13` (current `13`)
  - `weights_sum=36.0`
- [ ] Fail-fast sidecar validation package reviewed and passed:
  - missing-row fail-fast
  - row-hash mismatch fail-fast

## 4. Expected Exposure Verification
- [ ] Declared family exposure units match approved design:
  - no-call adversarial: `13`
  - read_file symbol-name: `10`
  - valid rg_search contrastive: `13`
  - uncertainty: `0`
- [ ] Sidecar family allocation summary matches declared exposure units.
- [ ] Expected realized range bands are documented and acceptable.
- [ ] Drift expectations are documented:
  - acceptable: `<=3`
  - watch: `4..6`
  - halt: `>6`

## 5. Detector Readiness Verification
- [ ] Threshold profile path resolves and profile id matches:
  - `stage_b_v1_geometry_mapping_collapse_profile`
- [ ] Detector input set is complete:
  - eval summary
  - threshold profile
  - baseline summary
  - geometry context (`stage_b_first_probe_geometry_context_input.json`)
- [ ] Detector geometry context input is the compact geometry context object (not full resolved-config JSON).
- [ ] Output paths are predeclared:
  - collapse watch interpretation
  - gate assessment
- [ ] Missing-baseline policy for delta thresholds is understood (`fail_fast`).

## 6. Baseline Verification
- [ ] Baseline summary exists and is the required file:
  - `/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i10r_counterbalanced_probe_canonical_eval_summary.json`
- [ ] Baseline provenance is acceptable for Stage B first live probe.
- [ ] Baseline contains required metric paths for detector rules.

## 7. Authorization Decision
- [ ] All required criteria in `stage_b_first_probe_go_no_go_summary.json` are satisfied.
- [ ] No halt criteria currently active.
- [ ] Escalation handling owner is assigned if watch state occurs.
- [ ] Explicit manual run authorization remains intentionally false until final GO signoff.

Decision:
- [ ] `GO` (authorized to execute)
- [ ] `NO_GO` (blocked pending prerequisites)

Reviewer:
- Name:
- Date (UTC):
- Notes:
