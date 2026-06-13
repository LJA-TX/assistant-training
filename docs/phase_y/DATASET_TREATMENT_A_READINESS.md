# Dataset Treatment A Readiness

## Determination

Ready and scientifically admissible.

## Evidence

- Train rows: `2160`
- Validation rows: `240`
- Tool-positive rows: `1393`
- Safety rows: `767`
- Anchor rows: `819` against a target of `819`
- Long-tail rows: `574`
- Exact tool-request cue retained: `true`
- Canonical `tool_calls` envelope valid: `true`
- Frozen scaffold preserved in train and validation: `true`
- All tool families represented: `true`
- Contamination zero across heldout validation, tool holdout, no-call, adversarial, and direct-answer splits: `true`

Treatment A preserves the frozen scaffold and safety block while increasing anchor concentration to the approved intermediate level.

## Readiness Conclusion

Treatment A is ready for governed execution under the existing Phase L framework.
