#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class EncodedExample:
    input_ids: list[int]
    labels: list[int]
    attention_mask: list[int]
    audit: dict[str, Any]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _canonical_json_text(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _find_manifest_for_config(repo_root: Path, config_path: Path) -> Path | None:
    manifests_dir = repo_root / "manifests" / "runs"
    if not manifests_dir.exists():
        return None
    config_resolved = config_path.resolve()
    for cand in sorted(manifests_dir.glob("*.json")):
        try:
            obj = _load_json(cand)
        except Exception:
            continue
        mp = obj.get("config_path")
        if not isinstance(mp, str):
            continue
        try:
            if Path(mp).resolve() == config_resolved:
                return cand
        except Exception:
            continue
    return None


def _resolve_run_gate(config: dict[str, Any], manifest: dict[str, Any] | None) -> tuple[bool, dict[str, Any]]:
    safety = config.get("safety", {}) if isinstance(config.get("safety"), dict) else {}
    requires_manual = bool(safety.get("requires_manual_review", False))
    cfg_approved = bool(safety.get("approved_to_run", False))
    man_approved = False
    if isinstance(manifest, dict):
        review_gate = manifest.get("review_gate", {})
        if isinstance(review_gate, dict):
            man_approved = bool(review_gate.get("approved_to_run", False))
    approved = (not requires_manual) or cfg_approved or man_approved
    return approved, {
        "requires_manual_review": requires_manual,
        "config_approved_to_run": cfg_approved,
        "manifest_approved_to_run": man_approved,
    }


def _validate_dataset_row_shape(row: dict[str, Any], row_idx: int) -> None:
    msgs = row.get("messages")
    if not isinstance(msgs, list) or len(msgs) < 3:
        raise RuntimeError(f"row {row_idx}: messages missing/short")
    if msgs[0].get("role") != "system":
        raise RuntimeError(f"row {row_idx}: message[0] must be system")
    if msgs[1].get("role") != "user":
        raise RuntimeError(f"row {row_idx}: message[1] must be user")
    if msgs[2].get("role") != "assistant":
        raise RuntimeError(f"row {row_idx}: message[2] must be assistant")
    assistant = msgs[2]
    tc = assistant.get("tool_calls")
    content = assistant.get("content")
    has_tool_target = isinstance(tc, list) and len(tc) >= 1
    has_text_target = isinstance(content, str) and bool(content.strip())
    if not has_tool_target and not has_text_target:
        raise RuntimeError(f"row {row_idx}: assistant target missing (tool_calls or content)")


def _serialize_assistant_target(assistant_msg: dict[str, Any]) -> str:
    # Support both tool-call JSON targets (Stage B) and plain assistant text targets (Stage A).
    tool_calls = assistant_msg.get("tool_calls")
    if isinstance(tool_calls, list) and tool_calls:
        normalized_calls: list[dict[str, Any]] = []
        for call in tool_calls:
            if not isinstance(call, dict):
                continue
            fn = call.get("function")
            if not isinstance(fn, dict):
                continue
            name = fn.get("name")
            if not isinstance(name, str) or not name.strip():
                continue
            raw_args = fn.get("arguments")
            parsed_args: Any = raw_args
            if isinstance(raw_args, str):
                try:
                    parsed_args = json.loads(raw_args)
                except Exception:
                    parsed_args = raw_args
            normalized_calls.append(
                {
                    "type": "function",
                    "function": {
                        "name": name.strip(),
                        "arguments": parsed_args,
                    },
                }
            )
        if not normalized_calls:
            raise RuntimeError("assistant target tool_calls malformed")
        payload = {"tool_calls": normalized_calls}
        return _canonical_json_text(payload)

    content = assistant_msg.get("content")
    if isinstance(content, str) and content.strip():
        return content

    raise RuntimeError("assistant target missing tool_calls/content")


def _default_prompt_template_cfg() -> dict[str, Any]:
    return {
        "mode": "tokenizer_chat_template",
        "fallback_mode": "fail_fast",
        "custom_template_name": None,
        "allow_custom_fallback": False,
    }


def _resolve_prompt_template_cfg(config: dict[str, Any]) -> dict[str, Any]:
    base = _default_prompt_template_cfg()
    user = config.get("prompt_template", {})
    if isinstance(user, dict):
        base.update(user)

    mode = str(base.get("mode", "tokenizer_chat_template"))
    if mode not in {"tokenizer_chat_template", "custom"}:
        raise RuntimeError(f"prompt_template.mode unsupported: {mode}")

    fallback_mode = str(base.get("fallback_mode", "fail_fast"))
    if fallback_mode not in {"fail_fast", "custom"}:
        raise RuntimeError(f"prompt_template.fallback_mode unsupported: {fallback_mode}")

    allow_custom_fallback = bool(base.get("allow_custom_fallback", False))
    custom_template_name = base.get("custom_template_name")
    if custom_template_name is not None:
        custom_template_name = str(custom_template_name)

    return {
        "mode": mode,
        "fallback_mode": fallback_mode,
        "custom_template_name": custom_template_name,
        "allow_custom_fallback": allow_custom_fallback,
    }


def _render_custom_prompt_prefix(system_text: str, user_text: str, custom_template_name: str | None) -> str:
    name = custom_template_name or "generic_roles_v1"
    if name == "generic_roles_v1":
        # Model-agnostic fallback template (no model-specific control tokens).
        return f"[SYSTEM]\n{system_text}\n[USER]\n{user_text}\n[ASSISTANT]\n"
    raise RuntimeError(f"unsupported custom_template_name: {name}")


def _render_prompt_prefix(
    system_text: str,
    user_text: str,
    tokenizer: Any,
    prompt_template_cfg: dict[str, Any],
    row_idx: int,
) -> tuple[str, dict[str, Any]]:
    mode = str(prompt_template_cfg["mode"])
    fallback_mode = str(prompt_template_cfg["fallback_mode"])
    allow_custom_fallback = bool(prompt_template_cfg["allow_custom_fallback"])
    custom_template_name = prompt_template_cfg.get("custom_template_name")

    if mode == "custom":
        if not custom_template_name:
            raise RuntimeError(
                "prompt_template.mode=custom requires prompt_template.custom_template_name"
            )
        text = _render_custom_prompt_prefix(system_text, user_text, custom_template_name)
        return text, {
            "prompt_template_mode": mode,
            "fallback_used": False,
            "custom_template_name": custom_template_name,
        }

    # mode == tokenizer_chat_template
    if not hasattr(tokenizer, "apply_chat_template"):
        missing_reason = "tokenizer.apply_chat_template missing"
    elif not getattr(tokenizer, "chat_template", None):
        missing_reason = "tokenizer.chat_template missing"
    else:
        missing_reason = ""

    if not missing_reason:
        messages = [
            {"role": "system", "content": system_text},
            {"role": "user", "content": user_text},
        ]
        try:
            text = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )
        except Exception as exc:
            missing_reason = f"apply_chat_template failed: {exc}"
        else:
            if not isinstance(text, str) or not text:
                missing_reason = "apply_chat_template returned empty/non-string"
            else:
                return text, {
                    "prompt_template_mode": mode,
                    "fallback_used": False,
                    "custom_template_name": custom_template_name,
                }

    can_custom_fallback = (
        fallback_mode == "custom"
        and allow_custom_fallback
        and bool(custom_template_name)
    )
    if not can_custom_fallback:
        raise RuntimeError(
            f"row {row_idx}: chat template unavailable ({missing_reason}); "
            "fail-fast per prompt_template policy"
        )

    text = _render_custom_prompt_prefix(system_text, user_text, custom_template_name)
    return text, {
        "prompt_template_mode": mode,
        "fallback_used": True,
        "custom_template_name": custom_template_name,
    }


