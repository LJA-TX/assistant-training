import importlib.util
import json
import sys
from pathlib import Path


SCRIPT_PATH = Path("/opt/ai-stack/assistant-training/scripts/stage_c5_scoring_path_integration.py")
FIXTURES_ROOT = Path("/opt/ai-stack/assistant-training/manifests/reports/stage_b_wp8_validation/fixtures")


def _load_module():
    spec = importlib.util.spec_from_file_location("stage_c5_scoring_path_integration", str(SCRIPT_PATH))
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write_records(path: Path):
    rows = [
        {
            "record_id": "score-001",
            "fixture_id": "A-C-001",
            "source_definition_id": "A-C-001",
            "model_identifier": "score-model-v0",
            "prompt_reference": "prompt://a-c-001",
            "raw_model_response": '{"tool_calls":[{"id":"call_1","type":"function","function":{"name":"read_file","arguments":"{\\"path\\":\\"/tmp/a.txt\\",\\"line_start\\":1,\\"line_end\\":2}"}}]}',
            "no_call_expected": False,
            "expected_tool_call_required": True,
            "expected_tool_name": "read_file",
            "expected_argument_keys": ["path", "line_start", "line_end"],
            "expected_strict_json_object": True,
            "wrapper_prohibited": True,
        },
        {
            "record_id": "score-002",
            "fixture_id": "A-C-004",
            "source_definition_id": "A-C-004",
            "model_identifier": "score-model-v0",
            "prompt_reference": "prompt://a-c-004",
            "raw_model_response": '{"tool_calls":[{"id":"call_1","type":"function","function":{"name":"read_file","arguments":"{\\"path\\":\\"/tmp/bad.json\\"}"}}]',
            "no_call_expected": False,
            "expected_tool_call_required": True,
            "expected_tool_name": "read_file",
            "expected_argument_keys": ["path"],
            "expected_strict_json_object": False,
            "wrapper_prohibited": True,
        },
        {
            "record_id": "score-003",
            "fixture_id": "A-C-006",
            "source_definition_id": "A-C-006",
            "model_identifier": "score-model-v0",
            "prompt_reference": "prompt://a-c-006",
            "raw_model_response": '{"message":"no tool call emitted"}',
            "no_call_expected": False,
            "expected_tool_call_required": True,
            "expected_tool_name": "read_file",
            "expected_argument_keys": ["path"],
            "expected_strict_json_object": True,
            "wrapper_prohibited": True,
        },
        {
            "record_id": "score-004",
            "fixture_id": "A-C-008",
            "source_definition_id": "A-C-008",
            "model_identifier": "score-model-v0",
            "prompt_reference": "prompt://a-c-008",
            "raw_model_response": '{"tool_calls":[{"id":"call_1","type":"function","function":{"name":"read_file"}}]}',
            "no_call_expected": False,
            "expected_tool_call_required": True,
            "expected_tool_name": "read_file",
            "expected_argument_keys": ["path"],
            "expected_strict_json_object": True,
            "wrapper_prohibited": True,
        },
        {
            "record_id": "score-005",
            "fixture_id": "A-C-007",
            "source_definition_id": "A-C-007",
            "model_identifier": "score-model-v0",
            "prompt_reference": "prompt://a-c-007",
            "raw_model_response": '{"tool_calls":[{"id":"call_1","type":"function","function":{"name":"list_dir","arguments":"{\\"path\\":\\"/tmp\\"}"}}]}',
            "no_call_expected": False,
            "expected_tool_call_required": True,
            "expected_tool_name": "read_file",
            "expected_argument_keys": ["path"],
            "expected_strict_json_object": True,
            "wrapper_prohibited": True,
        },
        {
            "record_id": "score-006",
            "fixture_id": "A-C-005",
            "source_definition_id": "A-C-005",
            "model_identifier": "score-model-v0",
            "prompt_reference": "prompt://a-c-005",
            "raw_model_response": 'Wrapper prefix {"tool_calls":[{"id":"call_1","type":"function","function":{"name":"read_file","arguments":"{\\"path\\":\\"/tmp/wrapped.txt\\"}"}}]} wrapper suffix',
            "no_call_expected": False,
            "expected_tool_call_required": True,
            "expected_tool_name": "read_file",
            "expected_argument_keys": ["path"],
            "expected_strict_json_object": False,
            "wrapper_prohibited": True,
        },
        {
            "record_id": "score-007",
            "fixture_id": "A-NI-004",
            "source_definition_id": "A-NI-004",
            "model_identifier": "score-model-v0",
            "prompt_reference": "prompt://a-ni-004",
            "raw_model_response": '{"tool_calls":[]}',
            "no_call_expected": True,
            "expected_tool_call_required": False,
            "expected_strict_json_object": True,
            "wrapper_prohibited": True,
        },
        {
            "record_id": "score-008",
            "fixture_id": "A-NI-004",
            "source_definition_id": "A-NI-004",
            "model_identifier": "score-model-v0",
            "prompt_reference": "prompt://a-ni-004b",
            "raw_model_response": '{"tool_calls":[{"id":"call_1","type":"function","function":{"name":"read_file","arguments":"{\\"path\\":\\"/tmp/unexpected.txt\\"}"}}]}',
            "no_call_expected": True,
            "expected_tool_call_required": False,
            "expected_tool_name": "read_file",
            "expected_argument_keys": ["path"],
            "expected_strict_json_object": True,
            "wrapper_prohibited": True,
        },
    ]
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")


