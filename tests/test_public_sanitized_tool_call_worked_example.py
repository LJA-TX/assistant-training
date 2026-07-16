from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

FIXTURE_PATH = REPO_ROOT / "docs" / "framework" / "examples" / "public_sanitized_tool_call_worked_example.json"
DOC_PATH = REPO_ROOT / "docs" / "framework" / "examples" / "public_sanitized_tool_call_worked_example.md"
README_PATH = REPO_ROOT / "README.md"
START_HERE_PATH = REPO_ROOT / "docs" / "current" / "start_here.md"

PUBLIC_PORTABLE_SURFACES = (
    "README.md",
    "docs/current/start_here.md",
    "evals/canonical_eval_manifest_v1.json",
    "docs/current/status/TRAINING_RUN_HISTORY.md",
    "docs/publication/public_reference_dispositions.json",
    "scripts/train_lora_sft.py",
    "scripts/eval_canonical_manifest.py",
    "scripts/repo_paths.py",
)


if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))


def _load_module(script_name: str, module_name: str):
    script_path = REPO_ROOT / "scripts" / script_name
    spec = importlib.util.spec_from_file_location(module_name, str(script_path))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _canonical_json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_fixture() -> dict:
    return json.loads(_read_text(FIXTURE_PATH))


def _render_prompt(system_content: str, registry: dict, user_content: str) -> str:
    return "SYSTEM\n" + system_content + "\nTOOLS\n" + _canonical_json(registry) + "\nUSER\n" + user_content + "\nASSISTANT\n"


def _expected_tool_payload(row: dict) -> dict | None:
    assistant_message = row["assistant_message"]
    if isinstance(assistant_message.get("tool_calls"), list):
        return assistant_message
    return None


def _build_eval_row(mod, row: dict):
    assistant_message = _expected_tool_payload(row)
    expected_no_call = row["row_role"] == "no_call_restraint"
    expected_tool = not expected_no_call
    expected_tool_names = mod._extract_tool_names(assistant_message) if assistant_message is not None else []
    expected_args = mod._extract_arguments(assistant_message)[0] if assistant_message is not None else []
    return mod.EvalRow(
        split="worked_example",
        row_index_1based=1,
        source_case_id=row["row_id"],
        system_text=row["source_fields"]["system_content"],
        user_text=row["source_fields"]["user_content"],
        prompt_prefix=row["rendered_prompt"],
        expected_tool=expected_tool,
        expected_no_call=expected_no_call,
        expected_payload=assistant_message,
        expected_tool_names=expected_tool_names,
        expected_args=expected_args,
        metadata=dict(row["dataset_row"].get("metadata") or {}),
    )


def _classify(mod, row: dict, prediction_text: str) -> dict:
    eval_row = _build_eval_row(mod, row)
    classified = mod._classify(eval_row, prediction_text)
    labels = mod._build_preaggregation_labels(eval_row, classified)
    return {"classified": classified, "labels": labels}


def _assert_expected_evaluator_result(mod, row: dict, prediction_text: str, expected: dict) -> None:
    actual = _classify(mod, row, prediction_text)
    combined = dict(actual["classified"])
    combined.update(actual["labels"])
    combined.setdefault("label", combined.get("primary_class"))
    for key, value in expected.items():
        if key == "precedence_note":
            continue
        assert combined[key] == value, (row["row_id"], key, combined[key], value)


def _assert_only_expected_performance_language(text: str) -> None:
    forbidden_patterns = [
        r"\b\d+(?:\.\d+)?%",
        r"\bimproved by\b",
        r"\bmodel improved\b",
        r"\boutperformed\b",
        r"\boutperforms\b",
        r"\bbenchmark result\b",
        r"\brun claim\b",
        r"\bmeasured model improvement\b",
    ]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, text, flags=re.IGNORECASE)


def _assert_no_sensitive_markers(text: str) -> None:
    forbidden_patterns = [
        r"/" "opt" "/ai-stack/",
        r"/" "home" "/roy/",
        r"BEGIN [A-Z ]*" "PRIVATE KEY",
        r"s" "k-[A-Za-z0-9]{20,}",
        r"gh" "p_[A-Za-z0-9]{20,}",
        r"xox" "[baprs]-[A-Za-z0-9-]{10,}",
        r"AK" "IA[0-9A-Z]{16}",
        r"[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+",
    ]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, text)


def _row_scored_target_record(row: dict) -> dict:
    return {
        "row_id": row["row_id"],
        "output_id": f"{row['row_id']}_scored_assistant_target",
        "output_kind": "scored_assistant_target",
        "serialized_output": row["assistant_target_text"],
        "output_sha256": row["assistant_target_sha256"],
        "expected_evaluator_result": row["expected_evaluator_result"],
    }


