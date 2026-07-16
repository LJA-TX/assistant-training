from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from types import SimpleNamespace
from pathlib import Path
from typing import Callable

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "validate_public_package.py"
PUBLIC_SOURCE_ENV = "ASSISTANT_TRAINING_PUBLIC_SOURCE_ROOT"
PUBLIC_IDENTITY_MARKER = "This checkout is the only authorized local publication origin."
PUBLIC_SOURCE_SENTINELS = (
    "README.md",
    "docs/current/start_here.md",
    "docs/framework/examples/public_sanitized_tool_call_worked_example.md",
    "docs/framework/examples/public_sanitized_tool_call_worked_example.json",
    "docs/publication/public_snapshot.json",
    "scripts/repo_paths.py",
    "tests/test_public_sanitized_tool_call_worked_example.py",
)

if str(REPO_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))

spec = importlib.util.spec_from_file_location("validate_public_package_under_test", SCRIPT_PATH)
assert spec is not None and spec.loader is not None
package = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = package
spec.loader.exec_module(package)


def _run_main(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], callback_name: str | None = None) -> tuple[int, str]:
    monkeypatch.setattr(package, "_load_repo_paths", lambda: SimpleNamespace(resolve_repo_root=lambda start=None: REPO_ROOT))
    monkeypatch.setattr(package, "_load_reference_validator", lambda root: SimpleNamespace(validate=lambda root: {"valid": True}))
    if callback_name:
        monkeypatch.setattr(package, callback_name, lambda root: (_ for _ in ()).throw(package.ValidationFailure("synthetic failure")))
    result = package.main()
    return result, capsys.readouterr().out


