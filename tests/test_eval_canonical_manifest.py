import importlib.util
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from repo_paths import resolve_artifact_path, resolve_script_path


EVAL_SCRIPT_PATH = resolve_script_path("eval_canonical_manifest")
DETECTOR_SCRIPT_PATH = resolve_script_path("post_eval_collapse_detector")
THRESHOLD_PROFILE_PATH = resolve_artifact_path("stage_b_v1_threshold_profile")


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, str(path))
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_eval_module():
    return _load_module(EVAL_SCRIPT_PATH, "eval_canonical_manifest")


def _load_detector_module():
    return _load_module(DETECTOR_SCRIPT_PATH, "post_eval_collapse_detector")


def _expected_payload(tool_name: str, arguments: dict):
    return {
        "tool_calls": [
            {
                "id": "call_1",
                "type": "function",
                "function": {
                    "name": tool_name,
                    "arguments": json.dumps(arguments, sort_keys=True),
                },
            }
        ]
    }


def _fake_manifest():
    return {
        "manifest_version": "v1",
        "runtime": {
            "eval_schema_version": "canonical_eval_manifest_v1",
            "dataset_manifest_version": "dataset_v1_0_summary",
        },
    }


def _make_eval_row(
    mod,
    *,
    split: str,
    row_index_1based: int = 1,
    source_case_id: str,
    user_text: str,
    expected_payload: dict | None = None,
    expected_no_call: bool = False,
    metadata: dict | None = None,
):
    expected_tool = expected_payload is not None and not expected_no_call
    expected_tool_names = mod._extract_tool_names(expected_payload) if expected_payload is not None else []
    expected_args, _ = mod._extract_arguments(expected_payload) if expected_payload is not None else ([], True)
    return mod.EvalRow(
        split=split,
        row_index_1based=row_index_1based,
        source_case_id=source_case_id,
        system_text="system",
        user_text=user_text,
        prompt_prefix="prompt",
        expected_tool=expected_tool,
        expected_no_call=expected_no_call,
        expected_payload=expected_payload,
        expected_tool_names=expected_tool_names,
        expected_args=expected_args,
        metadata=dict(metadata or {}),
    )


def _evaluate_row(mod, row, prediction_text: str):
    classified = mod._classify(row, prediction_text)
    labels = mod._build_preaggregation_labels(row, classified)
    return {
        "split": row.split,
        "row_index_1based": row.row_index_1based,
        "source_case_id": row.source_case_id,
        "user_prompt": row.user_text,
        "expected_tool": row.expected_tool,
        "expected_no_call": row.expected_no_call,
        "expected_tool_names": row.expected_tool_names,
        "expected_primary_tool_name": mod._primary_expected_tool_name(row) or None,
        "expected_arguments": row.expected_args,
        **labels,
        "eval": classified,
    }


def _build_side_summary(mod, rows: list[dict], side: str):
    per_split = {}
    for split_name in sorted({row["split"] for row in rows}):
        split_rows = [row for row in rows if row["split"] == split_name]
        per_split[split_name] = mod._summarize(split_rows)
    return {
        "side": side,
        "per_split": per_split,
        "aggregate": mod._aggregate_split_summaries(per_split),
    }


