import importlib.util
import json
import sys
from pathlib import Path


PACKAGE1C_SCRIPT_PATH = Path(
    "/opt/ai-stack/assistant-training/scripts/stage_c_package1c_passive_reconciliation_surface.py"
)
PACKAGE1D_SCRIPT_PATH = Path(
    "/opt/ai-stack/assistant-training/scripts/stage_c_package1d_migration_readiness_assessment.py"
)


def _load_module(script_path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, str(script_path))
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


def _write_json(path: Path, payload):
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_run_dir(run_dir: Path, package1c_mod):
    run_dir.mkdir(parents=True, exist_ok=True)

    summary = {
        "metrics": {
            "aggregate": {
                "invalid_json": 0.1,
            },
        },
        "failure_profile": {
            "tool_expected_rows": 3,
            "non_exact_tool_rows": 2,
            "failure_categories_non_exact_tool_rows": {
                "direct_answer_substitution": 1,
                "scalar_substitution": 0,
                "malformed_partial_json": 0,
                "near_canonical_wrapper_or_envelope_drift": 1,
                "other_non_exact": 0,
            },
            "read_file_exact_valid": {
                "count": 1,
                "rows": 2,
                "rate": 0.5,
            },
            "read_file_symbol_name_exact_valid": {
                "count": 1,
                "rows": 1,
                "rate": 1.0,
            },
            "anchor_exact_share": {
                "literal_tool_calls": 0.5,
                "paraphrastic_tool_call": 0.0,
                "schema_paraphrase": 0.0,
                "no_anchor_phrase": 0.5,
            },
        },
    }

    row_fact = {
        "report_version": "stage_c_package1_row_facts_v1",
        "artifact_scope": "authoritative_live_canonical_eval_row_facts",
        "row_fact_count": 3,
        "records": [
            {
                "row_id": "heldout_validation:1",
                "split_id": "heldout_validation",
                "excluded": False,
                "expected_tool_name": "read_file",
                "membership_markers": {
                    "family_a_tool_expected_eligible": True,
                    "family_b1_read_file_eligible": True,
                    "family_b1_symbol_name_member": None,
                    "family_b2_anchor_eligible": False,
                    "family_b2_no_anchor_member": None,
                    "family_b2_anchor_category": None,
                },
                "ownership_markers": {
                    "symbol_name_membership_owner": None,
                    "anchor_assignment_owner": None,
                    "anchor_taxonomy_owner": None,
                    "conflicting_ownership_markers": False,
                    "ownership_conflict_reasons": [],
                },
                "provenance": {
                    "row_source": "canonical_eval_live_evaluator",
                    "dataset_id": "canonical_eval_manifest_v1",
                    "dataset_version": "v1",
                    "extraction_timestamp_utc": "2026-06-04T00:00:00Z",
                    "evidence_digest": "digest-1",
                },
                "denominator_provenance": {
                    "eligible_population_source": "canonical_manifest_declared_eval_population",
                    "non_exact_population_source": "stage_c_family_a_scorer_evidence_artifact",
                    "read_file_population_source": "declared_expected_tool_identity",
                    "symbol_name_population_source": None,
                    "anchor_population_source": None,
                    "no_anchor_population_source": None,
                },
                "evidence": {
                    "source_case_id": "case-a",
                    "row_index_1based": 1,
                    "prompt_hint": "report one symbol name",
                },
            },
            {
                "row_id": "heldout_validation:2",
                "split_id": "heldout_validation",
                "excluded": False,
                "expected_tool_name": "read_file",
                "membership_markers": {
                    "family_a_tool_expected_eligible": True,
                    "family_b1_read_file_eligible": True,
                    "family_b1_symbol_name_member": None,
                    "family_b2_anchor_eligible": False,
                    "family_b2_no_anchor_member": None,
                    "family_b2_anchor_category": None,
                },
                "ownership_markers": {
                    "symbol_name_membership_owner": None,
                    "anchor_assignment_owner": None,
                    "anchor_taxonomy_owner": None,
                    "conflicting_ownership_markers": False,
                    "ownership_conflict_reasons": [],
                },
                "provenance": {
                    "row_source": "canonical_eval_live_evaluator",
                    "dataset_id": "canonical_eval_manifest_v1",
                    "dataset_version": "v1",
                    "extraction_timestamp_utc": "2026-06-04T00:00:00Z",
                    "evidence_digest": "digest-2",
                },
                "denominator_provenance": {
                    "eligible_population_source": "canonical_manifest_declared_eval_population",
                    "non_exact_population_source": "stage_c_family_a_scorer_evidence_artifact",
                    "read_file_population_source": "declared_expected_tool_identity",
                    "symbol_name_population_source": None,
                    "anchor_population_source": None,
                    "no_anchor_population_source": None,
                },
                "evidence": {
                    "source_case_id": "case-b",
                    "row_index_1based": 2,
                },
            },
            {
                "row_id": "tool_holdout:1",
                "split_id": "tool_holdout",
                "excluded": False,
                "expected_tool_name": "find_files",
                "membership_markers": {
                    "family_a_tool_expected_eligible": True,
                    "family_b1_read_file_eligible": False,
                    "family_b1_symbol_name_member": None,
                    "family_b2_anchor_eligible": False,
                    "family_b2_no_anchor_member": None,
                    "family_b2_anchor_category": None,
                },
                "ownership_markers": {
                    "symbol_name_membership_owner": None,
                    "anchor_assignment_owner": None,
                    "anchor_taxonomy_owner": None,
                    "conflicting_ownership_markers": False,
                    "ownership_conflict_reasons": [],
                },
                "provenance": {
                    "row_source": "canonical_eval_live_evaluator",
                    "dataset_id": "canonical_eval_manifest_v1",
                    "dataset_version": "v1",
                    "extraction_timestamp_utc": "2026-06-04T00:00:00Z",
                    "evidence_digest": "digest-3",
                },
                "denominator_provenance": {
                    "eligible_population_source": "canonical_manifest_declared_eval_population",
                    "non_exact_population_source": "stage_c_family_a_scorer_evidence_artifact",
                    "read_file_population_source": None,
                    "symbol_name_population_source": None,
                    "anchor_population_source": None,
                    "no_anchor_population_source": None,
                },
                "evidence": {
                    "source_case_id": "case-c",
                    "row_index_1based": 1,
                },
            },
        ],
    }

    family_a = {
        "report_version": "stage_c_package1_family_a_scorer_evidence_v1",
        "artifact_scope": "authoritative_live_canonical_eval_family_a_scorer_evidence",
        "failure_taxonomy_marker": "family_a_failure_taxonomy_v1",
        "scorer_semantics_marker": "canonical_eval_manifest_stage_c_package1_v1",
        "sides": {
            "base": {
                "record_count": 3,
                "tool_expected_eligible_count": 3,
                "exact_valid_count": 1,
                "non_exact_tool_expected_count": 2,
                "subtype_assigned_count": 1,
                "missing_evidence_count": 1,
                "subtype_counts": {
                    "wrong tool name": 1,
                },
                "missing_evidence_reason_counts": {
                    "current canonical evaluator does not emit approved direct-answer or scalar substitution evidence": 1,
                },
                "records": [
                    {
                        "row_id": "heldout_validation:1",
                        "tool_expected_eligibility": True,
                        "excluded": False,
                        "primary_outcome": "invalid_json",
                        "exact_valid": False,
                        "non_exact_tool_expected": True,
                        "subtype_assignment": None,
                        "missing_evidence": True,
                        "missing_evidence_reasons": [
                            "current canonical evaluator does not emit approved direct-answer or scalar substitution evidence",
                        ],
                        "failure_taxonomy_marker": "family_a_failure_taxonomy_v1",
                        "scorer_semantics_marker": "canonical_eval_manifest_stage_c_package1_v1",
                    },
                    {
                        "row_id": "heldout_validation:2",
                        "tool_expected_eligibility": True,
                        "excluded": False,
                        "primary_outcome": "exact_valid",
                        "exact_valid": True,
                        "non_exact_tool_expected": False,
                        "subtype_assignment": None,
                        "missing_evidence": False,
                        "missing_evidence_reasons": [],
                        "failure_taxonomy_marker": "family_a_failure_taxonomy_v1",
                        "scorer_semantics_marker": "canonical_eval_manifest_stage_c_package1_v1",
                    },
                    {
                        "row_id": "tool_holdout:1",
                        "tool_expected_eligibility": True,
                        "excluded": False,
                        "primary_outcome": "wrong_tool_name",
                        "exact_valid": False,
                        "non_exact_tool_expected": True,
                        "subtype_assignment": "wrong tool name",
                        "missing_evidence": False,
                        "missing_evidence_reasons": [],
                        "failure_taxonomy_marker": "family_a_failure_taxonomy_v1",
                        "scorer_semantics_marker": "canonical_eval_manifest_stage_c_package1_v1",
                    },
                ],
            },
        },
    }

    guardrails = {
        "guardrail_status": {
            "inference_behavior_detected": False,
            "substitution_behavior_detected": False,
            "reconstruction_behavior_detected": False,
            "legacy_summary_modified": False,
            "legacy_detector_surface_modified": False,
        },
        "guardrail_counts": {
            "row_fact_record_count": 3,
            "family_a_record_count": 3,
            "family_a_missing_evidence_count": 1,
        },
    }

    runtime_summary = {
        "report_version": "stage_c_package1_live_canonical_evaluator_v1",
        "artifact_scope": "authoritative_row_fact_and_family_a_emission_only",
        "manifest_path": "/tmp/fake_manifest.json",
        "row_fact_count": 3,
        "family_a_side_record_counts": {
            "base": 3,
        },
        "legacy_surface_policy": {
            "summary_json": "preserved",
            "comparison_rows_jsonl": "preserved",
            "detector_metrics": "unchanged",
            "threshold_behavior": "unchanged",
            "comparability_policy": "unchanged",
        },
        "guardrail_status": dict(guardrails["guardrail_status"]),
    }

    _write_json(run_dir / package1c_mod.SUMMARY_ARTIFACT_NAME, summary)
    _write_json(run_dir / package1c_mod.STAGE_C_ROW_FACT_ARTIFACT_NAME, row_fact)
    _write_json(run_dir / package1c_mod.STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME, family_a)
    _write_json(run_dir / package1c_mod.STAGE_C_GOVERNANCE_GUARDRAILS_ARTIFACT_NAME, guardrails)
    _write_json(run_dir / package1c_mod.STAGE_C_RUNTIME_CONTRACT_SUMMARY_ARTIFACT_NAME, runtime_summary)

    comparison_rows_path = run_dir / "comparison_rows.jsonl"
    comparison_rows_text = '{"split":"heldout_validation","row_index_1based":1}\n'
    comparison_rows_path.write_text(comparison_rows_text, encoding="utf-8")

    summary_text = (run_dir / package1c_mod.SUMMARY_ARTIFACT_NAME).read_text(encoding="utf-8")
    return {
        "summary_text": summary_text,
        "comparison_rows_text": comparison_rows_text,
    }