def test_successful_orchestration_has_stable_output(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    result, output = _run_main(monkeypatch, capsys)

    assert result == 0
    assert output == (
        "[PASS] repository root and required public surfaces\n"
        "[PASS] snapshot/front-door consistency\n"
        "[PASS] public reference validation\n"
        "[PASS] Harborview public example validation\n"
        "Public package validation: PASS\n"
    )


@pytest.mark.parametrize(
    "failure_phase",
    ["_validate_snapshot_front_door", "_validate_reference_package", "_validate_harborview"],
)
def test_each_failed_phase_returns_nonzero_and_stable_failure(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    failure_phase: str,
) -> None:
    result, output = _run_main(monkeypatch, capsys, failure_phase)

    assert result == 1
    assert "[FAIL]" in output
    assert "synthetic failure" in output
    assert output.endswith("Public package validation: FAIL\n")


def test_root_resolution_failure_returns_nonzero(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(package, "_load_repo_paths", lambda: (_ for _ in ()).throw(RuntimeError("no root")))

    result = package.main()
    output = capsys.readouterr().out

    assert result == 1
    assert output == (
        "[FAIL] repository root and required public surfaces: no root\n"
        "Public package validation: FAIL\n"
    )


def test_required_surface_failure_is_reported(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(package, "_load_repo_paths", lambda: SimpleNamespace(resolve_repo_root=lambda start=None: tmp_path))

    result = package.main()
    output = capsys.readouterr().out

    assert result == 1
    assert "missing required public surface(s)" in output
    assert output.endswith("Public package validation: FAIL\n")


@pytest.mark.parametrize("snapshot_mode", ["missing", "malformed", "front_door_mismatch"])
def test_snapshot_failures_are_detected(tmp_path: Path, snapshot_mode: str) -> None:
    for relative in ("README.md", "docs/current/start_here.md", "docs/publication/public_snapshot.json"):
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO_ROOT / relative, destination)

    snapshot_path = tmp_path / "docs/publication/public_snapshot.json"
    if snapshot_mode == "missing":
        snapshot_path.unlink()
    elif snapshot_mode == "malformed":
        snapshot_path.write_text("{not json", encoding="utf-8")
    else:
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        snapshot["snapshot_id"] = "mismatched-snapshot"
        snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")

    with pytest.raises(package.ValidationFailure):
        package._validate_snapshot_front_door(tmp_path)


def test_reference_validator_failure_is_propagated(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(package, "_load_reference_validator", lambda root: SimpleNamespace(validate=lambda root: {"valid": False}))

    with pytest.raises(package.ValidationFailure, match="reference validator returned FAIL"):
        package._validate_reference_package(REPO_ROOT)


def test_harborview_assertion_or_exception_is_propagated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeModule:
        def validate_fixture_contract_and_canonical_evaluator_reuse(self) -> None:
            raise AssertionError("bad fixture")

        def validate_documents_links_contamination_boundaries_and_public_portability(self) -> None:
            pass

        def validate_fixture_identity_and_join_integrity(self) -> None:
            pass

    monkeypatch.setattr(package, "_load_harborview_module", lambda root: FakeModule())

    with pytest.raises(package.ValidationFailure, match="Harborview validator failed"):
        package._validate_harborview(tmp_path)


def _tree_digest(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        relative = path.relative_to(root).as_posix()
        result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def _looks_like_public_source(root: Path) -> bool:
    if not all((root / relative).is_file() for relative in PUBLIC_SOURCE_SENTINELS):
        return False
    try:
        agents_text = (root / "AGENTS.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return False
    return PUBLIC_IDENTITY_MARKER in agents_text


def _public_source_root() -> Path:
    override = os.environ.get(PUBLIC_SOURCE_ENV)
    if override:
        candidate = Path(override).expanduser().resolve()
        if not _looks_like_public_source(candidate):
            raise RuntimeError(f"{PUBLIC_SOURCE_ENV} does not identify a public package")
        return candidate
    sibling = REPO_ROOT.parent / "assistant-training-public"
    if sibling != REPO_ROOT and _looks_like_public_source(sibling):
        return sibling
    if _looks_like_public_source(REPO_ROOT):
        return REPO_ROOT
    raise RuntimeError("no public package source is available")


def _copy_public_candidate(destination: Path) -> None:
    source_root = _public_source_root()
    shutil.copytree(source_root, destination, ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"))
    projected = (
        "scripts/validate_public_package.py",
        "scripts/validate_public_references.py",
        "tests/test_public_sanitized_tool_call_worked_example.py",
        "tests/test_validate_public_package.py",
        "README.md",
        "docs/current/start_here.md",
    )
    for relative in projected:
        source = REPO_ROOT / relative
        if not source.is_file():
            source = source_root / relative
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def test_end_to_end_candidate_succeeds_without_writes_or_bytecode(tmp_path: Path) -> None:
    candidate = tmp_path / "public-candidate"
    _copy_public_candidate(candidate)
    before = _tree_digest(candidate)
    env = os.environ.copy()
    env.pop("PYTHONDONTWRITEBYTECODE", None)

    completed = subprocess.run(
        [sys.executable, str(candidate / "scripts/validate_public_package.py")],
        cwd=tmp_path,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert completed.stdout == (
        "[PASS] repository root and required public surfaces\n"
        "[PASS] snapshot/front-door consistency\n"
        "[PASS] public reference validation\n"
        "[PASS] Harborview public example validation\n"
        "Public package validation: PASS\n"
    )
    assert completed.stderr == ""
    assert _tree_digest(candidate) == before


def _run_ephemeral_candidate(tmp_path: Path, mutate: Callable[[Path], None]) -> tuple[subprocess.CompletedProcess[str], dict[str, str], dict[str, str]]:
    candidate = tmp_path / "arbitrarily-named-public-clone"
    _copy_public_candidate(candidate)
    mutate(candidate)
    before = _tree_digest(candidate)
    env = os.environ.copy()
    env.pop("PYTHONDONTWRITEBYTECODE", None)
    completed = subprocess.run(
        [sys.executable, str(candidate / "scripts/validate_public_package.py")],
        cwd=tmp_path,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    after = _tree_digest(candidate)
    return completed, before, after


def _assert_clean_reference_failure(completed: subprocess.CompletedProcess[str], before: dict[str, str], after: dict[str, str]) -> None:
    assert completed.returncode != 0
    assert "[FAIL] public reference validation:" in completed.stdout
    assert completed.stdout.endswith("Public package validation: FAIL\n")
    assert completed.stderr == ""
    assert "Traceback" not in completed.stdout
    assert "Traceback" not in completed.stderr
    assert before == after


def test_unclassified_missing_markdown_reference_fails_in_reference_phase(tmp_path: Path) -> None:
    def mutate(candidate: Path) -> None:
        readme = candidate / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8") + "\n[synthetic missing reference](missing-public-file.md)\n", encoding="utf-8")

    completed, before, after = _run_ephemeral_candidate(tmp_path, mutate)
    _assert_clean_reference_failure(completed, before, after)


def test_stale_disposition_metadata_fails_in_reference_phase(tmp_path: Path) -> None:
    def mutate(candidate: Path) -> None:
        path = candidate / "docs/publication/public_reference_dispositions.json"
        metadata = json.loads(path.read_text(encoding="utf-8"))
        metadata["dispositions"].append(
            {
                "source": "README.md",
                "kind": "json_path",
                "json_path": "synthetic.stale",
                "target": "never-consumed.md",
                "disposition": "intentional_public_omission",
                "reason": "synthetic stale metadata entry",
            }
        )
        path.write_text(json.dumps(metadata), encoding="utf-8")

    completed, before, after = _run_ephemeral_candidate(tmp_path, mutate)
    _assert_clean_reference_failure(completed, before, after)


def test_altered_canonical_hash_target_fails_in_reference_phase(tmp_path: Path) -> None:
    def mutate(candidate: Path) -> None:
        path = candidate / "scripts/eval_canonical_manifest.py"
        path.write_text(path.read_text(encoding="utf-8") + "\n# synthetic hash mutation\n", encoding="utf-8")

    completed, before, after = _run_ephemeral_candidate(tmp_path, mutate)
    _assert_clean_reference_failure(completed, before, after)


@pytest.mark.parametrize(
    ("dependency", "expected_phase", "failure_text"),
    [
        ("repo_paths.py", "repository root and required public surfaces", "local module is missing"),
        ("validate_public_references.py", "public reference validation", "local module is missing"),
    ],
)
def test_missing_local_dependencies_fail_in_their_phase(tmp_path: Path, dependency: str, expected_phase: str, failure_text: str) -> None:
    def mutate(candidate: Path) -> None:
        (candidate / "scripts" / dependency).unlink()

    completed, before, after = _run_ephemeral_candidate(tmp_path, mutate)
    assert completed.returncode != 0
    assert f"[FAIL] {expected_phase}:" in completed.stdout
    assert failure_text in completed.stdout
    assert completed.stdout.endswith("Public package validation: FAIL\n")
    assert completed.stderr == ""
    assert "Traceback" not in completed.stdout
    assert before == after


@pytest.mark.parametrize(
    ("dependency", "expected_phase"),
    [
        ("repo_paths.py", "repository root and required public surfaces"),
        ("validate_public_references.py", "public reference validation"),
    ],
)
def test_import_failing_local_dependencies_fail_without_traceback(tmp_path: Path, dependency: str, expected_phase: str) -> None:
    def mutate(candidate: Path) -> None:
        (candidate / "scripts" / dependency).write_text("raise RuntimeError('synthetic import failure')\n", encoding="utf-8")

    completed, before, after = _run_ephemeral_candidate(tmp_path, mutate)
    assert completed.returncode != 0
    assert f"[FAIL] {expected_phase}: local module failed to import: {dependency}" in completed.stdout
    assert completed.stdout.endswith("Public package validation: FAIL\n")
    assert completed.stderr == ""
    assert "Traceback" not in completed.stdout
    assert "Traceback" not in completed.stderr
    assert before == after


def test_projected_test_works_in_arbitrarily_named_clone_without_sibling(tmp_path: Path) -> None:
    if os.environ.get("PUBLIC_VALIDATION_CLONE_PROBE") == "1":
        pytest.skip("nested clone probe disabled")
    candidate = tmp_path / "ordinary-public-clone-name"
    _copy_public_candidate(candidate)
    env = os.environ.copy()
    env.pop(PUBLIC_SOURCE_ENV, None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PUBLIC_VALIDATION_CLONE_PROBE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/test_validate_public_package.py"],
        cwd=candidate,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert completed.stderr == ""


def test_private_canonical_root_is_rejected_without_public_sibling(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    private_like_root = REPO_ROOT
    if _looks_like_public_source(REPO_ROOT):
        private_like_root = tmp_path / "private-like-root"
        shutil.copytree(_public_source_root(), private_like_root)
        agents = private_like_root / "AGENTS.md"
        agents.write_text(agents.read_text(encoding="utf-8").replace(PUBLIC_IDENTITY_MARKER, ""), encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "REPO_ROOT", private_like_root)
    original = _looks_like_public_source
    sibling = private_like_root.parent / "assistant-training-public"
    monkeypatch.delenv(PUBLIC_SOURCE_ENV, raising=False)
    monkeypatch.setattr(sys.modules[__name__], "_looks_like_public_source", lambda root: False if root == sibling else original(root))

    with pytest.raises(RuntimeError, match="no public package source is available"):
        _public_source_root()


def test_arbitrarily_named_public_clone_is_accepted(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    clone = tmp_path / "public-source-with-an-arbitrary-name"
    shutil.copytree(_public_source_root(), clone)
    monkeypatch.delenv(PUBLIC_SOURCE_ENV, raising=False)
    monkeypatch.setattr(sys.modules[__name__], "REPO_ROOT", clone)

    assert _public_source_root() == clone.resolve()


def test_valid_explicit_public_source_override_is_accepted(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    clone = tmp_path / "explicit-public-source"
    shutil.copytree(_public_source_root(), clone)
    monkeypatch.setenv(PUBLIC_SOURCE_ENV, str(clone))

    assert _public_source_root() == clone.resolve()


def test_private_like_explicit_public_source_override_is_rejected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    private_like_root = REPO_ROOT
    if _looks_like_public_source(REPO_ROOT):
        private_like_root = tmp_path / "private-like-root"
        shutil.copytree(_public_source_root(), private_like_root)
        agents = private_like_root / "AGENTS.md"
        agents.write_text(agents.read_text(encoding="utf-8").replace(PUBLIC_IDENTITY_MARKER, ""), encoding="utf-8")
    monkeypatch.setenv(PUBLIC_SOURCE_ENV, str(private_like_root))

    with pytest.raises(RuntimeError, match=f"{PUBLIC_SOURCE_ENV} does not identify a public package"):
        _public_source_root()
