import importlib.util
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from repo_paths import resolve_fixture_root, resolve_script_path


SCRIPT_PATH = resolve_script_path("stage_c3_evaluator_runtime_integration")
FIXTURES_ROOT = resolve_fixture_root()


def _load_module():
    spec = importlib.util.spec_from_file_location("stage_c3_evaluator_runtime_integration", str(SCRIPT_PATH))
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_stage_c3_runtime_integration_emits_baseline_artifact_bundle(tmp_path):
    mod = _load_module()

    summary = mod.run_stage_c3_runtime_integration(FIXTURES_ROOT, tmp_path)

    assert summary["fixture_count"] == 117
    assert summary["harness_issue_count"] == 0
    assert summary["reconciliation_fail_count"] == 0

    expected_artifacts = {
        "fixture_inventory",
        "row_fact_metadata",
        "state_axis",
        "aggregation_summary",
        "reconciliation_summary",
        "governance_guardrails",
        "validation_issues",
        "runtime_contract_summary",
    }
    assert set(summary["artifact_paths"].keys()) == expected_artifacts

    for artifact_name in expected_artifacts:
        path = Path(summary["artifact_paths"][artifact_name])
        assert path.exists(), artifact_name

    summary_path = Path(summary["summary_path"])
    assert summary_path.exists()


def test_stage_c3_state_axis_artifact_preserves_axes_and_no_collapsed_state(tmp_path):
    mod = _load_module()
    summary = mod.run_stage_c3_runtime_integration(FIXTURES_ROOT, tmp_path)

    state_artifact = _load_json(Path(summary["artifact_paths"]["state_axis"]))
    records = state_artifact["records"]
    assert state_artifact["record_count"] == len(records) == 117

    completeness_values = {record["completeness"] for record in records}
    computability_values = {record["current_run_computability"] for record in records}
    comparability_values = {record["comparability"] for record in records}

    assert completeness_values <= {"complete", "partial", "missing"}
    assert computability_values <= {"current-run computable", "current-run noncomputable"}
    assert comparability_values <= {
        "comparison-allowed",
        "bridge-required",
        "reference-only",
        "comparison-blocked",
    }

    for record in records:
        assert "state" not in record
        assert "combined_state" not in record


def test_stage_c3_row_fact_and_guardrail_artifacts_show_no_inference_flags(tmp_path):
    mod = _load_module()
    summary = mod.run_stage_c3_runtime_integration(FIXTURES_ROOT, tmp_path)

    row_fact_artifact = _load_json(Path(summary["artifact_paths"]["row_fact_metadata"]))
    guardrail_artifact = _load_json(Path(summary["artifact_paths"]["governance_guardrails"]))

    assert row_fact_artifact["row_fact_count"] == 117

    for record in row_fact_artifact["records"]:
        flags = record["evidence"]["guardrail_flags"]
        assert flags["inference_used"] is False
        assert flags["substitution_used"] is False
        assert flags["reconstruction_used"] is False

    status = guardrail_artifact["guardrail_status"]
    assert status["collapsed_state_behavior_detected"] is False
    assert status["forbidden_detector_behavior_detected"] is False
    assert status["inference_behavior_detected"] is False
    assert status["substitution_behavior_detected"] is False
    assert status["reconstruction_behavior_detected"] is False


def test_stage_c3_aggregation_and_reconciliation_artifacts_are_auditable(tmp_path):
    mod = _load_module()
    summary = mod.run_stage_c3_runtime_integration(FIXTURES_ROOT, tmp_path)

    inventory = _load_json(Path(summary["artifact_paths"]["fixture_inventory"]))
    aggregation = _load_json(Path(summary["artifact_paths"]["aggregation_summary"]))
    reconciliation = _load_json(Path(summary["artifact_paths"]["reconciliation_summary"]))
    validation_issues = _load_json(Path(summary["artifact_paths"]["validation_issues"]))

    family_total_rows = sum(int(report["total_rows"]) for report in aggregation["family_reports"])
    assert family_total_rows == inventory["fixture_count"]

    assert reconciliation["total_checks"] == 4
    for result in reconciliation["results"]:
        assert result["check_id"]
        assert result["check_type"]
        assert result["result"] in {"pass", "fail", "blocked"}
        assert isinstance(result["evaluated_inputs"], dict)
        assert isinstance(result["reasons"], list)

    assert validation_issues["issue_count"] == inventory["harness_issue_count"] == 0


def test_stage_c3_runtime_contract_summary_consistent_with_component_artifacts(tmp_path):
    mod = _load_module()
    summary = mod.run_stage_c3_runtime_integration(FIXTURES_ROOT, tmp_path)

    runtime_summary = _load_json(Path(summary["artifact_paths"]["runtime_contract_summary"]))
    reconciliation = _load_json(Path(summary["artifact_paths"]["reconciliation_summary"]))
    validation_issues = _load_json(Path(summary["artifact_paths"]["validation_issues"]))

    assert runtime_summary["contract_scope"] == "stage_c3_baseline_integration"
    assert runtime_summary["harness_issue_count"] == validation_issues["issue_count"]
    assert runtime_summary["reconciliation_fail_count"] == reconciliation["fail_count"]