def _row_output_records(row: dict) -> list[dict]:
    records: list[dict] = [_row_scored_target_record(row)]
    for bad in row.get("illustrative_bad_outputs", []):
        records.append(bad)
    fabricated = row.get("fabricated_tool_result")
    if fabricated is not None:
        records.append(fabricated)
    post_tool = row.get("illustrative_post_tool_response")
    if post_tool is not None:
        records.append(post_tool)
    return records


def validate_fixture_contract_and_canonical_evaluator_reuse():
    fixture = _load_fixture()
    train_mod = _load_module("train_lora_sft.py", "train_lora_sft_public_worked_example")
    eval_mod = _load_module("eval_canonical_manifest.py", "eval_canonical_manifest_public_worked_example")
    assert hasattr(train_mod, "_serialize_assistant_target")
    assert hasattr(eval_mod, "_classify")
    assert hasattr(eval_mod, "_build_preaggregation_labels")
    row_prompt_map = {entry["row_id"]: entry for entry in fixture["row_to_prompt_map"]}
    row_output_map = {entry["output_id"]: entry for entry in fixture["row_to_output_map"]}

    assert fixture["schema_version"] == "public-sanitized-tool-call-worked-example-v1"
    assert fixture["package_id"] == "harborview-public-sanitized-tool-call-example-v1"
    assert fixture["artifact_role"] == "synthetic_public_demonstration"
    assert fixture["execution_status"] == "synthetic_not_executed"
    assert fixture["render_contract"] == "synthetic-render-v1"

    registry = fixture["registry"]
    assert [tool["name"] for tool in registry["tools"]] == [
        "search_catalog",
        "get_availability",
        "place_hold",
    ]
    for tool in registry["tools"]:
        params = tool["parameters"]
        assert params["type"] == "object"
        assert set(params["required"]) == set(params["properties"].keys())

    rendered_registry = _canonical_json(registry)
    assert fixture["registry_sha256"] == _sha256_text(rendered_registry)

    rows = fixture["rows"]
    assert len(rows) == 3
    assert {row["row_id"] for row in rows} == {
        "demo_row_availability_01",
        "demo_row_definition_02",
        "demo_row_hold_03",
    }
    assert {row["row_role"] for row in rows} == {
        "correct_tool_call",
        "no_call_restraint",
        "anti_substitution",
    }

    call_ids: set[str] = set()
    output_records: list[dict] = []

    for row in rows:
        assert row["execution_status"] == "synthetic_not_executed"
        assert row["source_fields"]["row_id"] == row["row_id"]
        assert row["source_fields"]["row_role"] == row["row_role"]
        assert row["expected_assistant_action"]

        assistant_message = row["assistant_message"]
        dataset_messages = row["dataset_row"]["messages"]
        assert isinstance(dataset_messages, list)
        assert len(dataset_messages) == 3
        assert [message["role"] for message in dataset_messages] == ["system", "user", "assistant"]
        assert dataset_messages[0]["content"] == row["source_fields"]["system_content"]
        assert dataset_messages[1]["content"] == row["source_fields"]["user_content"]
        assert dataset_messages[2] == assistant_message
        assert row["source_fields"]["assistant_message"] == assistant_message
        assert row["source_fields"]["system_content"] == dataset_messages[0]["content"]

        if row["row_role"] == "no_call_restraint":
            assert set(assistant_message.keys()) == {"role", "content"}
            assert assistant_message["content"]
            assert "tool_calls" not in assistant_message
            assert row["dataset_row"]["metadata"]["source_case_id"] == row["row_id"]
            assert row["dataset_row"]["metadata"]["row_role"] == row["row_role"]
            assert row["dataset_row"]["metadata"]["expected_tool"] is False
            assert row["dataset_row"]["metadata"]["expected_no_call"] is True
            assert "tool" not in row["dataset_row"]["metadata"]
            assert "prompt_visible_arguments" not in row["dataset_row"]["metadata"]
        else:
            assert set(assistant_message.keys()) == {"role", "tool_calls"}
            assert isinstance(assistant_message["tool_calls"], list)
            assert len(assistant_message["tool_calls"]) == 1
            call = assistant_message["tool_calls"][0]
            assert call["type"] == "function"
            assert call["id"] in {"call_demo_availability_01", "call_demo_hold_03"}
            assert call["id"] not in call_ids
            call_ids.add(call["id"])

            expected_args_by_row = {
                "demo_row_availability_01": {"branch_code": "central-01", "item_id": "hv-item-204"},
                "demo_row_hold_03": {
                    "branch_code": "central-01",
                    "item_id": "hv-item-204",
                    "patron_ref": "patron-demo-17",
                },
            }
            expected_tool_name_by_row = {
                "demo_row_availability_01": "get_availability",
                "demo_row_hold_03": "place_hold",
            }
            expected_args = expected_args_by_row[row["row_id"]]
            expected_tool_name = expected_tool_name_by_row[row["row_id"]]
            assert call["function"]["name"] == expected_tool_name
            assert call["function"]["arguments"] == _canonical_json(expected_args)
            assert json.loads(call["function"]["arguments"]) == expected_args
            assert row["dataset_row"]["metadata"]["source_case_id"] == row["row_id"]
            assert row["dataset_row"]["metadata"]["row_role"] == row["row_role"]
            assert row["dataset_row"]["metadata"]["expected_tool"] is True
            assert row["dataset_row"]["metadata"]["expected_no_call"] is False
            assert row["dataset_row"]["metadata"]["tool"] == expected_tool_name
            assert row["dataset_row"]["metadata"]["prompt_visible_arguments"] == row["prompt_visible_arguments"]
            assert row["prompt_visible_arguments"]

        expected_prompt = _render_prompt(
            row["source_fields"]["system_content"],
            registry,
            row["source_fields"]["user_content"],
        )
        assert row["rendered_prompt"] == expected_prompt
        assert row["prompt_sha256"] == _sha256_text(expected_prompt)
        assert row["source_sha256"] == _sha256_text(_canonical_json(row["source_fields"]))

        expected_target = train_mod._serialize_assistant_target(assistant_message)
        assert row["assistant_target_text"] == expected_target
        assert row["assistant_target_sha256"] == _sha256_text(expected_target)

        if row["row_role"] == "no_call_restraint":
            assert "prompt_visible_arguments" not in row["dataset_row"]["metadata"]
        else:
            for value in row.get("prompt_visible_arguments", {}).values():
                assert value in row["rendered_prompt"]
                assert value in row["source_fields"]["user_content"]

        _assert_expected_evaluator_result(eval_mod, row, row["assistant_target_text"], row["expected_evaluator_result"])

        if row["row_role"] == "correct_tool_call":
            bad_direct = row["illustrative_bad_outputs"][0]
            _assert_expected_evaluator_result(eval_mod, row, bad_direct["serialized_output"], bad_direct["expected_evaluator_result"])

            bad_missing = row["illustrative_bad_outputs"][1]
            _assert_expected_evaluator_result(eval_mod, row, bad_missing["serialized_output"], bad_missing["expected_evaluator_result"])
        elif row["row_role"] == "anti_substitution":
            bad_wrong_tool = row["illustrative_bad_outputs"][0]
            _assert_expected_evaluator_result(eval_mod, row, bad_wrong_tool["serialized_output"], bad_wrong_tool["expected_evaluator_result"])

            bad_wrong_args = row["illustrative_bad_outputs"][1]
            _assert_expected_evaluator_result(eval_mod, row, bad_wrong_args["serialized_output"], bad_wrong_args["expected_evaluator_result"])
        else:
            assert row["expected_evaluator_result"]["label"] == "refusal_expected"
            assert row["expected_evaluator_result"]["exact_valid"] is False

        for output_record in _row_output_records(row):
            if output_record["output_kind"] == "scored_assistant_target":
                assert "execution_status" not in output_record
                assert output_record["serialized_output"] == row["assistant_target_text"]
                assert output_record["output_sha256"] == row["assistant_target_sha256"]
            else:
                assert output_record["execution_status"] == "synthetic_not_executed"
                assert output_record["output_sha256"] == _sha256_text(output_record["serialized_output"])
            output_records.append(output_record)

            mapped = row_output_map[output_record["output_id"]]
            assert mapped["row_id"] == output_record["row_id"]
            assert mapped["output_id"] == output_record["output_id"]
            assert mapped["output_kind"] == output_record["output_kind"]
            assert mapped["output_sha256"] == output_record["output_sha256"]

        prompt_entry = row_prompt_map[row["row_id"]]
        assert {"row_id", "prompt_sha256"} == set(prompt_entry.keys())
        assert prompt_entry["row_id"] == row["row_id"]
        assert prompt_entry["prompt_sha256"] == row["prompt_sha256"]

    assert call_ids == {"call_demo_availability_01", "call_demo_hold_03"}

    assert len(output_records) == 11
    assert len({record["output_id"] for record in output_records}) == 11

    output_map_ids = {entry["output_id"] for entry in fixture["row_to_output_map"]}
    assert output_map_ids == {record["output_id"] for record in output_records}
    assert len(fixture["row_to_output_map"]) == 11

    scored_target_ids = {
        "demo_row_availability_01_scored_assistant_target",
        "demo_row_definition_02_scored_assistant_target",
        "demo_row_hold_03_scored_assistant_target",
    }
    scored_target_entries = [entry for entry in fixture["row_to_output_map"] if entry["output_kind"] == "scored_assistant_target"]
    assert {entry["output_id"] for entry in scored_target_entries} == scored_target_ids
    assert len(scored_target_entries) == 3
    for entry in scored_target_entries:
        assert set(entry.keys()) == {"row_id", "output_id", "output_kind", "output_sha256"}
        row = {row["row_id"]: row for row in rows}[entry["row_id"]]
        assert entry["output_sha256"] == row["assistant_target_sha256"]

    assert fixture["rows"][1]["assistant_target_text"] == (
        "A library card identifies the borrower and allows eligible items to be borrowed or placed on hold."
    )
    assert fixture["rows"][1]["expected_evaluator_result"]["label"] == "refusal_expected"
    assert fixture["rows"][1]["expected_evaluator_result"]["exact_valid"] is False
    assert fixture["rows"][0]["expected_evaluator_result"]["label"] == "exact_valid"
    assert fixture["rows"][2]["expected_evaluator_result"]["label"] == "exact_valid"
    assert fixture["rows"][1]["source_fields"]["system_content"] == fixture["rows"][1]["dataset_row"]["messages"][0]["content"]


