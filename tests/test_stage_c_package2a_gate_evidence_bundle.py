import importlib.util
import json
import sys
from pathlib import Path


SCRIPT_PATH = Path("/opt/ai-stack/assistant-training/scripts/stage_c_package2a_gate_evidence_bundle.py")


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "stage_c_package2a_gate_evidence_bundle",
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
    governance_report_input_prefix: str,
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
        "metrics": {
            "aggregate": {
                "invalid_json": 0.1,
                "no_call_correctness": 1.0,
            },
        },
        "failure_profile": {
            "read_file_exact_valid": {
                "count": 1,
                "rows": 2,
                "rate": 0.5,
            },
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
        "row_fact_count": 2,
        "records": [
            {
                "row_id": "heldout_validation:1",
                "split_id": "heldout_validation",
                "membership_markers": {
                    "family_b1_read_file_eligible": True,
                },
                "provenance": {
                    "extraction_timestamp_utc": extraction_timestamp,
                },
            },
            {
                "row_id": "heldout_validation:2",
                "split_id": "heldout_validation",
                "membership_markers": {
                    "family_b1_read_file_eligible": True,
                },
                "provenance": {
                    "extraction_timestamp_utc": extraction_timestamp,
                },
            },
        ],
    }
    _write_json(run_dir / mod.STAGE_C_ROW_FACT_ARTIFACT_NAME, row_fact)

    family_a = {
        "sides": {
            "base": {
                "records": [
                    {"row_id": "heldout_validation:1", "exact_valid": False},
                    {"row_id": "heldout_validation:2", "exact_valid": True},
                ],
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
            "row_fact_record_count": {"value": 2},
            "family_a_tool_expected_population_count": {"value": 2},
            "family_a_missing_evidence_count": {"value": 0},
            "ownership_conflict_row_count": {"value": 0},
        },
        "input_artifacts": {
            "run_dir": governance_report_input_prefix,
            "row_fact_metadata": {"path": f"{governance_report_input_prefix}/row_fact.json"},
            "family_a_scorer_evidence": {"path": f"{governance_report_input_prefix}/family_a.json"},
            "governance_guardrails": {"path": f"{governance_report_input_prefix}/guardrails.json"},
            "runtime_contract_summary": {"path": f"{governance_report_input_prefix}/runtime_summary.json"},
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
                "surface_id": "read_file_exact_valid_rate",
                "reconciliation_status": "aligned",
                "reason_code": "direct_stage_c_rate_matches_legacy_rate",
                "reason": "aligned",
                "authoritative_source": {
                    "artifact_paths": [f"{governance_report_input_prefix}/row_fact.json"],
                    "value": {
                        "rows": 2,
                        "count": 1,
                        "rate": 0.5,
                        "row_ids": ["heldout_validation:1", "heldout_validation:2"],
                        "missing_family_a_row_ids": [],
                    },
                },
                "legacy_source": {
                    "artifact_path": f"{governance_report_input_prefix}/summary.json",
                    "value": {"rows": 2, "count": 1, "rate": 0.5},
                },
                "ownership_authority": {
                    "authoritative": "dataset metadata + scorer consumed by evaluator",
                    "legacy": "legacy evaluator failure_profile",
                },
            }
        ],
    }
    _write_json(run_dir / mod.STAGE_C_PACKAGE1C_RECONCILIATION_REPORT_NAME, package1c)

    package1d = {
        "readiness_counts": {"migration-ready": 1},
        "integrity_checks": {
            "row_id_uniqueness_preserved": True,
            "family_a_rows_resolve_to_row_facts": True,
            "guardrails_clear": True,
            "legacy_surface_policy_preserved": True,
            "package1c_surface_count_matches": True,
        },
        "compatibility_surface_assessments": [
            {
                "surface_id": "read_file_exact_valid_rate",
                "readiness_state": "migration-ready",
                "reasoning": "aligned and clear",
                "blocking_conditions": [],
                "reconciliation_record": {
                    "surface_id": "read_file_exact_valid_rate",
                    "reconciliation_status": "aligned",
                },
                "authoritative_support": {
                    "read_file_row_ids": ["heldout_validation:1", "heldout_validation:2"],
                    "missing_family_a_row_ids": [],
                    "exact_valid_count": 1,
                },
            }
        ],
    }
    _write_json(run_dir / mod.STAGE_C_PACKAGE1D_READINESS_REPORT_NAME, package1d)

    threshold_profile = {
        "metric_catalog": {
            "read_file_exact_valid_rate": {
                "path": "failure_profile.read_file_exact_valid.rate",
            }
        },
        "catastrophic_thresholds": [
            {
                "rule_id": "read_file_exact_valid_rate_lt_0_40",
                "metric_id": "read_file_exact_valid_rate",
                "basis": "absolute",
                "comparator": "lt",
                "threshold": 0.4,
            }
        ],
        "tradeoff_watch_thresholds": [
            {
                "rule_id": "read_file_exact_valid_rate_lt_0_70",
                "metric_id": "read_file_exact_valid_rate",
                "basis": "absolute",
                "comparator": "lt",
                "threshold": 0.7,
            }
        ],
    }
    threshold_profile_path = run_dir / "threshold_profile.json"
    _write_json(threshold_profile_path, threshold_profile)
    return mod, threshold_profile_path


