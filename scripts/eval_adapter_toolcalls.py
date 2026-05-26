#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gc
import json
import os
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STRONG_SYSTEM_PROMPT_OVERRIDE = (
    "You are a tool-call emission model. For every request requiring a tool, output only strict JSON "
    "in this exact shape: "
    "{\"tool_calls\":[{\"function\":{\"arguments\":\"{...}\",\"name\":\"tool_name\"},\"id\":\"call_1\",\"type\":\"function\"}]}. "
    "Do not answer conversationally. Do not simulate tool results. Do not use markdown. "
    "Do not include prose before or after the JSON."
)


@dataclass
class PromptRow:
    row_index_1based: int
    source_case_id: str
    tool: str
    system_text: str
    user_text: str
    prompt_prefix: str
    expected_payload: dict[str, Any] | None
    expected_no_call: bool


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            raw = line.strip()
            if not raw:
                continue
            try:
                rows.append(json.loads(raw))
            except Exception as exc:
                raise RuntimeError(f"invalid JSONL at {path}:{line_no}: {exc}") from exc
    return rows


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _canonical_json_text(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True)


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

    custom_template_name = base.get("custom_template_name")
    if custom_template_name is not None:
        custom_template_name = str(custom_template_name)

    return {
        "mode": mode,
        "fallback_mode": fallback_mode,
        "custom_template_name": custom_template_name,
        "allow_custom_fallback": bool(base.get("allow_custom_fallback", False)),
    }


def _render_custom_prompt_prefix(system_text: str, user_text: str, custom_template_name: str | None) -> str:
    name = custom_template_name or "generic_roles_v1"
    if name == "generic_roles_v1":
        return f"[SYSTEM]\n{system_text}\n[USER]\n{user_text}\n[ASSISTANT]\n"
    raise RuntimeError(f"unsupported custom_template_name: {name}")


def _render_prompt_prefix(
    system_text: str,
    user_text: str,
    tokenizer: Any,
    prompt_template_cfg: dict[str, Any],
    row_idx: int,
) -> str:
    mode = str(prompt_template_cfg["mode"])
    fallback_mode = str(prompt_template_cfg["fallback_mode"])
    allow_custom_fallback = bool(prompt_template_cfg["allow_custom_fallback"])
    custom_template_name = prompt_template_cfg.get("custom_template_name")

    if mode == "custom":
        if not custom_template_name:
            raise RuntimeError("prompt_template.mode=custom requires prompt_template.custom_template_name")
        return _render_custom_prompt_prefix(system_text, user_text, custom_template_name)

    missing_reason = ""
    if not hasattr(tokenizer, "apply_chat_template"):
        missing_reason = "tokenizer.apply_chat_template missing"
    elif not getattr(tokenizer, "chat_template", None):
        missing_reason = "tokenizer.chat_template missing"

    if not missing_reason:
        try:
            text = tokenizer.apply_chat_template(
                [
                    {"role": "system", "content": system_text},
                    {"role": "user", "content": user_text},
                ],
                tokenize=False,
                add_generation_prompt=True,
            )
        except Exception as exc:
            missing_reason = f"apply_chat_template failed: {exc}"
        else:
            if isinstance(text, str) and text:
                return text
            missing_reason = "apply_chat_template returned empty/non-string"

    can_custom_fallback = (
        fallback_mode == "custom"
        and allow_custom_fallback
        and bool(custom_template_name)
    )
    if not can_custom_fallback:
        raise RuntimeError(
            f"row {row_idx}: chat template unavailable ({missing_reason}); fail-fast per prompt_template policy"
        )
    return _render_custom_prompt_prefix(system_text, user_text, custom_template_name)


def _validate_row(row: dict[str, Any], row_idx: int) -> None:
    msgs = row.get("messages")
    if not isinstance(msgs, list) or len(msgs) < 3:
        raise RuntimeError(f"row {row_idx}: messages missing/short")
    if msgs[0].get("role") != "system":
        raise RuntimeError(f"row {row_idx}: message[0] must be system")
    if msgs[1].get("role") != "user":
        raise RuntimeError(f"row {row_idx}: message[1] must be user")
    if msgs[2].get("role") != "assistant":
        raise RuntimeError(f"row {row_idx}: message[2] must be assistant")


