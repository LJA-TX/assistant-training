import importlib.util
import json
import sys
from pathlib import Path


SCRIPT_PATH = Path("/opt/ai-stack/assistant-training/scripts/stage_c8_non_authoritative_detector_projection_adapter.py")
FIXTURES_ROOT = Path("/opt/ai-stack/assistant-training/manifests/reports/stage_b_wp8_validation/fixtures")
THRESHOLD_PROFILE_PATH = Path("/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_threshold_profile.json")


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "stage_c8_non_authoritative_detector_projection_adapter",
        str(SCRIPT_PATH),
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _copy_sample_inputs(target_path: Path):
    source = Path("/opt/ai-stack/assistant-training/reports/stage_c6/input/stage_c6_sample_output_records.jsonl")
    target_path.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def _run(tmp_path: Path):
    mod = _load_module()
    output_records_path = tmp_path / "c8_outputs.jsonl"
    _copy_sample_inputs(output_records_path)
    artifacts_dir = tmp_path / "artifacts"

    summary = mod.run_stage_c8_projection_adapter(
        fixtures_root=FIXTURES_ROOT,
        output_records_path=output_records_path,
        threshold_profile_path=THRESHOLD_PROFILE_PATH,
        artifacts_dir=artifacts_dir,
    )
    return summary


def test_stage_c8_emits_required_projection_artifacts(tmp_path):
    summary = _run(tmp_path)

    expected = {
        "projection_adapter",
        "projected_eval_summary",
        "projected_baseline_summary",
        "noncomputable_metrics",
        "compatibility_harness",
        "projection_validation",
        "stage_c6_summary",
        "stage_c6_validation_issue_summary",
    }
    assert set(summary["artifact_paths"].keys()) == expected
    for path in summary["artifact_paths"].values():
        assert Path(path).exists()

    flags = summary["adapter_flags"]
    assert flags["authoritative_detector_output"] is False
    assert flags["detector_migration_enabled"] is False
    assert flags["threshold_profile_migration_enabled"] is False


def test_unambiguous_metrics_are_projected_without_enabling_migration(tmp_path):
    summary = _run(tmp_path)
    projection = _load_json(Path(summary["artifact_paths"]["projection_adapter"]))

    records = projection["metric_records"]
    assert records["no_call_correctness_aggregate"]["projection_status"] == "computed"
    assert records["wrapper_leakage_overall"]["projection_status"] == "computed"
    assert records["invalid_json_overall"]["projection_status"] == "computed"
    assert records["direct_answer_substitution_count"]["projection_status"] == "computed"

    projected_eval = _load_json(Path(summary["artifact_paths"]["projected_eval_summary"]))
    assert projected_eval["adapter_flags"]["authoritative_detector_output"] is False
    assert projected_eval["adapter_flags"]["detector_migration_enabled"] is False
    assert projected_eval["adapter_flags"]["threshold_profile_migration_enabled"] is False

    assert projected_eval["metrics"]["aggregate"]["no_call_correctness"] == 0.5
    assert projected_eval["metrics"]["aggregate"]["wrapper_leakage"] == 0.125
    assert projected_eval["metrics"]["aggregate"]["invalid_json"] == 0.25
    assert (
        projected_eval["failure_profile"]["failure_categories_non_exact_tool_rows"]["direct_answer_substitution"] == 2.0
    )


def test_blocked_and_missing_source_metrics_are_explicitly_noncomputable(tmp_path):
    summary = _run(tmp_path)
    noncomputable = _load_json(Path(summary["artifact_paths"]["noncomputable_metrics"]))
    rows = {row["metric_id"]: row for row in noncomputable["records"]}

    assert rows["no_call_correctness_adversarial"]["projection_status"] == "noncomputable_blocked"
    assert rows["no_call_correctness_adversarial"]["reason_code"] == "blocked_adversarial_subset_mapping_unavailable"

    assert rows["no_anchor_exact_valid_share"]["projection_status"] == "noncomputable_blocked"
    assert rows["no_anchor_exact_valid_share"]["reason_code"] == "blocked_no_anchor_share_semantic_mismatch"

    assert rows["read_file_exact_valid_rate"]["projection_status"] == "noncomputable_missing_source"
    assert rows["read_file_exact_valid_rate"]["reason_code"] == "source_family_concept_missing_in_current_run"

    assert rows["read_file_symbol_name_exact_valid_rate"]["projection_status"] == "noncomputable_missing_source"
    assert rows["read_file_symbol_name_exact_valid_rate"]["reason_code"] == "source_family_concept_missing_in_current_run"


def test_compatibility_harness_proves_consumer_readability_and_axis_preservation(tmp_path):
    summary = _run(tmp_path)
    compatibility = _load_json(Path(summary["artifact_paths"]["compatibility_harness"]))

    assert compatibility["fail_count"] == 0
    checks = {check["check_id"]: check for check in compatibility["checks"]}
    assert checks["schema_continuity_metric_catalog_coverage"]["result"] == "pass"
    assert checks["axis_preservation"]["result"] == "pass"
    assert checks["evidence_preservation"]["result"] == "pass"
    assert checks["consumer_readability"]["result"] == "pass"

    detector_outputs = compatibility["detector_outputs"]
    assert Path(detector_outputs["collapse_watch_interpretation_path"]).exists()
    assert Path(detector_outputs["gate_assessment_path"]).exists()

    consumer_details = checks["consumer_readability"]["details"]
    assert "no_call_correctness_adversarial_lt_1_0" in consumer_details["noncomputable_rule_ids"]
    assert "no_anchor_exact_valid_share_lt_0_75" in consumer_details["noncomputable_rule_ids"]


def test_projection_validation_keeps_guardrails_and_migration_flags_disabled(tmp_path):
    summary = _run(tmp_path)
    validation = _load_json(Path(summary["artifact_paths"]["projection_validation"]))

    assert validation["fail_count"] == 0
    checks = {check["check_id"]: check for check in validation["checks"]}
    assert checks["unambiguous_mapping_stability"]["result"] == "pass"
    assert checks["blocked_metrics_noncomputable"]["result"] == "pass"
    assert checks["no_inference_substitution_reconstruction"]["result"] == "pass"
    assert checks["migration_flags_disabled"]["result"] == "pass"
    assert checks["consumer_compatibility_harness"]["result"] == "pass"

