# Dataset Risk Assessment

## Risk Summary

The biggest practical risk is not raw dataset size. It is style drift and benchmark contamination if the wrong families are used too heavily or without filtering. The second biggest risk is overfitting to a narrow tool-positive pattern instead of broadening tool-call competence.

## Risk Table

| Candidate | Data Contamination Risk | Schema Mismatch Risk | Quality Risk | Licensing Risk | Behavioral Regression Risk | Overfitting Risk |
|---|---|---|---|---|---|---|
| xLAM / APIGen | Low to medium | Low to medium | Low | Low | Low | Low to medium |
| APIGen-MT | Medium | Medium | Low to medium | Medium to high | Medium | Medium |
| ToolACE | Medium | Medium | Medium | Low | Medium | Medium |
| Glaive function-calling v2 | Medium | Medium to high | Medium | Low | Medium to high | Medium |
| BFCL-related public datasets | High if used for training | Medium | Low as benchmark, high as training input | Low | High | High |
| When2Call | Medium | Medium | Low to medium | Low | Low to medium | Medium |
| ToolBench | Medium to high | Medium to high | High | Low | High | Medium |

## Candidate Notes

### xLAM / APIGen

- Best quality signals in the survey reduce data quality risk.
- The main work is canonicalization into the runtime schema and keeping benchmark overlap controlled.

### APIGen-MT

- The NC license is the main external constraint.
- The small corpus size means it should be used as a targeted supplement, not a dominant source.

### ToolACE

- Good candidate, but it is more synthetic and agentic than the current runtime profile.
- Use filtered subsets and check for wrapper/prose drift.

### Glaive function-calling v2

- Broad, but provenance detail is thinner.
- The risk is less about license and more about style quality and schema compatibility.

### BFCL-related public datasets

- Training on benchmark assets is a contamination problem first and a data problem second.
- Use for eval or diagnostics, not for the training corpus.

### When2Call

- Excellent for preserving no-call behavior.
- Risk is mainly that it does not solve the tool-argument problem by itself.

### ToolBench

- The legacy breadth is attractive, but the style is old and more conversational.
- If used, it should be heavily filtered and down-weighted.

## Mitigations

- Canonicalize all external tool-call examples into the assistant-runtime schema before ingestion.
- Keep benchmark assets out of the training corpus.
- Preserve the current no-call and refusal ratios unless validation proves a different balance is better.
- Add a leakage check for any external family that might overlap with evaluation assets.
- Prefer high-verification sources first and legacy synthetic corpora last.
## Sources Used

- `EXTERNAL_DATASET_SURVEY.md`
- `docs/appendix_a_operational_execution_contract_v3a.md`
- `data/v1_0/dataset_v1_0_leakage_report.json`