def _expected_payload_from_row(row: dict[str, Any], row_idx: int) -> tuple[dict[str, Any] | None, bool]:
    assistant_msg = row["messages"][2]
    tool_calls = assistant_msg.get("tool_calls")
    if isinstance(tool_calls, list):
        if len(tool_calls) == 0:
            return {"tool_calls": []}, True
        return {"tool_calls": tool_calls}, False
    # Fallback for datasets that encode no-call in assistant content.
    if "tool_calls" not in assistant_msg:
        return None, True
    raise RuntimeError(f"row {row_idx}: assistant tool_calls shape invalid")


def _coerce_arguments(value: Any) -> tuple[Any, bool]:
    if isinstance(value, str):
        try:
            return json.loads(value), True
        except Exception:
            return value, False
    return value, True


def _extract_tool_names(payload: dict[str, Any]) -> list[str]:
    names: list[str] = []
    tool_calls = payload.get("tool_calls")
    if not isinstance(tool_calls, list):
        return names
    for call in tool_calls:
        fn = call.get("function") if isinstance(call, dict) else None
        name = fn.get("name") if isinstance(fn, dict) else None
        names.append(str(name) if isinstance(name, str) else "")
    return names


def _extract_arguments(payload: dict[str, Any]) -> tuple[list[Any], bool]:
    values: list[Any] = []
    ok = True
    tool_calls = payload.get("tool_calls")
    if not isinstance(tool_calls, list):
        return values, False
    for call in tool_calls:
        if not isinstance(call, dict):
            ok = False
            values.append(None)
            continue
        fn = call.get("function")
        if not isinstance(fn, dict) or "arguments" not in fn:
            ok = False
            values.append(None)
            continue
        parsed, parsed_ok = _coerce_arguments(fn.get("arguments"))
        ok = ok and parsed_ok
        values.append(parsed)
    return values, ok


def _validate_tool_payload_shape(payload: Any) -> tuple[bool, str]:
    if not isinstance(payload, dict):
        return False, "payload_not_object"
    if "tool_calls" not in payload:
        return False, "missing_tool_calls"
    tool_calls = payload.get("tool_calls")
    if not isinstance(tool_calls, list):
        return False, "tool_calls_not_list"
    for i, call in enumerate(tool_calls):
        if not isinstance(call, dict):
            return False, f"tool_call_{i}_not_object"
        fn = call.get("function")
        if not isinstance(fn, dict):
            return False, f"tool_call_{i}_missing_function"
        if not isinstance(fn.get("name"), str):
            return False, f"tool_call_{i}_missing_function_name"
        if "arguments" not in fn:
            return False, f"tool_call_{i}_missing_arguments"
    return True, "ok"


def _extract_json_payload(raw_text: str) -> tuple[Any | None, bool, str]:
    text = raw_text.strip()
    if not text:
        return None, False, "empty_output"
    try:
        return json.loads(text), False, "strict"
    except Exception:
        pass

    first = text.find("{")
    last = text.rfind("}")
    if first >= 0 and last > first:
        candidate = text[first : last + 1]
        try:
            return json.loads(candidate), True, "embedded"
        except Exception:
            return None, False, "invalid_json"
    return None, False, "invalid_json"


