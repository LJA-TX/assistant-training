#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from repo_paths import resolve_repo_root


def _resolve_repo_root_relative_path(raw_path: str, *, repo_root: Path) -> Path:
    # Relative paths in manifests/configs are interpreted from the repository root, not cwd.
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return (repo_root / path).resolve()


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: preflight_lora_run.py <run_manifest.json>")
        return 2

    repo_root = resolve_repo_root()
    manifest_path = _resolve_repo_root_relative_path(sys.argv[1], repo_root=repo_root)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    config_path = _resolve_repo_root_relative_path(manifest["config_path"], repo_root=repo_root)
    config = json.loads(config_path.read_text(encoding="utf-8"))

    checks = []

    model_path = _resolve_repo_root_relative_path(config["model"]["model_name_or_path"], repo_root=repo_root)
    tok_path = _resolve_repo_root_relative_path(config["model"]["tokenizer_name_or_path"], repo_root=repo_root)
    checks.append(("model_path_exists", model_path.exists() and model_path.is_dir()))
    checks.append(("tokenizer_path_exists", tok_path.exists() and tok_path.is_dir()))

    train_path = _resolve_repo_root_relative_path(config["dataset"]["train_jsonl"], repo_root=repo_root)
    val_path = _resolve_repo_root_relative_path(config["dataset"]["val_jsonl"], repo_root=repo_root)
    checks.append(("train_exists", train_path.exists()))
    checks.append(("val_exists", val_path.exists()))

    # Fail-fast gate requirement
    fallback = config.get("loss", {}).get("fallback_behavior_if_not_supported")
    checks.append(("assistant_only_fail_fast_configured", fallback == "fail_fast"))

    adapter_dir = _resolve_repo_root_relative_path(config["outputs"]["adapter_output_dir"], repo_root=repo_root)
    checks.append(("adapter_output_not_present", not adapter_dir.exists()))

    failed = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print(f"{name}: {'OK' if ok else 'FAIL'}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