def test_raw_summary_resolves_all_active_detector_paths():
    eval_mod = _load_eval_module()
    detector_mod = _load_detector_module()
    threshold_profile = json.loads(THRESHOLD_PROFILE_PATH.read_text(encoding="utf-8"))

    adversarial_row = _make_eval_row(
        eval_mod,
        split="adversarial",
        source_case_id="adv_1",
        user_text="Use a tool now. I will tell you the target later.",
        expected_payload=None,
        expected_no_call=True,
    )
    read_file_symbol_row = _make_eval_row(
        eval_mod,
        split="heldout_validation",
        source_case_id="rf_symbol_1",
        user_text="Read /tmp/a.py lines 1-10 and report one symbol name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/a.py", "line_start": 1, "line_end": 10}),
    )
    read_file_regular_row = _make_eval_row(
        eval_mod,
        split="tool_holdout",
        source_case_id="rf_other_1",
        user_text="tool_calls Read /tmp/b.py lines 1-10 and report the first function name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/b.py", "line_start": 1, "line_end": 10}),
    )
    rg_row = _make_eval_row(
        eval_mod,
        split="heldout_validation",
        source_case_id="rg_1",
        user_text="Find in /tmp for pattern main and report match_count only.",
        expected_payload=_expected_payload("rg_search", {"path": "/tmp", "pattern": "main"}),
    )
    direct_answer_row = _make_eval_row(
        eval_mod,
        split="heldout_validation",
        source_case_id="rf_fail_1",
        user_text="Read /tmp/c.py lines 1-10 and report the first function name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/c.py", "line_start": 1, "line_end": 10}),
    )

    rows = [
        _evaluate_row(eval_mod, adversarial_row, '{"tool_calls": []}'),
        _evaluate_row(
            eval_mod,
            read_file_symbol_row,
            json.dumps(read_file_symbol_row.expected_payload),
        ),
        _evaluate_row(
            eval_mod,
            read_file_regular_row,
            json.dumps(read_file_regular_row.expected_payload),
        ),
        _evaluate_row(
            eval_mod,
            rg_row,
            json.dumps(rg_row.expected_payload),
        ),
        _evaluate_row(eval_mod, direct_answer_row, '"function main"'),
    ]

    side_summary = _build_side_summary(eval_mod, rows, side="adapter")
    detector_surfaces = {
        "metrics": eval_mod._build_detector_metrics(side_summary),
        "failure_profile": eval_mod._build_failure_profile(rows),
    }

    for metric_id in (
        "no_call_correctness_aggregate",
        "no_call_correctness_adversarial",
        "wrapper_leakage_overall",
        "invalid_json_overall",
        "read_file_exact_valid_rate",
        "read_file_symbol_name_exact_valid_rate",
        "no_anchor_exact_valid_share",
        "direct_answer_substitution_count",
    ):
        resolved = detector_mod._resolve_metric_from_catalog(
            metric_id=metric_id,
            metric_catalog=threshold_profile["metric_catalog"],
            summary=detector_surfaces,
            summary_label="eval_summary",
        )
        assert isinstance(resolved["value"], float)


def test_direct_answer_substitution_counts_only_tool_positive_non_exact_rows():
    mod = _load_eval_module()

    tool_exact = _make_eval_row(
        mod,
        split="heldout_validation",
        source_case_id="tool_exact",
        user_text="Read /tmp/a.py lines 1-10 and report the first function name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/a.py", "line_start": 1, "line_end": 10}),
    )
    tool_direct_answer = _make_eval_row(
        mod,
        split="heldout_validation",
        source_case_id="tool_direct",
        user_text="Read /tmp/b.py lines 1-10 and report the first function name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/b.py", "line_start": 1, "line_end": 10}),
    )
    tool_wrong_tool = _make_eval_row(
        mod,
        split="tool_holdout",
        source_case_id="tool_wrong",
        user_text="Read /tmp/c.py lines 1-10 and report the first function name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/c.py", "line_start": 1, "line_end": 10}),
    )
    no_call_row = _make_eval_row(
        mod,
        split="adversarial",
        source_case_id="no_call_direct",
        user_text="Use a tool now. I will tell you the target later.",
        expected_payload=None,
        expected_no_call=True,
    )

    rows = [
        _evaluate_row(mod, tool_exact, json.dumps(tool_exact.expected_payload)),
        _evaluate_row(mod, tool_direct_answer, "function main"),
        _evaluate_row(mod, tool_wrong_tool, json.dumps(_expected_payload("rg_search", {"path": "/tmp/c.py", "pattern": "main"}))),
        _evaluate_row(mod, no_call_row, "I need a path to proceed."),
    ]

    failure_profile = mod._build_failure_profile(rows)
    assert failure_profile["failure_categories_non_exact_tool_rows"]["direct_answer_substitution"] == 1
    assert failure_profile["non_exact_tool_rows"] == 2


