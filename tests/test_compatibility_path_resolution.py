import importlib.util
import json
import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from repo_paths import REPO_ROOT_ENV


def _load_script(script_name: str, module_name: str):
    script_path = Path(__file__).resolve().parents[1] / "scripts" / script_name
    spec = importlib.util.spec_from_file_location(module_name, str(script_path))
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _create_sentinel_repo(root: Path) -> None:
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "scripts").mkdir(parents=True, exist_ok=True)
    (root / "evals").mkdir(parents=True, exist_ok=True)
    (root / "AGENTS.md").write_text("sentinel\n", encoding="utf-8")
    (root / "docs" / "goal_charter_v5a.md").write_text("sentinel\n", encoding="utf-8")


def test_build_dataset_defaults_follow_resolved_repo_root(monkeypatch, tmp_path):
    mod = _load_script("build_dataset_v1.py", "build_dataset_v1")
    repo_root = tmp_path / "synthetic-repo"
    _create_sentinel_repo(repo_root)

    monkeypatch.setenv(REPO_ROOT_ENV, str(repo_root))
    monkeypatch.setattr(sys, "argv", ["build_dataset_v1.py", "--tool-sources", "dummy.jsonl"])

    args = mod.parse_args()

    assert args.output_root == str(repo_root / "data" / "v1_0")
    assert args.eval_output_root == str(repo_root / "evals" / "data" / "canonical_v1")


def test_preflight_paths_are_repo_root_relative_not_cwd_relative(monkeypatch, tmp_path):
    mod = _load_script("preflight_lora_run.py", "preflight_lora_run")
    repo_root = tmp_path / "synthetic-repo"
    _create_sentinel_repo(repo_root)

    (repo_root / "manifests" / "runs").mkdir(parents=True, exist_ok=True)
    (repo_root / "configs" / "lora").mkdir(parents=True, exist_ok=True)
    (repo_root / "models" / "base").mkdir(parents=True, exist_ok=True)
    (repo_root / "tokenizers" / "base").mkdir(parents=True, exist_ok=True)
    (repo_root / "data").mkdir(parents=True, exist_ok=True)

    manifest_path = repo_root / "manifests" / "runs" / "synthetic.run_manifest.json"
    config_path = repo_root / "configs" / "lora" / "synthetic.config.json"
    train_path = repo_root / "data" / "train.jsonl"
    val_path = repo_root / "data" / "val.jsonl"

    train_path.write_text("{}\n", encoding="utf-8")
    val_path.write_text("{}\n", encoding="utf-8")

    config_path.write_text(
        json.dumps(
            {
                "model": {
                    "model_name_or_path": "models/base",
                    "tokenizer_name_or_path": "tokenizers/base",
                },
                "dataset": {
                    "train_jsonl": "data/train.jsonl",
                    "val_jsonl": "data/val.jsonl",
                },
                "loss": {
                    "fallback_behavior_if_not_supported": "fail_fast",
                },
                "outputs": {
                    "adapter_output_dir": "outputs/adapter",
                },
            }
        ),
        encoding="utf-8",
    )
    manifest_path.write_text(
        json.dumps({"config_path": "configs/lora/synthetic.config.json"}),
        encoding="utf-8",
    )

    outside_cwd = tmp_path / "outside-cwd"
    outside_cwd.mkdir()

    monkeypatch.chdir(outside_cwd)
    monkeypatch.setenv(REPO_ROOT_ENV, str(repo_root))
    monkeypatch.setattr(
        sys,
        "argv",
        ["preflight_lora_run.py", "manifests/runs/synthetic.run_manifest.json"],
    )

    assert mod.main() == 0


def test_train_lora_config_resolution_is_repo_root_relative(monkeypatch, tmp_path):
    mod = _load_script("train_lora_sft.py", "train_lora_sft")
    repo_root = tmp_path / "synthetic-repo"
    _create_sentinel_repo(repo_root)
    config_path = repo_root / "configs" / "lora" / "synthetic.config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text("{}", encoding="utf-8")

    monkeypatch.setenv(REPO_ROOT_ENV, str(repo_root))

    assert mod._resolve_repo_root_relative_path("configs/lora/synthetic.config.json", repo_root=repo_root) == config_path
    assert mod._resolve_repo_root_relative_path(str(config_path), repo_root=repo_root) == config_path
