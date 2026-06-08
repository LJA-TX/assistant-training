Assessment and documentation creation authorized.

# PUBLIC_REPO_03_HISTORICAL_EVIDENCE_SPINE_DESIGN

## 1. Executive Summary

The historical evidence spine should answer a narrow reviewer question:

What is the minimum historical trail a public reader needs in order to understand how this methodology evolved, why the public package looks the way it does, and why the repository should be trusted as a disciplined technical effort?

The spine should not behave like an archive. It should behave like a curated evidence path.

Best design:
- a hybrid structure
- thematic grouping as the primary organization
- chronological ordering within each theme
- a single index page that explains how to read the evidence

This preserves reviewer value without allowing the historical layer to expand into a second archive. The spine should remain bounded, decision-bearing, and easy to navigate from the public front door.

## 2. Evidence Spine Purpose

The evidence spine exists to prove that the current public method is the result of real work, not a synthetic or static shell.

It answers four reader questions:
- how did the methodology evolve?
- what major failures or constraints caused the method to change?
- what governance or publication decisions shaped the current boundary?
- what small set of historical records best proves sustained, disciplined work?

The spine is not trying to tell the whole project history. It is trying to make the current repository credible to a technically competent reviewer.

## 3. Evidence Organization Strategy

Recommended organization: **hybrid model**.

### Why hybrid is best
- pure chronology is too flat and makes readers browse blindly
- pure theme can hide the actual sequence of decisions
- milestone-only organization can overemphasize closure records and underemphasize methodology shifts
- hybrid grouping gives readers both meaning and sequence

### Proposed ordering rule
1. group by theme
2. sort artifacts chronologically within each theme
3. keep one compact index that shows the full path at a glance

### Suggested theme order
1. lineage and inflection points
2. methodology transitions
3. current-state milestones
4. governance and publication-history decisions

This order moves from how the method changed, to how the process matured, to what the current state became, to how publication governance was refined.

## 4. Reader Journey

### First-time visitor
Recommended path:
1. `README.md`
2. `docs/current/start_here.md`
3. `docs/current/current_status.md`
4. `docs/current/framework_vs_history.md`
5. `docs/framework/lineages/README.md`

Goal:
- understand what the repository is
- understand what is current
- understand where history begins
- see the evidence spine as a curated trail, not an archive dump

### Technical reviewer
Recommended path:
1. `README.md`
2. `docs/framework/lineages/README.md`
3. lineage evidence items
4. methodology transition records
5. current-state milestone records
6. governance/publication-history records
7. `scripts/`
8. `tests/`

Goal:
- inspect the method
- inspect the historical basis for the method
- verify that the evidence is bounded and decision-bearing

### Codex-for-OSS reviewer
Recommended path:
1. `README.md`
2. `docs/current/framework_vs_history.md`
3. `docs/framework/lineages/README.md`
4. selected lineage items
5. selected methodology transitions
6. selected governance/publication-history records
7. `scripts/`
8. `tests/`

Goal:
- assess seriousness
- assess maintenance discipline
- assess methodology evolution
- assess governance maturity
- assess whether the public repo looks intentionally curated

## 5. Evidence Index Design

The primary index should be `docs/framework/lineages/README.md`.

### Index responsibilities
- explain the purpose of the evidence spine
- state the minimum reading path
- group the evidence by theme
- explain why each artifact matters
- show the full spine on one page
- prevent the reader from mistaking the spine for an archive

### Suggested sections for the index
1. **Purpose**
   - one short paragraph explaining what the spine answers
2. **How to Read This Spine**
   - a minimum reading path for quick use
3. **Theme 1: Lineage and Inflection Points**
   - the earliest methodological pivots and constraint events
4. **Theme 2: Methodology Transitions**
   - process-architecture and regimen-shaping assessments
5. **Theme 3: Current-State Milestones**
   - closure determinations and launch plans that show the present state emerging
6. **Theme 4: Governance and Publication History**
   - independent review and public-front-door refinement
7. **Evidence Legend**
   - tags or labels such as `lineage`, `methodology`, `milestone`, `governance`

### Artifact presentation format
Each listed artifact should have:
- a short title
- a one-sentence reason it matters
- a theme label
- optional predecessor/successor hints if that improves navigation