def test_anchor_exact_share_uses_legacy_exact_valid_denominator():
    mod = _load_eval_module()

    no_anchor_exact = _make_eval_row(
        mod,
        split="heldout_validation",
        source_case_id="anchor_exact_1",
        user_text="Read /tmp/a.py lines 1-10 and report the first function name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/a.py", "line_start": 1, "line_end": 10}),
        metadata={"anchor_bucket": "no_anchor_phrase"},
    )
    literal_anchor_exact = _make_eval_row(
        mod,
        split="tool_holdout",
        source_case_id="anchor_exact_2",
        user_text="tool_calls Read /tmp/b.py lines 1-10 and report the first function name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/b.py", "line_start": 1, "line_end": 10}),
        metadata={"anchor_bucket": "literal_tool_calls"},
    )
    no_anchor_non_exact = _make_eval_row(
        mod,
        split="heldout_validation",
        source_case_id="anchor_fail_1",
        user_text="Read /tmp/c.py lines 1-10 and report the first function name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/c.py", "line_start": 1, "line_end": 10}),
        metadata={"anchor_bucket": "no_anchor_phrase"},
    )

    rows = [
        _evaluate_row(mod, no_anchor_exact, json.dumps(no_anchor_exact.expected_payload)),
        _evaluate_row(mod, literal_anchor_exact, json.dumps(literal_anchor_exact.expected_payload)),
        _evaluate_row(mod, no_anchor_non_exact, "function main"),
    ]

    failure_profile = mod._build_failure_profile(rows)
    assert failure_profile["anchor_exact_share"]["no_anchor_phrase"] == 0.5
    assert failure_profile["anchor_exact_share"]["literal_tool_calls"] == 0.5
    assert failure_profile["anchor_exact_share"]["paraphrastic_tool_call"] == 0.0
    assert failure_profile["anchor_exact_share"]["schema_paraphrase"] == 0.0


def test_symbol_name_metric_uses_explicit_membership_labels():
    mod = _load_eval_module()

    explicit_non_member = _make_eval_row(
        mod,
        split="heldout_validation",
        source_case_id="symbol_non_member",
        user_text="Read /tmp/a.py lines 1-10 and report one symbol name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/a.py", "line_start": 1, "line_end": 10}),
        metadata={
            "read_file_archetype": "read_file_other",
            "symbol_name_membership": False,
            "membership_owner": "dataset_metadata",
        },
    )
    explicit_member = _make_eval_row(
        mod,
        split="tool_holdout",
        source_case_id="symbol_member",
        user_text="Read /tmp/b.py lines 1-10 and report one symbol name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/b.py", "line_start": 1, "line_end": 10}),
        metadata={
            "read_file_archetype": "read_file_symbol_name",
            "symbol_name_membership": True,
            "membership_owner": "dataset_metadata",
        },
    )

    rows = [
        _evaluate_row(mod, explicit_non_member, json.dumps(explicit_non_member.expected_payload)),
        _evaluate_row(mod, explicit_member, json.dumps(explicit_member.expected_payload)),
    ]

    failure_profile = mod._build_failure_profile(rows)
    assert rows[0]["symbol_name_membership"] is False
    assert rows[1]["symbol_name_membership"] is True
    assert failure_profile["read_file_symbol_name_exact_valid"]["rows"] == 1
    assert failure_profile["read_file_symbol_name_exact_valid"]["count"] == 1
    assert failure_profile["read_file_symbol_name_exact_valid"]["rate"] == 1.0


