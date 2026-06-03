#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gc
import json
import os
import random
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CLASS_PRIORITY = [
    "invalid_json",
    "invalid_schema",
    "wrapper_leakage",
    "missing_tool_call",
    "unexpected_tool_call",
    "wrong_tool_name",
    "wrong_arguments",
    "other_failure",
]

LEGACY_ANCHOR_BUCKETS = (
    "literal_tool_calls",
    "paraphrastic_tool_call",
    "schema_paraphrase",
    "no_anchor_phrase",
)

FAILURE_SUBTYPE_KEYS = (
    "direct_answer_substitution",
    "scalar_substitution",
    "malformed_partial_json",
    "near_canonical_wrapper_or_envelope_drift",
    "other_non_exact",
)

LEGACY_ANCHOR_TAXONOMY_MARKER = "legacy_prompt_anchor_bucket_v1"
EVALUATOR_PREAGGREGATION_OWNER = "evaluator_pre_aggregation_v1"
DATASET_METADATA_OWNER = "dataset_metadata"


@dataclass
class EvalRow:
    split: str
    row_index_1based: int
    source_case_id: str
    system_text: str
    user_text: str
    prompt_prefix: str
    expected_tool: bool
    expected_no_call: bool
    expected_payload: dict[str, Any] | None
    expected_tool_names: list[str]
    expected_args: list[Any]
    metadata: dict[str, Any]


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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
                raise RuntimeError(f"invalid JSONL {path}:{line_no}: {exc}") from exc
    return rows


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _coerce_args(raw_args: Any) -> tuple[Any, bool]:
    if isinstance(raw_args, str):
        try:
            parsed = json.loads(raw_args)
            return parsed, True
        except Exception:
            return raw_args, False
    return raw_args, isinstance(raw_args, dict)


def _extract_tool_names(payload: dict[str, Any]) -> list[str]:
    names: list[str] = []
    tool_calls = payload.get("tool_calls")
    if not isinstance(tool_calls, list):
        return names
    for call in tool_calls:
        if not isinstance(call, dict):
            names.append("")
            continue
        fn = call.get("function")
        if not isinstance(fn, dict):
            names.append("")
            continue
        name = fn.get("name")
        names.append(str(name) if isinstance(name, str) else "")
    return names


def _extract_arguments(payload: dict[str, Any]) -> tuple[list[Any], bool]:
    args: list[Any] = []
    ok = True
    tool_calls = payload.get("tool_calls")
    if not isinstance(tool_calls, list):
        return args, False
    for call in tool_calls:
        if not isinstance(call, dict):
            args.append(None)
            ok = False
            continue
        fn = call.get("function")
        if not isinstance(fn, dict):
            args.append(None)
            ok = False
            continue
        parsed, parse_ok = _coerce_args(fn.get("arguments"))
        args.append(parsed)
        ok = ok and parse_ok
    return args, ok


def _validate_schema(payload: Any) -> tuple[bool, str]:
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
        if call.get("type") != "function":
            return False, f"tool_call_{i}_type_not_function"
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
        return None, False, "empty"

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
            return None, False, "invalid"

    return None, False, "invalid"


def _looks_like_tool_intent(text: str) -> bool:
    lowered = text.lower()
    if "tool_calls" in lowered:
        return True
    if "to=functions." in lowered:
        return True
    if "<toolcall" in lowered or "<tool_call" in lowered:
        return True
    if re.search(r'"name"\s*:\s*"[a-z_]+"', text) and re.search(r'"arguments"\s*:', text):
        return True
    return False


def _rate(num: int, den: int) -> float:
    return float(num) / float(den) if den else 0.0


def _is_number_token(text: str) -> bool:
    return bool(re.fullmatch(r"[-+]?\d+(\.\d+)?", text.strip()))


def _primary_expected_tool_name(row: EvalRow) -> str:
    if not row.expected_tool_names:
        return ""
    return str(row.expected_tool_names[0] or "")


