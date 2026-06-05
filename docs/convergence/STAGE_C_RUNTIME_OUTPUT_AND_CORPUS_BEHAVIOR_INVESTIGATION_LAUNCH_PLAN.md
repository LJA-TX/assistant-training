# Stage C Runtime-Output And Corpus-Behavior Investigation Launch Plan

## Scope

This document defines the launch plan for the next Stage C investigation family that follows the completed blocker-oriented branch centered on:

- `direct_answer_substitution_count`

This package is planning only.

It does not:

1. launch the investigation family
2. perform runtime-output analysis
3. perform corpus analysis
4. create implementation work
5. create migration work
6. create governance changes
7. reopen completed blocker-branch determinations

## Inputs

Primary transition and branch-outcome records:

1. [STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md:1)
2. [STAGE_C_PACKAGE_7K_BRANCH_OUTCOME_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_PACKAGE_7K_BRANCH_OUTCOME_ASSESSMENT.md:1)
3. [STAGE_C_PACKAGE_6B_CONDITIONAL_BLOCKER_ORIENTED_BRANCH_ADOPTION_DETERMINATION.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_PACKAGE_6B_CONDITIONAL_BLOCKER_ORIENTED_BRANCH_ADOPTION_DETERMINATION.md:1)

Primary blocker-branch and runtime-evidence records:

4. [STAGE_C_PACKAGE_5B_DIRECT_ANSWER_SUBSTITUTION_BLOCKER_PERSISTENCE_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_PACKAGE_5B_DIRECT_ANSWER_SUBSTITUTION_BLOCKER_PERSISTENCE_ASSESSMENT.md:1)
5. [STAGE_C_PACKAGE_5C_DIRECT_ANSWER_SUBTYPE_COMPLETENESS_INVESTIGATION.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_PACKAGE_5C_DIRECT_ANSWER_SUBTYPE_COMPLETENESS_INVESTIGATION.md:1)
6. [STAGE_C_PACKAGE_5D_SCORER_COMPLETENESS_VERSUS_GOVERNANCE_PRESERVATION_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_PACKAGE_5D_SCORER_COMPLETENESS_VERSUS_GOVERNANCE_PRESERVATION_ASSESSMENT.md:1)
7. [STAGE_C_PACKAGE_7D_DIRECT_ANSWER_SCORER_PATHWAY_INVESTIGATION.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_PACKAGE_7D_DIRECT_ANSWER_SCORER_PATHWAY_INVESTIGATION.md:1)
8. [STAGE_C_TECHNICAL_SPIKE_DIRECT_ANSWER_SCORER_PATHWAY_EVIDENCE_EMISSION_PROBE.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_TECHNICAL_SPIKE_DIRECT_ANSWER_SCORER_PATHWAY_EVIDENCE_EMISSION_PROBE.md:1)
9. [STAGE_C_RUNTIME_OUTPUT_FORENSICS_DIRECT_ANSWER_MISSING_EVIDENCE_INVESTIGATION.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_RUNTIME_OUTPUT_FORENSICS_DIRECT_ANSWER_MISSING_EVIDENCE_INVESTIGATION.md:1)
10. [STAGE_C_LEGACY_SURFACE_VALIDITY_ASSESSMENT_DIRECT_ANSWER_SUBSTITUTION.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_LEGACY_SURFACE_VALIDITY_ASSESSMENT_DIRECT_ANSWER_SUBSTITUTION.md:1)

Project charter input:

11. [goal_charter_v5a.md](/opt/ai-stack/assistant-training/docs/goal_charter_v5a.md:1)

## 1. Investigation Family Definition

### Investigation-Family Name

Stage C Runtime-Output And Corpus-Behavior Investigation

### Purpose

Determine how the frozen canonical corpus and the model's emitted runtime outputs interact to produce the current contamination-heavy, non-observable direct-answer surface behavior.

### Scope

This family focuses on:

1. runtime-output regime characterization
2. transcript contamination patterns
3. corpus-induced output behavior
4. observability limits for governed substitution evidence
5. split-level and cohort-level behavior differences
6. evaluator-artifact visibility limits as observed through emitted artifacts

This family does not focus on:

1. extending blocker-branch governance ladders
2. scorer-pathway authorization work
3. detector or threshold migration work
4. migration-gate advancement

### Relationship To The Completed Blocker Branch

This is a new investigation family rather than a continuation of the blocker branch because the blocker branch answered a different class of question:

1. whether the direct-answer blocker was legitimate, stable, bounded, and transitionable
2. whether a safe scorer-pathway probe could surface authoritative evidence
3. whether the legacy and authoritative disagreement could be localized and explained

The remaining uncertainty is now different in kind:

1. what the model actually emits on the frozen corpus
2. how corpus composition contributes to those emissions
3. whether observable governed substitution evidence exists anywhere in the output regime

That is a runtime-output and corpus-behavior question, not a blocker-branch governance question.

## 2. Core Research Questions

The next family should treat the following questions as primary:

1. What runtime-output regime dominates the authoritative missing-evidence population?
2. What specific output patterns create prompt/task echo with transcript contamination?
3. Do those patterns cluster by split, row family, or corpus subset?
4. Is the authoritative evidence target absent from runtime outputs, or present only in mixed and unusable form?
5. How much of the current behavior appears corpus-induced rather than scorer-induced?
6. Are there small observable sub-cohorts that differ materially from the dominant contamination regime?
7. What are the practical observability limits of the current evaluator and scorer artifacts given the frozen corpus outputs?

## 3. Launch Hypothesis Ledger

This is a starting hypothesis set, not a conclusion set.

| Hypothesis | Rationale | Supporting Evidence | Contradictory Evidence | Expected Observations If True |
|---|---|---|---|---|
| `H1` The dominant blocker is a contamination-heavy runtime-output regime, not an unexercised clean substitution branch. | The technical spike changed scorer-pathway logic without changing runtime outcomes. | Technical spike: direct-answer `0`, scalar `0`, missing-evidence `134`; runtime forensics: `0/134` tool-intent hits; legacy validity: `116/125` prompt/task echo plus transcript contamination. | `3` ambiguous rows still exist and are not fully reducible to the dominant cohort. | Runtime-output analysis will keep finding transcript-echo and prompt/task contamination as the dominant observable behavior. |
| `H2` Corpus composition contributes materially to the contamination regime. | The blocker persists across the frozen corpus, and `tool_holdout` contributes a nontrivial share of structurally incapable rows. | Runtime forensics and closure package identify corpus behavior as a dominant remaining uncertainty; legacy population spans both `heldout_validation` and `tool_holdout`. | No direct corpus-composition causal analysis has yet been performed. | Split-level review will show recurring contamination signatures that cluster by split or scenario type. |
| `H3` The authoritative path is not suppressing a meaningful clean direct-answer or scalar population. | Repeated runs, spike, and forensics found no clean governed evidence population surfacing through the authoritative artifacts. | `5B`, technical spike, runtime forensics, and legacy validity assessment. | A small answer-like sub-cohort may still exist within the `3` ambiguous rows. | Additional artifact review will continue to show missingness driven by output form rather than hidden positive evidence. |
| `H4` Legacy `direct_answer_substitution_count` is mostly an invalid-output contamination proxy, not a faithful semantic measure. | Legacy and authoritative populations overlap heavily, but the observed runtime behaviors do not match the claimed semantics. | Legacy validity: `125/125` overlap with authoritative missing-evidence; `0/125` genuine direct-answer rows observed. | Legacy may still retain limited operational usefulness as a reproducible contamination marker. | Further runtime-output review will reinforce contamination-heavy semantics and weaken faithful direct-answer interpretations. |
| `H5` The highest remaining information gain is in artifact-level output analysis before any renewed scorer-pathway or evaluator-path consideration. | The branch has already exhausted high-value governance and bounded pathway framing. | `7K` and blocker-branch closure both shift priority to runtime-output and corpus behavior. | If a hidden artifact-visibility defect exists, evaluator-artifact review could become more central than currently expected. | Early packages in this family will produce more knowledge by inspecting outputs and corpus groupings than by revisiting pathway authorizations. |

## 4. Candidate Workstreams

Candidate workstreams for this family:

### A. Runtime-Output Regime Analysis

Characterize the dominant emitted-output shapes across the authoritative missing-evidence population, including transcript contamination, prompt echo, task echo, malformed tool-intent, and answer-like fragments.

### B. Corpus Composition Analysis

Assess whether split composition, scenario composition, or prompt/task structure correlates with the observed output regime.

### C. Split-Level Behavior Analysis

Compare `heldout_validation` and `tool_holdout` output behavior to determine whether the contamination regime is uniform or split-sensitive.

### D. Contamination-Pattern Analysis

Identify recurring contamination motifs, including transcript markers, instruction restatement, prompt copying, and mixed answer-prefix behaviors.

### E. Observability Analysis

Determine whether the target evidence is directly observable, indirectly observable, or operationally absent from emitted runtime artifacts on the frozen corpus.

### F. Evaluator-Artifact Analysis

Examine how existing emitted artifacts expose or fail to expose the behaviors of interest without changing evaluator or scorer logic.

No workstream is initiated by this package.

## 5. Evidence Requirements

Evidence that would strengthen the launch hypotheses:

1. repeated runtime-output examples showing stable contamination motifs across the missing-evidence population
2. split-level or cohort-level clustering that ties output behavior to corpus composition
3. artifact evidence showing that answer-like behavior remains mixed, contaminated, or otherwise non-observable under current governed rules
4. direct examples showing why legacy-counted rows fail authoritative observability tests

Evidence that would weaken the launch hypotheses:

1. discovery of a sizable clean output sub-cohort already present in runtime artifacts
2. evidence that contamination motifs are rare rather than dominant
3. evidence that corpus composition has little relationship to output behavior
4. evidence that evaluator-artifact visibility, rather than runtime output, is the main bottleneck

Evidence that would falsify key launch hypotheses:

1. a stable clean direct-answer or scalar population already present in emitted artifacts
2. proof that a hidden artifact or parsing defect, rather than output behavior, is the primary cause of authoritative missingness
3. proof that contamination is incidental and not the dominant explanation for the legacy-authoritative gap

## 6. Success Criteria

Meaningful progress in this family should be defined by knowledge generation rather than metric movement.

Success criteria:

1. the runtime-output regime is described with artifact-grounded categories rather than assumptions
2. the role of corpus composition is either strengthened, weakened, or bounded by direct evidence
3. the observability limits of the current emitted artifacts are made explicit
4. the repository can distinguish output-regime questions from scorer-pathway questions without conflating them
5. at least one high-value next uncertainty is resolved or sharply narrowed

## 7. Risk Assessment

### Scope-Creep Risk

Risk:

1. runtime-output work expands back into scorer redesign, evaluator redesign, or governance reconsideration

Containment:

1. keep initial packages observational
2. treat pathway changes as out of scope unless a later package explicitly reauthorizes them

### Governance-Regression Risk

Risk:

1. the new family may implicitly reopen blocker-branch determinations

Containment:

1. treat blocker-branch conclusions as fixed inputs unless future authority explicitly reopens them

### Overfitting-To-Artifacts Risk

Risk:

1. narrow reading of a single artifact type could overstate conclusions about the full runtime regime

Containment:

1. cross-check runtime outputs, comparison rows, row facts, and scorer evidence artifacts together

### Methodology Risk

Risk:

1. observational categories could become ad hoc or unstable

Containment:

1. require reproducible category definitions and repeated-run evidence where relevant

## 8. Relationship To The Original Charter

This family is not a direct model-improvement package, but it still serves the charter in [goal_charter_v5a.md](/opt/ai-stack/assistant-training/docs/goal_charter_v5a.md:1).

It moves the repository closer to:

1. evaluator understanding
2. training-regimen understanding
3. post-training methodology extraction

It contributes to model improvement indirectly by clarifying:

1. what runtime behavior the current corpus is eliciting
2. whether the corpus is reinforcing contamination-heavy invalid-output patterns
3. whether future post-training work should target corpus composition, evaluation framing, or another locus

Relative alignment:

1. strongest alignment: evaluator understanding and post-training methodology extraction
2. medium alignment: training-regimen understanding
3. indirect alignment: eventual model improvement

## 9. Recommended Initial Work Package

Recommended first package:

- Stage C Runtime-Output Regime Characterization Assessment

### Why This First

This is the single highest-information-gain first step because:

1. runtime forensics already showed that the dominant uncertainty is the emitted output regime
2. the technical spike weakened the case for immediate further scorer-pathway work on the frozen corpus
3. legacy validity analysis showed the semantic gap is driven by what the outputs actually are, not just by how they are named
4. output-regime characterization creates the best foundation for any later corpus, evaluator, or scorer investigation

The recommended first package should remain observational and should not perform implementation.

## 10. Transition Readiness Assessment

### Is The Repository Ready To Begin This Family

Yes.

### Prerequisites Already Present

1. blocker-branch closure and transition record
2. stable repeated-run evidence
3. runtime technical-spike evidence
4. runtime-output forensic method
5. legacy-surface validity method
6. explicit continuity requirements from the closure package

### Prerequisites Still Missing

No blocking prerequisite is missing for launch-plan purposes.

Future work will still need:

1. package-level scoping for the first observational slice
2. explicit artifact-selection boundaries for the first runtime-output package

## Final Determination

The single highest-information-gain first step for this family is:

- artifact-grounded runtime-output regime characterization of the authoritative missing-evidence population

Repository evidence supports that choice because:

1. the blocker branch already resolved the governance and bounded-pathway questions
2. the technical spike showed that the smallest safe scorer-pathway change does not move runtime outcomes
3. runtime forensics showed that the dominant remaining uncertainty is output behavior, not hidden authoritative evidence
4. legacy validity analysis showed that the observed disagreement is driven by what the model emits, not just by surface naming differences

This launch plan does not begin that work.

It establishes the scope, hypotheses, workstreams, evidence requirements, and first-step recommendation for the next investigation family.
