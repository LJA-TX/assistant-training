# H1/H2 Success Preservation Factors

## Ranked Factors

### 1. Frozen control scaffold and low-delta patching

**Confidence: high**

H1 and H2 were not full rebuilds. Each modified only `100` tool-positive rows on top of the frozen Stage B recovery surface, with the non-tool slices held fixed.

Evidence:

- [H1 summary](/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h1_diversity_patch_summary.json)
- [H2 summary](/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_phase_i_h2_commitment_patch_summary.json)
- [Stage B recovery i3 summary](/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_stage_b_recovery_i3_summary.json)

Why it matters:

- The same row-count shell stayed in place.
- Only the positive tool surface was perturbed.
- The later datasets changed the whole corpus and therefore changed multiple control surfaces at once.

### 2. Exact-tool-request cue on the positive rows

**Confidence: high**

H1 and H2 both kept the majority of tool-positive rows on the exact-tool-request system prompt.

Measured on the tool-positive rows:

- H1: `949/1404` rows, or `67.6%`, used the exact-tool-request cue.
- H2: `938/1404` rows, or `66.8%`, used the exact-tool-request cue.

By contrast:

- v1.1: `0%` of tool-positive rows used that cue.
- v1.2: `0%` of tool-positive rows used that cue.

This is the strongest prompt-surface difference between the successful patch runs and the later failed datasets.

### 3. High anchor concentration

**Confidence: high**

H1/H2 concentrated the tool-positive mass on the core anchors:

- `rg_search`
- `read_file`
- `find_files`
- `debug_tools`
- `run_command`

Quantitatively:

- H1 core-anchor share: `0.6546`
- H2 core-anchor share: `0.7258`
- H1 `rg_search + read_file` share: `0.4409`
- H2 `rg_search + read_file` share: `0.5121`

Later datasets were less concentrated:

- v1.1 core-anchor share: `0.1937`
- v1.1 `rg_search + read_file` share: `0.0733`
- v1.2 core-anchor share: `0.5212`
- v1.2 `rg_search + read_file` share: `0.3116`

### 4. Lower tool-family entropy

**Confidence: high**

H1/H2 had much lower tool entropy than the later full rebuilds.

Tool entropy bits:

- H1: `3.7065`
- H2: `3.3356`
- v1.1: `4.6987`
- v1.2: `4.2237`

Effective tool counts:

- H1: `13.05`
- H2: `10.10`
- v1.1: `25.97`
- v1.2: `18.68`

This is a strong signal that the later datasets spread learning mass too broadly.

### 5. Tool-positive density alone was not decisive

**Confidence: medium**

The density numbers do not explain the outcome by themselves:

- H1: `0.65`
- H2: `0.65`
- v1.1: `0.60`
- v1.2: `0.6449`

v1.2 is close to H1/H2 on density but still does not recover capability. Density is necessary context, not the driver.

### 6. Raw prompt entropy is not the decisive predictor

**Confidence: medium**

This is the caution point.

If you look only at the corpus-wide system-prompt entropy proxy, H1/H2 are not lower than the later datasets. In fact, the later datasets are lower-entropy by that coarse measure because they use one strict-JSON tool prompt on the tool-positive rows and one runtime assistant prompt on the rest.

So the winning property is not "lower entropy" in the abstract. The winning property is **cue specificity**:

- exact-tool-request on the tool-positive rows,
- plus a small number of narrow companion prompts,
- plus high anchor concentration.

## What Later Interventions Lost

### v1.1 lost

- exact-tool-request exposure,
- anchor concentration,
- and the narrow patch-local intervention shape.

### v1.2 lost

- exact-tool-request exposure,
- much of the H1/H2 anchor concentration,
- and the patch-local shape.

### Phase Q lost

- exact schema realization,
- despite restoring some anchor weighting.

### Phase U lost

- surrounding scaffold breadth and anchor diversity,
- despite using the canonical envelope on every row.

## Preservation Model

The smallest model consistent with the evidence is conjunctive:

1. preserve the frozen scaffold,
2. preserve the exact-tool-request cue,
3. preserve high anchor concentration,
4. do not broaden the prompt manifold too early.

If any one of those conditions is removed, capability degrades. If two are removed, collapse is likely.
