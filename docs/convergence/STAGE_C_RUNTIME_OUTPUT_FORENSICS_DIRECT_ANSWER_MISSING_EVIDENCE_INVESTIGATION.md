# Stage C Runtime Output Forensics Direct-Answer Missing-Evidence Investigation

## Scope

This slice investigates the authoritative missing-evidence population for:

- `direct_answer_substitution_count`

It is observational only.

It does not:

1. modify scorer behavior
2. modify evaluator behavior
3. modify detector behavior
4. modify threshold behavior
5. modify migration flags
6. reopen readiness
7. reopen gate
8. perform implementation

## Inputs

Primary runtime artifacts reviewed:

1. `/tmp/stage_c_technical_spike_before/comparison_rows.jsonl`
2. `/tmp/stage_c_technical_spike_before/stage_c_family_a_scorer_evidence_artifact.json`
3. `/tmp/stage_c_technical_spike_before/stage_c_row_fact_metadata_artifact.json`
4. `/tmp/stage_c_technical_spike_before/stage_c_package1c_passive_reconciliation_report.json`
5. `/tmp/stage_c_technical_spike_before/stage_c_package1d_migration_readiness_assessment.json`
6. [stage_c_technical_spike_direct_answer_assessment.json](/opt/ai-stack/assistant-training/manifests/reports/stage_c_technical_spike_direct_answer_assessment.json:1)
7. [stage_c_runtime_output_forensics_direct_answer_missing_evidence_assessment.json](/opt/ai-stack/assistant-training/manifests/reports/stage_c_runtime_output_forensics_direct_answer_missing_evidence_assessment.json:1)

Code surfaces used for runtime predicate interpretation:

1. [eval_canonical_manifest.py](/opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py:205)
2. [stage_c1_evaluator_foundation.py](/opt/ai-stack/assistant-training/scripts/stage_c1_evaluator_foundation.py:1)

## Summary Determination

The authoritative missing-evidence population persists primarily because the frozen-corpus runtime outputs do not expose clean scorer-owned substitution evidence.

Observed runtime shape:

1. `134/134` missing-evidence rows remained `primary_class=invalid_json`
2. `134/134` remained `parse_mode=invalid`
3. `134/134` remained `schema_reason=payload_not_parsed`
4. `0/134` satisfied the live tool-intent predicate
5. `0/134` satisfied the bounded scalar-substitution predicate

The missing-evidence population is therefore not being held open by missing row identity, missing metadata, or hidden clean scalar outputs.

It is being held open by actual emitted output structure.

## Missing-Evidence Population Inventory

Population counts:

1. missing-evidence rows: `134`
2. structurally incapable rows: `131`
3. ambiguous rows: `3`
4. reconciliation state: `requires_future_migration`
5. readiness state: `migration-blocked`

Split distribution:

1. `heldout_validation`: `94`
2. `tool_holdout`: `40`

Legacy subtype distribution inside the authoritative missing-evidence cohort:

1. legacy `direct_answer_substitution`: `125`
2. legacy `malformed_partial_json`: `9`

Expected-tool distribution is broad, not concentrated in one tool:

1. `rg_search`: `46`
2. `read_file`: `27`
3. `find_files`: `12`
4. `debug_tools`: `7`
5. `check_service_health`: `6`
6. `get_system_datetime`: `6`

Artifact coverage was complete for the missing-evidence cohort:

1. comparison rows resolved: `134/134`
2. row facts resolved: `134/134`
3. scorer evidence records resolved: `134/134`

## Runtime Output Examination

The authoritative pathway did not fail because records were absent.

It failed because the runtime outputs did not present governed evidence in an observable form.

Key runtime predicate observations:

1. missing rows with tool-intent signal: `0`
2. subtype-assigned rows with tool-intent signal: `6`
3. missing rows with scalar-candidate signal: `0`
4. subtype-assigned rows with scalar-candidate signal: `0`

The only currently assigned authoritative subtype remained:

1. `malformed output`: `6`

Those `6` rows are precisely the rows whose invalid output still crosses `_looks_like_tool_intent(...)`.

Representative missing-output examples:

1. task/prompt echo with transcript contamination
   - `heldout_validation:1`
   - `Show /opt/ai-stack/runtimes/assistant-runtime/server/agent.py starting at line 1080 for 25 lines and report one symbol name.\n[SYSTEM]...`
2. pure transcript contamination
   - `heldout_validation:4`
   - `[SYSTEM]\nUse ONLY the exact tool requested. Keep final answer concise...`
3. answer-prefix plus transcript contamination
   - `heldout_validation:10`
   - `The first function name is: main\n[SYSTEM]...`
4. instructional assertion plus transcript contamination
   - `heldout_validation:44`
   - `Tool validation is not required for this task.\n[SYSTEM]...`
5. tool-label repetition
   - `heldout_validation:11`
   - `Tool: python\nTool: python\nTool: python...`
6. task/prompt echo without transcript contamination
   - `heldout_validation:50`
   - `Use json_edit on /opt/ai-stack/runtimes/assistant-runtime/.state/.tool_ft_tmp.json ...`

What evidence was absent:

1. no strict JSON scalar outputs
2. no clean direct-answer-only outputs
3. no clean scalar-only outputs
4. no malformed outputs with tool-intent signal inside the missing-evidence cohort

## Blocker Taxonomy

Repository-derived blocker categories:

| Category | Rows | Cohort | Observability | Remediability |
|---|---:|---|---|---|
| task/prompt echo with transcript contamination | 116 | structurally incapable | absent from runtime outputs | currently non-remediable |
| pure transcript contamination | 9 | structurally incapable | absent from runtime outputs | currently non-remediable |
| instructional assertion plus transcript contamination | 4 | structurally incapable | absent from runtime outputs | currently non-remediable |
| answer-prefix plus transcript contamination | 3 | ambiguous | indirectly observable | possibly remediable |
| tool-label repetition | 1 | structurally incapable | absent from runtime outputs | currently non-remediable |
| task/prompt echo without transcript contamination | 1 | structurally incapable | absent from runtime outputs | currently non-remediable |

The taxonomy aligns exactly with the protected cohorts:

1. `131` structurally incapable rows = every category except answer-prefix contamination
2. `3` ambiguous rows = answer-prefix contamination only

## Cohort Distribution Assessment

Dominant blocker category:

1. task/prompt echo with transcript contamination: `116/134`

Rare categories:

1. answer-prefix plus transcript contamination: `3`
2. instructional assertion plus transcript contamination: `4`
3. tool-label repetition: `1`
4. task/prompt echo without transcript contamination: `1`

Clustering observations:

1. all `40` `tool_holdout` rows fall into the dominant task/prompt-echo category
2. pure transcript contamination appears only in `heldout_validation`
3. the three known ambiguous rows align exactly with the answer-prefix category

## Remediability Assessment

Category-level assessment:

1. task/prompt echo with transcript contamination
   - currently non-remediable on the frozen corpus
   - rationale: no clean scorer-owned substitution evidence is present
2. pure transcript contamination
   - currently non-remediable
   - rationale: output is transcript replay only
3. instructional assertion plus transcript contamination
   - currently non-remediable
   - rationale: output asserts tool-policy-like text rather than governed substitution evidence
4. answer-prefix plus transcript contamination
   - possibly remediable
   - rationale: answer-like material exists, but only in mixed contaminated form
5. tool-label repetition
   - currently non-remediable
6. task/prompt echo without transcript contamination
   - currently non-remediable

This assessment is observational only.

It does not recommend implementation.

## Observability Assessment

Direct-answer target:

1. classification: `theoretically representable but not directly observable`
2. rationale: the only answer-like outputs are the `3` ambiguous rows, and each is mixed with transcript contamination

Scalar target:

1. classification: `absent from runtime outputs`
2. rationale: `0` missing rows satisfied the strict scalar predicate and `0` authoritative scalar rows were emitted

Overall surface observability:

1. classification: `theoretically representable but not observable on the frozen corpus`
2. rationale: runtime outputs expose echo and contamination patterns rather than clean scorer-owned substitution evidence

## Legacy Versus Authoritative Gap Analysis

Legacy surface:

1. direct-answer count: `125`
2. scalar-substitution count: `0`
3. malformed-partial-json count: `15`

Authoritative surface:

1. direct-answer count: `0`
2. scalar-substitution count: `0`
3. malformed-output count: `6`
4. missing-evidence rows that legacy counts as direct-answer: `125`
5. missing-evidence rows that legacy counts as malformed-partial-json: `9`

Primary explanation for the `125` vs `0` gap:

1. legacy text-pattern classification treats many evidence-poor invalid outputs as `direct_answer_substitution`
2. the authoritative pathway requires scorer-owned observable evidence and therefore preserves missingness
3. the gap is therefore mainly evidence-interpretation mismatch over evidence-poor runtime outputs, not missing row identity or missing metadata

## Strategic Interpretation

What the technical spike taught us:

1. the smallest governance-safe scalar pathway change was a real runtime no-op
2. no hidden scalar-candidate rows exist on the frozen corpus
3. the missing-evidence cohort never crosses the live tool-intent predicate either

Previously plausible explanations weakened by direct artifact review:

1. that clean scalar rows were present but merely unreachable
2. that row-fact or ownership metadata gaps were driving the blocker
3. that a trivial bounded scorer-pathway patch was likely to surface new authoritative evidence

Explanations strengthened by direct artifact review:

1. runtime outputs are dominated by transcript contamination and prompt/task echo
2. the legacy direct-answer count is largely an interpretation of invalid text, not a direct observation of governed substitution evidence
3. the dominant remaining uncertainty is observability of scorer-owned evidence in the emitted outputs

## Future-Investigation Assessment

Highest-information next uncertainty:

1. runtime outputs

Why:

1. the current artifacts already localize the problem away from row facts, metadata, and simple bounded scorer mechanics
2. the remaining question is what output regime the frozen corpus actually elicits
3. corpus composition is the secondary uncertainty because the `tool_holdout` split contributes `40` structurally incapable rows inside the dominant echo category

## Final Question

Based on direct examination of runtime artifacts, what is the most likely explanation for the persistence of the authoritative missing-evidence population?

The most likely explanation is that the frozen-corpus outputs almost never contain clean scorer-owned substitution evidence at all.

Instead:

1. `131` rows are structurally incapable prompt/task or transcript echoes
2. `3` rows are answer-like prefixes immediately mixed with transcript contamination
3. `0` rows satisfy the live tool-intent predicate
4. `0` rows satisfy the bounded scalar-substitution predicate

Because the runtime outputs themselves never present governed substitution evidence in an observable form, the authoritative pathway continues to preserve missing evidence rather than emit direct-answer or scalar-substitution rows.

## Boundary Confirmation

Confirmed unchanged:

1. scorer behavior
2. evaluator behavior
3. detector behavior
4. threshold behavior
5. migration flags
6. readiness state
7. gate state
