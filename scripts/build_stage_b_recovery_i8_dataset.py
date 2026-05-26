#!/usr/bin/env python3
"""
Stage B i8 dataset builder scaffold (bounded pre-execution implementation).

This file intentionally does not generate train/val JSONL outputs yet.
Execution behavior remains scaffold-only until explicit follow-on approval.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

RUN_NAME = "stage_b_llama31_8b_base_v1_i8"
PARENT_BASELINE = "stage_b_llama31_8b_base_v1_i3"
TARGETED_TOOLS = ("rg_search", "read_file")

# Doctrine boundaries for i8 scaffolding.
FORBIDDEN_GLOBAL_PRESSURES = (
    "global_negation_heavy_schema_pressure",
    "global_imperative_template_rewrites",
    "wrapper_key_blacklist_flooding",
    "semantic_flattening",
)


@dataclass(frozen=True)
class BuilderInputs:
    stage_b_train_jsonl: Path
    stage_b_val_jsonl: Path
    dataset_summary_json: Path
    eval_heldout_jsonl: Path
    eval_tool_holdout_jsonl: Path
    eval_no_call_jsonl: Path
    eval_adversarial_jsonl: Path
    eval_direct_answer_jsonl: Path
    tool_sources: tuple[Path, ...]


def _now_utc() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _resolve_inputs(args: argparse.Namespace) -> BuilderInputs:
    return BuilderInputs(
        stage_b_train_jsonl=Path(args.stage_b_train_jsonl).resolve(),
        stage_b_val_jsonl=Path(args.stage_b_val_jsonl).resolve(),
        dataset_summary_json=Path(args.dataset_summary_json).resolve(),
        eval_heldout_jsonl=Path(args.eval_heldout_jsonl).resolve(),
        eval_tool_holdout_jsonl=Path(args.eval_tool_holdout_jsonl).resolve(),
        eval_no_call_jsonl=Path(args.eval_no_call_jsonl).resolve(),
        eval_adversarial_jsonl=Path(args.eval_adversarial_jsonl).resolve(),
        eval_direct_answer_jsonl=Path(args.eval_direct_answer_jsonl).resolve(),
        tool_sources=tuple(Path(p).resolve() for p in args.tool_sources),
    )


def _fail_fast_input_validation(inputs: BuilderInputs) -> None:
    required_paths = [
        inputs.stage_b_train_jsonl,
        inputs.stage_b_val_jsonl,
        inputs.dataset_summary_json,
        inputs.eval_heldout_jsonl,
        inputs.eval_tool_holdout_jsonl,
        inputs.eval_no_call_jsonl,
        inputs.eval_adversarial_jsonl,
        inputs.eval_direct_answer_jsonl,
        *inputs.tool_sources,
    ]
    missing = [str(p) for p in required_paths if not p.exists()]
    if missing:
        raise RuntimeError("missing required inputs:\n- " + "\n- ".join(missing))


def _fail_fast_scaffold_boundaries(args: argparse.Namespace) -> None:
    # This explicit fail-fast keeps dataset emission impossible during bounded scaffolding.
    if args.enable_dataset_emission:
        raise RuntimeError(
            "dataset emission is disabled for i8 scaffolding phase; "
            "remove --enable-dataset-emission and request explicit authorization"
        )

    if args.output_root:
        raise RuntimeError(
            "output_root writes are blocked in scaffold mode; "
            "dataset files must not be produced in this phase"
        )


def _build_intervention_plan_stub(*, inputs: BuilderInputs, seed: int) -> dict[str, Any]:
    # SECTION: localized intervention doctrine.
    # Only rg_search/read_file corrective shaping is admissible in i8.
    # TODO(i8-scaffold): Implement targeted row selection once dataset generation is authorized.
    targeted_selection = {
        "status": "todo",
        "targeted_tools": list(TARGETED_TOOLS),
        "selection_strategy": "hybrid-localized",
        "notes": [
            "tool-family-localized corrective replay for rg_search/read_file only",
            "global composition invariants must remain unchanged",
            "no global prompt rewrites are allowed",
        ],
    }

    # SECTION: diversity-preservation doctrine.
    # i8 must not collapse local prompt styles into a single template family.
    # TODO(i8-scaffold): Implement style-bucket and prompt-skeleton guards before emission.
    diversity_controls = {
        "status": "todo",
        "required_checks": [
            "style_bucket_distribution_check",
            "prompt_skeleton_concentration_check",
            "localized_semantic_variety_check",
        ],
        "fail_fast_on": [
            "single_skeleton_dominance",
            "imperative_template_homogenization",
            "tool_family_prompt_style_collapse",
        ],
    }

    # SECTION: anti-overconstraint doctrine.
    # i4/i5 failure mechanism: broad schema pressure caused suppression/flattening.
    # TODO(i8-scaffold): Add bounded lexical shaping with explicit forbidden-pattern scanner.
    anti_overconstraint = {
        "status": "todo",
        "forbidden_global_pressures": list(FORBIDDEN_GLOBAL_PRESSURES),
        "required_localized_cues": [
            "parse_anchor_reinforcement_without_global_negation",
            "object_shape_examples_without_wrapper_blacklist_flooding",
        ],
    }

    # SECTION: contamination governance doctrine.
    # Any heldout/tool_holdout overlap is blocking and aborts generation.
    # TODO(i8-scaffold): Wire overlap audit prior to any write path.
    contamination_controls = {
        "status": "todo",
        "blocking_audits": [
            "heldout_prompt_overlap",
            "heldout_target_overlap",
            "heldout_source_case_overlap",
            "tool_holdout_prompt_overlap",
            "tool_holdout_target_overlap",
            "tool_holdout_source_case_overlap",
        ],
        "on_failure": "abort_before_dataset_emission",
    }

    return {
        "generated_utc": _now_utc(),
        "run_name": RUN_NAME,
        "parent_baseline": PARENT_BASELINE,
        "seed": seed,
        "scaffold_only": True,
        "inputs": {
            "stage_b_train_jsonl": str(inputs.stage_b_train_jsonl),
            "stage_b_val_jsonl": str(inputs.stage_b_val_jsonl),
            "dataset_summary_json": str(inputs.dataset_summary_json),
            "tool_sources": [str(p) for p in inputs.tool_sources],
        },
        "intervention_plan": targeted_selection,
        "diversity_controls": diversity_controls,
        "anti_overconstraint": anti_overconstraint,
        "contamination_controls": contamination_controls,
        "next_implementation_gate": "pending_human_review",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Scaffold for Stage B i8 dataset builder "
            "(parseability recovery test with schema-spill guards)."
        )
    )
    parser.add_argument("--stage-b-train-jsonl", default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_train.jsonl")
    parser.add_argument("--stage-b-val-jsonl", default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_val.jsonl")
    parser.add_argument("--dataset-summary-json", default="/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_summary.json")
    parser.add_argument("--eval-heldout-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/heldout_validation.jsonl")
    parser.add_argument("--eval-tool-holdout-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/tool_holdout.jsonl")
    parser.add_argument("--eval-no-call-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/no_call.jsonl")
    parser.add_argument("--eval-adversarial-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/adversarial.jsonl")
    parser.add_argument("--eval-direct-answer-jsonl", default="/opt/ai-stack/assistant-training/evals/data/canonical_v1/direct_answer.jsonl")
    parser.add_argument(
        "--tool-sources",
        nargs="+",
        default=[
            "/opt/ai-stack/assistant-training/data/tool_ft_allaliases_20260525_from_qual_reports_freq.jsonl",
            "/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_aug_rebalanced_20260417T104659Z.jsonl",
            "/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_aug_focus_rebalanced_20260417T104747Z.jsonl",
        ],
    )
    parser.add_argument("--seed", type=int, default=20260526)
    parser.add_argument(
        "--output-root",
        default="",
        help="Blocked in scaffold phase; present only for future implementation parity.",
    )
    parser.add_argument(
        "--enable-dataset-emission",
        action="store_true",
        help="Blocked in scaffold phase; included as explicit fail-fast boundary.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    _fail_fast_scaffold_boundaries(args)

    inputs = _resolve_inputs(args)
    _fail_fast_input_validation(inputs)

    plan = _build_intervention_plan_stub(inputs=inputs, seed=int(args.seed))
    print(json.dumps(plan, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
