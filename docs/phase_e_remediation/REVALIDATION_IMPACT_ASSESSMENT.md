# Revalidation Impact Assessment

## Questions

- Are the Phase E results still usable?
- Would rerunning them under the previous evaluator likely change conclusions?
- Is there evidence of scoring drift?

## Evidence

### Base revalidation

- The base rerun reproduces the old run at the classification level.
- Classification diff count against the older run: `0`.
- Aggregate metrics remain unchanged.

### Adapter revalidation

- The adapter rerun shifts four `heldout_validation` rows:
  - row `56`, case `p0_read_file_2`
  - row `69`, case `p1_run_command_1`
  - row `87`, case `p0_rg_search_3`
  - row `114`, case `p0_read_file_2`
- The differences are between `invalid_json` and `invalid_schema`, driven by different generated texts.
- Aggregate metrics remain stable aside from a one-row swap between the two adjacent error buckets:
  - `invalid_json`: `55` -> `56`
  - `invalid_schema`: `80` -> `79`
- The Phase E gate outcomes do not change:
  - exact JSON validity improvement target fails
  - tool-name improvement target fails
  - invalid JSON decrease passes
  - wrapper leakage passes
  - no-call correctness passes

## Assessment

- Are the Phase E results still usable? Yes.
- Would rerunning them under the previous evaluator likely change conclusions? No.
- Is there evidence of scoring drift? No evidence of canonical scoring drift.

## Caveat

The adapter rerun is not bitwise identical at the row-output level, so a few rows move between adjacent failure buckets.
That variance does not change the Phase E conclusion.
