Assessment and documentation creation authorized.

# PUBLIC_OPS_01_PUBLICATION_OPERATIONS_MODEL

## 1. Executive Summary

The ongoing publication model should be event-driven, review-gated, and derived from the canonical/private repository.

`assistant-training-private` remains the source of truth. `assistant-training` remains a selective curated derivative that is updated only when a publication review concludes that a canonical change belongs in the public package.

The operating goal is not maximum publication frequency. The goal is sustainable public credibility:
- keep the curated repository current enough to remain trustworthy
- keep it bounded enough to remain readable
- keep it selective enough to avoid archive creep
- keep the update process light enough to sustain over time

Recommended operating model:
- publication review is triggered by meaningful events, not by every commit
- a publication delta is computed against the last published public baseline
- automated checks pre-classify the delta
- Codex prepares the review package and flags category/rights risks
- a human approves or rejects the curated update
- every actual publication update produces a small canonical publication bulletin

This model preserves transparency, methodology dissemination, evidence preservation, Codex-for-OSS viability, and long-term project credibility without turning the public repository into a mirror.

## 2. Publication Objectives

Ongoing publication exists to make the public repository a durable, inspectable expression of the project’s method and governance.

| Objective | What it means operationally |
|---|---|
| Transparency | Show why the curated/public repository looks the way it does and what changed since the prior publication. |
| Methodology dissemination | Keep the public surface focused on the reusable regimen, doctrine, framework, and evaluation contract. |
| Evidence preservation | Preserve a bounded trail of curated historical evidence so readers can see how the method evolved. |
| Codex-for-OSS viability | Keep the public package structured so an automated or semi-automated reviewer can assess seriousness, rigor, and maintenance discipline. |
| Long-term credibility | Demonstrate that the project is maintained through deliberate review, not ad hoc publishing. |

The publication process should support these objectives without broadening the public repository beyond its intended boundary.

## 3. Publication Triggers

Publication review should be triggered by meaningful repository events, not by a fixed requirement to publish on every change.

### Recommended trigger model
Use an **event-driven model with a quarterly heartbeat**:
- event-driven for meaningful publication-relevant changes
- quarterly heartbeat to prevent the public repository from becoming stale

### Trigger classes
| Trigger | Review required? | Notes |
|---|---|---|
| Milestone completion | Yes | Any milestone that changes the public narrative, public core, or evidence spine should trigger review. |
| Methodology change | Yes | Changes to doctrine, framework, current-state orientation, or public navigation should always be reviewed. |
| Evidence-spine change | Yes | Additions, retirements, or replacements in curated historical evidence are publication-relevant. |
| Rights or license change | Yes | Any change affecting publication rights, notices, or included-family eligibility is a gate event. |
| Significant ad hoc finding | Yes | A newly discovered issue, correction, or major insight should trigger review if it affects public-facing material. |
| Cadence heartbeat | Yes, but only as a review checkpoint | Use a fixed cadence as a stale-repo guard, not as a content driver. |

### Trigger policy
- milestone events should dominate cadence
- cadence should not force unnecessary publication
- ad hoc findings should be batched until they are coherent enough to justify a publication update

## 4. Publication Delta Model

Publication should answer one question:

What changed since the last publication that matters to the curated public repository?

### Delta source of truth
Compare the canonical/private repository against the last published curated baseline.

### Delta classification
Every changed item should be classified into one of these outcomes:
- `Publish`
- `Publish with review`
- `Hold`
- `Exclude`
- `Escalate`

### Candidate identification rules
A change is publication-relevant if it:
- changes Public Core
- changes Public Supporting
- changes Curated Historical Evidence
- changes rights/publication posture
- changes navigation or reader flow
- changes the meaning of what the public repo claims to be

A change is usually not publication-relevant if it:
- only affects Canonical Only families
- is a local operational artifact
- is a generated report or manifest that stays private
- does not affect the public narrative, reader journey, or evidence spine

### Delta grouping
Candidates should be grouped by publication impact rather than by raw file list:
1. public-core delta
2. supporting/navigation delta
3. historical-evidence delta
4. rights/publication-doctrine delta
5. canonical-only no-public-action delta

### Practical selection rule
The publication candidate list should be built from:
- direct changes in included families
- canonical-only changes that alter a public-facing concept, policy, or boundary
- evidence additions or retirements that alter the bounded evidence spine

This makes the delta model stable and reviewable.

## 5. Publication Review Workflow

The publication review workflow should be layered so that automation does preclassification, Codex does synthesis, and a human makes the final approval decision.

