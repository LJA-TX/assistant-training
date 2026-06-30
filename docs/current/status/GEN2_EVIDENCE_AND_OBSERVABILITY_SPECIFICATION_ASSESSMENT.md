# Gen-2 Evidence And Observability Specification Assessment

Date: 2026-06-30

## Scope

This document provides a documentation-only strategic assessment of whether the Gen-2 program should eventually include a dedicated `GEN2_EVIDENCE_AND_OBSERVABILITY_SPECIFICATION.md` artifact, and if so, what role that artifact should play.

Its purpose is to define the methodological problem such a specification would solve, the kinds of evidence it would need to govern, and the boundaries required to keep it scientific rather than operational.

This document does **not** authorize D2 planning, training, evaluation execution, experiment design, treatment-arm design, run planning, preregistration creation, manifest edits, hash-claim edits, or governance reinterpretation.

`Gen-2` remains a strategic program label only.

## Inputs

- [current_status.md](../current_status.md)
- [project_outcomes_to_date.md](../project_outcomes_to_date.md)
- [GEN2_PROGRAM_CHARTER.md](./GEN2_PROGRAM_CHARTER.md)
- [GEN2_PROSPECTIVE_EVIDENCE_PROGRAM_ASSESSMENT.md](./GEN2_PROSPECTIVE_EVIDENCE_PROGRAM_ASSESSMENT.md)
- [GEN2_STRATEGIC_DIRECTION_OPTIONS_ASSESSMENT.md](./GEN2_STRATEGIC_DIRECTION_OPTIONS_ASSESSMENT.md)
- [GEN2_SCOPE_BOUNDARY_ASSESSMENT.md](./GEN2_SCOPE_BOUNDARY_ASSESSMENT.md)
- [D1_CLOSURE_AND_D2_READINESS_ASSESSMENT.md](./D1_CLOSURE_AND_D2_READINESS_ASSESSMENT.md)
- [../../continuity/D1_MECHANISM_HYPOTHESIS_INVENTORY_SPECIFICATION.md](../../continuity/D1_MECHANISM_HYPOTHESIS_INVENTORY_SPECIFICATION.md)
- [../../continuity/D1_MECHANISM_HYPOTHESIS_INVENTORY.md](../../continuity/D1_MECHANISM_HYPOTHESIS_INVENTORY.md)
- [../../continuity/STAGE_C_CLOSURE_CONTINUITY_PACKAGE.md](../../continuity/STAGE_C_CLOSURE_CONTINUITY_PACKAGE.md)
- [../../convergence/STAGE_C_FINAL_DISPOSITION_AND_PUBLICATION_ASSESSMENT.md](../../convergence/STAGE_C_FINAL_DISPOSITION_AND_PUBLICATION_ASSESSMENT.md)
- [TRAINING_RUN_HISTORY.md](./TRAINING_RUN_HISTORY.md)

## Current Basis

The current repository-backed basis for this assessment is:

- Stage B is complete.
- Stage C is complete and closed as historical work with retained guidance.
- D1 is complete and published.
- The Gen-2 charter package is published and integrated.
- The Gen-2 program is currently defined as an explanatory-comparability and observability program.
- `D0-BLK-TRAINING-SCRIPT-PROVENANCE-001` remains active.
- D2 planning is not authorized.
- The public repository remains a bounded curated package rather than an open-ended working archive.

## Determination

A prospective `GEN2_EVIDENCE_AND_OBSERVABILITY_SPECIFICATION.md` **does belong inside the Gen-2 program identity** as a foundational methodological asset.

It should be treated as a scientific admissibility specification, not as an execution document.

Its role would be to translate the Gen-2 charter's observability-first and evidence-discipline principles into a reusable capture-and-interpretation standard for any future claim-bearing Gen-2 work.

It would not, by itself:

- authorize D2;
- authorize study design;
- authorize execution;
- select interventions;
- define treatment arms;
- define runs; or
- weaken existing authority boundaries.

In short: the charter defines what Gen-2 is for, while a future evidence-and-observability specification would define what evidence must exist before future Gen-2 findings could be treated as scientifically admissible.

## 1. Problem This Specification Would Solve

The current Gen-2 charter identifies observability, provenance, claim-tier discipline, and evidence capture as non-negotiable. What it does not yet provide is a dedicated methodological surface that states, in one place, exactly what evidence must exist before later interpretation is allowed.

That gap creates several risks:

1. observability requirements remain scattered across multiple documents rather than consolidated into a reusable standard;
2. future work could satisfy the spirit of the charter unevenly or inconsistently;
3. missing evidence could be discovered only after interpretation has already begun;
4. studies could drift into summary-score reporting without preserving the surfaces needed for later explanation; and
5. future comparisons could look formally similar while resting on materially different evidence quality.

The prospective specification would solve a narrow but important problem:

- it would likely define the minimum evidence package needed for later explanatory, comparative, or mechanism-oriented interpretation;
- it would distinguish archival retention from scientific admissibility;
- it would likely state which metadata count as first-class evidence rather than clerical detail; and
- it would likely make later invalidation or downgrade rules explicit instead of leaving them to narrative judgment.

## 2. Illustrative Evidence Categories A Future Specification Would Likely Need To Address

If the repository later decided to author such a specification, it would likely need to address evidence across categories like the following.

These are illustrative categories suggested by the charter and by Gen-1 lessons, not a committed final schema.

### 2.1 Study Framing And Comparison-Class Evidence

- study identity and scope statement;
- claim tier being pursued;
- declared comparison class;
- declared control or reference class;
- explicit fixed surfaces;
- explicit allowed-to-vary surfaces; and
- declared interpretation boundary.

### 2.2 Prompt-Surface Evidence

- exact rendered prompts whenever prompt construction materially affects interpretation;
- prompt template identity;
- render-path identity;
- serialization details when relevant; and
- prompt-surface hashes or equivalent integrity markers.

### 2.3 Dataset And Row-Provenance Evidence

- dataset identity and version;
- row identity for every claim-bearing example;
- source provenance for rows or exemplars;
- inclusion/exclusion basis when it materially affects interpretation; and
- lineage from source row to rendered prompt to emitted output.

### 2.4 Implementation And Configuration Evidence

- script or implementation identity;
- config identity;
- model or baseline identity;
- seed and environment pinning when relevant;
- evaluator/scorer identity; and
- versioned surfaces for any machinery that materially shapes outputs or scores.

### 2.5 Behavioral Output Evidence

- raw outputs underlying later claims;
- tool-use traces or equivalent behavioral artifacts when the claim concerns tool behavior;
- scored outputs mapped back to the originating rows; and
- preserved evidence of failures as well as successes.

### 2.6 Evaluation And Measurement Evidence

- measurement contract identity;
- scorer inputs and outputs;
- summary tables linked to underlying row-level evidence;
- validation results for measurement surfaces; and
- any aggregation logic needed to interpret reported totals or rates.

### 2.7 Confound, Uncertainty, And Claim-Qualification Evidence

- structured confound records;
- explicit uncertainty statements;
- declared known interpretation limits;
- evidence-role typing for artifacts used in support of claims; and
- separation between descriptive evidence and stronger explanatory interpretation.

### 2.8 Evidence-Creation And Validation Evidence

- the evidence-creation code or equivalent machinery when it is part of the reproducibility boundary;
- validation outputs proving the evidence package was formed as declared; and
- append-only change history for claim-bearing surfaces.

### 2.9 Runtime Evidence When Runtime Claims Are Made

If a study makes runtime-behavior claims, runtime artifacts would likely need explicit treatment. A future specification may choose to treat runtime evidence as conditional on claim type rather than universally required for every artifact regardless of claim.

## 3. Metadata A Future Specification May Need To Treat As First-Class Evidence

Based on the charter and the published Gen-1 lessons, a future specification may choose to treat the following metadata as first-class evidence rather than as supporting notes:

1. artifact identity and artifact hashes;
2. row identifiers and row-to-output mappings;
3. source provenance identifiers;
4. prompt template identity;
5. render-path identity;
6. model, baseline, and implementation identifiers;
7. config identifiers;
8. evaluator and scorer identifiers;
9. version identifiers for datasets, prompts, evaluation contracts, and code paths;
10. fixed-surface declarations;
11. allowed-to-vary declarations;
12. comparison-class and reference-class declarations;
13. claim tier and evidence-role typing;
14. confound identifiers or structured confound references;
15. timestamps and sequence ordering where they materially affect interpretation; and
16. validation status for claim-bearing artifacts.

The methodological point is simple: if later interpretation depends on a field, a future specification may need to treat that field as part of the evidence rather than as "metadata only."

## 4. Observability Themes That Follow From Gen-1 Lessons

