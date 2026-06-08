No repository changes were made.

# OSS_PKG_06_CURATED_REPOSITORY_IMPLEMENTATION_PLAN

## 1. Executive Summary

The curated/public repository should be implemented as a selective derivative of the canonical/private repository, not as a mirror and not as a second authority center. The implementation plan should therefore treat publication as a gated packaging process:

- canonical/private remains the source of truth;
- curated/public is derived from approved canonical material;
- publication is selective, reviewable, and bounded;
- bulk archive, data-bearing, report-heavy, and provenance-heavy surfaces remain canonical-only by default;
- a small, intentional `Curated Historical Evidence` layer is allowed, but it must stay narrow.

The most important operational rule is that the public repository should be built from a frozen canonical baseline after boundary review, validation, and license/rights gating. It should not accrete by ad hoc copying or independent public-only edits.

## 2. Initial Population Strategy

The first public repository should be created as a deliberate snapshot from canonical/private, not as an ongoing mirror.

Recommended sequencing:
1. Freeze the public inclusion boundary by category.
2. Verify the canonical/private source state and confirm there are no authority conflicts.
3. Complete the license/rights gate before external publication.
4. Assemble the curated tree from approved canonical material in a controlled staging step.
5. Validate content, links, hygiene, and category boundaries.
6. Perform a final publication review.
7. Publish the curated repository as an initial release.

Recommended review checkpoints:
- boundary review: confirm the inclusion categories are correct
- doctrine review: confirm the public package does not redefine authority
- hygiene review: confirm no secrets, PII, or machine-specific leaks were introduced
- historical-evidence review: confirm any selected history is bounded and reviewer-relevant
- final publication review: confirm the package is ready for external inspection

Recommended readiness gates:
- canonical/private source is the authority
- public content is fully classified
- no canonical-only family is accidentally included
- historical evidence remains bounded
- license/rights are resolved before public release
- validation passes on the assembled curated tree

## 3. Asset Mapping Strategy

Implementation should treat categories as assembly rules, not as a file-by-file freeform choice.

| Category | Implementation meaning | Update rule |
|---|---|---|
| Public Core | Required in the curated repository | Included by default; any omission must be intentional and reviewed |
| Public Supporting | Useful but optional | Included when it improves reviewability or onboarding without creating noise |
| Curated Historical Evidence | Bounded reviewer-facing history | Included only by nomination and review; growth must stay controlled |
| Canonical Only | Private-only by default | Excluded from the curated repository unless explicitly reclassified |

### Category rules in practice
- Public Core should carry the public method: doctrine, current-state guidance, framework, scripts, tests, and the canonical evaluation contract.
- Public Supporting should be small and low-cost, such as lightweight navigation aids or compatibility-friendly helpers when they improve public understanding.
- Curated Historical Evidence should be limited to decision-bearing history that explains major methodology evolution, governance inflection points, or publication decisions.
- Canonical Only should remain in the private repository: bulk `data/`, `reports/`, `manifests/`, generated artifacts, dense archive material, and provenance-sensitive research notes.

### Decision rules
- If a file is necessary to understand the current method, it is a candidate for Public Core.
- If a file adds clarity but not necessity, it is Public Supporting.
- If a file mainly proves how the method evolved, and that evidence is compact and decision-bearing, it is Curated Historical Evidence.
- If a file’s main value is archival depth, provenance, or local operational residue, it is Canonical Only.

## 4. Publication Workflow

The conceptual workflow should be:

canonical change
↓
publication review
↓
curated update

### Canonical change
All substantive content changes should originate in the canonical/private repository.

### Publication review
A distinct publication review should decide whether the canonical change:
- belongs in Public Core,
- belongs in Public Supporting,
- belongs in Curated Historical Evidence,
- or remains Canonical Only.

### Curated update
The curated repository should be updated only from approved canonical material.

### Workflow principles
- The curated repository should never lead on substantive content.
- Public-only edits should not introduce new doctrine or new authority.
- If a public change would alter meaning, the canonical source must be corrected first.
- If a public change is only presentational, it still needs traceability back to canonical content.
- Publication should be a reviewable act, not a background sync.

## 5. Curated Historical Evidence Workflow

Curated Historical Evidence should be maintained as a bounded evidence set, not a growing archive.

### Nomination
A candidate should be nominated only if it clearly demonstrates one of the following:
- a major methodology pivot
- a major governance inflection
- a closure or freeze decision
- a publication-architecture decision
- an independent review that materially influenced direction
- a concise milestone record that explains the project’s evolution

### Review
Each nomination should be checked against:
- uniqueness of evidence value
- compactness
- reviewer relevance
- overlap with existing evidence
- risk of archive creep

