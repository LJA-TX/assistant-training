# ASSISTANT-TRAINING CONTINUITY DOCUMENT

## Post-Topology Closure / Pre-Publication Update Baseline

### Date: 2026-06-14

---

# Project Identity

Repository:

```text
https://github.com/LJA-TX/assistant-training
```

Canonical worktree:

```text
/opt/ai-stack/assistant-training
```

Current branch:

```text
main
```

Current published tip:

```text
ec0bc3a
```

Repository status:

```text
## main...origin/main
```

Clean.

Synchronized.

No outstanding experimental debt.

---

# Current Project Objective

The project is no longer primarily:

```text
Fine-tune Llama-3.1-8B for better tool calling
```

The broader objective has become:

```text
Develop a reusable scientific training regimen
for discovering, validating, reproducing,
and explaining tool-use capability improvements
in foundation models.
```

The training regimen itself is increasingly the product.

Improved models are important outputs, but the methodology now has equal or greater value.

---

# Major Findings To Date

## External Baselines

Benchmarks completed:

```text
Llama-3.1-8B-Base
Llama-3.1-8B-Instruct
Llama-3.1-8B-Instruct-NVFP4
```

All sit at the canonical exact-tool floor:

```text
exact JSON = 0.0
tool-name = 0.0
argument = 0.0
```

while preserving:

```text
no-call = 1.0
```

and:

```text
adversarial no-call = 1.0
```

Interpretation:

```text
NVFP4 quantization does not appear to be the cause
of missing tool-call capability.

Instruct and NVFP4 are behaviorally equivalent
on the frozen canonical contract.
```

---

## H-Series

H1 and H2 remain the strongest results in the repository.

H1:

```text
exact JSON = 0.44
tool-name = 0.714
argument = 0.629
```

H2:

```text
exact JSON = 0.48
tool-name = 0.771
argument = 0.693
```

H2 remains the highest-performing run ever recorded.

These runs define the only clear high-capability regime in the project.

---

# Completed Investigations

## Phase I

Hypothesis sweep.

Result:

```text
H1 and H2 succeeded.
```

Formal attribution:

```text
inconclusive_external_first
```

but evidence strongly indicates H1/H2 captured a real phenomenon.

---

## Dataset v1.1

Phases:

```text
K
L
M
N
```

Result:

```text
Safety preserved.
Capability collapsed.
```

Root cause attributed primarily to dataset shape and signal dilution.

---

## Dataset v1.2

Phases:

```text
O
P
Q
R
S
T
U
V
```

Result:

```text
Partial recovery only.
```

Schema repair alone was not sufficient.

---

## Anchor Concentration Investigation

Phases:

```text
W
X
Y
Z
ZA
ZB
ZC
ZD
```

Result:

```text
Anchor concentration is contributory
but not sufficient.
```

Best exact JSON:

```text
0.085
```

Still far below H1/H2.

---

## Topology Investigation

Phases:

```text
ZE
ZF
ZG
ZH
ZI
ZJ
ZK
```

Result:

```text
Topology hypothesis weakened.
```

Topological variation affects metrics but cannot explain H1/H2.

Formal classification:

```text
Weakened
```

---

# Current Project-Wide Comparison

| Regime        | Exact JSON |
| ------------- | ---------: |
| Base          |        0.0 |
| Instruct      |        0.0 |
| NVFP4         |        0.0 |
| H0            |      0.045 |
| Phase Q       |       0.03 |
| Phase U       |        0.0 |
| Anchor Best   |      0.085 |
| Topology Best |       0.05 |
| H1            |       0.44 |
| H2            |       0.48 |

Interpretation:

```text
H1/H2 remain unique.

No later intervention has recreated
the H1/H2 capability regime.
```

---

# Current Causal Frontier

Per Phase ZK:

```text
Schema realization
Exact tool_calls envelope normalization
```

is now the highest-information unresolved target.

Anchor concentration:

```text
Contributory
```

Topology:

```text
Weakened
```

Schema-only repair:

```text
Not supported
```

The remaining question is:

```text
What preserved the H1/H2 realization regime?
```

---

# Public Repository Status

Phase ZK readiness assessment:

```text
READY
```

Public-update rationale:

* Topology branch closed.
* Anchor branch closed.
* External baselines complete.
* Repository normalized.
* Project-wide comparison established.
* Clear next causal target identified.

Current recommendation:

```text
Publish milestone update
before beginning the next major experiment.
```

---

# Workflow

Continue established cadence:

1. Codex performs implementation work.
2. ChatGPT evaluates results.
3. Grok / Composer used for independent review when useful.
4. Prefer evidence over intuition.
5. Follow data even when results are inconvenient.
6. Maintain governance discipline.
7. Keep publication hygiene high.

---

# Immediate Next Priority

Primary:

```text
Prepare public repository update package.
```

Secondary:

```text
Begin planning the next schema-realization /
tool_calls-envelope investigation.
```

Do not reopen:

```text
Anchor sweep
Topology sweep
```

unless new evidence emerges.

Both investigations are considered closed.

---

# Most Important Lesson Learned

The project has repeatedly demonstrated that:

```text
tool-use capability can exist
without being present in the base model,
the instruction-tuned model,
or the production NVFP4 deployment model.
```

The challenge is no longer proving that the capability exists.

The challenge is understanding precisely why H1/H2 produced it and how to reproduce it reliably.