def _prompt_anchor_bucket(prompt: str) -> str:
    lowered = prompt.lower()
    if "tool_calls" in lowered:
        return "literal_tool_calls"
    if "tool call" in lowered or "tool-call" in lowered or "function call" in lowered:
        return "paraphrastic_tool_call"
    if "json object" in lowered or "structured payload" in lowered or "canonical payload" in lowered:
        return "schema_paraphrase"
    return "no_anchor_phrase"


def _read_file_archetype(prompt: str) -> str:
    lowered = prompt.lower()
    if "report whether" in lowered and "appears" in lowered:
        return "read_file_boolean_presence"
    if "first function name" in lowered:
        return "read_file_first_function_name"
    if "symbol name" in lowered:
        return "read_file_symbol_name"
    return "read_file_other"


def _coerce_optional_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes"}:
            return True
        if lowered in {"false", "0", "no"}:
            return False
    return None


def _anchor_assignment_labels(row: EvalRow) -> tuple[str, str, str]:
    meta = row.metadata
    explicit_bucket = None
    for key in ("anchor_bucket", "eval_anchor_bucket", "intervention_i10_anchor_bucket"):
        value = meta.get(key)
        if isinstance(value, str) and value.strip():
            explicit_bucket = value.strip()
            break
    explicit_owner = str(meta.get("anchor_assignment_owner") or "").strip() or None
    explicit_taxonomy = str(meta.get("anchor_taxonomy_marker") or "").strip() or None
    if explicit_bucket is not None:
        return (
            explicit_bucket,
            explicit_owner or DATASET_METADATA_OWNER,
            explicit_taxonomy or LEGACY_ANCHOR_TAXONOMY_MARKER,
        )
    return (
        _prompt_anchor_bucket(row.user_text),
        explicit_owner or EVALUATOR_PREAGGREGATION_OWNER,
        explicit_taxonomy or LEGACY_ANCHOR_TAXONOMY_MARKER,
    )


def _read_file_membership_labels(row: EvalRow) -> tuple[str | None, bool | None, str | None]:
    if _primary_expected_tool_name(row) != "read_file":
        return None, None, None

    meta = row.metadata
    explicit_archetype = None
    for key in ("read_file_archetype", "eval_read_file_archetype", "intervention_i10_query_archetype"):
        value = meta.get(key)
        if isinstance(value, str) and value.strip():
            explicit_archetype = value.strip()
            break
    explicit_membership = _coerce_optional_bool(meta.get("symbol_name_membership"))
    explicit_owner = (
        str(
            meta.get("membership_owner")
            or meta.get("symbol_name_membership_owner")
            or ""
        ).strip()
        or None
    )

    if explicit_archetype is not None:
        membership = explicit_membership if explicit_membership is not None else explicit_archetype == "read_file_symbol_name"
        return explicit_archetype, membership, explicit_owner or DATASET_METADATA_OWNER

    if explicit_membership is not None:
        archetype = "read_file_symbol_name" if explicit_membership else "read_file_other"
        return archetype, explicit_membership, explicit_owner or DATASET_METADATA_OWNER

    derived_archetype = _read_file_archetype(row.user_text)
    return (
        derived_archetype,
        derived_archetype == "read_file_symbol_name",
        explicit_owner or EVALUATOR_PREAGGREGATION_OWNER,
    )


def _failure_subtype(row: EvalRow, classified: dict[str, Any]) -> str | None:
    if not row.expected_tool or bool(classified.get("exact_valid", False)):
        return None

    generated = str(classified.get("generated_text") or "").strip()
    lowered = generated.lower()
    parse_mode = str(classified.get("parse_mode") or "")
    schema_reason = str(classified.get("schema_reason") or "")
    primary_class = str(classified.get("primary_class") or "")

    if primary_class in {"wrong_tool_name", "wrong_arguments", "wrapper_leakage", "missing_tool_call"}:
        return "near_canonical_wrapper_or_envelope_drift"
    if schema_reason == "missing_tool_calls":
        return "near_canonical_wrapper_or_envelope_drift"

    if parse_mode in {"invalid", "empty"} or schema_reason in {"payload_not_parsed", "payload_not_object"}:
        if _is_number_token(generated) or lowered in {"true", "false", "null"}:
            return "scalar_substitution"
        if generated.startswith("{") or generated.startswith("[") or _looks_like_tool_intent(generated):
            return "malformed_partial_json"
        return "direct_answer_substitution"

    if primary_class == "invalid_schema":
        if generated.startswith("{") or generated.startswith("[") or _looks_like_tool_intent(generated):
            return "malformed_partial_json"
        return "near_canonical_wrapper_or_envelope_drift"

    return "other_non_exact"


