# Phase V Control Surface Comparison

## Question

What critical properties did H1/H2 preserve that later interventions did not?

## Answer

H1 and H2 preserved a **frozen Stage B recovery scaffold** with a **small, patch-local intervention**, **high anchor concentration**, and a **semantically specific tool-request cue** on the positive rows. Later datasets either broadened the tool manifold, diluted the anchor mass, or replaced the exact request cue with a different prompt regime. Phase Q and Phase U then showed that changing only one of those axes was not enough.

Sources:

- [H1 summary](/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_summary.json)
- [H2 summary](/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_summary.json)
- [v1.1 summary](/opt/ai-stack/assistant-training/data/v1_1/dataset_v1_1_summary.json)
- [v1.2 summary](/opt/ai-stack/assistant-training/data/v1_2/dataset_v1_2_summary.json)
- [Phase L execution review](/opt/ai-stack/assistant-training/docs/phase_l/PHASE_L_EXECUTION_REVIEW.md)
- [Phase Q execution review](/opt/ai-stack/assistant-training/docs/phase_q/PHASE_Q_EXECUTION_REVIEW.md)
- [Phase U execution review](/opt/ai-stack/assistant-training/docs/phase_u/PHASE_U_EXECUTION_REVIEW.md)
- [Phase R schema realization analysis](/opt/ai-stack/assistant-training/docs/phase_r/SCHEMA_REALIZATION_ANALYSIS.md)

## Data-Side Comparison

| Dataset | Train rows | Tool-positive rows | Tool-positive density | Core anchor share | `rg_search + read_file` share | Tool entropy bits | Effective tool count | Prompt regime signal |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| H1 | `2160` | `1404` | `0.65` | `0.6546` | `0.4409` | `3.7065` | `13.0546` | `949` exact-tool-request, `455` strict-JSON |
| H2 | `2160` | `1404` | `0.65` | `0.7258` | `0.5121` | `3.3356` | `10.0954` | `938` exact-tool-request, `366` strict-JSON, `100` concise-request |
| v1.1 | `2160` | `1296` | `0.60` | `0.1937` | `0.0733` | `4.6987` | `25.9685` | `100%` strict-JSON on tool rows; `8` balanced prompt styles |
| v1.2 | `2160` | `1393` | `0.6449` | `0.5212` | `0.3116` | `4.2237` | `18.6834` | `100%` strict-JSON on tool rows; `8` balanced prompt styles |
| Phase T patch | `60` | `60` | `1.0` | `1.0` across 5 anchors | `1.0` for the 5 anchors | `0.0` for tool rows | `5` | `60` strict-JSON rows only |

Interpretation:

- H1/H2 kept the same train size as the recovery scaffold and only replaced `100` tool-positive rows.
- v1.1 flattened tool frequency across all `26` tool families.
- v1.2 restored anchor weighting but still used the broader prompt-style manifold.
- The Phase T patch was maximally narrow: `60` tool-positive rows, only the five core anchors, and a single canonical envelope shape.

## Prompt-Regime Comparison

The later full datasets have explicit prompt-style tags:

- v1.1 prompt-style entropy: about `3.0` bits over `8` balanced styles.
- v1.2 prompt-style entropy: about `3.0` bits over `8` balanced styles.

H1/H2 predate those style tags, so the closest available proxy is the system-prompt distribution on tool-positive rows:

- H1 tool-positive prompt entropy proxy: `0.9088` bits.
- H2 tool-positive prompt entropy proxy: `1.1659` bits.

That proxy is lower than the full-corpus entropy of the later datasets, but the more important distinction is semantic:

- H1/H2 keep a majority of tool-positive rows on the exact-tool-request cue.
- v1.1 and v1.2 remove that cue from tool-positive rows and replace it with a single strict-JSON system prompt plus broader prompt-style tagging.

## Run-Side Comparison

| Run | exact JSON | tool-name accuracy | argument accuracy | wrapper leakage | no-call correctness | adversarial no-call correctness | Dominant failure mode |
|---|---:|---:|---:|---:|---:|---:|---|
| H1 | `0.44` | `0.7143` | `0.6286` | `0.0` | `0.9` | `0.7` | `32` wrapper drift |
| H2 | `0.48` | `0.7714` | `0.6929` | `0.005` | `0.8` | `0.4` | `29` wrapper drift |
| Phase L / v1.1 | `0.0` | `0.0429` | `0.0071` | `0.0` | `1.0` | `1.0` | `70` wrapper drift, `55` direct-answer substitutions |
| Phase Q / v1.2 | `0.03` | `0.0714` | `0.0429` | `0.0` | `0.7667` | `0.3` | `94` wrapper drift |
| Phase U patch | `0.0` | `0.0` | `0.0` | `0.0` | `1.0` | `1.0` | `125` direct-answer substitutions |

## What Changed

### H1/H2

- Preserved the frozen recovery scaffold.
- Replaced only `100` tool-positive rows.
- Kept anchor concentration high.
- Preserved the exact tool-request cue on most positive rows.

### v1.1

- Rebuilt the entire corpus.
- Flattened the tool family distribution to near-uniform.
- Preserved safety, but lost exact JSON realization.

### v1.2

- Rebuilt the entire corpus again.
- Restored some anchor concentration.
- Still did not recover the exact `tool_calls` envelope.

### Phase Q

- Kept the v1.2 corpus.
- Showed broad wrapper drift even on core anchors.
- Confirmed that anchor weighting alone does not guarantee schema realization.

### Phase U

- Replaced the corpus with a tiny schema-repair patch.
- Preserved safety perfectly.
- Collapsed into direct answers instead of tool calls.

## Bottom Line

H1/H2 preserved a conjunction of properties that later interventions did not keep together:

1. a frozen control scaffold,
2. an exact-tool-request cue on the positive rows,
3. high anchor concentration,
4. and a small patch budget.

Later work split those properties apart. The result was safety without capability in v1.1/v1.2, and safety plus direct-answer collapse in Phase U.
