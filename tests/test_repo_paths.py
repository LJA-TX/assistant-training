import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from repo_paths import resolve_artifact_path, resolve_repo_root, resolve_script_path


def test_resolve_repo_root_from_test_path():
    assert resolve_repo_root(start=Path(__file__)) == Path(__file__).resolve().parents[1]


def test_resolve_repo_root_honors_environment_override(monkeypatch, tmp_path):
    repo_root = tmp_path / "synthetic-repo"
    (repo_root / "docs").mkdir(parents=True, exist_ok=True)
    (repo_root / "scripts").mkdir(parents=True, exist_ok=True)
    (repo_root / "evals").mkdir(parents=True, exist_ok=True)
    (repo_root / "AGENTS.md").write_text("sentinel\n", encoding="utf-8")
    (repo_root / "docs" / "goal_charter_v5a.md").write_text("sentinel\n", encoding="utf-8")

    nested_start = repo_root / "nested" / "deeper" / "placeholder.py"
    nested_start.parent.mkdir(parents=True, exist_ok=True)
    nested_start.write_text("# placeholder\n", encoding="utf-8")

    monkeypatch.setenv("ASSISTANT_TRAINING_REPO_ROOT", str(repo_root))

    assert resolve_repo_root(start=nested_start) == repo_root.resolve()


def test_alpha_scoped_roles_resolve_against_current_repo():
    root = resolve_repo_root()

    assert resolve_script_path("eval_canonical_manifest") == root / "scripts" / "eval_canonical_manifest.py"
    assert resolve_script_path("post_eval_collapse_detector") == root / "scripts" / "post_eval_collapse_detector.py"
    assert resolve_script_path("stage_c1_evaluator_foundation") == root / "scripts" / "stage_c1_evaluator_foundation.py"
    assert resolve_script_path("stage_c_e1_prompt_trace_evidence_creation") == root / "scripts" / "stage_c_e1_prompt_trace_evidence_creation.py"
    assert resolve_artifact_path("canonical_eval_manifest") == root / "evals" / "canonical_eval_manifest_v1.json"
