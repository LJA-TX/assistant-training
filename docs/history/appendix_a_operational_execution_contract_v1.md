# Appendix A — Operational Execution Contract (v1)

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

## 2.1 Canonical Eval Assets

Default canonical evaluation assets:
- held-out validation split
- all-tool holdout split
- no-call/policy split
- adversarial malformed-request split
- direct-answer/non-tool split

All eval manifests must record:
- dataset paths
- dataset hashes
- split versions
- scoring script version

## 2.2 Frozen Decode Defaults

Unless explicitly testing decode robustness, default eval inference settings:
- temperature: 0.0
- top_p: 1.0
- do_sample: false
- repetition_penalty: 1.0
- max_new_tokens: fixed per eval suite
- seed: fixed and recorded

Any deviation must be recorded.

## 2.3 Frozen Prompt Contract

Default evaluation prompt serialization:
- tokenizer-native chat template
- add_generation_prompt=true
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

Target distribution guidance:
- 35–55% tool-call positives
- 15–30% no-call/direct-answer behavior
- 10–20% runtime-oriented instruct behavior
- 5–15% refusal/policy/safety behavior
- 5–15% adversarial/error/malformed-request behavior

Synthetic/paraphrased content:
- preferred: <50%
- hard ceiling: 70%

Pure paraphrase inflation is prohibited.

Codex must favor:
- semantic diversity
- tool diversity
- argument diversity
- phrasing diversity

over raw row count.

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

Preferred isolation:
- hold out entire tool families where feasible
- hold out entire semantic task clusters where feasible

Evaluation contamination must be treated as a serious failure.

---

# 5. Definition of a Serious Run

A run is considered “serious” if it:
- performs actual gradient updates;
- produces adapter artifacts;
- consumes nontrivial compute;
- or is intended for comparison/promotion.

A serious run must include:
- config
- manifest/run record
- dataset manifest/version
- masking audit
- training summary
- evaluation summary
- runtime/schema pinning metadata

Minimum serious-run expectations:
- complete canonical eval suite;
- recorded hyperparameters;
- recorded dataset composition summary;
- reproducible launch command.

Tiny exploratory runs may be excluded from promotion consideration.

---

# 6. Numeric Promotion Gates

These thresholds define default advancement guidance.

## 6.1 Minimum Promising Threshold

Compared against base model:
- exact JSON validity improvement
- lower invalid_json rate
- nonzero held-out tool-name accuracy
- non-catastrophic no-call regression
- no major unsafe/tool-happy regression

Suggested numeric guidance:
- ≥10% exact JSON validity on held-out eval
- ≥5% held-out tool-name accuracy
- wrapper leakage not worse than base by >5%
- no-call correctness not degraded by >10%

## 6.2 Strong Candidate Threshold

Suggested strong-candidate guidance:
- ≥50% exact JSON validity
- ≥35% tool-name accuracy
- ≥25% argument accuracy
- low wrapper leakage
- stable no-call behavior
- acceptable adversarial/policy behavior

These are guidance targets, not rigid mathematical truths.

Codex may promote/demote based on broader behavioral evidence.

---

# 7. Safety Evaluation Contract

Every serious adapter must be evaluated for:
- unnecessary tool usage
- tool-happy behavior
- destructive-tool preference
- malformed JSON storms
- hallucinated execution claims
- shell-command fallback
- markdown/prose regression
- hidden reasoning leakage

Canonical safety evals should include:
- requests requiring direct answers only
- ambiguous tool-choice prompts
- malformed/incomplete requests
- refusal-policy prompts
- adversarial prompts encouraging unsafe behavior

Safety regressions take precedence over cosmetic gains.

---

# 8. Stage Execution Defaults

Recommended default progression:

## Stage A
Runtime-oriented instruct alignment.

Primary focus:
- concise runtime behavior
- structured obedience
- no-call behavior
- anti-shell/prose fallback

## Stage B
Tool-call specialization.

Primary focus:
- JSON validity
- tool selection
- canonical arguments
- multi-tool robustness if appropriate

## Stage C
Refinement and robustness.

Primary focus:
- leakage reduction
- stability
- adversarial robustness
- no-call refinement

Codex may:
- interleave stages;
- perform curriculum mixing;
- perform ablations;
- revisit earlier stages.

However:
- promotion decisions should favor behavioral stability over rapid experimentation.

---

# 9. Checkpoint Promotion Rules

A checkpoint should not be promoted solely due to:
- lower train loss
- lower eval loss
- prettier curves

Promotion should prioritize:
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

# 10. Run Budget and Escalation Policy

Codex should operate efficiently.

Default soft guidance:
- avoid excessive low-signal micro-runs;
- avoid runaway dataset expansion;
- avoid excessive repeated failed experiments.

Codex should escalate/pause if:
- repeated regressions occur;
- eval drift is detected;
- runtime semantics become unstable;
- licensing ambiguity appears;
- safety regressions persist;
- no measurable progress occurs across multiple serious runs.

Codex may terminate the goal if:
- no approved path to progress remains;
- data quality is insufficient;
- runtime objectives appear unreachable under current constraints.

---

# 11. Human Approval Triggers

Codex must pause and request human direction if:
- licensing or redistribution status is ambiguous;
- destructive/sensitive behavior appears necessary;
- hidden CoT contamination cannot be safely filtered;
- production-runtime safety would be compromised;
- major runtime semantic changes are proposed;
- catastrophic behavioral regressions appear;
- resource usage materially exceeds expectations.

---

# 12. Canonical Model and Storage Guidance

Preferred local model mirror root:
- `/mnt/mirrors/hf_mirrors/transformers/`

Expected initial operational target path:
- `/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-instruct`

Codex may:
- fetch approved models;
- update mirrors;
- use newer validated checkpoints;
- cache converted/tokenized datasets.

Codex should avoid:
- unnecessary duplicate model copies;
- uncontrolled dataset sprawl;
- redundant artifact duplication.

---

# 13. Artifact Retention and Reporting

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
- preserve strong/promising runs indefinitely;
- archive failed runs compactly;
- preserve enough metadata for reproducibility.

---

# 14. Final Operational Principle

The objective is not merely:
- lower loss;
- higher benchmark scores;
- or more tool calls.

The objective is:
- a disciplined runtime-oriented assistant;
- with stable structured-output behavior;
- reliable tool/no-tool discrimination;
- strong schema obedience;
- and measurable held-out behavioral improvement over base.

