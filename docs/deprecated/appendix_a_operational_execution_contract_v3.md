# Appendix A — Operational Execution Contract (v3)

This appendix supplements the main `/goal` charter.

The charter defines:
- mission
- authority
- philosophy
- safety doctrine
- high-level success criteria

This appendix defines:
- frozen evaluation contracts
- dataset composition rules
- promotion gates
- operational limits
- reproducibility requirements
- stopping conditions

If this appendix conflicts with the main charter, the stricter safety/runtime interpretation applies.

---

# 1. Runtime Contract Pinning

Codex must pin runtime semantics before serious training/eval begins.

Required pinned artifacts:
- assistant-runtime git commit
- tool schema version
- eval schema version
- dataset manifest version
- tokenizer version
- training-script version
- eval-script version
- dependency lock snapshot
- training seed(s)
- CUDA version
- torch version
- transformers version
- PEFT version
- container/image digest if applicable

Pinned references must be recorded in:
- run manifests
- eval summaries
- dataset manifests

Codex must not silently change:
- tool schemas
- canonical argument structure
- eval semantics
- prompt serialization semantics
- scoring semantics

mid-cycle.

If runtime semantics must change:
- create a new evaluation generation/version;
- preserve prior evaluation comparability where practical.

---

# 2. Frozen Evaluation Contract

All serious runs must evaluate against a fixed baseline suite.

## 2.1 Canonical Eval Manifest

Canonical evaluation must use a single pinned manifest artifact.

Canonical location:
- `/opt/ai-stack/assistant-training/evals/canonical_eval_manifest_v1.json`

The manifest must pin:
- dataset paths
- dataset hashes
- split hashes
- scorer script paths
- scorer hashes
- decode parameters
- prompt serialization contract
- tokenizer version
- evaluation order
- random seed(s)

Cross-run comparability must use the same manifest version unless a new evaluation generation is explicitly created.

## 2.2 Canonical Eval Assets

Canonical evaluation categories:
- held-out validation split
- all-tool holdout split
- no-call/policy split
- adversarial malformed-request split
- direct-answer/non-tool split

## 2.3 Frozen Decode Defaults

Unless explicitly testing decode robustness:

- temperature: `0.0`
- top_p: `1.0`
- do_sample: `false`
- repetition_penalty: `1.0`
- max_new_tokens: fixed per eval suite
- seed: fixed and recorded

Any deviation must be recorded.

## 2.4 Frozen Prompt Contract

Default evaluation prompt serialization:
- tokenizer-native chat template
- `add_generation_prompt=true`
- no hidden reasoning scaffolds
- no eval-only prompt hacks unless explicitly documented

Strong-system overrides may be used only for:
- diagnostics
- ablation studies
- failure analysis

not for canonical promotion scoring.

---

# 3. Dataset Composition Rules

Dataset composition must remain behaviorally balanced.

## 3.1 Canonical Composition Targets

Default normalized composition target:

- 45% tool-call positives
- 25% runtime behavioral alignment
- 15% no-call/direct-answer behavior
- 10% refusal/policy/safety behavior
- 5% adversarial/error/malformed-request behavior

Preferred tolerance:
- ±5 absolute percentage points per category

Total dataset composition should normalize to approximately 100%.

## 3.2 Synthetic Data Constraints

Synthetic/paraphrased content:
- preferred: `<50%`
- hard ceiling: `70%`

Pure paraphrase inflation is prohibited.

Codex must favor:
- semantic diversity
- tool diversity
- argument diversity
- phrasing diversity

over raw row count.

High-quality synthetic runtime-alignment generation is authorized when:
- natural data is insufficient
- behavioral goals are explicit
- outputs are reviewed through eval and contamination controls

---

# 4. Dataset Deduplication and Leakage Rules

Before serious training:
- deduplicate prompts
- deduplicate assistant targets
- deduplicate canonicalized tool calls
- deduplicate near-identical paraphrases where practical

Required leakage checks:
- train/val overlap
- train/eval overlap
- canonical target overlap
- source_case_id overlap
- tool-family holdout integrity
- semantic-cluster holdout integrity where practical

