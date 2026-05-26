# Codex `/goal` Charter — Condensed Ingestion Version (v3)

## Goal
Build a reproducible post-training pipeline for a runtime-oriented **Llama 3.1-8B** assistant with measurable gains in:
- strict tool-call JSON validity
- tool-name accuracy & argument accuracy
- schema compliance
- low wrapper/prose leakage
- safe no-call behavior
- runtime instruction obedience

**Target behavior**: structured, concise, schema-obedient, low-fluff, low-hallucination, runtime-oriented, contract-following.

**Disfavored**: chatty assistant behavior, markdown-heavy output, personality/roleplay alignment, shell-command fallback, hallucinated execution, generic chatbot tuning.

Do not silently redefine runtime objectives, evaluation semantics, or schema expectations across iterations.

---

## Background
A prior Llama-3.2-3B-Instruct probe validated the pipeline (`dataset → split → trainer → masking → QLoRA → adapter save → eval`) but failed behaviorally (malformed JSON, prose responses, shell fallback, weak tool compliance).

**Conclusion**: Tool-call SFT alone is insufficient. Runtime-oriented instruct alignment is required in addition to tool specialization.

Behavioral evaluation metrics take precedence over train/eval loss improvement.

---

## Primary Target
**Default model**: Llama 3.1-8B.  
Codex may choose base or instruct after recording rationale.  
**Default preference**: base (to reduce inherited chatbot behavior).

---

## Training Architecture

### Stage A — Runtime-Oriented Instruct Alignment
Teach structured-output obedience, concise compliance, schema discipline, no fake execution claims, tool/no-tool discrimination, no-call behavior, and low conversational filler.

### Stage B — Tool-Call Specialization
Teach strict JSON emission, canonical tool-call structure and arguments, tool selection, argument synthesis, and policy/no-call behavior.

### Stage C — Optional Refinement
Later improvements to leakage reduction, JSON stability, no-call refinement, and brevity.

---

## Repositories
- **Training repo** (`/opt/ai-stack/assistant-training`): owns datasets, transforms, validation, configs, manifests, training/eval scripts, artifacts, reports.
- **Runtime repo** (`/opt/ai-stack/runtimes/assistant-runtime`): owns tool schemas, runtime semantics, validation cases, production behavior.

---

## Autonomous Authority
The `/goal` charter is the approval envelope. Codex may autonomously inspect repos, create scripts/tests/builders/transforms, review/filter datasets, generate synthetic/paraphrased data, run validations/preflights/training/eval, iterate configs/datasets, discard weak adapters, and write reports/recommendations.

Continue until success, no approved path exists, or Roy intervenes.

---

## Provenance Requirements
Every serious run must emit:
- config
- manifest/run record
- dataset version
- model path
- adapter path
- masking audit
- training summary
- eval summary

Manifests are audit artifacts (not launch gates).

---

## Dataset Policy
External datasets may be used after review. For every candidate record:
- source
- license
- fine-tune permission
- schema/tool-call style
- malformed JSON prevalence
- CoT contamination
- unsafe/destructive content
- conversion feasibility
- fit to runtime goals
- recommendation:
  - use
  - filter/convert
  - reject

Do not expand datasets through low-quality paraphrase inflation merely to increase row count.

---

## Preferred Dataset Characteristics

**Prefer**:
- structured output
- JSON discipline
- function calling
- tool use
- concise assistant behavior
- runtime compliance
- schema adherence
- safe failure handling

**Disfavor / filter**:
- chatbot chatter
- roleplay/personality optimization
- markdown-centric formatting
- shell-command-as-answer patterns
- hidden CoT traces
- verbose conversational padding

---

## Safety Constraints

### No hidden CoT training
Reject or strip `<think>`, scratchpads, hidden reasoning traces, and hidden CoT unless later approved.

### No destructive defaults
Mutating examples must use temp paths, `.state` paths, dry-run/status-only operations, or harmless synthetic examples.

### Preserve assistant-only masking
Training must preserve:
- `labels=-100` for system/user/prompt tokens
- supervision only for assistant target tokens

Masking audits required for all runs.

### Use tokenizer-native chat templates
Default:
`tokenizer.apply_chat_template(..., add_generation_prompt=True)`

### Do not merge adapters by default
Keep adapters separate. Do not overwrite base weights.

---

## Optimization Priority Order
1. Correctness
2. Schema/tool-call validity
3. Safety/runtime discipline
4. Generalization
5. Stylistic quality
6. Verbosity reduction

---

## Starting Tasks
1. Inventory current repo/dataset state.
2. Decide whether running prepared v0.2 3B probe is still useful.
3. Establish Llama 3.1-8B baseline eval.
4. Review candidate external datasets.
5. Build Dataset v1.0:
   - in-house runtime data
   - synthetic/paraphrased runtime data
   - approved external data
6. Train/evaluate adapters autonomously.

---

## Dataset v1.0 Targets
Dataset should include:
- runtime-oriented instruct examples
- tool-call positives
- tool/no-tool discrimination
- safe failure behavior
- policy/no-call examples
- JSON-format discipline

**Scale target**:
- minimum: ~2k rows
- preferred: ~5k–10k rows if quality remains high

**Quality > quantity.**

---

## Required Evaluations
For every serious adapter run:
- train eval
- held-out validation eval
- all-tool holdout eval
- no-call eval
- failure/policy eval
- base vs adapter comparison

**Metrics**:
- strict JSON validity
- tool-name accuracy & argument accuracy
- schema validity
- wrapper leakage
- no-call correctness
- failure-category distribution

---

## Success Criteria

### Promising
- nonzero exact JSON validity
- nonzero held-out tool-name accuracy
- lower invalid_json rate than base
- no major unsafe/tool-happy regression

### Strong
- high JSON validity
- meaningful tool-name & argument accuracy
- robust multi-tool behavior
- low wrapper leakage
- acceptable no-call behavior
- reproducible artifacts

### Final Objective
A reproducible runtime-oriented model that measurably outperforms the base model on held-out structured tool-call evaluations while maintaining disciplined runtime behavior.
