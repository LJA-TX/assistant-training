import importlib.util
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "eval_adapter_toolcalls.py"


def _load_module():
    spec = importlib.util.spec_from_file_location('eval_adapter_toolcalls', str(SCRIPT_PATH))
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _expected_payload():
    return {
        'tool_calls': [
            {
                'id': 'call_1',
                'type': 'function',
                'function': {
                    'name': 'read_file',
                    'arguments': '{"path":"/tmp/a.txt","line_start":1,"line_end":2}',
                },
            }
        ]
    }


def test_extract_json_payload_strict_and_embedded():
    mod = _load_module()

    obj, leakage, mode = mod._extract_json_payload('{"tool_calls": []}')
    assert isinstance(obj, dict)
    assert leakage is False
    assert mode == 'strict'

    obj2, leakage2, mode2 = mod._extract_json_payload('Here is output: {"tool_calls": []} done')
    assert isinstance(obj2, dict)
    assert leakage2 is True
    assert mode2 == 'embedded'


def test_evaluate_prediction_success_path():
    mod = _load_module()
    expected = _expected_payload()
    predicted = mod._canonical_json_text(expected)

    out = mod._evaluate_prediction(predicted, expected, expected_no_call=False)
    assert out['exact_tool_call_json_valid'] is True
    assert out['tool_name_accuracy'] is True
    assert out['argument_accuracy'] is True
    assert out['wrapper_or_prose_leakage'] is False
    assert out['primary_failure_category'] == 'ok'


def test_evaluate_prediction_detects_wrong_tool_and_args():
    mod = _load_module()
    expected = _expected_payload()
    predicted = '{"tool_calls":[{"id":"call_1","type":"function","function":{"name":"list_dir","arguments":"{\\"path\\":\\"/tmp\\"}"}}]}'

    out = mod._evaluate_prediction(predicted, expected, expected_no_call=False)
    assert out['tool_name_accuracy'] is False
    assert out['argument_accuracy'] is False
    assert 'wrong_tool_name' in out['issues']
    assert 'wrong_arguments' in out['issues']


def test_summary_no_call_available_flag_and_counts():
    mod = _load_module()

    rows = [
        {
            'base': {
                'exact_tool_call_json_valid': True,
                'tool_name_accuracy': True,
                'argument_accuracy': True,
                'wrapper_or_prose_leakage': False,
                'expected_no_call': False,
                'predicted_no_call': False,
                'primary_failure_category': 'ok',
            },
            'adapter': {
                'exact_tool_call_json_valid': True,
                'tool_name_accuracy': True,
                'argument_accuracy': True,
                'wrapper_or_prose_leakage': False,
                'expected_no_call': False,
                'predicted_no_call': False,
                'primary_failure_category': 'ok',
            },
        },
        {
            'base': {
                'exact_tool_call_json_valid': True,
                'tool_name_accuracy': False,
                'argument_accuracy': False,
                'wrapper_or_prose_leakage': False,
                'expected_no_call': True,
                'predicted_no_call': False,
                'primary_failure_category': 'unexpected_tool_call_when_no_call_expected',
            },
            'adapter': {
                'exact_tool_call_json_valid': True,
                'tool_name_accuracy': False,
                'argument_accuracy': False,
                'wrapper_or_prose_leakage': False,
                'expected_no_call': True,
                'predicted_no_call': True,
                'primary_failure_category': 'ok',
            },
        },
    ]

    base_summary = mod._summarize_side(rows, 'base')
    adapter_summary = mod._summarize_side(rows, 'adapter')

    assert base_summary['no_call_behavior']['available'] is True
    assert base_summary['no_call_behavior']['expected_no_call_rows'] == 1
    assert base_summary['no_call_behavior']['incorrect'] == 1

    assert adapter_summary['no_call_behavior']['available'] is True
    assert adapter_summary['no_call_behavior']['correct'] == 1