def validate_documents_links_contamination_boundaries_and_public_portability():
    fixture = _load_fixture()
    doc_text = _read_text(DOC_PATH)
    readme_text = _read_text(README_PATH)
    start_here_text = _read_text(START_HERE_PATH)
    fixture_text = _read_text(FIXTURE_PATH)
    manifest_text = _read_text(REPO_ROOT / "evals" / "canonical_eval_manifest_v1.json")
    training_history_text = _read_text(REPO_ROOT / "docs" / "current" / "status" / "TRAINING_RUN_HISTORY.md")
    pub_ref_text = _read_text(REPO_ROOT / "docs" / "publication" / "public_reference_dispositions.json")

    assert "[public_sanitized_tool_call_worked_example.json](./public_sanitized_tool_call_worked_example.json)" in doc_text
    assert "public_sanitized_tool_call_worked_example.md" in readme_text
    assert "public_sanitized_tool_call_worked_example.md" in start_here_text

    for text in (doc_text, readme_text, start_here_text):
        _assert_no_sensitive_markers(text)
        _assert_only_expected_performance_language(text)

    for text in (fixture_text, doc_text):
        _assert_no_sensitive_markers(text)
        _assert_only_expected_performance_language(text)

    for blocked_text in (manifest_text, training_history_text, pub_ref_text):
        assert "docs/framework/examples/public_sanitized_tool_call_worked_example" not in blocked_text
        assert "harborview-public-sanitized-tool-call-example-v1" not in blocked_text
        assert "demo_row_availability_01" not in blocked_text

    assert fixture["canonical_manifest_exclusion"]["status"] == "excluded"
    assert fixture["canonical_manifest_exclusion"]["checked_surfaces"] == [
        "evals/canonical_eval_manifest_v1.json",
        "docs/current/status/TRAINING_RUN_HISTORY.md",
        "docs/publication/public_reference_dispositions.json",
    ]

    for relative_path in PUBLIC_PORTABLE_SURFACES:
        assert (REPO_ROOT / relative_path).exists()
    for relative_path, needle in (
        ("scripts/train_lora_sft.py", "def _serialize_assistant_target"),
        ("scripts/eval_canonical_manifest.py", "def _classify"),
        ("scripts/eval_canonical_manifest.py", "def _build_preaggregation_labels"),
        ("scripts/repo_paths.py", "def resolve_repo_root"),
    ):
        text = _read_text(REPO_ROOT / relative_path)
        assert needle in text
    assert len(PUBLIC_PORTABLE_SURFACES) == 8


