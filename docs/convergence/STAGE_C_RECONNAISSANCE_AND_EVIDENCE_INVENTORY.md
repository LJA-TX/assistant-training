# Stage C Reconnaissance And Evidence Inventory

## Executive Summary

Stage C already has substantial evidence, but most of it points in the same direction: the frozen corpus does not surface a clean governed direct-answer or scalar population, and the legacy direct-answer surface is best treated as a contamination-heavy proxy rather than a faithful semantic measure.

The strongest evidence comes from the runtime-output forensics, the repeated-run technical spike, and the blocker-persistence assessment. Those artifacts are direct, stable across repeated runs, and explicitly preserve guardrails and row identities. The evaluator/scoring chain artifacts add useful direct evidence about parse failures, no-call mismatches, wrapper leakage, and partial tool payloads, but they are narrower samples than the full missing-evidence cohort.

What is still missing is not more migration work. It is a sharper behavioral explanation for the frozen corpus: why the dominant contamination regime appears so stable, whether it clusters by split or corpus family beyond the current observations, and whether the small ambiguous cohort is genuinely distinct or just a thin edge of the same regime.

### What do we already know?

- The authoritative missing-evidence population is stable and large: `134` rows.
- That population splits into `131` structurally incapable rows and `3` ambiguous rows.
- The missing-evidence rows never hit the live tool-intent predicate and never hit the bounded scalar predicate.
- The legacy `direct_answer_substitution_count` surface is not observing a hidden clean positive class; it is counting mostly invalid, echoed, or contaminated outputs.
- The repeated-run blocker inventory is stable across runs, with identical row identities and identical blocker shape.
- The current evaluator/scoring pipeline preserves malformed outputs, partial arguments, wrapper leakage, and no-call mismatches without reconstruction or inference.

### What do we think we know?

- The dominant runtime regime is prompt/task echo with transcript contamination, not a clean direct-answer regime.
- Corpus composition likely contributes materially to the observed regime, because the `tool_holdout` rows cluster inside the dominant echo category.
- The `3` ambiguous rows look like a small answer-prefix contamination cohort rather than a clean direct-answer subpopulation.
- Wrapper leakage, argument drift, and no-call restraint failures are real, but they appear as secondary behaviors rather than the dominant regime.

### What do we not yet know?

- Whether corpus composition is causal, merely correlated, or only a partial amplifier of the dominant regime.
- Whether the ambiguous rows are a distinct subcluster or just a boundary case of the same contamination pattern.
- Whether tool overcalling, tool undercalling, wrapper persistence, and argument drift have consistent rates across splits beyond the current sample and cohort-level observations.
- Whether any hidden clean positive population exists outside the currently observed frozen artifacts. Current evidence says no, but that remains a negative conclusion, not a positive causal explanation.

## Evidence Inventory

### 1. Launch And Transition Context

| Artifact path | Artifact type | Creation purpose | Current relevance to Stage C |
|---|---|---|---|
| `docs/current/current_status.md` | Status document | Records the current repository boundary and what remains parked | High as context; it confirms the Stage C runtime-output / corpus-behavior family is parked |
| `docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md` | Launch plan | Defines the runtime-output / corpus-behavior investigation family and its questions | High as framing; it states the scope and the expected evidence shape |
| `docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN_ACCEPTANCE_ASSESSMENT.md` | Acceptance assessment | Confirms the launch plan was accepted without executing runtime analysis | Medium; it marks the boundary between planning and evidence work |
| `docs/current/roadmap/STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN_IMPLEMENTATION_SUMMARY.md` | Implementation summary | Records the launch-plan package deliverable set | Medium; it is procedural context, not runtime evidence |
| `docs/continuity/post-publication_transition_return_to_stage_c_continuity_2026-06-09.md` | Continuity memo | Re-centers the project on Stage C runtime-output investigation | High as transition context; not direct runtime evidence |

### 2. Runtime-Output Forensics And Legacy-Surface Evidence

