import importlib.util
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from repo_paths import resolve_script_path


SCRIPT_PATH = resolve_script_path("stage_c_e1_prompt_trace_evidence_creation")
EVAL_SCRIPT_PATH = resolve_script_path("eval_canonical_manifest")


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, str(path))
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_script_module():
    return _load_module(SCRIPT_PATH, "stage_c_e1_prompt_trace_evidence_creation")


def _load_eval_module():
    return _load_module(EVAL_SCRIPT_PATH, "eval_canonical_manifest")


def _write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


class DummyTokenizer:
    def __init__(self, *, has_chat_template: bool = True):
        self.chat_template = "{{dummy}}" if has_chat_template else None

    def apply_chat_template(self, messages, tokenize=False, add_generation_prompt=False):
        assert tokenize is False
        rendered = ""
        for message in messages:
            rendered += f"[{message['role'].upper()}]\n{message['content']}\n"
        if add_generation_prompt:
            rendered += "[ASSISTANT]\n"
        return rendered

    def encode(self, text, add_special_tokens=False):
        assert add_special_tokens is False
        return [ord(ch) for ch in text]


def _trace_row(system_text: str, user_text: str, assistant_payload, source_case_id: str):
    row = {
        "messages": [
            {"role": "system", "content": system_text},
            {"role": "user", "content": user_text},
            {"role": "assistant", **assistant_payload},
        ],
        "metadata": {"source_case_id": source_case_id},
    }
    return row


