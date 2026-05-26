{
  "manifest_version": "v1",
  "created_utc": "2026-05-25T00:00:00Z",

  "charter_version": "goal_charter_v5a",
  "appendix_version": "appendix_a_operational_execution_contract_v3a",
  "metric_spec_version": "metric_specification_v1a",

  "runtime": {
    "assistant_runtime_repo": "/opt/ai-stack/runtimes/assistant-runtime",
    "assistant_runtime_commit": "PIN_REQUIRED",
    "tool_schema_version": "v1",
    "eval_schema_version": "v1"
  },

  "tokenizer": {
    "path": "/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base",
    "version": "llama-3.1-8b-base",
    "chat_template_mode": "tokenizer_native",
    "add_generation_prompt": true
  },

  "decode_defaults": {
    "temperature": 0.0,
    "top_p": 1.0,
    "do_sample": false,
    "repetition_penalty": 1.0,
    "max_new_tokens": 256,
    "seed": 1234
  },

  "datasets": {
    "heldout_validation": {
      "path": "PIN_REQUIRED",
      "sha256": "PIN_REQUIRED",
      "rows": 100,
      "promotion_eligible": true
    },

    "tool_holdout": {
      "path": "PIN_REQUIRED",
      "sha256": "PIN_REQUIRED",
      "rows": 40,
      "promotion_eligible": true
    },

    "no_call": {
      "path": "PIN_REQUIRED",
      "sha256": "PIN_REQUIRED",
      "rows": 20,
      "promotion_eligible": true
    },

    "adversarial": {
      "path": "PIN_REQUIRED",
      "sha256": "PIN_REQUIRED",
      "rows": 20,
      "promotion_eligible": true
    }
  },

  "scoring": {
    "scorer_script": "/opt/ai-stack/assistant-training/scripts/eval_adapter_toolcalls.py",
    "scorer_sha256": "PIN_REQUIRED",
    "metric_spec_version": "metric_specification_v1a.md"
  },

  "integrity": {
    "frozen_eval_contract": true,
    "allow_dynamic_dataset_discovery": false,
    "allow_implicit_latest_resolution": false,
    "cross_version_comparison_requires_annotation": true
  }
}