The strongest Gen-1 lessons imply a specific observability doctrine for Gen-2. A future specification would likely need to resolve themes like the following.

### 4.1 Observability Must Exist At Source

Gen-1 suggests that evidence materially affecting interpretation would likely need to be captured when the artifact is created, not inferred later from adjacent files or memory.

### 4.2 Prompt Construction Is Part Of The Evidence When It Changes Meaning

If prompt construction can alter behavior, a future specification may need to treat the exact rendered prompt surface as part of the scientific record rather than as an implementation detail.

### 4.3 Summary Metrics Are Not Self-Interpreting

Gen-1 suggests that scores, counts, and tables are not sufficient on their own. A future specification would likely need them to remain linked to the underlying row-level, prompt-level, and output-level evidence that gave rise to them.

### 4.4 Evidence Roles Must Remain Distinct

A future specification would likely need clear separation between behavioral evidence, governance evidence, provenance evidence, contract evidence, and continuity-context evidence so they are not mixed interchangeably in support of claims.

### 4.5 Confounds Must Be Structured Rather Than Buried In Narrative

Gen-1 showed that explanation work becomes unreliable when confounds are handled in prose alone. A future specification may therefore choose to codify structured confound capture whenever work intends to support more than descriptive claims.

### 4.6 Evidence-Creation Machinery Sometimes Belongs Inside The Scientific Boundary

When the code or workflow that created the evidence is the only reliable way to understand what happened, a future specification may need to treat that machinery as part of the evidence package rather than as disposable scaffolding.

### 4.7 Missing Evidence Must Stay Missing

Any future specification would likely inherit the Gen-1 lesson that later substitution, repair, or inference-based backfill is not a fix. It is an admissibility problem.

## 5. Evidence Likely Needing Creation-Time Capture

A future specification would likely need to identify some evidence as creation-time capture obligations because later reconstruction would be lossy or credibility-damaging.

Illustrative examples include:

1. exact rendered prompts when prompt construction affects interpretation;
2. row identities and source lineage;
3. raw outputs and tool-use traces behind later claims;
4. prompt, dataset, scorer, and config version identifiers;
5. fixed-surface and allowed-to-vary declarations for the claim-bearing artifact;
6. comparison class and reference class declarations;
7. script, evaluator, and environment identities where they affect interpretation;
8. hashes or integrity markers for claim-bearing artifacts;
9. structured confound records;
10. validation outputs that attest the evidence package was formed as declared; and
11. append-only change history for prompt, render, and contract-bearing surfaces.

The common thread is that these are all difficult, lossy, or credibility-damaging to reconstruct after the fact.

## 6. Evidence Failures A Future Specification May Need To Treat As Interpretation-Limiting

A future specification would likely need to say more explicitly which evidence failures block later interpretation and which merely force stronger qualification or downgrade.

This does **not** mean every incomplete artifact must be deleted. It suggests that certain evidence failures would likely need to block comparative, explanatory, or mechanism-oriented interpretation, even if the artifact is retained for archival or descriptive reference.

Possible examples of failures a future specification may choose to codify include:

1. missing exact rendered prompts when prompt construction materially affects interpretation;
2. missing or ambiguous row provenance for claim-bearing examples;
3. inability to map summary scores back to underlying row-level outputs;
4. unknown or drifting dataset, prompt, scorer, or contract version identity;
5. missing fixed-surface, varying-surface, or comparison-class declarations;
6. missing raw outputs behind reported behavioral claims;
7. runtime claims made without preserved runtime evidence;
8. mechanistic or explanatory claims made without structured confound capture;
9. post-hoc repair, substitution, or inferred reconstruction of evidence that should have been captured at source;
10. mixing behavioral, governance, provenance, and continuity evidence without explicit role separation; and
11. missing validation evidence when the evidence-creation path itself is part of the reproducibility boundary.

A future specification may also need to distinguish:

- failures that block all meaningful interpretation;
- failures that force downgrade to descriptive-only interpretation; and
- failures that merely require stronger qualification.

That tiering would belong inside the specification itself, not in this assessment.

## 7. Relationship To The Existing Gen-2 Charter

The prospective specification is best understood as a methodological companion to the Gen-2 charter, not a replacement for it.

The charter currently defines:

- Gen-2 identity;
- scope boundaries;
- non-goals;
- success criteria;
- non-negotiable principles; and
- high-level evidence and observability doctrine.

