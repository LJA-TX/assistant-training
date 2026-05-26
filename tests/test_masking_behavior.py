import importlib.util
import json
import sys
from pathlib import Path


SCRIPT_PATH = Path("/opt/ai-stack/assistant-training/scripts/train_lora_sft.py")


def _load_module():
    spec = importlib.util.spec_from_file_location("train_lora_sft", str(SCRIPT_PATH))
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


class DummyTokenizer:
    def __init__(self, has_chat_template=True):
        self.bos_token_id = 1
        self.eos_token_id = 2
        self.pad_token_id = 0
        self.chat_template = "{{dummy}}" if has_chat_template else None

    def encode(self, text, add_special_tokens=False):
        # deterministic char-level tokenizer
        return [ord(ch) for ch in text]

    def decode(self, ids, skip_special_tokens=False):
        out = []
        for i in ids:
            if skip_special_tokens and i in {self.bos_token_id, self.eos_token_id, self.pad_token_id}:
                continue
            if i in {self.bos_token_id, self.eos_token_id, self.pad_token_id}:
                out.append(f"<{i}>")
            else:
                out.append(chr(i))
        return "".join(out)

    def apply_chat_template(self, messages, tokenize=False, add_generation_prompt=False):
        assert tokenize is False
        prefix = ""
        for m in messages:
            prefix += f"[{m['role'].upper()}]\\n{m['content']}\\n"
        if add_generation_prompt:
            prefix += "[ASSISTANT]\\n"
        return prefix


def _sample_row():
    return {
        "messages": [
            {"role": "system", "content": "system rule"},
            {"role": "user", "content": "do thing"},
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": "call_1",
                        "type": "function",
                        "function": {
                            "name": "list_dir",
                            "arguments": "{\"path\":\"/tmp\"}",
                        },
                    }
                ],
            },
        ],
        "metadata": {"case_id": "x1", "tool": "list_dir"},
    }


def test_explicit_masking_supervises_assistant_only():
    mod = _load_module()
    row = _sample_row()
    tok = DummyTokenizer()
    ex = mod._encode_with_explicit_masking(row, 1, tok, max_seq_length=4096)

    assert len(ex.input_ids) == len(ex.labels) == len(ex.attention_mask)
    assert any(v == -100 for v in ex.labels)
    supervised = [tid for tid, lab in zip(ex.input_ids, ex.labels) if lab != -100]
    masked = [tid for tid, lab in zip(ex.input_ids, ex.labels) if lab == -100]
    assert len(supervised) > 0
    assert len(masked) > 0
    assert ex.audit["supervised_label_token_count"] == len(supervised)
    assert ex.audit["masked_token_count"] == len(masked)

    expected_target_text = mod._serialize_assistant_target(row["messages"][2])
    decoded = ex.audit["decoded_supervised_target_text"]
    assert expected_target_text in decoded
    assert ex.audit["prompt_template_mode"] == "tokenizer_chat_template"
    assert ex.audit["fallback_used"] is False
    assert ex.audit["manual_bos_added"] is False
    assert ex.audit["first_input_token_id"] != tok.bos_token_id
    assert ex.audit["tokenizer_bos_token_id"] == tok.bos_token_id
    assert ex.audit["tokenizer_eos_token_id"] == tok.eos_token_id
    assert ex.audit["eos_appended"] is True
    assert isinstance(ex.audit["decoded_prompt_prefix_tail"], str)


def test_fail_fast_when_target_span_empty():
    mod = _load_module()
    row = {
        "messages": [
            {"role": "system", "content": "s"},
            {"role": "user", "content": "u"},
            {"role": "assistant", "tool_calls": []},
        ]
    }
    tok = DummyTokenizer(has_chat_template=True)
    try:
        mod._encode_with_explicit_masking(row, 1, tok, max_seq_length=4096)
        raise AssertionError("expected RuntimeError")
    except RuntimeError as exc:
        assert "assistant target missing" in str(exc)


def test_plain_text_assistant_target_supported():
    mod = _load_module()
    row = {
        "messages": [
            {"role": "system", "content": "s"},
            {"role": "user", "content": "u"},
            {"role": "assistant", "content": "Direct answer without tools."},
        ]
    }
    tok = DummyTokenizer(has_chat_template=True)
    ex = mod._encode_with_explicit_masking(row, 1, tok, max_seq_length=4096)
    decoded = ex.audit["decoded_supervised_target_text"]
    assert "Direct answer without tools." in decoded


def test_fail_fast_when_chat_template_missing_and_no_fallback():
    mod = _load_module()
    row = _sample_row()
    tok = DummyTokenizer(has_chat_template=False)
    try:
        mod._encode_with_explicit_masking(row, 1, tok, max_seq_length=4096)
        raise AssertionError("expected RuntimeError")
    except RuntimeError as exc:
        assert "chat template unavailable" in str(exc)