def _run(tmp_path: Path):
    package1c_mod = _load_module(
        PACKAGE1C_SCRIPT_PATH,
        "stage_c_package1c_passive_reconciliation_surface_for_package1d_tests",
    )
    package1d_mod = _load_module(
        PACKAGE1D_SCRIPT_PATH,
        "stage_c_package1d_migration_readiness_assessment",
    )
    run_dir = tmp_path / "run"
    sentinels = _write_run_dir(run_dir, package1c_mod)
    reconciliation_summary = package1c_mod.run_stage_c_package1c_passive_reconciliation_surface(
        run_dir=run_dir
    )
    readiness_summary = package1d_mod.run_stage_c_package1d_migration_readiness_assessment(
        run_dir=run_dir
    )
    readiness_report = json.loads(
        Path(readiness_summary["report_path"]).read_text(encoding="utf-8")
    )
    return package1d_mod, run_dir, sentinels, reconciliation_summary, readiness_summary, readiness_report


def test_package1d_emits_readiness_report_and_expected_states(tmp_path):
    _, _, _, reconciliation_summary, readiness_summary, readiness_report = _run(tmp_path)

    assert Path(readiness_summary["report_path"]).exists()
    assert reconciliation_summary["surface_count"] == 4
    assert readiness_summary["surface_count"] == 4
    assert readiness_summary["readiness_counts"] == {
        "insufficient-evidence": 1,
        "migration-blocked": 1,
        "migration-ready": 1,
        "not-comparable": 1,
    }

    assessments = {
        row["surface_id"]: row
        for row in readiness_report["compatibility_surface_assessments"]
    }
    assert assessments["read_file_exact_valid_rate"]["readiness_state"] == "migration-ready"
    assert (
        assessments["read_file_symbol_name_exact_valid_rate"]["readiness_state"]
        == "insufficient-evidence"
    )
    assert assessments["direct_answer_substitution_count"]["readiness_state"] == "migration-blocked"
    assert assessments["no_anchor_exact_valid_share"]["readiness_state"] == "not-comparable"


