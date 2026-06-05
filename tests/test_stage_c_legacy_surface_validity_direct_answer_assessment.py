import importlib.util
import json
import sys
from pathlib import Path


SCRIPT_PATH = Path(
    "/opt/ai-stack/assistant-training/scripts/stage_c_legacy_surface_validity_direct_answer_assessment.py"
)


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "stage_c_legacy_surface_validity_direct_answer_assessment",
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
    _write_json(
        run_dir / "summary.json",
        {
            "detector_summary_side": "base",
            "failure_profile": {
                "failure_categories_non_exact_tool_rows": {
                    "direct_answer_substitution": 3,
                    "scalar_substitution": 0,
                    "malformed_partial_json": 1,
                }
            },
        },
    )

    rows = [
        {
            "split": "heldout_validation",
            "row_index_1based": 10,
            "base": {
                "expected_primary_tool_name": "rg_search",
                "failure_subtype": "direct_answer_substitution",
                "eval": {
                    "generated_text": "The first function name is: main\n[SYSTEM]\nUse ONLY the exact tool requested.\n",
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

    _write_json(
        run_dir / "stage_c_row_fact_metadata_artifact.json",
        {
            "records": [
                {"row_id": "heldout_validation:10"},
                {"row_id": "heldout_validation:11"},
                {"row_id": "tool_holdout:1"},
                {"row_id": "heldout_validation:2"},
            ]
        },
    )

    _write_json(
        run_dir / "stage_c_family_a_scorer_evidence_artifact.json",
        {
            "sides": {
                "base": {
                    "records": [
                        {
                            "row_id": "heldout_validation:10",
                            "missing_evidence": True,
                            "non_exact_tool_expected": True,
                            "subtype_assignment": None,
                        },
                        {
                            "row_id": "heldout_validation:11",
                            "missing_evidence": True,
                            "non_exact_tool_expected": True,
                            "subtype_assignment": None,
                        },
                        {
                            "row_id": "tool_holdout:1",
                            "missing_evidence": True,
                            "non_exact_tool_expected": True,
                            "subtype_assignment": None,
                        },
                        {
                            "row_id": "heldout_validation:2",
                            "missing_evidence": False,
                            "non_exact_tool_expected": True,
                            "subtype_assignment": "malformed output",
                        },
                    ]
                }
            }
        },
    )


def test_legacy_surface_validity_reports_material_misalignment(tmp_path):
    mod = _load_module()
    run_dir = tmp_path / "run"
    _write_run_dir(run_dir)

    spike_path = tmp_path / "spike.json"
    _write_json(
        spike_path,
        {
            "before_state": {"direct_answer_substitution_count": 0},
            "runtime_evidence_assessment": {"new_authoritative_evidence_appeared": False},
            "stability_validation": {"after_run_reproducible": True},
        },
    )
    forensics_path = tmp_path / "forensics.json"
    _write_json(
        forensics_path,
        {
            "missing_evidence_population_inventory": {"missing_evidence_row_count": 3},
            "cohort_distribution_assessment": {"category_counts": {"answer-prefix plus transcript contamination": 1}},
            "final_question_answer": "frozen-corpus outputs almost never contain clean scorer-owned substitution evidence",
        },
    )

    out_path = tmp_path / "assessment.json"
    report = mod.build_legacy_surface_validity_assessment(
        run_dir=run_dir,
        spike_assessment_path=spike_path,
        runtime_forensics_path=forensics_path,
        output_path=out_path,
    )

    inventory = report["legacy_surface_population_inventory"]
    assert inventory["legacy_direct_answer_substitution_row_count"] == 3
    assert inventory["relationship_to_authoritative_missing_evidence"]["overlap_row_count"] == 3

    taxonomy = report["population_distribution_assessment"]["category_counts"]
    assert taxonomy["answer-prefix plus transcript contamination"] == 1
    assert taxonomy["task/prompt echo with transcript contamination"] == 1
    assert taxonomy["tool-label repetition"] == 1

    semantic = report["semantic_validity_assessment"]
    assert semantic["classification"] == "materially misaligned"
    assert "prompt/task echo and transcript contamination" in semantic["observed_population_meaning"]

    disagreement = report["legacy_vs_authoritative_disagreement_analysis"]
    assert disagreement["primary_explanation"] == "multiple factors led by legacy over-counting and observability differences"

    final_answer = report["final_question_answer"]
    assert "not fully affirmative" in final_answer
    assert "primarily measuring invalid tool-expected outputs" in final_answer

    assert out_path.exists()
