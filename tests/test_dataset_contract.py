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


def _canonical_row(system_text: str, file_path: str, line_start: int = 1, line_end: int = 2):
    args = json.dumps(
        {"line_end": line_end, "line_start": line_start, "path": file_path},
        ensure_ascii=False,
        sort_keys=True,
    )
    return {
        "messages": [
            {"role": "system", "content": system_text},
            {"role": "user", "content": f"Read {file_path} lines {line_start}-{line_end}."},
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": "call_1",
                        "type": "function",
                        "function": {
                            "name": "read_file",
                            "arguments": args,
                        },
                    }
                ],
            },
        ]
    }


def _write_dataset(root: Path, version: str, system_text: str):
    base = root / version
    base.mkdir(parents=True, exist_ok=True)
    train = base / "train.jsonl"
    val = base / "val.jsonl"
    rows = [
        _canonical_row(system_text, "/tmp/a.txt"),
        _canonical_row(system_text, "/tmp/b.txt", line_start=3, line_end=4),
    ]
    payload = "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n"
    train.write_text(payload, encoding="utf-8")
    val.write_text(payload, encoding="utf-8")
    return train, val


def test_dataset_contract_paths_exist(tmp_path):
    for version in ("v0_1", "v0_2"):
        train, val = _write_dataset(
            tmp_path,
            version,
            "You are a dataset contract test model."
            if version == "v0_1"
            else "You are an assistant-runtime tool-call emission model.",
        )
        assert train.exists()
        assert val.exists()


def test_dataset_rows_are_canonical(tmp_path):
    for version in ("v0_1", "v0_2"):
        train, val = _write_dataset(
            tmp_path,
            version,
            "You are a dataset contract test model."
            if version == "v0_1"
            else "You are an assistant-runtime tool-call emission model.",
        )
        for path in (train, val):
            for row in _rows(path):
                _validate_row(row)


def test_v0_2_system_prompt_is_strict_contract(tmp_path):
    strict_prefix = "You are an assistant-runtime tool-call emission model."
    train, val = _write_dataset(tmp_path, "v0_2", strict_prefix)
    for path in (train, val):
        for row in _rows(path):
            msgs = row["messages"]
            assert msgs[0]["role"] == "system"
            content = str(msgs[0].get("content") or "")
            assert content.startswith(strict_prefix)
