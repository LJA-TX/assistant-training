# Revised Autonomous Codex `/goal` Charter

## Goal Name

```text id="v7d4yw"
assistant-runtime-toolcall-lora-llama31-8b
```

---

# Mission

Create a reproducible, evaluated post-training workflow that produces a measurable improvement in assistant-runtime behavior for the **Llama 3.1-8B family**, using the existing assistant-training repo as the foundation.

The goal is **not** merely to train an adapter.

The goal is to produce a runtime-oriented assistant model that measurably improves:

```text id="kp4u1r"
strict tool-call JSON emission
tool-name accuracy
argument accuracy
schema compliance
low prose/wrapper leakage
safe no-call/failure behavior
runtime instruction obedience
structured-output discipline
```

The project explicitly authorizes:

```text id="7bwhxu"
runtime-oriented instruct alignment
+
tool-call specialization
```

as complementary training objectives.

---

# Background

A first probe using **Llama-3.2-3B-Instruct** successfully proved the engineering pipeline:

```text id="txqf5q"
dataset → split → trainer → masking → QLoRA → adapter save → eval
```

but failed behaviorally.

The model continued reverting to:

```text id="cw0v7t"
chatty assistant behavior
shell-command fallback
malformed JSON
conversational prose
```

even after tool-call SFT.

This suggests the problem is not merely “tool-call formatting,” but deeper assistant-runtime behavioral alignment.

Accordingly, this goal authorizes a broader and more structured training approach.

---

# Primary Target Model

Default target:

```text id="g8z4ri"
Llama 3.1-8B
```

Codex may choose either:

```text id="nny9v4"
Llama-3.1-8B base
or
Llama-3.1-8B-Instruct
```

after recording a short rationale.

Default assumption:

```text id="nfg9fp"
Prefer Llama-3.1-8B base if practical, because a less chat-biased starting point may produce cleaner runtime behavior after targeted alignment.
```

Codex may evaluate both paths if beneficial.

---

# Core Philosophy

This project is **not** attempting to build a generic public chatbot.

The desired model behavior is:

```text id="uz0e0z"
disciplined
runtime-oriented
schema-obedient
structured
concise
low-fluff
low-hallucination
tool-aware
contract-following
```

The project explicitly disfavors:

```text id="7j64q9"
overly conversational behavior
assistant personality bleed
markdown-heavy output
verbose explanations
shell-command fallback as default behavior
hallucinated execution
roleplay-heavy alignment
generic internet-chatbot tuning
```

---

# Training Architecture

Codex is authorized to pursue a multi-stage curriculum.

Recommended conceptual stages:

---

## Stage A — Runtime-Oriented Instruct Alignment

Goal:

```text id="2wbo7n"
Teach the model to behave like an assistant-runtime model.
```

This stage may include:

* concise instruction-following
* structured-output obedience
* contract-following behavior
* schema discipline
* low-markdown behavior
* no fake execution claims
* proper no-call behavior
* tool-vs-no-tool discrimination
* refusal discipline where appropriate
* direct answer formatting
* suppression of unnecessary conversational filler

This is:

```text id="x5w8np"
runtime instruct tuning
```

not generic chatbot alignment.

---

## Stage B — Tool-Call Specialization

Goal:

```text id="8b7y8j"
Teach strict assistant-runtime tool-call behavior.
```

This stage may include:

* strict JSON emission
* canonical tool-call structure
* canonical argument formatting
* argument synthesis
* tool selection
* multi-tool behavior where justified
* failure handling
* policy/no-call behavior
* tool-call schema adherence

---

## Stage C — Optional Preference/Behavior Refinement

Only if useful.

Possible later-stage refinement:

* reduction of wrapper leakage
* JSON stability improvements
* policy refinement
* improved no-call discrimination
* runtime brevity refinement
* inference-temperature robustness

---

# Starting Repositories

Primary training repo:

```text id="kg8y7x"
/opt/ai-stack/assistant-training
```

Runtime/source-data repo:

```text id="wjp8oq"
/opt/ai-stack/runtimes/assistant-runtime
```

Training repo responsibilities:

```text id="xkby8u"
dataset intake
dataset transformation
dataset validation
training configs
run manifests
trainer scripts
adapter artifacts
evaluation harnesses
reports
```

Runtime repo responsibilities:

```text id="n5u5jq"
tool schemas
historical reports
runtime validation cases
tool semantics
production runtime behavior
```

---

# Autonomous Execution Authority

The `/goal` charter itself is the approval envelope.

Codex is authorized to autonomously:

```text id="3rjv7u"
inspect repos
create scripts/tests/dataset builders/filters
review external datasets
transform datasets
generate synthetic/paraphrased examples
run validations/preflights
launch training runs
launch eval runs
discard weak adapters
iterate configs/datasets
write reports/recommendations
```

Codex should **not** stop for human approval before routine training/evaluation runs that comply with this charter.

Codex should continue autonomously until:

```text id="tw4b8j"
1. the target model is deemed successfully trained;
2. there is no approved path to progress; or
3. Roy intervenes.
```

---

# Provenance Requirements

Human approval gates are removed.

However, every serious run must still produce reproducible provenance records:

```text id="4n44js"
config
manifest/run record
dataset version
base model path
adapter output path
masking audit
training summary
evaluation summary
comparison rows where applicable
```

