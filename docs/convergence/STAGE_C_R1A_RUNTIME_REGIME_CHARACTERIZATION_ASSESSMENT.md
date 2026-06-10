# Stage C R1A Runtime Regime Characterization Assessment

## Executive Summary

This is a read-only characterization of frozen Stage C artifacts. No new runtime evaluations were run, and no detector, scorer, threshold, governance, migration, or corpus changes were made.

The evidence splits into two observable layers:

1. A 134-row authoritative missing-evidence cohort from runtime-output forensics and blocker-persistence artifacts.
2. An 8-record C4/C5/C6 operational output-shape sample from ingestion, scoring, and reporting artifacts.

The dominant regime in the authoritative cohort is prompt/task echo with transcript contamination: `116/134` rows, or `86.6%`.

The three ambiguous rows are best treated as boundary cases of that same contamination regime, not as a separate clean direct-answer population.

The most predictive variable overall is contamination motif. Split is secondary. Tool family is weak. Output shape is highly informative inside the small operational sample, but it does not explain the full frozen corpus as well as contamination motif.

No authoritative frozen artifact in the examined set shows clean direct-answer or scalar substitution evidence.

## Evidence Base

Direct runtime evidence used here:

- `docs/convergence/STAGE_C_RECONNAISSANCE_AND_EVIDENCE_INVENTORY.md`
- `manifests/reports/stage_c_runtime_output_forensics_direct_answer_missing_evidence_assessment.json`
- `manifests/reports/stage_c_legacy_surface_validity_direct_answer_assessment.json`
- `manifests/reports/stage_c_technical_spike_direct_answer_assessment.json`
- `manifests/reports/stage_c_package5b_direct_answer_blocker_persistence_assessment.json`
- `reports/stage_c4/contract_artifacts/c4_output_inventory_artifact.json`
- `reports/stage_c4/contract_artifacts/c4_parse_toolcall_status_artifact.json`
- `reports/stage_c5/contract_artifacts/c5_per_output_scoring_status_artifact.json`
- `reports/stage_c5/contract_artifacts/c5_parse_tool_nocall_scoring_summary_artifact.json`
- `reports/stage_c5/contract_artifacts/c5_wrapper_leakage_scoring_summary_artifact.json`
- `reports/stage_c5/contract_artifacts/c5_validation_issues_artifact.json`
- `reports/stage_c6/reporting_artifacts/c6_runtime_scoring_summary_artifact.json`
- `reports/stage_c6/reporting_artifacts/c6_parse_tool_nocall_summary_artifact.json`
- `reports/stage_c6/reporting_artifacts/c6_wrapper_leakage_summary_artifact.json`
- `reports/stage_c6/reporting_artifacts/c6_validation_issue_summary_artifact.json`

Evidence quality notes:

- Direct and trustworthy for runtime characterization: runtime forensics, technical spike, blocker persistence, and the C4/C5/C6 output artifacts.
- Indirect but still useful as a proxy check: the legacy surface validity assessment.
- The operational sample is small, so it supports regime identification, not population-wide rate claims outside the 8-record sample.

## A. Runtime Regime Taxonomy

### A1. Authoritative missing-evidence cohort

These regimes come from the 134-row authoritative missing-evidence population in the runtime-forensics report.

| Regime | Identifying characteristics | Count | Share of cohort | Evidence directness |
|---|---|---:|---:|---|
| Prompt/task echo with transcript contamination | Output restates the task or prompt and carries transcript markers | 116 | 86.6% | Direct |
| Pure transcript contamination | Transcript markers appear without the stronger task/prompt echo pattern | 9 | 6.7% | Direct |
| Instructional assertion plus transcript contamination | Output asserts instructions or meta-instructions before transcript markers | 4 | 3.0% | Direct |
| Answer-prefix plus transcript contamination | Output begins with answer-like text and then mixes transcript markers | 3 | 2.2% | Direct, but these 3 rows are the ambiguous cohort |
| Task/prompt echo without transcript contamination | Task echo is present, but transcript markers are absent | 1 | 0.7% | Direct |
| Tool-label repetition | Repeated tool-label strings appear without a valid payload | 1 | 0.7% | Direct |

Observed cohort shape:

- `131/134` rows are structurally incapable of supporting a clean approved direct-answer or scalar substitution claim.
- `3/134` rows are ambiguous, but they still land in the answer-prefix plus transcript contamination regime.
- The authoritative report records `0` genuine direct-answer rows and `0` scalar-substitution rows.

### A2. Operational output-shape sample

These regimes come from the 8-record C4/C5/C6 sample. Each regime appears once, so each is `12.5%` of the sample.

