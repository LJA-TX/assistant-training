import importlib.util
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from repo_paths import resolve_artifact_path, resolve_fixture_root, resolve_repo_root, resolve_script_path


SCRIPT_PATH = resolve_script_path("stage_c8_non_authoritative_detector_projection_adapter")
FIXTURES_ROOT = resolve_fixture_root()
THRESHOLD_PROFILE_PATH = resolve_artifact_path("stage_b_v1_threshold_profile")


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
    source = resolve_artifact_path("stage_c6_sample_output_records")
    target_path.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def _write_records(target_path: Path, records: list[dict]):
    target_path.write_text(
        "\n".join(json.dumps(record, sort_keys=True) for record in records) + "\n",
        encoding="utf-8",
    )


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


def _run_with_records(tmp_path: Path, records: list[dict]):
    mod = _load_module()
    output_records_path = tmp_path / "c8_outputs.jsonl"
    _write_records(output_records_path, records)
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
        "baseline_delta_gate",
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


def test_convergence_metadata_source_paths_are_repo_root_resolved_and_present():
    mod = _load_module()
    repo_root = resolve_repo_root()
    paths = mod._convergence_metadata_source_paths()

    assert set(paths) == {
        "c7_gate",
        "c9a_contract",
        "c9b_review",
        "c9c_gate",
        "c9d_disposition",
        "c10a_plan",
    }
    for value in paths.values():
        path = Path(value)
        assert path.is_absolute()
        assert path.exists()
        assert path.is_relative_to(repo_root)


def test_blocked_and_missing_source_metrics_are_explicitly_noncomputable(tmp_path):
    summary = _run(tmp_path)
    noncomputable = _load_json(Path(summary["artifact_paths"]["noncomputable_metrics"]))
    rows = {row["metric_id"]: row for row in noncomputable["records"]}

    assert rows["no_call_correctness_adversarial"]["projection_status"] == "noncomputable_blocked"
    assert rows["no_call_correctness_adversarial"]["reason_code"] == "blocked_adversarial_subset_mapping_unavailable"

    assert rows["no_anchor_exact_valid_share"]["projection_status"] == "noncomputable_blocked"
    assert rows["no_anchor_exact_valid_share"]["reason_code"] == "blocked_no_anchor_share_semantic_mismatch"
    assert rows["no_anchor_exact_valid_share"]["evidence"]["disposition"] == "authoritative_noncomputable_preservation"

    assert rows["read_file_exact_valid_rate"]["projection_status"] == "noncomputable_missing_source"
    assert rows["read_file_exact_valid_rate"]["reason_code"] == "source_family_concept_missing_in_current_run"

    assert rows["read_file_symbol_name_exact_valid_rate"]["projection_status"] == "noncomputable_missing_source"
    assert rows["read_file_symbol_name_exact_valid_rate"]["reason_code"] == "source_family_concept_missing_in_current_run"


def test_compatibility_harness_proves_consumer_readability_and_axis_preservation(tmp_path):
    summary = _run(tmp_path)
    compatibility = _load_json(Path(summary["artifact_paths"]["compatibility_harness"]))

    assert compatibility["fail_count"] == 0
    assert compatibility["adapter_flags"]["authoritative_detector_output"] is False
    assert compatibility["adapter_flags"]["detector_migration_enabled"] is False
    assert compatibility["adapter_flags"]["threshold_profile_migration_enabled"] is False
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
    assert checks["adversarial_mapping_contract_behavior"]["result"] == "pass"
    assert checks["no_anchor_noncomputable_preservation"]["result"] == "pass"
    assert checks["baseline_delta_gate_blocked_for_compatibility_baseline"]["result"] == "pass"
    assert checks["no_inference_substitution_reconstruction"]["result"] == "pass"
    assert checks["migration_flags_disabled"]["result"] == "pass"
    assert checks["consumer_compatibility_harness"]["result"] == "pass"


