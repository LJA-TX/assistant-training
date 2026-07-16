#!/usr/bin/env python3
"""Validate repository-relative references in the curated public package.

The private repository is the canonical home of this tool.  Validation is
performed against a separately supplied public checkout and its exact
disposition metadata; private files are never copied or used as substitutes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote, urlsplit


DEFAULT_METADATA = "docs/publication/public_reference_dispositions.json"
DISPOSITION_VALUES = {
    "publication_defect",
    "intentional_public_omission",
    "historical_provenance",
    "generated_output",
    "optional_output",
    "indeterminate",
}
FAIL_DISPOSITIONS = {"publication_defect", "indeterminate"}
MARKDOWN_LINK_RE = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
PATH_KEYS = {
    "artifact_files",
    "bundle_manifest_path",
    "bundle_path",
    "dataset_builder_script",
    "dataset_manifest_path",
    "dependency_lock_snapshot_path",
    "evaluation_contract_path",
    "legacy_eval_script",
    "metric_spec_path",
    "package_readme",
    "package_root",
    "project_wide_comparison_table_path",
    "published_bundle_path",
    "scorer_script",
    "snapshot_path",
    "source_run_path",
    "supporting_documents",
    "training_script",
}
CANONICAL_HASH_PAIRS = (
    (("runtime", "dataset_manifest_path"), ("runtime", "dataset_manifest_sha256")),
    (("scoring", "scorer_script"), ("scoring", "scorer_sha256")),
    (("scoring", "metric_spec_path"), ("scoring", "metric_spec_sha256")),
    (("scoring", "legacy_eval_script"), ("scoring", "legacy_eval_sha256")),
    (("training_and_eval_code", "training_script"), ("training_and_eval_code", "training_script_sha256")),
    (("training_and_eval_code", "dataset_builder_script"), ("training_and_eval_code", "dataset_builder_sha256")),
    (("environment", "snapshot_path"), ("environment", "snapshot_sha256")),
    (("environment", "dependency_lock_snapshot_path"), ("environment", "dependency_lock_snapshot_sha256")),
)


@dataclass(frozen=True)
class Reference:
    source: str
    kind: str
    target: str
    location: str
    status: str
    disposition: str | None = None
    detail: str | None = None
    canonical_field: str | None = None
    historical_hash: str | None = None
    actual_sha256: str | None = None
    verification_status: str | None = None
    historical_provenance_status: str | None = None


def _relative(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _is_url(value: str) -> bool:
    return bool(urlsplit(value).scheme)


def _target_path(root: Path, target: str, *, base: Path) -> Path | None:
    target = unquote(target.split("#", 1)[0])
    if not target or _is_url(target) or target.startswith("/"):
        return None
    candidate = (base / target).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate


def _load_metadata(root: Path, metadata_path: str) -> tuple[dict[tuple[str, str, str, str], dict[str, Any]], dict[tuple[str, str, str], dict[str, Any]], list[str]]:
    path = (root / metadata_path).resolve()
    if not path.is_file():
        return {}, {}, [f"metadata file is missing: {metadata_path}"]
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, {}, [f"metadata file cannot be read: {metadata_path}: {exc}"]
    errors: list[str] = []
    if document.get("schema_version") != 1:
        errors.append("metadata schema_version must be 1")
    entries = document.get("dispositions")
    if not isinstance(entries, list):
        return {}, {}, errors + ["metadata dispositions must be a list"]
    index: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for number, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            errors.append(f"metadata disposition {number} is not an object")
            continue
        source = entry.get("source")
        kind = entry.get("kind", "json_path")
        targets = entry.get("targets", [entry.get("target")])
        json_paths = entry.get("json_paths", [entry.get("json_path", "")])
        disposition = entry.get("disposition")
        dispositions = entry.get("dispositions", [disposition] * len(targets) if isinstance(targets, list) else [])
        reason = entry.get("reason")
        if not isinstance(targets, list) or not isinstance(json_paths, list) or not isinstance(dispositions, list) or len(targets) != len(json_paths) or len(targets) != len(dispositions):
            errors.append(f"metadata disposition {number} must have equally sized targets/json_paths")
            continue
        if not all(isinstance(x, str) and x for x in (source, kind, reason)) or not all(
            isinstance(x, str) and x for x in (*targets, *json_paths, *dispositions)
        ):
            errors.append(f"metadata disposition {number} has missing required fields")
            continue
        for target, json_path, target_disposition in zip(targets, json_paths, dispositions):
            if target_disposition not in DISPOSITION_VALUES:
                errors.append(f"metadata disposition {number} has invalid disposition {target_disposition!r}")
            key = (source, kind, json_path, target)
            if key in index:
                errors.append(f"metadata disposition {number} duplicates {key}")
            index[key] = {
                **entry,
                "target": target,
                "json_path": json_path,
                "disposition": target_disposition,
                "_metadata_key": key,
            }
    verification_index: dict[tuple[str, str, str], dict[str, Any]] = {}
    verification_entries = document.get("public_verification", [])
    if not isinstance(verification_entries, list):
        errors.append("metadata public_verification must be a list")
        verification_entries = []
    required = {
        "source",
        "path",
        "sha256",
        "canonical_field",
        "canonical_hash",
        "relationship",
        "provenance_classification",
        "historical_provenance_status",
        "note",
    }
    for number, entry in enumerate(verification_entries, 1):
        if not isinstance(entry, dict) or not required.issubset(entry):
            errors.append(f"metadata public_verification {number} is missing required fields")
            continue
        if not all(isinstance(entry[field], str) and entry[field] for field in required):
            errors.append(f"metadata public_verification {number} has non-empty string field violations")
            continue
        if not re.fullmatch(r"[0-9a-fA-F]{64}", entry["sha256"]):
            errors.append(f"metadata public_verification {number} has malformed current SHA-256")
        if not re.fullmatch(r"[0-9a-fA-F]{64}", entry["canonical_hash"]):
            errors.append(f"metadata public_verification {number} has malformed canonical SHA-256")
        key = (entry["source"], entry["canonical_field"], entry["path"])
        if key in verification_index:
            errors.append(f"metadata public_verification {number} duplicates {key}")
        verification_index[key] = {**entry, "_verification_key": key}
    return index, verification_index, errors


def _metadata_for(
    index: dict[tuple[str, str, str, str], dict[str, Any]],
    reference: Reference,
) -> dict[str, Any] | None:
    exact = index.get((reference.source, reference.kind, reference.location if reference.kind == "json_path" else "", reference.target))
    if exact is not None:
        return exact
    if reference.kind == "hash_target":
        return index.get((reference.source, "json_path", reference.location, reference.target))
    return None


def _with_disposition(reference: Reference, index: dict[tuple[str, str, str, str], dict[str, Any]]) -> Reference:
    entry = _metadata_for(index, reference)
    if entry is None:
        return reference
    return Reference(**{**asdict(reference), "disposition": entry["disposition"], "detail": entry["reason"]})


def _public_verification_for(
    verification_index: dict[tuple[str, str, str], dict[str, Any]],
    reference: Reference,
) -> dict[str, Any] | None:
    if reference.kind != "hash_target" or reference.canonical_field is None:
        return None
    return verification_index.get((reference.source, reference.canonical_field, reference.target))


def _markdown_references(root: Path, index: dict[tuple[str, str, str, str], dict[str, Any]]) -> list[Reference]:
    references: list[Reference] = []
    for path in sorted(root.rglob("*.md")):
        if path.resolve() == (root / DEFAULT_METADATA).resolve():
            continue
        source = _relative(root, path)
        for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for match in MARKDOWN_LINK_RE.finditer(line):
                raw = match.group(1).strip().split()[0].strip("<>") if match.group(1).strip() else ""
                if not raw:
                    continue
                if raw.startswith("#"):
                    references.append(Reference(source, "anchor", raw, str(line_number), "valid"))
                    continue
                if _is_url(raw):
                    references.append(Reference(source, "external_url", raw, str(line_number), "valid"))
                    continue
                target = raw.split("#", 1)[0]
                resolved = _target_path(root, target, base=path.parent)
                if resolved is None:
                    ref = Reference(source, "repository_link", raw, str(line_number), "unresolved", detail="outside public root")
                else:
                    ref = Reference(source, "repository_link", raw, str(line_number), "valid" if resolved.exists() else "unresolved")
                references.append(_with_disposition(ref, index))
    return references


def _path_value_references(
    root: Path,
    source_path: Path,
    value: str,
    json_path: str,
    *,
    package_relative: bool = False,
    index: dict[tuple[str, str, str, str], dict[str, Any]],
) -> list[Reference]:
    source = _relative(root, source_path)
    if _is_url(value):
        return [Reference(source, "external_url", value, json_path, "valid")]
    if value.startswith("/") or value.startswith("<"):
        kind = "generated_output" if value.startswith("<") else "historical_provenance"
        return [Reference(source, kind, value, json_path, "valid", detail="non-repository path literal")]
    base = source_path.parent if package_relative else root
    resolved = _target_path(root, value, base=base)
    status = "valid" if resolved is not None and resolved.exists() else "unresolved"
    ref = Reference(source, "json_path", value, json_path, status)
    return [_with_disposition(ref, index)]


def _walk_defined_json_paths(root: Path, path: Path, value: Any, json_path: str = "") -> Iterable[tuple[str, str, bool]]:
    if isinstance(value, dict):
        for key in sorted(value):
            child_path = f"{json_path}.{key}" if json_path else key
            child = value[key]
            is_dataset_path = key == "path" and json_path.startswith("datasets.")
            if isinstance(child, str) and (key in PATH_KEYS or is_dataset_path):
                yield child_path, child, key in {"artifact_files", "supporting_documents"} and path.name == "package_manifest.json"
            elif isinstance(child, list) and key in {"artifact_files", "supporting_documents"}:
                for index, item in enumerate(child):
                    if isinstance(item, str):
                        yield f"{child_path}[{index}]", item, key == "artifact_files" and path.name == "package_manifest.json"
            yield from _walk_defined_json_paths(root, path, child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_defined_json_paths(root, path, child, f"{json_path}[{index}]")


def _nested_value(document: dict[str, Any], path: tuple[str, ...]) -> Any:
    value: Any = document
    for key in path:
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value


def _canonical_hash_references(
    root: Path,
    source_path: Path,
    document: dict[str, Any],
    index: dict[tuple[str, str, str, str], dict[str, Any]],
    verification_index: dict[tuple[str, str, str], dict[str, Any]],
) -> list[Reference]:
    pairs = list(CANONICAL_HASH_PAIRS)
    datasets = document.get("datasets")
    if not isinstance(datasets, dict):
        return [
            Reference(
                _relative(root, source_path),
                "hash_target",
                "<missing datasets object>",
                "datasets",
                "unresolved",
                "publication_defect",
                "canonical manifest datasets must be an object",
            )
        ]
    for name in sorted(datasets):
        pairs.append((("datasets", name, "path"), ("datasets", name, "sha256")))

    references: list[Reference] = []
    source = _relative(root, source_path)
    for path_keys, hash_keys in pairs:
        location = ".".join(path_keys)
        canonical_field = ".".join(hash_keys)
        target_value = _nested_value(document, path_keys)
        hash_value = _nested_value(document, hash_keys)
        target = target_value if isinstance(target_value, str) and target_value else "<missing path>"
        if not isinstance(target_value, str) or not target_value:
            references.append(
                Reference(source, "hash_target", target, location, "unresolved", "publication_defect", "required path field is missing or not a non-empty string", canonical_field=canonical_field, historical_hash=hash_value if isinstance(hash_value, str) else None)
            )
            continue
        if not isinstance(hash_value, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", hash_value):
            references.append(
                Reference(source, "hash_target", target, location, "unresolved", "publication_defect", "required SHA-256 field is missing or malformed", canonical_field=canonical_field, historical_hash=hash_value if isinstance(hash_value, str) else None)
            )
            continue

        resolved = _target_path(root, target, base=root)
        status = "valid" if resolved is not None and resolved.is_file() else "unresolved"
        reference = Reference(source, "hash_target", target, location, status, canonical_field=canonical_field, historical_hash=hash_value)
        reference = _with_disposition(reference, index)
        if status == "valid":
            actual = hashlib.sha256(resolved.read_bytes()).hexdigest()
            verification = _public_verification_for(verification_index, reference)
            if actual.lower() == hash_value.lower():
                reference = Reference(**{**asdict(reference), "actual_sha256": actual, "verification_status": "historical_hash_verified", "historical_provenance_status": "verified_current_bytes"})
            elif verification is not None and verification["sha256"].lower() == actual.lower() and verification["canonical_hash"].lower() == hash_value.lower():
                reference = Reference(**{**asdict(reference), "actual_sha256": actual, "verification_status": "current_public_verified_historical_mismatch", "historical_provenance_status": verification["historical_provenance_status"], "detail": verification["note"]})
            else:
                reference = Reference(
                    **{
                        **asdict(reference),
                        "status": "unresolved",
                        "disposition": "publication_defect",
                        "actual_sha256": actual,
                        "detail": f"sha256 mismatch: expected {hash_value}, got {actual}; no exact valid public-verification record",
                    }
                )
        references.append(reference)
    return references


def _json_references(root: Path, index: dict[tuple[str, str, str, str], dict[str, Any]], verification_index: dict[tuple[str, str, str], dict[str, Any]]) -> tuple[list[Reference], list[dict[str, str]]]:
    references: list[Reference] = []
    malformed_json: list[dict[str, str]] = []
    for path in sorted(root.rglob("*.json")):
        if _relative(root, path) == DEFAULT_METADATA:
            continue
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            malformed_json.append({"source": _relative(root, path), "error": str(exc)})
            continue
        for json_path, value, package_relative in _walk_defined_json_paths(root, path, document):
            references.extend(_path_value_references(root, path, value, json_path, package_relative=package_relative, index=index))

        if path.name == "canonical_eval_manifest_v1.json" and isinstance(document, dict):
            references.extend(_canonical_hash_references(root, path, document, index, verification_index))
    return references, malformed_json


def validate(public_root: Path, metadata_path: str = DEFAULT_METADATA) -> dict[str, Any]:
    public_root = public_root.resolve()
    index, verification_index, metadata_errors = _load_metadata(public_root, metadata_path)
    json_references, malformed_json = _json_references(public_root, index, verification_index)
    references = _markdown_references(public_root, index) + json_references
    consumed_metadata = {
        entry["_metadata_key"]
        for reference in references
        if (entry := _metadata_for(index, reference)) is not None
    }
    stale_metadata = [
        {
            "source": entry.get("source"),
            "kind": entry.get("kind", "json_path"),
            "json_path": entry.get("json_path", ""),
            "target": entry.get("target"),
            "disposition": entry.get("disposition"),
        }
        for key, entry in sorted(index.items())
        if key not in consumed_metadata
    ]
    consumed_verification = {
        entry["_verification_key"]
        for reference in references
        if (entry := _public_verification_for(verification_index, reference)) is not None
        and reference.verification_status == "current_public_verified_historical_mismatch"
    }
    stale_public_verification = [
        {
            "source": entry["source"],
            "path": entry["path"],
            "canonical_field": entry["canonical_field"],
        }
        for key, entry in sorted(verification_index.items())
        if key not in consumed_verification
    ]
    unresolved = [reference for reference in references if reference.status == "unresolved"]
    unclassified = [reference for reference in unresolved if not reference.disposition]
    defects = [reference for reference in unresolved if reference.disposition in FAIL_DISPOSITIONS]
    counts_by_type = Counter(reference.kind for reference in references)
    counts_by_disposition = Counter(reference.disposition or "unclassified" for reference in unresolved)
    hash_targets = [reference for reference in references if reference.kind == "hash_target"]
    hash_summary = {
        "total": len(hash_targets),
        "present_verified": sum(reference.status == "valid" for reference in hash_targets),
        "intentionally_omitted": sum(
            reference.status == "unresolved" and reference.disposition == "intentional_public_omission"
            for reference in hash_targets
        ),
        "mismatched": sum("sha256 mismatch" in (reference.detail or "") for reference in hash_targets),
        "historical_mismatches_documented": sum(reference.verification_status == "current_public_verified_historical_mismatch" for reference in hash_targets),
        "historical_provenance_unresolved": sum(reference.historical_provenance_status == "unrecovered_original_bytes" for reference in hash_targets),
    }
    result = {
        "schema_version": 1,
        "public_root": str(public_root),
        "metadata_path": metadata_path,
        "reference_count": len(references),
        "counts_by_type": dict(sorted(counts_by_type.items())),
        "counts_by_disposition": dict(sorted(counts_by_disposition.items())),
        "hash_summary": hash_summary,
        "hash_targets": [asdict(reference) for reference in hash_targets],
        "references": [asdict(reference) for reference in references],
        "metadata_errors": sorted(metadata_errors),
        "stale_metadata": stale_metadata,
        "stale_public_verification": stale_public_verification,
        "public_verification_count": len(verification_index),
        "malformed_json": malformed_json,
        "unclassified": [asdict(reference) for reference in unclassified],
        "defects": [asdict(reference) for reference in defects],
        "unresolved": [asdict(reference) for reference in unresolved],
        "valid": not metadata_errors and not stale_metadata and not stale_public_verification and not malformed_json and not unclassified and not defects,
    }
    return result


def _human_report(result: dict[str, Any]) -> str:
    lines = [
        f"public reference validation: {'PASS' if result['valid'] else 'FAIL'}",
        f"references: {result['reference_count']}",
        "counts by type: " + ", ".join(f"{key}={value}" for key, value in result["counts_by_type"].items()),
        "counts by disposition: " + ", ".join(f"{key}={value}" for key, value in result["counts_by_disposition"].items()) or "counts by disposition: none",
        "hash targets: " + ", ".join(f"{key}={value}" for key, value in result["hash_summary"].items()),
    ]
    if result["metadata_errors"]:
        lines.extend(f"metadata error: {error}" for error in result["metadata_errors"])
    for entry in result["stale_metadata"]:
        lines.append(f"stale metadata: {entry['source']}:{entry['json_path']} -> {entry['target']}")
    for entry in result["stale_public_verification"]:
        lines.append(f"stale public verification: {entry['source']}:{entry['canonical_field']} -> {entry['path']}")
    for entry in result["malformed_json"]:
        lines.append(f"malformed JSON: {entry['source']}: {entry['error']}")
    for label in ("unclassified", "defects"):
        for reference in result[label]:
            lines.append(f"{label}: {reference['source']}:{reference['location']} -> {reference['target']}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("public_root", type=Path)
    parser.add_argument("--metadata", default=DEFAULT_METADATA)
    parser.add_argument("--json-output", type=Path, help="write the machine-readable result to this path")
    args = parser.parse_args(argv)
    result = validate(args.public_root, args.metadata)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.json_output:
        args.json_output.write_text(rendered, encoding="utf-8")
    print(_human_report(result), end="")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