| Artifact path | Artifact type | Creation purpose | Current relevance to Stage C |
|---|---|---|---|
| `manifests/reports/stage_c_runtime_output_forensics_direct_answer_missing_evidence_assessment.json` | Machine-readable forensic assessment | Classifies the authoritative missing-evidence cohort and its output shapes | Very high; this is one of the strongest direct evidence sources |
| `docs/convergence/STAGE_C_RUNTIME_OUTPUT_FORENSICS_DIRECT_ANSWER_MISSING_EVIDENCE_INVESTIGATION.md` | Investigation narrative | Explains what the runtime outputs actually look like and what the missing-evidence cohort contains | Very high; direct explanation of runtime behavior |
| `docs/convergence/STAGE_C_RUNTIME_OUTPUT_FORENSICS_DIRECT_ANSWER_MISSING_EVIDENCE_ACCEPTANCE_ASSESSMENT.md` | Acceptance assessment | Confirms the forensics slice established the missing-evidence cohort properties | High; it marks the evidence as accepted and stable |
| `docs/convergence/STAGE_C_RUNTIME_OUTPUT_FORENSICS_DIRECT_ANSWER_MISSING_EVIDENCE_IMPLEMENTATION_SUMMARY.md` | Implementation summary | Records the read-only analyzer and the evidence it emits | High; useful for provenance and scope boundaries |
| `manifests/reports/stage_c_legacy_surface_validity_direct_answer_assessment.json` | Machine-readable assessment | Compares the legacy direct-answer surface with authoritative evidence | Very high; it supports the proxy-vs-semantic validity judgment |
| `docs/convergence/STAGE_C_LEGACY_SURFACE_VALIDITY_ASSESSMENT_DIRECT_ANSWER_SUBSTITUTION.md` | Investigation narrative | Characterizes what the legacy direct-answer surface is actually measuring | Very high; direct evidence about semantic misalignment |
| `docs/convergence/STAGE_C_LEGACY_SURFACE_VALIDITY_ASSESSMENT_DIRECT_ANSWER_SUBSTITUTION_ACCEPTANCE_ASSESSMENT.md` | Acceptance assessment | Confirms the legacy-surface validity finding | High; it documents the accepted conclusion |

### 3. Technical Spike And Repeated-Run Persistence

| Artifact path | Artifact type | Creation purpose | Current relevance to Stage C |
|---|---|---|---|
| `manifests/reports/stage_c_technical_spike_direct_answer_assessment.json` | Machine-readable assessment | Captures before/after runtime deltas for the scorer-pathway spike | Very high; it is direct evidence that the bounded scorer change was runtime-inert |
| `manifests/reports/stage_c_technical_spike_direct_answer_bundle_before.json` | Run bundle | Captures the pre-change state of the frozen corpus outputs | Very high; it is the baseline half of the repeated-run comparison |
| `manifests/reports/stage_c_technical_spike_direct_answer_bundle_after_run_a.json` | Run bundle | Captures after-run-A state | Very high; used for stability and delta analysis |
| `manifests/reports/stage_c_technical_spike_direct_answer_bundle_after_run_b.json` | Run bundle | Captures after-run-B state | Very high; used for repeated-run reproducibility |
| `docs/convergence/STAGE_C_TECHNICAL_SPIKE_DIRECT_ANSWER_SCORER_PATHWAY_EVIDENCE_EMISSION_PROBE.md` | Investigation narrative | Describes the bounded scorer-pathway evidence-emission probe | Very high; direct runtime evidence and containment boundary |
| `docs/convergence/STAGE_C_TECHNICAL_SPIKE_DIRECT_ANSWER_SCORER_PATHWAY_EVIDENCE_EMISSION_PROBE_ACCEPTANCE_ASSESSMENT.md` | Acceptance assessment | Confirms the spike stayed inside its authorized boundary and produced stable results | High; validates trustworthiness of the spike evidence |
| `docs/convergence/STAGE_C_TECHNICAL_SPIKE_DIRECT_ANSWER_SCORER_PATHWAY_EVIDENCE_EMISSION_PROBE_IMPLEMENTATION_SUMMARY.md` | Implementation summary | Records the probe slice and the emitted assessment | High; provenance for the spike artifacts |

### 4. Blocker Persistence And Post-Blocker Branch Evidence