### Minimum reading path
The index should provide a short path for time-limited readers:
1. `README.md`
2. `docs/framework/lineages/README.md`
3. `i2_contamination_event.md`
4. `i6_isolated_variable_pivot.md`
5. `STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md`
6. `STAGE_B_COMPLETION_DETERMINATION.md`
7. `OSS_01_INDEPENDENT_REVIEW_AND_RECONCILIATION_GROK.md`
8. `OSS_05_PUBLIC_FRONT_DOOR_IMPLEMENTATION_SUMMARY.md`

That short path is enough to show the major arc without requiring the reader to consume all 12 artifacts immediately.

## 6. Evidence Boundaries

### Belongs in the spine
Artifacts that:
- mark major methodological pivots
- document closure, readiness, or freeze decisions
- show major governance or publication decisions
- explain why the current public method looks the way it does
- are compact enough to read without archive context
- add a new question/answer pair for the reviewer

### Does not belong in the spine
Artifacts that are primarily:
- bulk archive records
- routine housekeeping
- operational manifests
- generated reports
- research memos
- exploratory notes that require archive context to interpret
- duplicated summaries that do not add new evidence value

### How future additions are evaluated
Future additions should be accepted only if they:
- represent a major new inflection point
- add evidence not already present in the spine
- can be read independently
- do not increase the spine into a second archive

If a new artifact merely repeats an existing theme without adding new evidence value, it should not be added.

## 7. Growth Control

The spine must remain bounded by design.

### Artifact cap
- Keep the active spine at approximately 12 artifacts, inclusive of the index page if the index is counted as part of the spine presentation.
- If the index is treated as separate navigation, keep the evidence set itself at about 11 artifacts.

### Replacement rules
- Additions should usually replace older or weaker items in the same theme rather than expand the set.
- If a new item is added, it should displace an item that is redundant, less compact, or less decision-bearing.

### Retirement criteria
Retire an item if:
- it is superseded by a more compact or clearer record
- it no longer adds reviewer value
- another artifact now expresses the same decision more cleanly
- it creates disproportionate maintenance or explanation burden

### Bounded growth principle
The spine should be refreshed only when it materially improves reviewer value. Otherwise, it should stay fixed.

## 8. AGENTS.md Assessment

`AGENTS.md` should be referenced from the evidence spine only as a supporting navigation pointer, not as a historical evidence item.

Recommended treatment:
- do not include `AGENTS.md` in the evidence list itself
- do include a brief note in the index or adjacent reader guidance pointing maintainers to it

Rationale:
- `AGENTS.md` helps explain process routing and agentic workflow
- it supports maintainability
- but it is not part of the historical record being curated by the spine
- including it as evidence would blur the boundary between historical proof and operational guidance

So the correct use is a side reference, not a spine artifact.

## 9. Recommended Evidence Spine Blueprint

### Spine structure
- `docs/framework/lineages/README.md`
  - purpose
  - reading guide
  - theme map
  - minimum reading path
  - evidence legend

### Theme 1: Lineage and inflection points
- `i2_contamination_event.md`
- `i4_i5_overconstraint_collapse.md`
- `i6_isolated_variable_pivot.md`
- `i7_coupled_schema_dynamics.md`
- `i8_pre_training_governance_snapshot.md`

### Theme 2: Methodology transitions
- `STAGE_BC_PROCESS_ARCHITECTURE_PROPOSAL.md`
- `STAGE_C_BLOCKER_BRANCH_CLOSURE_AND_RUNTIME_OUTPUT_TRANSITION_ASSESSMENT.md`

### Theme 3: Current-state milestones
- `STAGE_B_COMPLETION_DETERMINATION.md`
- `STAGE_C_RUNTIME_OUTPUT_AND_CORPUS_BEHAVIOR_INVESTIGATION_LAUNCH_PLAN.md`

### Theme 4: Governance and publication history
- `OSS_01_INDEPENDENT_REVIEW_AND_RECONCILIATION_GROK.md`
- `OSS_05_PUBLIC_FRONT_DOOR_IMPLEMENTATION_SUMMARY.md`

### Index behavior
- show all artifacts in one bounded place
- preserve thematic grouping
- keep the reader on a short path from current-state orientation into evidence

## 10. Final Recommendation

Adopt a hybrid historical evidence spine with thematic grouping and chronological order within each theme.

Keep the spine small, decision-bearing, and reviewer-friendly. Use `docs/framework/lineages/README.md` as the primary index. Reference `AGENTS.md` only as a support pointer, not as a spine artifact. Preserve the 12-artifact evidence set as a bounded historical trail that proves methodology evolution without turning the public repository into an archive.
