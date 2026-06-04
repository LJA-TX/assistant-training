import importlib.util
import json
import sys
from pathlib import Path


SCRIPT_PATH = Path(
    "/opt/ai-stack/assistant-training/scripts/stage_c_package5b_direct_answer_blocker_persistence.py"
)


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "stage_c_package5b_direct_answer_blocker_persistence",
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


def _write_run_dir(
    run_dir: Path,
    *,
    manifest_path: Path,
    generated_utc: str,
    extraction_timestamp: str,
    direct_answer_count: int,
    missing_evidence_row_ids: list[str],
    missing_reason: str,
):
    mod = _load_module()
    run_dir.mkdir(parents=True, exist_ok=True)

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
            "failure_categories_non_exact_tool_rows": {
                "direct_answer_substitution": direct_answer_count,
                "malformed_output": 1,
            }
        },
    }
    _write_json(run_dir / mod.SUMMARY_ARTIFACT_NAME, summary)
    (run_dir / mod.COMPARISON_ROWS_ARTIFACT_NAME).write_text(
        '{"split":"heldout_validation","row_index_1based":1}\n',
        encoding="utf-8",
    )

    row_fact = {
        "report_version": "stage_c_package1_row_facts_v1",
        "artifact_scope": "authoritative_live_canonical_eval_row_facts",
        "row_fact_count": 3,
        "records": [
            {
                "row_id": "heldout_validation:1",
                "split_id": "heldout_validation",
                "membership_markers": {
                    "family_a_tool_expected_eligible": True,
                },
                "provenance": {
                    "extraction_timestamp_utc": extraction_timestamp,
                },
            },
            {
                "row_id": "heldout_validation:2",
                "split_id": "heldout_validation",
                "membership_markers": {
                    "family_a_tool_expected_eligible": True,
                },
                "provenance": {
                    "extraction_timestamp_utc": extraction_timestamp,
                },
            },
            {
                "row_id": "tool_holdout:1",
                "split_id": "tool_holdout",
                "membership_markers": {
                    "family_a_tool_expected_eligible": True,
                },
                "provenance": {
                    "extraction_timestamp_utc": extraction_timestamp,
                },
            },
        ],
    }
    _write_json(run_dir / mod.STAGE_C_ROW_FACT_ARTIFACT_NAME, row_fact)

    family_a_records = []
    for row_id in ["heldout_validation:1", "heldout_validation:2", "tool_holdout:1"]:
        if row_id in missing_evidence_row_ids:
            family_a_records.append(
                {
                    "row_id": row_id,
                    "tool_expected_eligibility": True,
                    "excluded": False,
                    "primary_outcome": "invalid_json",
                    "exact_valid": False,
                    "non_exact_tool_expected": True,
                    "subtype_assignment": None,
                    "missing_evidence": True,
                    "missing_evidence_reasons": [missing_reason],
                    "failure_taxonomy_marker": "tax",
                    "scorer_semantics_marker": "sem",
                }
            )
        else:
            family_a_records.append(
                {
                    "row_id": row_id,
                    "tool_expected_eligibility": True,
                    "excluded": False,
                    "primary_outcome": "invalid_json",
                    "exact_valid": False,
                    "non_exact_tool_expected": True,
                    "subtype_assignment": "direct-answer substitution" if row_id == "heldout_validation:1" and direct_answer_count else "malformed output",
                    "missing_evidence": False,
                    "missing_evidence_reasons": [],
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
    _write_json(run_dir / mod.STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME, family_a)

    guardrails = {
        "guardrail_status": {
            "inference_behavior_detected": False,
            "substitution_behavior_detected": False,
            "reconstruction_behavior_detected": False,
            "legacy_summary_modified": False,
            "legacy_detector_surface_modified": False,
        },
    }
    _write_json(run_dir / mod.STAGE_C_GOVERNANCE_GUARDRAILS_ARTIFACT_NAME, guardrails)

    runtime_contract = {
        "legacy_surface_policy": {
            "summary_json": "preserved",
            "comparison_rows_jsonl": "preserved",
            "detector_metrics": "unchanged",
            "threshold_behavior": "unchanged",
            "comparability_policy": "unchanged",
        },
    }
    _write_json(run_dir / mod.STAGE_C_RUNTIME_CONTRACT_SUMMARY_ARTIFACT_NAME, runtime_contract)

    package1b = {
        "consumer_scope": "stage_c_package1b_family_a_passive_governance_consumer",
        "reported_values": {
            "row_fact_record_count": {"value": 3},
            "family_a_tool_expected_population_count": {"value": 3},
            "family_a_exact_valid_tool_expected_count": {"value": 0},
            "family_a_non_exact_tool_expected_count": {"value": 3},
            "family_a_subtype_assigned_count": {"value": 3 - len(missing_evidence_row_ids)},
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
    _write_json(run_dir / mod.STAGE_C_PACKAGE1B_GOVERNANCE_REPORT_NAME, package1b)

    package1c = {
        "reconciled_surfaces": [
            {
                "surface_id": "direct_answer_substitution_count",
                "reconciliation_status": "requires_future_migration",
                "reason_code": "authoritative_family_a_subtype_surface_incomplete",
                "reason": "incomplete subtype surface",
                "authoritative_source": {
                    "artifact_paths": [str(run_dir / mod.STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME)],
                    "value": {
                        "direct_answer_substitution_count": direct_answer_count,
                        "direct_answer_row_ids": ["heldout_validation:1"] if direct_answer_count else [],
                        "non_exact_tool_expected_row_count": 3,
                        "missing_evidence_row_ids": missing_evidence_row_ids,
                    },
                },
                "legacy_source": {
                    "artifact_path": str(run_dir / mod.SUMMARY_ARTIFACT_NAME),
                    "value": direct_answer_count,
                },
                "ownership_authority": {
                    "authoritative": "scorer consumed by evaluator",
                    "legacy": "legacy evaluator failure_profile",
                },
            }
        ],
    }
    _write_json(run_dir / mod.STAGE_C_PACKAGE1C_RECONCILIATION_REPORT_NAME, package1c)

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
                "blocking_conditions": [
                    {
                        "condition_code": "authoritative_family_a_subtype_surface_incomplete",
                    }
                ],
                "reconciliation_record": {
                    "surface_id": "direct_answer_substitution_count",
                    "reconciliation_status": "requires_future_migration",
                },
                "authoritative_support": {
                    "non_exact_tool_expected_row_count": 3,
                    "direct_answer_row_ids": ["heldout_validation:1"] if direct_answer_count else [],
                    "missing_evidence_row_ids": missing_evidence_row_ids,
                },
            }
        ],
    }
    _write_json(run_dir / mod.STAGE_C_PACKAGE1D_READINESS_REPORT_NAME, package1d)

    threshold_profile = {
        "missing_baseline_policy": "fail_fast",
        "metric_catalog": {
            "direct_answer_substitution_count": {
                "path": "failure_profile.failure_categories_non_exact_tool_rows.direct_answer_substitution",
            }
        },
        "catastrophic_thresholds": [],
        "tradeoff_watch_thresholds": [
            {
                "rule_id": "direct_answer_substitution_delta_gt_3",
                "metric_id": "direct_answer_substitution_count",
                "basis": "delta_vs_baseline",
                "comparator": "gt",
                "threshold": 3.0,
            }
        ],
    }
    threshold_profile_path = run_dir / "threshold_profile.json"
    _write_json(threshold_profile_path, threshold_profile)
    return mod, threshold_profile_path


def test_package5b_build_bundle_captures_direct_answer_blocker_shape(tmp_path):
    mod = _load_module()
    manifest_path = tmp_path / "manifest.json"
    _write_json(
        manifest_path,
        {
            "manifest_version": "v1",
            "runtime": {
                "eval_schema_version": "canonical_eval_manifest_v1",
                "dataset_manifest_version": "dataset_v1_0_summary",
            },
            "evaluation_order": ["heldout_validation", "tool_holdout"],
            "split_hashes": {"heldout_validation": "hash-a", "tool_holdout": "hash-b"},
            "datasets": {
                "heldout_validation": {"rows": 2},
                "tool_holdout": {"rows": 1},
            },
        },
    )

    run_dir = tmp_path / "run"
    _, threshold_profile_path = _write_run_dir(
        run_dir,
        manifest_path=manifest_path,
        generated_utc="2026-06-04T12:00:00Z",
        extraction_timestamp="2026-06-04T12:00:00Z",
        direct_answer_count=1,
        missing_evidence_row_ids=["heldout_validation:2", "tool_holdout:1"],
        missing_reason="current canonical evaluator does not emit approved direct-answer or scalar substitution evidence",
    )

    output_path = tmp_path / "bundle.json"
    summary = mod.build_blocker_bundle(
        run_dir=run_dir,
        bundle_label="run_a",
        output_path=output_path,
        threshold_profile_path=threshold_profile_path,
    )
    bundle = json.loads(output_path.read_text(encoding="utf-8"))

    assert summary["reconciliation_status"] == "requires_future_migration"
    assert summary["readiness_state"] == "migration-blocked"
    assert summary["missing_evidence_count"] == 2
    assert bundle["blocker_inventory"]["tool_expected_population_count"] == 3
    assert bundle["blocker_inventory"]["non_exact_tool_expected_count"] == 3
    assert bundle["blocker_inventory"]["subtype_assigned_count"] == 1
    assert bundle["blocker_inventory"]["direct_answer_substitution_count"] == 1
    assert bundle["blocker_inventory"]["missing_evidence_count"] == 2
    assert bundle["blocker_inventory"]["missing_evidence_row_ids"] == [
        "heldout_validation:2",
        "tool_holdout:1",
    ]
    assert bundle["blocker_inventory"]["missing_evidence_reason_counts"] == {
        "current canonical evaluator does not emit approved direct-answer or scalar substitution evidence": 2
    }
    assert bundle["dependency_inventory"]["missing_baseline_policy"] == "fail_fast"
    assert bundle["dependency_inventory"]["threshold_consumers"]["watch_rules"][0]["rule_id"] == (
        "direct_answer_substitution_delta_gt_3"
    )


def test_package5b_compare_bundles_reports_strong_reproducibility(tmp_path):
    mod = _load_module()
    manifest_path = tmp_path / "manifest.json"
    _write_json(
        manifest_path,
        {
            "manifest_version": "v1",
            "runtime": {
                "eval_schema_version": "canonical_eval_manifest_v1",
                "dataset_manifest_version": "dataset_v1_0_summary",
            },
            "evaluation_order": ["heldout_validation", "tool_holdout"],
            "split_hashes": {"heldout_validation": "hash-a", "tool_holdout": "hash-b"},
            "datasets": {
                "heldout_validation": {"rows": 2},
                "tool_holdout": {"rows": 1},
            },
        },
    )

    left_run = tmp_path / "left_run"
    right_run = tmp_path / "right_run"
    _, left_threshold_profile = _write_run_dir(
        left_run,
        manifest_path=manifest_path,
        generated_utc="2026-06-04T12:00:00Z",
        extraction_timestamp="2026-06-04T12:00:00Z",
        direct_answer_count=0,
        missing_evidence_row_ids=["heldout_validation:1", "heldout_validation:2"],
        missing_reason="current canonical evaluator lacks approved Family A subtype evidence for this non-exact tool-expected row",
    )
    _, right_threshold_profile = _write_run_dir(
        right_run,
        manifest_path=manifest_path,
        generated_utc="2026-06-04T12:05:00Z",
        extraction_timestamp="2026-06-04T12:05:00Z",
        direct_answer_count=0,
        missing_evidence_row_ids=["heldout_validation:1", "heldout_validation:2"],
        missing_reason="current canonical evaluator lacks approved Family A subtype evidence for this non-exact tool-expected row",
    )

    left_bundle_path = tmp_path / "left_bundle.json"
    right_bundle_path = tmp_path / "right_bundle.json"
    mod.build_blocker_bundle(
        run_dir=left_run,
        bundle_label="left",
        output_path=left_bundle_path,
        threshold_profile_path=left_threshold_profile,
    )
    mod.build_blocker_bundle(
        run_dir=right_run,
        bundle_label="right",
        output_path=right_bundle_path,
        threshold_profile_path=right_threshold_profile,
    )

    comparison_path = tmp_path / "comparison.json"
    summary = mod.compare_blocker_bundles(
        left_bundle_path=left_bundle_path,
        right_bundle_path=right_bundle_path,
        output_path=comparison_path,
    )
    comparison = json.loads(comparison_path.read_text(encoding="utf-8"))

    assert summary["reproducibility_classification"] == "strongly reproducible"
    assert summary["focus_readiness_migration_blocked_both"] is True
    assert summary["focus_reconciliation_requires_future_migration_both"] is True
    assert comparison["stability_findings"]["blocker_inventory_stable"] is True
    assert comparison["stability_findings"]["missing_evidence_row_ids_stable"] is True
    assert comparison["stability_findings"]["missing_evidence_reasons_stable"] is True
    assert comparison["reproducibility_assessment"]["classification"] == "strongly reproducible"