def _encode_with_explicit_masking(
    row: dict[str, Any],
    row_idx: int,
    tokenizer: Any,
    max_seq_length: int,
    prompt_template_cfg: dict[str, Any] | None = None,
) -> EncodedExample:
    _validate_dataset_row_shape(row, row_idx)
    msgs = row["messages"]
    system_text = str(msgs[0].get("content") or "")
    user_text = str(msgs[1].get("content") or "")
    assistant_msg = msgs[2]
    assistant_target_text = _serialize_assistant_target(assistant_msg)

    pt_cfg = prompt_template_cfg or _default_prompt_template_cfg()
    prefix_text, prefix_meta = _render_prompt_prefix(
        system_text=system_text,
        user_text=user_text,
        tokenizer=tokenizer,
        prompt_template_cfg=pt_cfg,
        row_idx=row_idx,
    )

    prefix_ids = tokenizer.encode(prefix_text, add_special_tokens=False)
    target_ids = tokenizer.encode(assistant_target_text, add_special_tokens=False)
    if len(target_ids) == 0:
        raise RuntimeError(f"row {row_idx}: empty assistant target token span")

    # In tokenizer_chat_template mode, do not prepend BOS manually.
    # The tokenizer template already owns prefix serialization.
    manual_bos_allowed = prefix_meta["prompt_template_mode"] != "tokenizer_chat_template"
    bos: list[int] = []
    if manual_bos_allowed and getattr(tokenizer, "bos_token_id", None) is not None:
        bos = [int(tokenizer.bos_token_id)]
    manual_bos_added = bool(bos)

    eos: list[int] = []
    if getattr(tokenizer, "eos_token_id", None) is not None:
        eos = [int(tokenizer.eos_token_id)]
    eos_appended = bool(eos)

    input_ids = bos + prefix_ids + target_ids + eos
    if len(input_ids) > max_seq_length:
        raise RuntimeError(
            f"row {row_idx}: sequence length {len(input_ids)} exceeds max_seq_length={max_seq_length}; "
            "increase max_seq_length or shorten prompts."
        )

    labels = ([-100] * (len(bos) + len(prefix_ids))) + target_ids + (eos if eos else [])
    if len(labels) != len(input_ids):
        raise RuntimeError(f"row {row_idx}: label/input length mismatch")

    supervised_ids = [tid for tid, lab in zip(input_ids, labels) if lab != -100]
    expected_supervised = target_ids + (eos if eos else [])
    if supervised_ids != expected_supervised:
        raise RuntimeError(f"row {row_idx}: supervised span verification failed")

    decoded_supervised = tokenizer.decode(supervised_ids, skip_special_tokens=False)
    decoded_expected = tokenizer.decode(expected_supervised, skip_special_tokens=False)
    if decoded_supervised != decoded_expected:
        raise RuntimeError(f"row {row_idx}: decoded supervised span mismatch")
    decoded_prefix_tail = tokenizer.decode(prefix_ids[-128:], skip_special_tokens=False) if prefix_ids else ""

    audit = {
        "row_index_1based": row_idx,
        "input_token_count": len(input_ids),
        "supervised_label_token_count": len(supervised_ids),
        "masked_token_count": len(input_ids) - len(supervised_ids),
        "first_input_token_id": input_ids[0] if input_ids else None,
        "tokenizer_bos_token_id": getattr(tokenizer, "bos_token_id", None),
        "tokenizer_eos_token_id": getattr(tokenizer, "eos_token_id", None),
        "manual_bos_added": manual_bos_added,
        "eos_appended": eos_appended,
        "prompt_template_mode": prefix_meta["prompt_template_mode"],
        "fallback_used": bool(prefix_meta["fallback_used"]),
        "custom_template_name": prefix_meta.get("custom_template_name"),
        "decoded_prompt_prefix_tail": decoded_prefix_tail,
        "decoded_supervised_target_text": decoded_supervised,
        "source_case_id": (row.get("metadata") or {}).get("source_case_id")
        or (row.get("metadata") or {}).get("case_id"),
        "tool": ((row.get("metadata") or {}).get("tool") or ""),
    }
    return EncodedExample(
        input_ids=input_ids,
        labels=labels,
        attention_mask=[1] * len(input_ids),
        audit=audit,
    )


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


