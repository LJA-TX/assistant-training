# Codex `/goal` Charter — Further Condensed (v5)

## Goal
Build a reproducible post-training pipeline for a runtime-oriented **Llama 3.1-8B** assistant with measurable gains in:
- strict tool-call JSON validity
- tool-name accuracy & argument accuracy
- schema compliance
- low wrapper/prose leakage
- safe no-call behavior
- runtime instruction obedience

**Target behavior**:
- structured
- concise
- schema-obedient
- low-fluff
- low-hallucination
- runtime-oriented
- contract-following

**Disfavored**:
- chatty assistant behavior
- markdown-heavy output
- personality/roleplay alignment
- shell-command fallback
- hallucinated execution
- generic chatbot tuning

Do not silently redefine runtime objectives, evaluation semantics, schema expectations, or scoring semantics across iterations.

Behavioral evaluation metrics take precedence over train/eval loss improvement.

Appendix A promotion/evaluation gates are the binding operational authority for autonomous advancement decisions.

---

## Background
A prior Llama-3.2-3B-Instruct probe validated the pipeline:

`dataset → split → trainer → masking → QLoRA → adapter save → eval`

but failed behaviorally:
- malformed JSON
- prose responses
- shell fallback
- weak tool compliance

**Conclusion**:
Tool-call SFT alone is insufficient.

The project intentionally favors:
- a cleaner behavioral substrate
- over inherited chatbot priors,

accepting additional curriculum and alignment complexity in exchange for stronger long-term runtime-discipline potential.

---

## Primary Target

### Canonical Autonomous Target
- Llama-3.1-8B base

### Expected Initial Model Path
- `/mnt/mirrors/hf_mirrors/transformers/llama-3.1-8b-base`

### Operational Objective
Construct disciplined runtime-assistant behavior through:
1. runtime behavioral alignment
2. tool-call specialization

### Instruct-Model Experiments
Permitted for:
- comparative research
- baselines
- curriculum experiments
- ablation studies

However:
- instruct-model paths are non-canonical unless later promoted by evidence.

---

## Training Architecture

### Stage A — Runtime Behavioral Alignment
Teach:
- structured-output obedience
- concise compliance
- schema discipline
- no fake execution claims
- tool/no-tool discrimination
- no-call behavior
- anti-wrapper behavior
- low conversational filler

### Stage B — Tool-Call Specialization
Teach:
- strict JSON emission
- canonical tool-call structure
- canonical arguments
- tool selection
- argument synthesis
- policy/no-call behavior

### Stage C — Optional Refinement
Possible later refinement:
- leakage reduction
- JSON stability
- no-call refinement
- brevity refinement
- adversarial robustness

Codex may:
- perform runtime behavioral alignment
- perform tool-call specialization
- perform staged or mixed curriculum training
- mix runtime-alignment and tool-call datasets when beneficial

**Objective**:
A disciplined runtime assistant, not merely a chatbot with tools.

---

## Repositories

### Training Repo
`/opt/ai-stack/assistant-training`

Owns:
- datasets
- transforms
- validation
- configs
- manifests
- training/eval scripts
- artifacts
- reports

### Runtime Repo
`/opt/ai-stack/runtimes/assistant-runtime`

Owns:
- tool schemas
- runtime semantics
- validation cases
- production behavior

### Model Service
- `/opt/ai-stack/runtimes/modular`
- `/opt/ai-stack/runtimes/monolith`

### Stack Repo
`/opt/ai-stack/stacks/llama-3.1-8b-base`

---

## Autonomous Authority

The `/goal` charter is the approval envelope.

Codex may autonomously:
- inspect repos
- create scripts/tests/builders/transforms
- review/filter/fetch/download datasets
- canonicalize schemas
- convert formats
- generate synthetic/paraphrased runtime data
- run validations/preflights/training/eval
- iterate configs/datasets
- discard weak adapters
- write reports/recommendations

within Appendix A operational constraints.

Continue until:
1. success;
2. no approved path exists; or
3. Roy intervenes.

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

Manifests are audit artifacts, not launch gates.

---

## Dataset Policy

Codex may autonomously:
- investigate datasets
- fetch/download datasets
- filter datasets
- canonicalize schemas
- convert formats
- build hybrid datasets
- generate synthetic/paraphrased runtime data

within reasonable local compute/storage constraints.

External datasets may be used after review.

For every candidate dataset or subset:
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

Canonicalize external tool-call formats into the assistant-runtime schema before training whenever practical.

Aggressively filter or down-weight datasets exhibiting:
- excessive conversational padding
- assistant socialization
- wrapper-heavy behavior
- markdown-heavy behavior
- shell-command-as-answer patterns

Preference should be given to:
- concise
- execution-oriented
- schema-disciplined
- low-wrapper

assistant behavior.

### High-Priority Candidate Dataset Families

Codex is explicitly authorized to investigate and potentially use filtered/canonicalized subsets of:

- **Salesforce xLAM / APIGen**
  - primary tool-call correctness data

- **NVIDIA When2Call**
  - no-call / tool-decision behavior

- **APIGen-MT**
  - multi-turn tool use

- **ToolACE**
  - later-stage diversity/generalization

- **Glaive function-calling datasets**
  - anti-tool-happy balancing

---

## Safety Constraints

### No hidden CoT training
Reject or strip:
- `<think>`
- scratchpads
- hidden reasoning traces
- hidden CoT

unless later approved.

### No destructive defaults
Mutating examples must use:
- temp paths
- `.state` paths
- dry-run/status-only operations
- harmless synthetic examples

### Preserve assistant-only masking
Training must preserve:
- `labels=-100` for system/user/prompt tokens
- supervision only for assistant target tokens

Masking audits required for all runs.

### Use tokenizer-native chat templates
Default:
`tokenizer.apply_chat_template(..., add_generation_prompt=True)`

### Do not merge adapters by default
Keep adapters separate.
Do not overwrite base weights.

### Preserve no-call behavior
Do not train toward unconditional tool usage.

Preserve:
- strong direct-answer behavior
- strong no-call behavior
- disciplined runtime restraint

where appropriate.

---

## Optimization Priority Order

1. correctness
2. schema/tool-call validity
3. safety/runtime discipline
4. generalization
5. behavioral stability
6. verbosity reduction
7. conversational polish

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
   - canonicalized runtime schema data
6. Train/evaluate adapters autonomously.

---

## Dataset v1.0 Targets

Dataset should include:
- runtime behavioral alignment examples
- tool-call positives
- tool/no-tool discrimination
- safe failure behavior
- policy/no-call examples
- JSON-format discipline

### Scale Target
- minimum: ~2k rows
- preferred: ~5k–10k rows if quality remains high

### Principle
Quality > quantity.

---

## Required Evaluations

For every serious adapter run:
- train eval
- held-out validation eval
- all-tool holdout eval
- no-call eval
- failure/policy eval
- base vs adapter comparison

Additionally evaluate:
- tool-happy behavior
- unnecessary tool-call frequency
- direct-answer regression
- ordinary non-tool assistant behavior

### Metrics
- strict JSON validity
- tool-name accuracy
- argument accuracy
- schema validity
- wrapper leakage
- no-call correctness
- failure-category distribution

Metric formulas and scoring semantics are governed by canonical evaluation specifications referenced by Appendix A.

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
