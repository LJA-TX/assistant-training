# Stage B First Probe Sampler Hook Fix Recommendation

## Recommendation
`SIGNATURE_FIX_ONLY`

## Why
- Failure is caused by one localized mismatch:
  - custom hook: `_get_train_sampler(self)`
  - installed Trainer invocation: `sampler_fn(dataset)`
- Installed Transformers (`5.9.0`) defines base signature with optional dataset arg.
- No evidence of data contract, loss-path, or broader Trainer integration defects.

## Minimal Fix Shape
- Update custom hook signature in `_GeometrySamplingTrainer` to accept the dataset argument expected by current Trainer invocation.
- Keep sampler construction logic and determinism controls unchanged.
- Keep exposure ledger schemas and artifact wiring unchanged.

## Why Not Other Options
- `COMPATIBILITY_WRAPPER`:
  - optional for multi-version hardening, but not required to resolve this failure in the current environment.
- `BROADER_TRAINER_REFACTOR`:
  - not justified by current evidence; issue is narrow and reproducible as a signature mismatch.

## Post-Fix Verification Targets (for later implementation phase)
1. Training starts past dataloader construction.
2. No tensor contract changes.
3. No loss-path changes.
4. Weighted sampler determinism metadata unchanged.
5. Realized/drift exposure artifacts emitted via normal runtime path.
