import json
from pathlib import Path


def _rows(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _validate_row(row: dict):
    msgs = row.get("messages")
    assert isinstance(msgs, list) and len(msgs) >= 3
    assert msgs[0].get("role") == "system"
    assert msgs[1].get("role") == "user"
    assert msgs[2].get("role") == "assistant"
    tc = msgs[2].get("tool_calls")
    assert isinstance(tc, list) and len(tc) == 1
    fn = tc[0].get("function")
    assert isinstance(fn, dict)
    name = fn.get("name")
    args = fn.get("arguments")
    assert isinstance(name, str) and name
    assert isinstance(args, str)
    obj = json.loads(args)
    assert isinstance(obj, dict)
    assert args == json.dumps(obj, ensure_ascii=False, sort_keys=True)


def _dataset_paths(version: str):
    base = "/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data"
    return (
        Path(f"{base}/tool_sft_broad_allaliases_20260504_v2_positive_aug_inferred_{version}_train_grouped.jsonl"),
        Path(f"{base}/tool_sft_broad_allaliases_20260504_v2_positive_aug_inferred_{version}_val_grouped.jsonl"),
    )


def test_dataset_contract_paths_exist():
    for version in ("v0_1", "v0_2"):
        train, val = _dataset_paths(version)
        assert train.exists()
        assert val.exists()


def test_dataset_rows_are_canonical():
    for version in ("v0_1", "v0_2"):
        train, val = _dataset_paths(version)
        for path in (train, val):
            for row in _rows(path):
                _validate_row(row)


def test_v0_2_system_prompt_is_strict_contract():
    strict_prefix = "You are an assistant-runtime tool-call emission model."
    train, val = _dataset_paths("v0_2")
    for path in (train, val):
        for row in _rows(path):
            msgs = row["messages"]
            assert msgs[0]["role"] == "system"
            content = str(msgs[0].get("content") or "")
            assert content.startswith(strict_prefix)