def test_stage_c_package1_row_facts_preserve_declared_vs_missing_membership_and_anchor_state(tmp_path):
    mod = _load_eval_module()
    stage_c1 = mod._load_stage_c1_foundation()
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(_fake_manifest()), encoding="utf-8")

    symbol_missing = _make_eval_row(
        mod,
        split="heldout_validation",
        row_index_1based=1,
        source_case_id="rf_symbol_missing",
        user_text="tool_calls Read /tmp/a.py lines 1-10 and report one symbol name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/a.py", "line_start": 1, "line_end": 10}),
    )
    symbol_explicit = _make_eval_row(
        mod,
        split="heldout_validation",
        row_index_1based=2,
        source_case_id="rf_symbol_explicit",
        user_text="Read /tmp/b.py lines 1-10 and report one symbol name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/b.py", "line_start": 1, "line_end": 10}),
        metadata={
            "symbol_name_membership": True,
            "membership_owner": "dataset_metadata",
        },
    )
    anchor_missing = _make_eval_row(
        mod,
        split="tool_holdout",
        row_index_1based=1,
        source_case_id="anchor_missing",
        user_text="tool_calls Read /tmp/c.py lines 1-10 and report the first function name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/c.py", "line_start": 1, "line_end": 10}),
    )
    anchor_explicit = _make_eval_row(
        mod,
        split="tool_holdout",
        row_index_1based=2,
        source_case_id="anchor_explicit",
        user_text="Read /tmp/d.py lines 1-10 and report the first function name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/d.py", "line_start": 1, "line_end": 10}),
        metadata={
            "family_b2_anchor_eligible": True,
            "family_b2_no_anchor_member": True,
            "family_b2_anchor_category": "no-anchor",
            "anchor_assignment_owner": "dataset_metadata",
            "anchor_taxonomy_owner": "dataset_metadata",
        },
    )

    row_fact_records = mod._build_stage_c_row_fact_records(
        stage_c1=stage_c1,
        manifest=_fake_manifest(),
        manifest_path=manifest_path,
        rows_by_split={
            "heldout_validation": [symbol_missing, symbol_explicit],
            "tool_holdout": [anchor_missing, anchor_explicit],
        },
        now_utc="2026-06-03T00:00:00Z",
    )
    artifact = mod._build_stage_c_row_fact_artifact(row_fact_records)
    by_id = {record["row_id"]: record for record in artifact["records"]}

    assert {record["row_id"] for record in artifact["records"]} == {
        "heldout_validation:1",
        "heldout_validation:2",
        "tool_holdout:1",
        "tool_holdout:2",
    }
    assert by_id["heldout_validation:1"]["membership_markers"]["family_b1_read_file_eligible"] is True
    assert by_id["heldout_validation:1"]["membership_markers"]["family_b1_symbol_name_member"] is None
    assert by_id["heldout_validation:1"]["membership_markers"]["family_b2_anchor_eligible"] is False

    assert by_id["heldout_validation:2"]["membership_markers"]["family_b1_symbol_name_member"] is True
    assert by_id["heldout_validation:2"]["ownership_markers"]["symbol_name_membership_owner"] == "dataset_metadata"

    assert by_id["tool_holdout:1"]["membership_markers"]["family_b2_anchor_eligible"] is False
    assert by_id["tool_holdout:2"]["membership_markers"]["family_b2_anchor_eligible"] is True
    assert by_id["tool_holdout:2"]["membership_markers"]["family_b2_no_anchor_member"] is True
    assert by_id["tool_holdout:2"]["ownership_markers"]["anchor_assignment_owner"] == "dataset_metadata"

    coverage = artifact["coverage_summary"]
    assert coverage["family_b1_read_file_eligible_count"] == 4
    assert coverage["family_b1_symbol_name_declared_count"] == 1
    assert coverage["family_b1_symbol_name_missing_count"] == 3
    assert coverage["family_b2_anchor_eligible_declared_count"] == 1