class _TokenizedDataset:
    def __init__(self, items: list[EncodedExample]) -> None:
        self.items = items

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, idx: int) -> dict[str, Any]:
        item = self.items[idx]
        return {
            "input_ids": item.input_ids,
            "labels": item.labels,
            "attention_mask": item.attention_mask,
        }


class _PadCollator:
    def __init__(self, pad_token_id: int) -> None:
        self.pad_token_id = int(pad_token_id)

    def __call__(self, batch: list[dict[str, Any]]) -> dict[str, torch.Tensor]:
        import torch

        max_len = max(len(x["input_ids"]) for x in batch)
        input_ids, labels, attention = [], [], []
        for x in batch:
            n = len(x["input_ids"])
            pad_n = max_len - n
            input_ids.append(x["input_ids"] + [self.pad_token_id] * pad_n)
            labels.append(x["labels"] + [-100] * pad_n)
            attention.append(x["attention_mask"] + [0] * pad_n)
        return {
            "input_ids": torch.tensor(input_ids, dtype=torch.long),
            "labels": torch.tensor(labels, dtype=torch.long),
            "attention_mask": torch.tensor(attention, dtype=torch.long),
        }


def _build_masking_audit(train_items: list[EncodedExample], val_items: list[EncodedExample]) -> dict[str, Any]:
    return {
        "train_first_3": [x.audit for x in train_items[:3]],
        "val_first_2": [x.audit for x in val_items[:2]],
    }