def validate_fixture_identity_and_join_integrity():
    fixture = _load_fixture()
    row_map = {row["row_id"]: row for row in fixture["rows"]}
    prompt_map = {entry["row_id"]: entry["prompt_sha256"] for entry in fixture["row_to_prompt_map"]}
    output_map = {entry["output_id"]: entry for entry in fixture["row_to_output_map"]}

    assert len(prompt_map) == 3
    assert set(prompt_map) == set(row_map)
    assert len(output_map) == 11

    for row_id, row in row_map.items():
        assert prompt_map[row_id] == row["prompt_sha256"]

    row_output_ids: set[str] = set()
    for row in fixture["rows"]:
        for output_record in _row_output_records(row):
            assert output_record["output_id"] not in row_output_ids
            row_output_ids.add(output_record["output_id"])
            assert output_map[output_record["output_id"]]["row_id"] == row["row_id"]
            assert output_map[output_record["output_id"]]["output_sha256"] == output_record["output_sha256"]

    assert len(row_output_ids) == 11


def test_fixture_contract_and_canonical_evaluator_reuse():
    validate_fixture_contract_and_canonical_evaluator_reuse()


def test_documents_links_contamination_boundaries_and_public_portability():
    validate_documents_links_contamination_boundaries_and_public_portability()


def test_fixture_identity_and_join_integrity():
    validate_fixture_identity_and_join_integrity()
