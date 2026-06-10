# External Dataset Survey

## Scope

This survey covers the major tool-calling and function-calling dataset families identified during research. The goal is not to choose an ingestion list yet, but to characterize what each family is actually good for.

## Survey Summary

| Family | Purpose | Size | Provenance | Maintenance Status | License | Quality Signals | Strengths | Weaknesses |
|---|---|---:|---|---|---|---|---|---|
| Salesforce xLAM / APIGen 60k | Canonical function-calling / tool-use training data | 60k | Data collected by APIGen across 3,673 executable APIs and 21 categories | Active / maintained by Salesforce research repo activity and releases through 2025 | CC BY 4.0 | Three-stage verification: format checking, real function executions, semantic verification; human eval over 600 samples reported >95% correct rate | Strong schema discipline, broad API coverage, high confidence quality | Partial release constraints, still needs canonicalization to the runtime schema |
| Salesforce APIGen-MT-5k | Multi-turn agentic function-calling data | 5k | Automated generation pipeline for realistic multi-turn trajectories; retail and airline domains | Static research release, with published 2025 paper | CC BY-NC 4.0 | Three-stage verification; human eval over 200 sampled trajectories reported 99% success | Multi-turn behavior, policy/domain interplay, strong verification | NC license, domain skew, smaller corpus |
| ToolACE | Tool-learning / agentic tool-use corpus | 11.3k rows visible in viewer; paper describes a larger API pool and broader generated corpus | Automatic agentic pipeline with dual-layer verification | Static research release | Apache 2.0 | Rule-based and model-based verification; reports strong BFCL results | Diverse tool coverage, good fit for tool-selection breadth | More agentic and synthetic than a runtime-discipline-first corpus |
| Glaive function-calling v2 | Broad function-calling format corpus | 113k default subset | Public function-call dataset with sparse provenance detail on the card | Static public release | Apache 2.0 | Large volume, simple function-call format | Breadth and format exposure | Weak provenance detail, likely synthetic/conversational style drift |
| BFCL-related public datasets | Benchmark / evaluation suites for function calling | Multiple JSON files, benchmark-sized | Live leaderboard and benchmark releases | Maintained as benchmark assets, not as training corpora | Apache 2.0 | Multi-category benchmark coverage | Excellent for evaluation and diagnostics | Should not be treated as training data because of benchmark contamination risk |
| When2Call | Tool-decision / no-call / follow-up behavior | 15k SFT, 9k preference, plus benchmark splits | Synthetic benchmark for deciding when to call tools | Static benchmark release with scripts in GitHub | CC BY 4.0 | Explicitly targets tool-call decision making | Very strong fit for no-call correctness and runtime restraint | Does not by itself teach deep tool argument synthesis |
| ToolBench | Large-scale tool-use instruction tuning | Large-scale; dataset card classifies it in the 100k-1M range | Auto-constructed with ChatGPT tool-use data | Legacy open release | Apache 2.0 | Broad historical coverage | Useful as a legacy breadth reference | Older style, more conversational noise, higher wrapper-regression risk |

## Notes By Family

### Salesforce xLAM / APIGen

- Best used as the primary source family for strict tool-call positives.
- The verification pipeline is strong enough to support runtime-schema canonicalization.
- This is the clearest match for tool-name and argument accuracy work.

### Salesforce APIGen-MT

- Best used as a secondary multi-turn supplement.
- It is attractive for domain-sensitive dialogue and follow-up behavior.
- The NC license means it must be treated carefully if downstream reuse is expected.

### ToolACE

- Good candidate for later-stage diversity and more complex tool routing.
- Stronger as a filtered supplement than as a dominant source.

### Glaive function-calling v2

- Useful as a broad format supplement if canonicalized and aggressively filtered.
- Provenance is less explicit than the Salesforce datasets, so quality checks matter more.

### BFCL-related public datasets

- Strong benchmark assets, not training assets.
- Best used for diagnostics and contamination checks rather than ingestion.

### When2Call

- Strong supplement for the no-call / follow-up / admit-limits boundary.
- This family aligns directly with the charter's runtime-discipline emphasis.

### ToolBench

- Legacy breadth reference, not a preferred primary source.
- If used at all, it should be heavily filtered and down-weighted.

## Sources Used

- https://huggingface.co/datasets/Salesforce/xLAM-function-calling-60k
- https://github.com/SalesforceAIResearch/xLAM
- https://arxiv.org/abs/2406.18518
- https://huggingface.co/datasets/Salesforce/APIGen-MT-5k
- https://arxiv.org/abs/2504.03601
- https://huggingface.co/datasets/Team-ACE/ToolACE
- https://arxiv.org/abs/2409.00920
- https://huggingface.co/datasets/glaiveai/glaive-function-calling-v2
- https://huggingface.co/datasets/gorilla-llm/Berkeley-Function-Calling-Leaderboard
- https://huggingface.co/datasets/nvidia/When2Call
- https://huggingface.co/datasets/tuandunghcmut/toolbench-v1