| Artifact path | Artifact type | Creation purpose | Current relevance to Stage C |
|---|---|---|---|
| `manifests/reports/stage_c_package5b_direct_answer_blocker_bundle_run_a.json` | Run bundle | First repeated full run for blocker persistence | Very high; direct persistence evidence |
| `manifests/reports/stage_c_package5b_direct_answer_blocker_bundle_run_b.json` | Run bundle | Second repeated full run for blocker persistence | Very high; direct persistence evidence |
| `manifests/reports/stage_c_package5b_direct_answer_blocker_persistence_assessment.json` | Machine-readable assessment | Compares run A and run B for blocker stability | Very high; the key repeated-run persistence artifact |
| `docs/convergence/STAGE_C_PACKAGE_5B_DIRECT_ANSWER_SUBSTITUTION_BLOCKER_PERSISTENCE_ASSESSMENT.md` | Investigation narrative | Explains the stable blocker shape, row identities, and lack of direct-answer/scalar emission | Very high; direct evidence and interpretation |
| `docs/convergence/STAGE_C_PACKAGE_7D_DIRECT_ANSWER_SCORER_PATHWAY_INVESTIGATION.md` | Investigation narrative | Localizes the live authoritative gap to scorer-pathway handoff logic | High; useful for ownership localization, not for new runtime facts |

### 5. Evaluator, Ingestion, Scoring, And Reporting Chain