def _build_preaggregation_labels(row: EvalRow, classified: dict[str, Any]) -> dict[str, Any]:
    anchor_bucket, anchor_assignment_owner, anchor_taxonomy_marker = _anchor_assignment_labels(row)
    read_file_archetype, symbol_name_membership, membership_owner = _read_file_membership_labels(row)
    return {
        "failure_subtype": _failure_subtype(row, classified),
        "anchor_bucket": anchor_bucket,
        "anchor_assignment_owner": anchor_assignment_owner,
        "anchor_taxonomy_marker": anchor_taxonomy_marker,
        "read_file_archetype": read_file_archetype,
        "symbol_name_membership": symbol_name_membership,
        "membership_owner": membership_owner,
    }


def _build_detector_metrics(side_summary: dict[str, Any]) -> dict[str, Any]:
    aggregate = side_summary["aggregate"]
    adversarial = side_summary["per_split"]["adversarial"]
    return {
        "aggregate": {
            "exact_json_validity": float(aggregate["exact_json_validity"]["rate"]),
            "invalid_json": float(aggregate["invalid_json_rate"]),
            "tool_name_accuracy": float(aggregate["tool_name_accuracy"]["rate"]),
            "argument_accuracy": float(aggregate["argument_accuracy"]["rate"]),
            "wrapper_leakage": float(aggregate["wrapper_leakage_rate"]),
            "no_call_correctness": float(aggregate["no_call_correctness"]["rate"]),
        },
        "probes": {
            "no_call_adversarial": {
                "no_call_correctness": float(adversarial["no_call_correctness"]["rate"]),
            }
        },
    }


def _tool_expected_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for row in rows if bool(row["expected_tool"])]


def _build_failure_profile(rows: list[dict[str, Any]]) -> dict[str, Any]:
    tool_rows = _tool_expected_rows(rows)
    non_exact_tool_rows = [row for row in tool_rows if not bool(row["eval"]["exact_valid"])]

    subtype_counts = Counter({key: 0 for key in FAILURE_SUBTYPE_KEYS})
    for row in non_exact_tool_rows:
        subtype = str(row.get("failure_subtype") or "other_non_exact")
        if subtype not in subtype_counts:
            subtype = "other_non_exact"
        subtype_counts[subtype] += 1

    read_file_rows = [row for row in tool_rows if str(row.get("expected_primary_tool_name") or "") == "read_file"]
    read_file_exact = sum(1 for row in read_file_rows if bool(row["eval"]["exact_valid"]))

    symbol_rows = [row for row in read_file_rows if row.get("symbol_name_membership") is True]
    symbol_exact = sum(1 for row in symbol_rows if bool(row["eval"]["exact_valid"]))

    exact_tool_rows = [row for row in tool_rows if bool(row["eval"]["exact_valid"])]
    anchor_counts = Counter({bucket: 0 for bucket in LEGACY_ANCHOR_BUCKETS})
    for row in exact_tool_rows:
        bucket = str(row.get("anchor_bucket") or "")
        if bucket in anchor_counts:
            anchor_counts[bucket] += 1

    exact_tool_row_count = len(exact_tool_rows)
    anchor_share = {
        bucket: _rate(anchor_counts[bucket], exact_tool_row_count)
        for bucket in LEGACY_ANCHOR_BUCKETS
    }

    return {
        "tool_expected_rows": len(tool_rows),
        "non_exact_tool_rows": len(non_exact_tool_rows),
        "failure_categories_non_exact_tool_rows": {
            key: int(subtype_counts.get(key, 0))
            for key in FAILURE_SUBTYPE_KEYS
        },
        "read_file_exact_valid": {
            "count": read_file_exact,
            "rows": len(read_file_rows),
            "rate": _rate(read_file_exact, len(read_file_rows)),
        },
        "read_file_symbol_name_exact_valid": {
            "count": symbol_exact,
            "rows": len(symbol_rows),
            "rate": _rate(symbol_exact, len(symbol_rows)),
        },
        "anchor_exact_share": anchor_share,
    }


