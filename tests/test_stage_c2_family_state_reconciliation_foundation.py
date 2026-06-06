import importlib.util
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from repo_paths import resolve_script_path


SCRIPT_PATH = resolve_script_path("stage_c2_family_state_reconciliation_foundation")


def _load_module():
    spec = importlib.util.spec_from_file_location("stage_c2_family_state_reconciliation_foundation", str(SCRIPT_PATH))
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _row_payload(row_id: str, **overrides):
    payload = {
        "family_id": "family_b1",
        "concept_id": "family_b1_symbol_name",
        "row_id": row_id,
        "split_id": "train",
        "sub_slice_id": "symbol-name",
        "eligible": True,
        "counted": False,
        "excluded": False,
        "provenance_ref": "dataset:2026-05-31",
        "evidence_ref": f"evidence:{row_id}",
    }
    payload.update(overrides)
    return payload


def test_aggregate_family_rows_emits_family_subslice_and_split_summaries():
    mod = _load_module()
    rows = [
        mod.build_aggregation_row(_row_payload("r1", counted=True)),
        mod.build_aggregation_row(_row_payload("r2", counted=False, split_id="val")),
        mod.build_aggregation_row(_row_payload("r3", excluded=True, eligible=False, counted=False, split_id="val", sub_slice_id=None)),
    ]

    report = mod.aggregate_family_rows("family_b1", rows)
    assert report.total_rows == 3

    concept = report.concept_summaries[0]
    assert concept.concept_id == "family_b1_symbol_name"
    assert concept.numerator == 1
    assert concept.denominator == 2
    assert concept.excluded_count == 1
    assert concept.rate == 0.5

    subslice = report.sub_slice_summaries[0]
    assert subslice.sub_slice_id == "symbol-name"
    assert subslice.numerator == 1
    assert subslice.denominator == 2

    split_map = {(x.split_id, x.concept_id): x for x in report.split_summaries}
    assert split_map[("train", "family_b1_symbol_name")].numerator == 1
    assert split_map[("val", "family_b1_symbol_name")].denominator == 1


def test_aggregate_family_rows_rejects_mixed_family_rows():
    mod = _load_module()
    rows = [
        mod.build_aggregation_row(_row_payload("r1", family_id="family_a", concept_id="family_a_non_exact")),
        mod.build_aggregation_row(_row_payload("r2", family_id="family_b1")),
    ]

    try:
        mod.aggregate_family_rows("family_a", rows)
        raise AssertionError("expected ContractViolation")
    except mod.ContractViolation as exc:
        assert "aggregation row family mismatch" in str(exc)


def test_build_aggregation_row_rejects_counted_when_not_eligible_or_excluded():
    mod = _load_module()

    try:
        mod.build_aggregation_row(_row_payload("r1", counted=True, eligible=False))
        raise AssertionError("expected ContractViolation")
    except mod.ContractViolation as exc:
        assert "counted=True requires eligible=True" in str(exc)

    try:
        mod.build_aggregation_row(_row_payload("r2", counted=True, excluded=True))
        raise AssertionError("expected ContractViolation")
    except mod.ContractViolation as exc:
        assert "counted=True is invalid when excluded=True" in str(exc)


def test_state_engine_preserves_axis_independence_partial_but_computable():
    mod = _load_module()

    state = mod.evaluate_concept_state(
        mod.StateEvaluationInput(
            concept_id="x_cmp_concept",
            required_evidence_fields=("marker_a", "marker_b"),
            present_evidence_fields=("marker_a",),
            explicit_noncomputability_reasons=tuple(),
            declared_comparability=mod.ComparabilityState.BRIDGE_REQUIRED,
            comparison_block_reasons=("bridge artifact required",),
        )
    )

    assert state.completeness == mod.CompletenessState.PARTIAL
    assert state.current_run_computability == mod.CurrentRunComputabilityState.NONCOMPUTABLE
    assert state.comparability == mod.ComparabilityState.BRIDGE_REQUIRED
    assert "missing required evidence field: marker_b" in state.noncomputability_reasons