def test_custom_fallback_used_only_when_explicitly_configured():
    mod = _load_module()
    row = _sample_row()
    tok = DummyTokenizer(has_chat_template=False)
    cfg = {
        "mode": "tokenizer_chat_template",
        "fallback_mode": "custom",
        "allow_custom_fallback": True,
        "custom_template_name": "generic_roles_v1",
    }
    ex = mod._encode_with_explicit_masking(
        row,
        1,
        tok,
        max_seq_length=4096,
        prompt_template_cfg=cfg,
    )
    assert ex.audit["fallback_used"] is True
    assert ex.audit["custom_template_name"] == "generic_roles_v1"
    # tokenizer_chat_template mode still must not prepend BOS manually
    assert ex.audit["manual_bos_added"] is False

    # If custom fallback is not explicitly allowed, fail-fast.
    cfg_disallowed = {
        "mode": "tokenizer_chat_template",
        "fallback_mode": "custom",
        "allow_custom_fallback": False,
        "custom_template_name": "generic_roles_v1",
    }
    try:
        mod._encode_with_explicit_masking(
            row,
            1,
            tok,
            max_seq_length=4096,
            prompt_template_cfg=cfg_disallowed,
        )
        raise AssertionError("expected RuntimeError")
    except RuntimeError as exc:
        assert "chat template unavailable" in str(exc)


def test_masking_audit_only_does_not_load_model_or_train(tmp_path):
    mod = _load_module()
    row = _sample_row()

    train_path = tmp_path / "train.jsonl"
    val_path = tmp_path / "val.jsonl"
    train_path.write_text("\n".join(json.dumps(row) for _ in range(3)) + "\n", encoding="utf-8")
    val_path.write_text("\n".join(json.dumps(row) for _ in range(2)) + "\n", encoding="utf-8")

    config = {
        "dataset": {
            "format": "openai_messages_with_assistant_tool_calls",
            "train_jsonl": str(train_path),
            "val_jsonl": str(val_path),
            "max_seq_length": 2048,
        },
        "outputs": {
            "run_root": str(tmp_path / "run"),
            "adapter_output_dir": str(tmp_path / "run" / "adapter"),
            "logs_dir": str(tmp_path / "run" / "logs"),
        },
        "prompt_template": {
            "mode": "tokenizer_chat_template",
            "fallback_mode": "fail_fast",
        },
    }

    called = {"model_loader": 0}

    def _tok_loader(_cfg):
        return DummyTokenizer(has_chat_template=True)

    def _model_loader(_cfg):
        called["model_loader"] += 1
        raise AssertionError("model loader must not be called in masking-audit-only")

    mod._load_tokenizer_only = _tok_loader
    mod._load_model_and_tokenizer = _model_loader

    prompt_cfg = mod._resolve_prompt_template_cfg(config)
    rc = mod._run_masking_audit_only(
        config=config,
        config_path=tmp_path / "config.json",
        manifest_path=None,
        gate_info={"requires_manual_review": True},
        prompt_template_cfg=prompt_cfg,
    )
    assert rc == 0
    assert called["model_loader"] == 0
    assert (tmp_path / "run" / "preflight" / "masking_audit.json").exists()


def test_approval_gate_requires_manifest_or_config_approval():
    mod = _load_module()
    config = {"safety": {"requires_manual_review": True, "approved_to_run": False}}
    manifest = {"review_gate": {"approved_to_run": False}}
    approved, info = mod._resolve_run_gate(config, manifest)
    assert approved is False
    assert info["requires_manual_review"] is True

    manifest2 = {"review_gate": {"approved_to_run": True}}
    approved2, _ = mod._resolve_run_gate(config, manifest2)
    assert approved2 is True


def _prepare_cfg_for_output_dirs(run_root: Path) -> dict:
    return {
        "outputs": {
            "run_root": str(run_root),
            "adapter_output_dir": str(run_root / "adapter"),
            "logs_dir": str(run_root / "logs"),
            "allow_overwrite_run_root": False,
        }
    }


def test_prepare_output_dirs_allows_preflight_only_run_root(tmp_path):
    mod = _load_module()
    run_root = tmp_path / "run"
    (run_root / "preflight").mkdir(parents=True, exist_ok=True)
    (run_root / "preflight" / "masking_audit.json").write_text("{}", encoding="utf-8")
    (run_root / "preflight" / "resolved_config.json").write_text("{}", encoding="utf-8")
    cfg = _prepare_cfg_for_output_dirs(run_root)

    mod._prepare_output_dirs(cfg, run_root)

    assert (run_root / "adapter").exists()
    assert (run_root / "logs").exists()


def test_prepare_output_dirs_refuses_existing_training_artifacts(tmp_path):
    mod = _load_module()
    cases = [
        ("adapter", lambda root: (root / "adapter").mkdir(parents=True, exist_ok=True)),
        ("logs", lambda root: (root / "logs").mkdir(parents=True, exist_ok=True)),
        ("checkpoints", lambda root: (root / "checkpoints").mkdir(parents=True, exist_ok=True)),
        (
            "training_summary",
            lambda root: (root / "training_summary.json").write_text("{}", encoding="utf-8"),
        ),
    ]

    for case_name, create_artifact in cases:
        run_root = tmp_path / f"run_{case_name}"
        (run_root / "preflight").mkdir(parents=True, exist_ok=True)
        cfg = _prepare_cfg_for_output_dirs(run_root)
        create_artifact(run_root)
        try:
            mod._prepare_output_dirs(cfg, run_root)
            raise AssertionError("expected RuntimeError")
        except RuntimeError as exc:
            assert "existing training artifacts" in str(exc)
