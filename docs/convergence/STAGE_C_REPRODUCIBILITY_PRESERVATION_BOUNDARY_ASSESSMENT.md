# Stage C Reproducibility-Preservation Boundary Assessment

## Executive Summary

Under a reproducibility-preservation objective, the Stage C archival boundary should be **expanded** to include the E1 evidence-creation implementation artifacts:

- `scripts/stage_c_e1_prompt_trace_evidence_creation.py`
- `tests/test_stage_c_e1_prompt_trace_evidence_creation.py`

These are not unrelated implementation artifacts. They are the thin evidence-generation infrastructure that produced and guards the E1 prompt-trace bundle.

Recommended archival strategy:

- preserve the Stage C methodology docs as the historical narrative record;
- preserve the E1 prompt-trace bundle as the primary evidence object;
- preserve the E1 creation script and its regression test as the reproducibility mechanism; and
- exclude broader runtime/evaluator helpers and repo-wide publication cleanup artifacts that are not Stage C-specific.

This recommendation does not change any Stage C conclusions, classifications, or doctrine disposition.

## 1. Direct Answers

### 1. Should the E1 implementation artifacts be part of the Stage C historical record?

**Yes, under a reproducibility-preservation objective.**

The E1 script and test are part of the historical record because they preserve the mechanism that generated the evidence bundle, not just the bundle itself.

### 2. Are these evidence-generation infrastructure or unrelated implementation artifacts?

They are **evidence-generation infrastructure**.

Why:

- the script constructs the exact rendered prompt trace bundle;
- the script records render-path metadata, hashes, and validation artifacts;
- the test enforces the non-generation, non-scoring, non-detector boundary; and
- the test proves the exact prompt snapshots match the built prompt prefix.

### 3. What is the recommended archival boundary?

Use a **hybrid reproducibility-preservation boundary**:

- keep the Stage C methodology docs and review/disposition artifacts;
- keep the E1 prompt-trace evidence bundle;
- keep the E1 evidence-creation script and test; and
- exclude broader runtime/evaluator code that is not Stage C-specific.

## 2. Evidence-Generation Infrastructure Assessment

The E1 creator script is tightly scoped to the reproducibility of the prompt-trace bundle:

- it loads the canonical evaluator render path;
- it selects the representative affected row and control row;
- it captures `row.prompt_prefix` after `_build_rows(...)`;
- it stops before `_eval_one_side(...)` and `_infer(...)`;
- it writes the exact prompt snapshots; and
- it validates hashes and render-only execution.

The accompanying test is equally important:

- it asserts the exact prompt snapshots match the built prompt prefix;
- it asserts the run remains render-only;
- it asserts `_infer` and `_eval_one_side` are not called; and
- it checks fallback metadata behavior when the tokenizer chat template is missing.

Together, these artifacts preserve the minimal mechanism needed to regenerate the E1 evidence bundle and verify that the mechanism stayed within the intended boundary.

## 3. Documentation/ Evidence-Only Versus Full Reproducibility Preservation

### Documentation/Evidence-Only Preservation

Advantages:

- smallest archival surface;
- easiest to curate and review;
- least likely to pull in unrelated runtime code;
- keeps the archive focused on conclusions and evidence rather than execution machinery.

Disadvantages:

- loses the explicit mechanism used to create the E1 evidence;
- makes later reproduction less transparent;
- forces future reviewers to infer how the bundle was created from docs alone;
- weakens the preservation of the exact evidence-production boundary.

### Full Reproducibility Preservation

Advantages:

- preserves the exact creation mechanism for the E1 evidence bundle;
- makes the archive more useful for later re-execution or verification;
- strengthens provenance for future regimen extraction work;
- preserves the smallest runnable evidence-creation slice rather than only its outputs.

Disadvantages:

- increases the archive surface;
- can couple the archival boundary to implementation details;
- can tempt the archive to expand into broader runtime/evaluator internals if the boundary is not kept narrow;
- requires careful exclusion of unrelated helper code and repo-wide publication artifacts.

## 4. Coupling Assessment

Including the E1 script and test does create a limited dependency chain on the canonical evaluator render path.

That coupling is **desirable**, because it is the exact path the evidence-creation slice was designed to exercise.

What should not be included:

- the broader evaluator implementation;
- generic repo-path helpers; or
- unrelated runtime, scorer, detector, or publication-cleanup code.

Those broader files are useful repository infrastructure, but they are not part of the Stage C archival boundary needed to preserve the E1 evidence-creation mechanism.

## 5. Recommended Archival Boundary

For a project whose long-term objective is extracting a reusable model-training and evaluation regimen, the recommended boundary is:

1. preserve the methodology narrative;
2. preserve the primary evidence bundle;
3. preserve the thin mechanism that created the evidence; and
4. exclude broad runtime infrastructure that is not specific to the preserved evidence slice.

