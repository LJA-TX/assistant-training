# Stage C Transition From Evidence Extraction To Evidence Creation Assessment

## Executive Summary

This is a strictly observational transition assessment of the frozen Stage C evidence set. No code was modified, no runtime evaluations were run, and no datasets, detectors, scorers, thresholds, governance controls, migration status, or training artifacts were changed.

The practical answer is:

- **Yes, Stage C has reached the practical limit of evidence extraction from the existing frozen artifacts.**
- The remaining uncertainty is structural, not analytical: the exact rendered prompts for the affected rows are not present in the frozen record.
- Additional retrospective reports over the same artifact set are now low-yield.
- The smallest high-value next step is a **render-only prompt trace** on one representative affected row and one clean control row, with exact prompt text and render-path metadata captured as new evidence.

This document does not propose remediation or retraining. It only marks the transition from observing existing artifacts to creating the missing evidence.

## A. Evidence Extraction Closure Assessment

### What has been conclusively answered?

| Question | Status | Evidence basis |
|---|---|---|
| What runtime regime dominates the frozen Stage C missing-evidence cohort? | Answered | `prompt/task echo with transcript contamination` dominates at `116/134` rows. See [STAGE_C_R1A_RUNTIME_REGIME_CHARACTERIZATION_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_R1A_RUNTIME_REGIME_CHARACTERIZATION_ASSESSMENT.md#L12) |
| What contamination markers are present? | Answered | Role markers, echoed task text, echoed system instruction, answer-like prefixes, tool-label repetition, and wrapper/prose leakage are all observed. See [STAGE_C_R1B_CONTAMINATION_ORIGIN_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_R1B_CONTAMINATION_ORIGIN_ASSESSMENT.md#L9) |
| What is the prompt construction path used by the evaluator? | Answered at pipeline level | The evaluator builds a chat prompt from `system` + `user` messages and decodes continuation only. See [scripts/eval_canonical_manifest.py](/opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py#L807) and [scripts/eval_canonical_manifest.py](/opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py#L924) |
| Can the exact rendered prompts for the affected rows be recovered from the frozen Stage C record? | Answered: no | Stage C R1D concludes they are not recoverable from the existing Stage C evidence. See [STAGE_C_R1D_RENDERED_PROMPT_RECOVERABILITY_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_R1D_RENDERED_PROMPT_RECOVERABILITY_ASSESSMENT.md#L9) |
| Is the causal picture single-source or mixed-source? | Answered | The best-supported reading is mixed-source, with prompt/harness construction and model continuation bias as the best-evidenced proximal contributors. See [STAGE_C_R1C_PROMPT_CONSTRUCTION_AND_CAUSALITY_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_R1C_PROMPT_CONSTRUCTION_AND_CAUSALITY_ASSESSMENT.md#L7) |
| Are there clean governed direct-answer or scalar positives in the authoritative missing-evidence cohort? | Answered | No authoritative clean positives were observed. See [STAGE_C_R1A_RUNTIME_REGIME_CHARACTERIZATION_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_R1A_RUNTIME_REGIME_CHARACTERIZATION_ASSESSMENT.md#L18) |
| Are the three ambiguous rows a separate clean class? | Answered | They are boundary cases of the dominant contamination regime. See [STAGE_C_R1A_RUNTIME_REGIME_CHARACTERIZATION_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_R1A_RUNTIME_REGIME_CHARACTERIZATION_ASSESSMENT.md#L14) |

### What do we already know?

- The dominant observable regime is established and stable. See [STAGE_C_R1A_RUNTIME_REGIME_CHARACTERIZATION_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_R1A_RUNTIME_REGIME_CHARACTERIZATION_ASSESSMENT.md#L12).
- The contamination-marker inventory is established and mixed-source. See [STAGE_C_R1B_CONTAMINATION_ORIGIN_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_R1B_CONTAMINATION_ORIGIN_ASSESSMENT.md#L7).
- The evaluator’s prompt construction path is established at the algorithm level, not the row-specific render level. See [scripts/eval_canonical_manifest.py](/opt/ai-stack/assistant-training/scripts/eval_canonical_manifest.py#L801).
- The exact rendered prompt for the affected rows is absent from the frozen record. See [STAGE_C_R1D_RENDERED_PROMPT_RECOVERABILITY_ASSESSMENT.md](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_R1D_RENDERED_PROMPT_RECOVERABILITY_ASSESSMENT.md#L105).

### What do we think we know?

- The observed outputs are best explained as a combination of prompt/harness construction effects, corpus-construction effects, and model continuation bias.
- The prompt/harness path is the best evidenced proximal mechanism because the evaluator builds a chat prompt before generation and only the continuation is recorded.
- The exact echoed system instruction is plausibly tied to training-style data, but the frozen artifacts do not isolate where that text entered the final causal chain.

## B. Remaining Uncertainty Inventory

### What remains unresolved?

| Unresolved question | Why it remains unresolved | Blocking factor |
|---|---|---|
| What exact rendered prompt was sent for each affected row? | The frozen Stage C record stores input messages and output continuation, but not the rendered prompt string. | Missing evidence |
| Did the affected rows use tokenizer-native rendering or the `generic_roles_v1` fallback? | The row-level render-path choice is not recorded in Stage C artifacts. | Missing evidence |
| What exact tokenizer chat template text was used for the frozen model revision? | The repository preserves the manifest and code path, but not the exact tokenizer template artifact for the relevant runtime instance. | Missing evidence |
| Did the prompt already contain the echoed markers, or were they generated during continuation? | That requires the exact rendered prompt to compare against `generated_text`. | Missing evidence |
| Was the echoed instruction introduced by corpus construction, prompt serialization, or model memorization/continuation? | The current record lacks the exact prompt trace and upstream provenance step. | Missing evidence |
| How much of the observed regime is attributable to corpus-construction effects versus prompt/harness effects versus model continuation bias? | The current evidence supports a mixed causal account, but not a quantitative decomposition. | Missing evidence |
| Are split and tool family causal, or merely correlated with regime membership? | The existing reports establish correlation and concentration, not causation. | Insufficient intervention evidence |

### Which unresolved questions are blocked by missing evidence?

- Exact rendered prompt text for affected rows.
- Per-row native-vs-fallback render-path choice.
- Exact tokenizer template text for the frozen revision.
- Exact provenance of the echoed instruction in the causal chain.
- Quantitative weighting among corpus, prompt/harness, and continuation effects.

### Which unresolved questions are blocked by insufficient evidence-generation, not insufficient analysis?

- Whether split is causal or just correlated.
- Whether tool family is causal or just correlated.
- Whether the observed causal mixture changes under a prompt-render trace versus the frozen continuation-only record.

## C. Evidence Creation Opportunity Assessment

### Has additional observational reporting reached diminishing returns?

Yes, for the frozen Stage C artifact set.

Reason:

- The main open question is now an absent artifact, not an unexamined interpretation.
- R1D already establishes that the exact rendered prompts are not recoverable from the existing Stage C evidence.
- More retrospective reports over the same frozen corpus can rephrase the same limits, but they cannot create the missing prompt trace.

### What is the smallest high-value evidence-creation opportunity?

The smallest useful experiment is:

1. render the prompt for **one representative affected row** from the dominant cohort
2. render the prompt for **one clean control row**
3. stop before generation, scoring, detector execution, or any threshold/migration logic
4. record the exact rendered prompt text and render-path metadata as a new artifact

### Why this is the smallest high-value experiment

- One affected row is enough to recover a missing prompt trace for a representative exemplar of the dominant regime.
- One control row is enough to provide a discriminating contrast for whether the prompt renderer itself is producing the relevant markers or whether those markers are unique to the affected cohort.
- Avoiding generation keeps the experiment in evidence-creation mode, not evaluation mode.

### What evidence would that experiment generate?

| Evidence produced | What it would show |
|---|---|
| Exact rendered prompt string | Whether the prompt already contains the markers that appear in `generated_text` |
| Prompt prefix tail | Whether `[SYSTEM]`, `[USER]`, and `[ASSISTANT]` appear in the rendered prompt for the affected row |
| Render-path flag | Whether tokenizer-native rendering or fallback rendering was used |
| Template identity | Whether `generic_roles_v1` or another template path was used |
| Prompt hash / snapshot ID | A stable reference for later comparison and audit |
| Side-by-side control prompt | Whether the affected row differs from a clean control at the prompt level or only at the continuation level |

## D. Smallest High-Value Experiment Recommendation

### Recommended experiment

Run a **prompt-render-only trace** on:

- one dominant affected row, such as `heldout_validation:2 / p0_rg_search_4`
- one clean control row, such as a direct-answer control from `evals/data/canonical_v1/direct_answer.jsonl`

Capture:

- the full rendered prompt prefix
- the render-path decision
- the template identity
- a stable hash of the rendered prompt

Do **not** run generation, scoring, detectors, or migration logic.

### Why this is the right next evidence step

- It directly targets the exact missing evidence identified in R1C and R1D.
- It is the smallest experiment that can convert the current structural gap into an observable artifact.
- It produces the contrast needed to evaluate whether prompt/harness construction is the proximate source of the markers or whether the markers emerge only after the prompt is rendered and the model continues.

### What major hypotheses that evidence would strengthen or weaken

| If the experiment shows... | It strengthens | It weakens |
|---|---|---|
| The affected-row prompt already contains the echoed instruction and role markers | Prompt/harness construction as a proximate source; mixed-source explanation with a stronger prompt component | Pure continuation-only explanations |
| The affected-row prompt does **not** contain those markers, but `generated_text` still does | Model continuation bias; downstream replay behavior | Prompt/harness construction as the direct source of the markers |
| The affected row uses fallback rendering while the control uses tokenizer-native rendering | Prompt-template and chat-template contributions | Claims that the render path is irrelevant |
| The affected row and control share the same render path, but only the affected row echoes markers in continuation | Corpus-construction or model-memory effects become relatively stronger than renderer-specific effects | A renderer-only explanation |
| The exact echoed instruction appears in the prompt trace exactly as rendered | The prompt/harness path is an actual carrier of the observed text | Any claim that the prompt text was absent and only the model produced the markers |

## E. Stage C Transition Recommendation

Stage C should now transition from **evidence extraction** to **evidence creation**.

### Recommendation

- Treat further retrospective reports over the frozen record as low-value unless they are explicitly preparing the new prompt-trace artifact.
- Move the next effort to the render-only trace experiment described above.
- Use that experiment to create the missing row-level prompt evidence before any further causal refinement.

### Direct transition answer

The project has reached the practical limit of evidence extraction from existing artifacts. The next useful work is not more interpretation of the frozen record; it is creation of the exact prompt evidence that the frozen record lacks.
