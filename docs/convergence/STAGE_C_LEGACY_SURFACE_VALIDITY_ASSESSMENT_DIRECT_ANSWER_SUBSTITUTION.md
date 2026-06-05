# Stage C Legacy Surface Validity Assessment Direct-Answer Substitution

## Scope

This slice assesses the semantic validity of the legacy:

- `direct_answer_substitution_count`

surface.

It is observational only.

It does not:

1. modify scorer behavior
2. modify evaluator behavior
3. modify detector behavior
4. modify threshold behavior
5. modify migration flags
6. modify governance doctrine
7. reopen readiness
8. reopen gate
9. perform implementation

## Inputs

Primary runtime artifacts reviewed:

1. `/tmp/stage_c_technical_spike_before/comparison_rows.jsonl`
2. `/tmp/stage_c_technical_spike_before/stage_c_family_a_scorer_evidence_artifact.json`
3. `/tmp/stage_c_technical_spike_before/stage_c_row_fact_metadata_artifact.json`
4. [stage_c_technical_spike_direct_answer_assessment.json](/opt/ai-stack/assistant-training/manifests/reports/stage_c_technical_spike_direct_answer_assessment.json:1)
5. [stage_c_runtime_output_forensics_direct_answer_missing_evidence_assessment.json](/opt/ai-stack/assistant-training/manifests/reports/stage_c_runtime_output_forensics_direct_answer_missing_evidence_assessment.json:1)
6. [stage_c_legacy_surface_validity_direct_answer_assessment.json](/opt/ai-stack/assistant-training/manifests/reports/stage_c_legacy_surface_validity_direct_answer_assessment.json:1)

Relevant evaluator logic:

1. [eval_canonical_manifest.py](/opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py:535)
2. [eval_canonical_manifest.py](/opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py:650)

## Summary Determination

The legacy `direct_answer_substitution_count` surface is materially misaligned with its claimed semantic meaning.

Based on direct runtime artifacts, it is not primarily measuring genuine direct-answer substitution behavior.

It is primarily measuring invalid tool-expected outputs dominated by:

1. prompt/task echo with transcript contamination
2. smaller instruction-assertion and answer-prefix contamination cases
3. other invalid echo artifacts

The core repository conclusion is:

1. the surface is operationally reproducible
2. the surface is semantically weak
3. the surface behaves more like a broad invalid echo/contamination counter than a genuine direct-answer substitution measure

## Legacy Surface Population Inventory

Legacy population:

1. total rows: `125`
2. `heldout_validation`: `85`
3. `tool_holdout`: `40`

All `125/125` legacy-counted rows overlap the authoritative missing-evidence population.

There is zero overlap with authoritative direct-answer, scalar-substitution, or malformed-output positive rows.

Observed authoritative state overlap:

1. authoritative `missing_evidence`: `125`
2. authoritative positive subtype rows: `0`

Population shape:

1. `125/125` rows are `primary_class=invalid_json`
2. `125/125` rows are `parse_mode=invalid`
3. `125/125` rows are `schema_reason=payload_not_parsed`

The population is not homogeneous.

It contains distinct subgroups, but one subgroup dominates:

1. task/prompt echo with transcript contamination: `116/125` (`92.8%`)

## Runtime Artifact Review

Representative observed outputs:

1. task/prompt echo with transcript contamination
   - `heldout_validation:1`
   - `Show /opt/ai-stack/runtimes/assistant-runtime/server/agent.py starting at line 1080 for 25 lines and report one symbol name.\n[SYSTEM]...`
2. answer-prefix plus transcript contamination
   - `heldout_validation:10`
   - `The first function name is: main\n[SYSTEM]...`
3. instructional assertion plus transcript contamination
   - `heldout_validation:44`
   - `Tool validation is not required for this task.\n[SYSTEM]...`
4. tool-label repetition
   - `heldout_validation:11`
   - `Tool: python\nTool: python\nTool: python...`
5. task/prompt echo without transcript contamination
   - `heldout_validation:50`
   - `Use json_edit on /opt/ai-stack/runtimes/assistant-runtime/.state/.tool_ft_tmp.json ...`

Observed runtime predicates:

1. legacy rows with authoritative tool-intent signal: `0`
2. legacy rows with bounded scalar-candidate signal: `0`
3. legacy rows with answer-like mixed prefix: `3`
4. observed genuine direct-answer-only rows: `0`

This means the legacy direct-answer population is not hiding a large pool of clean governed evidence.

## Behavioral Taxonomy

Repository-derived behavior taxonomy for the legacy-counted population:

| Category | Rows | Percentage |
|---|---:|---:|
| task/prompt echo with transcript contamination | 116 | 92.8% |
| instructional assertion plus transcript contamination | 4 | 3.2% |
| answer-prefix plus transcript contamination | 3 | 2.4% |
| tool-label repetition | 1 | 0.8% |
| task/prompt echo without transcript contamination | 1 | 0.8% |

Not observed:

1. genuine direct-answer substitution
2. clean scalar substitution