| Artifact path | Artifact type | Creation purpose | Current relevance to Stage C |
|---|---|---|---|
| `reports/stage_c1/stage_c1_fixture_harness_report.json` | Harness report | Confirms the Stage C1 fixture harness baseline | Medium; foundational, not runtime-output specific |
| `reports/stage_c2/stage_c2_foundation_report.json` | Foundation report | Records family aggregation and reconciliation foundation | Medium; foundational evidence for later stages |
| `reports/stage_c3/baseline_contract_artifacts/c3_runtime_contract_summary_artifact.json` | Runtime contract summary | Captures the baseline runtime contract state | High; direct preservation evidence |
| `reports/stage_c3/baseline_contract_artifacts/c3_fixture_inventory_artifact.json` | Fixture inventory | Enumerates the baseline fixture coverage | High; direct evidence of coverage and split structure |
| `reports/stage_c3/baseline_contract_artifacts/c3_state_axis_artifact.json` | State-axis artifact | Preserves completeness / computability / comparability axes | High; direct evidence that state axes are separated, not collapsed |
| `reports/stage_c3/baseline_contract_artifacts/c3_validation_issues_artifact.json` | Validation issues artifact | Lists baseline validation issues | High; shows the absence of runtime reconstruction or inference issues |
| `reports/stage_c3/baseline_contract_artifacts/c3_governance_guardrails_artifact.json` | Guardrails artifact | Records guardrail status | High; direct preservation evidence |
| `reports/stage_c3/baseline_contract_artifacts/c3_reconciliation_summary_artifact.json` | Reconciliation summary | Summarizes partition and reconciliation checks | High; direct preservation evidence |
| `reports/stage_c4/input/stage_c4_sample_output_records.jsonl` | Raw output sample | Sample runtime outputs for Stage C4 real-output ingestion | High; direct evidence of emitted text shapes |
| `reports/stage_c4/contract_artifacts/c4_output_inventory_artifact.json` | Output inventory artifact | Classifies raw outputs by parse/tool/no-call status | Very high; direct behavioral evidence |
| `reports/stage_c4/contract_artifacts/c4_parse_toolcall_status_artifact.json` | Parse/tool status artifact | Records parse status and tool-call status per record | Very high; direct evidence for schema drift, argument drift, and call omission |
| `reports/stage_c4/contract_artifacts/c4_state_axis_from_outputs_artifact.json` | State-axis artifact | Preserves completeness/computability/comparability for output records | Very high; direct evidence that no collapse occurred |
| `reports/stage_c4/contract_artifacts/c4_row_fact_metadata_artifact.json` | Row-fact metadata artifact | Carries provenance, expected tool names, and guardrail flags | Very high; direct provenance and ownership evidence |
| `reports/stage_c4/contract_artifacts/c4_runtime_contract_summary_artifact.json` | Runtime contract summary | Summarizes record counts, validation issues, and guardrail state | High; useful aggregate evidence |
| `reports/stage_c4/contract_artifacts/c4_reconciliation_summary_from_outputs_artifact.json` | Reconciliation summary | Checks output-derived reconciliation arithmetic | High; evidence of internal consistency |
| `reports/stage_c4/contract_artifacts/c4_validation_issues_artifact.json` | Validation issues artifact | Enumerates parse/tool-call issues | Very high; direct evidence for malformed output, tool omission, and wrapper leakage |
| `reports/stage_c5/input/stage_c5_sample_output_records.jsonl` | Raw output sample | Sample runtime outputs for Stage C5 scoring | High; direct evidence of scoring behavior on emitted text |
| `reports/stage_c5/contract_artifacts/c5_runtime_scoring_summary.json` | Scoring summary | Aggregates Stage C5 scoring outcomes | High; direct evaluation evidence |
| `reports/stage_c5/contract_artifacts/c5_per_output_scoring_status_artifact.json` | Per-output scoring status | Per-record scoring and failure reasons | Very high; direct evidence for wrapper leakage, missing args, and no-call mismatches |
| `reports/stage_c5/contract_artifacts/c5_parse_tool_nocall_scoring_summary_artifact.json` | Parse/tool/no-call summary | Aggregates parse, tool-call, and no-call statuses | Very high; direct evidence for call omission and malformed payloads |
| `reports/stage_c5/contract_artifacts/c5_wrapper_leakage_scoring_summary_artifact.json` | Wrapper leakage summary | Aggregates wrapper/prose leakage findings | High; direct evidence of wrapper persistence, but only in a small sample |
| `reports/stage_c5/contract_artifacts/c5_scoring_input_binding_artifact.json` | Scoring input binding artifact | Preserves record-to-expectation binding | High; useful for interpretability and provenance |
| `reports/stage_c5/contract_artifacts/c5_governance_guardrails_artifact.json` | Guardrails artifact | Records no inference / no substitution / no reconstruction behavior | High; direct preservation evidence |
| `reports/stage_c5/contract_artifacts/c5_validation_issues_artifact.json` | Validation issues artifact | Enumerates scoring failures | Very high; direct evidence for tool-call omission, wrong tool name, missing args, and no-call mismatch |
| `reports/stage_c6/input/stage_c6_sample_output_records.jsonl` | Raw output sample | Sample runtime outputs for Stage C6 reporting | High; direct evidence used for report integration |
| `reports/stage_c6/reporting_artifacts/c6_runtime_scoring_summary_artifact.json` | Runtime scoring summary | Stage C6 aggregate runtime scoring | High; direct integration evidence |
| `reports/stage_c6/reporting_artifacts/c6_parse_tool_nocall_summary_artifact.json` | Parse/tool/no-call summary | Stage C6 aggregate parse and call behavior | High; direct aggregate evidence |
| `reports/stage_c6/reporting_artifacts/c6_wrapper_leakage_summary_artifact.json` | Wrapper leakage summary | Stage C6 wrapper summary | Medium-high; same family as C5 wrapper evidence |
| `reports/stage_c6/reporting_artifacts/c6_validation_issue_summary_artifact.json` | Validation issue summary | Stage C6 validation issue aggregate | High; direct aggregate evidence |
| `reports/stage_c6/reporting_artifacts/c6_detector_projection_preparation_artifact.json` | Projection-preparation artifact | Prepares the downstream detector-projection view without changing behavior | High for boundary evidence; indirect for runtime regime evidence |
| `reports/stage_c6/reporting_artifacts/scoring/ingestion/c4_output_inventory_artifact.json` | Ingested output inventory | Re-exposes the C4 output inventory in reporting form | High; direct and easy to consume |
| `reports/stage_c6/reporting_artifacts/scoring/ingestion/c4_reconciliation_summary_from_outputs_artifact.json` | Ingested reconciliation summary | Re-exposes output reconciliation | High; direct consistency evidence |
| `reports/stage_c6/reporting_artifacts/scoring/ingestion/fixture_baseline/c3_runtime_contract_summary_artifact.json` | Ingested baseline summary | Re-exposes the Stage C3 baseline contract state | Medium-high; mostly provenance and continuity |

Related adjacent aggregation artifacts are present as well, including:

- `reports/stage_c4/contract_artifacts/c4_governance_guardrails_artifact.json`
- `reports/stage_c4/contract_artifacts/c4_runtime_integration_summary.json`
- `reports/stage_c5/contract_artifacts/c5_per_fixture_scoring_status_artifact.json`
- `reports/stage_c6/reporting_artifacts/c6_per_fixture_scoring_summary_artifact.json`
- `reports/stage_c6/reporting_artifacts/c6_per_model_scoring_summary_artifact.json`
- `reports/stage_c6/reporting_artifacts/c6_governance_guardrail_summary_artifact.json`

