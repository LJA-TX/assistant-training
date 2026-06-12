# H1/H2 Success Factors

## Bottom Line

H1 and H2 succeeded because they were **control-preserving, low-delta patch runs** on top of the frozen Stage B recovery surface, not full corpus rewrites. They kept the positive tool-call scaffold narrow and exact, with high anchor concentration and a much lower prompt-style entropy than the later full-dataset hybrids.

The later datasets, `v1.1` and `v1.2`, changed the whole train surface. They widened the prompt/style manifold and redistributed tool-positive mass more broadly. That helped v1.2 recover some anchor density, but it did not recreate the H1/H2 realization regime.

## Row-Level Comparison

| Dataset | Train rows | Tool-positive density | Core-anchor share of tool-positive rows | `rg_search + read_file` share | Prompt regime |
|---|---:|---:|---:|---:|---|
| H1 | `2160` | `0.65` | `0.6546` | `0.4409` | `exact_tool_requested` + `strict_json_tool_calls` |
| H2 | `2160` | `0.65` | `0.7258` | `0.5121` | `exact_tool_requested` + `strict_json_tool_calls` + small tail |
| v1.1 | `2160` | `0.60` | `0.1937` | `0.0733` | 8 balanced prompt styles |
| v1.2 | `2160` | `0.6449` | `0.5212` | `0.3116` | 8 balanced prompt styles |

Source evidence:

- [H1 summary](/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_summary.json)
- [H2 summary](/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_summary.json)
- [v1.1 summary](/opt/ai-stack/assistant-training/data/v1_1/dataset_v1_1_summary.json)
- [v1.2 summary](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_summary.json)

## Specific Properties That Matter

### 1. H1/H2 were patch runs, not rebuilds

H1 and H2 each changed only `100` tool-positive rows while leaving the rest of the Stage B recovery corpus frozen.

- H1 patch rows were concentrated on `list_dir`, `list_models`, `move_path`, `git_diff`, `list_active_ports`, and `write_file`.
- H2 patch rows were concentrated on `rg_search`, `debug_tools`, `run_command`, `apply_unified_diff`, `read_file`, `copy_path`, `get_system_datetime`, `archive_create`, and `check_service_health`.

That is a small perturbation on a stable scaffold, not a wholesale composition change.

### 2. H1/H2 kept the control surface intact

The control surface was explicitly framed as `semantic-disambiguation + compact JSON target shaping + contamination exclusions`.

The H1/H2 corpora inherited that scaffold and preserved the non-tool slices. The later datasets did not.

Source:

- [Stage B recovery i3 summary](/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_summary.json)

### 3. H1/H2 concentrated the exact envelope cue

On the H1/H2 positive rows, the system prompt regime was narrow:

- H1: `exact_tool_requested` `949`, `strict_json_tool_calls` `455`
- H2: `exact_tool_requested` `938`, `strict_json_tool_calls` `366`, `other` `100`

By contrast, v1.1 and v1.2 spread tool-positive rows across eight balanced prompt styles:

- `anchor_light`
- `canonical`
- `concise`
- `contrastive`
- `evidence`
- `paraphrastic`
- `structured`
- `uncertainty`

That is a major difference in schema-realization pressure.

### 4. H2 had the strongest anchor pressure

H2 put `72.6%` of its tool-positive rows into the five anchor tools:

- `rg_search`
- `read_file`
- `find_files`
- `debug_tools`
- `run_command`

H1 was also anchor-heavy at `65.5%`.

v1.1 collapsed that to `19.4%`.
v1.2 improved it to `52.1%`, but still did not match H1/H2.

## Why This Produced Better Metrics

H1/H2 achieved:

- exact JSON validity near `0.44` to `0.48`
- tool-name accuracy near `0.71` to `0.77`
- argument accuracy near `0.63` to `0.69`
- heldout exact-valid near `0.64` to `0.75`

That profile is consistent with a model that learned the **exact tool-call realization pattern** from a stable scaffold and repeated anchor exposure.

The later hybrids did not reproduce that regime:

- v1.1 flattened tool frequency almost uniformly across all 26 tools.
- v1.2 restored anchor weighting, but not enough to recover the H1/H2 envelope behavior.
- Phase Q shows the consequence: the model often emits the right inner function object, but not the required outer `tool_calls` wrapper.

## Conclusion

The H1/H2 win is best explained by:

1. a frozen control scaffold,
2. small targeted patch budgets,
3. high anchor concentration,
4. narrow exact-envelope prompting,
5. and low prompt-style entropy.

The later datasets changed too many of those variables at once.
