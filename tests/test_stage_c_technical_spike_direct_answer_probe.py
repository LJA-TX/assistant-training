import importlib.util
import json
import sys
from pathlib import Path


PACKAGE5B_TEST_HELPER_PATH = Path(
    "/opt/ai-stack/assistant-training/scripts/stage_c_package5b_direct_answer_blocker_persistence.py"
)
SPIKE_SCRIPT_PATH = Path(
    "/opt/ai-stack/assistant-training/scripts/stage_c_technical_spike_direct_answer_probe.py"
)


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, str(path))
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_spike_module():
    return _load_module(SPIKE_SCRIPT_PATH, "stage_c_technical_spike_direct_answer_probe")


def _write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_run_dir(
    run_dir: Path,
    *,
    manifest_path: Path,
    generated_utc: str,
    extraction_timestamp: str,
    direct_answer_count: int,
    subtype_rows: dict[str, str],
    missing_evidence_row_ids: list[str],
    missing_reason: str,
):
    package5b = _load_module(PACKAGE5B_TEST_HELPER_PATH, "stage_c_package5b_direct_answer_blocker_persistence")
    run_dir.mkdir(parents=True, exist_ok=True)

    failure_categories = {
        "direct_answer_substitution": direct_answer_count,
        "malformed_output": 1,
        "scalar_substitution": 0,
    }
    summary = {
        "generated_utc": generated_utc,
        "manifest_path": str(manifest_path),
        "model_name_or_path": "/tmp/fake-model",
        "adapter_dir": None,
        "decode_defaults": {
            "temperature": 0.0,
            "top_p": 1.0,
            "do_sample": False,
            "repetition_penalty": 1.0,
            "max_new_tokens": 64,
            "seed": 1234,
        },
        "detector_summary_side": "base",
        "failure_profile": {
            "failure_categories_non_exact_tool_rows": failure_categories,
        },
    }
    _write_json(run_dir / package5b.SUMMARY_ARTIFACT_NAME, summary)
    (run_dir / package5b.COMPARISON_ROWS_ARTIFACT_NAME).write_text(
        '{"split":"heldout_validation","row_index_1based":1}\n',
        encoding="utf-8",
    )

    all_row_ids = [
        "heldout_validation:10",
        "heldout_validation:28",
        "heldout_validation:77",
        "heldout_validation:99",
        "heldout_validation:120",
    ]
    row_fact = {
        "report_version": "stage_c_package1_row_facts_v1",
        "artifact_scope": "authoritative_live_canonical_eval_row_facts",
        "row_fact_count": len(all_row_ids),
        "records": [
            {
                "row_id": row_id,
                "split_id": row_id.split(":")[0],
                "membership_markers": {
                    "family_a_tool_expected_eligible": True,
                },
                "provenance": {
                    "extraction_timestamp_utc": extraction_timestamp,
                },
                "evidence": {"source_case_id": row_id},
            }
            for row_id in all_row_ids
        ],
    }
    _write_json(run_dir / package5b.STAGE_C_ROW_FACT_ARTIFACT_NAME, row_fact)

    family_a_records = []
    for row_id in all_row_ids:
        subtype = subtype_rows.get(row_id)
        missing = row_id in missing_evidence_row_ids
        family_a_records.append(
            {
                "row_id": row_id,
                "tool_expected_eligibility": True,
                "excluded": False,
                "primary_outcome": "invalid_schema" if subtype == "scalar substitution" else "invalid_json",
                "exact_valid": False,
                "non_exact_tool_expected": True,
                "subtype_assignment": subtype,
                "missing_evidence": missing,
                "missing_evidence_reasons": [missing_reason] if missing else [],
                "failure_taxonomy_marker": "tax",
                "scorer_semantics_marker": "sem",
            }
        )

    family_a = {
        "sides": {
            "base": {
                "records": family_a_records,
            },
        },
    }
    _write_json(run_dir / package5b.STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME, family_a)

    guardrails = {
        "guardrail_status": {
            "inference_behavior_detected": False,
            "substitution_behavior_detected": False,
            "reconstruction_behavior_detected": False,
            "legacy_summary_modified": False,
            "legacy_detector_surface_modified": False,
        },
    }
    _write_json(run_dir / package5b.STAGE_C_GOVERNANCE_GUARDRAILS_ARTIFACT_NAME, guardrails)

    runtime_contract = {
        "legacy_surface_policy": {
            "summary_json": "preserved",
            "comparison_rows_jsonl": "preserved",
            "detector_metrics": "unchanged",
            "threshold_behavior": "unchanged",
            "comparability_policy": "unchanged",
        },
    }
    _write_json(run_dir / package5b.STAGE_C_RUNTIME_CONTRACT_SUMMARY_ARTIFACT_NAME, runtime_contract)

    package1b = {
        "consumer_scope": "stage_c_package1b_family_a_passive_governance_consumer",
        "reported_values": {
            "row_fact_record_count": {"value": len(all_row_ids)},
            "family_a_tool_expected_population_count": {"value": len(all_row_ids)},
            "family_a_exact_valid_tool_expected_count": {"value": 0},
            "family_a_non_exact_tool_expected_count": {"value": len(all_row_ids)},
            "family_a_subtype_assigned_count": {"value": len(all_row_ids) - len(missing_evidence_row_ids)},
            "family_a_missing_evidence_count": {"value": len(missing_evidence_row_ids)},
            "family_a_missing_evidence_reason_counts": {
                "value": {missing_reason: len(missing_evidence_row_ids)}
            },
        },
        "integrity_checks": {
            "row_id_uniqueness_preserved": True,
            "tool_expected_row_ids_have_family_a_records": True,
            "family_a_row_ids_resolve_to_row_facts": True,
            "guardrails_clear": True,
        },
    }
    _write_json(run_dir / package5b.STAGE_C_PACKAGE1B_GOVERNANCE_REPORT_NAME, package1b)

    package1c = {
        "reconciled_surfaces": [
            {
                "surface_id": "direct_answer_substitution_count",
                "reconciliation_status": "requires_future_migration",
                "reason_code": "authoritative_family_a_subtype_surface_incomplete",
                "reason": "incomplete subtype surface",
                "authoritative_source": {"value": {"direct_answer_substitution_count": direct_answer_count}},
                "legacy_source": {"value": direct_answer_count},
                "ownership_authority": {"authoritative": "scorer", "legacy": "legacy evaluator"},
            }
        ],
    }
    _write_json(run_dir / package5b.STAGE_C_PACKAGE1C_RECONCILIATION_REPORT_NAME, package1c)

    package1d = {
        "readiness_counts": {"migration-blocked": 1},
        "integrity_checks": {
            "row_id_uniqueness_preserved": True,
            "family_a_rows_resolve_to_row_facts": True,
            "guardrails_clear": True,
            "legacy_surface_policy_preserved": True,
            "package1c_surface_count_matches": True,
        },
        "compatibility_surface_assessments": [
            {
                "surface_id": "direct_answer_substitution_count",
                "readiness_state": "migration-blocked",
                "reasoning": "missing subtype evidence",
                "blocking_conditions": [{"condition": "missing subtype evidence"}],
                "reconciliation_record": {"surface_id": "direct_answer_substitution_count"},
                "authoritative_support": {"status": "bounded"},
            }
        ],
    }
    _write_json(run_dir / package5b.STAGE_C_PACKAGE1D_READINESS_REPORT_NAME, package1d)