### 6. Detector Projection And Non-Authoritative Adapter Boundary

| Artifact path | Artifact type | Creation purpose | Current relevance to Stage C |
|---|---|---|---|
| `docs/convergence/STAGE_C8_NON_AUTHORITATIVE_DETECTOR_PROJECTION_ADAPTER.md` | Adapter design narrative | Defines a non-authoritative projection adapter | High for boundary control; indirect for runtime characterization |
| `docs/convergence/STAGE_C8_DETECTOR_PROJECTION_ADAPTER_CONFORMANCE_REPORT.md` | Conformance report | Confirms non-authoritative, non-inference, non-reconstruction posture | High for boundary control; not runtime characterization |
| `docs/convergence/STAGE_C10A_NON_AUTHORITATIVE_ADAPTER_INTEGRATION_PLAN.md` | Integration plan | Defines the smallest safe non-authoritative adapter slice | High for boundary control; indirect for runtime characterization |
| `docs/convergence/STAGE_C10A_NON_AUTHORITATIVE_ADAPTER_INTEGRATION_CLOSURE_DETERMINATION.md` | Closure determination | Confirms what can be incorporated without detector migration | High for boundary control |
| `docs/convergence/STAGE_C10B_NON_AUTHORITATIVE_ADAPTER_INTEGRATION_IMPLEMENTATION_SUMMARY.md` | Implementation summary | Records the non-authoritative adapter integration | High for boundary control; indirect for runtime evidence |
| `docs/convergence/STAGE_C10B_NON_AUTHORITATIVE_ADAPTER_INTEGRATION_CONFORMANCE_REPORT.md` | Conformance report | Confirms the adapter remains migration-disabled | High for boundary control |
| `docs/convergence/STAGE_C10C_REFRESHED_DETECTOR_MIGRATION_GATE_REASSESSMENT.md` | Reassessment | Rechecks migration readiness after non-authoritative adapter work | High for boundary control |

## A. Runtime Regime Taxonomy

The taxonomy is layered. The first family comes from the authoritative missing-evidence cohort. The second comes from the smaller C4/C5/C6 output-shape sample.

### A1. Contamination Regimes In The Missing-Evidence Cohort

| Regime | Identifying characteristics | Count | Share |
|---|---|---:|---:|
| Prompt/task echo with transcript contamination | Output restates the task or prompt and carries transcript markers | 116 | 86.6% |
| Pure transcript contamination | Transcript markers are present without the stronger task/prompt echo pattern | 9 | 6.7% |
| Instructional assertion plus transcript contamination | Output asserts instructions or meta-instructions before transcript markers | 4 | 3.0% |
| Answer-prefix plus transcript contamination | Output begins with answer-like text and then mixes in transcript markers | 3 | 2.2% |
| Task/prompt echo without transcript contamination | Task echo is present but transcript markers are not | 1 | 0.7% |
| Tool-label repetition | Repeated tool-label strings appear without a valid payload | 1 | 0.7% |

### A2. Output-Shape Regimes In The C4/C5/C6 Sample

| Regime | Identifying characteristics | Count | Share |
|---|---|---:|---:|
| Exact-valid tool-call completion | Strict JSON, correct tool, complete arguments, no wrapper leakage | 1 | 12.5% |
| Clean no-call emission | Strict JSON with empty `tool_calls` where no-call is expected | 1 | 12.5% |
| Malformed payload / parse failure | Invalid JSON, no parseable payload | 1 | 12.5% |
| Wrapper / envelope drift | Invalid JSON with embedded object plus prose wrapper | 1 | 12.5% |
| Missing tool call | Strict JSON, but `tool_calls` key missing where required | 1 | 12.5% |
| Wrong-tool selection | Tool call is present but the emitted tool name differs from the expected one | 1 | 12.5% |
| Argument drift / partial payload | Tool call is present but arguments are missing or incomplete | 1 | 12.5% |
| No-call restraint failure | A tool call is emitted where no-call was expected | 1 | 12.5% |

## B. Regime Distribution Assessment

### Measured Findings

- The authoritative missing-evidence cohort contains `134` rows.
- The split distribution is `94` heldout_validation rows and `40` tool_holdout rows.
- The dominant regime is prompt/task echo with transcript contamination: `116/134` rows.
- The remaining missing-evidence rows are partitioned into four smaller contamination regimes and two singleton regimes.
- The C4/C5/C6 sample contains `8` records, and each of the eight output-shape regimes above appears once.
- The three ambiguous rows are all heldout_validation rows and all belong to the answer-prefix plus transcript contamination regime.

