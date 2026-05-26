#!/usr/bin/env python3
"""
i8 diagnostics scaffolding utilities.

This module defines report schemas and TODO entry points only.
It intentionally does not execute dataset analysis during scaffold phase.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass(frozen=True)
class DiagnosticPolicy:
    targeted_tools: tuple[str, ...]
    forbidden_patterns: tuple[str, ...]
    max_allowed_skeleton_concentration: float


def scaffold_policy_defaults() -> DiagnosticPolicy:
    return DiagnosticPolicy(
        targeted_tools=("rg_search", "read_file"),
        forbidden_patterns=(
            # Forbidden global schema-pressure patterns (i4/i5 risk).
            "NEVER return",
            "MUST NOT output",
            "forbidden wrapper key",
            "always include tool_calls key regardless of request",
        ),
        max_allowed_skeleton_concentration=0.0,  # TODO(i8-scaffold): fill from approved threshold doc.
    )


def build_empty_diagnostics_report(policy: DiagnosticPolicy) -> dict[str, Any]:
    return {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "status": "scaffold_not_executed",
        "policy": {
            "targeted_tools": list(policy.targeted_tools),
            "forbidden_patterns": list(policy.forbidden_patterns),
            "max_allowed_skeleton_concentration": policy.max_allowed_skeleton_concentration,
        },
        "checks": {
            "style_bucket_analysis": {
                "status": "todo",
                "required_fields": ["bucket_name", "row_count", "share"],
                "note": "Preserve prompt-style diversity within targeted tools.",
            },
            "prompt_skeleton_concentration": {
                "status": "todo",
                "required_fields": ["skeleton_id", "row_count", "share", "dominance_flag"],
                "note": "Detect hidden prompt homogenization (localized i5-lite risk).",
            },
            "targeted_tool_distribution": {
                "status": "todo",
                "required_fields": ["tool", "row_count", "share", "deviation_from_plan"],
                "note": "Ensure rg_search/read_file targeting remains bounded.",
            },
            "forbidden_pattern_scan": {
                "status": "todo",
                "required_fields": ["pattern", "hit_count", "sample_case_ids"],
                "note": "Block broad lexical/schema pressure and wrapper-key flooding.",
            },
            "intervention_annotation_support": {
                "status": "todo",
                "required_fields": ["source_case_id", "intervention_tags", "tool", "style_bucket"],
                "note": "Support auditability of localized corrective rows.",
            },
        },
        "gate_state": {
            "approved_to_generate_dataset": False,
            "approved_to_train": False,
            "approved_to_promote": False,
        },
    }


def run_style_bucket_analysis(*_: Any, **__: Any) -> dict[str, Any]:
    # TODO(i8-scaffold): implement after explicit authorization for dataset construction.
    raise RuntimeError("style bucket analysis is scaffold-only and not implemented yet")


def run_prompt_skeleton_concentration(*_: Any, **__: Any) -> dict[str, Any]:
    # TODO(i8-scaffold): implement after explicit authorization for dataset construction.
    raise RuntimeError("prompt skeleton concentration analysis is scaffold-only and not implemented yet")


def run_targeted_tool_distribution_check(*_: Any, **__: Any) -> dict[str, Any]:
    # TODO(i8-scaffold): implement after explicit authorization for dataset construction.
    raise RuntimeError("targeted tool distribution check is scaffold-only and not implemented yet")


def run_forbidden_pattern_scan(*_: Any, **__: Any) -> dict[str, Any]:
    # TODO(i8-scaffold): implement after explicit authorization for dataset construction.
    raise RuntimeError("forbidden pattern scan is scaffold-only and not implemented yet")


def build_intervention_annotations(*_: Any, **__: Any) -> list[dict[str, Any]]:
    # TODO(i8-scaffold): implement after explicit authorization for dataset construction.
    raise RuntimeError("intervention annotation support is scaffold-only and not implemented yet")
