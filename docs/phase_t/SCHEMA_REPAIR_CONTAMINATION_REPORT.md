# Schema Repair Contamination Report

## Scope

The patch was checked against the frozen canonical evaluation assets listed in `evals/canonical_eval_manifest_v1.json`:

- `heldout_validation`
- `tool_holdout`
- `no_call`
- `adversarial`
- `direct_answer`

## Validation Method

The patch rows were compared against each frozen split on three exact-match surfaces:

- prompt text;
- assistant target text;
- source case ID.

## Results

| Frozen split | Prompt overlap | Target overlap | Source-case overlap |
|---|---:|---:|---:|
| `heldout_validation` | 0 | 0 | 0 |
| `tool_holdout` | 0 | 0 | 0 |
| `no_call` | 0 | 0 | 0 |
| `adversarial` | 0 | 0 | 0 |
| `direct_answer` | 0 | 0 | 0 |

## Determination

Contamination status is clean.

No overlap was detected with any frozen evaluation split on any of the checked surfaces.

## Notes

The patch uses phase-specific prompts, phase-specific case IDs, and phase-specific target shapes so it stays disjoint from the frozen canonical evaluation contract.