### Inclusion
Include only if the candidate adds a new question/answer pair for a reviewer, such as:
- why the methodology changed
- why the governance shifted
- why the public boundary looks the way it does
- why the project moved from one stage to another

### Retirement
Retire or demote a historical evidence item if:
- it becomes redundant with a more concise record
- it is superseded by a better evidence artifact
- it no longer adds reviewer value
- it starts to create archive pressure

### Growth control
- Keep the set small.
- Favor a fixed evidence spine over open-ended growth.
- Require a positive rationale for every new addition.
- Prefer replacement or consolidation over accumulation.

## 6. Validation Strategy

Validation should be different at each stage.

### Before initial publication
Verify:
- all included files belong to approved categories
- no Canonical Only material is present
- no secrets or PII are exposed
- no machine-specific paths or host assumptions are leaking into the public package in an unacceptable way
- links resolve within the curated repository
- current-state guidance is internally consistent
- historical evidence is bounded and decision-bearing
- the license/rights gate is complete
- the public package is readable as a coherent whole

### Before a major curated update
Verify:
- the change is still category-appropriate
- the public repository still reflects canonical truth
- no category drift occurred
- no archive creep was introduced
- no public-facing contradiction was added
- any added history still fits the evidence spine
- the update does not widen the public package beyond its intended boundary

### Before a historical-evidence addition
Verify:
- the item is genuinely evidence, not archive residue
- it adds reviewer value not already covered
- it is compact enough to read in the public package
- it does not duplicate another evidence item
- it does not create a maintenance burden disproportionate to its value

## 7. License Integration Assessment

License decisions should sit before external publication, not after it.

### Recommended placement
- Internal preparation of the curated package may proceed before final license adoption.
- External publication should not proceed before final license adoption and rights clarity.
- The curated repository should not be made public while its distribution rights remain unsettled.

### Practical interpretation
- treat license adoption as a pre-publication gate
- treat license/rights clarity as required before the first public release
- allow packaging work to continue locally while the license decision is being finalized
- do not treat the curated repository as externally published until that gate is cleared

### Why this matters
The curated repository is a public distribution product. Its publication should not get ahead of its legal and rights basis.

## 8. Risk Assessment

| Risk | Why it matters | Mitigation |
|---|---|---|
| Publication drift | The curated repo diverges from canonical truth | Keep canonical as source of truth and require publication review for changes |
| Authority confusion | Public repo appears to be an independent authority | State the authority model explicitly and keep precedence clear |
| Archive creep | Historical evidence grows into a second archive | Keep Curated Historical Evidence bounded and nomination-driven |
| Provenance mistakes | Mixed provenance content leaks into the public package | Use category gates and validation before publication |
| Review fatigue | Too many files make publication decisions noisy | Keep the curated set small and prefer distilled evidence |
| Stale publication | Public repo lags canonical changes | Make curated updates derivative and review-triggered |
| License gap | Public release proceeds without rights clarity | Require license adoption before first public publication |
| Hygiene regressions | Paths, hostnames, or sensitive artifacts leak into public package | Run hygiene validation before every publication gate |

## 9. Recommended Implementation Phases

### Phase 1: Publication preparation
- Freeze doctrine and publication categories.
- Confirm canonical/private authority.
- Define the initial public inclusion boundary.
- Establish the historical evidence spine.

### Phase 2: Curated assembly
- Select Public Core.
- Select limited Public Supporting material.
- Select a bounded Curated Historical Evidence set.
- Exclude Canonical Only material from the curated package.

### Phase 3: Validation
- Check category boundaries.
- Check links and navigation coherence.
- Check hygiene and provenance risk.
- Check evidence set size and reviewer value.
- Check that the package still reads as a coherent public repository.

### Phase 4: License gate and final review
- Confirm the license/rights decision is complete.
- Perform the final publication review.
- Resolve any publication defects before external release.

### Phase 5: Publication
- Publish the curated repository only after the above gates are satisfied.
- Treat the result as the first public snapshot, not a mirror sync.

### Phase 6: Maintenance
- Re-derive curated updates from canonical changes.
- Add historical evidence only through nomination and review.
- Periodically reassess whether evidence items remain necessary.
- Keep archive pressure under control.

## 10. Final Recommendation

Adopt a gated, canonical-first implementation model:

- canonical/private is the source of truth;
- curated/public is a selective derivative;
- publication is intentional and reviewable;
- Curated Historical Evidence remains small and decision-bearing;
- bulk history, data, reports, manifests, and research artifacts remain canonical-only by default;
- final license adoption must occur before external publication.

This plan preserves the repository’s public value while keeping the curated surface bounded, credible, and maintainable.