def _select_detector_side(
    *,
    base_summary: dict[str, Any],
    base_rows: list[dict[str, Any]],
    adapter_summary: dict[str, Any] | None,
    adapter_rows: list[dict[str, Any]],
) -> tuple[str, dict[str, Any], list[dict[str, Any]]]:
    if adapter_summary is not None:
        return "adapter", adapter_summary, adapter_rows
    return "base", base_summary, base_rows


def _expected_from_row(row: dict[str, Any]) -> tuple[bool, bool, dict[str, Any] | None, list[str], list[Any]]:
    msgs = row.get("messages")
    if not isinstance(msgs, list) or len(msgs) < 3:
        raise RuntimeError("row messages missing/short")
    assistant = msgs[2]
    if not isinstance(assistant, dict) or assistant.get("role") != "assistant":
        raise RuntimeError("assistant message missing")

    tool_calls = assistant.get("tool_calls")
    if isinstance(tool_calls, list) and len(tool_calls) > 0:
        payload = {"tool_calls": tool_calls}
        names = _extract_tool_names(payload)
        args, _ = _extract_arguments(payload)
        return True, False, payload, names, args

    return False, True, None, [], []


def _render_custom_prompt_prefix(system_text: str, user_text: str, custom_template_name: str) -> str:
    if custom_template_name == "generic_roles_v1":
        return f"[SYSTEM]\\n{system_text}\\n[USER]\\n{user_text}\\n[ASSISTANT]\\n"
    raise RuntimeError(f"unsupported custom template: {custom_template_name}")


def _prompt_prefix(system_text: str, user_text: str, tokenizer: Any, tokenizer_cfg: dict[str, Any]) -> str:
    mode = str(tokenizer_cfg.get("chat_template_mode", "tokenizer_native"))
    allow_custom_fallback = bool(tokenizer_cfg.get("allow_custom_fallback", False))
    custom_template_name = str(tokenizer_cfg.get("custom_template_name", "generic_roles_v1"))

    if mode == "custom":
        return _render_custom_prompt_prefix(system_text, user_text, custom_template_name)

    if not hasattr(tokenizer, "apply_chat_template"):
        if allow_custom_fallback:
            return _render_custom_prompt_prefix(system_text, user_text, custom_template_name)
        raise RuntimeError("tokenizer.apply_chat_template missing")
    if not getattr(tokenizer, "chat_template", None):
        if allow_custom_fallback:
            return _render_custom_prompt_prefix(system_text, user_text, custom_template_name)
        raise RuntimeError("tokenizer.chat_template missing")

    text = tokenizer.apply_chat_template(
        [
            {"role": "system", "content": system_text},
            {"role": "user", "content": user_text},
        ],
        tokenize=False,
        add_generation_prompt=True,
    )
    if isinstance(text, str) and text:
        return text
    if allow_custom_fallback:
        return _render_custom_prompt_prefix(system_text, user_text, custom_template_name)
    raise RuntimeError("empty prompt template output")


