import importlib.util
import json
import sys
from pathlib import Path


EVAL_SCRIPT_PATH = Path("/opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py")
DETECTOR_SCRIPT_PATH = Path("/opt/ai-stack/assistant-training/scripts/post_eval_collapse_detector.py")
THRESHOLD_PROFILE_PATH = Path("/opt/ai-stack/assistant-training/manifests/reports/stage_b_v1_threshold_profile.json")


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


def _make_eval_row(
    mod,
    *,
    split: str,
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
        row_index_1based=1,
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
