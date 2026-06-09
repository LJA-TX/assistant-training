# Codex `/goal` Charter — Condensed Ingestion Version

## Goal

Build a reproducible post-training pipeline that produces a runtime-oriented Llama 3.1-8B assistant with measurable improvement in:

* strict tool-call JSON validity
* tool-name accuracy
* argument accuracy
* schema compliance
* low wrapper/prose leakage
* safe no-call behavior
* runtime instruction obedience

Target behavior:

* structured
* concise
* schema-obedient
* low-fluff
* low-hallucination
* runtime-oriented
* contract-following

Disfavor:

* chatty assistant behavior
* markdown-heavy output
* personality/roleplay alignment
* shell-command fallback
* hallucinated execution
* generic chatbot tuning

---

# Background

A prior Llama-3.2-3B-Instruct probe proved the engineering pipeline:

```text id="oqh1s6"
dataset → split → trainer → masking → QLoRA → adapter save → eval
```

but failed behaviorally:

* malformed JSON
* prose responses
* shell-command fallback
* weak tool-call compliance

Conclusion:

```text id="w80k3r"
Tool-call SFT alone was insufficient.
Runtime-oriented instruct alignment is authorized in addition to tool specialization.
```

---

# Primary Target

Default target:

```text id="yvgnme"
Llama 3.1-8B
```

Codex may choose:

* base
* instruct

after recording rationale.

Default preference:

```text id="ewxf9x"
Prefer base if practical to reduce inherited chatbot behavior.
```

---

# Training Architecture

## Stage A — Runtime-Oriented Instruct Alignment

Teach:

* structured-output obedience
* concise compliance
* schema discipline
* no fake execution claims
* tool/no-tool discrimination
* no-call behavior
* low conversational filler

## Stage B — Tool-Call Specialization

Teach:

* strict JSON emission
* canonical tool-call structure
* canonical arguments
* tool selection
* argument synthesis
* policy/no-call behavior

## Stage C — Optional Refinement

Possible later refinement:

* leakage reduction
* JSON stability
* no-call refinement
* brevity refinement

---

# Repositories

Training repo:

```text id="jlwmmg"
/opt/ai-stack/assistant-training
```

Runtime/source-data repo:

```text id="orh9h2"
/opt/ai-stack/runtimes/assistant-runtime
```

Training repo owns:

* datasets
* transforms
* validation
* configs
* manifests
* training/eval scripts
* artifacts
* reports

Runtime repo owns:

* tool schemas
* runtime semantics
* validation cases
* production behavior

---

# Autonomous Authority

The `/goal` charter is the approval envelope.

Codex may autonomously:

* inspect repos
* create scripts/tests/builders/transforms
* review/filter datasets
* generate synthetic/paraphrased data
* run validations/preflights
* launch training/eval runs
* iterate configs/datasets
* discard weak adapters
* write reports/recommendations

Codex should continue until:

1. success;
2. no approved path exists; or
3. Roy intervenes.

---

# Provenance Requirements

Every serious run must emit:

* config
* manifest/run record
* dataset version
* model path
* adapter path
* masking audit
* training summary
* eval summary

Manifests are audit artifacts, not launch gates.

---

# Dataset Policy

External datasets may be investigated and used after review.

For every candidate dataset, record:

* source
* license
* fine-tune permission
* schema/tool-call style
* malformed JSON prevalence
* CoT contamination
* unsafe/destructive content
* conversion feasibility
* fit to runtime goals
* recommendation:

  * use
  * filter/convert
  * reject

---

# Preferred Dataset Characteristics

Prefer:

* structured output
* JSON discipline
* function calling
* tool use
* concise assistant behavior
* runtime compliance
* schema adherence
* safe failure handling

Disfavor/filter:

* chatbot chatter
* roleplay/personality optimization
* markdown-centric formatting
* shell-command-as-answer patterns
* hidden CoT traces
* verbose conversational padding

---

# Safety Constraints

## No hidden CoT training

Reject/strip:

* `<think>`
* scratchpads
* hidden reasoning traces
* hidden CoT

unless later approved.

## No destructive defaults

Mutating examples must use:

* temp paths
* `.state` paths
* dry-run/status-only operations
* harmless synthetic examples

## Preserve assistant-only masking

Training must preserve:

```text id="p4lw2h"
labels=-100 for system/user/prompt tokens
supervision only for assistant target tokens
```

Masking audits required for all runs.

## Use tokenizer-native chat templates

Default:

```text id="1vgcnf"
tokenizer.apply_chat_template(..., add_generation_prompt=True)
```

## Do not merge adapters by default

Keep adapters separate.
Do not overwrite base weights.

---

# Optimization Priority Order

1. correctness
2. schema/tool-call validity
3. safety/runtime discipline
4. generalization
5. stylistic quality
6. verbosity reduction

---

# Starting Tasks

1. Inventory current repo/dataset state.
2. Decide whether running prepared v0.2 3B probe is still useful.
3. Establish Llama 3.1-8B baseline eval.
4. Review candidate external datasets.
5. Build dataset v1.0:

   * in-house runtime data
   * synthetic/paraphrased runtime data
   * approved external data
6. Train/evaluate adapters autonomously.

---

# Dataset v1.0 Targets

Dataset should include:

* runtime-oriented instruct examples
* tool-call positives
* tool/no-tool discrimination
* safe failure behavior
* policy/no-call examples
* JSON-format discipline

Scale target:

```text id="vjlwm5"
minimum: ~2k rows
preferred: ~5k–10k rows if quality remains high
```

Quality > quantity. ([GitHub][1])

---

# Required Evaluations

For every serious adapter:

* train eval
* held-out validation eval
* all-tool holdout eval
* no-call eval
* failure/policy eval
* base vs adapter comparison

Metrics:

* strict JSON validity
* tool-name accuracy
* argument accuracy
* schema validity
* wrapper leakage
* no-call correctness
* failure-category distribution

---

# Success Criteria

Promising:

* nonzero exact JSON validity
* nonzero held-out tool-name accuracy
* lower invalid_json rate than base
* no major unsafe/tool-happy regression

Strong:

* high JSON validity
* meaningful tool-name accuracy
* meaningful argument accuracy
* robust multi-tool behavior
* low wrapper leakage
* acceptable no-call behavior
* reproducible artifacts

Final objective:

```text id="6hr8qk"
A reproducible runtime-oriented model that measurably outperforms the base model on held-out structured tool-call evaluations while maintaining disciplined runtime behavior.
```

Research on fine-tuning repeatedly emphasizes that data quality/curation and behavioral alignment matter more than raw dataset size, especially for smaller models and structured-output tasks. ([GitHub][1])

[1]: https://github.com/LightChen233/Awesome-Long-Chain-of-Thought-Reasoning?utm_source=chatgpt.com "LightChen233/Awesome-Long-Chain-of-Thought-Reasoning"