def _build_prompt_rows(rows: list[dict[str, Any]], tokenizer: Any, prompt_template_cfg: dict[str, Any]) -> list[PromptRow]:
    out: list[PromptRow] = []
    for idx, row in enumerate(rows, start=1):
        _validate_row(row, idx)
        msgs = row["messages"]
        system_text = str(msgs[0].get("content") or "")
        user_text = str(msgs[1].get("content") or "")
        payload, expected_no_call = _expected_payload_from_row(row, idx)
        prefix = _render_prompt_prefix(
            system_text=system_text,
            user_text=user_text,
            tokenizer=tokenizer,
            prompt_template_cfg=prompt_template_cfg,
            row_idx=idx,
        )
        meta = row.get("metadata") or {}
        source_case_id = str(meta.get("source_case_id") or meta.get("case_id") or f"row_{idx}")
        tool = str(meta.get("tool") or "")
        out.append(
            PromptRow(
                row_index_1based=idx,
                source_case_id=source_case_id,
                tool=tool,
                system_text=system_text,
                user_text=user_text,
                prompt_prefix=prefix,
                expected_payload=payload,
                expected_no_call=expected_no_call,
            )
        )
    return out


def _apply_system_prompt_override(rows: list[dict[str, Any]], override_text: str) -> list[dict[str, Any]]:
    patched: list[dict[str, Any]] = []
    for idx, row in enumerate(rows, start=1):
        msgs = row.get("messages")
        if not isinstance(msgs, list) or len(msgs) < 1 or not isinstance(msgs[0], dict):
            raise RuntimeError(f"row {idx}: cannot apply system override; malformed messages")
        row_copy = dict(row)
        msgs_copy = [dict(m) if isinstance(m, dict) else m for m in msgs]
        first = msgs_copy[0]
        if not isinstance(first, dict):
            raise RuntimeError(f"row {idx}: messages[0] is not an object")
        first["role"] = "system"
        first["content"] = override_text
        msgs_copy[0] = first
        row_copy["messages"] = msgs_copy
        patched.append(row_copy)
    return patched


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


def _load_base_model_and_tokenizer(config: dict[str, Any]):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    model_cfg = config["model"]
    tok = AutoTokenizer.from_pretrained(
        model_cfg["tokenizer_name_or_path"],
        trust_remote_code=bool(model_cfg.get("trust_remote_code", False)),
    )
    if tok.pad_token_id is None:
        if tok.eos_token_id is None:
            raise RuntimeError("tokenizer has neither pad_token_id nor eos_token_id")
        tok.pad_token = tok.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_cfg["model_name_or_path"],
        trust_remote_code=bool(model_cfg.get("trust_remote_code", False)),
        torch_dtype=_resolve_dtype(model_cfg.get("torch_dtype", "bfloat16")),
        device_map="auto",
    )
    model.eval()
    return model, tok


def _infer_outputs(
    model: Any,
    tokenizer: Any,
    prompt_rows: list[PromptRow],
    max_new_tokens: int,
) -> list[str]:
    import torch

    outputs: list[str] = []
    try:
        model_device = next(model.parameters()).device
    except StopIteration:
        model_device = torch.device("cpu")

    for row in prompt_rows:
        encoded = tokenizer(
            row.prompt_prefix,
            return_tensors="pt",
            add_special_tokens=False,
        )
        encoded = {k: v.to(model_device) for k, v in encoded.items()}

        with torch.inference_mode():
            gen_ids = model.generate(
                **encoded,
                do_sample=False,
                max_new_tokens=max_new_tokens,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )

        input_len = int(encoded["input_ids"].shape[1])
        new_ids = gen_ids[0][input_len:]
        text = tokenizer.decode(new_ids, skip_special_tokens=True)
        outputs.append(text)
    return outputs


