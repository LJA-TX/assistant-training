#!/usr/bin/env python3
"""
i8 preflight validation integration scaffold.

This script wires required validation flow points but does not execute
dataset-generation or training-time workflows in this phase.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from i8_diagnostics_scaffold import build_empty_diagnostics_report, scaffold_policy_defaults


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _require_paths_exist(paths: list[Path]) -> None:
    missing = [str(p) for p in paths if not p.exists()]
    if missing:
        raise RuntimeError("missing required path(s):\n- " + "\n- ".join(missing))


def _scaffold_validation_plan(args: argparse.Namespace) -> dict[str, Any]:
    policy = scaffold_policy_defaults()

    return {
        "report_version": "1.0",
        "generated_utc": _now_utc(),
        "iteration": "stage_b_llama31_8b_base_v1_i8",
        "status": "scaffold_not_executed",
        "required_flow_points": [
            {
                "name": "overlap_audit",
                "status": "planned_not_run",
                "inputs": [
                    str(Path(args.eval_heldout_jsonl).resolve()),
                    str(Path(args.eval_tool_holdout_jsonl).resolve()),
                ],
                "blocking": True,
            },
            {
                "name": "diversity_checks",
                "status": "planned_not_run",
                "subchecks": [
                    "style_bucket_analysis",
                    "prompt_skeleton_concentration",
                    "localized_semantic_variety",
                ],
                "blocking": True,
            },
            {
                "name": "forbidden_pattern_checks",
                "status": "planned_not_run",
                "subchecks": [
                    "global_negation_pressure_scan",
                    "imperative_template_rewrite_scan",
                    "wrapper_key_blacklist_flooding_scan",
                ],
                "blocking": True,
            },
            {
                "name": "tool_family_distribution_checks",
                "status": "planned_not_run",
                "subchecks": [
                    "targeted_tool_distribution",
                    "non_target_tool_envelope_stability",
                ],
                "blocking": True,
            },
            {
                "name": "spill_guard_interpretation_support",
                "status": "planned_not_run",
                "subchecks": [
                    "payload_not_parsed_vs_payload_not_object_shift_readout",
                    "missing_tool_calls_coupling_readout",
                ],
                "blocking": False,
            },
        ],
        "diagnostics_stub": build_empty_diagnostics_report(policy),
        "approval_state": {
            "approved_to_run": False,
            "approved_to_generate_dataset": False,
            "approved_to_train": False,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaffold i8 preflight validation plan (no execution).")
    parser.add_argument("--eval-heldout-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/heldout_validation.jsonl")
    parser.add_argument("--eval-tool-holdout-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/tool_holdout.jsonl")
    parser.add_argument("--manifest-path", default="/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_i8_preflight_validation_plan.template.json")
    parser.add_argument(
        "--write-plan",
        action="store_true",
        help="Optional write path for scaffold plan template. Defaults to stdout only.",
    )
    parser.add_argument(
        "--execute-checks",
        action="store_true",
        help="Forbidden in scaffold phase. Included only as an explicit fail-fast boundary.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.execute_checks:
        raise RuntimeError("check execution is not authorized in scaffold phase")

    heldout = Path(args.eval_heldout_jsonl).resolve()
    tool_holdout = Path(args.eval_tool_holdout_jsonl).resolve()
    _require_paths_exist([heldout, tool_holdout])

    plan = _scaffold_validation_plan(args)

    if args.write_plan:
        out = Path(args.manifest_path).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps(plan, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