Required isolation goals:
- preserve tool-family holdouts whenever feasible
- preserve semantic-task holdouts whenever feasible

Evaluation contamination is a serious failure.

Contaminated evaluation suites:
- must be regenerated
- versioned
- documented

---

# 5. Definition of a Serious Run

A run is considered “serious” if it:
- performs actual gradient updates
- produces adapter artifacts
- consumes nontrivial compute
- or is intended for comparison/promotion

A serious run must include:
- config
- manifest/run record
- dataset manifest/version
- masking audit
- training summary
- evaluation summary
- runtime/schema pinning metadata

Minimum serious-run expectations:
- complete canonical eval suite
- recorded hyperparameters
- recorded dataset composition summary
- reproducible launch command
- recorded seeds/environment versions

Tiny exploratory runs may be excluded from promotion consideration.

---

# 6. Numeric Promotion Gates

Promotion gates are binding unless explicitly escalated for human review.

All gate deltas use absolute percentage-point deltas unless otherwise documented.

## 6.1 Minimum Promising Threshold

Compared against canonical base baseline:

Required:
- exact JSON validity improvement
- lower invalid_json rate
- nonzero held-out tool-name accuracy
- no catastrophic no-call regression
- no major unsafe/tool-happy regression

Default minimum thresholds:
- ≥10 absolute percentage-point exact JSON validity improvement on held-out eval
- ≥5 absolute percentage-point held-out tool-name accuracy
- wrapper leakage not worse than base by >5 absolute percentage points
- no-call correctness not degraded by >10 absolute percentage points

Failure to meet thresholds:
- blocks autonomous promotion
- requires explicit escalation or additional experimentation

## 6.2 Strong Candidate Threshold

Suggested strong-candidate thresholds:
- ≥50% exact JSON validity
- ≥35% tool-name accuracy
- ≥25% argument accuracy
- low wrapper leakage
- stable no-call behavior
- acceptable adversarial/policy behavior

Improvement in structured runtime behavior takes precedence over conversational fluency or socially optimized assistant behavior.

## 6.3 Minimum Evaluation Floor

No checkpoint may be autonomously promoted using fewer than:
- 100 canonical evaluation rows total
- 20 no-call evaluation rows
- 20 held-out tool-call rows

unless explicitly escalated for human review.

## 6.4 Exception Protocol

Codex may recommend promotion despite gate failure only if:
- broader behavioral evidence strongly supports advancement
- the exception is explicitly documented
- the rationale is preserved in promotion artifacts
- human review is requested

Autonomous self-override without documentation is prohibited.

---

# 7. Metric Definitions

Detailed metric formulas and scorer semantics must be defined in canonical evaluation specifications referenced by the eval manifest.

## 7.1 Exact JSON Validity

A response is exact-valid only if:
- valid parseable JSON
- canonical schema-compliant
- no extraneous wrapper/prose content
- no malformed structure

## 7.2 Tool-Name Accuracy

Correct iff:
- emitted tool name exactly matches canonical expected tool

## 7.3 Argument Accuracy

Correct iff:
- canonicalized emitted arguments semantically match expected arguments

Minor ordering differences:
- ignored where semantically equivalent

## 7.4 Wrapper Leakage

Wrapper leakage occurs if:
- prose
- markdown
- shell-command framing
- conversational wrappers
- non-schema text

surround or contaminate canonical tool-call output.

## 7.5 No-Call Correctness

Correct iff:
- the model appropriately avoids tool usage when canonical behavior requires direct-answer/refusal/no-call behavior.

---

# 8. Safety Evaluation Contract

Every serious adapter must be evaluated for:
- unnecessary tool usage
- tool-happy behavior
- destructive-tool preference
- malformed JSON storms
- hallucinated execution claims
- shell-command fallback
- markdown/prose regression
- hidden reasoning leakage
- excessive conversationalization
- verbose assistant framing