def test_package2a_build_bundle_captures_focus_surface_and_dependency_inventory(tmp_path):
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
            "evaluation_order": ["heldout_validation"],
            "split_hashes": {"heldout_validation": "hash-a"},
            "datasets": {
                "heldout_validation": {"rows": 2},
            },
        },
    )

    run_dir = tmp_path / "run_a"
    _, threshold_profile_path = _write_run_dir(
        run_dir,
        manifest_path=manifest_path,
        generated_utc="2026-06-04T00:00:00Z",
        extraction_timestamp="2026-06-04T00:00:00Z",
        governance_report_input_prefix="/tmp/run_a",
    )
    output_path = tmp_path / "bundle_run_a.json"

    summary = mod.build_gate_evidence_bundle(
        run_dir=run_dir,
        bundle_label="run_a",
        output_path=output_path,
        threshold_profile_path=threshold_profile_path,
    )
    bundle = json.loads(output_path.read_text(encoding="utf-8"))

    assert summary["reconciliation_status"] == "aligned"
    assert summary["readiness_state"] == "migration-ready"
    assert bundle["focus_surface"] == "read_file_exact_valid_rate"
    assert bundle["row_identity_snapshot"]["unique_row_id_count"] == 2
    assert bundle["guardrail_results"]["guardrails_clear"] is True
    assert bundle["focus_surface_reconciliation"]["reconciliation_status"] == "aligned"
    assert bundle["focus_surface_readiness"]["readiness_state"] == "migration-ready"
    assert bundle["dependency_inventory"]["legacy_metric_path"] == "failure_profile.read_file_exact_valid.rate"
    assert bundle["dependency_inventory"]["threshold_consumers"]["catastrophic_rules"][0]["rule_id"] == "read_file_exact_valid_rate_lt_0_40"
    assert bundle["dependency_inventory"]["threshold_consumers"]["watch_rules"][0]["rule_id"] == "read_file_exact_valid_rate_lt_0_70"


def test_package2a_compare_bundles_reports_semantic_stability_across_repeated_runs(tmp_path):
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
            "evaluation_order": ["heldout_validation"],
            "split_hashes": {"heldout_validation": "hash-a"},
            "datasets": {
                "heldout_validation": {"rows": 2},
            },
        },
    )

    run_a = tmp_path / "run_a"
    _, threshold_profile_path_a = _write_run_dir(
        run_a,
        manifest_path=manifest_path,
        generated_utc="2026-06-04T00:00:00Z",
        extraction_timestamp="2026-06-04T00:00:00Z",
        governance_report_input_prefix="/tmp/run_a",
    )
    run_b = tmp_path / "run_b"
    _, threshold_profile_path_b = _write_run_dir(
        run_b,
        manifest_path=manifest_path,
        generated_utc="2026-06-04T01:00:00Z",
        extraction_timestamp="2026-06-04T01:00:00Z",
        governance_report_input_prefix="/tmp/run_b",
    )

    bundle_a_path = tmp_path / "bundle_run_a.json"
    bundle_b_path = tmp_path / "bundle_run_b.json"
    mod.build_gate_evidence_bundle(
        run_dir=run_a,
        bundle_label="run_a",
        output_path=bundle_a_path,
        threshold_profile_path=threshold_profile_path_a,
    )
    mod.build_gate_evidence_bundle(
        run_dir=run_b,
        bundle_label="run_b",
        output_path=bundle_b_path,
        threshold_profile_path=threshold_profile_path_b,
    )

    comparison_path = tmp_path / "bundle_comparison.json"
    summary = mod.compare_gate_evidence_bundles(
        left_bundle_path=bundle_a_path,
        right_bundle_path=bundle_b_path,
        output_path=comparison_path,
    )
    comparison = json.loads(comparison_path.read_text(encoding="utf-8"))

    assert summary["focus_reconciliation_aligned_both"] is True
    assert summary["focus_readiness_migration_ready_both"] is True
    assert summary["comparison_rows_hash_stable"] is True

    findings = comparison["stability_findings"]
    assert findings["manifest_identity_stable"] is True
    assert findings["runtime_configuration_stable"] is True
    assert findings["summary_semantic_digest_stable"] is True
    assert findings["row_fact_semantic_digest_stable"] is True
    assert findings["comparison_rows_hash_stable"] is True
    assert findings["row_identity_stable"] is True
    assert findings["read_file_row_identity_stable"] is True
    assert findings["package1b_snapshot_stable"] is True
    assert findings["focus_reconciliation_stable"] is True
    assert findings["focus_reconciliation_aligned_both"] is True
    assert findings["focus_readiness_stable"] is True
    assert findings["focus_readiness_migration_ready_both"] is True
    assert findings["guardrails_clear_both"] is True
    assert findings["legacy_surface_stable"] is True
    assert findings["readiness_integrity_checks_stable"] is True

    raw_hashes = comparison["raw_hash_comparison"]
    assert raw_hashes["summary_json"]["equal"] is False
    assert raw_hashes["row_fact_metadata"]["equal"] is False