def test_spike_assessment_reports_scalar_delta_and_preserved_protected_rows(tmp_path):
    spike = _load_spike_module()

    manifest_path = tmp_path / "manifest.json"
    _write_json(
        manifest_path,
        {
            "manifest_version": "v1",
            "runtime": {
                "eval_schema_version": "canonical_eval_manifest_v1",
                "dataset_manifest_version": "dataset_v1_0_summary",
            },
            "datasets": {
                "heldout_validation": {"rows": 5},
            },
            "split_hashes": {"heldout_validation": "abc"},
            "evaluation_order": ["heldout_validation"],
        },
    )

    before_run = tmp_path / "before"
    after_run_a = tmp_path / "after_a"
    after_run_b = tmp_path / "after_b"
    missing_reason = "current canonical evaluator does not emit approved direct-answer or scalar substitution evidence"

    _write_run_dir(
        before_run,
        manifest_path=manifest_path,
        generated_utc="2026-06-05T00:00:00Z",
        extraction_timestamp="2026-06-05T00:00:00Z",
        direct_answer_count=0,
        subtype_rows={"heldout_validation:120": "malformed output"},
        missing_evidence_row_ids=[
            "heldout_validation:10",
            "heldout_validation:28",
            "heldout_validation:77",
            "heldout_validation:99",
        ],
        missing_reason=missing_reason,
    )
    _write_run_dir(
        after_run_a,
        manifest_path=manifest_path,
        generated_utc="2026-06-05T01:00:00Z",
        extraction_timestamp="2026-06-05T01:00:00Z",
        direct_answer_count=0,
        subtype_rows={"heldout_validation:120": "scalar substitution"},
        missing_evidence_row_ids=[
            "heldout_validation:10",
            "heldout_validation:28",
            "heldout_validation:77",
            "heldout_validation:99",
        ],
        missing_reason=missing_reason,
    )
    _write_run_dir(
        after_run_b,
        manifest_path=manifest_path,
        generated_utc="2026-06-05T02:00:00Z",
        extraction_timestamp="2026-06-05T02:00:00Z",
        direct_answer_count=0,
        subtype_rows={"heldout_validation:120": "scalar substitution"},
        missing_evidence_row_ids=[
            "heldout_validation:10",
            "heldout_validation:28",
            "heldout_validation:77",
            "heldout_validation:99",
        ],
        missing_reason=missing_reason,
    )

    assessment = spike.build_spike_assessment(
        before_run_dir=before_run,
        after_run_dir_a=after_run_a,
        after_run_dir_b=after_run_b,
        before_bundle_path=tmp_path / "before_bundle.json",
        after_bundle_a_path=tmp_path / "after_a_bundle.json",
        after_bundle_b_path=tmp_path / "after_b_bundle.json",
        assessment_output_path=tmp_path / "assessment.json",
    )

    assert assessment["runtime_evidence_assessment"]["new_authoritative_evidence_appeared"] is True
    assert assessment["runtime_evidence_assessment"]["scalar_substitution_delta"] == 1
    assert assessment["preservation_audit"]["after_run_a"]["structurally_incapable"]["all_rows_preserved"] is True
    assert assessment["preservation_audit"]["after_run_a"]["ambiguous"]["all_rows_preserved"] is True
    assert assessment["stability_validation"]["after_run_reproducible"] is True
    assert assessment["downstream_independence_review"]["after_run_a"]["legacy_direct_answer_count_unchanged"] is True
