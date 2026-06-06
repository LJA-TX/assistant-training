import importlib.util
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from repo_paths import resolve_fixture_root, resolve_script_path


SCRIPT_PATH = resolve_script_path("stage_c1_evaluator_foundation")


def _load_module():
    spec = importlib.util.spec_from_file_location("stage_c1_evaluator_foundation", str(SCRIPT_PATH))
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _row_fact_payload():
    return {
        "row_id": "row-001",
        "split_id": "train",
        "excluded": False,
        "expected_tool_name": "read_file",
        "membership_markers": {
            "family_a_tool_expected_eligible": True,
            "family_b1_read_file_eligible": True,
            "family_b1_symbol_name_member": True,
            "family_b2_anchor_eligible": True,
            "family_b2_no_anchor_member": False,
            "family_b2_anchor_category": "anchor-positive",
        },
        "ownership_markers": {
            "symbol_name_membership_owner": "dataset_metadata",
            "anchor_assignment_owner": "anchor_assignment_pipeline",
            "anchor_taxonomy_owner": "anchor_taxonomy_registry",
            "conflicting_ownership_markers": False,
            "ownership_conflict_reasons": [],
        },
        "provenance": {
            "row_source": "tooling_eval_rows",
            "dataset_id": "tool_eval_set",
            "dataset_version": "2026-05-31",
            "extraction_timestamp_utc": "2026-05-31T00:00:00Z",
            "evidence_digest": "sha256:abc123",
        },
        "denominator_provenance": {
            "eligible_population_source": "eligible_rows_table",
            "non_exact_population_source": "family_a_non_exact_rows",
            "read_file_population_source": "family_b1_read_file_rows",
            "symbol_name_population_source": "family_b1_symbol_name_rows",
            "anchor_population_source": "family_b2_anchor_rows",
            "no_anchor_population_source": "family_b2_no_anchor_rows",
        },
        "evidence": {
            "raw_record_locator": "s3://bucket/path",
        },
    }


def test_build_row_fact_record_happy_path():
    mod = _load_module()
    rec = mod.build_row_fact_record(_row_fact_payload())

    assert rec.row_id == "row-001"
    assert rec.membership_markers.family_b1_symbol_name_member is True
    assert rec.ownership_markers.symbol_name_membership_owner == "dataset_metadata"
    assert rec.denominator_provenance.eligible_population_source == "eligible_rows_table"
    assert rec.evidence["raw_record_locator"] == "s3://bucket/path"


def test_build_row_fact_record_rejects_missing_ownership_for_symbol_name_member():
    mod = _load_module()
    payload = _row_fact_payload()
    payload["ownership_markers"]["symbol_name_membership_owner"] = None

    try:
        mod.build_row_fact_record(payload)
        raise AssertionError("expected ContractViolation")
    except mod.ContractViolation as exc:
        assert "symbol_name_membership_owner is required" in str(exc)


def test_emit_family_a_scorer_evidence_rejects_other_subtype_and_preserves_missing_evidence():
    mod = _load_module()

    try:
        mod.emit_family_a_scorer_evidence(
            mod.FamilyAScorerEvidenceInput(
                row_id="row-101",
                tool_expected_eligibility=True,
                excluded=False,
                exact_valid=False,
                primary_outcome="non-exact",
                failure_taxonomy_marker="family_a_failure_taxonomy_v1",
                scorer_semantics_marker="scorer_semantics_v1",
                declared_subtype="other",
                missing_evidence_reasons=tuple(),
            )
        )
        raise AssertionError("expected ContractViolation")
    except mod.ContractViolation as exc:
        assert "declared_subtype 'other' is prohibited" in str(exc)

    rec = mod.emit_family_a_scorer_evidence(
        mod.FamilyAScorerEvidenceInput(
            row_id="row-102",
            tool_expected_eligibility=True,
            excluded=False,
            exact_valid=False,
            primary_outcome="non-exact",
            failure_taxonomy_marker="family_a_failure_taxonomy_v1",
            scorer_semantics_marker="scorer_semantics_v1",
            declared_subtype=None,
            missing_evidence_reasons=("missing approved non-exact subtype assignment",),
        )
    )
    assert rec.non_exact_tool_expected is True
    assert rec.subtype_assignment is None
    assert rec.missing_evidence is True
    assert rec.missing_evidence_reasons == ("missing approved non-exact subtype assignment",)


def test_emit_family_a_scorer_evidence_accepts_approved_subtype_only():
    mod = _load_module()

    rec = mod.emit_family_a_scorer_evidence(
        mod.FamilyAScorerEvidenceInput(
            row_id="row-103",
            tool_expected_eligibility=True,
            excluded=False,
            exact_valid=False,
            primary_outcome="non-exact",
            failure_taxonomy_marker="family_a_failure_taxonomy_v1",
            scorer_semantics_marker="scorer_semantics_v1",
            declared_subtype="wrong tool name",
            missing_evidence_reasons=tuple(),
        )
    )
    assert rec.subtype_assignment == "wrong tool name"
    assert rec.missing_evidence is False


def test_fixture_harness_reports_zero_issues_for_authoritative_fixture_corpus():
    mod = _load_module()
    root = resolve_fixture_root()

    report = mod.run_fixture_harness(root)
    assert report.fixture_count == 117
    assert report.issue_count == 0
    assert report.invalid_fixture_count == 0
    assert report.fixture_counts_by_family_group == {
        "common_state": 18,
        "cross_family": 27,
        "family_a": 25,
        "family_b1": 24,
        "family_b2": 23,
    }


def test_fixture_harness_rejects_collapsed_state_and_forbidden_detector_inference(tmp_path):
    mod = _load_module()

    fixture = {
        "fixture_id": "A-C-999",
        "source_definition_id": "SCEN-A-C-999",
        "source_documents": ["test"],
        "classification": {},
        "required_inputs": {},
        "expected_state": {
            "completeness": "complete",
            "current_run_computability": "current-run computable",
            "comparability": "comparison-blocked",
            "noncomputability_reasons": [],
            "state": "collapsed",
        },
        "expected_detector_treatment": {
            "infer_missing_denominator": True,
        },
        "expected_reconciliation_behavior": {},
        "acceptance_criteria": [],
        "rationale": "test",
    }

    path = tmp_path / "bad_fixture.json"
    path.write_text(json.dumps(fixture, indent=2), encoding="utf-8")

    report = mod.run_fixture_harness(tmp_path)
    issue_codes = {issue.issue_code for issue in report.issues}
    assert "collapsed_state_field" in issue_codes
    assert "forbidden_detector_behavior" in issue_codes
    assert report.invalid_fixture_count == 1


def test_fixture_harness_rejects_invalid_axis_values(tmp_path):
    mod = _load_module()

    fixture = {
        "fixture_id": "B2-C-999",
        "source_definition_id": "SCEN-B2-C-999",
        "source_documents": ["test"],
        "classification": {},
        "required_inputs": {},
        "expected_state": {
            "completeness": "unknown",
            "current_run_computability": "unknown",
            "comparability": "unknown",
            "noncomputability_reasons": [],
        },
        "expected_detector_treatment": {},
        "expected_reconciliation_behavior": {},
        "acceptance_criteria": [],
        "rationale": "test",
    }

    path = tmp_path / "bad_axis_fixture.json"
    path.write_text(json.dumps(fixture, indent=2), encoding="utf-8")

    report = mod.run_fixture_harness(tmp_path)
    issue_codes = {issue.issue_code for issue in report.issues}
    assert "invalid_completeness_state" in issue_codes
    assert "invalid_current_run_computability_state" in issue_codes
    assert "invalid_comparability_state" in issue_codes