| Regime | Record id | Identifying characteristics | Count | Share of sample |
|---|---|---|---:|---:|
| Exact-valid tool-call completion | `score-001` | Strict JSON, correct tool, complete arguments, no wrapper leakage | 1 | 12.5% |
| Malformed payload / parse failure | `score-002` | Invalid JSON, no parseable payload | 1 | 12.5% |
| Missing tool call | `score-003` | Strict JSON, but `tool_calls` key missing where required | 1 | 12.5% |
| Argument drift / partial payload | `score-004` | Tool call is present, but arguments are missing or incomplete | 1 | 12.5% |
| Wrong-tool selection | `score-005` | Tool call is present, but the emitted tool name differs from the expected one | 1 | 12.5% |
| Wrapper / envelope drift | `score-006` | Invalid JSON with embedded object plus wrapper/prose leakage | 1 | 12.5% |
| Clean no-call emission | `score-007` | Strict JSON with empty `tool_calls` where no-call is expected | 1 | 12.5% |
| No-call restraint failure | `score-008` | A tool call is emitted where no-call was expected | 1 | 12.5% |

Operational summary:

- `2/8` records pass overall.
- `6/8` records fail overall.
- `23` combined validation issues are recorded across C4 and C5.
- Wrapper leakage is observed once, on `score-006`.

## B. Regime Distribution Assessment

### Measured findings

The authoritative missing-evidence cohort is the main population for corpus-scale regime characterization.

| Evidence family | Observation | Count / ratio | Directness |
|---|---|---:|---|
| Missing-evidence cohort | Total rows | `134` | Direct |
| Missing-evidence cohort | Split distribution | `94` heldout_validation, `40` tool_holdout | Direct |
| Missing-evidence cohort | Dominant contamination regime | `116/134` prompt/task echo with transcript contamination | Direct |
| Missing-evidence cohort | Remaining contamination regimes | `9` pure transcript contamination, `4` instructional assertion plus transcript contamination, `3` answer-prefix plus transcript contamination, `1` task/prompt echo without transcript contamination, `1` tool-label repetition | Direct |
| Missing-evidence cohort | Tool-family concentration | Dominant regime spans many tool families; largest are `rg_search` and `read_file` | Direct |
| Missing-evidence cohort | Ambiguous cohort | `3` rows, all in heldout_validation, all answer-prefix plus transcript contamination | Direct |
| Legacy surface proxy | Legacy direct-answer proxy rows | `125` | Indirect/proxy |
| Legacy surface proxy | Overlap with authoritative missing-evidence | `125/125` overlap, `100%` | Indirect/proxy |
| Legacy surface proxy | Genuine authoritative direct-answer rows | `0` | Indirect/proxy |
| Technical spike | Direct-answer and scalar deltas | `0` delta before vs after | Direct |
| Blocker persistence | Repeated-run stability | Strongly reproducible; identical row identities and blocker shape across runs | Direct |
| C4/C5/C6 sample | Output-shape regimes | 8 distinct regimes, one per record | Direct |
| C4/C5/C6 sample | Validation burden | `2` pass, `6` fail, `23` combined validation issues | Direct |

Tool-family distribution within the missing-evidence cohort is broad, which is why tool family is not a strong explanatory variable.

- `rg_search` and `read_file` are the largest families inside the dominant contamination regime.
- `rg_search` also dominates the two smaller answer-like contamination motifs.
- `json_edit` appears only in the single task/prompt echo without transcript contamination row.
- `read_file` appears in the tool-label repetition singleton and in the pure transcript contamination subset.

### Inferred findings

- The missing-evidence cohort is not a clean direct-answer population. It is a contamination-heavy proxy surface.
- Split is a secondary correlate. All `40` tool_holdout rows fall inside the dominant prompt/task echo with transcript contamination regime.
- Tool family is weak as a regime selector because the dominant regime spans many families and the same family can appear in multiple regimes.
- The operational sample shows that tool-call failure can fragment into parse failure, missing call, wrong tool, argument drift, wrapper leakage, and no-call restraint failure. That makes output shape highly useful inside the small sample, but not sufficient by itself to explain the corpus-scale contamination regime.
- The three ambiguous rows are boundary cases of the dominant contamination regime, not a separate clean direct-answer class.

### Unresolved findings

- Whether split is causal, merely correlated, or only a partial amplifier of the dominant contamination regime.
- Whether tool family contributes causally or only mirrors prompt composition.
- Whether the ambiguous cohort is a distinct subcluster or just the thin edge of the dominant contamination pattern.
- Whether any hidden clean positive population exists outside the currently observed frozen artifacts. The current evidence does not show one, but that remains a negative inference.

## C. Explanatory Power Assessment

| Observed variable | Predictive value | Evidence basis |
|---|---|---|
| Contamination motif | Strongest overall | The 134-row authoritative cohort is partitioned cleanly by contamination motif, with one motif dominating `116/134` rows |
| Output shape | Strong inside the operational sample | The 8-record C4/C5/C6 sample cleanly separates valid completion, malformed payload, missing call, wrong tool, wrong args, wrapper drift, clean no-call, and no-call failure |
| Split | Secondary | All `40` tool_holdout rows are inside the dominant regime, but minority regimes are heldout_validation-only |
| Tool family | Weak | The dominant regime spans many tool families, and the same family appears across multiple regimes |
| None of the above | Not supported | The observed regimes are explainable by the listed variables, with contamination motif the best overall explanation |