Manifests are:

```text id="x2u9l7"
audit artifacts
```

not launch blockers.

---

# External Dataset Policy

Codex is authorized to investigate external datasets.

However, external datasets must be reviewed before use.

For every candidate dataset, Codex must record:

```text id="0qgg8m"
dataset name
source
license
redistribution/fine-tune permission
schema style
tool-call format
quality observations
malformed JSON prevalence
deduplication concerns
chain-of-thought contamination
unsafe/destructive content
conversion feasibility
fit to runtime objectives
recommendation:
  use
  filter/convert
  reject
```

---

# Explicitly Disfavored Dataset Types

Codex should strongly avoid or heavily filter datasets dominated by:

```text id="1d7g3n"
generic chatbot chatter
roleplay-heavy behavior
assistant personality optimization
markdown-centric formatting
internet-forum tone
verbose conversational padding
shell-command-as-answer patterns
hidden chain-of-thought traces
```

Examples include many:

```text id="ev5b4n"
ShareGPT-style dumps
OpenHermes-style personality-heavy mixtures
unfiltered Alpaca derivatives
```

unless carefully filtered and justified.

---

# Preferred Dataset Characteristics

Preferred datasets teach:

```text id="m6ye1l"
structured output
JSON discipline
function calling
tool use
runtime compliance
instruction obedience
concise assistant behavior
schema adherence
safe failure handling
```

---

# Safety Constraints

---

## 1. No hidden chain-of-thought training

Reject or strip:

```text id="ysgnjlwm"
<think>
scratchpad
analysis traces
reasoning traces
hidden CoT
```

unless explicitly approved later.

---

## 2. No destructive default behavior

Mutating examples must use:

```text id="i0e78k"
temp paths
.state paths
dry-run modes
status-only operations
harmless synthetic examples
```

The model should not learn dangerous filesystem or shell habits.

---

## 3. Preserve assistant-only masking

Training must preserve:

```text id="i76a3q"
labels=-100 for system/user/prompt tokens
supervision only for assistant target tokens
```

Masking audits are required for all runs.

---

## 4. Use tokenizer-native chat templates by default

Prompt serialization should use:

```text id="wxq5vr"
tokenizer.apply_chat_template(..., add_generation_prompt=True)
```

unless a named/custom fallback is justified and documented.

---

## 5. Do not merge adapters by default

Adapters should remain separate unless explicitly approved later.

Do not overwrite base weights.

---

# Recommended Starting Tasks

---

## Task 1 — Inventory Current State

Inspect:

```text id="ecqwy7"
/opt/ai-stack/assistant-training
/opt/ai-stack/runtimes/assistant-runtime/reports/ft_data
```

Verify actual on-disk state.

---

## Task 2 — Decide Whether to Run v0.2

Codex should decide whether running the prepared:

```text id="mp95x2"
Llama-3.2-3B-Instruct v0.2 probe
```

is still useful before moving to 8B.

Record rationale.

---

## Task 3 — Establish Llama 3.1-8B Baseline

Identify local model path/mirror.

Run baseline evaluations before training.

---

## Task 4 — External Dataset Review

Investigate:

```text id="5qkcvw"
function-calling datasets
tool-use datasets
structured-output datasets
runtime-oriented instruct datasets
JSON-discipline datasets
```

Classify each candidate:

```text id="0bq4a0"
use
filter/convert
reject
```

---

## Task 5 — Build Dataset v1.0

Combine:

```text id="j09cjk"
1. in-house assistant-runtime examples
2. generated/paraphrased runtime examples
3. approved external examples
```

Dataset should include:

```text id="jlwmii"
tool-call positives
runtime-oriented instruct examples
tool/no-tool discrimination
safe failure behavior
policy/no-call examples
structured-output discipline
JSON formatting discipline
```

Target scale:

```text id="ol4z48"
minimum: ~2,000 rows
preferred: ~5,000–10,000 rows if quality remains high
```

---

## Task 6 — Train and Evaluate

Codex may autonomously iterate:

```text id="s91eg8"
datasets
configs
LoRA targets
learning rates
epochs
curriculum ordering
base vs instruct checkpoints
```

Required evaluations:

```text id="2c9g2p"
train eval
held-out validation eval
all-tool holdout eval
no-call eval
failure/policy eval
base vs adapter comparison
```

Metrics:

```text id="kz4r2n"
strict JSON validity
tool-name accuracy
argument accuracy
schema validity
wrapper/prose leakage
no-call correctness
failure-category distribution
```

---

# Success Criteria

A run is promising if it achieves:

```text id="wz09x0"
nonzero exact JSON validity
nonzero held-out tool-name accuracy
lower invalid_json rate than base
no catastrophic unsafe/tool-happy regression
```

A run is strong if it achieves:

```text id="6gnfh1"
high strict JSON validity
meaningful tool-name accuracy
meaningful argument accuracy
robust behavior across tool families
low prose/wrapper leakage
acceptable no-call behavior
reproducible artifacts
```

---

# Final Objective

A successful outcome is **not** merely a completed training run.

A successful outcome is:

```text id="jlwmm1"
a reproducible assistant-runtime-oriented model
that measurably outperforms the base model
on held-out structured tool-call evaluations
while maintaining disciplined runtime behavior
```

