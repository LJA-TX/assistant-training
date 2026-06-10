# Stage C R1B Contamination Origin Assessment

## Executive Summary

This is a strictly observational, read-only assessment of the frozen Stage C evidence set. No code was modified, no runtime evaluations were run, and no datasets, detectors, scorers, thresholds, governance controls, migration status, or training artifacts were changed.

The marker evidence supports a mixed-source contamination explanation, not a single-source one.

The strongest observed markers are:

- literal transcript delimiters and role markers: `[SYSTEM]`, `[USER]`
- echoed task/prompt text
- echoed system-instruction text
- small boundary variants such as answer-like prefixes and tool-label repetition

The most likely upstream mechanism is corpus-construction contamination over a chat-templated prompt scaffold, with prompt-template and chat-template contamination as the dominant components. Source-data contamination likely contributes to the task/prompt echoes. Evaluation-artifact contamination is possible for a minority of meta-instruction-like rows, but it is not the best explanation for the dominant regime.

Confidence:

- High that the contamination is mixed-source rather than single-source
- High that chat-template contamination is present
- High that prompt-template contamination is present
- Moderate that corpus-construction contamination is the primary upstream mechanism
- Moderate that source-data contamination contributes
- Low that evaluation-artifact contamination is the primary source

## Evidence Base

Accepted Stage C artifacts used here:

- [STAGE_C_RECONNAISSANCE_AND_EVIDENCE_INVENTORY.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_RECONNAISSANCE_AND_EVIDENCE_INVENTORY.md)
- [STAGE_C_R1A_RUNTIME_REGIME_CHARACTERIZATION_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_R1A_RUNTIME_REGIME_CHARACTERIZATION_ASSESSMENT.md)
- [STAGE_C_RUNTIME_OUTPUT_FORENSICS_DIRECT_ANSWER_MISSING_EVIDENCE_INVESTIGATION.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_RUNTIME_OUTPUT_FORENSICS_DIRECT_ANSWER_MISSING_EVIDENCE_INVESTIGATION.md)
- [STAGE_C_LEGACY_SURFACE_VALIDITY_ASSESSMENT_DIRECT_ANSWER_SUBSTITUTION.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_LEGACY_SURFACE_VALIDITY_ASSESSMENT_DIRECT_ANSWER_SUBSTITUTION.md)
- [STAGE_C_PACKAGE_5C_DIRECT_ANSWER_SUBTYPE_COMPLETENESS_INVESTIGATION.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_PACKAGE_5C_DIRECT_ANSWER_SUBTYPE_COMPLETENESS_INVESTIGATION.md)
- [STAGE_C_PACKAGE_1A_CANONICAL_ROW_IDENTITY_CONTRACT_CLARIFICATION.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_PACKAGE_1A_CANONICAL_ROW_IDENTITY_CONTRACT_CLARIFICATION.md)
- [stage_c_runtime_output_forensics_direct_answer_missing_evidence_assessment.json](/opt/ai-stack/assistant-training/manifests/reports/stage_c_runtime_output_forensics_direct_answer_missing_evidence_assessment.json)
- [stage_c_legacy_surface_validity_direct_answer_assessment.json](/opt/ai-stack/assistant-training/manifests/reports/stage_c_legacy_surface_validity_direct_answer_assessment.json)
- [stage_c_technical_spike_direct_answer_assessment.json](/opt/ai-stack/assistant-training/manifests/reports/stage_c_technical_spike_direct_answer_assessment.json)
- [stage_c_package5b_direct_answer_blocker_persistence_assessment.json](/opt/ai-stack/assistant-training/manifests/reports/stage_c_package5b_direct_answer_blocker_persistence_assessment.json)
- [stage_c4_sample_output_records.jsonl](/opt/ai-stack/assistant-training/reports/stage_c4/input/stage_c4_sample_output_records.jsonl)
- [c4_output_inventory_artifact.json](/opt/ai-stack/assistant-training/reports/stage_c4/contract_artifacts/c4_output_inventory_artifact.json)
- [c4_parse_toolcall_status_artifact.json](/opt/ai-stack/assistant-training/reports/stage_c4/contract_artifacts/c4_parse_toolcall_status_artifact.json)
- [c5_per_output_scoring_status_artifact.json](/opt/ai-stack/assistant-training/reports/stage_c5/contract_artifacts/c5_per_output_scoring_status_artifact.json)
- [c5_parse_tool_nocall_scoring_summary_artifact.json](/opt/ai-stack/assistant-training/reports/stage_c5/contract_artifacts/c5_parse_tool_nocall_scoring_summary_artifact.json)
- [c5_wrapper_leakage_scoring_summary_artifact.json](/opt/ai-stack/assistant-training/reports/stage_c5/contract_artifacts/c5_wrapper_leakage_scoring_summary_artifact.json)
- [c5_validation_issues_artifact.json](/opt/ai-stack/assistant-training/reports/stage_c5/contract_artifacts/c5_validation_issues_artifact.json)
- [c6_runtime_scoring_summary_artifact.json](/opt/ai-stack/assistant-training/reports/stage_c6/reporting_artifacts/c6_runtime_scoring_summary_artifact.json)
- [c6_parse_tool_nocall_summary_artifact.json](/opt/ai-stack/assistant-training/reports/stage_c6/reporting_artifacts/c6_parse_tool_nocall_summary_artifact.json)
- [c6_wrapper_leakage_summary_artifact.json](/opt/ai-stack/assistant-training/reports/stage_c6/reporting_artifacts/c6_wrapper_leakage_summary_artifact.json)
- [c6_validation_issue_summary_artifact.json](/opt/ai-stack/assistant-training/reports/stage_c6/reporting_artifacts/c6_validation_issue_summary_artifact.json)