Bottom line:

- The most predictive explanatory variable appears to be contamination motif.
- Output shape is the best local descriptor for the 8-record operational sample.
- Split is secondary.
- Tool family is weak.

## D. Ambiguous Cohort Assessment

The runtime-forensics report marks these three rows as ambiguous, with `cohort_classification = ambiguous`, `observability = indirectly observable`, and `remediability = possibly remediable`.

| Row id | Split | Expected tool | Legacy subtype | Observable pattern | Assessment |
|---|---|---|---|---|---|
| `heldout_validation:10` | heldout_validation | `rg_search` | direct_answer_substitution | Answer-like prefix followed by transcript contamination | Boundary case of dominant contamination regime |
| `heldout_validation:28` | heldout_validation | `rg_search` | direct_answer_substitution | Answer-like prefix followed by transcript contamination | Boundary case of dominant contamination regime |
| `heldout_validation:77` | heldout_validation | `rg_search` | direct_answer_substitution | Answer-like prefix followed by transcript contamination | Boundary case of dominant contamination regime |

Why these are not a separate clean regime:

- All three are still transcript-contaminated.
- All three are in heldout_validation, not tool_holdout.
- All three expect `rg_search`.
- All three carry the same legacy direct-answer substitution label, but the authoritative runtime-forensics report does not elevate them into a clean direct-answer class.

Conclusion on the ambiguous cohort:

- They are not genuinely distinct from the dominant contamination regime on the evidence currently available.
- They are best treated as boundary cases of that regime.

## E. Stage C-R1A Conclusions

### What runtime regimes exist?

- Prompt/task echo with transcript contamination.
- Pure transcript contamination.
- Instructional assertion plus transcript contamination.
- Answer-prefix plus transcript contamination.
- Task/prompt echo without transcript contamination.
- Tool-label repetition.
- Exact-valid tool-call completion.
- Malformed payload / parse failure.
- Missing tool call.
- Wrong-tool selection.
- Argument drift / partial payload.
- Wrapper / envelope drift.
- Clean no-call emission.
- No-call restraint failure.

### Which regime dominates?

- Prompt/task echo with transcript contamination dominates the frozen evidence set.
- It accounts for `116/134` rows, or `86.6%`, of the authoritative missing-evidence cohort.

### What evidence supports that conclusion?

- The runtime-forensics report explicitly partitions the 134-row missing-evidence cohort and shows the dominant contamination regime at `116` rows.
- The same report shows the remaining rows are smaller contamination variants, not a clean direct-answer or scalar population.
- The legacy direct-answer proxy surface overlaps the authoritative missing-evidence rows at `125/125`, which shows the old surface is a proxy over contaminated outputs rather than a semantic direct-answer class.
- The technical spike reports `0` deltas for direct-answer and scalar evidence across repeated before/after runs.
- The blocker-persistence assessment reports stable row identities, blocker reasons, and legacy surface snapshots across repeated runs.
- The C4/C5/C6 sample independently shows the operational surface can express clean completion, malformed payload, missing call, wrong tool, wrong arguments, wrapper leakage, and no-call restraint failure, which is consistent with a contamination-heavy environment rather than a clean direct-answer population.

### What remains unknown?

- Whether split or tool family is causal rather than correlated.
- Whether the ambiguous rows form a true subcluster or are simply the edge of the dominant regime.
- Whether any hidden clean positive population exists outside the frozen artifacts currently in scope.

### Direct answers to the core questions

- What runtime regimes exist? The corpus-level contamination regimes plus the smaller operational output-shape regimes listed above.
- Which regime dominates? Prompt/task echo with transcript contamination.
- What evidence supports that conclusion? The 134-row runtime-forensics partition, the 100% overlap between the legacy proxy surface and authoritative missing-evidence rows, and the repeated-run stability checks.
- What remains unknown? The causal role of split and tool family, the distinctness of the ambiguous cohort, and whether any unseen clean positive class exists.

### What do we already know?

- The frozen corpus does not provide clean authoritative direct-answer or scalar substitution evidence.
- The dominant observed behavior is contamination-heavy prompt/task echo.
- The ambiguous rows do not escape that contamination regime.

### What do we think we know?

- The legacy direct-answer surface is a contaminated proxy, not a faithful semantic measure.
- The operational failure modes are stable enough to separate into parse failure, missing call, wrong tool, argument drift, wrapper drift, and no-call failure.
- Contamination motif is the best overall explanation of regime membership.

### What do we not yet know?

- Why the dominant contamination regime is so stable.
- Whether split and tool family are causal or just correlated.
- Whether the ambiguous cohort is genuinely distinct.
- Whether any hidden clean positive population exists beyond the currently observed frozen artifacts.