def _build_rows(split: str, rows: list[dict[str, Any]], tokenizer: Any, tokenizer_cfg: dict[str, Any]) -> list[EvalRow]:
    out: list[EvalRow] = []
    for idx, row in enumerate(rows, start=1):
        msgs = row.get("messages")
        if not isinstance(msgs, list) or len(msgs) < 3:
            raise RuntimeError(f"{split} row {idx}: messages missing/short")
        if not isinstance(msgs[0], dict) or not isinstance(msgs[1], dict):
            raise RuntimeError(f"{split} row {idx}: malformed message entries")
        if msgs[0].get("role") != "system" or msgs[1].get("role") != "user":
            raise RuntimeError(f"{split} row {idx}: first two roles must be system/user")

        expected_tool, expected_no_call, expected_payload, expected_tool_names, expected_args = _expected_from_row(row)
        meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        source_case_id = str(meta.get("source_case_id") or meta.get("case_id") or f"{split}_{idx}")

        out.append(
            EvalRow(
                split=split,
                row_index_1based=idx,
                source_case_id=source_case_id,
                system_text=str(msgs[0].get("content") or ""),
                user_text=str(msgs[1].get("content") or ""),
                prompt_prefix=_prompt_prefix(
                    str(msgs[0].get("content") or ""),
                    str(msgs[1].get("content") or ""),
                    tokenizer,
                    tokenizer_cfg,
                ),
                expected_tool=expected_tool,
                expected_no_call=expected_no_call,
                expected_payload=expected_payload,
                expected_tool_names=expected_tool_names,
                expected_args=expected_args,
                metadata=dict(meta),
            )
        )
    return out


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


def _load_base_model_and_tokenizer(model_name_or_path: str, dtype_name: str):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(model_name_or_path)
    if tok.pad_token_id is None:
        if tok.eos_token_id is None:
            raise RuntimeError("tokenizer has neither pad_token_id nor eos_token_id")
        tok.pad_token = tok.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path,
        torch_dtype=_resolve_dtype(dtype_name),
        device_map="auto",
    )
    model.eval()
    return model, tok


def _infer(
    model: Any,
    tokenizer: Any,
    rows: list[EvalRow],
    decode_cfg: dict[str, Any],
) -> list[str]:
    import torch

    outputs: list[str] = []
    try:
        model_device = next(model.parameters()).device
    except StopIteration:
        model_device = torch.device("cpu")

    for row in rows:
        encoded = tokenizer(row.prompt_prefix, return_tensors="pt", add_special_tokens=False)
        encoded = {k: v.to(model_device) for k, v in encoded.items()}

        with torch.inference_mode():
            gen = model.generate(
                **encoded,
                do_sample=bool(decode_cfg["do_sample"]),
                temperature=float(decode_cfg["temperature"]),
                top_p=float(decode_cfg["top_p"]),
                repetition_penalty=float(decode_cfg["repetition_penalty"]),
                max_new_tokens=int(decode_cfg["max_new_tokens"]),
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )

        start = int(encoded["input_ids"].shape[1])
        new_ids = gen[0][start:]
        outputs.append(tokenizer.decode(new_ids, skip_special_tokens=True))

    return outputs