def test_package1d_is_deterministic_and_leaves_legacy_files_unchanged(tmp_path):
    mod, run_dir, sentinels, _, summary_first, report_first = _run(tmp_path)

    summary_path = run_dir / "summary.json"
    comparison_rows_path = run_dir / "comparison_rows.jsonl"
    assert summary_path.read_text(encoding="utf-8") == sentinels["summary_text"]
    assert comparison_rows_path.read_text(encoding="utf-8") == sentinels["comparison_rows_text"]

    summary_second = mod.run_stage_c_package1d_migration_readiness_assessment(run_dir=run_dir)
    report_second = json.loads(Path(summary_second["report_path"]).read_text(encoding="utf-8"))

    assert summary_first == summary_second
    assert report_first == report_second
    assert summary_path.read_text(encoding="utf-8") == sentinels["summary_text"]
    assert comparison_rows_path.read_text(encoding="utf-8") == sentinels["comparison_rows_text"]


def test_package1d_preserves_missingness_and_blocked_state_visibility(tmp_path):
    _, _, _, _, _, readiness_report = _run(tmp_path)
    assessments = {
        row["surface_id"]: row
        for row in readiness_report["compatibility_surface_assessments"]
    }

    symbol_surface = assessments["read_file_symbol_name_exact_valid_rate"]
    assert symbol_surface["readiness_state"] == "insufficient-evidence"
    assert symbol_surface["authoritative_support"]["declared_symbol_membership_row_ids"] == []
    assert (
        symbol_surface["blocking_conditions"][0]["condition_code"]
        == "authoritative_declared_symbol_membership_unavailable"
    )

    direct_answer_surface = assessments["direct_answer_substitution_count"]
    assert direct_answer_surface["readiness_state"] == "migration-blocked"
    assert direct_answer_surface["authoritative_support"]["direct_answer_row_ids"] == []
    assert direct_answer_surface["authoritative_support"]["missing_evidence_row_ids"] == [
        "heldout_validation:1"
    ]

    no_anchor_surface = assessments["no_anchor_exact_valid_share"]
    assert no_anchor_surface["readiness_state"] == "not-comparable"
    assert no_anchor_surface["authoritative_support"]["declared_anchor_row_ids"] == []
    assert no_anchor_surface["authoritative_support"]["declared_no_anchor_row_ids"] == []


