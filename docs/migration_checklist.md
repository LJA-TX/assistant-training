# Migration Checklist (assistant-runtime -> assistant-training)

1. Freeze dataset inputs (train/val JSONL + split manifest/audit).
2. Copy training config + run manifest into this repo.
3. Verify model/tokenizer paths and trainer dependencies.
4. Verify assistant-only/completion-only loss behavior in trainer implementation.
5. Add/confirm contract tests:
   - canonical JSON arguments
   - `messages` schema integrity
   - tool-call shape compliance
6. Confirm no run output overwrite risk.
7. Require explicit approval gate before launching training.
8. Record adapter artifact metadata + eval summary post-run.
