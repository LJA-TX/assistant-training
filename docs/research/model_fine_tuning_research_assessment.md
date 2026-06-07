I think there are several genuinely promising candidates here — and importantly, they are promising for *different reasons*. I would not treat this as “pick one dataset.” I would think in layers.

Below is my current assessment.

---

# Highest-Priority Candidates

## 1. [Salesforce xLAM / APIGen datasets](https://huggingface.co/datasets/Salesforce/xlam-function-calling-60k?utm_source=chatgpt.com)

Associated paper:
([arXiv][1])

### Why I think this is probably your best starting point

This looks extremely aligned with your goals:

* function calling
* structured generation
* executable/verifiable APIs
* large scale
* open fine-tuning orientation
* explicitly targeted at small/open models
* strong benchmark performance claims

The important part is this:

```text id="k5jvab"
verified executable APIs
semantic verification
format checking
```

That is exactly the kind of discipline your project needs.

Your runtime objectives are:

* structured correctness,
* schema obedience,
* argument correctness,
* low hallucination.

xLAM/APIGen appears designed around those concerns rather than “assistant personality.”

### My current risk assessment

#### Strengths

* probably strongest direct alignment
* function-calling-native
* modern
* strong scale
* designed for SFT
* proven on smaller models

#### Risks

* may contain CoT/reasoning traces in some subsets
* may encode tool-call schema assumptions different from assistant-runtime
* may overfit toward its own tool wrappers
* 60k may be too large/noisy unfiltered

### My recommendation

```text id="qfwlzr"
HIGH PRIORITY REVIEW
```

Probably your best initial external candidate.

---

# 2. [NVIDIA When2Call](https://huggingface.co/datasets/nvidia/When2Call?utm_source=chatgpt.com)

Associated repo:
([GitHub][2])

### Why this is extremely important

Honestly?

This may be the single most *strategically* important dataset for your architecture.

Because your earlier failures strongly suggest:

```text id="b7r8hx"
the model does not understand WHEN to call tools.
```

not merely:

```text id="pcw0ji"
HOW to format them.
```

That distinction matters enormously.

NVIDIA explicitly focuses on:

* when NOT to call tools,
* follow-up questions,
* insufficient information,
* inability handling,
* decision boundaries.

That maps *directly* onto your:

* no-call behavior,
* runtime discipline,
* anti-tool-happy behavior,
* policy behavior.

### My recommendation

```text id="g1q7a0"
ESSENTIAL SUPPLEMENTAL DATASET
```

I would almost certainly want this mixed into training eventually.

Potentially:

* not the primary dataset,
* but strategically critical.

---

# 3. [ToolACE](https://huggingface.co/Team-ACE?utm_source=chatgpt.com)

Paper:
([OpenReview][3])

### Why it matters

ToolACE appears heavily focused on:

* diversity,
* realistic complexity,
* multi-agent synthesis,
* API breadth,
* tool-learning difficulty.

This may become valuable later for:

* generalization,
* unseen tool robustness,
* multi-tool workflows.

### My concern

It may be:

* too broad,
* too synthetic,
* too “agentic”
* too benchmark-oriented

for your initial runtime-discipline phase.

You are not trying to build:

```text id="94b47u"
an autonomous internet super-agent
```

You are trying to build:

```text id="tuk0pq"
a disciplined runtime tool-caller.
```

Those are different.

### My recommendation

```text id="9j5rf4"
SECOND-WAVE DATASET
```

Worth investigating after initial stability exists.

---

# 4. [Nous Hermes Function Calling v1](https://huggingface.co/datasets/NousResearch/hermes-function-calling-v1?utm_source=chatgpt.com)

Mentioned in:
([Towards AI][4])

### My assessment

Potentially useful, but I am more cautious here.

The Hermes ecosystem historically trends more toward:

* assistant personality,
* conversational helpfulness,
* general assistant tuning.

That is not inherently bad — but your project is unusually disciplined.

### Risks

* conversational bleed
* markdown verbosity
* “assistant vibes”
* shell/prose fallback tendencies

### Possible use

Maybe:

```text id="t9uqz7"
filtered instruct-alignment substrate
```

but probably not primary tool-call data.

---

# 5. When2Call + xLAM together

This combination actually stands out to me.

Because together they cover:

## xLAM/APIGen

```text id="nqmf8d"
how to call tools correctly
```

## When2Call

```text id="o1qv60"
when NOT to call tools
```

That combination is unusually aligned with your charter.

---

# Datasets I would be cautious about

## Generic ShareGPT derivatives

Unless aggressively filtered:

```text id="vwnu0v"
too conversational
too markdown-heavy
too personality-oriented
```

---

## Massive synthetic agent datasets

Risk:

```text id="yks0t9"
tool-happy behavior
multi-step overengineering
hallucinated planning
```

---

## CoT-heavy tool datasets

Your charter explicitly disfavors hidden reasoning traces.

Many modern agent datasets now include:

* reasoning,
* scratchpads,
* hidden planning,
* chain-of-thought.

Codex needs to filter aggressively.

---

# One thing I think you should explicitly authorize

I think Codex should be allowed to:

```text id="uq8lxu"
extract subsets
filter aggressively
convert schemas
build hybrid datasets
```

rather than treating external datasets as monoliths.

That is probably the right architecture.

---

# My current strategic recommendation

If this were my project, I would probably pursue:

## Stage A — Runtime Instruct Alignment

Likely:

* mostly in-house
* plus carefully filtered structured-output/instruction data

Goal:

```text id="3bkr5f"
teach disciplined runtime behavior
```

---

## Stage B — Tool Calling

Primary candidates:

### Core:

```text id="cty5n8"
xLAM/APIGen
```

### Supplemental:

```text id="5xkuyj"
When2Call
```

### Possibly later:

```text id="w0p7w9"
ToolACE subsets
```

---

# Most important insight from this search

I think your instinct was correct:

```text id="c24h40"
You probably do NOT have enough in-house data alone.
```

But I also think your caution was correct:

```text id="rr4xk0"
Blindly ingesting public tool datasets would be dangerous.
```

The right answer is probably:

```text id="sc0fzf"
carefully curated hybridization
```

not:

* pure in-house,
* nor pure public-dataset ingestion.

[1]: https://arxiv.org/abs/2406.18518?utm_source=chatgpt.com "APIGen: Automated Pipeline for Generating Verifiable and Diverse Function-Calling Datasets"
[2]: https://github.com/NVIDIA/When2Call?utm_source=chatgpt.com "NVIDIA/When2Call: A dataset for training and evaluating ..."
[3]: https://openreview.net/forum?id=8EB8k6DdCU&utm_source=chatgpt.com "ToolACE: Winning the Points of LLM Function Calling"
[4]: https://pub.towardsai.net/fine-tuning-open-source-models-for-function-calling-a-complete-guide-with-unsloth-and-docker-0a5501d7a08c?utm_source=chatgpt.com "Fine-Tuning Open Source Models for Function Calling"