The observed categories are runtime-derived.

They are not imposed from doctrine.

## Population Distribution Assessment

Dominant category:

1. task/prompt echo with transcript contamination: `116/125`

Rare categories:

1. instructional assertion plus transcript contamination: `4/125`
2. answer-prefix plus transcript contamination: `3/125`
3. tool-label repetition: `1/125`
4. task/prompt echo without transcript contamination: `1/125`

Interpretive consequence:

1. the legacy count is not distributed across multiple equally plausible direct-answer modes
2. it is overwhelmingly concentrated in one contamination-heavy echo mode

## Semantic Validity Assessment

Classification:

1. `materially misaligned`

Why:

1. `0` genuine direct-answer rows were observed
2. `125/125` legacy rows are authoritative missing-evidence rows
3. `116/125` rows are prompt/task echo with transcript contamination
4. `0/125` rows satisfy the authoritative tool-intent predicate
5. `0/125` rows satisfy the bounded scalar-substitution predicate

Relationship between intended meaning and observed meaning:

1. intended meaning: genuine direct-answer substitution in tool-expected non-exact rows
2. observed meaning: invalid tool-expected outputs dominated by prompt/task echo and transcript contamination, with a small mixed answer-like subset

That gap is too large to classify as merely partial validity.

## Legacy Versus Authoritative Disagreement Analysis

The disagreement is best explained by multiple factors led by:

1. legacy over-counting
2. differing semantic definitions
3. observability differences
4. ownership differences

The strongest concrete mechanism is the legacy fallback logic in [_failure_subtype(...) ](/opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py:650):

1. invalid outputs that are not scalar tokens
2. and do not start with `{` or `[`
3. and do not look like tool-intent text

are labeled legacy `direct_answer_substitution`.

That boundary is largely lexical, not semantic.

By contrast, the authoritative path in [_stage_c_family_a_declared_subtype(...) ](/opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py:535):

1. emits `malformed output` only for invalid rows with explicit tool-intent evidence
2. emits `scalar substitution` only for the narrow strict-scalar predicate
3. otherwise preserves missing evidence

So the disagreement is not primarily:

1. authoritative blindness to a clean direct-answer population

It is primarily:

1. a broad evaluator-owned fallback surface versus a stricter scorer-owned evidence surface

## Surface Reliability Assessment

Interpretability:

1. low
2. the surface name implies genuine direct-answer substitution, but the counted population is mostly contamination-heavy echo

Reproducibility:

1. high
2. prior spike and forensics work established stable repeated-run counts and stable row sets

Semantic stability:

1. low
2. the surface consistently counts a stable invalid-output population, but that population is not semantically aligned with the surface label

Operational usefulness:

1. limited and indirect
2. it remains usable as a detector-facing warning signal for invalid echo-like tool failures
3. it is not strong evidence about true direct-answer substitution behavior

Suitability for detector-facing use:

1. operationally usable but semantically weak

## Strategic Interpretation

What runtime forensics revealed about this surface:

1. the legacy surface is not measuring a hidden authoritative positive class
2. the disagreement is not mainly a missing-metadata story
3. the counted population is overwhelmingly transcript-contaminated prompt/task echo

Previously plausible explanations weakened:

1. that authoritative scoring simply failed to notice many clean direct-answer rows
2. that the disagreement mostly reflects metadata or row-fact incompleteness
3. that the legacy surface is broadly semantically faithful but stricter than the authoritative path

Explanations strengthened:

1. the legacy surface is primarily a broad invalid-output fallback counter
2. the surface label overstates the semantic specificity of what is being counted
3. runtime output regime is the main source of disagreement

What the repository now knows that it did not know before:

1. the legacy direct-answer surface is a stable proxy for contamination-heavy invalid outputs
2. it is not a faithful direct measure of genuine direct-answer substitution behavior

## Future Direction Assessment

Highest-information-gain next area:

1. runtime-output analysis

Secondary area:

1. corpus analysis

Why:

1. the legacy surface semantics are now well-characterized
2. the dominant remaining uncertainty is the output regime the corpus elicits
3. further legacy-surface analysis is likely to have diminishing returns relative to runtime or corpus investigation

## Final Question

Based on direct examination of repository artifacts and runtime outputs, is the legacy `direct_answer_substitution_count` surface measuring the phenomenon it claims to measure?

Not fully.

More precisely:

1. it is not primarily measuring genuine direct-answer substitution behavior
2. it is primarily measuring invalid tool-expected outputs dominated by prompt/task echo with transcript contamination
3. it also includes a small mixed answer-like subset and related echo artifacts

Repository conclusion:

1. treat the surface as a reproducible but materially misaligned proxy for contamination-heavy invalid tool-expected outputs
2. do not interpret it as a semantically faithful direct-answer substitution measure

## Boundary Confirmation

Confirmed unchanged:

1. scorer behavior
2. evaluator behavior
3. detector behavior
4. threshold behavior
5. migration flags
6. governance doctrine
7. readiness state
8. gate state
