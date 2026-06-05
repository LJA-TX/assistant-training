import importlib.util
import json
import sys
from pathlib import Path


SCRIPT_PATH = Path(
    "/opt/ai-stack/assistant-training/scripts/"
    "stage_c_runtime_output_forensics_direct_answer_missing_evidence.py"
)


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "stage_c_runtime_output_forensics_direct_answer_missing_evidence",
        str(SCRIPT_PATH),
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_run_dir(run_dir: Path):
    run_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "detector_summary_side": "base",
        "failure_profile": {
            "failure_categories_non_exact_tool_rows": {
                "direct_answer_substitution": 3,
                "scalar_substitution": 0,
                "malformed_partial_json": 1,
            }
        },
    }
    _write_json(run_dir / "summary.json", summary)

    rows = [
        {
            "split": "heldout_validation",
            "row_index_1based": 10,
            "base": {
                "expected_primary_tool_name": "rg_search",
                "failure_subtype": "direct_answer_substitution",
                "eval": {
                    "generated_text": (
                        "The first function name is: main\n[SYSTEM]\nUse ONLY the exact tool requested.\n"
                    ),
                    "primary_class": "invalid_json",
                    "parse_mode": "invalid",
                    "schema_reason": "payload_not_parsed",
                },
            },
        },
        {
            "split": "heldout_validation",
            "row_index_1based": 11,
            "base": {
                "expected_primary_tool_name": "read_file",
                "failure_subtype": "direct_answer_substitution",
                "eval": {
                    "generated_text": "Tool: python\nTool: python\nTool: python\n",
                    "primary_class": "invalid_json",
                    "parse_mode": "invalid",
                    "schema_reason": "payload_not_parsed",
                },
            },
        },
        {
            "split": "tool_holdout",
            "row_index_1based": 1,
            "base": {
                "expected_primary_tool_name": "find_files",
                "failure_subtype": "direct_answer_substitution",
                "eval": {
                    "generated_text": (
                        "Use find_files with root /tmp and pattern service.py.\n[SYSTEM]\nUse ONLY the exact tool requested.\n"
                    ),
                    "primary_class": "invalid_json",
                    "parse_mode": "invalid",
                    "schema_reason": "payload_not_parsed",
                },
            },
        },
        {
            "split": "heldout_validation",
            "row_index_1based": 2,
            "base": {
                "expected_primary_tool_name": "rg_search",
                "failure_subtype": "malformed_partial_json",
                "eval": {
                    "generated_text": "Use rg_search in /tmp for string \"tool_calls\".\n[SYSTEM]\n...",
                    "primary_class": "invalid_json",
                    "parse_mode": "invalid",
                    "schema_reason": "payload_not_parsed",
                },
            },
        },
    ]
    with (run_dir / "comparison_rows.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")

    row_fact_records = [
        {
            "row_id": "heldout_validation:10",
            "split_id": "heldout_validation",
            "membership_markers": {"family_a_tool_expected_eligible": True},
        },
        {
            "row_id": "heldout_validation:11",
            "split_id": "heldout_validation",
            "membership_markers": {"family_a_tool_expected_eligible": True},
        },
        {
            "row_id": "tool_holdout:1",
            "split_id": "tool_holdout",
            "membership_markers": {"family_a_tool_expected_eligible": True},
        },
        {
            "row_id": "heldout_validation:2",
            "split_id": "heldout_validation",
            "membership_markers": {"family_a_tool_expected_eligible": True},
        },
    ]
    _write_json(
        run_dir / "stage_c_row_fact_metadata_artifact.json",
        {"records": row_fact_records},
    )

    family_a_records = [
        {
            "row_id": "heldout_validation:10",
            "tool_expected_eligibility": True,
            "excluded": False,
            "primary_outcome": "invalid_json",
            "exact_valid": False,
            "non_exact_tool_expected": True,
            "subtype_assignment": None,
            "missing_evidence": True,
            "missing_evidence_reasons": [
                "current canonical evaluator does not emit approved direct-answer or scalar substitution evidence"
            ],
        },
        {
            "row_id": "heldout_validation:11",
            "tool_expected_eligibility": True,
            "excluded": False,
            "primary_outcome": "invalid_json",
            "exact_valid": False,
            "non_exact_tool_expected": True,
            "subtype_assignment": None,
            "missing_evidence": True,
            "missing_evidence_reasons": [
                "current canonical evaluator does not emit approved direct-answer or scalar substitution evidence"
            ],
        },
        {
            "row_id": "tool_holdout:1",
            "tool_expected_eligibility": True,
            "excluded": False,
            "primary_outcome": "invalid_json",
            "exact_valid": False,
            "non_exact_tool_expected": True,
            "subtype_assignment": None,
            "missing_evidence": True,
            "missing_evidence_reasons": [
                "current canonical evaluator does not emit approved direct-answer or scalar substitution evidence"
            ],
        },
        {
            "row_id": "heldout_validation:2",
            "tool_expected_eligibility": True,
            "excluded": False,
            "primary_outcome": "invalid_json",
            "exact_valid": False,
            "non_exact_tool_expected": True,
            "subtype_assignment": "malformed output",
            "missing_evidence": False,
            "missing_evidence_reasons": [],
        },
    ]
    _write_json(
        run_dir / "stage_c_family_a_scorer_evidence_artifact.json",
        {
            "sides": {
                "base": {
                    "records": family_a_records,
                }
            }
        },
    )

    _write_json(
        run_dir / "stage_c_package1c_passive_reconciliation_report.json",
        {
            "reconciled_surfaces": [
                {
                    "surface_id": "direct_answer_substitution_count",
                    "reconciliation_status": "requires_future_migration",
                }
            ]
        },
    )
    _write_json(
        run_dir / "stage_c_package1d_migration_readiness_assessment.json",
        {
            "compatibility_surface_assessments": [
                {
                    "surface_id": "direct_answer_substitution_count",
                    "readiness_state": "migration-blocked",
                }
            ]
        },
    )


