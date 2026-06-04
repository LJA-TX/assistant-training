# Stage C Package 2B Detector Impact Review

## Scope

This review inventories every active detector path that consumes or resolves the compatibility-bearing surface:

- `read_file_exact_valid_rate`

The scope is assessment only.

No detector migration is performed.

## Conformance Targets

This review checks:

1. active detector path inventory is complete;
2. metric-resolution path is traced from threshold profile to detector outputs;
3. downstream detector decision path is explicit;
4. current source authority is identified;
5. current Stage C wiring status is identified without projecting migration behavior.

## Findings

### 1. Active Detector Resolution Path

The active detector remains the legacy path-based detector in `scripts/post_eval_collapse_detector.py`.

Active resolution chain:

1. `manifests/reports/stage_b_v1_threshold_profile.json`
   - metric catalog entry:
     - `metric_id`: `read_file_exact_valid_rate`
     - `path`: `failure_profile.read_file_exact_valid.rate`
2. `scripts/post_eval_collapse_detector.py::_build_metric_dependency_maps`
   - collects the metric dependency because both active rules for this surface reference `read_file_exact_valid_rate`
3. `scripts/post_eval_collapse_detector.py::_resolve_required_metrics`
   - requests the metric from the threshold profile catalog for current-run rule evaluation
4. `scripts/post_eval_collapse_detector.py::_resolve_metric_from_catalog`
   - resolves `failure_profile.read_file_exact_valid.rate` from `summary.json`
5. `scripts/post_eval_collapse_detector.py::_evaluate_rules`
   - evaluates catastrophic and watch rules using the resolved numeric value
6. `scripts/post_eval_collapse_detector.py::_decide_status`
   - folds rule outcomes into detector status according to threshold-profile precedence
7. `scripts/post_eval_collapse_detector.py::_run_detector`
   - emits:
     - `collapse_watch_interpretation.json`
     - `gate_assessment.json`

### 2. Detector Consumer Table

| Consumer Location | Function / Surface | Metric Resolution Path | Downstream Decision Path | Current Source | Stage C Authoritative Source Wired In? |
|---|---|---|---|---|---|
| `scripts/post_eval_collapse_detector.py` | `_resolve_metric_from_catalog` | `metric_catalog.read_file_exact_valid_rate -> failure_profile.read_file_exact_valid.rate` | feeds resolved current metric into rule evaluation | legacy-only `summary.json` | No |
| `scripts/post_eval_collapse_detector.py` | `_resolve_required_metrics` | requests `read_file_exact_valid_rate` because active rules depend on it | unresolved metric becomes detector noncomputable input; resolved metric becomes rule input | legacy-only `summary.json` | No |
| `scripts/post_eval_collapse_detector.py` | `_run_detector` | consumes resolved current metric set | evaluates catastrophic + watch rule groups, then emits detector `status`, `progression_allowed`, `halt_recommended` | legacy-only `summary.json` | No |
| `scripts/post_eval_collapse_detector.py` | `collapse_watch.rule_evaluation` and `gate.active_rule_ids` outputs | inherits rule results for `read_file_exact_valid_rate` | persistent detector-facing governance output consumed by run artifacts | legacy-only `summary.json` | No |
| `scripts/stage_c8_non_authoritative_detector_projection_adapter.py` | `_build_metric_records`, `_build_projected_eval_summary`, `_run_detector` call | computes a projected `failure_profile.read_file_exact_valid.rate` from Stage C aggregation evidence and replays detector non-authoritatively | compatibility-only adapter evidence | non-authoritative Stage C adapter path only | Not active; non-authoritative only |

### 3. Downstream Detector Decision Path

For this surface, the detector path is:

1. resolve current metric value from `summary.json`;
2. compare against catastrophic rule `read_file_exact_valid_rate_lt_0_40`;
3. compare against watch rule `read_file_exact_valid_rate_lt_0_70`;
4. apply profile precedence:
   - `catastrophic_halt`
   - `halt_progression`
   - `watch`
   - `pass`
5. emit detector-facing decisions:
   - `collapse_watch.status`
   - `gate.status`
   - `gate.progression_allowed`
   - `gate.halt_recommended`
   - triggered rule IDs in both artifacts

This is a direct legacy detector dependency, not a passive observability surface.

### 4. Current Source Authority

Current active detector source:

1. legacy evaluator `failure_profile.read_file_exact_valid.rate` from `summary.json`

Current passive authoritative Stage C source:

1. Package 1C consumes:
   - `stage_c_row_fact_metadata_artifact.json`
   - `stage_c_family_a_scorer_evidence_artifact.json`
2. Package 1D consumes Package 1C output for readiness classification

The active detector does not currently read:

1. Stage C row-fact artifacts;
2. Stage C Family A scorer evidence artifacts;
3. Package 1C reconciliation artifacts;
4. Package 1D readiness artifacts.

### 5. Detector-Impact Determination

Detector impact for `read_file_exact_valid_rate` is narrow but real:

1. the active detector expects a numeric legacy path at `failure_profile.read_file_exact_valid.rate`;
2. the active rule engine treats this surface as both catastrophic and watch bearing;
3. the active detector has no authoritative Stage C input path for this surface;
4. the only Stage C-to-detector mapping currently implemented is explicitly non-authoritative in Package C8.

## Validation Results

Validation evidence used:

1. `scripts/post_eval_collapse_detector.py`
2. `manifests/reports/stage_b_v1_threshold_profile.json`
3. `scripts/stage_c8_non_authoritative_detector_projection_adapter.py`
4. Package 2A gate-evidence bundle dependency inventory

No code execution was required in Package 2B because the relevant runtime behavior was already captured in Package 2A full-run evidence.

## Governance Concerns

1. The active detector still binds directly to a legacy `failure_profile` path, not to declared Stage C family artifacts.
2. The detector assumes metric-path continuity rather than authoritative artifact-class continuity.
3. Because the current live path is legacy-only, any eventual migration would affect a rule-bearing detector input, not merely an informational metric.

## Residual Ambiguities

1. Package 2B does not define rollback procedure; it only confirms that detector impact is explicit and bounded enough to review.
2. Package 2B does not authorize whether an eventual migrated detector should consume Package 1C-style reconciliation output, Package C8-style adapter output, or a later authoritative detector input envelope.

## Determination

The detector-impact review requirement from Package 1E is satisfied for `read_file_exact_valid_rate`.

Basis:

1. every active detector resolution point for the metric is inventoried;
2. the downstream decision path is explicit;
3. the live source is confirmed legacy-only;
4. the existing Stage C authoritative source is confirmed passive-only and not currently wired into detector authority.

## Boundary Confirmation

This review does not:

1. modify `scripts/post_eval_collapse_detector.py`;
2. modify the threshold profile;
3. introduce detector projection;
4. enable detector migration;
5. authorize cutover.
