from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any


REPO_ROOT_ENV = "ASSISTANT_TRAINING_REPO_ROOT"

_SCRIPT_ROLE_PATHS: dict[str, str] = {
    "eval_canonical_manifest": "scripts/eval_canonical_manifest.py",
    "post_eval_collapse_detector": "scripts/post_eval_collapse_detector.py",
    "stage_c1_evaluator_foundation": "scripts/stage_c1_evaluator_foundation.py",
    "stage_c2_family_state_reconciliation_foundation": "scripts/stage_c2_family_state_reconciliation_foundation.py",
    "stage_c3_evaluator_runtime_integration": "scripts/stage_c3_evaluator_runtime_integration.py",
    "stage_c4_real_output_ingestion": "scripts/stage_c4_real_output_ingestion.py",
    "stage_c5_scoring_path_integration": "scripts/stage_c5_scoring_path_integration.py",
    "stage_c6_scoring_report_integration": "scripts/stage_c6_scoring_report_integration.py",
    "stage_c8_non_authoritative_detector_projection_adapter": (
        "scripts/stage_c8_non_authoritative_detector_projection_adapter.py"
    ),
    "stage_c_e1_prompt_trace_evidence_creation": "scripts/stage_c_e1_prompt_trace_evidence_creation.py",
}

_ARTIFACT_ROLE_PATHS: dict[str, str] = {
    "canonical_eval_manifest": "evals/canonical_eval_manifest_v1.json",
    "wp8_fixture_root": "manifests/reports/stage_b_wp8_validation/fixtures",
    "stage_b_v1_threshold_profile": "manifests/reports/stage_b_v1_threshold_profile.json",
    "stage_c3_baseline_artifacts_dir": "reports/stage_c3/baseline_contract_artifacts",
    "stage_c4_contract_artifacts_dir": "reports/stage_c4/contract_artifacts",
    "stage_c5_contract_artifacts_dir": "reports/stage_c5/contract_artifacts",
    "stage_c6_reporting_artifacts_dir": "reports/stage_c6/reporting_artifacts",
    "stage_c8_projection_artifacts_dir": "reports/stage_c8/projection_artifacts",
    "stage_c4_sample_output_records": "reports/stage_c4/input/stage_c4_sample_output_records.jsonl",
    "stage_c5_sample_output_records": "reports/stage_c5/input/stage_c5_sample_output_records.jsonl",
    "stage_c6_sample_output_records": "reports/stage_c6/input/stage_c6_sample_output_records.jsonl",
}

_OPTIONAL_OUTPUT_ARTIFACT_ROLES = {
    "stage_c3_baseline_artifacts_dir",
    "stage_c4_contract_artifacts_dir",
    "stage_c5_contract_artifacts_dir",
    "stage_c6_reporting_artifacts_dir",
    "stage_c8_projection_artifacts_dir",
}