def test_package1d_reports_taxonomy_boundaries_and_integrity_checks(tmp_path):
    _, _, _, _, _, readiness_report = _run(tmp_path)

    assert set(readiness_report["readiness_taxonomy"]) == {
        "insufficient-evidence",
        "migration-blocked",
        "migration-ready",
        "not-comparable",
    }

    boundaries = readiness_report["assessment_boundaries"]
    assert boundaries["reads_stage_c_authoritative_artifacts"] is True
    assert boundaries["reads_package1c_reconciliation_artifact"] is True
    assert boundaries["reads_detector_outputs_directly"] is False
    assert boundaries["reads_threshold_outputs_directly"] is False
    assert boundaries["performs_reconstruction"] is False
    assert boundaries["performs_detector_projection"] is False
    assert boundaries["performs_threshold_projection"] is False
    assert boundaries["creates_replacement_metrics"] is False
    assert boundaries["authorizes_migration"] is False

    integrity = readiness_report["integrity_checks"]
    assert integrity["row_id_uniqueness_preserved"] is True
    assert integrity["family_a_rows_resolve_to_row_facts"] is True
    assert integrity["guardrails_clear"] is True
    assert integrity["legacy_surface_policy_preserved"] is True
    assert integrity["package1c_surface_count_matches"] is True