### Tool-Family Distribution

- The dominant contamination regime spans many tool families, not one narrow tool family.
- Within that dominant regime, the largest tool families are `rg_search` (`35`) and `read_file` (`21`).
- The minority contamination motifs are split-specific and often tool-family concentrated:
  - answer-prefix plus transcript contamination: `rg_search` only (`3`)
  - instructional assertion plus transcript contamination: `rg_search` only (`4`)
  - pure transcript contamination: `read_file` (`5`) and `rg_search` (`4`)
  - task/prompt echo without transcript contamination: `json_edit` only (`1`)
  - tool-label repetition: `read_file` only (`1`)

### Inferred Findings

- Split is a secondary correlate. All `40` tool_holdout rows fall inside the dominant prompt/task-echo regime, while the minority contamination motifs appear only in heldout_validation.
- Output shape is highly explanatory inside the C4/C5/C6 sample, because each sampled record cleanly lands in one output-shape regime.
- Contamination motif is the strongest overall regime-level descriptor because it exactly partitions the 134-row missing-evidence cohort.

### Unresolved Findings

- Whether split is causal or only correlated with the dominant regime.
- Whether tool family contributes causally or only reflects prompt composition.
- Whether any clean positive population exists outside the observed frozen artifacts.

## C. Explanatory Power Assessment

| Observed variable | Predictive value | Evidence basis |
|---|---|---|
| Split | Moderate | All `40` tool_holdout rows are in the dominant regime, but the minority regimes are heldout_validation-only |
| Tool family | Weak | The dominant regime spans many tool families, and the same tool family can appear in multiple regimes |
| Output shape | High locally | The C4/C5/C6 sample separates clean completion, omission, malformed payload, wrong tool, wrong args, wrapper drift, and no-call failure |
| Contamination motif | Strongest overall | The 134-row missing-evidence cohort is partitioned exactly by contamination motif |
| None of the above | Not supported | The observed regimes are explainable by the variables above, with contamination motif the best overall explanation |

Overall conclusion on explanatory power:

- The most predictive variable is contamination motif.
- Output shape is the strongest mechanism-level descriptor in the smaller C4/C5/C6 sample, but it does not replace contamination motif as the cohort-level explanation.
- Split is a secondary correlate.
- Tool family is the weakest of the listed variables.

## D. Ambiguous Cohort Assessment

The three ambiguous rows are:

| Row ID | Split | Expected tool family | Legacy subtype | Observed regime | Notes |
|---|---|---|---|---|---|
| `heldout_validation:10` | heldout_validation | `rg_search` | `direct_answer_substitution` | answer-prefix plus transcript contamination | Starts with answer-like text and then mixes transcript markers |
| `heldout_validation:28` | heldout_validation | `rg_search` | `direct_answer_substitution` | answer-prefix plus transcript contamination | Same boundary pattern as row 10 |
| `heldout_validation:77` | heldout_validation | `rg_search` | `direct_answer_substitution` | answer-prefix plus transcript contamination | Same boundary pattern as rows 10 and 28 |

Assessment:

- The ambiguous cohort is not a clean direct-answer or scalar population.
- All three rows are mixed with transcript contamination.
- All three rows align with the same answer-prefix plus transcript contamination category.
- All three rows are heldout_validation-only.
- In the current evidence set, they are boundary cases of the dominant contamination regime, not a distinct clean regime.

## E. Stage C-R1A Conclusions

### What runtime regimes exist?

- Prompt/task echo with transcript contamination
- Pure transcript contamination
- Instructional assertion plus transcript contamination
- Answer-prefix plus transcript contamination
- Task/prompt echo without transcript contamination
- Tool-label repetition
- Exact-valid tool-call completion
- Clean no-call emission
- Malformed payload / parse failure
- Wrapper / envelope drift
- Missing tool call
- Wrong-tool selection
- Argument drift / partial payload
- No-call restraint failure

### Which regime dominates?

- Prompt/task echo with transcript contamination dominates the frozen evidence set.
- It accounts for `116/134` missing-evidence rows, or `86.6%` of that cohort.

### What evidence supports that conclusion?

