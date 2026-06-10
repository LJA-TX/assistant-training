# Stage C Doctrine Adoption Candidate Assessment

## Executive Summary

Stage C produced one doctrine-worthy methodology result and several supporting guidance results.

The doctrine-worthy result is narrow but durable:

- when prompt construction can affect interpretation, the exact rendered prompt must be treated as a first-class evidence artifact;
- prompt provenance must be attached to that artifact through row identity, source/manifest provenance, render-path metadata, and hashes; and
- continuation text alone is not sufficient to establish prompt provenance or prompt-origin claims.

What remains provisional is the packaging and sampling pattern used to create that evidence in Stage C:

- render-only trace bundles;
- one affected row plus one clean control row;
- a manifest / JSONL / raw prompt / validation-report bundle shape; and
- the exact minimum control strategy for more complex future families.

This assessment stays on methodology governance only. It does not revisit contamination analysis.

## Adoption Standard Used Here

For Stage C methodology to qualify for doctrine-level adoption, the finding must:

1. be directly supported by completed evidence, not a single ad hoc observation;
2. be independent of the specific contamination content;
3. generalize to future evaluation families;
4. improve observability or interpretability without changing model, scorer, detector, or threshold behavior; and
5. be stable enough to state as a norm, not merely as a one-off recommendation.

Under that standard, Stage C supports one strong doctrine rule and several supporting guidance rules.

## 1. Which Findings Meet Doctrine-Level Adoption?

| Finding | Recommendation | Why it meets the standard |
|---|---|---|
| Exact rendered prompts are first-class evidence artifacts | **Doctrine** | Stage C showed the decisive missing fact was the rendered prompt itself, and the E1 trace created it as durable evidence. |
| Prompt provenance must be captured with the rendered prompt | **Doctrine** | The rendered text is not self-authenticating without row identity, source provenance, render-path metadata, and hashes. |
| Continuation text alone is insufficient for prompt-origin claims | **Doctrine** | Prompt-origin questions cannot be settled from post-prompt continuation alone. |
| Prompt and continuation surfaces must be preserved separately when prompt construction may affect interpretation | **Doctrine** | Causal discrimination requires pre-generation and post-generation surfaces to remain distinct. |

These are mature enough for formal adoption because they are content-independent and generalize beyond the Stage C case.

## 2. Which Findings Remain Provisional?

| Finding | Recommendation | Why it remains provisional |
|---|---|---|
| Render-only evidence creation is the preferred next step when prompt recovery is blocked | **Guidance** | Strongly supported by Stage C, but it is a procedure for evidence creation, not a universal norm about evidence validity. |
| A clean control prompt should accompany prompt-surface investigations | **Guidance** | The control row clearly improved interpretation in Stage C, but the exact control strategy is not yet proven universal. |
| The manifest / JSONL / raw prompt / validation-report bundle shape is the preferred packaging pattern | **Guidance** | Proven useful in Stage C, but still a packaging convention rather than a doctrine requirement. |
| The minimum useful sample for prompt-trace creation is one affected row plus one control row | **Guidance** | Validated in Stage C as a smallest useful experiment, but not yet frozen as a universal minimum for all families. |
| The exact minimum control strategy for complex multi-turn or dynamically rendered families | **Open question** | Stage C does not yet establish how many controls or render snapshots are needed in more complex cases. |

## 3. Classification By Category

### Doctrine

1. Exact rendered prompts are first-class evidence artifacts.
2. Prompt provenance must be attached to the rendered prompt artifact.
3. Continuation text alone is insufficient for prompt-origin claims.
4. Prompt and continuation surfaces must be preserved separately when prompt construction is relevant.

### Guidance

1. Use render-only trace bundles when exact prompt recovery is the blocker.
2. Include a clean control prompt whenever the question is comparative.
3. Package the evidence as a manifest, JSONL index, raw prompt snapshots, and validation report.
4. Start with one affected row and one control row unless a family-specific reason requires broader sampling.

### Observation

1. Stage C’s frozen record did not preserve the exact rendered prompt.
2. The E1 render-only trace created the missing prompt evidence.
3. The E1 validation report passed render-only checks and confirmed exact hash match.

### Open Question

1. What is the minimum prompt-trace control strategy for more complex families with multi-turn or conditional prompt construction?

## 4. Exact Doctrine Statement To Adopt

If rendered prompts are to be treated as first-class evidence artifacts, the doctrine statement should read:

> When prompt construction may affect interpretation, the exact rendered prompt MUST be captured as a first-class evidence artifact. The artifact MUST be accompanied by row identity, source dataset and manifest provenance, render-path metadata, and stable hashes or fingerprints. Continuation text alone MUST NOT be used to infer prompt provenance or to substitute for the rendered prompt.

That statement is intentionally narrow:

- it governs evidence capture;
- it does not prescribe detector behavior;
- it does not change evaluator behavior; and
- it does not depend on any particular contamination content.

## 5. How Future Evaluation Families Should Demonstrate Compliance

Future evaluation families should demonstrate compliance by producing a render-trace bundle that shows all of the following:

1. the canonical render path used to build the prompt;
2. the exact rendered prompt text preserved as a raw file;
3. row identity and source-case binding for every captured prompt;
4. source dataset and manifest provenance, including hashes;
5. template or tokenizer identity, including any fallback choice;
6. a validation report confirming exactness, hash match, and render-only execution; and
7. a clean control prompt whenever the investigation is comparative.

Operationally, compliance should be visible in the evidence bundle itself:

- exact prompt snapshot present;
- provenance metadata present;
- hash verification present;
- render-only status present;
- no generation path entered;
- no scoring or detector path entered; and
- control prompt present when a comparative claim is being made.

## 6. Final Adoption Determination

### Adopt As Doctrine

- exact rendered prompts are first-class evidence artifacts;
- prompt provenance must accompany the rendered prompt;
- continuation text alone is not sufficient for prompt-origin claims; and
- prompt and continuation surfaces must remain separate when prompt construction matters.

### Keep As Guidance

- render-only trace bundles as the preferred evidence-creation pattern;
- one affected row plus one clean control row as the smallest useful prompt-trace experiment; and
- the manifest / JSONL / raw prompt / validation-report packaging pattern.

### Keep As Observation

- Stage C could not recover exact prompts from the frozen record; and
- E1 successfully created the missing prompt evidence without generation.

### Keep As Open Question

- the minimum control strategy for more complex future families.