def test_c10b_baseline_delta_gate_blocks_compatibility_only_baseline(tmp_path):
    summary = _run(tmp_path)
    gate = _load_json(Path(summary["artifact_paths"]["baseline_delta_gate"]))

    assert gate["authoritative_detector_output"] is False
    assert gate["detector_migration_enabled"] is False
    assert gate["threshold_profile_migration_enabled"] is False
    assert gate["compatibility_only_baseline"] is True
    assert gate["rule_count"] == 1
    assert gate["blocked_rule_count"] == 1

    rule = gate["rule_records"][0]
    assert rule["rule_id"] == "direct_answer_substitution_delta_gt_3"
    assert rule["gate_result"] == "blocked"
    assert "baseline_compatibility_only" in rule["reason_codes"]
    assert "comparability_status_missing" in rule["reason_codes"]


def test_c10b_contract_references_are_emitted(tmp_path):
    summary = _run(tmp_path)
    projection = _load_json(Path(summary["artifact_paths"]["projection_adapter"]))

    assert projection["integration_scope"] == "stage_c10b_non_authoritative_contract_integration"
    contract_sources = projection["contract_sources"]
    assert "STAGE_C9A_ADVERSARIAL_NO_CALL_SUBSET_MAPPING_REVIEW.md" in contract_sources[
        "c9a_adversarial_no_call_subset_mapping"
    ]
    assert "STAGE_C9C_BASELINE_DELTA_COMPARABILITY_GATE_REVIEW.md" in contract_sources[
        "c9c_baseline_delta_comparability_gate"
    ]
    assert "STAGE_C9D_NO_ANCHOR_METRIC_DISPOSITION_REVIEW.md" in contract_sources[
        "c9d_no_anchor_metric_disposition"
    ]


def test_c10b_adversarial_metric_computes_only_from_explicit_subset_evidence(tmp_path):
    records = [
        {
            "record_id": "adv-explicit-001",
            "fixture_id": "A-NI-004",
            "source_definition_id": "A-NI-004",
            "model_identifier": "score-model-v0",
            "prompt_reference": "prompt://adv-explicit-001",
            "raw_model_response": "{\"tool_calls\":[]}",
            "no_call_expected": True,
            "expected_tool_call_required": False,
            "expected_strict_json_object": True,
            "wrapper_prohibited": True,
            "subset_id": "adversarial_no_call",
        },
        {
            "record_id": "adv-explicit-002",
            "fixture_id": "A-NI-004",
            "source_definition_id": "A-NI-004",
            "model_identifier": "score-model-v0",
            "prompt_reference": "prompt://adv-explicit-002",
            "raw_model_response": (
                "{\"tool_calls\":[{\"id\":\"call_1\",\"type\":\"function\","
                "\"function\":{\"name\":\"read_file\",\"arguments\":\"{\\\"path\\\":\\\"/tmp/unexpected.txt\\\"}\"}}]}"
            ),
            "no_call_expected": True,
            "expected_tool_call_required": False,
            "expected_tool_name": "read_file",
            "expected_argument_keys": ["path"],
            "expected_strict_json_object": True,
            "wrapper_prohibited": True,
            "source_split": "adversarial",
        },
        {
            "record_id": "aggregate-no-call-only",
            "fixture_id": "A-NI-004",
            "source_definition_id": "A-NI-004",
            "model_identifier": "score-model-v0",
            "prompt_reference": "prompt://aggregate-no-call-only",
            "raw_model_response": "{\"tool_calls\":[]}",
            "no_call_expected": True,
            "expected_tool_call_required": False,
            "expected_strict_json_object": True,
            "wrapper_prohibited": True,
        },
    ]

    summary = _run_with_records(tmp_path, records)
    projection = _load_json(Path(summary["artifact_paths"]["projection_adapter"]))
    record = projection["metric_records"]["no_call_correctness_adversarial"]

    assert record["projection_status"] == "computed"
    assert record["value"] == 0.5
    assert record["evidence"]["reason_code"] == "source_adversarial_subset_explicit_evidence_computed"
    assert record["evidence"]["denominator"] == 2.0
    assert record["evidence"]["numerator"] == 1.0
    assert {row["record_id"] for row in record["evidence"]["included_records"]} == {
        "adv-explicit-001",
        "adv-explicit-002",
    }

    validation = _load_json(Path(summary["artifact_paths"]["projection_validation"]))
    checks = {check["check_id"]: check for check in validation["checks"]}
    assert checks["adversarial_mapping_contract_behavior"]["result"] == "pass"
