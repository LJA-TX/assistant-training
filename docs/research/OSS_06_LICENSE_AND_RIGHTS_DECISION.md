# OSS_06_LICENSE_AND_RIGHTS_DECISION

Assessment only. No repository changes were made. This is a rights-posture assessment, not legal advice.

## 1. Executive Summary

Apache-2.0 remains the leading license candidate for the public, curated repository, but only for the first-party material that is actually intended to be published. The mixed-provenance families identified in OSS-03 / OSS-03A still make a blanket “everything in the canonical repo is Apache-2.0 public material” posture too broad.

Current state checks support that conclusion:

- No `LICENSE`, `NOTICE`, or `COPYING` files are present in the tree.
- A local scan found no obvious third-party copyright or license headers in the primary text files I sampled.
- `data/README.md` explicitly says the canonical input datasets live in an external source of truth under `assistant-runtime`.
- `data/v1_0/dataset_v1_0_summary.json` records external runtime dataset files as inputs and pins evaluation splits derived from them.
- `evals/canonical_eval_manifest_v1.json` is first-party contract metadata, but it references external runtime and environment paths, so it still deserves file-level review before public publication.

Bottom line:

- Code, tests, and the authored documentation layers are broadly licensable under Apache-2.0.
- Training datasets, evaluation datasets, reports, and generated artifacts should remain unpublished by default.
- The curated/public repository becomes easier to license cleanly because it excludes the rights-heavy data/report surfaces.
- Apache-2.0 still fits the project’s public-inspection and reuse goals well.

## 2. Asset-Class Rights Assessment

| Asset class | Rights classification | Rationale |
|---|---|---|
| Source code | Clearly licensable | Maintainer-authored implementation; no obvious vendored third-party source or notice headers were found in the sampled text scan. |
| Tests | Clearly licensable | Repository-specific validation code with the same authorship posture as the code. |
| Documentation | Likely licensable | Mostly original prose, but the umbrella includes subfamilies that should still be reviewed file-by-file before publication. |
| Framework documents | Clearly licensable | Authoritative doctrine and methodology docs appear to be original repository-authored material. |
| Current-state documents | Clearly licensable | Current-state and orientation docs are original and maintainership-defined. |
| Continuity documents | Clearly licensable | Compact handoff snapshots, original narrative, no obvious third-party material detected. |
| Convergence documents | Likely licensable | Mostly original closure/history records, but the family is large and some items merit file-level review before public inclusion. |
| Housekeeping documents | Likely licensable | Governance/preservation docs are original, but some are review or preservation artifacts and should still be checked at file level if published. |
| Research documents | Needs review | Exploratory and provenance-sensitive; some items summarize external datasets or publication-architecture research and should not be assumed blanket-safe. |
| Evaluation manifests | Likely licensable | First-party contract/metadata artifacts, but they reference external runtime paths and should be reviewed before public release. |
| Training datasets | Should remain unpublished | Mixed provenance and external source-of-truth inputs; rights are not fully closed for public distribution. |
| Evaluation datasets | Should remain unpublished | Mixed provenance and derivative holdout construction; public release would need separate rights clearance. |
| Reports | Should remain unpublished | Derived summaries/output records; high provenance and publication burden. |
| Generated artifacts | Should remain unpublished | Operational outputs, logs, and artifact bundles are not appropriate for public publication by default. |

## 3. Apache-2.0 Reassessment

### Suitability
Yes. Apache-2.0 still fits the project’s intended public posture well.

### Advantages
- Permissive and well understood.
- Supports source code and documentation clearly.
- Includes a patent grant, which is useful for a technical methodology repo.
- Compatible with public inspection and downstream reuse.
- Fits a curated/public repository that is intentionally selective.

### Disadvantages
- It does not solve provenance problems for mixed-provenance data or generated artifacts.
- It can create a false impression that every tracked artifact is equally safe to publish unless the package boundary is explicit.
- If any retained third-party notice-bearing material exists, `NOTICE` handling has to be done carefully.

### Compatibility with project goals
Strong fit:
- the project wants public inspection, not community development;
- the core public value is the regimen itself;
- permissive licensing supports research and reuse without adding contributor-governance complexity.

### Compatibility with public inspection posture
Strong fit:
- Apache-2.0 makes the curated repository easy to inspect and reuse;
- the curated boundary can exclude the rights-heavy families, which improves clarity.

### Compatibility with future reuse
Strong fit:
- the code, tests, and authored docs are straightforward for future reuse under Apache-2.0;
- the data/report/archive surfaces remain separate and do not need to be forced into the same license posture.

### Recommendation
Apache-2.0 remains the recommended license candidate for the curated/public repository and the first-party materials that are intended for public release.

## 4. Rights Boundary Assessment

### Assets that can reasonably be represented as first-party
- Source code
- Tests
- Most authored documentation
- Framework documents
- Current-state documents
- Continuity documents
- Most convergence history documents
- Most housekeeping/governance documents
- Evaluation manifest metadata

### Assets that are mixed provenance
- Training datasets
- Evaluation datasets
- Reports
- Generated artifacts
- `data/v1_0/` and similar lineage datasets
- `evals/data/`
- `manifests/runs/`
- `manifests/reports/`
- environment snapshots and other execution records
- some research documents that discuss or summarize external datasets, papers, or acquisition strategy
- any artifact that preserves model outputs or imported external material