### Automated assessment opportunities
Automated checks should identify:
- file presence in allowed or disallowed families
- link validity
- markdown hygiene / trailing whitespace / formatting defects
- obvious rights/provenance signals
- machine-specific path leakage
- evidence-spine size and duplication issues
- whether the change touches an approved public category

### Codex responsibilities
Codex should:
- summarize the canonical delta
- classify each candidate by publication category
- identify contradictions or boundary violations
- group file-level changes into publication items
- draft the publication bulletin
- recommend publish / hold / escalate decisions
- identify any file-level rights review needed before release

### Human-review responsibilities
The human reviewer should:
- approve category promotions
- approve or reject Curated Historical Evidence additions
- resolve rights and publication-doctrine questions
- verify the curated update still represents the canonical source faithfully
- decide whether the update is ready for external publication

### Approval gates
No curated update should proceed unless all of the following pass:
- boundary gate: correct families only
- rights gate: no unresolved publication-rights issues
- hygiene gate: no obvious defects or sensitive leaks
- coherence gate: the public repo still reads as a coherent package
- reviewer-value gate: the change is worth publishing
- evidence gate: the historical layer remains bounded

### Workflow summary
canonical change -> automated classification -> Codex review package -> human approval -> curated update -> publication bulletin

## 6. Publication Bulletin Model

Yes. Every actual publication update should create a short publication bulletin.

### Purpose
The bulletin is the durable publication record that explains:
- what was published
- why it was published
- what remained excluded
- what validations were run
- what the next publication concern is

It is the public-repository equivalent of an internal release note and decision capsule.

### Recommended properties
- append-only
- canonical/private repository artifact
- small enough to read quickly
- linked to the publication baseline
- written after review, not before

### Suggested structure
1. **Update ID / timestamp**
   - unique publication update label and source baseline
2. **Trigger**
   - milestone, methodology change, evidence change, rights change, or cadence review
3. **Delta summary**
   - what changed by category
4. **Publication decisions**
   - what was published, held, excluded, or escalated
5. **Validation results**
   - hygiene, link, boundary, and rights checks
6. **Curated historical evidence changes**
   - additions, retirements, or replacements
7. **Residual risks**
   - anything still worth watching
8. **Next review date**
   - when the next heartbeat or event-driven review should occur

### Bulletin rule
If there is no actual curated update, no bulletin is required beyond whatever internal review record is used for the closed review cycle.

## 7. Maintenance Burden Assessment

The operating model should keep publication effort predictable.

### Routine publication updates
Expected effort:
- low to moderate
- typically a few focused hours
- dominated by review, validation, and bulletin drafting rather than by file movement or assembly work

### Major publication updates
Expected effort:
- moderate to high
- typically one to two working days
- driven by methodology changes, evidence-spine adjustments, rights posture changes, or navigation rewrites

### Sustainable target
Keep most publication updates in the routine category.

The model is sustainable if:
- small changes are batched until they are coherent
- major updates are tied to meaningful milestones
- the evidence spine stays bounded
- the public package does not churn on every internal change

If the process starts to require frequent major updates, the public boundary is too wide or the release cadence is too aggressive.

## 8. Future Automation Opportunities

The following publication-process elements could reasonably become semi-automated later:

- delta extraction between canonical/private and last published curated baseline
- category classification suggestions for changed files
- link and markdown hygiene checks
- rights/provenance keyword scanning
- evidence-spine duplication and cap checking
- stale-public-repository alerts
- publication bulletin draft generation
- change-summary generation for Codex review
- category-boundary validation for included families

What should remain human-controlled:
- category promotion decisions
- rights/notice decisions
- curated historical evidence inclusion or retirement
- final publication approval

## 9. Risk Assessment

| Risk | Why it matters | Mitigation |
|---|---|---|
| Stale public repository | Public readers lose trust if the curated repo lags the canonical source too much | Use event-driven updates plus a quarterly heartbeat review. |
| Over-publication | Too many updates can turn the curated repo into a noisy mirror | Require publication relevance, batching, and human approval. |
| Under-publication | Too few updates can make the public repo feel abandoned or misleading | Use the heartbeat review and trigger-based reviews for significant events. |
| Publication drift | Curated/public content could diverge from canonical truth | Keep canonical/private authoritative and require publication review for every change. |
| Review fatigue | Too many ambiguous updates can overburden maintainers and reviewers | Keep the curated boundary narrow and the evidence spine bounded. |

## 10. Final Recommendation

Adopt an event-driven publication operations model with a quarterly heartbeat review, a bounded delta model, layered review, and a mandatory publication bulletin for every actual curated update.

In short:
- canonical/private changes first
- publication review second
- curated/public update third
- bulletin last

This is the most sustainable way to keep the public repository current, credible, and bounded without forcing every internal change into an external release.