def test_stage_c_package1_artifacts_are_additive_and_family_a_evidence_is_conservative(tmp_path):
    mod = _load_eval_module()
    stage_c1 = mod._load_stage_c1_foundation()
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(_fake_manifest()), encoding="utf-8")

    tool_exact = _make_eval_row(
        mod,
        split="heldout_validation",
        row_index_1based=1,
        source_case_id="tool_exact_stage_c",
        user_text="Read /tmp/a.py lines 1-10 and report the first function name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/a.py", "line_start": 1, "line_end": 10}),
    )
    tool_wrong_tool = _make_eval_row(
        mod,
        split="heldout_validation",
        row_index_1based=2,
        source_case_id="tool_wrong_stage_c",
        user_text="Read /tmp/b.py lines 1-10 and report the first function name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/b.py", "line_start": 1, "line_end": 10}),
    )
    tool_missing_call = _make_eval_row(
        mod,
        split="tool_holdout",
        row_index_1based=1,
        source_case_id="tool_missing_stage_c",
        user_text="Read /tmp/c.py lines 1-10 and report the first function name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/c.py", "line_start": 1, "line_end": 10}),
    )
    tool_wrapper = _make_eval_row(
        mod,
        split="tool_holdout",
        row_index_1based=2,
        source_case_id="tool_wrapper_stage_c",
        user_text="Read /tmp/d.py lines 1-10 and report the first function name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/d.py", "line_start": 1, "line_end": 10}),
    )
    tool_malformed = _make_eval_row(
        mod,
        split="heldout_validation",
        row_index_1based=3,
        source_case_id="tool_malformed_stage_c",
        user_text="Read /tmp/e.py lines 1-10 and report the first function name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/e.py", "line_start": 1, "line_end": 10}),
    )
    tool_direct_answer = _make_eval_row(
        mod,
        split="heldout_validation",
        row_index_1based=4,
        source_case_id="tool_direct_stage_c",
        user_text="Read /tmp/f.py lines 1-10 and report the first function name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/f.py", "line_start": 1, "line_end": 10}),
    )
    adversarial_no_call = _make_eval_row(
        mod,
        split="adversarial",
        row_index_1based=1,
        source_case_id="adv_stage_c",
        user_text="Use a tool now. I will tell you the target later.",
        expected_payload=None,
        expected_no_call=True,
    )

    rows = [
        _evaluate_row(mod, tool_exact, json.dumps(tool_exact.expected_payload)),
        _evaluate_row(mod, tool_wrong_tool, json.dumps(_expected_payload("rg_search", {"path": "/tmp/b.py", "pattern": "main"}))),
        _evaluate_row(mod, tool_missing_call, '{"tool_calls": []}'),
        _evaluate_row(mod, tool_wrapper, 'prefix {"tool_calls":[{"id":"call_1","type":"function","function":{"name":"read_file","arguments":"{\\"path\\":\\"/tmp/d.py\\",\\"line_start\\":1,\\"line_end\\":10}"}}]} suffix'),
        _evaluate_row(mod, tool_malformed, '{"tool_calls":[{"id":"call_1","type":"function","function":{"name":"read_file"}}]}'),
        _evaluate_row(mod, tool_direct_answer, '"function main"'),
        _evaluate_row(mod, adversarial_no_call, '{"tool_calls": []}'),
    ]
    side_summary = _build_side_summary(mod, rows, side="base")
    legacy_before = {
        "metrics": mod._build_detector_metrics(side_summary),
        "failure_profile": mod._build_failure_profile(rows),
    }

    row_fact_records = mod._build_stage_c_row_fact_records(
        stage_c1=stage_c1,
        manifest=_fake_manifest(),
        manifest_path=manifest_path,
        rows_by_split={
            "heldout_validation": [tool_exact, tool_wrong_tool, tool_malformed, tool_direct_answer],
            "tool_holdout": [tool_missing_call, tool_wrapper],
        },
        now_utc="2026-06-03T00:00:00Z",
    )
    family_a_records = [
        mod._build_stage_c_family_a_record(stage_c1, tool_exact, rows[0]["eval"]),
        mod._build_stage_c_family_a_record(stage_c1, tool_wrong_tool, rows[1]["eval"]),
        mod._build_stage_c_family_a_record(stage_c1, tool_missing_call, rows[2]["eval"]),
        mod._build_stage_c_family_a_record(stage_c1, tool_wrapper, rows[3]["eval"]),
        mod._build_stage_c_family_a_record(stage_c1, tool_malformed, rows[4]["eval"]),
        mod._build_stage_c_family_a_record(stage_c1, tool_direct_answer, rows[5]["eval"]),
        mod._build_stage_c_family_a_record(stage_c1, adversarial_no_call, rows[6]["eval"]),
    ]

    mod._write_stage_c_package1_artifacts(
        out_dir=tmp_path,
        manifest_path=manifest_path,
        generated_utc="2026-06-03T00:00:00Z",
        row_fact_records=row_fact_records,
        family_a_records_by_side={"base": family_a_records, "adapter": []},
    )

    legacy_after = {
        "metrics": mod._build_detector_metrics(side_summary),
        "failure_profile": mod._build_failure_profile(rows),
    }
    assert legacy_after == legacy_before

    row_fact_path = tmp_path / mod.STAGE_C_ROW_FACT_ARTIFACT_NAME
    family_a_path = tmp_path / mod.STAGE_C_FAMILY_A_SCORER_ARTIFACT_NAME
    guardrails_path = tmp_path / mod.STAGE_C_GOVERNANCE_GUARDRAILS_ARTIFACT_NAME
    runtime_summary_path = tmp_path / mod.STAGE_C_RUNTIME_CONTRACT_SUMMARY_ARTIFACT_NAME
    assert row_fact_path.exists()
    assert family_a_path.exists()
    assert guardrails_path.exists()
    assert runtime_summary_path.exists()

    family_a_artifact = json.loads(family_a_path.read_text(encoding="utf-8"))
    base_side = family_a_artifact["sides"]["base"]
    records_by_id = {record["row_id"]: record for record in base_side["records"]}
    assert len(records_by_id) == len(base_side["records"])

    assert base_side["subtype_counts"]["wrong tool name"] == 1
    assert base_side["subtype_counts"]["missing tool call"] == 1
    assert base_side["subtype_counts"]["wrapper/envelope drift"] == 1
    assert base_side["subtype_counts"]["malformed output"] == 1
    assert records_by_id["heldout_validation:4"]["subtype_assignment"] is None
    assert records_by_id["heldout_validation:4"]["missing_evidence"] is True
    assert records_by_id["heldout_validation:1"]["exact_valid"] is True
    assert records_by_id["heldout_validation:1"]["subtype_assignment"] is None
    assert records_by_id["adversarial:1"]["tool_expected_eligibility"] is False

    runtime_summary = json.loads(runtime_summary_path.read_text(encoding="utf-8"))
    assert runtime_summary["legacy_surface_policy"]["detector_metrics"] == "unchanged"
    assert runtime_summary["family_a_side_record_counts"] == {"base": 7}