### Assets that create uncertainty
- `data/README.md` points to external runtime-owned source datasets.
- `data/v1_0/dataset_v1_0_summary.json` shows that the local dataset is assembled from external runtime dataset files plus local sources.
- `evals/canonical_eval_manifest_v1.json` references external runtime paths, which is fine as metadata but still requires file-level review before public release.
- Any file containing verbatim external excerpts, copied snippets, or imported review text should be checked individually before publication.

### Prior provenance concerns, explicitly
The earlier provenance assessments still stand:
- the dataset family is mixed;
- derived evaluation and report surfaces are not clean enough to assume blanket public publication rights;
- the public repo should omit those families unless separate rights clearance exists.

## 5. Publication Readiness Gate

Before `assistant-training` becomes publicly visible, the following minimum conditions should be satisfied:

1. The public-included files are either first-party or explicitly cleared for publication.
2. Apache-2.0 is adopted for the public package’s first-party code/docs.
3. Any retained third-party attribution material is accounted for in `NOTICE` if needed.
4. Mixed-provenance families stay excluded from the public package unless separately cleared.
5. The curated/public boundary is explicit enough that no one can reasonably assume datasets, reports, or generated artifacts are covered by default public distribution rights.
6. No unresolved file-level rights questions remain for the files that will actually be published.

Practical interpretation:
- the curated/public repository can be prepared before final license adoption,
- but external visibility should wait until rights are clear for the included files.

## 6. Curated Repository Assessment

The curated/public repository improves the licensing posture rather than complicating it.

Why:
- it lets you publish only the first-party code, tests, docs, evaluation contract, and a bounded historical evidence layer;
- it avoids the rights-heavy dataset/report/archive families entirely;
- it makes an Apache-2.0 package realistic and clean.

Implications for the public categories:

- **Public Core**: mostly first-party code/docs; straightforward Apache-2.0 coverage.
- **Public Supporting**: same general posture; low extra rights risk if kept lightweight.
- **Curated Historical Evidence**: mostly original history docs, but any item containing external excerpts or model-generated review content should receive file-level rights review before inclusion.

Net effect:
- the curated/public repository does not broaden rights uncertainty;
- it narrows it.

## 7. Risk Assessment

| Risk | Why it matters | Mitigation |
|---|---|---|
| License mismatch | Public package could imply broader rights than intended | Keep one rights policy and derive curated/public from canonical-approved material |
| Provenance uncertainty | Datasets and derived artifacts are mixed provenance | Exclude them from the public package unless separately cleared |
| Third-party material | Any copied or quoted material can create publication risk | File-level review for research/history docs that quote or embed outside material |
| Dataset contamination | Publicly publishing mixed-provenance corpora can misrepresent rights status | Keep training and evaluation datasets canonical-only by default |
| Publication misrepresentation | Readers may assume all tracked files are equally licensed | Add explicit publication disclosures about excluded families |
| Future contributor confusion | Curated/public could be mistaken for a full mirror | State clearly that the public repo is selective and derived |
| NOTICE omission | Retained attribution notices could be mishandled | Include `NOTICE` only if required by retained attribution material |
| Rights drift | Public package might expand without re-review | Require rights review for any curated boundary change |

## 8. Recommended License Package

Policy-level recommendation:

- `LICENSE`: Apache-2.0, as the default license for the curated/public repository’s first-party code and docs.
- `NOTICE`: only if retained attribution notices or third-party notices need to be preserved in the distributed public package.
- Attribution guidance: a short publication note in the public README explaining that the curated repo is a selective derivative of the canonical/private repo, and clarifying which families remain canonical-only.
- Publication disclosures: explicitly state that training datasets, evaluation datasets, reports, generated artifacts, and most run/archive surfaces remain canonical-only unless separately cleared.

Optional but sensible:
- short per-file Apache headers for new source files and docs in the public repo, if you want consistency with common Apache practice.

## 9. Final Recommendation

Apache-2.0 remains the recommended license candidate for the curated/public repository and the first-party materials intended for public release.

Do not publish the public repository until the rights gate is complete for the included files.

In practice:
- publish code, tests, and authored docs under Apache-2.0;
- keep mixed-provenance datasets, reports, and generated artifacts out of the public package by default;
- use `NOTICE` only if retained attribution material requires it;
- make the curated/public boundary explicit so the license does not get misread as covering everything in the canonical/private repository.

## Sources Used

Local repository evidence:
- [README.md](/opt/ai-stack/assistant-training/README.md)
- [docs/goal_charter_v5a.md](/opt/ai-stack/assistant-training/docs/goal_charter_v5a.md)
- [docs/appendix_a_operational_execution_contract_v3a.md](/opt/ai-stack/assistant-training/docs/appendix_a_operational_execution_contract_v3a.md)
- [docs/metric_specification_v1a.md](/opt/ai-stack/assistant-training/docs/metric_specification_v1a.md)
- [data/README.md](/opt/ai-stack/assistant-training/data/README.md)
- [data/v1_0/dataset_v1_0_summary.json](/opt/ai-stack/assistant-training/data/v1_0/dataset_v1_0_summary.json)
- [evals/canonical_eval_manifest_v1.json](/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json)

Official Apache sources:
- https://www.apache.org/licenses/LICENSE-2.0.html
- https://www.apache.org/legal/apply-license

No `LICENSE`, `NOTICE`, or `COPYING` files were present in the repository scan.
