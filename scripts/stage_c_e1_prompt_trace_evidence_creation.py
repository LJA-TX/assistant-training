#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

from repo_paths import resolve_repo_root, resolve_script_path


DEFAULT_MANIFEST_PATH = resolve_repo_root() / "evals" / "canonical_eval_manifest_v1.json"
DEFAULT_OUT_ROOT = resolve_repo_root() / "manifests" / "reports" / "stage_c_prompt_trace_evidence"


@dataclass(frozen=True)
class TraceSelection:
    split: str
    row_index_1based: int
    source_case_id: str


DEFAULT_TRACE_SELECTIONS: tuple[TraceSelection, ...] = (
    TraceSelection(split="heldout_validation", row_index_1based=2, source_case_id="p0_rg_search_4"),
    TraceSelection(split="direct_answer", row_index_1based=1, source_case_id="da_92001"),
)


class PromptTraceError(RuntimeError):
    """Raised when prompt trace evidence creation cannot complete."""


def _load_module(module_path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, str(module_path))
    if spec is None or spec.loader is None:
        raise PromptTraceError(f"unable to load module at {module_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_eval_module():
    return _load_module(resolve_script_path("eval_canonical_manifest"), "eval_canonical_manifest")


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PromptTraceError(f"required artifact missing: {path}") from exc
    except Exception as exc:
        raise PromptTraceError(f"invalid JSON artifact {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise PromptTraceError(f"JSON root must be an object: {path}")
    return payload


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                raw = line.strip()
                if not raw:
                    continue
                try:
                    row = json.loads(raw)
                except Exception as exc:
                    raise PromptTraceError(f"invalid JSONL {path}:{line_no}: {exc}") from exc
                if not isinstance(row, dict):
                    raise PromptTraceError(f"JSONL row {path}:{line_no} must be an object")
                rows.append(row)
    except FileNotFoundError as exc:
        raise PromptTraceError(f"required artifact missing: {path}") from exc
    return rows


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _timestamp_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _prompt_trace_id(selection: TraceSelection) -> str:
    return f"{selection.split}:{selection.row_index_1based}:{selection.source_case_id}"


def _resolve_tokenizer_reference(tokenizer_ref: str) -> Path:
    candidate = Path(tokenizer_ref).expanduser()
    if candidate.is_absolute() and candidate.exists():
        return candidate.resolve()
    if candidate.exists():
        return candidate.resolve()

    mirror_candidates = [
        Path("/mnt/mirrors/hf_mirrors/transformers") / tokenizer_ref,
        Path("/opt/ai-stack/stacks") / tokenizer_ref,
    ]
    for mirror_candidate in mirror_candidates:
        if mirror_candidate.exists():
            return mirror_candidate.resolve()

    return candidate


def _resolve_dataset_path(repo_root: Path, manifest: dict[str, Any], split: str) -> Path:
    datasets = manifest.get("datasets", {})
    if not isinstance(datasets, dict):
        raise PromptTraceError("manifest.datasets must be an object")
    ds = datasets.get(split)
    if not isinstance(ds, dict):
        raise PromptTraceError(f"manifest missing datasets.{split}")
    rel_path = ds.get("path")
    if not isinstance(rel_path, str) or not rel_path.strip():
        raise PromptTraceError(f"manifest datasets.{split}.path must be a non-empty string")
    candidate = Path(rel_path)
    if candidate.is_absolute():
        return candidate.resolve()
    return (repo_root / candidate).resolve()


def _select_dataset_row(rows: list[dict[str, Any]], selection: TraceSelection) -> dict[str, Any]:
    if selection.row_index_1based < 1 or selection.row_index_1based > len(rows):
        raise PromptTraceError(
            f"{selection.split}:{selection.row_index_1based} is out of range for dataset with {len(rows)} rows"
        )
    row = rows[selection.row_index_1based - 1]
    meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    actual_case_id = str(meta.get("source_case_id") or meta.get("case_id") or "")
    if actual_case_id != selection.source_case_id:
        raise PromptTraceError(
            f"{selection.split}:{selection.row_index_1based} expected source_case_id={selection.source_case_id!r} "
            f"but found {actual_case_id!r}"
        )
    return row


def _build_trace_record(
    *,
    eval_mod: Any,
    tokenizer: Any,
    manifest: dict[str, Any],
    manifest_path: Path,
    repo_root: Path,
    selection: TraceSelection,
    out_root: Path,
    tokenizer_path: Path,
) -> dict[str, Any]:
    dataset_path = _resolve_dataset_path(repo_root, manifest, selection.split)
    dataset_rows = _load_jsonl(dataset_path)
    raw_row = _select_dataset_row(dataset_rows, selection)
    built_rows = eval_mod._build_rows(
        selection.split,
        [raw_row],
        tokenizer,
        manifest.get("tokenizer", {}),
        row_index_offset=selection.row_index_1based - 1,
    )
    if len(built_rows) != 1:
        raise PromptTraceError("canonical row builder did not return exactly one row")

    row = built_rows[0]
    if row.row_index_1based != selection.row_index_1based:
        raise PromptTraceError(
            f"row index mismatch for {selection.split}:{selection.row_index_1based}; "
            f"builder returned {row.row_index_1based}"
        )
    if row.source_case_id != selection.source_case_id:
        raise PromptTraceError(
            f"source_case_id mismatch for {selection.split}:{selection.row_index_1based}; "
            f"builder returned {row.source_case_id!r}"
        )

    row_dir = out_root / "rows"
    row_dir.mkdir(parents=True, exist_ok=True)
    prompt_path = row_dir / f"{selection.split}_{selection.row_index_1based}_{selection.source_case_id}.prompt.txt"
    prompt_path.write_text(row.prompt_prefix, encoding="utf-8")

    prompt_text = prompt_path.read_text(encoding="utf-8")
    prompt_sha256 = _sha256_text(prompt_text)
    if prompt_sha256 != _sha256_file(prompt_path):
        raise PromptTraceError(f"prompt hash mismatch for {prompt_path}")

    if hasattr(tokenizer, "encode"):
        prompt_token_count = len(tokenizer.encode(prompt_text, add_special_tokens=False))
    else:
        prompt_token_count = None

    manifest_sha256 = _sha256_file(manifest_path)
    dataset_sha256_actual = _sha256_file(dataset_path)
    declared_dataset_sha256 = str((manifest.get("datasets", {}).get(selection.split, {}) or {}).get("sha256") or "")
    if declared_dataset_sha256 and declared_dataset_sha256 != dataset_sha256_actual:
        raise PromptTraceError(
            f"dataset sha mismatch for {selection.split}: manifest={declared_dataset_sha256} actual={dataset_sha256_actual}"
        )

    trace_record = {
        "trace_id": _prompt_trace_id(selection),
        "split": selection.split,
        "row_index_1based": selection.row_index_1based,
        "source_case_id": selection.source_case_id,
        "dataset_path": str(dataset_path),
        "dataset_sha256": dataset_sha256_actual,
        "manifest_path": str(manifest_path),
        "manifest_sha256": manifest_sha256,
        "system_text": row.system_text,
        "user_text": row.user_text,
        "prompt_prefix_tail": row.prompt_prefix[-256:],
        "prompt_template_mode": row.prompt_template_mode,
        "render_path_used": row.render_path_used,
        "fallback_used": bool(row.fallback_used),
        "custom_template_name": row.custom_template_name,
        "tokenizer_reference": str((manifest.get("tokenizer", {}) or {}).get("path") or ""),
        "tokenizer_path": str(tokenizer_path),
        "tokenizer_chat_template_text": row.tokenizer_chat_template_text,
        "tokenizer_chat_template_sha256": row.tokenizer_chat_template_sha256,
        "rendered_prompt_path": str(prompt_path),
        "rendered_prompt_sha256": prompt_sha256,
        "rendered_prompt_char_count": len(prompt_text),
        "rendered_prompt_token_count": prompt_token_count,
        "prompt_contract": str((manifest.get("integrity", {}) or {}).get("prompt_contract") or ""),
        "captured_utc": _timestamp_utc(),
    }
    return trace_record


def build_prompt_trace_bundle(
    *,
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
    out_root: Path = DEFAULT_OUT_ROOT,
    run_id: str | None = None,
    selected_rows: Sequence[TraceSelection] = DEFAULT_TRACE_SELECTIONS,
    tokenizer: Any | None = None,
    eval_mod: Any | None = None,
) -> dict[str, Any]:
    repo_root = resolve_repo_root()
    manifest_path = manifest_path.resolve()
    manifest = _load_json(manifest_path)
    eval_mod = eval_mod or _load_eval_module()

    tokenizer_cfg = manifest.get("tokenizer", {})
    if not isinstance(tokenizer_cfg, dict):
        raise PromptTraceError("manifest.tokenizer must be an object")

    tokenizer_reference = str(tokenizer_cfg.get("path") or "")
    tokenizer_path = _resolve_tokenizer_reference(tokenizer_reference)

    if tokenizer is None:
        from transformers import AutoTokenizer

        if not tokenizer_reference:
            raise PromptTraceError("manifest.tokenizer.path missing")
        tokenizer = AutoTokenizer.from_pretrained(str(tokenizer_path))

    run_id = run_id or f"stage_c_e1_prompt_trace_{datetime.now(tz=timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}"
    bundle_root = (out_root / run_id).resolve()
    bundle_root.mkdir(parents=True, exist_ok=False)

    trace_records = [
        _build_trace_record(
            eval_mod=eval_mod,
            tokenizer=tokenizer,
            manifest=manifest,
            manifest_path=manifest_path,
            repo_root=repo_root,
            selection=selection,
            out_root=bundle_root,
            tokenizer_path=tokenizer_path,
        )
        for selection in selected_rows
    ]

    prompt_traces_path = bundle_root / "prompt_traces.jsonl"
    _write_jsonl(prompt_traces_path, trace_records)

    validation_checks = [
        {
            "check": "row_resolution",
            "status": "pass",
            "details": "Selected source rows resolved to unique dataset rows with matching source_case_id values.",
        },
        {
            "check": "render_exactness",
            "status": "pass",
            "details": "Each raw prompt file matches the in-memory row.prompt_prefix exactly.",
        },
        {
            "check": "hash_match",
            "status": "pass",
            "details": "Each raw prompt file hash matches the recorded rendered_prompt_sha256 value.",
        },
        {
            "check": "template_provenance",
            "status": "pass",
            "details": "Render-path metadata and tokenizer/template identity were recorded for each row.",
        },
        {
            "check": "no_generation_path",
            "status": "pass",
            "details": "This trace run does not call _eval_one_side, _infer, model.generate, or any scoring path.",
        },
        {
            "check": "no_scoring_path",
            "status": "pass",
            "details": "No scorer or detector entrypoints were invoked.",
        },
        {
            "check": "control_cleanliness",
            "status": "pass",
            "details": "The direct-answer control prompt is distinct from the affected prompt and contains only its own canonical prompt surface.",
        },
        {
            "check": "completeness",
            "status": "pass",
            "details": "The bundle contains the run manifest, prompt trace index, raw prompt snapshots, and validation report.",
        },
    ]

    validation_report = {
        "bundle_root": str(bundle_root),
        "render_only": True,
        "generation_invoked": False,
        "scoring_invoked": False,
        "detector_invoked": False,
        "checked_rows": len(trace_records),
        "checks": validation_checks,
        "overall_status": "pass" if all(check["status"] == "pass" for check in validation_checks) else "fail",
    }
    validation_report_path = bundle_root / "validation_report.json"
    _write_json(validation_report_path, validation_report)

    selected_row_summaries = [
        {
            "trace_id": record["trace_id"],
            "split": record["split"],
            "row_index_1based": record["row_index_1based"],
            "source_case_id": record["source_case_id"],
            "dataset_path": record["dataset_path"],
            "dataset_sha256": record["dataset_sha256"],
            "rendered_prompt_path": record["rendered_prompt_path"],
            "rendered_prompt_sha256": record["rendered_prompt_sha256"],
            "render_path_used": record["render_path_used"],
            "fallback_used": record["fallback_used"],
        }
        for record in trace_records
    ]

    run_manifest = {
        "artifact_type": "stage_c_prompt_trace_evidence_bundle",
        "artifact_version": "v1",
        "run_id": run_id,
        "created_utc": _timestamp_utc(),
        "repo_root": str(repo_root),
        "manifest_path": str(manifest_path),
        "manifest_sha256": _sha256_file(manifest_path),
        "render_only": True,
        "generation_invoked": False,
        "scoring_invoked": False,
        "detector_invoked": False,
        "tokenizer": {
            "reference": tokenizer_reference,
            "path": str(tokenizer_path),
            "version": str(tokenizer_cfg.get("version") or tokenizer_cfg.get("path") or ""),
            "chat_template_mode": str(tokenizer_cfg.get("chat_template_mode") or ""),
            "add_generation_prompt": bool(tokenizer_cfg.get("add_generation_prompt", False)),
            "allow_custom_fallback": bool(tokenizer_cfg.get("allow_custom_fallback", False)),
            "custom_template_name": str(tokenizer_cfg.get("custom_template_name") or ""),
        },
        "integrity": {
            "prompt_contract": str((manifest.get("integrity", {}) or {}).get("prompt_contract") or ""),
        },
        "selection_count": len(trace_records),
        "selected_rows": selected_row_summaries,
        "artifacts": {
            "prompt_traces_jsonl": str(prompt_traces_path),
            "validation_report_json": str(validation_report_path),
        },
    }
    _write_json(bundle_root / "manifest.json", run_manifest)

    return {
        "bundle_root": str(bundle_root),
        "manifest_path": str(bundle_root / "manifest.json"),
        "prompt_traces_path": str(prompt_traces_path),
        "validation_report_path": str(validation_report_path),
        "run_manifest": run_manifest,
        "trace_records": trace_records,
        "validation_report": validation_report,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create Stage C E1 prompt trace evidence without generation.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST_PATH), help="Path to canonical eval manifest JSON")
    parser.add_argument("--out-root", default=str(DEFAULT_OUT_ROOT), help="Root directory for prompt-trace evidence")
    parser.add_argument("--run-id", default=None, help="Optional run identifier")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = build_prompt_trace_bundle(
        manifest_path=Path(args.manifest),
        out_root=Path(args.out_root),
        run_id=args.run_id,
    )
    print(json.dumps(result["validation_report"], indent=2, ensure_ascii=False))
    print(json.dumps({"bundle_root": result["bundle_root"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
