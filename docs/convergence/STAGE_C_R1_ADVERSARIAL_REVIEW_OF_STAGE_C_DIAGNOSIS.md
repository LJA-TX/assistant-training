# Stage C R1 Adversarial Review of Contamination Diagnosis

**Date**: 2026 (review conducted on available frozen artifacts)
**Reviewer posture**: Independent adversarial. Evidence examined; current working diagnosis (as summarized in the query and in R1A/R1B) tested for falsifiability. No assumption that the diagnosis is correct.
**Scope**: Strictly the three provided Stage C convergence artifacts plus their cited primary sources (runtime forensics JSON, legacy validity JSON, blocker persistence JSON, C4 sample records + contract artifacts, eval_canonical_manifest.py predicate logic, representative tool fine-tune data, direct_answer eval split, and related Stage C/B narratives). Read-only. No new runs.

## Evidence Base Reviewed (Primary, Not Just Summaries)

- `docs/convergence/STAGE_C_RECONNAISSANCE_AND_EVIDENCE_INVENTORY.md`
- `docs/convergence/STAGE_C_R1A_RUNTIME_REGIME_CHARACTERIZATION_ASSESSMENT.md`
- `docs/convergence/STAGE_C_R1B_CONTAMINATION_ORIGIN_ASSESSMENT.md`
- `manifests/reports/stage_c_runtime_output_forensics_direct_answer_missing_evidence_assessment.json` (134-row classification, categories, excerpts, predicate observations)
- `manifests/reports/stage_c_legacy_surface_validity_direct_answer_assessment.json` (125-row legacy overlap, 100% mapping to missing-evidence, taxonomy)
- `manifests/reports/stage_c_package5b_direct_answer_blocker_persistence_assessment.json` (repeated-run identity and blocker stability)
- `reports/stage_c4/input/stage_c4_sample_output_records.jsonl` + `c4_output_inventory_artifact.json` (operational variety sample)
- `scripts/eval_canonical_manifest.py` (core: `_looks_like_tool_intent`, `_stage_c_family_a_declared_subtype`, `_failure_subtype` / legacy direct_answer logic, `_stage_c_scalar_substitution_candidate`)
- `data/tool_ft_allaliases_20260525_from_qual_reports.jsonl` (source of the exact echoed system instruction)
- `evals/data/canonical_v1/direct_answer.jsonl` (separate clean direct-answer eval set with different system prompt)
- Supporting narratives: forensics investigation, legacy surface validity assessment, Package 5C subtype completeness, various Stage C package runtime validation reports, blocker persistence.
- Cross-references in goal_charter, Stage B eval redesign contracts, and training configs (chat template / prompt_template usage).

**Key quantitative anchors** (stable across repeated-run bundles and forensics):
- Tool-expected non-exact rows under focus: 140.
- Authoritative missing-evidence: 134 (131 structurally incapable + 3 ambiguous).
- Subtype-assigned (malformed output): 6.
- Authoritative direct-answer or scalar-substitution in this cohort: 0.
- Legacy direct_answer_substitution: 125, with 125/125 overlap to the authoritative missing-evidence rows and 0 overlap to authoritative positive subtypes.
- Dominant regime per forensics taxonomy: "prompt/task echo with transcript contamination" — 116/134.
- All 40 tool_holdout rows fall inside the dominant echo regime.
- Transcript markers (`[SYSTEM]`, `[USER]`): 132/134.
- Primary class for all 134: invalid_json; parse_mode: invalid; schema_reason: payload_not_parsed.
- 0 missing-evidence rows satisfied the live tool-intent predicate.
- 0 satisfied the bounded scalar-substitution candidate predicate.
- C4/C5/C6 operational sample: 8 records (one per illustrated failure/success shape); deliberately small and diverse, not a rate sample for the 134.

## Core Definitions (From Code and Doctrine, Not Assumption)