def _classify(row: EvalRow, prediction_text: str) -> dict[str, Any]:
    parsed, wrapper, parse_mode = _extract_json_payload(prediction_text)
    schema_ok, schema_reason = _validate_schema(parsed) if parsed is not None else (False, "payload_not_parsed")

    predicted_tool_names: list[str] = []
    predicted_args: list[Any] = []
    predicted_args_ok = False
    predicted_has_tool_call = False
    if schema_ok:
        predicted_tool_names = _extract_tool_names(parsed)
        predicted_args, predicted_args_ok = _extract_arguments(parsed)
        tc = parsed.get("tool_calls") if isinstance(parsed, dict) else None
        predicted_has_tool_call = isinstance(tc, list) and len(tc) > 0

    tool_name_correct = False
    arg_correct = False
    if row.expected_tool and schema_ok and predicted_has_tool_call:
        tool_name_correct = predicted_tool_names == row.expected_tool_names
        arg_correct = predicted_args_ok and predicted_args == row.expected_args

    primary_class = "other_failure"
    secondary: list[str] = []

    if row.expected_no_call:
        if schema_ok:
            tc = parsed.get("tool_calls") if isinstance(parsed, dict) else None
            if isinstance(tc, list) and len(tc) == 0:
                primary_class = "refusal_expected"
            elif isinstance(tc, list) and len(tc) > 0:
                primary_class = "unexpected_tool_call"
            else:
                primary_class = "invalid_schema"
                secondary.append(schema_reason)
        else:
            if _looks_like_tool_intent(prediction_text):
                primary_class = "invalid_json" if parse_mode == "invalid" else "invalid_schema"
            else:
                primary_class = "refusal_expected"
    else:
        failures: list[str] = []

        if parse_mode == "invalid" or parse_mode == "empty":
            failures.append("invalid_json")
        if parsed is not None and not schema_ok:
            failures.append("invalid_schema")
            secondary.append(schema_reason)
        if wrapper:
            failures.append("wrapper_leakage")

        if schema_ok:
            tc = parsed.get("tool_calls") if isinstance(parsed, dict) else None
            if not isinstance(tc, list) or len(tc) == 0:
                failures.append("missing_tool_call")
            else:
                if not tool_name_correct:
                    failures.append("wrong_tool_name")
                if not arg_correct:
                    failures.append("wrong_arguments")

        if not failures:
            primary_class = "exact_valid"
        else:
            for cls in CLASS_PRIORITY:
                if cls in failures:
                    primary_class = cls
                    break

    exact_valid = primary_class == "exact_valid"

    return {
        "generated_text": prediction_text,
        "parse_mode": parse_mode,
        "wrapper_leakage": wrapper,
        "schema_ok": schema_ok,
        "schema_reason": schema_reason,
        "expected_tool": row.expected_tool,
        "expected_no_call": row.expected_no_call,
        "predicted_tool_names": predicted_tool_names,
        "predicted_arguments": predicted_args,
        "tool_name_correct": tool_name_correct,
        "argument_correct": arg_correct,
        "primary_class": primary_class,
        "secondary_annotations": secondary,
        "exact_valid": exact_valid,
    }


def _summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(rows)
    classes = Counter(r["eval"]["primary_class"] for r in rows)
    tool_expected_rows = sum(1 for r in rows if r["eval"]["expected_tool"])
    no_call_expected_rows = sum(1 for r in rows if r["eval"]["expected_no_call"])

    exact_valid_count = classes.get("exact_valid", 0)
    wrapper_count = classes.get("wrapper_leakage", 0)

    tool_name_correct = sum(
        1
        for r in rows
        if r["eval"]["expected_tool"] and r["eval"]["tool_name_correct"]
    )
    arg_correct = sum(
        1
        for r in rows
        if r["eval"]["expected_tool"] and r["eval"]["argument_correct"]
    )
    no_call_correct = classes.get("refusal_expected", 0)

    return {
        "rows": total,
        "class_counts": dict(sorted(classes.items(), key=lambda kv: kv[0])),
        "exact_json_validity": {"count": exact_valid_count, "rate": _rate(exact_valid_count, total)},
        "invalid_json_rate": _rate(classes.get("invalid_json", 0), total),
        "tool_name_accuracy": {"count": tool_name_correct, "rate": _rate(tool_name_correct, tool_expected_rows)},
        "argument_accuracy": {"count": arg_correct, "rate": _rate(arg_correct, tool_expected_rows)},
        "wrapper_leakage_rate": _rate(wrapper_count, total),
        "no_call_correctness": {
            "count": no_call_correct,
            "rate": _rate(no_call_correct, no_call_expected_rows),
            "expected_rows": no_call_expected_rows,
        },
        "tool_expected_rows": tool_expected_rows,
    }


