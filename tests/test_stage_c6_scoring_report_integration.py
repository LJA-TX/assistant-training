import importlib.util
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from repo_paths import resolve_artifact_path, resolve_fixture_root, resolve_script_path


SCRIPT_PATH = resolve_script_path("stage_c6_scoring_report_integration")
FIXTURES_ROOT = resolve_fixture_root()


def _load_module():
    spec = importlib.util.spec_from_file_location("stage_c6_scoring_report_integration", str(SCRIPT_PATH))
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _copy_sample_inputs(target_path: Path):
    source = resolve_artifact_path("stage_c5_sample_output_records")
    target_path.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def _run(tmp_path: Path):
    mod = _load_module()
    output_records_path = tmp_path / "c6_outputs.jsonl"
    _copy_sample_inputs(output_records_path)
    artifacts_dir = tmp_path / "artifacts"

    summary = mod.run_stage_c6_reporting_integration(
        fixtures_root=FIXTURES_ROOT,
        output_records_path=output_records_path,
        artifacts_dir=artifacts_dir,
    )
    return summary


def test_stage_c6_emits_required_reporting_artifacts(tmp_path):
    summary = _run(tmp_path)

    expected = {
        "per_fixture_scoring_summary",
        "per_model_scoring_summary",
        "parse_tool_nocall_summary",
        "wrapper_leakage_summary",
        "validation_issue_summary",
        "governance_guardrail_summary",
        "runtime_scoring_summary",
        "detector_projection_preparation",
    }
    assert set(summary["artifact_paths"].keys()) == expected
    for path in summary["artifact_paths"].values():
        assert Path(path).exists()


def test_reports_preserve_failure_visibility_and_evidence_links(tmp_path):
    summary = _run(tmp_path)

    per_fixture = _load_json(Path(summary["artifact_paths"]["per_fixture_scoring_summary"]))
    runtime = _load_json(Path(summary["artifact_paths"]["runtime_scoring_summary"]))

    assert runtime["overall_fail_count"] > 0

    failing_rows = [row for row in per_fixture["records"] if row["fail_count"] > 0]
    assert failing_rows, "expected at least one failing fixture summary"
    for row in failing_rows:
        assert isinstance(row["evidence_links"], list)
        assert row["evidence_links"], "failing fixture should retain evidence links"


def test_state_axes_preserved_and_not_collapsed_in_detector_preparation(tmp_path):
    summary = _run(tmp_path)

    detector_prep = _load_json(Path(summary["artifact_paths"]["detector_projection_preparation"]))
    assert detector_prep["authoritative_detector_output"] is False
    assert detector_prep["detector_migration_enabled"] is False

    records = detector_prep["prepared_projection_records"]
    assert records
    for row in records:
        axes = row["projection_state_axes"]
        assert "completeness" in axes
        assert "current_run_computability" in axes
        assert "comparability" in axes
        assert "state" not in axes
        assert "combined_state" not in axes


def test_detector_preparation_is_non_authoritative_and_keeps_provenance_visibility(tmp_path):
    summary = _run(tmp_path)

    detector_prep = _load_json(Path(summary["artifact_paths"]["detector_projection_preparation"]))
    governance = _load_json(Path(summary["artifact_paths"]["governance_guardrail_summary"]))

    assert detector_prep["projection_scope"] == "preparation_only_non_authoritative"
    assert detector_prep["threshold_profile_migration_enabled"] is False

    first = detector_prep["prepared_projection_records"][0]
    provenance = first["projection_provenance"]
    assert "provenance" in provenance
    assert "denominator_provenance" in provenance

    status = governance["migration_authority"]
    assert status["detector_projection_authoritative"] is False
    assert status["detector_migration_enabled"] is False


def test_parse_tool_nocall_and_wrapper_summaries_include_record_level_visibility(tmp_path):
    summary = _run(tmp_path)

    parse_tool = _load_json(Path(summary["artifact_paths"]["parse_tool_nocall_summary"]))
    wrapper = _load_json(Path(summary["artifact_paths"]["wrapper_leakage_summary"]))

    assert isinstance(parse_tool["parse_failure_record_ids"], list)
    assert isinstance(parse_tool["tool_call_missing_record_ids"], list)
    assert isinstance(parse_tool["no_call_mismatch_record_ids"], list)

    assert wrapper["wrapper_counts"]["record_count"] > 0
    assert isinstance(wrapper["wrapper_failure_reasons"], list)