def _evaluate_prediction(
    predicted_text: str,
    expected_payload: dict[str, Any] | None,
    expected_no_call: bool,
) -> dict[str, Any]:
    parsed_payload, wrapper_leakage, parse_mode = _extract_json_payload(predicted_text)
    shape_ok = False
    shape_reason = "payload_not_parsed"
    if parsed_payload is not None:
        shape_ok, shape_reason = _validate_tool_payload_shape(parsed_payload)

    predicted_no_call = False
    predicted_tool_names: list[str] = []
    predicted_args: list[Any] = []
    predicted_args_parse_ok = False
    if shape_ok:
        tool_calls = parsed_payload.get("tool_calls", [])
        predicted_no_call = isinstance(tool_calls, list) and len(tool_calls) == 0
        predicted_tool_names = _extract_tool_names(parsed_payload)
        predicted_args, predicted_args_parse_ok = _extract_arguments(parsed_payload)

    expected_tool_names: list[str] = []
    expected_args: list[Any] = []
    expected_args_parse_ok = False
    if expected_payload is not None:
        expected_tool_names = _extract_tool_names(expected_payload)
        expected_args, expected_args_parse_ok = _extract_arguments(expected_payload)

    tool_name_accuracy = (
        shape_ok and expected_payload is not None and predicted_tool_names == expected_tool_names
    )
    argument_accuracy = (
        shape_ok
        and expected_payload is not None
        and expected_args_parse_ok
        and predicted_args_parse_ok
        and predicted_args == expected_args
    )

    exact_toolcall_json_valid = (parse_mode == "strict") and shape_ok

    issues: list[str] = []
    if parse_mode == "empty_output":
        issues.append("empty_output")
    elif parse_mode == "invalid_json" or parsed_payload is None:
        issues.append("invalid_json")
    if parsed_payload is not None and not shape_ok:
        issues.append(f"invalid_schema:{shape_reason}")
    if wrapper_leakage:
        issues.append("wrapper_or_prose_leakage")

    if expected_no_call:
        if shape_ok and not predicted_no_call:
            issues.append("unexpected_tool_call_when_no_call_expected")
    else:
        if not shape_ok:
            pass
        elif predicted_no_call:
            issues.append("predicted_no_call_but_tool_call_expected")
        else:
            if not tool_name_accuracy:
                issues.append("wrong_tool_name")
            if not argument_accuracy:
                issues.append("wrong_arguments")

    severity = [
        "empty_output",
        "invalid_json",
        "invalid_schema",
        "predicted_no_call_but_tool_call_expected",
        "unexpected_tool_call_when_no_call_expected",
        "wrong_tool_name",
        "wrong_arguments",
        "wrapper_or_prose_leakage",
    ]

    primary = "ok"
    for s in severity:
        if s == "invalid_schema":
            if any(x.startswith("invalid_schema:") for x in issues):
                primary = "invalid_schema"
                break
            continue
        if s in issues:
            primary = s
            break

    return {
        "generated_text": predicted_text,
        "parse_mode": parse_mode,
        "wrapper_or_prose_leakage": wrapper_leakage,
        "exact_tool_call_json_valid": exact_toolcall_json_valid,
        "parsed_payload": parsed_payload,
        "shape_ok": shape_ok,
        "shape_reason": shape_reason,
        "predicted_tool_names": predicted_tool_names,
        "predicted_arguments": predicted_args,
        "tool_name_accuracy": bool(tool_name_accuracy),
        "argument_accuracy": bool(argument_accuracy),
        "predicted_no_call": bool(predicted_no_call),
        "expected_no_call": bool(expected_no_call),
        "issues": issues,
        "primary_failure_category": primary,
    }


