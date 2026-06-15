# D0 Provenance Blocker Governance Options

## Scope

This package evaluates governance responses to the unresolved canonical `training_script_sha256` claim for `scripts/train_lora_sft.py`.

Current facts:

- the canonical hash claim is published in `evals/canonical_eval_manifest_v1.json`;
- the current live script hash differs from the claim;
- no reachable git blob for `scripts/train_lora_sft.py` reproduces the canonical hash; and
- D0 remains blocked until the provenance gap is resolved by an authoritative source or a later governance re-scope.

## Options

| Option | Scientific impact | Reproducibility impact | Publication impact | Implementation cost | Risk level |
|---|---|---|---|---|---|
| 1. Strict resolution required before certification | Strongest. Preserves causal attribution and keeps the certification question tied to the published canonical bytes. | Strongest. Certification only proceeds when the claimed bytes are reproducible from an authoritative source. | Strong. The publication record remains internally consistent and does not rewrite the manifest to fit the current tree. | Low to medium. Requires continued provenance work, but no reconstruction or authority relaxation. | Low |
| 2. External archive / publication bundle search | Strong positive if successful. Can recover the canonical bytes without changing the published claim. | High if successful. Provides a byte-preserving source outside the live tree. | Positive if a preserved bundle is found. Neutral if no artifact is located. | Medium. Requires targeted archival validation and source reconciliation. | Low to medium |
| 3. Current-tree reconstruction certification path | Weakens historical comparability. Shifts the question from canonical fidelity to current-tree equivalence. | Medium for current-tree reproducibility, low for reproducing the published canonical claim. | Mixed to negative unless the scope is explicitly redefined in governance. | Medium to high. Requires new authority surfaces and explicit re-labeling. | High |
| 4. Dual-track certification (historical and current-tree) | Scientifically usable only with strict labeling, but it risks conflating two different reference regimes. | Split. Reproducibility is possible per track, but audit interpretation becomes more complex. | Fragile. Readers can misread the canonical and current-tree results as interchangeable. | High. Adds parallel ledgers, reports, and review burden. | High |
| 5. Permanent documented exception | Weakest. Accepts unresolved provenance as a standing condition. | Poor. The canonical claim remains untestable against preserved bytes. | Negative. Undermines the authority of the published manifest and future citations. | Low to implement, high to govern. | Very high |

## Governance Notes

- Option 2 is an evidence-discovery path, not a certification mode.
- Option 3 and Option 4 require an explicit authority change before they can be treated as valid D0 scope.
- Option 5 should not be used to bypass the blocker.