- The runtime-output forensics assessment classifies all `134` missing-evidence rows and shows `0` clean direct-answer-only rows and `0` clean scalar-only rows.
- The repeated-run blocker-persistence assessment shows the same missing-evidence row set and blocker shape across runs.
- The technical spike shows `0` direct-answer delta, `0` scalar delta, and `0` missing-evidence delta across repeated runs.
- The legacy-surface validity assessment shows that the legacy direct-answer count is dominated by contamination-heavy invalid outputs, not a hidden clean positive class.
- The 40 tool_holdout rows all fall inside the dominant prompt/task-echo regime.

### What remains unknown?

- Whether split, tool family, or prompt structure is the causal driver of the regime rather than a correlate.
- Whether the ambiguous cohort has any further internal structure beyond the current answer-prefix contamination label.
- Whether any clean positive population exists outside the observed frozen artifacts.

## Existing Evidence Assessment

### Runtime-Output Forensics Family

- Evidence provided: `134` missing-evidence rows remain missing; `131` are structurally incapable and `3` are ambiguous; the missing cohort never reaches the live tool-intent predicate or the bounded scalar predicate.
- Stage C question it helps answer: What runtime behavior dominates the frozen corpus outputs, and is there any clean governed positive population hiding in the missing-evidence cohort?
- Direct or indirect: Direct.
- Trustworthy and relevant: Yes. The artifact is read-only, stable across repeated runs, and backed by explicit row identities and digests.

### Legacy-Surface Validity Family

- Evidence provided: The legacy `direct_answer_substitution_count` surface counts `125` rows, but those rows overlap `100%` with authoritative missing-evidence rows and are dominated by prompt/task echo with transcript contamination.
- Stage C question it helps answer: Is the legacy direct-answer surface a faithful semantic measure?
- Direct or indirect: Direct.
- Trustworthy and relevant: Yes, as a characterization of the legacy surface itself. No, as a semantic measure of clean direct-answer behavior.

### Technical Spike Family

- Evidence provided: The bounded scorer-pathway change produced `0` direct-answer delta, `0` scalar-substitution delta, and `0` missing-evidence delta across repeated runs.
- Stage C question it helps answer: Would a minimal governance-safe scorer-pathway change surface new authoritative evidence on the frozen corpus?
- Direct or indirect: Direct.
- Trustworthy and relevant: Yes. The repeated-run bundles are stable, preserve row identities, and leave guardrails unchanged.

### Blocker-Persistence Family

- Evidence provided: The repeated full runs are identical in blocker inventory, row identity, missing-evidence rows, and direct-answer row IDs; the surface is reproducible, not noisy.
- Stage C question it helps answer: Is the blocker real and stable enough to justify further observational work?
- Direct or indirect: Direct.
- Trustworthy and relevant: Yes. This is among the strongest evidence families in the repo.

### C4-C6 Evaluator And Scoring Chain

- Evidence provided: parse failures, embedded-object failures, missing tool-call keys, partial arguments, wrong tool names, wrapper leakage, and no-call mismatches are all explicitly represented.
- Stage C question it helps answer: What kinds of runtime-output failures exist before any detector migration or scorer redesign?
- Direct or indirect: Direct, but on a smaller sample than the full missing-evidence cohort.
- Trustworthy and relevant: Yes for behavioral types and guardrail preservation; limited for population-level claims because the sample is small.

### C3 Baseline And C8-C10 Boundary Family

- Evidence provided: the repo preserves state-axis separation, explicit guardrails, and a non-authoritative projection path that remains migration-disabled.
- Stage C question it helps answer: Are the runtime observations being confused with detector migration or threshold migration?
- Direct or indirect: Mostly indirect for runtime behavior; direct for boundary and preservation posture.
- Trustworthy and relevant: Yes, but this family is about safe boundaries, not about runtime-regime discovery.

### Launch And Continuity Documents

- Evidence provided: these documents establish the investigation family, current project posture, and the decision to re-center on runtime-output and corpus behavior.
- Stage C question it helps answer: What is the authorized investigative frame?
- Direct or indirect: Indirect.
- Trustworthy and relevant: Yes for scope and context; not evidence about runtime behavior itself.

## Runtime-Regime Characterization Readiness Assessment