def _run(tmp_path: Path):
    mod = _load_module()
    output_records_path = tmp_path / "c5_outputs.jsonl"
    _write_records(output_records_path)
    artifacts_dir = tmp_path / "artifacts"

    summary = mod.run_stage_c5_scoring_integration(
        fixtures_root=FIXTURES_ROOT,
        output_records_path=output_records_path,
        artifacts_dir=artifacts_dir,
    )
    return summary


def test_stage_c5_emits_scored_contract_artifacts(tmp_path):
    summary = _run(tmp_path)

    expected = {
        "scoring_input_binding",
        "per_output_scoring_status",
        "per_fixture_scoring_status",
        "parse_tool_nocall_scoring_summary",
        "wrapper_leakage_scoring_summary",
        "validation_issues",
        "governance_guardrails",
        "runtime_scoring_summary",
    }
    assert set(summary["artifact_paths"].keys()) == expected
    for path in summary["artifact_paths"].values():
        assert Path(path).exists()
    assert Path(summary["summary_path"]).exists()


def test_valid_strict_output_scores_as_valid_and_wrong_tool_is_not_corrected(tmp_path):
    summary = _run(tmp_path)
    per_output = _load_json(Path(summary["artifact_paths"]["per_output_scoring_status"]))
    rows = {row["record_id"]: row for row in per_output["records"]}

    score001 = rows["score-001"]
    assert score001["overall_status"] == "pass"
    dims001 = {d["dimension"]: d for d in score001["scoring_dimensions"]}
    assert dims001["strict_json_validity"]["status"] == "pass"
    assert dims001["tool_name_correctness"]["status"] == "pass"

    score005 = rows["score-005"]
    dims005 = {d["dimension"]: d for d in score005["scoring_dimensions"]}
    assert dims005["tool_name_correctness"]["status"] == "fail"
    assert "does not match expected" in dims005["tool_name_correctness"]["reason"]


def test_invalid_json_missing_tool_and_partial_arguments_are_preserved_and_scored(tmp_path):
    summary = _run(tmp_path)
    per_output = _load_json(Path(summary["artifact_paths"]["per_output_scoring_status"]))
    rows = {row["record_id"]: row for row in per_output["records"]}

    score002 = rows["score-002"]
    assert score002["parse_status"] == "invalid_json"
    dims002 = {d["dimension"]: d for d in score002["scoring_dimensions"]}
    assert dims002["strict_json_validity"]["status"] == "pass"

    score003 = rows["score-003"]
    assert score003["tool_call_status"] == "tool_calls_key_missing"
    dims003 = {d["dimension"]: d for d in score003["scoring_dimensions"]}
    assert dims003["tool_call_presence_absence"]["status"] == "fail"

    score004 = rows["score-004"]
    assert score004["tool_call_status"] == "tool_call_payload_partial_or_invalid"
    dims004 = {d["dimension"]: d for d in score004["scoring_dimensions"]}
    assert dims004["argument_presence_structure"]["status"] == "fail"


def test_wrapper_leakage_and_no_call_cases_are_scored_without_reconstruction(tmp_path):
    summary = _run(tmp_path)
    per_output = _load_json(Path(summary["artifact_paths"]["per_output_scoring_status"]))
    wrapper_summary = _load_json(Path(summary["artifact_paths"]["wrapper_leakage_scoring_summary"]))
    guardrails = _load_json(Path(summary["artifact_paths"]["governance_guardrails"]))

    rows = {row["record_id"]: row for row in per_output["records"]}

    score006 = rows["score-006"]
    assert score006["wrapper_or_prose_leakage"] is True
    dims006 = {d["dimension"]: d for d in score006["scoring_dimensions"]}
    assert dims006["wrapper_leakage"]["status"] == "fail"

    score007 = rows["score-007"]
    dims007 = {d["dimension"]: d for d in score007["scoring_dimensions"]}
    assert dims007["no_call_correctness"]["status"] == "pass"

    score008 = rows["score-008"]
    dims008 = {d["dimension"]: d for d in score008["scoring_dimensions"]}
    assert dims008["no_call_correctness"]["status"] == "fail"

    assert wrapper_summary["wrapper_or_prose_leakage_count"] >= 1

    status = guardrails["guardrail_status"]
    assert status["tool_call_reconstruction_performed"] is False
    assert status["argument_reconstruction_performed"] is False
    assert status["fallback_tool_name_inference_performed"] is False


def test_stage_c5_runtime_summary_and_fixture_rollup_present(tmp_path):
    summary = _run(tmp_path)
    runtime = _load_json(Path(summary["artifact_paths"]["runtime_scoring_summary"]))
    per_fixture = _load_json(Path(summary["artifact_paths"]["per_fixture_scoring_status"]))
    status_summary = _load_json(Path(summary["artifact_paths"]["parse_tool_nocall_scoring_summary"]))

    assert runtime["record_count"] == 8
    assert runtime["overall_pass_count"] + runtime["overall_fail_count"] == 8
    assert runtime["c4_summary"]["record_count"] == 8

    fixture_ids = {row["fixture_id"] for row in per_fixture["records"]}
    assert "A-C-001" in fixture_ids
    assert "A-C-007" in fixture_ids

    assert "strict_json_object" in status_summary["parse_status_counts"]
