# Phase I Dataset Variant Validation

## Validation Summary

Both treatment variants were built successfully from the frozen i3 control bytes.

## H1 Diversity Patch

- Dataset: `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_train.jsonl`
- Validation summary: `data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_summary.json`
- Patch size: `100` tool-positive rows
- Replacement distribution:
  - `list_dir`: `30`
  - `list_models`: `30`
  - `move_path`: `30`
  - `git_diff`: `4`
  - `list_active_ports`: `4`
  - `write_file`: `2`
- Row counts:
  - train: `2160`
  - val: `240`
- Frozen-slice checks:
  - non-tool slices unchanged: `true`
  - val bytes copied from control: `true`
  - row counts matched control: `true`
- Holdout contamination:
  - `heldout_validation`: `0` prompt / `0` target / `0` case-id overlap
  - `tool_holdout`: `0` prompt / `0` target / `0` case-id overlap

## H2 Commitment Patch

- Dataset: `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_train.jsonl`
- Validation summary: `data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_summary.json`
- Patch size: `100` tool-positive rows
- Replacement distribution:
  - `debug_tools`: `22`
  - `archive_create`: `11`
  - `run_command`: `11`
  - `copy_path`: `9`
  - `find_files`: `9`
  - `get_system_datetime`: `9`
  - `read_file`: `8`
  - `rg_search`: `8`
  - `apply_unified_diff`: `3`
  - `archive_extract`: `5`
  - `check_service_health`: `5`
- Row counts:
  - train: `2160`
  - val: `240`
- Frozen-slice checks:
  - non-tool slices unchanged: `true`
  - val bytes copied from control: `true`
  - row counts matched control: `true`
- Holdout contamination:
  - `heldout_validation`: `0` prompt / `0` target / `0` case-id overlap
  - `tool_holdout`: `0` prompt / `0` target / `0` case-id overlap

## Notes

- Both variants keep the control non-tool slices frozen.
- Both variants preserve the full train and val row counts.
- The only expected nonzero overlap in the summaries is against `no_call` and `adversarial`, and that overlap is inherited from the frozen control slice rather than introduced by the Phase I patch.
- No build-time kill rule tripped during dataset construction.

## Conclusion

The dataset-variant construction step is complete enough to support run-draft creation and later first-screen execution.
The draft configs and run manifests are now present in the tree alongside the dataset files and summaries.
