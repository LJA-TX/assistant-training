# Current Dataset Assessment

## Executive Summary

Dataset v1.0 is behaviorally balanced at the category level, but the tool-positive training signal is far narrower than the summary numbers suggest. The split preserves the charter's 45/25/15/10/5 balance, but the train tool-positive slice collapses to a single repeated case and a single tool. That is the clearest local explanation for weak exact-JSON, tool-name, and argument accuracy.

## Observed Facts

- Canonical current inputs are runtime-produced JSONL files, not manually edited datasets.
- `data/README.md` and `data/README (data-intake).md` point to the runtime-produced grouped tool SFT files as the source of truth.
- `data/v1_0/dataset_v1_0_summary.json` records:
  - generated UTC: `2026-05-26T00:35:23Z`
  - seed: `20260525`
  - normalized tool rows: `144`
  - train rows: `2160`
  - val rows: `240`
  - stage A/B train rows: `2160` each
  - canonical eval splits: heldout validation `100`, tool holdout `40`, no-call `20`, adversarial `20`, direct answer `20`
- The train/val composition exactly matches the charter targets:
  - tool_positive `45%`
  - runtime_alignment `25%`
  - no_call_direct `15%`
  - refusal_policy `10%`
  - adversarial_malformed `5%`
- The overall synthetic ratio is `0.55` in both train and val.
- The leakage report shows limited but nonzero overlap:
  - train vs val: `source_case_id_overlap=1`, `target_overlap=20`
  - train vs heldout_validation: `source_case_id_overlap=1`, `target_overlap=1`
  - val vs heldout_validation: `source_case_id_overlap=8`, `prompt_overlap=2`, `target_overlap=13`
- The generated train tool-positive slice has:
  - `972` rows
  - `1` unique prompt
  - `1` unique target
  - `1` unique case id: `p0_rg_search_3`
  - `1` tool name: `rg_search`
- The generated val tool-positive slice has:
  - `108` rows
  - `31` unique prompts
  - `23` unique targets
  - `15` unique case ids

## Interpretation

### Strengths

- The dataset preserves the charter's overall behavior mix.
- The runtime-alignment, no-call, and refusal-policy slices are present in meaningful proportions.
- The canonical evaluation assets exist and are versioned.
- The synthetic ratio is below the hard ceiling in Appendix A.

### Weaknesses

- The train tool-positive slice is effectively one repeated exemplar, so it cannot teach broad tool selection or argument synthesis.
- Tool diversity is absent from the train tool-positive slice even though the upstream raw sources contain broader tool coverage.
- The train slice is vulnerable to overfitting because the tool-positive target is repeated 972 times.
- The 55% synthetic ratio is acceptable but not ideal relative to the preferred `<50%` guidance.
- The leakage report shows that the dataset is not perfectly isolated, so the evaluation story depends on the frozen manifest and the already-established Phase E contract reconciliation.

### Likely Causes of the Phase E i3 Profile

- Exact JSON validity stayed low because the model did not see enough varied canonical tool-call outputs.
- Tool-name and argument accuracy stayed low because the train tool-positive signal did not cover enough tool families, prompts, or argument spaces.
- No-call correctness stayed strong because the runtime-alignment, no-call, and refusal-policy slices are explicit and well represented.
- Wrapper leakage stayed low because the dataset already discourages prose-heavy answers.

## Recommendation

Preserve the current balanced runtime/no-call/refusal structure, but replace the repeated tool-positive saturation with a broader, versioned tool-call corpus. The next dataset change should diversify tool names, prompts, and argument patterns while keeping the current no-call discipline intact.

## Sources Used

- `data/README.md`
- `data/README (data-intake).md`
- `data/v1_0/dataset_v1_0_summary.json`
- `data/v1_0/dataset_v1_0_leakage_report.json`
- `scripts/build_dataset_v1.py`
