# Thread Summary Document

## Assistant Tool-Calling Post-Training Project — Initial Probe Work

### 1. Project Purpose

This thread began as a design discussion for post-training / fine-tuning local models, initially focused on Llama 3.1-8B and Llama 3.2-3B. The immediate working objective became:

> Build a controlled LoRA/QLoRA training workflow that can teach a local model to emit assistant-runtime tool calls in strict canonical JSON format.

The project quickly narrowed to an empirical first probe using Llama-3.2-3B-Instruct, because it offered the fastest path to a measurable result.

---

## 2. Major Design Decisions

### Model strategy

We discussed the tradeoff between starting from base models versus Instruct models.

The final near-term decision was:

- Use Llama-3.2-3B-Instruct for the first pipeline probe.
- Use Llama 3.1-8B as the likely stronger target for the next serious goal-oriented effort.

The 3B-Instruct run was not expected to produce production behavior. It was intended to prove the machinery.

### Training method

The project used:

- QLoRA
- LoRA adapter-only save
- No adapter merge
- Assistant-completion-only loss
- Tokenizer-native chat-template prompt serialization
- Explicit label masking

The goal was not broad chatbot improvement. It was narrow runtime behavior:

- user request → correct tool-call JSON

---

## 3. Dataset Construction

Codex first found older prepared fine-tune data, but it was too narrow and heavily upsampled. It then built a broader positive-only dataset from assistant-runtime reports.

The dataset evolved through several gates.

### v0.0 / v0.1 seed

Initial broad positive dataset:

- 82 rows
- 26 tools
- 44 case IDs
- no contrastive negatives
- valid canonical JSON

Problem: most non-read_file / rg_search tools only had explicit tool-name prompts.

### Inferred natural-language augmentation

Codex added:

- 120 inferred rows
- 5 inferred examples for each of 24 under-covered tools
- total: 202 rows
- explicit: 52
- inferred: 150

A semantic audit found one mismatch involving overwrite=false versus mode:"overwrite"; that row was corrected.

### Grouped train/val split

Codex produced a grouped split:

- train: 162 rows
- val: 40 rows
- train tool coverage: 26/26
- val tool coverage: 8/26
- duplicate target leakage: 0
- source_case_id leakage: 0

This was sufficient for a first probe but not a full all-tool evaluation.

---

## 4. Separate Training Repo

Codex created a separate training repository:

/opt/ai-stack/assistant-training

This separated training concerns from production runtime concerns.

Repo scope:

- configs/lora/
- manifests/runs/
- scripts/
- tests/
- artifacts/
- docs/
- data/

The repo layout and migration checklist established that assistant-training owns training configs, manifests, scripts, adapter artifacts, and evaluation handoff, while production runtime/tool execution remains in assistant-runtime.

---

## 5. Trainer Implementation

Codex implemented:

scripts/train_lora_sft.py

Key properties:

- Reads JSON config
- Finds matching run manifest
- Enforces approval gate
- Loads tokenizer/model
- Uses tokenizer.apply_chat_template
- Uses explicit assistant-only label masking
- Supports QLoRA NF4
- Applies PEFT LoRA
- Saves adapter only
- Writes resolved_config.json
- Writes masking_audit.json
- Writes training_summary.json

Important fixes during review:

- Removed hardcoded Llama prompt markers
- Used tokenizer-native chat templates
- Disabled manual BOS injection in tokenizer_chat_template mode
- Added --masking-audit-only
- Allowed preflight-only run_root reuse
- Verified actual Llama tokenizer masking

The final masking audit showed correct native Llama chat-template serialization, no manual BOS, EOS appended, and supervision only over the assistant target JSON.

---

## 6. v0.1 Training Run

The first training run completed successfully.

Result:

- status: completed
- train rows: 162
- val rows: 40
- runtime: ~27.7s train
- eval runtime: ~2.2s
- train loss: 1.8271
- eval loss: 1.8210
- adapter saved

A final run manifest snapshot was created showing:

- status: completed
- training_started: true
- training_completed_utc populated
- approved_to_run: true
- approved_by: Roy Sikes

This proved the end-to-end training pipeline.

---

## 7. v0.1 Evaluation

Codex implemented:

scripts/eval_adapter_toolcalls.py

The harness compares:

- base model
- base + adapter

on identical prompts and reports:

- strict JSON validity
- tool-name accuracy
- argument accuracy
- wrapper/prose leakage
- no-call behavior if applicable
- failure categories

### Initial val40 evaluation

Result:

- Base: 0/40 exact JSON, 0/40 tool-name, 0/40 args
- Adapter: 0/40 exact JSON, 0/40 tool-name, 0/40 args

Both mostly failed as invalid_json.

### Train40 diagnostic

Result:

- Base: 0/40
- Adapter: 0/40

This showed the adapter had not even learned the training-row shape.

### Strong-system-prompt val40 diagnostic

Result:

- Base: 3/40 exact JSON
- Adapter: 2/40 exact JSON
- Both: 0/40 tool-name and argument accuracy

The stronger prompt slightly improved JSON-shape emission but did not yield semantic tool-call accuracy.

Conclusion:

> v0.1 proved the engineering pipeline, but did not produce usable tool-call behavior.

---

## 8. v0.2 Preparation

Based on the v0.1 failure, Codex prepared v0.2 artifacts.

Changes:

- Strict tool-call emission system prompt
- Same user prompts
- Same assistant targets
- Same metadata/group membership
- LoRA r=16
- alpha=32
- dropout=0.05
- 3 epochs
- learning_rate=1e-4
- target modules expanded:
  - q_proj
  - k_proj
  - v_proj
  - o_proj
  - gate_proj
  - up_proj
  - down_proj
- QLoRA NF4 preserved
- assistant-only masking preserved
- adapter-only save preserved

The v0.2 train dataset has:

- 162 rows
- 0 schema errors
- 26 tools covered in train

The v0.2 val dataset has:

- 40 rows
- 0 schema errors
- 8 tools represented

Semantic consistency checks showed:

- train suspect_count=0
- val suspect_count=0

The v0.2 masking audit confirmed the strict system prompt was actually present in the serialized prompt, and that only the assistant JSON target was supervised.

The v0.2 manifest remains approval-gated and untrained.

---

## 9. Current State at Thread End

### Completed

- Training repo scaffold
- Dataset builder/audits
- v0.1 dataset
- v0.1 grouped split
- Trainer backend
- Masking audit mode
- Approval-gated training
- v0.1 LoRA training run
- Evaluation harness
- v0.1 behavioral diagnostics
- v0.2 training artifacts
- v0.2 validation-only checks

### Not yet completed

- v0.2 training run
- v0.2 train10/train40/val40 diagnostics
- External dataset review/selection
- Llama 3.1-8B training campaign
- Codex /goal conversion

### Important lesson

The project proved the mechanics but not yet the behavior.

The next serious effort should target a stronger model, likely Llama 3.1-8B, and probably needs external function/tool-call training data after license, quality, schema, and contamination review.

