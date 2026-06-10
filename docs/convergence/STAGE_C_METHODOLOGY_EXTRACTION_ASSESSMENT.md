# Stage C Methodology Extraction Assessment

## Executive Summary

Stage C has produced a clear methodology-level result: when the central causal question depends on what was rendered into the model prompt, the rendered prompt itself must be treated as first-class evidence.

That conclusion is not a speculative design preference. It is demonstrated by the Stage C sequence:

1. the frozen record preserved inputs and continuations but not the exact rendered prompt;
2. retrospective analysis reached a hard limit because the prompt surface could not be recovered from the frozen artifacts;
3. the E1 render-only trace created the missing evidence without generation, scoring, or detector execution; and
4. the resulting prompt snapshots materially reduced the uncertainty boundary for the representative rows.

The reusable lesson is methodological, not domain-specific:

- exact prompt traces are evidence, not implementation detail;
- continuation text is not a substitute for prompt provenance;
- render-path metadata and hashes are required for later trust;
- a small affected-row/control-row pair is often enough to create discriminating evidence; and
- render-only evidence creation is the correct bridge when retrospective extraction has hit its limit.

Stage C-specific contamination markers do not generalize as content. The observability lesson does.

## Evidence Basis

This assessment is grounded in the completed Stage C record, especially:

- [Stage C transition assessment](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_TRANSITION_FROM_EVIDENCE_EXTRACTION_TO_EVIDENCE_CREATION_ASSESSMENT.md)
- [Stage C R1D prompt recoverability assessment](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_R1D_RENDERED_PROMPT_RECOVERABILITY_ASSESSMENT.md)
- [Stage C E1 prompt trace evidence creation plan](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_E1_PROMPT_TRACE_EVIDENCE_CREATION_PLAN.md)
- [Stage C E1 prompt trace evidence interpretation](/opt/ai-stack/assistant-training/docs/convergence/STAGE_C_E1_PROMPT_TRACE_EVIDENCE_INTERPRETATION.md)
- [E1 trace bundle](/opt/ai-stack/assistant-training/manifests/reports/stage_c_prompt_trace_evidence/stage_c_e1_prompt_trace_20260609T221315792398Z/)

## 1. Methodological Lessons Demonstrated By Evidence

### 1.1 Rendered prompts are evidence, not implementation detail

The strongest methodological result is that exact rendered prompts are necessary evidence whenever prompt construction could plausibly affect observed output behavior.

Why this is demonstrated:

- R1C established that prompt construction was part of the causal question.
- R1D established that the exact rendered prompts were not recoverable from the frozen Stage C record.
- E1 showed that the missing evidence could be created directly from the canonical render path.

This means the prompt surface is not a disposable intermediate. It is part of the observable record.

### 1.2 Continuation-only artifacts are insufficient for prompt provenance

Stage C also demonstrated a negative lesson: `generated_text` alone is not enough to reconstruct or validate the rendered prompt.

That matters because:

- the continuation can carry prompt-like markers;
- the continuation can look like transcript replay or wrapper leakage; and
- without the rendered prompt, those markers cannot be cleanly attributed to prompt content versus model continuation.

The methodological point is general: if the investigation needs to discriminate prompt-origin from continuation-origin behavior, the prompt itself must be archived.

### 1.3 Evidence extraction can hit a real structural ceiling

Stage C showed that retrospective analysis over a frozen record has diminishing returns once the decisive artifact is absent.

That is a process lesson:

- when the missing fact is exact prompt text, more output-side interpretation cannot create it;
- the correct next step is evidence creation, not more inference over the same frozen surface.

### 1.4 Render-only traces are the smallest high-value evidence-creation unit

E1 demonstrated that the smallest useful evidence-creation step was not a full evaluation run.

The useful unit was:

- one representative affected row;
- one clean control row;
- exact prompt rendering;
- no generation;
- no scoring;
- no detector execution; and
- stable metadata and hashes.

This is a broadly reusable methodology pattern whenever the question is about pre-generation surfaces.

### 1.5 Control rows are necessary, not optional

The clean control row in E1 did not add statistical breadth. It added interpretive power.

It established that:

- the canonical render path can produce a clean prompt surface; and
- the affected row’s special markers are row-content dependent, not an artifact of a degenerate universal renderer.

That is a general observability lesson: a representative control row is often enough to tell whether the renderer itself is the source of confusion.

### 1.6 Metadata and hashes are part of the evidence object

The E1 bundle showed that exact prompt text alone is still incomplete evidence unless it is paired with:

- row identity;
- source dataset path;
- dataset hash;
- manifest path;
- manifest hash;
- render-path decision;
- tokenizer/template identity; and
- prompt hash.

This is not auxiliary bookkeeping. It is what makes the prompt snapshot self-authenticating.

## 2. Stage C-Specific Lessons

These lessons are specific to the Stage C contamination investigation and should not be generalized as content:

1. the observed regime involved chat-shaped prompts with explicit role markers;
2. the key ambiguity was whether the markers were already present in the rendered prompt or emerged during continuation;
3. the dominant causal discussion involved corpus-construction effects, prompt/harness effects, and model continuation bias;
4. the investigation depended on a canonical chat-template render path and a fallback template path; and
5. the representative control was a direct-answer row from the same frozen evaluator family.