def _summarize_side(rows: list[dict[str, Any]], side: str) -> dict[str, Any]:
    total = len(rows)
    if total == 0:
        return {
            "rows": 0,
            "exact_tool_call_json_valid": {"count": 0, "rate": 0.0},
            "tool_name_accuracy": {"count": 0, "rate": 0.0},
            "argument_accuracy": {"count": 0, "rate": 0.0},
            "wrapper_or_prose_leakage": {"count": 0, "rate": 0.0},
            "no_call_behavior": {"available": False, "expected_no_call_rows": 0, "correct": 0, "incorrect": 0},
            "failure_categories": {},
        }

    def _rate(n: int, d: int) -> float:
        if d == 0:
            return 0.0
        return float(n) / float(d)

    side_rows = [r[side] for r in rows]
    expected_tool_rows = sum(1 for r in side_rows if not r["expected_no_call"])
    no_call_rows = sum(1 for r in side_rows if r["expected_no_call"])

    exact_json = sum(1 for r in side_rows if r["exact_tool_call_json_valid"])
    tool_acc = sum(1 for r in side_rows if (not r["expected_no_call"]) and r["tool_name_accuracy"])
    arg_acc = sum(1 for r in side_rows if (not r["expected_no_call"]) and r["argument_accuracy"])
    leakage = sum(1 for r in side_rows if r["wrapper_or_prose_leakage"])

    no_call_correct = sum(
        1 for r in side_rows if r["expected_no_call"] and r["predicted_no_call"]
    )
    no_call_incorrect = sum(
        1 for r in side_rows if r["expected_no_call"] and not r["predicted_no_call"]
    )

    cat = Counter(r["primary_failure_category"] for r in side_rows)

    return {
        "rows": total,
        "expected_tool_call_rows": expected_tool_rows,
        "exact_tool_call_json_valid": {
            "count": exact_json,
            "rate": _rate(exact_json, total),
        },
        "tool_name_accuracy": {
            "count": tool_acc,
            "rate": _rate(tool_acc, expected_tool_rows),
        },
        "argument_accuracy": {
            "count": arg_acc,
            "rate": _rate(arg_acc, expected_tool_rows),
        },
        "wrapper_or_prose_leakage": {
            "count": leakage,
            "rate": _rate(leakage, total),
        },
        "no_call_behavior": {
            "available": no_call_rows > 0,
            "expected_no_call_rows": no_call_rows,
            "correct": no_call_correct,
            "incorrect": no_call_incorrect,
        },
        "failure_categories": dict(sorted(cat.items(), key=lambda kv: kv[0])),
    }


def _delta(adapter_val: float, base_val: float) -> float:
    return adapter_val - base_val


def _build_summary(
    comparison_rows: list[dict[str, Any]],
    *,
    config_path: Path,
    adapter_dir: Path,
    val_jsonl: Path,
    out_dir: Path,
    strong_system_prompt_override_enabled: bool,
) -> dict[str, Any]:
    base_summary = _summarize_side(comparison_rows, "base")
    adapter_summary = _summarize_side(comparison_rows, "adapter")

    deltas = {
        "exact_tool_call_json_valid_rate": _delta(
            adapter_summary["exact_tool_call_json_valid"]["rate"],
            base_summary["exact_tool_call_json_valid"]["rate"],
        ),
        "tool_name_accuracy_rate": _delta(
            adapter_summary["tool_name_accuracy"]["rate"],
            base_summary["tool_name_accuracy"]["rate"],
        ),
        "argument_accuracy_rate": _delta(
            adapter_summary["argument_accuracy"]["rate"],
            base_summary["argument_accuracy"]["rate"],
        ),
        "wrapper_or_prose_leakage_rate": _delta(
            adapter_summary["wrapper_or_prose_leakage"]["rate"],
            base_summary["wrapper_or_prose_leakage"]["rate"],
        ),
    }

    return {
        "generated_utc": datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "config_path": str(config_path),
        "val_jsonl": str(val_jsonl),
        "adapter_dir": str(adapter_dir),
        "out_dir": str(out_dir),
        "strong_system_prompt_override_enabled": bool(strong_system_prompt_override_enabled),
        "system_prompt_override_text": STRONG_SYSTEM_PROMPT_OVERRIDE if strong_system_prompt_override_enabled else None,
        "rows_evaluated": len(comparison_rows),
        "base": base_summary,
        "adapter": adapter_summary,
        "delta_adapter_minus_base": deltas,
    }


