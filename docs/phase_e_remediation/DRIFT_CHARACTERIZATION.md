# Drift Characterization

## Scope

This document characterizes the evaluator-contract drift between the manifest pin and the current canonical evaluator.

## Evidence Summary

- Manifest scorer pin: `80af75c494e0da59f30f33a910997b5fdff15d4ffa8dca09988cdedc0fc06e3f`
- Current evaluator hash: `08a5cec22a781193365bed85b709ceebef534846602004bbfa047f4e0b59d738`
- Current evaluator file: `scripts/eval_canonical_manifest.py`

## Hash Lineage

| Commit | Date | Script SHA-256 | Observed change |
|---|---|---:|---|
| `7b694fb` | 2026-05-26 | `80af75c494e0da59f30f33a910997b5fdff15d4ffa8dca09988cdedc0fc06e3f` | Manifest-pinned baseline |
| `9124324` | 2026-06-03 | `3ca7069263ff2e9ffb929d2c9d51491a4e6c6f93655133d1dc224278b493b4b0` | Restored detector-facing eval surfaces |
| `19f126d` | 2026-06-04 | `6d25cab905b2d2f864934fde829dca2c44eb5b91ebc4349852f07634b92ffff1` | Implemented Stage C Package 1A row identity instantiation |
| `d82e0f0` | 2026-06-05 | `48343d84f59b4f2016a47adb7f41caaaf795616115d0558ea73895cd6092f2c5` | Ran Stage C direct-answer technical spike |
| `97491ef` | 2026-06-06 | `495da2ed9690e55c4f12f87bf404dbfacfc04cda4e06795949a5767986f51390` | Adopted compatibility path decoupling slice |
| `325bdb4` | 2026-06-10 | `08a5cec22a781193365bed85b709ceebef534846602004bbfa047f4e0b59d738` | Added E1 prompt trace and path registry support |

## What Changed

The hash changed because the evaluator file evolved through a sequence of intentional commits.
The current version adds prompt-trace provenance fields, row identity plumbing, and Stage C evidence emission helpers.
The core canonical scoring path remained the same.

## Intent, Review, Acceptance

- Intentional: yes, each hash-changing commit has an explicit change-focused commit message.
- Reviewed: no explicit PR review metadata was found in local or `gh` lookup results.
- Accepted: yes, the changes landed on `main` and are present in `origin/main`.

## Characterization

The drift is a versioning drift, not an unexplained mutation.
The manifest pin is stale relative to the current evaluator file, and the current evaluator is the landed version in the repository.