Those are Stage C-specific facts. The methodological lesson is that any future investigation with analogous ambiguity needs exact prompt recovery, not that it must reuse the same marker taxonomy.

## 3. Generalizable Lessons For Future Evaluation Families

The following lessons generalize beyond Stage C:

### 3.1 If the evaluation path serializes prompts, archive the rendered prompt

Any future evaluation family that:

- constructs a prompt from structured messages,
- uses chat templates,
- appends generation prompts, or
- depends on prompt serialization for model behavior

should preserve the exact rendered prompt as an evidence artifact.

### 3.2 Keep pre-generation and post-generation surfaces separate

Future investigations should preserve both surfaces independently:

- the exact rendered prompt;
- the exact continuation or output.

That separation is what makes causal discrimination possible.

### 3.3 Preserve the render contract, not just the text

The prompt text alone is not enough unless the bundle also preserves:

- template identity;
- render-path choice;
- tokenizer identity; and
- exact hash or fingerprint values.

This generalizes to any family where alternate render paths could exist.

### 3.4 Use immutable trace bundles

Stage C’s prompt trace bundle suggests a reusable bundle shape:

- manifest;
- JSONL trace index;
- raw prompt snapshots;
- validation report.

That bundle shape is likely reusable across future families whenever the investigation is observational rather than generative.

### 3.5 Use a clean control row

Future families should include a representative clean control whenever a prompt-surface question is under investigation.

The control row is what makes the evidence comparative instead of merely descriptive.

## 4. Has Stage C Demonstrated That Rendered Prompts Should Be First-Class Evidence Artifacts?

Yes.

High-confidence reasons:

- the exact rendered prompt was the missing evidence that blocked further causal discrimination;
- retrospective analysis could not recover it from the frozen record;
- E1 created it directly with a render-only trace; and
- the resulting prompt snapshots answered the specific question "what exactly was sent to the model?" for the representative rows.

The Stage C evidence therefore supports a doctrine-level rule for future families:

- if prompt construction could affect interpretation, the rendered prompt is a primary evidence artifact, not a scratchpad intermediate.

## 5. Additional Observability Artifacts That Appear Similarly Important

The Stage C record suggests that the following artifacts are nearly as important as the raw rendered prompt:

| Artifact | Why it matters |
|---|---|
| Raw rendered prompt snapshot | The primary object of prompt-surface evidence |
| Raw continuation or output snapshot | Needed to compare prompt-origin and continuation-origin markers |
| Render-path metadata | Distinguishes canonical, native, and fallback prompt construction |
| Template identity / fingerprint | Makes the prompt trace reproducible and auditable |
| Row identity and source-case binding | Prevents ambiguity about which row was rendered |
| Dataset and manifest hashes | Prove the bundle is tied to frozen inputs |
| Validation report | Shows the bundle is exact, complete, and render-only |
| Clean control prompt snapshot | Provides a direct comparator for interpretive contrast |

The most important addition beyond the prompt snapshot itself is the paired output snapshot when the causal question concerns prompt-versus-continuation discrimination.

## 6. Doctrine-Level Adoption Candidates

The following findings are mature enough to treat as doctrine-level methodology for future evaluation families:

1. **Rendered prompts are first-class evidence artifacts**
   High confidence. Demonstrated directly by the Stage C gap and the E1 recovery trace.

2. **Prompt provenance requires metadata, not text alone**
   High confidence. Demonstrated by the need for render-path, template, row, and hash information.

3. **Continuation-only evidence is insufficient for prompt-origin questions**
   High confidence. Demonstrated by the R1C/R1D uncertainty boundary and E1 closure of the prompt gap.

4. **Render-only evidence creation is the correct next step when prompt recovery is the blocker**
   High confidence. Demonstrated by the transition from extraction to E1.

5. **Representative control rows are necessary for prompt-surface interpretation**
   High confidence. Demonstrated by the E1 affected/control pair.

The following are not doctrine-level generalizations:

- the Stage C contamination taxonomy itself;
- the specific marker families observed in Stage C;
- the specific causal mix proposed for the Stage C cohort.

Those are family-specific findings, not reusable methodology doctrine.

## Direct Answers

### 1. What methodological lessons have been demonstrated by evidence?

Rendered prompts are primary evidence, prompt provenance needs metadata, continuation-only artifacts are insufficient for prompt-origin questions, and render-only trace creation is the smallest useful step when the prompt surface is missing.

### 2. Which lessons are specific to the Stage C contamination investigation?

The need to distinguish prompt markers from continuation markers in a chat-templated contamination case, and the use of a direct-answer control against an affected tool-directed row, are Stage C-specific.

### 3. Which lessons generalize to future evaluation families?

Exact prompt snapshots, render-path metadata, hashes, row binding, immutable trace bundles, clean control rows, and separate prompt/output surfaces generalize broadly.

### 4. Has Stage C demonstrated that rendered prompts should be treated as first-class evidence artifacts?

Yes, with high confidence.

### 5. What additional observability artifacts, if any, appear similarly important?

Raw continuation snapshots, render-path metadata, template fingerprints, row binding, dataset/manifest hashes, validation reports, and clean control snapshots.

### 6. Which findings are mature enough for doctrine-level adoption?

The first-class status of rendered prompts, the need for prompt provenance metadata, the insufficiency of continuation-only evidence for prompt-origin questions, the value of render-only trace creation, and the necessity of control rows.
