# Assistant Training Project — Revised Documents & Artifact Index

## 1. Thread Summary / Goal Documents

### Core Summary & Charter (this conversation)
- `Thread Summary Document` (generated in chat)
- `Draft Codex /goal Charter` (generated in chat)
- `Revised Autonomous /goal Charter` (generated in chat)

---

# 2. Assistant-Training Repository

## Repository Root
- [/opt/ai-stack/assistant-training/README.md](/opt/ai-stack/assistant-training/README.md)
- [/opt/ai-stack/assistant-training/pyproject.toml](/opt/ai-stack/assistant-training/pyproject.toml)

## Documentation
- [/opt/ai-stack/assistant-training/docs/repo_layout.md](/opt/ai-stack/assistant-training/docs/repo_layout.md)
- [/opt/ai-stack/assistant-training/docs/migration_checklist.md](/opt/ai-stack/assistant-training/docs/migration_checklist.md)

## Data Documentation
- [/opt/ai-stack/assistant-training/data/README.md](/opt/ai-stack/assistant-training/data/README.md)

---

# 3. Training Scripts

## LoRA Trainer
- [/opt/ai-stack/assistant-training/scripts/train_lora_sft.py](/opt/ai-stack/assistant-training/scripts/train_lora_sft.py)

## Preflight Script
- [/opt/ai-stack/assistant-training/scripts/preflight_lora_run.py](/opt/ai-stack/assistant-training/scripts/preflight_lora_run.py)

## Evaluation Harness
- [/opt/ai-stack/assistant-training/scripts/eval_adapter_toolcalls.py](/opt/ai-stack/assistant-training/scripts/eval_adapter_toolcalls.py)

---

# 4. Tests

## Dataset Contract Tests
- [/opt/ai-stack/assistant-training/tests/test_dataset_contract.py](/opt/ai-stack/assistant-training/tests/test_dataset_contract.py)

## Masking Behavior Tests
- [/opt/ai-stack/assistant-training/tests/test_masking_behavior.py](/opt/ai-stack/assistant-training/tests/test_masking_behavior.py)

## Evaluation Harness Tests
- [/opt/ai-stack/assistant-training/tests/test_eval_adapter_toolcalls.py](/opt/ai-stack/assistant-training/tests/test_eval_adapter_toolcalls.py)

---

# 5. v0.1 Training Configs & Manifests

## Config
- [/opt/ai-stack/assistant-training/configs/lora/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1.config.json](/opt/ai-stack/assistant-training/configs/lora/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1.config.json)

## Run Manifest
- [/opt/ai-stack/assistant-training/manifests/runs/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1.run_manifest.json)

## Final Manifest Snapshot
- [/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1/run_manifest.final.json](/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1/run_manifest.final.json)

---

# 6. v0.1 Training Artifacts

## Training Summary
- [/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1/training_summary.json](/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1/training_summary.json)

## Resolved Config
- [/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1/resolved_config.json](/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1/resolved_config.json)

## Masking Audit
- [/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1/masking_audit.json](/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1/masking_audit.json)

## Adapter Output Directory
- `/opt/ai-stack/assistant-training/artifacts/adapters/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1`

---

# 7. v0.1 Evaluation Outputs

## Initial Validation Eval
- [/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1/evals/toolcall_minimum_20260505T102102Z/summary.json](/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1/evals/toolcall_minimum_20260505T102102Z/summary.json)
- [/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1/evals/toolcall_minimum_20260505T102102Z/comparison_rows.jsonl](/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1/evals/toolcall_minimum_20260505T102102Z/comparison_rows.jsonl)

## Train40 Diagnostic Eval
- [/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1/evals/toolcall_train40_base_vs_adapter_20260505T102851Z/summary.json](/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1/evals/toolcall_train40_base_vs_adapter_20260505T102851Z/summary.json)
- [/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1/evals/toolcall_train40_base_vs_adapter_20260505T102851Z/comparison_rows.jsonl](/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1/evals/toolcall_train40_base_vs_adapter_20260505T102851Z/comparison_rows.jsonl)

