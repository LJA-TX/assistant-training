#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Mapping


class ContractViolation(RuntimeError):
    """Raised when contract-locked requirements are violated."""


class CompletenessState(str, Enum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    MISSING = "missing"


class CurrentRunComputabilityState(str, Enum):
    COMPUTABLE = "current-run computable"
    NONCOMPUTABLE = "current-run noncomputable"


class ComparabilityState(str, Enum):
    ALLOWED = "comparison-allowed"
    BRIDGE_REQUIRED = "bridge-required"
    REFERENCE_ONLY = "reference-only"
    BLOCKED = "comparison-blocked"


APPROVED_FAMILY_A_SUBTYPES = {
    "direct-answer substitution",
    "scalar substitution",
    "malformed output",
    "wrapper/envelope drift",
    "missing tool call",
    "wrong tool name",
    "wrong argument",
}


REQUIRED_FIXTURE_TOP_LEVEL_KEYS = {
    "fixture_id",
    "source_definition_id",
    "source_documents",
    "classification",
    "required_inputs",
    "expected_state",
    "expected_detector_treatment",
    "expected_reconciliation_behavior",
    "acceptance_criteria",
    "rationale",
}


REQUIRED_EXPECTED_STATE_KEYS = {
    "completeness",
    "current_run_computability",
    "comparability",
    "noncomputability_reasons",
}


ALLOWED_EXPECTED_STATE_EXTRA_KEYS = {
    "comparison_block_reasons",
    "parent_completeness",
    "parent_current_run_computability",
}


FORBIDDEN_TRUE_DETECTOR_PREFIXES = (
    "infer_",
    "substitute_",
    "reconstruct_",
)


FORBIDDEN_TRUE_DETECTOR_KEYS = {
    "use_proxy_or_reconstructed_metrics",
    "use_proxy_or_reconstructed_metric",
    "use_alternate_denominator",
    "use_alternate_population_denominator",
    "use_parent_sibling_mixed_tool_or_historical_denominator",
    "default_missing_ownership_to_dataset_metadata",
    "default_missing_ownership_to_evaluator",
}


@dataclass(frozen=True)
class RowFactMembershipMarkers:
    family_a_tool_expected_eligible: bool
    family_b1_read_file_eligible: bool
    family_b1_symbol_name_member: bool | None
    family_b2_anchor_eligible: bool
    family_b2_no_anchor_member: bool | None
    family_b2_anchor_category: str | None


@dataclass(frozen=True)
class RowFactOwnershipMarkers:
    symbol_name_membership_owner: str | None
    anchor_assignment_owner: str | None
    anchor_taxonomy_owner: str | None
    conflicting_ownership_markers: bool
    ownership_conflict_reasons: tuple[str, ...]


@dataclass(frozen=True)
class RowFactProvenance:
    row_source: str
    dataset_id: str
    dataset_version: str
    extraction_timestamp_utc: str
    evidence_digest: str


@dataclass(frozen=True)
class DenominatorProvenance:
    eligible_population_source: str
    non_exact_population_source: str
    read_file_population_source: str | None
    symbol_name_population_source: str | None
    anchor_population_source: str | None
    no_anchor_population_source: str | None


@dataclass(frozen=True)
class RowFactRecord:
    row_id: str
    split_id: str
    excluded: bool
    expected_tool_name: str | None
    membership_markers: RowFactMembershipMarkers
    ownership_markers: RowFactOwnershipMarkers
    provenance: RowFactProvenance
    denominator_provenance: DenominatorProvenance
    evidence: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FamilyAScorerEvidenceInput:
    row_id: str
    tool_expected_eligibility: bool
    excluded: bool
    exact_valid: bool
    primary_outcome: str
    failure_taxonomy_marker: str
    scorer_semantics_marker: str
    declared_subtype: str | None
    missing_evidence_reasons: tuple[str, ...]


@dataclass(frozen=True)
class FamilyAScorerEvidenceRecord:
    row_id: str
    tool_expected_eligibility: bool
    excluded: bool
    primary_outcome: str
    exact_valid: bool
    non_exact_tool_expected: bool
    subtype_assignment: str | None
    missing_evidence: bool
    missing_evidence_reasons: tuple[str, ...]
    failure_taxonomy_marker: str
    scorer_semantics_marker: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FixtureValidationIssue:
    fixture_path: str
    issue_code: str
    message: str


@dataclass(frozen=True)
class FixtureValidationReport:
    fixtures_root: str
    fixture_count: int
    valid_fixture_count: int
    invalid_fixture_count: int
    issue_count: int
    issue_counts_by_code: dict[str, int]
    state_tuple_counts: dict[str, int]
    fixture_counts_by_family_group: dict[str, int]
    issues: list[FixtureValidationIssue]

    def to_dict(self) -> dict[str, Any]:
        return {
            "fixtures_root": self.fixtures_root,
            "fixture_count": self.fixture_count,
            "valid_fixture_count": self.valid_fixture_count,
            "invalid_fixture_count": self.invalid_fixture_count,
            "issue_count": self.issue_count,
            "issue_counts_by_code": self.issue_counts_by_code,
            "state_tuple_counts": self.state_tuple_counts,
            "fixture_counts_by_family_group": self.fixture_counts_by_family_group,
            "issues": [asdict(issue) for issue in self.issues],
        }


def _require_nonempty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractViolation(f"{field_name} must be a non-empty string")
    return value.strip()


def _optional_nonempty_str(value: Any, field_name: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ContractViolation(f"{field_name} must be None or a non-empty string")
    return value.strip()


def _require_bool(value: Any, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ContractViolation(f"{field_name} must be a bool")
    return value


def _require_optional_bool(value: Any, field_name: str) -> bool | None:
    if value is None:
        return None
    if not isinstance(value, bool):
        raise ContractViolation(f"{field_name} must be bool or None")
    return value


def build_row_fact_record(payload: Mapping[str, Any]) -> RowFactRecord:
    row_id = _require_nonempty_str(payload.get("row_id"), "row_id")
    split_id = _require_nonempty_str(payload.get("split_id"), "split_id")
    excluded = _require_bool(payload.get("excluded"), "excluded")
    expected_tool_name = _optional_nonempty_str(payload.get("expected_tool_name"), "expected_tool_name")

    membership_raw = payload.get("membership_markers")
    if not isinstance(membership_raw, Mapping):
        raise ContractViolation("membership_markers must be an object")
    membership = RowFactMembershipMarkers(
        family_a_tool_expected_eligible=_require_bool(
            membership_raw.get("family_a_tool_expected_eligible"),
            "membership_markers.family_a_tool_expected_eligible",
        ),
        family_b1_read_file_eligible=_require_bool(
            membership_raw.get("family_b1_read_file_eligible"),
            "membership_markers.family_b1_read_file_eligible",
        ),
        family_b1_symbol_name_member=_require_optional_bool(
            membership_raw.get("family_b1_symbol_name_member"),
            "membership_markers.family_b1_symbol_name_member",
        ),
        family_b2_anchor_eligible=_require_bool(
            membership_raw.get("family_b2_anchor_eligible"),
            "membership_markers.family_b2_anchor_eligible",
        ),
        family_b2_no_anchor_member=_require_optional_bool(
            membership_raw.get("family_b2_no_anchor_member"),
            "membership_markers.family_b2_no_anchor_member",
        ),
        family_b2_anchor_category=_optional_nonempty_str(
            membership_raw.get("family_b2_anchor_category"),
            "membership_markers.family_b2_anchor_category",
        ),
    )

    ownership_raw = payload.get("ownership_markers")
    if not isinstance(ownership_raw, Mapping):
        raise ContractViolation("ownership_markers must be an object")
    conflict_reasons_raw = ownership_raw.get("ownership_conflict_reasons", [])
    if not isinstance(conflict_reasons_raw, list) or not all(isinstance(x, str) and x.strip() for x in conflict_reasons_raw):
        raise ContractViolation("ownership_markers.ownership_conflict_reasons must be a list of non-empty strings")
    ownership = RowFactOwnershipMarkers(
        symbol_name_membership_owner=_optional_nonempty_str(
            ownership_raw.get("symbol_name_membership_owner"),
            "ownership_markers.symbol_name_membership_owner",
        ),
        anchor_assignment_owner=_optional_nonempty_str(
            ownership_raw.get("anchor_assignment_owner"),
            "ownership_markers.anchor_assignment_owner",
        ),
        anchor_taxonomy_owner=_optional_nonempty_str(
            ownership_raw.get("anchor_taxonomy_owner"),
            "ownership_markers.anchor_taxonomy_owner",
        ),
        conflicting_ownership_markers=_require_bool(
            ownership_raw.get("conflicting_ownership_markers"),
            "ownership_markers.conflicting_ownership_markers",
        ),
        ownership_conflict_reasons=tuple(x.strip() for x in conflict_reasons_raw),
    )

    provenance_raw = payload.get("provenance")
    if not isinstance(provenance_raw, Mapping):
        raise ContractViolation("provenance must be an object")
    provenance = RowFactProvenance(
        row_source=_require_nonempty_str(provenance_raw.get("row_source"), "provenance.row_source"),
        dataset_id=_require_nonempty_str(provenance_raw.get("dataset_id"), "provenance.dataset_id"),
        dataset_version=_require_nonempty_str(provenance_raw.get("dataset_version"), "provenance.dataset_version"),
        extraction_timestamp_utc=_require_nonempty_str(
            provenance_raw.get("extraction_timestamp_utc"),
            "provenance.extraction_timestamp_utc",
        ),
        evidence_digest=_require_nonempty_str(provenance_raw.get("evidence_digest"), "provenance.evidence_digest"),
    )

    denominator_raw = payload.get("denominator_provenance")
    if not isinstance(denominator_raw, Mapping):
        raise ContractViolation("denominator_provenance must be an object")
    denominator = DenominatorProvenance(
        eligible_population_source=_require_nonempty_str(
            denominator_raw.get("eligible_population_source"),
            "denominator_provenance.eligible_population_source",
        ),
        non_exact_population_source=_require_nonempty_str(
            denominator_raw.get("non_exact_population_source"),
            "denominator_provenance.non_exact_population_source",
        ),
        read_file_population_source=_optional_nonempty_str(
            denominator_raw.get("read_file_population_source"),
            "denominator_provenance.read_file_population_source",
        ),
        symbol_name_population_source=_optional_nonempty_str(
            denominator_raw.get("symbol_name_population_source"),
            "denominator_provenance.symbol_name_population_source",
        ),
        anchor_population_source=_optional_nonempty_str(
            denominator_raw.get("anchor_population_source"),
            "denominator_provenance.anchor_population_source",
        ),
        no_anchor_population_source=_optional_nonempty_str(
            denominator_raw.get("no_anchor_population_source"),
            "denominator_provenance.no_anchor_population_source",
        ),
    )

    evidence = payload.get("evidence", {})
    if not isinstance(evidence, Mapping):
        raise ContractViolation("evidence must be an object")

    if membership.family_b1_symbol_name_member is True:
        if not membership.family_b1_read_file_eligible:
            raise ContractViolation(
                "family_b1_symbol_name_member=True requires family_b1_read_file_eligible=True"
            )
        if ownership.symbol_name_membership_owner is None:
            raise ContractViolation(
                "symbol_name_membership_owner is required when family_b1_symbol_name_member is declared"
            )

    if membership.family_b2_anchor_eligible:
        if ownership.anchor_assignment_owner is None:
            raise ContractViolation(
                "anchor_assignment_owner is required when family_b2_anchor_eligible=True"
            )
        if ownership.anchor_taxonomy_owner is None:
            raise ContractViolation(
                "anchor_taxonomy_owner is required when family_b2_anchor_eligible=True"
            )

    if membership.family_b2_no_anchor_member is True:
        if not membership.family_b2_anchor_eligible:
            raise ContractViolation(
                "family_b2_no_anchor_member=True requires family_b2_anchor_eligible=True"
            )
        if membership.family_b2_anchor_category not in {None, "no-anchor"}:
            raise ContractViolation(
                "family_b2_no_anchor_member=True requires family_b2_anchor_category to be None or 'no-anchor'"
            )

    if ownership.conflicting_ownership_markers and not ownership.ownership_conflict_reasons:
        raise ContractViolation(
            "ownership_conflict_reasons must be populated when conflicting_ownership_markers=True"
        )

    return RowFactRecord(
        row_id=row_id,
        split_id=split_id,
        excluded=excluded,
        expected_tool_name=expected_tool_name,
        membership_markers=membership,
        ownership_markers=ownership,
        provenance=provenance,
        denominator_provenance=denominator,
        evidence=dict(evidence),
    )


def emit_family_a_scorer_evidence(payload: FamilyAScorerEvidenceInput) -> FamilyAScorerEvidenceRecord:
    _require_nonempty_str(payload.row_id, "row_id")
    _require_nonempty_str(payload.primary_outcome, "primary_outcome")
    _require_nonempty_str(payload.failure_taxonomy_marker, "failure_taxonomy_marker")
    _require_nonempty_str(payload.scorer_semantics_marker, "scorer_semantics_marker")

    if payload.declared_subtype == "other":
        raise ContractViolation("declared_subtype 'other' is prohibited by Stage C0 contract lock")

    if payload.declared_subtype is not None and payload.declared_subtype not in APPROVED_FAMILY_A_SUBTYPES:
        raise ContractViolation(
            f"declared_subtype '{payload.declared_subtype}' is not an approved Family A subtype"
        )

    if not payload.tool_expected_eligibility or payload.excluded:
        return FamilyAScorerEvidenceRecord(
            row_id=payload.row_id,
            tool_expected_eligibility=payload.tool_expected_eligibility,
            excluded=payload.excluded,
            primary_outcome=payload.primary_outcome,
            exact_valid=payload.exact_valid,
            non_exact_tool_expected=False,
            subtype_assignment=None,
            missing_evidence=False,
            missing_evidence_reasons=tuple(),
            failure_taxonomy_marker=payload.failure_taxonomy_marker,
            scorer_semantics_marker=payload.scorer_semantics_marker,
        )

    if payload.exact_valid:
        return FamilyAScorerEvidenceRecord(
            row_id=payload.row_id,
            tool_expected_eligibility=True,
            excluded=False,
            primary_outcome=payload.primary_outcome,
            exact_valid=True,
            non_exact_tool_expected=False,
            subtype_assignment=None,
            missing_evidence=False,
            missing_evidence_reasons=tuple(),
            failure_taxonomy_marker=payload.failure_taxonomy_marker,
            scorer_semantics_marker=payload.scorer_semantics_marker,
        )

    if payload.declared_subtype is not None:
        if payload.missing_evidence_reasons:
            raise ContractViolation(
                "missing_evidence_reasons must be empty when declared_subtype is emitted"
            )
        return FamilyAScorerEvidenceRecord(
            row_id=payload.row_id,
            tool_expected_eligibility=True,
            excluded=False,
            primary_outcome=payload.primary_outcome,
            exact_valid=False,
            non_exact_tool_expected=True,
            subtype_assignment=payload.declared_subtype,
            missing_evidence=False,
            missing_evidence_reasons=tuple(),
            failure_taxonomy_marker=payload.failure_taxonomy_marker,
            scorer_semantics_marker=payload.scorer_semantics_marker,
        )

    reasons = payload.missing_evidence_reasons or (
        "missing approved non-exact subtype assignment",
    )
    return FamilyAScorerEvidenceRecord(
        row_id=payload.row_id,
        tool_expected_eligibility=True,
        excluded=False,
        primary_outcome=payload.primary_outcome,
        exact_valid=False,
        non_exact_tool_expected=True,
        subtype_assignment=None,
        missing_evidence=True,
        missing_evidence_reasons=tuple(reasons),
        failure_taxonomy_marker=payload.failure_taxonomy_marker,
        scorer_semantics_marker=payload.scorer_semantics_marker,
    )


def discover_fixture_paths(fixtures_root: Path) -> list[Path]:
    return sorted(fixtures_root.rglob("*.json"))


def _load_fixture(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ContractViolation(f"{path}: fixture root must be an object")
    return data


def _issue(path: Path, code: str, message: str) -> FixtureValidationIssue:
    return FixtureValidationIssue(fixture_path=str(path), issue_code=code, message=message)


def _validate_fixture(path: Path, fixture: Mapping[str, Any]) -> list[FixtureValidationIssue]:
    issues: list[FixtureValidationIssue] = []

    missing = REQUIRED_FIXTURE_TOP_LEVEL_KEYS - set(fixture.keys())
    for key in sorted(missing):
        issues.append(_issue(path, "missing_top_level_key", f"missing required top-level key: {key}"))

    if "expected_state" not in fixture or not isinstance(fixture.get("expected_state"), Mapping):
        issues.append(_issue(path, "expected_state_missing_or_invalid", "expected_state must be an object"))
        return issues

    state = fixture["expected_state"]
    missing_state = REQUIRED_EXPECTED_STATE_KEYS - set(state.keys())
    for key in sorted(missing_state):
        issues.append(_issue(path, "missing_expected_state_key", f"missing expected_state key: {key}"))

    extra_state = set(state.keys()) - REQUIRED_EXPECTED_STATE_KEYS - ALLOWED_EXPECTED_STATE_EXTRA_KEYS
    for key in sorted(extra_state):
        issues.append(_issue(path, "unexpected_expected_state_key", f"unexpected expected_state key: {key}"))

    if "state" in state or "combined_state" in state:
        issues.append(_issue(path, "collapsed_state_field", "collapsed state fields are prohibited"))

    completeness = state.get("completeness")
    if completeness not in {x.value for x in CompletenessState}:
        issues.append(_issue(path, "invalid_completeness_state", f"invalid completeness state: {completeness}"))

    current_run = state.get("current_run_computability")
    if current_run not in {x.value for x in CurrentRunComputabilityState}:
        issues.append(
            _issue(path, "invalid_current_run_computability_state", f"invalid current_run_computability state: {current_run}")
        )

    comparability = state.get("comparability")
    if comparability not in {x.value for x in ComparabilityState}:
        issues.append(_issue(path, "invalid_comparability_state", f"invalid comparability state: {comparability}"))

    reasons = state.get("noncomputability_reasons")
    if not isinstance(reasons, list) or not all(isinstance(x, str) for x in reasons):
        issues.append(_issue(path, "invalid_noncomputability_reasons", "noncomputability_reasons must be a list[str]"))

    if "comparison_block_reasons" in state:
        block_reasons = state.get("comparison_block_reasons")
        if not isinstance(block_reasons, list) or not all(isinstance(x, str) for x in block_reasons):
            issues.append(_issue(path, "invalid_comparison_block_reasons", "comparison_block_reasons must be a list[str]"))

    detector_treatment = fixture.get("expected_detector_treatment")
    if isinstance(detector_treatment, Mapping):
        for key, value in detector_treatment.items():
            if not isinstance(value, bool):
                continue
            if key in FORBIDDEN_TRUE_DETECTOR_KEYS and value:
                issues.append(_issue(path, "forbidden_detector_behavior", f"{key} must not be true"))
            if any(key.startswith(prefix) for prefix in FORBIDDEN_TRUE_DETECTOR_PREFIXES) and value:
                issues.append(_issue(path, "forbidden_detector_behavior", f"{key} must not be true"))

    return issues


def _family_group_from_fixture_id(fixture_id: str) -> str:
    if fixture_id.startswith("A-"):
        return "family_a"
    if fixture_id.startswith("B1-"):
        return "family_b1"
    if fixture_id.startswith("B2-"):
        return "family_b2"
    if fixture_id.startswith("X-"):
        return "cross_family"
    if fixture_id.startswith("WP8B-"):
        return "common_state"
    return "unknown"


def run_fixture_harness(fixtures_root: Path) -> FixtureValidationReport:
    paths = discover_fixture_paths(fixtures_root)
    issues: list[FixtureValidationIssue] = []
    state_counter: Counter[str] = Counter()
    family_counter: Counter[str] = Counter()

    valid_count = 0
    for path in paths:
        try:
            fixture = _load_fixture(path)
        except Exception as exc:  # pragma: no cover
            issues.append(_issue(path, "fixture_load_error", str(exc)))
            continue

        fixture_issues = _validate_fixture(path, fixture)
        issues.extend(fixture_issues)

        fixture_id = fixture.get("fixture_id")
        if isinstance(fixture_id, str):
            family_counter[_family_group_from_fixture_id(fixture_id)] += 1

        expected_state = fixture.get("expected_state")
        if isinstance(expected_state, Mapping):
            completeness = expected_state.get("completeness")
            current_run = expected_state.get("current_run_computability")
            comparability = expected_state.get("comparability")
            if isinstance(completeness, str) and isinstance(current_run, str) and isinstance(comparability, str):
                state_counter[f"{completeness} | {current_run} | {comparability}"] += 1

        if not fixture_issues:
            valid_count += 1

    issue_counter = Counter(issue.issue_code for issue in issues)

    return FixtureValidationReport(
        fixtures_root=str(fixtures_root),
        fixture_count=len(paths),
        valid_fixture_count=valid_count,
        invalid_fixture_count=len(paths) - valid_count,
        issue_count=len(issues),
        issue_counts_by_code=dict(sorted(issue_counter.items())),
        state_tuple_counts=dict(sorted(state_counter.items())),
        fixture_counts_by_family_group=dict(sorted(family_counter.items())),
        issues=issues,
    )


def _default_fixtures_root() -> Path:
    return Path("/opt/ai-stack/assistant-training/manifests/reports/stage_b_wp8_validation/fixtures")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stage C1 evaluator foundation fixture harness skeleton"
    )
    parser.add_argument(
        "--fixtures-root",
        default=str(_default_fixtures_root()),
        help="Path to Stage B WP8 fixture root",
    )
    parser.add_argument(
        "--report-output",
        default=None,
        help="Optional output path for fixture harness report JSON",
    )
    args = parser.parse_args()

    report = run_fixture_harness(Path(args.fixtures_root).resolve())
    payload = report.to_dict()

    if args.report_output:
        out_path = Path(args.report_output).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if report.issue_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