This is the best balance between:

- traceability,
- reproducibility,
- scope discipline, and
- long-term regimen reuse.

## 6. Exact Include List Under The Recommended Strategy

### Stage C methodology narrative and transition record

- `docs/convergence/STAGE_C_RECONNAISSANCE_AND_EVIDENCE_INVENTORY.md`
- `docs/convergence/STAGE_C_R1A_RUNTIME_REGIME_CHARACTERIZATION_ASSESSMENT.md`
- `docs/convergence/STAGE_C_R1B_CONTAMINATION_ORIGIN_ASSESSMENT.md`
- `docs/convergence/STAGE_C_R1C_PROMPT_CONSTRUCTION_AND_CAUSALITY_ASSESSMENT.md`
- `docs/convergence/STAGE_C_R1D_RENDERED_PROMPT_RECOVERABILITY_ASSESSMENT.md`
- `docs/convergence/STAGE_C_TRANSITION_FROM_EVIDENCE_EXTRACTION_TO_EVIDENCE_CREATION_ASSESSMENT.md`
- `docs/convergence/STAGE_C_E1_PROMPT_TRACE_EVIDENCE_CREATION_PLAN.md`
- `docs/convergence/STAGE_C_E1_PROMPT_TRACE_EVIDENCE_INTERPRETATION.md`
- `docs/convergence/STAGE_C_METHODOLOGY_EXTRACTION_ASSESSMENT.md`
- `docs/convergence/STAGE_C_DOCTRINE_ADOPTION_CANDIDATE_ASSESSMENT.md`
- `docs/convergence/STAGE_C_DOCTRINE_ADOPTION_ADVERSARIAL_REVIEW_Grok-Build.md`
- `docs/convergence/STAGE_C_DOCTRINE_ADOPTION_ADVERSARIAL_REVIEW_GB-Composer.md`
- `docs/convergence/STAGE_C_DOCTRINE_ADOPTION_ADVERSARIAL_REVIEW_Qwen3-Next-Thinking@UD-Q3-K-XL.md`
- `docs/convergence/STAGE_C_DOCTRINE_DISPOSITION_ASSESSMENT_GB-Composer.md`
- `docs/convergence/STAGE_C_METHODOLOGY_BRANCH_CLOSURE_ASSESSMENT.md`
- `docs/convergence/STAGE_C_FINAL_DISPOSITION_AND_PUBLICATION_ASSESSMENT.md`
- `docs/convergence/STAGE_C_PUBLICATION_AND_TRANSITION_PACKAGE.md`
- `docs/convergence/STAGE_C_FINAL_PUSH_READINESS_AND_PUBLICATION_HYGIENE_ASSESSMENT.md`
- `docs/convergence/STAGE_C_REPRODUCIBILITY_PRESERVATION_BOUNDARY_ASSESSMENT.md`

### E1 evidence bundle

- `manifests/reports/stage_c_prompt_trace_evidence/stage_c_e1_prompt_trace_20260609T221315792398Z/manifest.json`
- `manifests/reports/stage_c_prompt_trace_evidence/stage_c_e1_prompt_trace_20260609T221315792398Z/prompt_traces.jsonl`
- `manifests/reports/stage_c_prompt_trace_evidence/stage_c_e1_prompt_trace_20260609T221315792398Z/validation_report.json`
- `manifests/reports/stage_c_prompt_trace_evidence/stage_c_e1_prompt_trace_20260609T221315792398Z/rows/heldout_validation_2_p0_rg_search_4.prompt.txt`
- `manifests/reports/stage_c_prompt_trace_evidence/stage_c_e1_prompt_trace_20260609T221315792398Z/rows/direct_answer_1_da_92001.prompt.txt`

### E1 evidence-generation implementation artifacts

- `scripts/stage_c_e1_prompt_trace_evidence_creation.py`
- `tests/test_stage_c_e1_prompt_trace_evidence_creation.py`

## 7. Exact Exclude List Under The Recommended Strategy

Exclude the following from the Stage C archival boundary:

- `scripts/eval_canonical_manifest.py`
- `scripts/repo_paths.py`
- `tests/test_repo_paths.py`
- `docs/PUBLICATION_READINESS_AUDIT.md`
- `docs/continuity/post-publication_transition_return_to_stage_c_continuity_2026-06-09.md`

Also exclude any other unrelated runtime, scorer, detector, migration, or repo-wide publication cleanup files that are not explicitly named above.

## 8. Final Recommendation

**Expand the Stage C archival boundary to include the E1 evidence-creation implementation artifacts.**

That boundary gives the best long-term preservation value for a project that wants both:

- the historical evidence, and
- the ability to explain or re-create how that evidence was produced.

It preserves reproducibility without collapsing into the full runtime/evaluator codebase.
