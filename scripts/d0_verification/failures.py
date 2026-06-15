from __future__ import annotations


class D0VerificationError(RuntimeError):
    """Base class for dry-run D0 verification failures."""


class AuthorityResolutionError(D0VerificationError):
    """Raised when authority resolution cannot be completed."""


class MissingRequiredArtifactError(D0VerificationError):
    """Raised when a required source artifact is missing."""


class HashMismatchError(D0VerificationError):
    """Raised when a computed hash does not match the published claim."""


class OutputRootContainmentError(D0VerificationError):
    """Raised when an output path escapes the declared output root."""


class RunIdValidationError(D0VerificationError):
    """Raised when a run identifier is unsafe or malformed."""