| Question area | Existing evidence | Readiness | Notes |
|---|---|---|---|
| Tool overcalling | Small-sample evidence exists: `A-NI-004b` / `score-008` emitted a tool call where no-call was expected | Partial | We have direct examples, but no corpus-wide rate or split-specific causal explanation |
| Tool undercalling | Small-sample evidence exists: `A-C-006` / `score-003` omitted a required tool call | Partial | Direct evidence exists, but the regime is not yet quantified across all splits and families |
| Direct-answer persistence | Strong negative evidence: no clean direct-answer rows were observed; only `3` mixed answer-prefix rows remain | Partial, leaning strong for non-persistence | The evidence supports absence of clean direct-answer persistence, not presence of a clean regime |
| Wrapper persistence | One wrapper/prose leakage case appears in the 8-record sample; the larger missing-evidence cohort is mostly echo/contamination rather than wrapper-driven | Partial | Wrapper leakage is real but not yet shown to be the dominant regime |
| Schema drift | Strong evidence: invalid JSON, embedded objects, missing keys, and payload-not-parsed states are repeatedly observed | Strong | This is one of the clearest observed failure modes |
| Argument drift | Direct evidence: partial payloads, missing arguments, and wrong tool names appear in the scoring chain | Moderate | Enough to establish the behavior exists; not enough to map its full corpus distribution |
| Evaluator/runtime divergence | Strong evidence: authoritative missing-evidence vs legacy direct-answer counts diverge sharply and repeatably | Strong | The divergence is stable, reproducible, and not explained by a hidden clean positive population |
| Restraint failures | Direct evidence exists in no-call mismatches and unexpected tool emissions in no-call rows | Partial | Present, but not yet fully characterized as a runtime regime |
| Runtime behavioral clustering | Strong evidence: `116/134` missing-evidence rows are task/prompt echo with transcript contamination; split notes show all `tool_holdout` rows inside the dominant category | Strong | This is the clearest behavioral cluster currently available |

## Gap Analysis

### A. Evidence Already Available

- Stable negative evidence that the frozen corpus does not surface a clean governed direct-answer or scalar population.
- Stable repeated-run evidence that the blocker shape and row identities do not change across runs.
- Strong evidence that the legacy direct-answer surface is semantically misaligned with the authoritative missing-evidence cohort.
- Strong evidence that runtime outputs cluster around prompt/task echo with transcript contamination.
- Direct examples of parse failure, tool-call omission, partial payloads, wrong tool names, wrapper leakage, and no-call mismatches.

### B. Evidence Partially Available

- Tool overcalling and tool undercalling are directly observed, but only in small sample sets.
- Wrapper persistence is directly observed, but only weakly relative to the dominant contamination regime.
- Argument drift is directly observed, but not yet mapped across the full missing-evidence cohort.
- Restraint failures are visible, but not yet summarized into a corpus-level behavioral taxonomy.
- Evaluator/runtime divergence is obvious, but the causal story is still mostly interpretive rather than mechanistic.

### C. Evidence Completely Missing

- A causal explanation for why the dominant contamination regime appears so stable.
- A corpus-level comparison that can say whether the contamination regime is split-driven, family-driven, or just globally uniform.
- A stronger explanation for the `3` ambiguous rows beyond “answer-prefix plus transcript contamination.”
- Any direct positive evidence of a clean governed direct-answer or scalar subpopulation on the frozen corpus.
- Evidence that evaluator-artifact visibility, rather than runtime-output behavior, is the primary bottleneck.

## Recommended Next Action

Execute the smallest read-only Stage C runtime-output regime characterization step that adds the most information:

1. Reuse the existing frozen artifacts only.
2. Stratify the `134` missing-evidence rows and the `3` ambiguous rows by split, output shape, and contamination motif.
3. Compare `heldout_validation` against `tool_holdout` at the cluster level.
4. Treat the current technical-spike bundles and runtime-forensics artifacts as the evidence base.
5. Do not change scorer, evaluator, detector, threshold, or migration behavior.

Why this is the smallest high-value step:

- It is strictly observational.
- It targets the remaining uncertainty that the current evidence does not resolve: whether the dominant regime is uniform or split-sensitive.
- It maximizes information gain without reopening governance or migration work.

In repository terms, this is the next `Stage C Runtime-Output Regime Characterization Assessment`, but the smallest useful version is a split-stratified read-only analysis of the existing frozen artifacts, not any new runtime execution or code path change.
