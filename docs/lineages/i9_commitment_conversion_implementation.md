# Stage B i9 Commitment-Conversion Implementation

## Objective
Implement a bounded i9 dataset intervention to repair canonical commitment behavior under uncertainty while preserving i8 governance invariants.

Primary family:
- `near_miss_wrapper_envelope_repair_pairs`

Secondary family:
- `semantic_substitution_conversion_pairs`

Optional tertiary family:
- `uncertainty_conditioned_canonical_fallback`

## Scope Boundaries
- Localized to `rg_search` and `read_file`.
- No global coercive rewrites.
- No negation-heavy policing.
- No blacklist flooding.
- No semantic flattening monoculture.
- No canonical eval semantic drift.

## Implementation Artifacts
- Builder: `scripts/build_stage_b_recovery_i9_dataset.py`
- Diagnostics: `scripts/i9_diagnostics_scaffold.py`
- Family telemetry: `scripts/build_stage_b_v1_i9_family_concentration_review.py`
- Preflight: `scripts/validate_stage_b_recovery_i9_preflight.py`
- Declaration: `manifests/reports/stage_b_v1_i9_intervention_declaration.json`
- Readiness criteria: `manifests/reports/stage_b_v1_i9_training_eval_readiness_criteria.json`
- Risk assessment: `manifests/reports/stage_b_v1_i9_expected_risk_assessment.json`

## Builder Behavior
- Starts from i8 post-remediation train/val.
- Derives intervention candidates from i8 failure-signature skeletons.
- Applies deterministic family quotas with diversity caps.
- Appends conversion rows only; base rows remain unchanged.
- Enforces ambiguity hard blocks and contamination overlap blocks fail-fast.

## i9 Telemetry Additions
- Exact-valid by conversion source family (baseline proxy + post-eval placeholder).
- Wrapper/envelope repair success-rate hook.
- Semantic-substitution conversion success-rate hook.
- Anchor-dominance ratio and anchor-bucket distribution.
- Paraphrastic canonical success baseline distribution.
- Top-1 behavioral source share and monoculture detection.
- Canonical commitment diversity metrics.
- Near-canonical-to-exact baseline ratio.
- Scalar-substitution rebound detection hook.
- Collapse-watch conditions artifact.

## Governance State
All approval booleans remain false in implementation artifacts.
No training, eval rerun, or promotion action is performed in this phase.