def _resolve_dtype(name: str):
    import torch

    n = str(name).lower()
    if n in {"bf16", "bfloat16"}:
        return torch.bfloat16
    if n in {"fp16", "float16"}:
        return torch.float16
    if n in {"fp32", "float32"}:
        return torch.float32
    return torch.bfloat16


def _prepare_output_dirs(config: dict[str, Any], run_root: Path) -> None:
    outputs = config.get("outputs", {})
    allow_overwrite = bool(outputs.get("allow_overwrite_run_root", False))

    adapter_dir = Path(outputs["adapter_output_dir"])
    logs_dir = Path(outputs["logs_dir"])
    checkpoints_dir = run_root / "checkpoints"
    forbidden_files = [
        run_root / "resolved_config.json",
        run_root / "masking_audit.json",
        run_root / "training_summary.json",
    ]

    if run_root.exists() and not allow_overwrite:
        # Refuse overwrite if any known training artifact already exists.
        artifact_hits: list[str] = []
        for p in [adapter_dir, logs_dir, checkpoints_dir]:
            if p.exists():
                artifact_hits.append(str(p))
        for p in forbidden_files:
            if p.exists():
                artifact_hits.append(str(p))
        if artifact_hits:
            raise RuntimeError(
                "run_root contains existing training artifacts; refusing overwrite unless "
                f"outputs.allow_overwrite_run_root=true. hits={artifact_hits}"
            )

        # Existing run_root is allowed only when it contains preflight artifacts exclusively.
        non_preflight_entries = [p for p in run_root.iterdir() if p.name != "preflight"]
        if non_preflight_entries:
            raise RuntimeError(
                "run_root exists with non-preflight contents; refusing reuse unless "
                f"outputs.allow_overwrite_run_root=true. entries={[str(p) for p in non_preflight_entries]}"
            )

    run_root.mkdir(parents=True, exist_ok=True)
    adapter_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _validate_loss_requirements(config: dict[str, Any]) -> None:
    loss = config.get("loss", {})
    requested = bool(loss.get("assistant_completion_only_requested", False))
    if not requested:
        return
    required_flags = [
        bool(loss.get("assistant_only_loss", False)),
        bool(loss.get("completion_only_loss", False)),
        bool(loss.get("train_on_inputs", True)) is False,
    ]
    if not all(required_flags):
        raise RuntimeError(
            "assistant_completion_only_requested=true but loss flags are inconsistent; "
            "require assistant_only_loss=true, completion_only_loss=true, train_on_inputs=false"
        )
    if str(loss.get("fallback_behavior_if_not_supported", "")).lower() != "fail_fast":
        raise RuntimeError(
            "assistant-only masking requested but fallback_behavior_if_not_supported is not fail_fast"
        )


def _load_tokenizer_only(config: dict[str, Any]):
    from transformers import AutoTokenizer

    model_cfg = config["model"]
    tok = AutoTokenizer.from_pretrained(
        model_cfg["tokenizer_name_or_path"],
        trust_remote_code=bool(model_cfg.get("trust_remote_code", False)),
    )
    if tok.pad_token_id is None:
        if tok.eos_token_id is None:
            raise RuntimeError("tokenizer has neither pad_token_id nor eos_token_id")
        tok.pad_token = tok.eos_token
    return tok


def _load_model_and_tokenizer(config: dict[str, Any]):
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from transformers import AutoModelForCausalLM, BitsAndBytesConfig

    model_cfg = config["model"]
    quant_cfg = config.get("quantization", {})
    lora_cfg = config["lora"]

    tok = _load_tokenizer_only(config)

    model_kwargs: dict[str, Any] = {
        "trust_remote_code": bool(model_cfg.get("trust_remote_code", False)),
        "torch_dtype": _resolve_dtype(model_cfg.get("torch_dtype", "bfloat16")),
        "device_map": "auto",
    }

    if bool(lora_cfg.get("use_qlora", False)) and bool(quant_cfg.get("load_in_4bit", False)):
        bnb_cfg = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type=str(quant_cfg.get("bnb_4bit_quant_type", "nf4")),
            bnb_4bit_use_double_quant=bool(quant_cfg.get("bnb_4bit_use_double_quant", True)),
            bnb_4bit_compute_dtype=_resolve_dtype(quant_cfg.get("bnb_4bit_compute_dtype", "bfloat16")),
        )
        model_kwargs["quantization_config"] = bnb_cfg

    model = AutoModelForCausalLM.from_pretrained(
        model_cfg["model_name_or_path"],
        **model_kwargs,
    )

    if bool(lora_cfg.get("use_qlora", False)):
        model = prepare_model_for_kbit_training(model)

    peft_cfg = LoraConfig(
        r=int(lora_cfg["r"]),
        lora_alpha=int(lora_cfg["alpha"]),
        lora_dropout=float(lora_cfg["dropout"]),
        bias=str(lora_cfg.get("bias", "none")),
        task_type=str(lora_cfg.get("task_type", "CAUSAL_LM")),
        target_modules=list(lora_cfg.get("target_modules", [])),
    )
    model = get_peft_model(model, peft_cfg)
    model.print_trainable_parameters()
    return model, tok


