import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from repo_paths import (
    REPO_ROOT_ENV,
    fixture_registry,
    resolve_repo_root,
    validate_fixture_registry,
    validate_role_maps,
)


def _create_sentinel_repo(root: Path) -> None:
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "scripts").mkdir(parents=True, exist_ok=True)
    (root / "evals").mkdir(parents=True, exist_ok=True)
    (root / "AGENTS.md").write_text("sentinel\n", encoding="utf-8")
    (root / "docs" / "goal_charter_v5a.md").write_text("sentinel\n", encoding="utf-8")


def test_resolve_repo_root_from_test_path():
    assert resolve_repo_root(start=Path(__file__)) == Path(__file__).resolve().parents[1]


def test_resolve_repo_root_honors_environment_override(monkeypatch, tmp_path):
    repo_root = tmp_path / "synthetic-repo"
    _create_sentinel_repo(repo_root)
    nested_start = repo_root / "nested" / "deeper" / "placeholder.py"
    nested_start.parent.mkdir(parents=True, exist_ok=True)
    nested_start.write_text("# placeholder\n", encoding="utf-8")

    monkeypatch.setenv(REPO_ROOT_ENV, str(repo_root))

    assert resolve_repo_root(start=nested_start) == repo_root.resolve()


def test_role_maps_and_fixture_registry_validate_against_current_repo():
    validation = validate_role_maps()
    all_roles = validation["all_roles"]
    present_roles = validation["present_roles"]

    assert all_roles["script:eval_canonical_manifest"].exists()
    assert all_roles["artifact:wp8_fixture_root"].exists()
    assert "script:eval_canonical_manifest" in present_roles
    assert "artifact:wp8_fixture_root" in present_roles

    resolved_registry = validate_fixture_registry()
    assert set(resolved_registry) == {
        "fixture_family/wp8_validation",
        "threshold_profile/stage_b_v1",
        "sample_output/stage_c4_v1",
        "sample_output/stage_c5_v1",
        "sample_output/stage_c6_v1",
    }

    public_registry = fixture_registry()
    for artifact_id, record in public_registry.items():
        assert artifact_id in resolved_registry
        assert Path(record["current_path"]).exists()
        assert Path(record["recorded_source_path"]).exists()


def test_validate_role_maps_reports_optional_output_roles_separately():
    validation = validate_role_maps()
    all_roles = validation["all_roles"]
    present_roles = validation["present_roles"]
    optional_missing_roles = validation["optional_missing_roles"]

    optional_role = "artifact:stage_c8_projection_artifacts_dir"
    if all_roles[optional_role].exists():
        assert optional_role in present_roles
        assert optional_role not in optional_missing_roles
    else:
        assert optional_role not in present_roles
        assert optional_role in optional_missing_roles