def _aggregate_split_summaries(per_split: dict[str, dict[str, Any]]) -> dict[str, Any]:
    merged_rows = 0
    merged_classes: Counter[str] = Counter()
    tool_expected_rows = 0
    no_call_expected_rows = 0
    tool_name_correct = 0
    arg_correct = 0

    for summary in per_split.values():
        merged_rows += int(summary["rows"])
        merged_classes.update(summary["class_counts"])
        tool_expected_rows += int(summary.get("tool_expected_rows", 0))
        no_call_expected_rows += int(summary["no_call_correctness"]["expected_rows"])
        tool_name_correct += int(summary["tool_name_accuracy"]["count"])
        arg_correct += int(summary["argument_accuracy"]["count"])

    exact_valid_count = merged_classes.get("exact_valid", 0)
    wrapper_count = merged_classes.get("wrapper_leakage", 0)
    no_call_correct = merged_classes.get("refusal_expected", 0)

    return {
        "rows": merged_rows,
        "class_counts": dict(sorted(merged_classes.items(), key=lambda kv: kv[0])),
        "exact_json_validity": {"count": exact_valid_count, "rate": _rate(exact_valid_count, merged_rows)},
        "invalid_json_rate": _rate(merged_classes.get("invalid_json", 0), merged_rows),
        "tool_name_accuracy": {"count": tool_name_correct, "rate": _rate(tool_name_correct, tool_expected_rows)},
        "argument_accuracy": {"count": arg_correct, "rate": _rate(arg_correct, tool_expected_rows)},
        "wrapper_leakage_rate": _rate(wrapper_count, merged_rows),
        "no_call_correctness": {
            "count": no_call_correct,
            "rate": _rate(no_call_correct, no_call_expected_rows),
            "expected_rows": no_call_expected_rows,
        },
        "tool_expected_rows": tool_expected_rows,
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


def _eval_one_side(
    *,
    side_name: str,
    model: Any,
    tokenizer: Any,
    rows_by_split: dict[str, list[EvalRow]],
    decode_cfg: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    per_split_summary: dict[str, Any] = {}
    all_rows: list[dict[str, Any]] = []

    for split_name, split_rows in rows_by_split.items():
        generated = _infer(model, tokenizer, split_rows, decode_cfg)
        eval_rows: list[dict[str, Any]] = []
        for row, output_text in zip(split_rows, generated):
            classified = _classify(row, output_text)
            labels = _build_preaggregation_labels(row, classified)
            eval_rows.append(
                {
                    "split": split_name,
                    "row_index_1based": row.row_index_1based,
                    "source_case_id": row.source_case_id,
                    "user_prompt": row.user_text,
                    "expected_tool": row.expected_tool,
                    "expected_no_call": row.expected_no_call,
                    "expected_tool_names": row.expected_tool_names,
                    "expected_primary_tool_name": _primary_expected_tool_name(row) or None,
                    "expected_arguments": row.expected_args,
                    **labels,
                    "eval": classified,
                }
            )
        per_split_summary[split_name] = _summarize(eval_rows)
        all_rows.extend(eval_rows)

    return {
        "side": side_name,
        "per_split": per_split_summary,
        "aggregate": _aggregate_split_summaries(per_split_summary),
    }, all_rows


def _compute_delta(adapter: dict[str, Any], base: dict[str, Any]) -> dict[str, float]:
    def _d(path: list[str]) -> float:
        x = adapter
        y = base
        for k in path:
            x = x[k]
            y = y[k]
        return float(x) - float(y)

    return {
        "exact_json_validity_rate": _d(["aggregate", "exact_json_validity", "rate"]),
        "invalid_json_rate": _d(["aggregate", "invalid_json_rate"]),
        "tool_name_accuracy_rate": _d(["aggregate", "tool_name_accuracy", "rate"]),
        "argument_accuracy_rate": _d(["aggregate", "argument_accuracy", "rate"]),
        "wrapper_leakage_rate": _d(["aggregate", "wrapper_leakage_rate"]),
        "no_call_correctness_rate": _d(["aggregate", "no_call_correctness", "rate"]),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Canonical evaluator using frozen eval manifest and metric-spec v1a semantics.")
    parser.add_argument("--manifest", required=True, help="Path to canonical eval manifest JSON")
    parser.add_argument("--model-name-or-path", default=None, help="Override model path (default: manifest.tokenizer.path)")
    parser.add_argument("--adapter-dir", default=None, help="Optional adapter path for base+adapter comparison")
    parser.add_argument("--out-dir", default=None, help="Output directory")
    parser.add_argument("--torch-dtype", default="bfloat16", help="Torch dtype for model load")
    parser.add_argument("--max-samples-per-split", type=int, default=0, help="Optional sample cap per split")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest_path = Path(args.manifest).resolve()
    manifest = _load_json(manifest_path)

    model_path = str(args.model_name_or_path or manifest["tokenizer"]["path"])
    decode_cfg = dict(manifest["decode_defaults"])

    seed = int(decode_cfg.get("seed", 1234))
    random.seed(seed)
    try:
        import torch

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except Exception:
        pass

    split_keys = ["heldout_validation", "tool_holdout", "no_call", "adversarial"]
    if "direct_answer" in manifest.get("datasets", {}):
        split_keys.append("direct_answer")

    model, tokenizer = _load_base_model_and_tokenizer(model_path, args.torch_dtype)

    rows_by_split: dict[str, list[EvalRow]] = {}
    for split in split_keys:
        ds = manifest["datasets"].get(split)
        if not isinstance(ds, dict):
            raise RuntimeError(f"manifest missing datasets.{split}")
        path = Path(ds["path"]).resolve()
        rows = _load_jsonl(path)
        if args.max_samples_per_split and args.max_samples_per_split > 0:
            rows = rows[: args.max_samples_per_split]
        rows_by_split[split] = _build_rows(split, rows, tokenizer, manifest.get("tokenizer", {}))

    if args.out_dir:
        out_dir = Path(args.out_dir).resolve()
        out_dir.mkdir(parents=True, exist_ok=False)
    else:
        stamp = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out_dir = manifest_path.parent / "runs" / f"canonical_eval_{stamp}"
        out_dir.mkdir(parents=True, exist_ok=False)

    base_summary, base_rows = _eval_one_side(
        side_name="base",
        model=model,
        tokenizer=tokenizer,
        rows_by_split=rows_by_split,
        decode_cfg=decode_cfg,
    )

    adapter_summary = None
    adapter_rows: list[dict[str, Any]] = []
    deltas = None

    if args.adapter_dir:
        from peft import PeftModel

        adapter_model = PeftModel.from_pretrained(model, str(Path(args.adapter_dir).resolve()))
        adapter_model.eval()
        adapter_summary, adapter_rows = _eval_one_side(
            side_name="adapter",
            model=adapter_model,
            tokenizer=tokenizer,
            rows_by_split=rows_by_split,
            decode_cfg=decode_cfg,
        )
        deltas = _compute_delta(adapter_summary, base_summary)
        _release_model(adapter_model)

    comparison_rows: list[dict[str, Any]] = []
    by_key: dict[tuple[str, int], dict[str, Any]] = {}
    for row in base_rows:
        by_key[(str(row["split"]), int(row["row_index_1based"]))] = {"base": row}
    for row in adapter_rows:
        key = (str(row["split"]), int(row["row_index_1based"]))
        by_key.setdefault(key, {})["adapter"] = row

    for (split, idx), payload in sorted(by_key.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        entry: dict[str, Any] = {"split": split, "row_index_1based": idx}
        if "base" in payload:
            entry["base"] = payload["base"]
        if "adapter" in payload:
            entry["adapter"] = payload["adapter"]
        comparison_rows.append(entry)

    detector_side_name, detector_summary, detector_rows = _select_detector_side(
        base_summary=base_summary,
        base_rows=base_rows,
        adapter_summary=adapter_summary,
        adapter_rows=adapter_rows,
    )

    result = {
        "generated_utc": _now_utc(),
        "manifest_path": str(manifest_path),
        "model_name_or_path": model_path,
        "adapter_dir": str(Path(args.adapter_dir).resolve()) if args.adapter_dir else None,
        "decode_defaults": decode_cfg,
        "base": base_summary,
        "adapter": adapter_summary,
        "delta_adapter_minus_base": deltas,
        "detector_summary_side": detector_side_name,
        "metrics": _build_detector_metrics(detector_summary),
        "failure_profile": _build_failure_profile(detector_rows),
    }

    _write_json(out_dir / "summary.json", result)
    _write_jsonl(out_dir / "comparison_rows.jsonl", comparison_rows)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(json.dumps({"comparison_rows_path": str(out_dir / "comparison_rows.jsonl")}, ensure_ascii=False))

    _release_model(model)
    return 0


if __name__ == "__main__":
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    raise SystemExit(main())