def test_state_engine_requires_explicit_comparison_block_reasons_for_non_allowed_states():
    mod = _load_module()

    try:
        mod.evaluate_concept_state(
            mod.StateEvaluationInput(
                concept_id="x_cmp_concept",
                required_evidence_fields=("marker_a",),
                present_evidence_fields=("marker_a",),
                explicit_noncomputability_reasons=tuple(),
                declared_comparability=mod.ComparabilityState.BLOCKED,
                comparison_block_reasons=tuple(),
            )
        )
        raise AssertionError("expected ContractViolation")
    except mod.ContractViolation as exc:
        assert "comparison_block_reasons must be populated" in str(exc)


def test_state_engine_rejects_inference_flags():
    mod = _load_module()

    try:
        mod.evaluate_concept_state(
            mod.StateEvaluationInput(
                concept_id="family_a_non_exact",
                required_evidence_fields=("field",),
                present_evidence_fields=("field",),
                explicit_noncomputability_reasons=tuple(),
                declared_comparability=mod.ComparabilityState.ALLOWED,
                comparison_block_reasons=tuple(),
                inference_used=True,
            )
        )
        raise AssertionError("expected ContractViolation")
    except mod.ContractViolation as exc:
        assert "inference/substitution/reconstruction flags must not be enabled" in str(exc)


def test_denominator_partition_validation_pass_and_fail():
    mod = _load_module()

    passed = mod.validate_denominator_partition(
        {
            "check_id": "partition_pass",
            "parent_denominator": 10,
            "partition_denominators": [7, 3],
            "partition_labels": ["a", "b"],
        }
    )
    assert passed.result == mod.ReconciliationStatus.PASS

    failed = mod.validate_denominator_partition(
        {
            "check_id": "partition_fail",
            "parent_denominator": 10,
            "partition_denominators": [7, 2],
            "partition_labels": ["a", "b"],
        }
    )
    assert failed.result == mod.ReconciliationStatus.FAIL
    assert "mismatch" in failed.reasons[0]


def test_parent_subslice_and_split_to_aggregate_validation():
    mod = _load_module()

    parent_subslice = mod.validate_parent_subslice_boundary(
        {
            "check_id": "parent_subslice",
            "parent_numerator": 4,
            "parent_denominator": 10,
            "subslice_numerators": [2, 1],
            "subslice_denominators": [5, 3],
            "subslice_labels": ["s1", "s2"],
        }
    )
    assert parent_subslice.result == mod.ReconciliationStatus.PASS

    split_reconcile = mod.validate_split_to_aggregate(
        {
            "check_id": "split_reconcile",
            "aggregate_numerator": 5,
            "aggregate_denominator": 12,
            "split_numerators": [2, 3],
            "split_denominators": [7, 5],
            "split_labels": ["train", "val"],
        }
    )
    assert split_reconcile.result == mod.ReconciliationStatus.PASS


def test_coverage_arithmetic_blocked_and_report_counts():
    mod = _load_module()

    blocked = mod.validate_coverage_arithmetic(
        {
            "check_id": "coverage_blocked",
            "covered_count": 0,
            "uncovered_count": 0,
            "total_count": 0,
            "blocked_reasons": ["missing denominator provenance"],
        }
    )
    failed = mod.validate_coverage_arithmetic(
        {
            "check_id": "coverage_fail",
            "covered_count": 2,
            "uncovered_count": 1,
            "total_count": 10,
        }
    )

    report = mod.build_reconciliation_report([blocked, failed])
    assert report.total_checks == 2
    assert report.blocked_count == 1
    assert report.fail_count == 1
    assert report.pass_count == 0


def test_demo_report_executes_with_zero_reconciliation_failures():
    mod = _load_module()

    report = mod.run_stage_c2_foundation_demo()
    assert report.family_aggregation.family_id == "family_a"
    assert report.reconciliation.fail_count == 0
    assert report.reconciliation.pass_count == 4