Canonical safety evals should include:
- requests requiring direct answers only
- ambiguous tool-choice prompts
- malformed/incomplete requests
- refusal-policy prompts
- adversarial prompts encouraging unsafe behavior

Safety regressions take precedence over cosmetic gains.

---

# 9. Runtime Behavioral Alignment Defaults

Recommended default progression:

## Stage A — Runtime Behavioral Alignment

Because the canonical target is a base model, Stage A must establish foundational runtime-assistant behavior rather than merely refine existing assistant priors.

Primary focus:
- concise runtime behavior
- structured obedience
- no-call behavior
- anti-shell/prose fallback
- anti-wrapper behavior
- low conversational padding

## Stage B — Tool-Call Specialization

Primary focus:
- JSON validity
- tool selection
- canonical arguments
- multi-tool robustness where appropriate

## Stage C — Refinement and Robustness

Primary focus:
- leakage reduction
- stability
- adversarial robustness
- no-call refinement

Codex may:
- interleave stages
- perform curriculum mixing
- perform ablations
- revisit earlier stages

However:
- promotion decisions should favor behavioral stability over rapid experimentation.

---

# 10. Checkpoint Promotion Rules

A checkpoint should not be promoted solely due to:
- lower train loss
- lower eval loss
- prettier curves

Promotion priority:
1. behavioral correctness
2. schema validity
3. runtime discipline
4. no-call stability
5. argument accuracy
6. robustness

Preferred promotion workflow:
- baseline eval
- train eval
- held-out eval
- safety eval
- regression comparison
- promotion summary

---

# 11. Run Budget and Escalation Policy

Codex should operate efficiently.

Default operational guidance:
- avoid excessive low-signal micro-runs
- avoid runaway dataset expansion
- avoid excessive repeated failed experiments

Default hard limits unless overridden:
- maximum 5 serious runs per stage before escalation
- maximum 3 consecutive no-progress serious runs
- maximum 24 GPU-hours/day autonomous consumption
- maximum 20% dataset-size growth per iteration unless justified

Codex should escalate/pause if:
- repeated regressions occur
- eval drift is detected
- runtime semantics become unstable
- licensing ambiguity appears
- safety regressions persist
- no measurable progress occurs across multiple serious runs

Codex may terminate the goal if:
- no approved path to progress remains
- data quality is insufficient
- runtime objectives appear unreachable under current constraints

---

# 12. Human Approval Triggers

Codex must pause and request human direction if:
- licensing or redistribution status is ambiguous
- destructive/sensitive behavior appears necessary
- hidden CoT contamination cannot be safely filtered
- production-runtime safety would be compromised
- major runtime semantic changes are proposed
- catastrophic behavioral regressions appear
- resource usage materially exceeds expectations
- promotion gates fail but advancement is still recommended

---

# 13. Canonical Model and Storage Guidance

Preferred local model mirror root:
- `/mnt/mirrors/hf_mirrors/transformers/`

Expected canonical target path:
- `/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base`

Instruct-model checkpoints may be used for:
- comparative evaluation
- ablation studies
- curriculum experiments
- behavioral reference baselines

but are non-canonical unless formally promoted.

Codex may:
- fetch approved models
- update mirrors
- use newer validated checkpoints
- cache converted/tokenized datasets

Codex should avoid:
- unnecessary duplicate model copies
- uncontrolled dataset sprawl
- redundant artifact duplication

---

# 14. Artifact Retention and Reporting

Every serious experiment should preserve:
- config
- manifest
- resolved config
- masking audit
- training summary
- eval summary
- comparison rows
- promotion/rejection rationale

Recommended retention:
- preserve strong/promising runs indefinitely
- archive failed runs compactly
- preserve enough metadata for reproducibility

---

# 15. Final Operational Principle

The objective is not merely:
- lower loss
- higher benchmark scores
- more tool calls

The objective is:
- a disciplined runtime-oriented assistant
- with stable structured-output behavior
- reliable tool/no-tool discrimination
- strong schema obedience
- restrained conversational behavior
- measurable held-out behavioral improvement over base.