def _release_model(model: Any) -> None:
    try:
        del model
    finally:
        gc.collect()
        try:
            import torch

            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except Exception:
            pass


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate base vs adapter tool-call behavior on held-out prompts.")
    parser.add_argument("--config", required=True, help="Path to training config JSON")
    parser.add_argument("--adapter-dir", default=None, help="Adapter directory; default is config.outputs.adapter_output_dir")
    parser.add_argument("--val-jsonl", default=None, help="Held-out validation JSONL; default is config.dataset.val_jsonl")
    parser.add_argument("--out-dir", default=None, help="Output directory for evaluation reports")
    parser.add_argument("--max-samples", type=int, default=0, help="Optional cap on evaluated rows (0 = all)")
    parser.add_argument("--max-new-tokens", type=int, default=192, help="Generation max_new_tokens")
    parser.add_argument(
        "--strong-system-prompt-override",
        action="store_true",
        help="Replace each row's system prompt with strict tool-call emission instructions for diagnostics.",
    )
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    config = _load_json(config_path)

    val_jsonl = Path(args.val_jsonl or config["dataset"]["val_jsonl"]).resolve()
    adapter_dir = Path(args.adapter_dir or config["outputs"]["adapter_output_dir"]).resolve()
    run_root = Path(config["outputs"]["run_root"]).resolve()

    if not val_jsonl.exists():
        raise RuntimeError(f"val JSONL not found: {val_jsonl}")
    if not adapter_dir.exists():
        raise RuntimeError(f"adapter dir not found: {adapter_dir}")

    if args.out_dir:
        out_dir = Path(args.out_dir).resolve()
    else:
        stamp = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out_dir = run_root / "evals" / f"toolcall_minimum_{stamp}"
    out_dir.mkdir(parents=True, exist_ok=False)

    prompt_template_cfg = _resolve_prompt_template_cfg(config)

    raw_rows = _load_jsonl(val_jsonl)
    if args.max_samples and args.max_samples > 0:
        raw_rows = raw_rows[: args.max_samples]
    if args.strong_system_prompt_override:
        raw_rows = _apply_system_prompt_override(raw_rows, STRONG_SYSTEM_PROMPT_OVERRIDE)

    model, tokenizer = _load_base_model_and_tokenizer(config)
    prompt_rows = _build_prompt_rows(raw_rows, tokenizer, prompt_template_cfg)

    base_outputs = _infer_outputs(
        model=model,
        tokenizer=tokenizer,
        prompt_rows=prompt_rows,
        max_new_tokens=int(args.max_new_tokens),
    )

    from peft import PeftModel

    adapter_model = PeftModel.from_pretrained(model, str(adapter_dir))
    adapter_model.eval()

    adapter_outputs = _infer_outputs(
        model=adapter_model,
        tokenizer=tokenizer,
        prompt_rows=prompt_rows,
        max_new_tokens=int(args.max_new_tokens),
    )

    comparison_rows: list[dict[str, Any]] = []
    for p, base_text, adapter_text in zip(prompt_rows, base_outputs, adapter_outputs):
        expected_payload = p.expected_payload
        base_eval = _evaluate_prediction(base_text, expected_payload, p.expected_no_call)
        adapter_eval = _evaluate_prediction(adapter_text, expected_payload, p.expected_no_call)

        expected_tool_names: list[str] = []
        expected_arguments: list[Any] = []
        if expected_payload is not None:
            expected_tool_names = _extract_tool_names(expected_payload)
            expected_arguments, _ = _extract_arguments(expected_payload)

        comparison_rows.append(
            {
                "row_index_1based": p.row_index_1based,
                "source_case_id": p.source_case_id,
                "tool": p.tool,
                "user_prompt": p.user_text,
                "expected_no_call": p.expected_no_call,
                "expected_tool_names": expected_tool_names,
                "expected_arguments": expected_arguments,
                "expected_payload_canonical": _canonical_json_text(expected_payload) if expected_payload is not None else None,
                "base": base_eval,
                "adapter": adapter_eval,
            }
        )

    summary = _build_summary(
        comparison_rows,
        config_path=config_path,
        adapter_dir=adapter_dir,
        val_jsonl=val_jsonl,
        out_dir=out_dir,
        strong_system_prompt_override_enabled=bool(args.strong_system_prompt_override),
    )

    _write_json(out_dir / "summary.json", summary)
    _write_jsonl(out_dir / "comparison_rows.jsonl", comparison_rows)

    # Compact console summary
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(json.dumps({"comparison_rows_path": str(out_dir / "comparison_rows.jsonl")}, ensure_ascii=False))

    _release_model(adapter_model)
    return 0


if __name__ == "__main__":
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    raise SystemExit(main())