_FIXTURE_REGISTRY: dict[str, dict[str, Any]] = {
    "fixture_family/wp8_validation": {
        "artifact_id": "fixture_family/wp8_validation",
        "artifact_role": "wp8_fixture_root",
        "kind": "fixture_family",
        "active_surface": True,
        "sha256_mode": "tree",
        "recorded_source_role": "wp8_fixture_root",
        "recorded_source_kind": "fixture_path",
        "historical_source_kind": "fixture_path",
        "preservation_reason": (
            "Active evaluator fixtures remain under manifests/reports until fixture extraction is separately authorized."
        ),
        "consumer_scripts": (
            "stage_c1_evaluator_foundation",
            "stage_c3_evaluator_runtime_integration",
            "stage_c4_real_output_ingestion",
            "stage_c5_scoring_path_integration",
            "stage_c6_scoring_report_integration",
            "stage_c8_non_authoritative_detector_projection_adapter",
        ),
        "consumer_tests": (
            "test_stage_c1_evaluator_foundation",
            "test_stage_c3_evaluator_runtime_integration",
            "test_stage_c4_real_output_ingestion",
            "test_stage_c5_scoring_path_integration",
            "test_stage_c6_scoring_report_integration",
            "test_stage_c8_non_authoritative_detector_projection_adapter",
        ),
        "notes": "Active WP8 validation fixture corpus used by the Stage C evaluator chain.",
    },
    "threshold_profile/stage_b_v1": {
        "artifact_id": "threshold_profile/stage_b_v1",
        "artifact_role": "stage_b_v1_threshold_profile",
        "kind": "threshold_profile",
        "active_surface": True,
        "sha256_mode": "file",
        "recorded_source_role": "stage_b_v1_threshold_profile",
        "recorded_source_kind": "report_path",
        "historical_source_kind": "report_path",
        "preservation_reason": (
            "The active threshold profile remains under manifests/reports until fixture/sample extraction is authorized."
        ),
        "consumer_scripts": (
            "eval_canonical_manifest",
            "stage_c8_non_authoritative_detector_projection_adapter",
        ),
        "consumer_tests": (
            "test_eval_canonical_manifest",
            "test_stage_c8_non_authoritative_detector_projection_adapter",
        ),
        "notes": "Active threshold profile consumed by the Stage C evaluator compatibility slice.",
    },
    "sample_output/stage_c4_v1": {
        "artifact_id": "sample_output/stage_c4_v1",
        "artifact_role": "stage_c4_sample_output_records",
        "kind": "sample_artifact",
        "active_surface": True,
        "sha256_mode": "file",
        "recorded_source_role": "stage_c4_sample_output_records",
        "recorded_source_kind": "report_path",
        "historical_source_kind": "report_path",
        "preservation_reason": (
            "Stage C4 sample outputs remain in the tracked report tree until sample extraction is authorized."
        ),
        "consumer_scripts": ("stage_c4_real_output_ingestion",),
        "consumer_tests": ("test_stage_c4_real_output_ingestion",),
        "notes": "Active Stage C4 sample output records kept in-place for compatibility adoption.",
    },
    "sample_output/stage_c5_v1": {
        "artifact_id": "sample_output/stage_c5_v1",
        "artifact_role": "stage_c5_sample_output_records",
        "kind": "sample_artifact",
        "active_surface": True,
        "sha256_mode": "file",
        "recorded_source_role": "stage_c5_sample_output_records",
        "recorded_source_kind": "report_path",
        "historical_source_kind": "report_path",
        "preservation_reason": (
            "Stage C5 sample outputs remain in the tracked report tree until sample extraction is authorized."
        ),
        "consumer_scripts": ("stage_c5_scoring_path_integration", "stage_c6_scoring_report_integration"),
        "consumer_tests": ("test_stage_c5_scoring_path_integration", "test_stage_c6_scoring_report_integration"),
        "notes": "Active Stage C5 sample output records kept in-place for compatibility adoption.",
    },
    "sample_output/stage_c6_v1": {
        "artifact_id": "sample_output/stage_c6_v1",
        "artifact_role": "stage_c6_sample_output_records",
        "kind": "sample_artifact",
        "active_surface": True,
        "sha256_mode": "file",
        "recorded_source_role": "stage_c6_sample_output_records",
        "recorded_source_kind": "report_path",
        "historical_source_kind": "report_path",
        "preservation_reason": (
            "Stage C6 sample outputs remain in the tracked report tree until sample extraction is authorized."
        ),
        "consumer_scripts": (
            "stage_c6_scoring_report_integration",
            "stage_c8_non_authoritative_detector_projection_adapter",
        ),
        "consumer_tests": (
            "test_stage_c6_scoring_report_integration",
            "test_stage_c8_non_authoritative_detector_projection_adapter",
        ),
        "notes": "Active Stage C6 sample output records kept in-place for compatibility adoption.",
    },
}


def _has_required_sentinels(candidate: Path) -> bool:
    return (
        (candidate / "AGENTS.md").is_file()
        and (candidate / "docs" / "goal_charter_v5a.md").is_file()
        and (candidate / "scripts").is_dir()
        and (candidate / "evals").is_dir()
    )


@lru_cache(maxsize=None)
def _resolve_repo_root_cached(env_value: str | None, start_path_text: str) -> Path:
    if env_value:
        candidate = Path(env_value).expanduser().resolve()
        if _has_required_sentinels(candidate):
            return candidate
        raise RuntimeError(
            f"{REPO_ROOT_ENV}={candidate} does not look like the assistant-training repository root"
        )

    start_path = Path(start_path_text).resolve()
    if start_path.is_file():
        start_path = start_path.parent

    for candidate in (start_path, *start_path.parents):
        if _has_required_sentinels(candidate):
            return candidate

    raise RuntimeError(f"unable to resolve repository root from {start_path_text}")