def test_runtime_forensics_reports_artifact_based_missing_evidence_categories(tmp_path):
    mod = _load_module()
    run_dir = tmp_path / "run"
    _write_run_dir(run_dir)

    spike_path = tmp_path / "spike.json"
    _write_json(
        spike_path,
        {
            "before_state": {"missing_evidence_count": 3},
            "stability_validation": {"after_run_reproducible": True},
            "runtime_evidence_assessment": {"new_authoritative_evidence_appeared": False},
        },
    )

    out_path = tmp_path / "assessment.json"
    report = mod.build_runtime_forensics(
        run_dir=run_dir,
        spike_assessment_path=spike_path,
        output_path=out_path,
    )

    inventory = report["missing_evidence_population_inventory"]
    assert inventory["missing_evidence_row_count"] == 3
    assert inventory["ambiguous_row_count"] == 1
    assert inventory["structurally_incapable_row_count"] == 2
    assert inventory["evidence_availability_patterns"]["looks_like_tool_intent_missing_count"] == 0
    assert inventory["evidence_availability_patterns"]["scalar_candidate_missing_count"] == 0

    category_counts = report["cohort_distribution_assessment"]["category_counts"]
    assert category_counts["answer-prefix plus transcript contamination"] == 1
    assert category_counts["task/prompt echo with transcript contamination"] == 1
    assert category_counts["tool-label repetition"] == 1

    gap = report["legacy_vs_authoritative_gap_analysis"]
    assert gap["authoritative_surface"]["authoritative_direct_answer_substitution_count"] == 0
    assert gap["authoritative_surface"]["authoritative_malformed_output_count"] == 1
    assert gap["legacy_failure_profile"]["direct_answer_substitution_count"] == 3

    assert "frozen-corpus outputs almost never contain clean scorer-owned substitution evidence" in report[
        "final_question_answer"
    ]
    assert out_path.exists()
