import importlib.util
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from repo_paths import resolve_fixture_root, resolve_script_path


SCRIPT_PATH = resolve_script_path("stage_c4_real_output_ingestion")
FIXTURES_ROOT = resolve_fixture_root()


def _load_module():
    spec = importlib.util.spec_from_file_location("stage_c4_real_output_ingestion", str(SCRIPT_PATH))
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write_output_records(path: Path) -> str:
    valid_response = (
        '{"tool_calls":[{"id":"call_1","type":"function","function":{"name":"read_file",'
        '"arguments":"{\\"path\\":\\"/tmp/a.txt\\",\\"line_start\\":1,\\"line_end\\":2}"}}]}'
    )
    wrapped_response = (
        'prefix prose {"tool_calls":[{"id":"call_1","type":"function","function":'
        '{"name":"read_file","arguments":"{\\"path\\":\\"/tmp/wrapped.txt\\"}"}}]} suffix'
    )
    invalid_json_response = '{"tool_calls":[{"id":"call_1","type":"function","function":{"name":"read_file"}}'
    partial_payload_response = '{"tool_calls":[{"id":"call_1","type":"function","function":{"name":"read_file"}}]}'
    missing_tool_calls_response = '{"message":"tool call omitted"}'

    rows = [
        {
            "record_id": "out-001",
            "fixture_id": "A-C-001",
            "source_definition_id": "A-C-001",
            "model_identifier": "model-x",
            "prompt_reference": "prompt://a-c-001",
            "raw_model_response": valid_response,
            "no_call_expected": False,
        },
        {
            "record_id": "out-002",
            "fixture_id": "A-C-005",
            "source_definition_id": "A-C-005",
            "model_identifier": "model-x",
            "prompt_reference": "prompt://a-c-005",
            "raw_model_response": wrapped_response,
            "no_call_expected": False,
        },
        {
            "record_id": "out-003",
            "fixture_id": "A-C-006",
            "source_definition_id": "A-C-006",
            "model_identifier": "model-x",
            "prompt_reference": "prompt://a-c-006",
            "raw_model_response": invalid_json_response,
            "no_call_expected": False,
        },
        {
            "record_id": "out-004",
            "fixture_id": "A-NI-004",
            "source_definition_id": "A-NI-004",
            "model_identifier": "model-x",
            "prompt_reference": "prompt://a-ni-004",
            "raw_model_response": '{"tool_calls":[]}',
            "no_call_expected": True,
        },
        {
            "record_id": "out-005",
            "fixture_id": "A-C-008",
            "source_definition_id": "A-C-008",
            "model_identifier": "model-x",
            "prompt_reference": "prompt://a-c-008",
            "raw_model_response": partial_payload_response,
            "no_call_expected": False,
        },
        {
            "record_id": "out-006",
            "fixture_id": "A-C-007",
            "source_definition_id": "A-C-007",
            "model_identifier": "model-x",
            "prompt_reference": "prompt://a-c-007",
            "raw_model_response": missing_tool_calls_response,
            "no_call_expected": False,
        },
    ]

    lines = [json.dumps(row, ensure_ascii=False) for row in rows]
    lines.append('{"record_id":"broken"')
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return valid_response


def _run(tmp_path: Path):
    mod = _load_module()
    output_records_path = tmp_path / "output_records.jsonl"
    valid_response = _write_output_records(output_records_path)
    artifacts_dir = tmp_path / "artifacts"

    summary = mod.run_stage_c4_output_ingestion(
        fixtures_root=FIXTURES_ROOT,
        output_records_path=output_records_path,
        artifacts_dir=artifacts_dir,
    )
    return summary, valid_response


def test_stage_c4_emits_required_contract_artifacts(tmp_path):
    summary, _ = _run(tmp_path)

    expected = {
        "output_inventory",
        "parse_toolcall_status",
        "row_fact_metadata",
        "state_axis_from_outputs",
        "aggregation_summary_from_outputs",
        "reconciliation_summary_from_outputs",
        "validation_issues",
        "governance_guardrails",
        "runtime_contract_summary",
    }
    assert set(summary["artifact_paths"].keys()) == expected
    for path in summary["artifact_paths"].values():
        assert Path(path).exists()

    assert Path(summary["summary_path"]).exists()
    assert summary["record_count"] == 7