def _run_masking_audit_only(
    *,
    config: dict[str, Any],
    config_path: Path,
    manifest_path: Path | None,
    gate_info: dict[str, Any] | None,
    prompt_template_cfg: dict[str, Any],
) -> int:
    dataset_cfg = config.get("dataset", {})
    if dataset_cfg.get("format") != "openai_messages_with_assistant_tool_calls":
        raise RuntimeError(
            f"Unsupported dataset.format={dataset_cfg.get('format')}; "
            "expected openai_messages_with_assistant_tool_calls"
        )
    max_seq_length = int(dataset_cfg.get("max_seq_length", 2048))
    train_rows = _load_jsonl(Path(dataset_cfg["train_jsonl"]))
    val_rows = _load_jsonl(Path(dataset_cfg["val_jsonl"]))
    if not train_rows or not val_rows:
        raise RuntimeError("train/val datasets must be non-empty")

    tokenizer = _load_tokenizer_only(config)

    train_items = [
        _encode_with_explicit_masking(
            row,
            i + 1,
            tokenizer,
            max_seq_length,
            prompt_template_cfg=prompt_template_cfg,
        )
        for i, row in enumerate(train_rows[:3])
    ]
    val_items = [
        _encode_with_explicit_masking(
            row,
            i + 1,
            tokenizer,
            max_seq_length,
            prompt_template_cfg=prompt_template_cfg,
        )
        for i, row in enumerate(val_rows[:2])
    ]
    masking_audit = _build_masking_audit(train_items, val_items)

    run_root = Path(config["outputs"]["run_root"])
    audit_out = Path(config.get("outputs", {}).get("masking_audit_only_path") or (run_root / "preflight" / "masking_audit.json"))
    _write_json(audit_out, masking_audit)

    resolved = {
        "config_path": str(config_path),
        "manifest_path": str(manifest_path) if manifest_path else None,
        "approval_gate": gate_info,
        "resolved_prompt_template": prompt_template_cfg,
        "masking_audit_only": True,
    }
    _write_json(run_root / "preflight" / "resolved_config.json", resolved)

    print(json.dumps(masking_audit, indent=2, ensure_ascii=False))
    print(json.dumps({"masking_audit_path": str(audit_out)}, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="LoRA SFT trainer for assistant tool-call dataset.")
    parser.add_argument("--config", required=True, help="Path to training config JSON")
    parser.add_argument(
        "--masking-audit-only",
        action="store_true",
        help="Run tokenizer-based masking audit only; skip model load, trainer construction, and training.",
    )
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    config = _load_json(config_path)
    repo_root = Path(__file__).resolve().parents[1]
    manifest_path = _find_manifest_for_config(repo_root, config_path)
    manifest = _load_json(manifest_path) if manifest_path else None
    prompt_template_cfg = _resolve_prompt_template_cfg(config)

    approved, gate_info = _resolve_run_gate(config, manifest)

    if args.masking_audit_only:
        # Audit-only mode intentionally bypasses approval gate because it does not train.
        return _run_masking_audit_only(
            config=config,
            config_path=config_path,
            manifest_path=manifest_path,
            gate_info=gate_info,
            prompt_template_cfg=prompt_template_cfg,
        )

    if not approved:
        raise RuntimeError(
            "training blocked by approval gate; requires manual review approval in config/manifest. "
            f"gate_info={gate_info}"
        )

    _validate_loss_requirements(config)

    dataset_cfg = config.get("dataset", {})
    if dataset_cfg.get("format") != "openai_messages_with_assistant_tool_calls":
        raise RuntimeError(
            f"Unsupported dataset.format={dataset_cfg.get('format')}; "
            "expected openai_messages_with_assistant_tool_calls"
        )

    run_root = Path(config["outputs"]["run_root"])
    _prepare_output_dirs(config, run_root)

    # Resolved config artifact
    resolved_config = {
        "config_path": str(config_path),
        "manifest_path": str(manifest_path) if manifest_path else None,
        "approval_gate": gate_info,
        "resolved_prompt_template": prompt_template_cfg,
        "config": config,
    }
    _write_json(run_root / "resolved_config.json", resolved_config)

    train_rows = _load_jsonl(Path(dataset_cfg["train_jsonl"]))
    val_rows = _load_jsonl(Path(dataset_cfg["val_jsonl"]))
    if not train_rows or not val_rows:
        raise RuntimeError("train/val datasets must be non-empty")

    # Load model/tokenizer and build datasets with explicit masking
    model, tokenizer = _load_model_and_tokenizer(config)
    max_seq_length = int(dataset_cfg.get("max_seq_length", 2048))

    train_items = [
        _encode_with_explicit_masking(
            row,
            i + 1,
            tokenizer,
            max_seq_length,
            prompt_template_cfg=prompt_template_cfg,
        )
        for i, row in enumerate(train_rows)
    ]
    val_items = [
        _encode_with_explicit_masking(
            row,
            i + 1,
            tokenizer,
            max_seq_length,
            prompt_template_cfg=prompt_template_cfg,
        )
        for i, row in enumerate(val_rows)
    ]

    masking_audit = _build_masking_audit(train_items, val_items)
    _write_json(run_root / "masking_audit.json", masking_audit)
    print(json.dumps(masking_audit, indent=2, ensure_ascii=False))

    train_ds = _TokenizedDataset(train_items)
    val_ds = _TokenizedDataset(val_items)
    pad_token_id = int(tokenizer.pad_token_id)
    collator = _PadCollator(pad_token_id=pad_token_id)

    # Lazy import heavy trainer classes
    from transformers import Trainer, TrainingArguments

    opt = config.get("optimization", {})
    logs_dir = Path(config["outputs"]["logs_dir"])
    output_dir = run_root / "checkpoints"
    output_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=float(opt.get("num_train_epochs", 1)),
        per_device_train_batch_size=int(opt.get("per_device_train_batch_size", 1)),
        per_device_eval_batch_size=int(opt.get("per_device_eval_batch_size", 1)),
        gradient_accumulation_steps=int(opt.get("gradient_accumulation_steps", 1)),
        learning_rate=float(opt.get("learning_rate", 5e-5)),
        lr_scheduler_type=str(opt.get("lr_scheduler_type", "cosine")),
        warmup_ratio=float(opt.get("warmup_ratio", 0.0)),
        weight_decay=float(opt.get("weight_decay", 0.0)),
        max_grad_norm=float(opt.get("max_grad_norm", 1.0)),
        logging_steps=int(opt.get("logging_steps", 10)),
        eval_strategy=str(opt.get("eval_strategy", "steps")),
        eval_steps=int(opt.get("eval_steps", 50)),
        save_strategy=str(opt.get("save_strategy", "steps")),
        save_steps=int(opt.get("save_steps", 50)),
        save_total_limit=int(opt.get("save_total_limit", 2)),
        bf16=bool(opt.get("bf16", True)),
        fp16=bool(opt.get("fp16", False)),
        gradient_checkpointing=bool(opt.get("gradient_checkpointing", True)),
        optim=str(opt.get("optim", "paged_adamw_8bit")),
        seed=int(opt.get("seed", 42)),
        report_to=[],
        logging_dir=str(logs_dir),
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        data_collator=collator,
        tokenizer=tokenizer,
    )

    # Train and save adapter only (no merge).
    train_result = trainer.train()
    eval_metrics = trainer.evaluate()

    adapter_out = Path(config["outputs"]["adapter_output_dir"])
    adapter_out.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(str(adapter_out))
    tokenizer.save_pretrained(str(adapter_out))

    summary = {
        "status": "completed",
        "train_rows": len(train_rows),
        "val_rows": len(val_rows),
        "run_root": str(run_root),
        "adapter_output_dir": str(adapter_out),
        "train_metrics": dict(train_result.metrics),
        "eval_metrics": dict(eval_metrics),
        "masking_audit_path": str(run_root / "masking_audit.json"),
        "resolved_config_path": str(run_root / "resolved_config.json"),
    }
    _write_json(run_root / "training_summary.json", summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    raise SystemExit(main())
