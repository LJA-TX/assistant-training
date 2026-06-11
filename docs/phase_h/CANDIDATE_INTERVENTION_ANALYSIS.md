# Candidate Intervention Analysis

## Design Rule

The smallest useful intervention in Phase H is a bounded change against the i3 internal-recovery baseline, not a new full dataset program.

For this experiment:

- non-tool categories stay frozen,
- total train and val row counts stay frozen,
- the canonical eval manifest stays frozen,
- the trainer and LoRA topology stay frozen for content probes,
- and each content intervention is capped to a bounded tool-positive patch rather than an open-ended rebuild.

## Control Surface

### Control dataset

- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_train.jsonl`
- `data/v1_0/dataset_v1_0_stage_b_recovery_i3_val.jsonl`

### Control training surface

Use a fresh bounded control repro built from the proven `stage_b_llama31_8b_base_v1_i10r_microprobe` execution shape:

- same base model,
- same tokenizer and chat-template mode,
- same loss masking,
- same QLoRA topology,
- same optimization defaults,
- same `0.2`-epoch bounded microprobe budget,
- same canonical evaluation manifest.

This fresh control is the direct comparator for all new Phase I treatments.

## Frozen Variables

The following must remain frozen for the content probes:

| Surface | Freeze rule |
|---|---|
| Base model | `llama-3.1-8b-base` unchanged |
| Tokenizer / prompt contract | unchanged |
| Canonical eval manifest | unchanged |
| Decode defaults | unchanged |
| Scoring semantics | unchanged |
| LoRA topology | unchanged |
| Loss masking | unchanged |
| Non-tool slices | byte-for-byte unchanged from i3 control |
| Total row counts | unchanged from control |
| External data usage | prohibited |

## Bounded Patch Budget

Each content intervention may alter only the tool-positive slice and must stay within this envelope:

- replace or overlay `80` to `120` tool-positive train rows;
- keep tool-positive train row count fixed at the control count;
- keep non-tool categories fixed;
- preserve train/heldout and train/tool-holdout contamination exclusions;
- document the exact patch count and replacement logic.

This cap keeps the experiment small enough to attribute outcomes to a narrow intervention instead of a full dataset rewrite.

## Candidate Interventions

### T1: Diversity-only probe

#### What changes

- Restore omitted or underrepresented internal tool families inside the bounded patch budget.
- Increase tail-tool and tail-case exposure using only internal sources already present in the repository.
- Keep the control target schema and prompt style as close to i3 as practical.

#### What must remain frozen

- no new schema forms;
- no new commitment-specific contrastive prompt family;
- no trainer/config changes.

#### Target effect

Test whether more internal tool, case, and argument diversity alone lifts tool-holdout and heldout tool accuracy.

#### Expected evidence if A is dominant

- larger lift on tool-holdout exact-valid and tool-name / argument accuracy than the commitment probe;
- limited movement in direct-answer and scalar substitution shares relative to the commitment probe.

### T2: Commitment-only probe

#### What changes

- Keep tool menu and argument payload family approximately matched to the replaced control rows.
- Use bounded anchor-light / paraphrastic tool-expected variants over the same tool intents.
- Add tool-expected anti-direct-answer pressure without adding new tools or new output schemas.

#### What must remain frozen

- no increase in tool-family breadth as the primary intervention;
- no config changes;
- no no-call slice changes.

#### Target effect

Test whether the main deficit is failure to enter tool-call mode under less literal prompt forms.

#### Expected evidence if B is dominant

- strong drop in direct-answer and scalar substitution share;
- rise in no-anchor exact-valid share;
- exact-valid improvement without requiring a large tool-holdout gain.

### T3: Schema-only probe

#### What changes

- Keep tool menu and intent family matched to control.
- Add bounded schema-realization pressure using exact canonical `tool_calls` envelope rows derived from Phase E `missing_tool_calls` and `payload_not_object` failure archetypes.
- Keep prompt intent close to control while focusing the patch on envelope correctness rather than menu breadth.

#### What must remain frozen

- no new tool families as the primary intervention;
- no trainer/config changes;
- no no-call slice changes.

#### Target effect

Test whether the main remaining bottleneck is canonical envelope realization after the model has already moved toward tool-call mode.

#### Expected evidence if C is dominant

- large reduction in invalid-schema share;
- clear reduction in `missing_tool_calls` and `payload_not_object`;
- smaller change in direct-answer and scalar substitution than the commitment probe.

### T4: Methodology-only probe

#### Preferred form

Use the exact control dataset bytes and alter only training methodology.

Preferred methodology change:

- enable bounded deterministic geometry or exposure weighting if it can be implemented using existing trainer support without redesign.

Fallback methodology change:

- keep dataset bytes fixed and change only the training schedule, starting with a simple `0.2 -> 0.35` epoch extension while all other optimizer surfaces remain fixed.

#### What must remain frozen

- dataset bytes;
- eval surface;
- prompt contract;
- non-tool slices;
- external data usage.

#### Target effect

Test whether a config-only or exposure-only change on frozen content can match or exceed the content probes.

#### Expected evidence if D is dominant

- methodology-only run matches or beats the best content probe on primary metrics;
- improvements occur without changing dataset content.

## Isolation Limits

Commitment and schema are not perfectly orthogonal:

- the model must first enter tool-call mode before exact schema can be scored,
- and schema pressure often reinforces commitment indirectly.

Phase H handles that by using:

1. a first screen that pits diversity against commitment,
2. a conditional schema split if commitment-related evidence wins,
3. and a separate methodology-only run only if content changes do not explain the outcome cleanly.

## Recommended Intervention Priority

Priority order for execution:

1. fresh control repro
2. commitment-only probe
3. diversity-only probe
4. schema-only probe if commitment wins or invalid-schema remains dominant
5. methodology-only probe if content probes remain inconclusive or if methodology plausibility stays high

This order follows the current evidence: commitment looks likeliest, diversity still needs a direct test, schema is second-order but still plausible, and methodology should be tested only if content probes do not settle the question.

## Sources Used

- `docs/Phase_H_Work_packages.md`
- `docs/phase_g/FAILURE_ATTRIBUTION_ANALYSIS.md`
- `docs/phase_g/RECOVERY_CORPUS_ANALYSIS.md`
- `docs/phase_g/INTERNAL_SIGNAL_INVENTORY.md`
- `configs/lora/stage_b_llama31_8b_base_v1_i10r_microprobe.config.json`
- `configs/lora/stage_b_llama31_8b_base_v1_geometry_probe_lh.config.json`
- `manifests/reports/stage_b_v1_geometry_mapping_design.md`