def test_valid_output_is_ingested_without_mutation_or_argument_reconstruction(tmp_path):
    summary, valid_response = _run(tmp_path)

    inventory = _load_json(Path(summary["artifact_paths"]["output_inventory"]))
    records = {record["record_id"]: record for record in inventory["records"]}
    out001 = records["out-001"]

    assert out001["raw_model_response"] == valid_response
    assert out001["raw_response_mutated"] is False
    assert out001["parse_status"] == "strict_json_object"
    assert out001["tool_call_status"] == "tool_call_payload_present"

    tool_payload = out001["parsed_tool_call_payload"]
    arguments = tool_payload["tool_calls"][0]["function"]["arguments"]
    assert isinstance(arguments, str)
    assert "line_start" in arguments


def test_invalid_unparseable_and_wrapper_outputs_remain_preserved_and_flagged(tmp_path):
    summary, _ = _run(tmp_path)

    inventory = _load_json(Path(summary["artifact_paths"]["output_inventory"]))
    validation = _load_json(Path(summary["artifact_paths"]["validation_issues"]))

    records = {record["record_id"]: record for record in inventory["records"]}
    assert records["out-002"]["wrapper_or_prose_leakage"] is True
    assert records["out-002"]["parse_status"] == "invalid_json_with_embedded_object"
    assert records["out-002"]["embedded_payload_candidate"] is not None

    assert records["out-003"]["parse_status"] == "invalid_json"
    assert records["out-003"]["parse_error"]

    assert records["line-7"]["parse_status"] == "record_json_invalid"
    issue_codes = {issue["issue_code"] for issue in validation["issues"]}
    assert "invalid_json_line" in issue_codes


def test_missing_and_partial_tool_call_payloads_are_not_reconstructed(tmp_path):
    summary, _ = _run(tmp_path)

    inventory = _load_json(Path(summary["artifact_paths"]["output_inventory"]))
    parse_status = _load_json(Path(summary["artifact_paths"]["parse_toolcall_status"]))

    records = {record["record_id"]: record for record in inventory["records"]}
    out005 = records["out-005"]
    out006 = records["out-006"]

    assert out005["tool_call_status"] == "tool_call_payload_partial_or_invalid"
    call = out005["parsed_tool_call_payload"]["tool_calls"][0]
    assert "arguments" not in call["function"]

    assert out006["tool_call_status"] == "tool_calls_key_missing"
    assert out006["parsed_tool_call_payload"] is None

    status_records = {record["record_id"]: record for record in parse_status["records"]}
    assert status_records["out-004"]["no_call_status"] == "expected_no_call_emitted"


def test_state_axis_and_guardrails_preserve_contract_constraints(tmp_path):
    summary, _ = _run(tmp_path)

    state = _load_json(Path(summary["artifact_paths"]["state_axis_from_outputs"]))
    guardrails = _load_json(Path(summary["artifact_paths"]["governance_guardrails"]))
    reconciliation = _load_json(Path(summary["artifact_paths"]["reconciliation_summary_from_outputs"]))

    assert state["record_count"] == 7
    for record in state["records"]:
        assert "state" not in record
        assert "combined_state" not in record
        assert record["comparability"] == "comparison-blocked"

    status = guardrails["guardrail_status"]
    assert status["collapsed_state_behavior_detected"] is False
    assert status["reconstruction_behavior_detected"] is False
    assert status["tool_call_reconstruction_performed"] is False
    assert status["argument_reconstruction_performed"] is False
    assert status["fallback_tool_name_inference_performed"] is False

    assert reconciliation["total_checks"] == 4
    for result in reconciliation["results"]:
        assert result["check_id"]
        assert result["result"] in {"pass", "fail", "blocked"}
