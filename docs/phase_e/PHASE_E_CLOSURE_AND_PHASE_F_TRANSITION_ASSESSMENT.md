# Phase E Closure And Phase F Transition Assessment

## Executive Summary

Phase E accomplished the core evidence-generation goal.
The canonical base model and the i3 restart adapter were both freshly revalidated against the frozen canonical manifest, and the resulting baseline deltas are now captured from fresh runs rather than historical memory.

The main caveat is contract drift: the manifest still pins an older scorer hash than the current evaluator script hash.
That means the baseline is operationally revalidated, but the contract is not strictly hash-stable without remediation.

## Environment Verification Results

- Branch: `main`
- HEAD: `325bdb4a38286180cf5c6d7ab36fa2ed642a2178`
- origin alignment: `HEAD == origin/main`
- Canonical model path: present and accessible
- i3 adapter path: present and accessible
- Canonical datasets: present and hash-matched
- Working tree: not clean because of the local untracked work-package files and Phase D/Phase E bundle directories

## Contract Verification Results

- Manifest integrity: pass
- Split integrity: pass
- Decode defaults: pass
- Dataset references: pass
- Model references: pass
- Scorer references: fail with caveat

The scorer-hash pin in the manifest is stale relative to the current evaluator script hash.

## Base Model Results

- Fresh base revalidation completed successfully.
- Exact JSON validity: 0.0
- Invalid JSON rate: 0.7
- Tool-name accuracy: 0.0
- Argument accuracy: 0.0
- Wrapper leakage rate: 0.0
- No-call correctness: 1.0
- Dominant failures: direct-answer substitution and malformed partial JSON

## i3 Results

- Fresh i3 adapter revalidation completed successfully.
- Exact JSON validity: 0.025
- Invalid JSON rate: 0.28
- Tool-name accuracy: 0.03571428571428571
- Argument accuracy: 0.03571428571428571
- Wrapper leakage rate: 0.0
- No-call correctness: 1.0
- Dominant failures: direct-answer substitution, scalar substitution, and near-canonical wrapper or envelope drift

## Baseline Delta Results

- Exact JSON validity: +0.025
- Invalid JSON rate: -0.42
- Tool-name accuracy: +0.03571428571428571
- Argument accuracy: +0.03571428571428571
- Wrapper leakage rate: 0.0
- No-call correctness: 0.0

Appendix A gate comparison:

- exact validity improvement target: fail
- tool-name improvement target: fail
- invalid JSON decrease: pass
- wrapper leakage: pass
- no-call correctness: pass

## Risks

- Scorer hash drift means the manifest pin is no longer strictly aligned with the current evaluator script.
- The working tree is not in a clean handoff state.
- The i3 adapter remains below the minimum-promising thresholds.
- The dataset family remains narrow in provenance diversity.

## Recommended Next Action

Perform remediation before launching any new training path.
The remediation should focus on contract hygiene and a clean handoff state, not on changing scoring semantics.

## Phase F Recommendation

**Option C: perform remediation before either Dataset v1.x expansion or Stage A training.**

## Go / No-Go Determination

- Go for closing Phase E as an evidence-generation phase
- No-go for moving directly into new training work from the current repository state
- Go only after the contract-drift and handoff-state caveats are addressed

## Boundary Confirmation

This assessment does not authorize new training or manifest changes.