## Strong-Prompt Validation Eval
- [/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1/evals/toolcall_val40_strong_prompt_base_vs_adapter_20260505T103138Z/summary.json](/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1/evals/toolcall_val40_strong_prompt_base_vs_adapter_20260505T103138Z/summary.json)
- [/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1/evals/toolcall_val40_strong_prompt_base_vs_adapter_20260505T103138Z/comparison_rows.jsonl](/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_1/evals/toolcall_val40_strong_prompt_base_vs_adapter_20260505T103138Z/comparison_rows.jsonl)

---

# 8. v0.2 Dataset Artifacts

## v0.2 Train Split
- [/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_broad_allaliases_20260504_v2_positive_aug_inferred_v0_2_train_grouped.jsonl](/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_broad_allaliases_20260504_v2_positive_aug_inferred_v0_2_train_grouped.jsonl)

## v0.2 Val Split
- [/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_broad_allaliases_20260504_v2_positive_aug_inferred_v0_2_val_grouped.jsonl](/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_broad_allaliases_20260504_v2_positive_aug_inferred_v0_2_val_grouped.jsonl)

## Preservation Audit
- [/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_broad_allaliases_20260504_v2_positive_aug_inferred_v0_2.preservation_audit.json](/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_broad_allaliases_20260504_v2_positive_aug_inferred_v0_2.preservation_audit.json)

## Dataset Summary
- [/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_broad_allaliases_20260504_v2_positive_aug_inferred_v0_2.summary.json](/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_broad_allaliases_20260504_v2_positive_aug_inferred_v0_2.summary.json)

---

# 9. v0.2 Configs & Manifest

## Config
- [/opt/ai-stack/assistant-training/configs/lora/lora_probe_llama_3_2_3b_instruct_toolcall_v0_2.config.json](/opt/ai-stack/assistant-training/configs/lora/lora_probe_llama_3_2_3b_instruct_toolcall_v0_2.config.json)

## Run Manifest
- [/opt/ai-stack/assistant-training/manifests/runs/lora_probe_llama_3_2_3b_instruct_toolcall_v0_2.run_manifest.json](/opt/ai-stack/assistant-training/manifests/runs/lora_probe_llama_3_2_3b_instruct_toolcall_v0_2.run_manifest.json)

---

# 10. v0.2 Validation Artifacts

## Masking Audit
- [/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_2/preflight/masking_audit.json](/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_2/preflight/masking_audit.json)

## Resolved Config
- [/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_2/preflight/resolved_config.json](/opt/ai-stack/assistant-training/artifacts/lora_probe_llama_3_2_3b_instruct_toolcall_v0_2/preflight/resolved_config.json)

## Dataset Schema Reports
- [/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_broad_allaliases_20260504_v2_positive_aug_inferred_v0_2_train_grouped.schema_validation.json](/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_broad_allaliases_20260504_v2_positive_aug_inferred_v0_2_train_grouped.schema_validation.json)
- [/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_broad_allaliases_20260504_v2_positive_aug_inferred_v0_2_val_grouped.schema_validation.json](/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_broad_allaliases_20260504_v2_positive_aug_inferred_v0_2_val_grouped.schema_validation.json)

## Semantic Consistency Reports
- [/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_broad_allaliases_20260504_v2_positive_aug_inferred_v0_2_train_grouped.semantic_consistency.json](/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_broad_allaliases_20260504_v2_positive_aug_inferred_v0_2_train_grouped.semantic_consistency.json)
- [/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_broad_allaliases_20260504_v2_positive_aug_inferred_v0_2_val_grouped.semantic_consistency.json](/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data/tool_sft_broad_allaliases_20260504_v2_positive_aug_inferred_v0_2_val_grouped.semantic_consistency.json)

