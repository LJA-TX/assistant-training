# Behavioral Gap Mapping

## Phase E Weakness Baseline

The Phase E evidence showed the following held-out behavior profile:

- exact JSON validity: `0.025`
- invalid JSON rate: `0.28`
- tool-name accuracy: `0.03571428571428571`
- argument accuracy: `0.03571428571428571`
- wrapper leakage: `0.0`
- no-call correctness: `1.0`

The dominant gap is therefore not no-call discipline. The dominant gap is tool-call specificity: the model needs broader canonical tool coverage, better argument synthesis, and more variation in tool-positive examples.

## Candidate Impact Map

| Candidate | Exact JSON Validity | Tool-Name Accuracy | Argument Accuracy | Wrapper Leakage | No-Call Correctness | Runtime Alignment |
|---|---|---|---|---|---|---|
| xLAM / APIGen | Likely improves | Likely improves strongly | Likely improves strongly | Likely neutral to slightly better after filtering | Likely neutral to slightly worse if over-weighted | Likely improves moderately |
| APIGen-MT | Likely improves | Likely improves | Likely improves | Likely neutral to slightly worse if not filtered | Likely improves or stays stable | Likely improves |
| ToolACE | Likely improves | Likely improves | Likely improves | Unknown to slightly worse if agentic traces are preserved | Likely neutral | Likely improves moderately |
| Glaive function-calling v2 | Likely improves | Likely improves modestly | Likely improves modestly | Risk of regression from prose-heavy style | Likely neutral to slightly worse | Likely neutral |
| BFCL-related public datasets | No meaningful training impact recommended | No meaningful training impact recommended | No meaningful training impact recommended | No meaningful training impact recommended | No meaningful training impact recommended | No meaningful training impact recommended |
| When2Call | Likely improves slightly | Limited direct impact | Limited direct impact | Likely neutral | Likely improves strongly | Likely improves strongly |
| ToolBench | Likely improves modestly | Likely improves modestly | Likely improves modestly | Higher regression risk | Likely worse if over-used | Likely weak or mixed |

## Detailed Mapping

### xLAM / APIGen

- Best fit for exact JSON validity, tool-name accuracy, and argument accuracy.
- The verification pipeline gives it the strongest chance of improving canonical tool-call quality without importing a lot of garbage.
- Unknown: how much of the improvement survives runtime-schema canonicalization and the current task distribution.

### APIGen-MT

- Best fit for multi-turn argument synthesis and follow-up behavior.
- Should help more with contextual argument selection than with plain format learning.
- Unknown: whether the smaller NC corpus is enough to move the held-out metrics materially.

### ToolACE

- Likely useful for tool breadth and more complex tool routing.
- Because it is more agentic, it may help selection accuracy while being less direct on strict schema discipline.
- Unknown: whether the generated style introduces wrapper leakage under our runtime prompt contract.

### Glaive function-calling v2

- Likely to help because it gives additional function-call examples at scale.
- The main concern is that provenance is thin, so style drift and low-signal examples are harder to exclude.
- Unknown: the degree to which the corpus is already close to the runtime schema.

### BFCL-related public datasets

- These are more useful as evaluation guardrails than as training inputs.
- Using them for training would not address the current gaps and would create contamination concerns.

### When2Call

- The clearest family for preserving and reinforcing no-call correctness.
- Strongly aligned with runtime restraint, clarifying questions, and admitting limits.
- Likely to help runtime alignment more than tool-argument detail.

### ToolBench

- Could improve generic tool-use exposure, but it is the most likely to regress wrapper leakage and conversational padding.
- It is too old and too broad to be a preferred primary fix for the current profile.

## Interpretation

- The current dataset needs more tool-positive diversity, not less no-call coverage.
- The best augmentation path is to widen tool-call examples without disturbing the strong no-call and refusal behavior.
- The current metrics suggest that runtime alignment is already working; the main leverage now is on canonical tool-call variety and argument grounding.

## Sources Used

- `docs/phase_e/PHASE_E_CLOSURE_AND_PHASE_F_TRANSITION_ASSESSMENT.md`
- `docs/phase_e_remediation/EVALUATOR_CONTRACT_DRIFT_FINAL_DETERMINATION.md`
- `CURRENT_DATASET_ASSESSMENT.md`
- `EXTERNAL_DATASET_SURVEY.md`
