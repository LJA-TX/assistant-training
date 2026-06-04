import importlib.util
import json
import sys
from pathlib import Path


SCRIPT_PATH = Path("/opt/ai-stack/assistant-training/scripts/stage_c_package1b_passive_governance_consumer.py")


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "stage_c_package1b_passive_governance_consumer",
        str(SCRIPT_PATH),
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _write_json(path: Path, payload):
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_run_dir(run_dir: Path, mod):
    run_dir.mkdir(parents=True, exist_ok=True)

    row_fact = {
        "report_version": "stage_c_package1_row_facts_v1",
        "artifact_scope": "authoritative_live_canonical_eval_row_facts",
        "row_fact_count": 3,
        "coverage_summary": {
            "family_a_tool_expected_eligible_count": 2,
            "family_b1_read_file_eligible_count": 2,
            "family_b1_symbol_name_declared_count": 1,
            "family_b1_symbol_name_missing_count": 1,
            "family_b2_anchor_eligible_declared_count": 1,
            "family_b2_anchor_eligible_missing_count": 2,
        },
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
                    "source_case_id": "dup_case",
                    "split": "heldout_validation",
                    "row_index_1based": 1,
                    "prompt_hint": "report one symbol name",
                    "guardrail_flags": {
                        "inference_used": False,
                        "substitution_used": False,
                        "reconstruction_used": False,
                    },
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
                    "family_b1_symbol_name_member": True,
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
                    "symbol_name_population_source": "declared_symbol_name_membership",
                    "anchor_population_source": None,
                    "no_anchor_population_source": None,
                },
                "evidence": {
                    "source_case_id": "dup_case",
                    "split": "heldout_validation",
                    "row_index_1based": 2,
                    "guardrail_flags": {
                        "inference_used": False,
                        "substitution_used": False,
                        "reconstruction_used": False,
                    },
                },
            },
            {
                "row_id": "tool_holdout:1",
                "split_id": "tool_holdout",
                "excluded": False,
                "expected_tool_name": None,
                "membership_markers": {
                    "family_a_tool_expected_eligible": False,
                    "family_b1_read_file_eligible": False,
                    "family_b1_symbol_name_member": None,
                    "family_b2_anchor_eligible": True,
                    "family_b2_no_anchor_member": True,
                    "family_b2_anchor_category": "no-anchor",
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
                    "anchor_population_source": "declared_family_b2_anchor_membership",
                    "no_anchor_population_source": "declared_family_b2_no_anchor_membership",
                },
                "evidence": {
                    "source_case_id": "anchor_case",
                    "split": "tool_holdout",
                    "row_index_1based": 1,
                    "prompt_hint": "first function name",
                    "guardrail_flags": {
                        "inference_used": False,
                        "substitution_used": False,
                        "reconstruction_used": False,
                    },
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
                "tool_expected_eligible_count": 2,
                "exact_valid_count": 0,
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
                        "primary_outcome": "wrong_tool_name",
                        "exact_valid": False,
                        "non_exact_tool_expected": True,
                        "subtype_assignment": "wrong tool name",
                        "missing_evidence": False,
                        "missing_evidence_reasons": [],
                        "failure_taxonomy_marker": "family_a_failure_taxonomy_v1",
                        "scorer_semantics_marker": "canonical_eval_manifest_stage_c_package1_v1",
                    },
                    {
                        "row_id": "tool_holdout:1",
                        "tool_expected_eligibility": False,
                        "excluded": False,
                        "primary_outcome": "refusal_expected",
                        "exact_valid": False,
                        "non_exact_tool_expected": False,
                        "subtype_assignment": None,
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

    _write_json(run_dir / mod.STAGE_C_ROW_FACT_ARTIFACT_NAME, row_fact)
    _write_json(run_dir / mod.STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME, family_a)
    _write_json(run_dir / mod.STAGE_C_GOVERNANCE_GUARDRAILS_ARTIFACT_NAME, guardrails)
    _write_json(run_dir / mod.STAGE_C_RUNTIME_CONTRACT_SUMMARY_ARTIFACT_NAME, runtime_summary)

    summary_path = run_dir / "summary.json"
    summary_text = json.dumps({"sentinel": "legacy-summary-unchanged"}, indent=2) + "\n"
    summary_path.write_text(summary_text, encoding="utf-8")

    comparison_rows_path = run_dir / "comparison_rows.jsonl"
    comparison_rows_text = '{"split":"heldout_validation","row_index_1based":1}\n'
    comparison_rows_path.write_text(comparison_rows_text, encoding="utf-8")

    return {
        "summary_text": summary_text,
        "comparison_rows_text": comparison_rows_text,
    }


def _run(tmp_path: Path):
    mod = _load_module()
    run_dir = tmp_path / "run"
    sentinels = _write_run_dir(run_dir, mod)
    summary = mod.run_stage_c_package1b_passive_governance_consumer(run_dir=run_dir)
    report = json.loads(Path(summary["report_path"]).read_text(encoding="utf-8"))
    return mod, run_dir, sentinels, summary, report


def test_package1b_emits_governance_report_and_lineage(tmp_path):
    mod, run_dir, _, summary, report = _run(tmp_path)

    assert Path(summary["report_path"]).exists()
    assert summary["consumer_scope"] == "stage_c_package1b_family_a_passive_governance_consumer"
    assert report["consumer_boundaries"]["reads_stage_c_artifacts_only"] is True
    assert report["consumer_boundaries"]["modifies_detector_inputs"] is False
    assert report["input_artifacts"]["row_fact_metadata"]["path"] == str(run_dir / mod.STAGE_C_ROW_FACT_ARTIFACT_NAME)

    reported = report["reported_values"]
    assert reported["family_a_tool_expected_population_count"]["value"] == 2
    assert reported["family_a_tool_expected_population_count"]["owning_authority"] == "dataset metadata"
    assert reported["family_a_missing_evidence_count"]["value"] == 1
    assert reported["family_a_missing_evidence_count"]["owning_authority"] == "scorer"
    assert reported["legacy_surface_policy"]["value"]["detector_metrics"] == "unchanged"


def test_package1b_is_deterministic_and_leaves_legacy_surfaces_unchanged(tmp_path):
    mod, run_dir, sentinels, summary_first, report_first = _run(tmp_path)

    summary_path = run_dir / "summary.json"
    comparison_rows_path = run_dir / "comparison_rows.jsonl"
    assert summary_path.read_text(encoding="utf-8") == sentinels["summary_text"]
    assert comparison_rows_path.read_text(encoding="utf-8") == sentinels["comparison_rows_text"]

    summary_second = mod.run_stage_c_package1b_passive_governance_consumer(run_dir=run_dir)
    report_second = json.loads(Path(summary_second["report_path"]).read_text(encoding="utf-8"))

    assert summary_first == summary_second
    assert report_first == report_second
    assert summary_path.read_text(encoding="utf-8") == sentinels["summary_text"]
    assert comparison_rows_path.read_text(encoding="utf-8") == sentinels["comparison_rows_text"]


def test_package1b_preserves_missingness_and_avoids_prompt_derived_reconstruction(tmp_path):
    _, _, _, _, report = _run(tmp_path)

    reported = report["reported_values"]
    assert reported["family_a_non_exact_tool_expected_count"]["value"] == 2
    assert reported["family_a_subtype_assigned_count"]["value"] == 1
    assert reported["family_a_missing_evidence_count"]["value"] == 1
    assert reported["family_a_missing_evidence_reason_counts"]["value"] == {
        "current canonical evaluator does not emit approved direct-answer or scalar substitution evidence": 1,
    }

    assert reported["declared_symbol_membership_row_count"]["value"] == 1
    assert reported["declared_symbol_membership_rows_missing_owner_count"]["value"] == 1
    assert reported["declared_anchor_row_count"]["value"] == 1
    assert reported["declared_anchor_rows_missing_assignment_owner_count"]["value"] == 1
    assert reported["declared_anchor_rows_missing_taxonomy_owner_count"]["value"] == 1

    assert report["supporting_row_sets"]["rows_with_missing_evidence"] == ["heldout_validation:1"]
    assert report["supporting_row_sets"]["rows_with_missing_symbol_membership_owner"] == ["heldout_validation:2"]
    assert report["supporting_row_sets"]["rows_with_missing_anchor_assignment_owner"] == ["tool_holdout:1"]
    assert report["supporting_row_sets"]["rows_with_missing_anchor_taxonomy_owner"] == ["tool_holdout:1"]

    # The first row contains prompt-like evidence text, but because governed membership is undeclared
    # the consumer must not synthesize symbol-name membership from that hint.
    assert "heldout_validation:1" not in report["supporting_row_sets"]["rows_with_missing_symbol_membership_owner"]


def test_package1b_integrity_checks_link_family_a_records_to_row_facts(tmp_path):
    _, _, _, summary, report = _run(tmp_path)

    assert summary["guardrails_clear"] is True
    assert report["integrity_checks"]["row_id_uniqueness_preserved"] is True
    assert report["integrity_checks"]["row_fact_count_matches_runtime_summary"] is True
    assert report["integrity_checks"]["family_a_side_record_count_matches_runtime_summary"] is True
    assert report["integrity_checks"]["tool_expected_row_ids_have_family_a_records"] is True
    assert report["integrity_checks"]["family_a_row_ids_resolve_to_row_facts"] is True
    assert report["integrity_checks"]["guardrails_clear"] is True