The future evidence-and-observability specification would likely address:

- which evidence categories it would likely treat as mandatory;
- which metadata it would likely elevate to first-class evidence;
- which surfaces it would likely expect at creation time;
- which admissibility failures it would likely treat as interpretation-limiting; and
- how claim-bearing evidence packages could remain inspectable and comparable.

Its likely role is therefore subordinate and translational:

- the charter states the governing scientific posture;
- the prospective specification operationalizes the evidence discipline required by that posture; and
- any future study-specific artifact would remain below both, if later separately authorized.

It would strengthen the charter's methodology, not reinterpret the charter's governance or authority order.

## 8. Relationship To Existing Methodological Surfaces

If such a specification were ever authored, it would need to integrate with existing methodological surfaces rather than create a parallel methodology stack.

In particular:

- the frozen canonical evaluation contract would remain the repository's pinned measurement surface; a future evidence-and-observability specification would likely complement it by clarifying what evidence must accompany claims made under that contract, not by replacing or reinterpreting the contract itself;
- the D1 inventory and its specification would remain the closest current model for typed evidence roles, structured confounds, and explicit claim support; a future specification would likely extend that discipline horizontally rather than invent an unrelated evidence language;
- the process-infrastructure checklists would remain responsible for hygiene, review, and publication-process discipline; a future specification would likely address scientific admissibility of evidence rather than generic repository process mechanics; and
- the Gen-2 charter would remain the controlling identity and boundary document; a future specification would translate and consolidate the charter's evidence and observability doctrine into a more reusable methodological surface.

The goal would be integration and consolidation across existing surfaces, not the creation of a competing doctrine, checklist family, or standalone operational framework.

Publication of this assessment would not commit the repository to authoring the future specification, nor would it commit the repository to any particular section set, evidence schema, or admissibility rule. It records only that such a methodological layer appears worth considering.

## 9. How Such A Specification Would Avoid Becoming Experiment Design Or D2 Planning

Such a specification would become out-of-bounds if it started choosing interventions rather than defining evidence discipline.

To avoid that drift, it would likely need to:

1. define evidence classes, not treatment arms;
2. define admissibility requirements, not run sequences;
3. define capture obligations, not execution recommendations;
4. define claim-tier and confound requirements, not study hypotheses to be tested next;
5. define comparison-surface declarations as generic requirements, not named study surfaces for a particular future run;
6. avoid target metrics, success thresholds, or optimization language;
7. avoid model-family selection, dataset redesign direction, or intervention prioritization; and
8. state explicitly that possession of a specification is not execution authority.

The right question for the specification would be:

"What evidence would have to exist before later interpretation is scientifically admissible?"

The wrong question would be:

"What should the next Gen-2 study do?"

## 10. Illustrative Structure A Future Specification Might Take

If such a specification were later authored, one plausible structure might include sections such as:

1. Scope and non-authorizations.
2. Relationship to the Gen-2 charter and existing doctrine.
3. Claim types and interpretation tiers.
4. Evidence-role taxonomy.
5. Mandatory evidence categories.
6. First-class metadata requirements.
7. Creation-time capture requirements.
8. Claim-conditional observability requirements.
9. Admissibility failures, downgrade rules, and invalidation conditions.
10. Validation, integrity, and append-only history requirements.
11. Evidence separation rules across behavioral, governance, provenance, contract, and continuity surfaces.
12. Explicit non-goals and boundary confirmation.

That kind of outline would help keep the document methodological, reusable, and clearly distinct from study design, but this assessment does not commit the repository to that exact structure.

## 11. Likely Role Inside Gen-2

Based on the current charter and published Gen-2 framing, the eventual existence of such a specification is most plausibly understood as:

- a likely prerequisite for scientifically serious future execution, not a substitute for authorization;
- a reusable observability-and-evidence doctrine layer beneath the charter;
- a prevention mechanism against Stage C and D0-style observability failures recurring; and
- an admissibility filter that forces future work to preserve uncertainty boundaries rather than repairing them narratively later.

The specification therefore appears to be a plausible foundational Gen-2 methodological asset, even though this assessment does not author it and does not authorize any later execution.

## Boundary Confirmation

This assessment is documentation-only.

It does not authorize:

- D2 planning or D2 execution;
- experiment design;
- treatment-arm design;
- run planning;
- manifests;
- preregistrations;
- training or evaluation execution; or
- governance reinterpretation.