def resolve_repo_root(start: Path | None = None) -> Path:
    env_value = os.environ.get(REPO_ROOT_ENV)
    start_path = Path(start).resolve() if start is not None else Path(__file__).resolve()
    return _resolve_repo_root_cached(env_value, str(start_path))


def _resolve_role_path(role: str, mapping: dict[str, str], role_kind: str) -> Path:
    try:
        relative_path = mapping[role]
    except KeyError as exc:
        available = ", ".join(sorted(mapping))
        raise KeyError(f"unknown {role_kind} role {role!r}; available roles: {available}") from exc
    return resolve_repo_root() / relative_path


def resolve_script_path(role: str) -> Path:
    return _resolve_role_path(role, _SCRIPT_ROLE_PATHS, "script")


def resolve_artifact_path(role: str) -> Path:
    return _resolve_role_path(role, _ARTIFACT_ROLE_PATHS, "artifact")


def resolve_fixture_root(role: str = "wp8_fixture_root") -> Path:
    return resolve_artifact_path(role)


def iter_resolved_role_paths() -> dict[str, Path]:
    resolved: dict[str, Path] = {}
    for role in sorted(_SCRIPT_ROLE_PATHS):
        resolved[f"script:{role}"] = resolve_script_path(role)
    for role in sorted(_ARTIFACT_ROLE_PATHS):
        resolved[f"artifact:{role}"] = resolve_artifact_path(role)
    return resolved


def validate_role_maps() -> dict[str, dict[str, Path]]:
    # Optional output roles are allowed to be absent before the corresponding
    # Stage C write step runs, but validation must still surface that absence.
    resolved = iter_resolved_role_paths()
    root = resolve_repo_root()
    present: dict[str, Path] = {}
    optional_missing: dict[str, Path] = {}
    missing_required: dict[str, Path] = {}
    for name, path in resolved.items():
        if path.exists():
            present[name] = path
            continue
        if name.startswith("artifact:") and name.split(":", 1)[1] in _OPTIONAL_OUTPUT_ARTIFACT_ROLES:
            if not path.is_absolute() or not path.parent.is_relative_to(root):
                missing_required[name] = path
            else:
                optional_missing[name] = path
            continue
        missing_required[name] = path
    if missing_required:
        details = ", ".join(
            f"{name} -> {path}" for name, path in sorted(missing_required.items())
        )
        raise RuntimeError(f"declared compatibility roles do not resolve: {details}")
    return {
        "all_roles": resolved,
        "present_roles": present,
        "optional_missing_roles": optional_missing,
    }


def fixture_registry() -> dict[str, dict[str, Any]]:
    registry: dict[str, dict[str, Any]] = {}
    for artifact_id, record in _FIXTURE_REGISTRY.items():
        resolved = dict(record)
        resolved["current_path"] = resolve_artifact_path(record["artifact_role"])
        resolved["recorded_source_path"] = resolve_artifact_path(record["recorded_source_role"])
        registry[artifact_id] = resolved
    return registry


def validate_fixture_registry() -> dict[str, dict[str, Any]]:
    registry = fixture_registry()
    missing_paths: dict[str, Path] = {}
    unknown_script_roles: list[str] = []
    missing_tests: list[str] = []
    tests_root = resolve_repo_root() / "tests"

    for artifact_id, record in registry.items():
        current_path = Path(record["current_path"])
        recorded_source_path = Path(record["recorded_source_path"])
        if not current_path.exists():
            missing_paths[f"{artifact_id}:current_path"] = current_path
        if not recorded_source_path.exists():
            missing_paths[f"{artifact_id}:recorded_source_path"] = recorded_source_path
        for script_role in record["consumer_scripts"]:
            if script_role not in _SCRIPT_ROLE_PATHS:
                unknown_script_roles.append(f"{artifact_id}:{script_role}")
        for test_name in record["consumer_tests"]:
            test_path = tests_root / f"{test_name}.py"
            if not test_path.exists():
                missing_tests.append(f"{artifact_id}:{test_path}")

    errors: list[str] = []
    if missing_paths:
        details = ", ".join(f"{name} -> {path}" for name, path in sorted(missing_paths.items()))
        errors.append(f"missing registry paths: {details}")
    if unknown_script_roles:
        errors.append("unknown consumer script roles: " + ", ".join(sorted(unknown_script_roles)))
    if missing_tests:
        errors.append("missing consumer tests: " + ", ".join(sorted(missing_tests)))
    if errors:
        raise RuntimeError("; ".join(errors))
    return registry