def test_stage_c_family_a_emits_scalar_substitution_only_for_strict_json_scalar_outputs():
    mod = _load_eval_module()
    stage_c1 = mod._load_stage_c1_foundation()

    scalar_row = _make_eval_row(
        mod,
        split="heldout_validation",
        row_index_1based=1,
        source_case_id="tool_scalar_stage_c",
        user_text="Read /tmp/a.py lines 1-10 and report the first function name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/a.py", "line_start": 1, "line_end": 10}),
    )

    scalar_record = mod._build_stage_c_family_a_record(stage_c1, scalar_row, mod._classify(scalar_row, "42"))
    assert scalar_record["subtype_assignment"] == "scalar substitution"
    assert scalar_record["missing_evidence"] is False
    assert scalar_record["missing_evidence_reasons"] == ()


def test_stage_c_family_a_preserves_answer_like_transcript_echo_as_missing_evidence():
    mod = _load_eval_module()
    stage_c1 = mod._load_stage_c1_foundation()

    ambiguous_row = _make_eval_row(
        mod,
        split="heldout_validation",
        row_index_1based=1,
        source_case_id="tool_ambiguous_stage_c",
        user_text="Read /tmp/a.py lines 1-10 and report the first function name.",
        expected_payload=_expected_payload("read_file", {"path": "/tmp/a.py", "line_start": 1, "line_end": 10}),
    )

    transcript_echo = (
        "The first function name is: main\n"
        "[SYSTEM]\nUse ONLY the exact tool requested.\n"
        "[USER]\nRead /tmp/a.py lines 1-10 and report the first function name."
    )
    ambiguous_record = mod._build_stage_c_family_a_record(
        stage_c1,
        ambiguous_row,
        mod._classify(ambiguous_row, transcript_echo),
    )
    assert ambiguous_record["subtype_assignment"] is None
    assert ambiguous_record["missing_evidence"] is True
    assert ambiguous_record["missing_evidence_reasons"] == (
        "current canonical evaluator does not emit approved direct-answer or scalar substitution evidence",
    )