**Authoritative (scorer-owned, Family A) path** (`_stage_c_family_a_declared_subtype`):
- invalid_json + `_looks_like_tool_intent(generated)` → "malformed output".
- Otherwise for invalid_json → missing_evidence ("current canonical evaluator does not emit approved direct-answer or scalar substitution evidence").
- invalid_schema + narrow `_stage_c_scalar_substitution_candidate` (specific primary_class/schema_reason + no tool-intent + parses as unambiguous scalar) → "scalar substitution".
- Most other invalid_schema cases → missing or malformed.
- The predicates are intentionally narrow and do not fall back to broad text heuristics or legacy-style interpretation. "Governed" here means scorer-owned observable evidence meeting these shapes.

**Legacy path** (`_failure_subtype`):
- For non-exact tool-expected invalid/parse failures: number/bool/null → scalar; starts with {/[ or looks_like_tool_intent → malformed_partial_json; else → "direct_answer_substitution".
- This is a broad evaluator-owned lexical fallback for evidence-poor invalid outputs.

**"Clean governed direct-answer population"** in context: A positive authoritative subtype (direct-answer substitution or scalar) that would be emitted for rows in the tool-expected non-exact denominator under the current narrow scorer semantics. The legacy surface previously counted many more via the fallback.

The 134 are defined by failing to cross the authoritative predicates on their emitted text.

## Concrete Examples of Dominant Regime (From Forensics JSON + Investigation Excerpts)

Dominant (task/prompt echo + transcript):
- `heldout_validation:1`: "Show /opt/ai-stack/runtimes/assistant-runtime/server/agent.py starting at line 1080 for 25 lines and report one symbol name.\n[SYSTEM]\nUse ONLY the exact tool requested. Keep final answer concise. If a tool result already answers the task, stop and finalize...."
- Similar for dozens of rg_search / read_file / find_files cases across heldout_validation and *all* 40 tool_holdout.
- The echoed system instruction is *identical* to the system message in `data/tool_ft_allaliases_20260525_from_qual_reports.jsonl` training-style messages (paired there with clean tool_calls assistant turns).

Pure transcript: outputs starting directly with `[SYSTEM]\nUse ONLY...` + prior user task.

Instructional assertion + transcript (minority, rg_search only): "Tool validation is not required for this task.\n[SYSTEM]..." or "Tool parse mode is enabled..."

Answer-prefix + transcript (the 3 ambiguous, all heldout_validation rg_search): "The first function name is: main\n[SYSTEM]\nUse ONLY..."

Tool-label repetition (singleton): repeated "Tool: python\n..." without payload.

In contrast, the small C4 operational sample includes:
- Clean strict tool call JSON.
- Wrapped prose + JSON ("I will call the tool now. {json} trailing prose").
- Missing `tool_calls` key or partial args.
- `{"tool_calls": []}` when no-call expected.
- `{"message": "tool call omitted"}`.
- Invalid JSON with embedded object.

Model *can* emit other regimes; the 134 cohort's outputs are a distinct, heavy echo cluster.

## Supported Conclusions (Strong, Hard to Falsify With Current Evidence)

1. The 134-row authoritative missing-evidence outputs are dominated by literal prompt/task echo immediately followed by chat-transcript markers (`[SYSTEM]`, `[USER]`) and the specific tool-use system instruction. 116/134 fall into one descriptive category; the taxonomy partitions the cohort cleanly.

2. Zero of the 134 satisfy the current authoritative live tool-intent lexical predicate or the narrow scalar candidate predicate. All are invalid_json / payload_not_parsed.

3. The legacy `direct_answer_substitution_count` (125) has 100% row overlap with the authoritative missing-evidence set and 0 overlap with authoritative positive subtypes for this surface. It is primarily counting the same evidence-poor echo outputs via a loose lexical fallback, not a hidden clean positive class. Semantic misalignment is strongly evidenced.

4. The blocker (row identities + output shapes producing the missing-evidence cohort) is strongly reproducible across repeated full runs (identical row sets, blocker inventory, legacy snapshots; key comparison and evidence digests match).

5. The 3 ambiguous rows are mixed (answer-like prefix + the same transcript contamination scaffold). They are boundary cases of the dominant regime on the observed text, not a separate clean direct-answer subpopulation. All three are heldout_validation + rg_search.

6. The small operational (C4/C5/C6) sample demonstrates that multiple output shapes exist in the broader runtime (clean tool calls, omissions, wrapper leakage, malformed, no-call restraint failures, etc.). Output shape is locally descriptive there.

7. Split is a real correlate: 100% of the 40 tool_holdout rows are inside the dominant echo regime; some minority motifs (pure transcript, answer-prefix) are heldout_validation-only.

8. The "authoritative missing-evidence" label and count for this surface are the direct result of applying the narrow scorer-owned predicates in `eval_canonical_manifest.py` to these specific emitted texts. The legacy surface used a broader bucket.

## Tentative Conclusions (Plausible but Inference-Heavy; Evidence Supports Directionally but Not Exclusively)

1. "Contamination motif" (prompt/task echo + transcript markers + occasional meta-instruction or answer-prefix) is the strongest descriptive partition of the 134-row cohort among the variables examined (split secondary; tool family weak; output shape strong locally in the tiny sample).

2. The markers in the outputs (exact system instruction from tool_ft SFT data + role delimiters) are consistent with chat-template serialization and prompt-template reuse. The echoed task text is consistent with source task data being replayed.

3. There is no large hidden clean governed direct-answer or scalar population *inside the examined 134-row missing-evidence cohort* under current definitions. The negative (0) is stable across forensics, technical spike (0 delta), and persistence checks.

4. The model exhibits regime variety across fixtures; the heavy echo is concentrated in the specific non-exact tool-expected rows that became the missing-evidence set (especially tool_holdout).

## Unsupported or Overclaimed Conclusions (Current Diagnosis Does Not Survive Scrutiny Here)

1. **"Corpus-construction contamination is the most likely upstream mechanism" (moderate confidence claimed in R1B)**:
   - The symptom (outputs containing serialized chat + exact training-style system instruction + task text) is real.
   - The tool_ft data artifact shows the instruction lives in (contrastive + canonical) tool-use message lists. This is positive evidence for a data-format / SFT construction contribution.
   - However, "most likely upstream" and the weighting toward "corpus-construction" over other loci is under-supported. The artifacts do not include the *exact prompt text sent to the model at inference* for these 134 rows (only references like "prompt://a-c-xxx" and the generated outputs). Without that, one cannot distinguish:
     - Training/SFT corpus construction (data that taught replay of chat prefixes).
     - Eval-time prompt renderer / harness construction (how the frozen fixtures + chat template were turned into the actual generation input for baseline-model-v0).
     - Model-level failure mode (the adapted model defaults to context continuation / transcript replay on these phrasings or when tool format following fails).
   - The claim is a reasonable inference but not the uniquely best-supported causal story from output-only + training-data-marker evidence.

2. **"Detector, scorer, evaluator, or reporting behavior is likely downstream of the contamination regime rather than the primary cause"**:
   - The *characterization* of the outputs as echo/contamination is independent of the detector/scorer (the forensics read the raw generated_text and applied descriptive clustering).
   - However, the *existence, size, and "blocker" status of the authoritative missing-evidence cohort* (134 rows requiring future migration) is directly produced by the authoritative subtype logic: for invalid_json without the narrow tool-intent lexical signal, it explicitly emits the missing_evidence reason instead of any direct-answer or scalar label. The legacy logic did the opposite for the same texts.
   - The "governed" bar (scorer-owned, narrow predicates only) is a Stage B/C redesign choice. The large missing cohort is co-determined by (a) what the model emitted on these fixtures and (b) what the new surface definition accepts as positive evidence. Treating the contamination as fully prior and the surface mechanics as merely "downstream" understates the definitional contribution to the observed "missing-evidence" phenomenon and the reconciliation blocker.
   - The technical spike (bounded scorer change → 0 delta) shows that *within the current narrow authoritative rules*, small scorer tweaks did not surface new evidence. That supports "the outputs themselves lack the required shapes," but does not prove the rules could not have been drawn differently or that the model would have produced clean governed substitutes under different conditioning.

3. **"The frozen corpus does not contain a clean governed direct-answer population" (as a global or strong negative)**:
   - Correctly scoped: inside the 134-row tool Family A non-exact missing-evidence cohort under current predicates, yes.
   - There *exists* a separate `evals/data/canonical_v1/direct_answer.jsonl` with clean prose direct answers under a different system prompt ("You are a runtime assistant. Be concise..."). The direct_answer split is explicitly noted as outside the tool-expected Family A denominator for this surface. The claim is therefore scoped, not a corpus-wide absence of direct-answer capability or data.
   - The model *did* emit answer-like prefixes in the 3 ambiguous cases (e.g., "The first function name is: main"), suggesting it can begin content responses on some tasks before transcript markers appear. These were still classified as mixed contamination, correctly per the text, but they are the closest observed approach to "direct" in the cohort.

4. Minor overclaim: Treating the 8-record operational sample as strong evidence that "output shape is highly informative" for the full regime. It usefully shows variety exists; it does not support population rates or replace the 134-row contamination-motif taxonomy.

## Alternative Hypotheses That Fit the Evidence (Plausible and Not Ruled Out)

1. **Model tool-calling fragility + transcript-replay bias (strongest alternative or co-equal explanation)**:
   - The baseline-model-v0 (post whatever adaptation) reliably emits strict tool JSON only on in-distribution or "easy" prompts. On the specific task phrasings, long contexts, or tool_holdout distribution, its failure mode is to continue the sequence it was shown (user task + the chat-serialized system instruction it saw in training data and/or the inference prompt). This is standard autoregressive behavior, not mysterious "contamination." The exact match to the tool_ft system message supports that the model saw this text in a chat format during adaptation and sometimes replays the prefix when uncertain about emitting a clean assistant turn.
   - Explains why *all* tool_holdout are uniform echo, why the instruction text recurs verbatim, and why other fixtures (per C4 sample) produce clean calls or different errors.
   - Predicts that changing prompt formatting, adding stronger format enforcement, or further targeted adaptation would change the regime more than "cleaning the corpus."

2. **Eval-time prompt construction / harness serialization for the frozen fixtures is the proximate source of the replayed transcript**:
   - The outputs contain role markers and the training system instruction because the generation prompt for these rows (built via whatever prompt:// resolution + chat template application in the harness) included them, and the model continued the transcript. The "frozen" outputs reflect a fixed prompt-builder + model combination. This is "construction" but at the point of *running the eval on the frozen set*, not necessarily an upstream training-corpus defect. Without the exact rendered prompt for the 134 vs. the clean cases, this cannot be distinguished from training-data issues.

3. **Surface-definition artifact + legacy vs. authoritative mismatch drives the "blocker" narrative more than raw model behavior**:
   - The 134 "missing" and the reconciliation blocker exist because the authoritative rules refuse to label these echo outputs as any positive subtype (by design: only narrow scorer-owned evidence counts). The same texts were previously bucketed as legacy direct_answer_substitution. If the doctrine had retained a broader "other invalid tool-expected" or "direct answer attempt" category (or relaxed the predicate), the missing cohort and blocker would shrink or disappear without any change to the model outputs. The contamination diagnosis correctly describes the texts; it does not fully explain why the *governance surface* treats them as a large persistent missing-evidence problem.

4. **Task / split construction for tool_holdout (and some heldout_validation) specifically elicits context-replay**:
   - These cases may have been derived from full transcripts, contrastive pairs, or long-context examples where the "user" content was embedded inside prior turns. The model treats the input as "continue this transcript" rather than "now produce a standalone assistant tool call." The uniform membership of all 40 tool_holdout in the dominant regime is consistent with a split-level prompt or data construction difference.

5. **Partial generation or capture artifact for the answer-prefix cases**:
   - The 3 ambiguous rows begin with a plausible content answer to the embedded question ("first function name is: main") then immediately transcript. This could reflect the model starting a direct response then the generation or post-capture process including additional context (bad stop conditions, echo in the runtime, or how raw responses were bundled in the spike/forensics artifacts). Less likely to explain the pure-echo majority, but relevant to whether the 3 are "remediable" vs. further evidence of the same replay mechanism.

6. **Insufficient distinction between training chat format and inference tool-call format**:
   - Training data uses `{"role": "system", ...}, {"role": "user", ...}, {"role": "assistant", "tool_calls": ...}`. If inference for eval uses a similar chat template but the model was not sufficiently trained to *stop* after the assistant role and emit only the tool_calls object (or the harness expects raw JSON without role markers), the model can emit role markers or replay the prefix. The presence of the markers in *generated* text is evidence the format boundary was not sharp for this model on these inputs.

None of these alternatives contradict the observed output texts or the 0 clean positives under current predicates. Several are at least as parsimonious as "mixed-source corpus-construction contamination as primary upstream" once one distinguishes descriptive regime from causal locus.

## Answers to the Eight Questions

1. **What conclusions are strongly supported by evidence?**
   The descriptive regime (echo + transcript markers dominate the 134; legacy surface misalignment is 100%; 0 clean governed positives per authoritative predicates in the cohort; repeated-run stability of the blocker row set and shapes; the 3 ambiguous are still contaminated; operational variety exists outside the cohort). The predicate logic in the evaluator script and the exact match of echoed text to tool_ft training data are directly verifiable.

2. **Which conclusions are only weakly supported?**
   The specific weighting that "corpus-construction contamination is the most likely upstream mechanism." The clean separation that "detector/evaluator/scorer behavior is downstream rather than contributory to the size of the missing-evidence phenomenon." Claims that the ambiguous rows or any edge case represent a distinct remediable clean subpopulation (they remain mixed on the text).

3. **What alternative explanations fit the evidence?**
   See the six alternatives above. The strongest are model replay bias on chat-formatted tool prompts (supported by the training data artifact + uniform tool_holdout behavior) and surface-definition choices co-producing the "blocker" (supported by direct comparison of `_stage_c_family_a_declared_subtype` vs `_failure_subtype` on the same invalid texts).

4. **Are there plausible explanations that Codex has overlooked?**
   Yes. The review did not appear to deeply inspect (or at least did not surface in the R1A/R1B summaries) the exact inference-time prompt construction for the 134 rows, the difference in system prompts between the tool_ft / eval tool cases vs. the separate direct_answer eval set, or the possibility that "replay of training chat prefix" is a predictable LM failure mode rather than an anomaly requiring "contamination" remediation. The training data artifact containing the exact echoed instruction is under-leveraged for distinguishing training-corpus vs. eval-prompt vs. model-adaptation explanations. The explicit "does not emit approved..." missing_evidence reason in the authoritative code is treated more as a neutral observation than as a definitional contributor to cohort size.

5. **Is the mixed-source contamination diagnosis justified?**
   Yes, descriptively: multiple marker families (role delimiters, repeated exact system instruction, task text, occasional meta-instruction or answer prefix, rare tool-label loops) co-occur and no single marker explains the whole cohort. The diagnosis is justified as a description of the *output texts*. It is weaker as a causal diagnosis of a single "contamination" process.

6. **Is corpus-construction contamination truly the most likely upstream mechanism?**
   Plausible and supported by the presence of the exact instruction in tool fine-tune message data, but not demonstrated as "most likely" over alternatives. The evidence is the *symptom in the outputs* plus one matching data artifact. Direct evidence of the construction step (which messages were serialized how, at training time vs. at the frozen eval run time) is absent from the reviewed artifacts. Prompt/harness construction at eval time and model continuation bias fit the same markers at least as well.

7. **Could detector, evaluator, scorer, threshold, or reporting behavior still explain the observations better than the contamination hypothesis?**
   They do not explain the *content* of the outputs (the echo texts are in the raw generated_text before scoring). They do substantially explain the *mapping of those outputs to "missing-evidence cohort of 134" and the reconciliation blocker*. The authoritative rules were deliberately drawn narrowly; the same outputs were previously interpreted (via legacy) as direct_answer_substitution. The "overwhelming majority" missing-evidence claim is true under the current rules; the rules themselves are part of why the number is large and why "clean governed" positives are absent by construction for these texts. The contamination hypothesis is better for *why the model emitted these particular strings*; the surface mechanics are better for *why this produces a large authoritative missing-evidence / migration-blocked state*.

8. **What evidence would most strongly strengthen or weaken the current diagnosis?**
   **Strengthen**: (a) The exact rendered prompt (including any chat template application and history) that was sent to the model for a sample of the 134 echo rows vs. clean tool-call rows; (b) provenance showing these exact task texts + the system instruction were injected during a specific corpus-construction step rather than being the natural inference prompt for the fixture; (c) an ablation where the same fixtures are re-run with a prompt variant that strips transcript markers or uses a non-chat completion format and the echo regime shrinks while clean tool or clean direct-answer rises.
   **Weaken / falsify**: (a) Discovery that the rendered inference prompts for the echo rows already contained the full transcript markers and task text (pointing to harness/prompt-builder or model continuation rather than "corpus" per se); (b) a controlled change to model prompting, decoding, or light adaptation that produces clean tool calls or clean direct answers on the same frozen row facts without changing any training corpus; (c) a broader authoritative subtype definition (or a "non-exact tool failure" bucket) that absorbs most of the 134 without requiring new model outputs, showing the "blocker" was largely definitional; (d) positive examples, inside the current non-exact tool-expected set, of clean prose direct answers or narrow scalars that the current predicates simply failed to credit (undermining the "no clean population" claim).

## Overall Assessment

The observational core of the Stage C R1 diagnosis survives adversarial review with high confidence: the frozen outputs for the authoritative missing-evidence cohort on this surface are dominated by prompt/task echo with transcript contamination; the legacy surface was counting those same outputs under a misleading label; there are no clean governed direct-answer or scalar positives inside that cohort per the current narrow authoritative rules; the blocker is stable.

The causal story — mixed-source with corpus-construction contamination as the primary upstream mechanism, and detector/scorer behavior as clearly downstream — is more fragile. It fits the markers but does not uniquely or most strongly explain them once one examines the evaluator predicates, the separate direct_answer eval data, the exact match to tool fine-tune system text, the uniform tool_holdout concentration, and the absence of the actual inference prompts in the reviewed artifacts. Plausible alternatives centered on model continuation bias under chat-formatted tool prompts, eval harness prompt construction, and the definitional strictness of the new "governed" surfaces fit the same evidence and would predict different remediation paths.

The current diagnosis is a useful descriptive and diagnostic starting point. It should be treated as "the outputs look like this and the current surface does not credit them as clean evidence" rather than a settled causal account of corpus defect that can be isolated from model behavior and surface design choices. Further work that opens the actual prompt sent vs. output, or that tests prompt/model variants on the fixed row facts, would be the highest-leverage next evidence.

**Boundary**: This review did not alter any code, thresholds, migration state, or governance posture. It is an independent reading of the frozen evidence.

## References to Primary Sources (for traceability)
- Forensics JSON and investigation for 134-row taxonomy and excerpts.
- Legacy validity JSON for 100% overlap and legacy logic description.
- Blocker persistence for stability.
- `scripts/eval_canonical_manifest.py:229` (`_looks_like_tool_intent`), `537` (`_stage_c_family_a_declared_subtype`), `652` (`_failure_subtype`).
- `data/tool_ft_allaliases_20260525_from_qual_reports.jsonl` for the echoed system instruction in training-style data.
- `evals/data/canonical_v1/direct_answer.jsonl` for the separate clean direct-answer set.
- C4 contract artifacts and sample records for operational variety.
- Package 5C and related for denominator (140 non-exact tool-expected, 134 missing).

This assessment is offered to test whether the diagnosis holds under adversarial pressure. The descriptive facts are robust; several causal and priority claims are not.