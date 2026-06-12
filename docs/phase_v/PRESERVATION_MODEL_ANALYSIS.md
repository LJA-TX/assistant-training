# Preservation Model Analysis

## Primary Question

What did H1/H2 preserve that v1.1, v1.2, Phase Q, and Phase U did not?

## Answer

H1/H2 preserved the **joint training context** in which exact tool-call behavior could be learned:

- a frozen Stage B recovery scaffold,
- a small patch of only `100` tool-positive rows,
- a majority of exact-tool-request prompts on those positive rows,
- and a high concentration of examples on a small set of anchor tools.

Later interventions split those properties apart:

- v1.1 preserved safety but flattened the tool manifold and removed the exact-tool-request cue from the tool-positive rows.
- v1.2 restored some anchor concentration but still did not recreate the H1/H2 cue structure.
- Phase Q showed that the resulting model often emits near-canonical but invalid envelopes.
- Phase U showed that schema-only repair, at least at micro-patch scale, preserves safety but can still collapse into direct answers.

## Ranked Preservation Model

### A. Frozen scaffold plus exact-tool-request cue plus anchor concentration

**Confidence: high**

This is the only model that explains all of the following at once:

- H1/H2 exact JSON around `0.44` to `0.48`,
- H1/H2 tool-name accuracy around `0.71` to `0.77`,
- H1/H2 argument accuracy around `0.63` to `0.69`,
- later capability collapse in v1.1/v1.2,
- Phase Q wrapper drift,
- Phase U direct-answer collapse.

Why it fits:

- H1/H2 keep the exact-tool-request cue on a majority of tool-positive rows.
- H1/H2 keep the core anchors dominant.
- H1/H2 change only a small fraction of the train surface.

### B. Anchor concentration as a necessary but not sufficient condition

**Confidence: high**

Anchor weighting matters, but it is not enough on its own.

Evidence:

- v1.2 restores anchor concentration relative to v1.1.
- Phase Q still fails badly on exact JSON and wrapper drift.
- Therefore, anchor concentration without the right cue structure does not recover the envelope.

### C. Exact envelope realization as a necessary but not sufficient condition

**Confidence: high**

Phase U is the counterexample:

- the patch is fully canonical on the schema surface,
- the patch is contamination-clean,
- the patch is limited to the five core anchors,
- yet exact JSON, tool-name accuracy, and argument accuracy all fall to `0.0`.

So exact schema text alone does not recover capability without the broader scaffold.

### D. Broad prompt-style diversity as a negative correlate for exact realization

**Confidence: medium**

v1.1 and v1.2 both use eight balanced prompt styles and fail to recover H1/H2-level capability.

This does not prove causality by itself, but it strongly suggests that widening the prompt manifold before schema realization is stable is counterproductive.

### E. Safety calibration as orthogonal to capability

**Confidence: high**

Safety calibration is important for no-call behavior, but it does not explain why H1/H2 recover capability and later interventions do not.

Evidence:

- Phase L preserved no-call and adversarial no-call safety, but exact JSON was `0.0`.
- Phase U preserved no-call and adversarial no-call safety, but exact JSON was still `0.0`.
- Therefore safety alone is orthogonal to the recovery question.

## Smallest Model Consistent With the Evidence

The smallest defensible model is a **conjunctive preservation model**:

> H1/H2 succeeded because they preserved the frozen scaffold, the exact-tool-request cue, and anchor concentration together.

This model is smaller than a broad "more data is better" story and smaller than a schema-only story.

## What This Model Rules Out

- It rules out prompt entropy alone as the driver.
- It rules out anchor concentration alone as the driver.
- It rules out strict JSON wording alone as the driver.
- It rules out safety calibration as the driver of capability recovery.

## Confidence Assessment

- Frozen scaffold contribution: high
- Exact-tool-request contribution: high
- Anchor concentration contribution: high
- Prompt-manifold widening as a failure mode: medium-high
- Trainer geometry as a primary cause: low

## Practical Reading

The preservation problem is not "did the model see JSON?" It is "did the model repeatedly see the exact tool-call contract, on a narrow anchor-heavy patch, inside a frozen scaffold?"

H1/H2 did. The later interventions did not keep all three conditions together.
