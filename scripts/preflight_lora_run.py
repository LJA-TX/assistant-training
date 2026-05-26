#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: preflight_lora_run.py <run_manifest.json>")
        return 2

    manifest_path = Path(sys.argv[1])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    config_path = Path(manifest["config_path"])
    config = json.loads(config_path.read_text(encoding="utf-8"))

    checks = []

    model_path = Path(config["model"]["model_name_or_path"])
    tok_path = Path(config["model"]["tokenizer_name_or_path"])
    checks.append(("model_path_exists", model_path.exists() and model_path.is_dir()))
    checks.append(("tokenizer_path_exists", tok_path.exists() and tok_path.is_dir()))

    train_path = Path(config["dataset"]["train_jsonl"])
    val_path = Path(config["dataset"]["val_jsonl"])
    checks.append(("train_exists", train_path.exists()))
    checks.append(("val_exists", val_path.exists()))

    # Fail-fast gate requirement
    fallback = config.get("loss", {}).get("fallback_behavior_if_not_supported")
    checks.append(("assistant_only_fail_fast_configured", fallback == "fail_fast"))

    adapter_dir = Path(config["outputs"]["adapter_output_dir"])
    checks.append(("adapter_output_not_present", not adapter_dir.exists()))

    failed = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print(f"{name}: {'OK' if ok else 'FAIL'}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