def test_prompt_trace_bundle_writes_exact_prompt_snapshots(tmp_path):
    script_mod = _load_script_module()
    eval_mod = _load_eval_module()

    eval_mod._infer = lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("_infer must not be called"))
    eval_mod._eval_one_side = lambda *args, **kwargs: (_ for _ in ()).throw(
        AssertionError("_eval_one_side must not be called")
    )

    manifest_path = tmp_path / "canonical_eval_manifest_v1.json"
    heldout_path = tmp_path / "heldout_validation.jsonl"
    direct_path = tmp_path / "direct_answer.jsonl"

    heldout_rows = [
        _trace_row(
            "sys 1",
            "user 1",
            {
                "tool_calls": [
                    {
                        "id": "call_1",
                        "type": "function",
                        "function": {"name": "rg_search", "arguments": "{}"},
                    }
                ]
            },
            "dummy_0",
        ),
        _trace_row(
            "sys 2",
            "user 2",
            {
                "tool_calls": [
                    {
                        "id": "call_1",
                        "type": "function",
                        "function": {"name": "rg_search", "arguments": "{}"},
                    }
                ]
            },
            "p0_rg_search_4",
        ),
    ]
    direct_rows = [
        _trace_row("ctrl sys", "ctrl user", {"content": "direct answer"}, "da_92001"),
    ]

    heldout_path.write_text("\n".join(json.dumps(row) for row in heldout_rows) + "\n", encoding="utf-8")
    direct_path.write_text("\n".join(json.dumps(row) for row in direct_rows) + "\n", encoding="utf-8")

    manifest = {
        "manifest_version": "v1",
        "runtime": {
            "eval_schema_version": "canonical_eval_manifest_v1",
            "dataset_manifest_version": "dataset_v1_0_summary",
        },
        "tokenizer": {
            "path": "dummy-tokenizer",
            "version": "dummy-tokenizer",
            "chat_template_mode": "tokenizer_native",
            "add_generation_prompt": True,
            "allow_custom_fallback": True,
            "custom_template_name": "generic_roles_v1",
        },
        "datasets": {
            "heldout_validation": {
                "path": str(heldout_path),
                "sha256": script_mod._sha256_file(heldout_path),
                "rows": 2,
            },
            "direct_answer": {
                "path": str(direct_path),
                "sha256": script_mod._sha256_file(direct_path),
                "rows": 1,
            },
        },
        "integrity": {"prompt_contract": "tokenizer.apply_chat_template(messages, add_generation_prompt=true)"},
    }
    _write_json(manifest_path, manifest)

    tokenizer = DummyTokenizer(has_chat_template=True)
    bundle = script_mod.build_prompt_trace_bundle(
        manifest_path=manifest_path,
        out_root=tmp_path / "out",
        run_id="run1",
        selected_rows=(
            script_mod.TraceSelection(split="heldout_validation", row_index_1based=2, source_case_id="p0_rg_search_4"),
            script_mod.TraceSelection(split="direct_answer", row_index_1based=1, source_case_id="da_92001"),
        ),
        tokenizer=tokenizer,
        eval_mod=eval_mod,
    )

    bundle_root = Path(bundle["bundle_root"])
    assert bundle_root.exists()
    assert Path(bundle["manifest_path"]).exists()
    assert Path(bundle["prompt_traces_path"]).exists()
    assert Path(bundle["validation_report_path"]).exists()

    trace_rows = [
        json.loads(line)
        for line in Path(bundle["prompt_traces_path"]).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert [row["row_index_1based"] for row in trace_rows] == [2, 1]
    assert [row["source_case_id"] for row in trace_rows] == ["p0_rg_search_4", "da_92001"]
    assert all(row["render_path_used"] == "tokenizer_native" for row in trace_rows)
    assert all(row["fallback_used"] is False for row in trace_rows)

    expected_prompts = {
        "heldout_validation_2": eval_mod._build_rows(
            "heldout_validation",
            [heldout_rows[1]],
            tokenizer,
            manifest["tokenizer"],
            row_index_offset=1,
        )[0].prompt_prefix,
        "direct_answer_1": eval_mod._build_rows(
            "direct_answer",
            [direct_rows[0]],
            tokenizer,
            manifest["tokenizer"],
            row_index_offset=0,
        )[0].prompt_prefix,
    }

    for row in trace_rows:
        prompt_path = Path(row["rendered_prompt_path"])
        prompt_text = prompt_path.read_text(encoding="utf-8")
        key = "heldout_validation_2" if row["split"] == "heldout_validation" else "direct_answer_1"
        assert prompt_text == expected_prompts[key]
        assert row["rendered_prompt_sha256"] == script_mod._sha256_text(prompt_text)
        assert row["rendered_prompt_char_count"] == len(prompt_text)
        assert row["rendered_prompt_token_count"] == len(tokenizer.encode(prompt_text, add_special_tokens=False))

    manifest_out = json.loads(Path(bundle["manifest_path"]).read_text(encoding="utf-8"))
    assert manifest_out["render_only"] is True
    assert manifest_out["generation_invoked"] is False
    assert manifest_out["scoring_invoked"] is False
    assert manifest_out["detector_invoked"] is False
    assert manifest_out["selection_count"] == 2
    assert manifest_out["selected_rows"][0]["trace_id"] == "heldout_validation:2:p0_rg_search_4"

    validation_out = json.loads(Path(bundle["validation_report_path"]).read_text(encoding="utf-8"))
    assert validation_out["overall_status"] == "pass"
    assert all(check["status"] == "pass" for check in validation_out["checks"])


def test_build_rows_records_fallback_metadata_when_chat_template_missing():
    eval_mod = _load_eval_module()
    tokenizer = DummyTokenizer(has_chat_template=False)
    row = {
        "messages": [
            {"role": "system", "content": "sys"},
            {"role": "user", "content": "user"},
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": "call_1",
                        "type": "function",
                        "function": {"name": "rg_search", "arguments": "{}"},
                    }
                ],
            },
        ],
        "metadata": {"source_case_id": "p0_rg_search_4"},
    }

    built = eval_mod._build_rows(
        "heldout_validation",
        [row],
        tokenizer,
        {
            "chat_template_mode": "tokenizer_native",
            "allow_custom_fallback": True,
            "custom_template_name": "generic_roles_v1",
        },
        row_index_offset=1,
    )[0]

    assert built.row_index_1based == 2
    assert built.render_path_used == "generic_roles_v1_fallback"
    assert built.fallback_used is True
    assert built.custom_template_name == "generic_roles_v1"