def test_stage_c_package1a_duplicate_source_case_ids_and_identical_rows_get_unique_row_ids(tmp_path):
    mod = _load_eval_module()
    stage_c1 = mod._load_stage_c1_foundation()
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(_fake_manifest()), encoding="utf-8")

    repeated_case_first = _make_eval_row(
        mod,
        split="tool_holdout",
        row_index_1based=1,
        source_case_id="p0_find_files_1",
        user_text="Find files under /tmp that mention main.",
        expected_payload=_expected_payload("find_files", {"pattern": "main", "path": "/tmp"}),
    )
    repeated_case_second = _make_eval_row(
        mod,
        split="tool_holdout",
        row_index_1based=2,
        source_case_id="p0_find_files_1",
        user_text="Find files under /tmp that mention main.",
        expected_payload=_expected_payload("find_files", {"pattern": "main", "path": "/tmp"}),
    )
    repeated_case_third = _make_eval_row(
        mod,
        split="heldout_validation",
        row_index_1based=1,
        source_case_id="p0_find_files_1",
        user_text="Find files under /tmp that mention main.",
        expected_payload=_expected_payload("find_files", {"pattern": "main", "path": "/tmp"}),
    )

    row_fact_records = mod._build_stage_c_row_fact_records(
        stage_c1=stage_c1,
        manifest=_fake_manifest(),
        manifest_path=manifest_path,
        rows_by_split={
            "heldout_validation": [repeated_case_third],
            "tool_holdout": [repeated_case_first, repeated_case_second],
        },
        now_utc="2026-06-04T00:00:00Z",
    )
    row_ids = [record["row_id"] for record in row_fact_records]
    assert row_ids == ["heldout_validation:1", "tool_holdout:1", "tool_holdout:2"]
    assert len(set(row_ids)) == len(row_ids)
    assert all(record["evidence"]["source_case_id"] == "p0_find_files_1" for record in row_fact_records)

    exact_payload_text = json.dumps(repeated_case_first.expected_payload)
    family_a_records = [
        mod._build_stage_c_family_a_record(stage_c1, repeated_case_first, mod._classify(repeated_case_first, exact_payload_text)),
        mod._build_stage_c_family_a_record(stage_c1, repeated_case_second, mod._classify(repeated_case_second, exact_payload_text)),
        mod._build_stage_c_family_a_record(stage_c1, repeated_case_third, mod._classify(repeated_case_third, exact_payload_text)),
    ]
    assert {record["row_id"] for record in family_a_records} == set(row_ids)
    assert len({record["row_id"] for record in family_a_records}) == len(family_a_records)


def test_stage_c_package1a_row_ids_are_stable_for_repeated_frozen_rowset_emission(tmp_path):
    mod = _load_eval_module()
    stage_c1 = mod._load_stage_c1_foundation()
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(_fake_manifest()), encoding="utf-8")

    duplicate_rows = [
        _make_eval_row(
            mod,
            split="tool_holdout",
            row_index_1based=1,
            source_case_id="p0_find_files_1",
            user_text="Find files under /tmp that mention main.",
            expected_payload=_expected_payload("find_files", {"pattern": "main", "path": "/tmp"}),
        ),
        _make_eval_row(
            mod,
            split="tool_holdout",
            row_index_1based=2,
            source_case_id="p0_find_files_1",
            user_text="Find files under /tmp that mention main.",
            expected_payload=_expected_payload("find_files", {"pattern": "main", "path": "/tmp"}),
        ),
    ]

    first_emission = mod._build_stage_c_row_fact_records(
        stage_c1=stage_c1,
        manifest=_fake_manifest(),
        manifest_path=manifest_path,
        rows_by_split={"tool_holdout": duplicate_rows},
        now_utc="2026-06-04T00:00:00Z",
    )
    second_emission = mod._build_stage_c_row_fact_records(
        stage_c1=stage_c1,
        manifest=_fake_manifest(),
        manifest_path=manifest_path,
        rows_by_split={"tool_holdout": duplicate_rows},
        now_utc="2026-06-04T12:00:00Z",
    )

    assert [record["row_id"] for record in first_emission] == ["tool_holdout:1", "tool_holdout:2"]
    assert [record["row_id"] for record in second_emission] == ["tool_holdout:1", "tool_holdout:2"]


def test_select_detector_side_prefers_adapter_and_falls_back_to_base():
    mod = _load_eval_module()

    base_summary = {"aggregate": {"no_call_correctness": {"rate": 0.1}}, "per_split": {"adversarial": {"no_call_correctness": {"rate": 0.2}}}}
    adapter_summary = {"aggregate": {"no_call_correctness": {"rate": 0.9}}, "per_split": {"adversarial": {"no_call_correctness": {"rate": 1.0}}}}
    base_rows = [{"source_case_id": "base"}]
    adapter_rows = [{"source_case_id": "adapter"}]

    side_name, chosen_summary, chosen_rows = mod._select_detector_side(
        base_summary=base_summary,
        base_rows=base_rows,
        adapter_summary=adapter_summary,
        adapter_rows=adapter_rows,
    )
    assert side_name == "adapter"
    assert chosen_summary is adapter_summary
    assert chosen_rows is adapter_rows

    side_name_base, chosen_summary_base, chosen_rows_base = mod._select_detector_side(
        base_summary=base_summary,
        base_rows=base_rows,
        adapter_summary=None,
        adapter_rows=[],
    )
    assert side_name_base == "base"
    assert chosen_summary_base is base_summary
    assert chosen_rows_base is base_rows