## A. Contamination Marker Inventory

The inventory below records observable markers only. Upstream source attribution is handled later as an inference.

| Marker family | Observed markers / motifs | Representative evidence | Prevalence estimate | Origin clue |
|---|---|---|---:|---|
| Transcript framing / role markers | `[SYSTEM]`, `[USER]` | Runtime-forensics examples in the prompt/task echo, transcript-only, answer-prefix, and instructional-assertion categories | `132/134` missing-evidence rows carry transcript markers | Strong chat-template signal |
| Prompt/task echo | Echoed task text such as file paths, `rg_search` requests, `Read ...`, `Find ...`, `Show ...`, `Retrieve ...`, `Use json_edit ...` | Dominant `task/prompt echo with transcript contamination` category plus the singleton `task/prompt echo without transcript contamination` | `116/134` dominant rows, plus adjacent echo variants | Strong prompt-template or source-data signal |
| Echoed system instruction | Repeated shared tool-use directive; the same instruction text is echoed after transcript markers in many examples | Appears across the transcript-contaminated categories in the runtime-forensics examples | No separate row-count is reported, but it is pervasive across the contaminated families | Strong prompt-template signal |
| Instructional assertion | Meta-instructions such as `Tool validation is not required for this task.` and `Tool parse mode is enabled.` | `heldout_validation:44`, `heldout_validation:65`, `heldout_validation:83`, `heldout_validation:88` | `4/134` | Possible prompt-template or evaluation-artifact signal |
| Answer-like prefix | `The first function name is: main` | `heldout_validation:10`, `heldout_validation:28`, `heldout_validation:77` | `3/134` | Mixed source-data / prompt-echo signal |
| Tool-label repetition | `Tool: python` repeated many times | `heldout_validation:11` | `1/134` | Possible source-data or corpus-construction artifact |
| Wrapper / prose leakage | `I will call the tool now. ... trailing prose`, `Wrapper prefix ... wrapper suffix` | C4 `out-002`; C5/C6 `score-006` | `1/6` in C4, `1/8` in C5/C6 | Output-formatting / corpus-construction signal |

Observed cohort shape from the runtime-forensics report:

- `131/134` rows are structurally incapable under the current doctrine.
- `3/134` rows are ambiguous, but they still use the same transcript-contaminated scaffold.
- `0/134` rows are clean governed direct-answer rows.
- `0/134` rows are clean scalar-substitution rows.

## B. Contamination Family Taxonomy

The families below are primary signal families, not mutually exclusive physical causes.

| Family | Defining markers | Estimated prevalence | Notes |
|---|---|---:|---|
| Chat-frame family | Literal transcript delimiters and role markers | `132/134` rows with transcript markers | Strongest non-content marker; points to chat-templated serialization |
| Prompt-echo family | Repeated task text and repeated tool-request phrasing | Dominant `116/134` regime, plus smaller echo variants | Best fit for a shared prompt scaffold or source-data replay |
| Meta-instruction family | Tool-policy-like assertions and parse/validation commentary | `4/134` | Looks like template or evaluation scaffolding, but not enough to dominate the cohort |
| Answer-prefix family | Answer-like lead-ins before transcript markers | `3/134` | Boundary case; not a clean direct-answer class |
| Tool-label family | Repeated tool labels instead of a valid payload | `1/134` | Isolated anomaly |
| Wrapper/prose family | Prose before or after a tool JSON fragment | `2` operational records across C4/C5/C6 samples | Directly observed in the operational sample, not in the authoritative missing-evidence cohort |

Interpretive note:

- The dominant cohort is not a single clean family.
- The observed markers stack on top of each other: prompt echoes, transcript delimiters, and shared instruction text recur together.
- That stack is the main reason a mixed-source explanation fits better than any single-source explanation.

## C. Contamination-Origin Assessment

The table below evaluates the candidate origin classes requested by the task.

| Origin hypothesis | Evidence for | Evidence against / limits | Assessment | Confidence |
|---|---|---|---|---|
| Source-data contamination | User-task text is echoed back into outputs; answer-like prefixes exist; the cohort is not a clean protocol artifact | The accepted Stage C artifacts do not expose the raw upstream source corpus directly | Likely contributor, but not sufficient as a single explanation | Moderate |
| Corpus-construction contamination | `source_case_id` is explicitly described as provenance carried through corpus construction; duplicated provenance is expected; the outputs preserve serialized prompt/transcript structure | The artifacts do not directly show the builder step that injected the contamination | Most likely upstream mechanism | Moderate |
| Prompt-template contamination | The same tool-use directive recurs across many examples; the prompt/task echo family dominates the cohort | The artifacts do not directly identify which file or builder inserted the template | Strong component of the origin | High |
| Chat-template contamination | Literal `[SYSTEM]` / `[USER]` markers recur in 132 rows | No meaningful counterevidence in the accepted artifacts | Strong component of the origin | High |
| Evaluation-artifact contamination | Some rows say things like `Tool validation is not required...` and `Tool parse mode is enabled.` | Those phrases are minority signals and do not explain the dominant prompt/task echo regime | Possible minor contributor, not primary | Low |
| Mixed-source contamination | Explains the co-occurrence of prompt echoes, role markers, meta-instructions, answer-like prefixes, and tool-label repetition | None significant | Best overall explanation | High |

### Bottom-line origin statement

The dominant contamination regime most likely comes from a mixed-source corpus-construction layer that serializes chat messages and prompt templates, rather than from a single isolated source.

More specifically:

- chat-template contamination is clearly present
- prompt-template contamination is clearly present
- source-data contamination likely contributes to the echoed task text
- evaluation-artifact contamination is only a secondary possibility for a minority of meta-instruction rows

This is an inference from the observed marker stack. The accepted Stage C artifacts do not directly name the upstream ingestion source.

## D. Ambiguous Cohort Comparison

The three ambiguous rows are:

- `heldout_validation:10`
- `heldout_validation:28`
- `heldout_validation:77`

Comparison against the dominant cohort:

| Row id | Shared markers with dominant cohort | Additional marker | Same contamination family? | Comment |
|---|---|---|---|---|
| `heldout_validation:10` | `[SYSTEM]`, `[USER]`, echoed system instruction, echoed task prompt | `The first function name is: main` | Yes | Boundary case of the dominant regime |
| `heldout_validation:28` | `[SYSTEM]`, `[USER]`, echoed system instruction, echoed task prompt | `The first function name is: main` | Yes | Boundary case of the dominant regime |
| `heldout_validation:77` | `[SYSTEM]`, `[USER]`, echoed system instruction, echoed task prompt | `The first function name is: main` | Yes | Boundary case of the dominant regime |

Assessment:

- The ambiguous rows are contaminated in the same way as the dominant cohort.
- They do not introduce a new origin signal.
- Their only distinctive feature is the answer-like prefix at the start of the output.

Confidence:

- High that they belong to the same contamination family as the dominant cohort
- High that they are boundary cases, not a separate clean source

## E. Confidence Assessment

### Major conclusions

| Conclusion | Confidence | Why |
|---|---|---|
| The contamination is mixed-source, not single-source | High | Multiple marker families co-occur and no single origin class explains them all |
| Chat-template contamination is present | High | Literal role markers recur in 132/134 rows |
| Prompt-template contamination is present | High | The same shared tool-use directive is echoed across the dominant contamination families |
| Corpus-construction contamination is the most likely upstream mechanism | Moderate | `source_case_id` is preserved as corpus provenance and the observed outputs look like serialized prompt/transcript scaffolding |
| Source-data contamination contributes | Moderate | The task text itself is echoed back, including the three answer-prefix rows |
| Evaluation-artifact contamination is not the primary source | Low as a primary explanation | The evaluation-like phrases are real, but they are too sparse to explain the dominant regime |
| The three ambiguous rows are the same contamination family as the dominant cohort | High | They share the same transcript markers and echoed prompt structure, with only an answer-like prefix added |

### What remains unknown

- The accepted Stage C artifacts do not directly reveal the upstream raw ingestion source.
- The evidence therefore cannot distinguish perfectly between source-data contamination and corpus-construction contamination.
- What it can say, with high confidence, is that the dominant regime is a mixed transcript/prompt echo artifact, not a clean single-source direct-answer class.
