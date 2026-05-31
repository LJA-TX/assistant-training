#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Mapping


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


class ReconciliationStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    BLOCKED = "blocked"


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


def _require_nonnegative_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int) or value < 0:
        raise ContractViolation(f"{field_name} must be a non-negative int")
    return value


def _dedupe_nonempty_strs(values: Iterable[str], field_name: str) -> tuple[str, ...]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        text = _require_nonempty_str(value, field_name)
        if text not in seen:
            seen.add(text)
            out.append(text)
    return tuple(out)


@dataclass(frozen=True)
class AggregationRow:
    family_id: str
    concept_id: str
    row_id: str
    split_id: str
    sub_slice_id: str | None
    eligible: bool
    counted: bool
    excluded: bool
    provenance_ref: str
    evidence_ref: str


@dataclass(frozen=True)
class AggregateMetricSummary:
    concept_id: str
    numerator: int
    denominator: int
    rate: float | None
    excluded_count: int
    row_count: int
    provenance_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True)
class SubSliceAggregateSummary:
    concept_id: str
    sub_slice_id: str
    numerator: int
    denominator: int
    rate: float | None
    excluded_count: int
    row_count: int
    provenance_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True)
class SplitAggregateSummary:
    concept_id: str
    split_id: str
    numerator: int
    denominator: int
    rate: float | None
    excluded_count: int
    row_count: int


@dataclass(frozen=True)
class FamilyAggregationReport:
    family_id: str
    total_rows: int
    concept_summaries: list[AggregateMetricSummary]
    sub_slice_summaries: list[SubSliceAggregateSummary]
    split_summaries: list[SplitAggregateSummary]

    def to_dict(self) -> dict[str, Any]:
        return {
            "family_id": self.family_id,
            "total_rows": self.total_rows,
            "concept_summaries": [asdict(x) for x in self.concept_summaries],
            "sub_slice_summaries": [asdict(x) for x in self.sub_slice_summaries],
            "split_summaries": [asdict(x) for x in self.split_summaries],
        }


@dataclass(frozen=True)
class StateEvaluationInput:
    concept_id: str
    required_evidence_fields: tuple[str, ...]
    present_evidence_fields: tuple[str, ...]
    explicit_noncomputability_reasons: tuple[str, ...]
    declared_comparability: ComparabilityState
    comparison_block_reasons: tuple[str, ...]
    inference_used: bool = False
    substitution_used: bool = False
    reconstruction_used: bool = False


@dataclass(frozen=True)
class ConceptStateRecord:
    concept_id: str
    completeness: CompletenessState
    current_run_computability: CurrentRunComputabilityState
    comparability: ComparabilityState
    noncomputability_reasons: tuple[str, ...]
    comparison_block_reasons: tuple[str, ...]
    missing_required_evidence_fields: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "concept_id": self.concept_id,
            "completeness": self.completeness.value,
            "current_run_computability": self.current_run_computability.value,
            "comparability": self.comparability.value,
            "noncomputability_reasons": list(self.noncomputability_reasons),
            "comparison_block_reasons": list(self.comparison_block_reasons),
            "missing_required_evidence_fields": list(self.missing_required_evidence_fields),
        }


@dataclass(frozen=True)
class ReconciliationCheckResult:
    check_id: str
    check_type: str
    result: ReconciliationStatus
    evaluated_inputs: dict[str, Any]
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "check_type": self.check_type,
            "result": self.result.value,
            "evaluated_inputs": self.evaluated_inputs,
            "reasons": list(self.reasons),
        }


@dataclass(frozen=True)
class ReconciliationFoundationReport:
    total_checks: int
    pass_count: int
    fail_count: int
    blocked_count: int
    results: list[ReconciliationCheckResult]

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_checks": self.total_checks,
            "pass_count": self.pass_count,
            "fail_count": self.fail_count,
            "blocked_count": self.blocked_count,
            "results": [x.to_dict() for x in self.results],
        }


@dataclass(frozen=True)
class StageC2FoundationReport:
    family_aggregation: FamilyAggregationReport
    state_records: list[ConceptStateRecord]
    reconciliation: ReconciliationFoundationReport

    def to_dict(self) -> dict[str, Any]:
        return {
            "family_aggregation": self.family_aggregation.to_dict(),
            "state_records": [x.to_dict() for x in self.state_records],
            "reconciliation": self.reconciliation.to_dict(),
        }


def build_aggregation_row(payload: Mapping[str, Any]) -> AggregationRow:
    family_id = _require_nonempty_str(payload.get("family_id"), "family_id")
    concept_id = _require_nonempty_str(payload.get("concept_id"), "concept_id")
    row_id = _require_nonempty_str(payload.get("row_id"), "row_id")
    split_id = _require_nonempty_str(payload.get("split_id"), "split_id")
    sub_slice_id = _optional_nonempty_str(payload.get("sub_slice_id"), "sub_slice_id")

    eligible = _require_bool(payload.get("eligible"), "eligible")
    counted = _require_bool(payload.get("counted"), "counted")
    excluded = _require_bool(payload.get("excluded"), "excluded")

    provenance_ref = _require_nonempty_str(payload.get("provenance_ref"), "provenance_ref")
    evidence_ref = _require_nonempty_str(payload.get("evidence_ref"), "evidence_ref")

    inference_used = payload.get("inference_used", False)
    substitution_used = payload.get("substitution_used", False)
    reconstruction_used = payload.get("reconstruction_used", False)
    if inference_used or substitution_used or reconstruction_used:
        raise ContractViolation("inference/substitution/reconstruction flags must not be enabled")

    if counted and not eligible:
        raise ContractViolation("counted=True requires eligible=True")
    if counted and excluded:
        raise ContractViolation("counted=True is invalid when excluded=True")

    return AggregationRow(
        family_id=family_id,
        concept_id=concept_id,
        row_id=row_id,
        split_id=split_id,
        sub_slice_id=sub_slice_id,
        eligible=eligible,
        counted=counted,
        excluded=excluded,
        provenance_ref=provenance_ref,
        evidence_ref=evidence_ref,
    )


def _rate(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


def aggregate_family_rows(family_id: str, rows: Iterable[AggregationRow]) -> FamilyAggregationReport:
    target_family = _require_nonempty_str(family_id, "family_id")
    row_list = list(rows)

    for row in row_list:
        if row.family_id != target_family:
            raise ContractViolation(
                f"aggregation row family mismatch: expected {target_family}, got {row.family_id}"
            )

    concept_groups: dict[str, list[AggregationRow]] = defaultdict(list)
    subslice_groups: dict[tuple[str, str], list[AggregationRow]] = defaultdict(list)
    split_groups: dict[tuple[str, str], list[AggregationRow]] = defaultdict(list)

    for row in row_list:
        concept_groups[row.concept_id].append(row)
        if row.sub_slice_id is not None:
            subslice_groups[(row.concept_id, row.sub_slice_id)].append(row)
        split_groups[(row.concept_id, row.split_id)].append(row)

    concept_summaries: list[AggregateMetricSummary] = []
    for concept_id, group in sorted(concept_groups.items()):
        denominator = sum(1 for row in group if row.eligible and not row.excluded)
        numerator = sum(1 for row in group if row.counted)
        excluded_count = sum(1 for row in group if row.excluded)
        provenance_refs = tuple(sorted({row.provenance_ref for row in group}))
        evidence_refs = tuple(sorted({row.evidence_ref for row in group}))
        concept_summaries.append(
            AggregateMetricSummary(
                concept_id=concept_id,
                numerator=numerator,
                denominator=denominator,
                rate=_rate(numerator, denominator),
                excluded_count=excluded_count,
                row_count=len(group),
                provenance_refs=provenance_refs,
                evidence_refs=evidence_refs,
            )
        )

    sub_slice_summaries: list[SubSliceAggregateSummary] = []
    for (concept_id, sub_slice_id), group in sorted(subslice_groups.items()):
        denominator = sum(1 for row in group if row.eligible and not row.excluded)
        numerator = sum(1 for row in group if row.counted)
        excluded_count = sum(1 for row in group if row.excluded)
        provenance_refs = tuple(sorted({row.provenance_ref for row in group}))
        evidence_refs = tuple(sorted({row.evidence_ref for row in group}))
        sub_slice_summaries.append(
            SubSliceAggregateSummary(
                concept_id=concept_id,
                sub_slice_id=sub_slice_id,
                numerator=numerator,
                denominator=denominator,
                rate=_rate(numerator, denominator),
                excluded_count=excluded_count,
                row_count=len(group),
                provenance_refs=provenance_refs,
                evidence_refs=evidence_refs,
            )
        )

    split_summaries: list[SplitAggregateSummary] = []
    for (concept_id, split_id), group in sorted(split_groups.items()):
        denominator = sum(1 for row in group if row.eligible and not row.excluded)
        numerator = sum(1 for row in group if row.counted)
        excluded_count = sum(1 for row in group if row.excluded)
        split_summaries.append(
            SplitAggregateSummary(
                concept_id=concept_id,
                split_id=split_id,
                numerator=numerator,
                denominator=denominator,
                rate=_rate(numerator, denominator),
                excluded_count=excluded_count,
                row_count=len(group),
            )
        )

    return FamilyAggregationReport(
        family_id=target_family,
        total_rows=len(row_list),
        concept_summaries=concept_summaries,
        sub_slice_summaries=sub_slice_summaries,
        split_summaries=split_summaries,
    )


def evaluate_concept_state(payload: StateEvaluationInput) -> ConceptStateRecord:
    concept_id = _require_nonempty_str(payload.concept_id, "concept_id")

    if payload.inference_used or payload.substitution_used or payload.reconstruction_used:
        raise ContractViolation("inference/substitution/reconstruction flags must not be enabled")

    required_fields = _dedupe_nonempty_strs(payload.required_evidence_fields, "required_evidence_fields")
    present_fields = _dedupe_nonempty_strs(payload.present_evidence_fields, "present_evidence_fields")
    explicit_reasons = _dedupe_nonempty_strs(
        payload.explicit_noncomputability_reasons,
        "explicit_noncomputability_reasons",
    )
    comparison_block_reasons = _dedupe_nonempty_strs(
        payload.comparison_block_reasons,
        "comparison_block_reasons",
    )

    missing_fields = tuple(field for field in required_fields if field not in set(present_fields))

    if not missing_fields:
        completeness = CompletenessState.COMPLETE
    elif len(missing_fields) == len(required_fields):
        completeness = CompletenessState.MISSING
    else:
        completeness = CompletenessState.PARTIAL

    missing_reasons = tuple(f"missing required evidence field: {field}" for field in missing_fields)
    noncomputability_reasons = _dedupe_nonempty_strs(
        (*explicit_reasons, *missing_reasons),
        "noncomputability_reasons",
    )

    current_run_computability = (
        CurrentRunComputabilityState.NONCOMPUTABLE
        if noncomputability_reasons
        else CurrentRunComputabilityState.COMPUTABLE
    )

    if payload.declared_comparability == ComparabilityState.ALLOWED:
        if comparison_block_reasons:
            raise ContractViolation(
                "comparison_block_reasons must be empty when declared_comparability is comparison-allowed"
            )
    else:
        if not comparison_block_reasons:
            raise ContractViolation(
                "comparison_block_reasons must be populated when declared_comparability is not comparison-allowed"
            )

    return ConceptStateRecord(
        concept_id=concept_id,
        completeness=completeness,
        current_run_computability=current_run_computability,
        comparability=payload.declared_comparability,
        noncomputability_reasons=noncomputability_reasons,
        comparison_block_reasons=comparison_block_reasons,
        missing_required_evidence_fields=missing_fields,
    )


def _base_reconciliation_inputs(payload: Mapping[str, Any], check_id_field: str = "check_id") -> str:
    check_id = _require_nonempty_str(payload.get(check_id_field), check_id_field)
    if payload.get("inference_used", False):
        raise ContractViolation(f"{check_id}: inference_used must be false")
    if payload.get("substitution_used", False):
        raise ContractViolation(f"{check_id}: substitution_used must be false")
    if payload.get("reconstruction_used", False):
        raise ContractViolation(f"{check_id}: reconstruction_used must be false")
    return check_id


def _as_int_tuple(values: Any, field_name: str) -> tuple[int, ...]:
    if not isinstance(values, (list, tuple)):
        raise ContractViolation(f"{field_name} must be a list or tuple")
    return tuple(_require_nonnegative_int(value, field_name) for value in values)


def _as_str_tuple(values: Any, field_name: str) -> tuple[str, ...]:
    if not isinstance(values, (list, tuple)):
        raise ContractViolation(f"{field_name} must be a list or tuple")
    return tuple(_require_nonempty_str(value, field_name) for value in values)


def _as_reason_tuple(values: Any, field_name: str) -> tuple[str, ...]:
    if values is None:
        return tuple()
    return _as_str_tuple(values, field_name)


def validate_denominator_partition(payload: Mapping[str, Any]) -> ReconciliationCheckResult:
    check_id = _base_reconciliation_inputs(payload)

    parent_denominator = _require_nonnegative_int(payload.get("parent_denominator"), "parent_denominator")
    partition_denominators = _as_int_tuple(payload.get("partition_denominators"), "partition_denominators")
    partition_labels = _as_str_tuple(payload.get("partition_labels"), "partition_labels")
    blocked_reasons = _as_reason_tuple(payload.get("blocked_reasons"), "blocked_reasons")

    if len(partition_denominators) != len(partition_labels):
        raise ContractViolation("partition_denominators and partition_labels must have equal length")

    evaluated_inputs = {
        "parent_denominator": parent_denominator,
        "partition_denominators": list(partition_denominators),
        "partition_labels": list(partition_labels),
    }

    if blocked_reasons:
        return ReconciliationCheckResult(
            check_id=check_id,
            check_type="denominator_partition",
            result=ReconciliationStatus.BLOCKED,
            evaluated_inputs=evaluated_inputs,
            reasons=blocked_reasons,
        )

    partition_sum = sum(partition_denominators)
    if partition_sum != parent_denominator:
        return ReconciliationCheckResult(
            check_id=check_id,
            check_type="denominator_partition",
            result=ReconciliationStatus.FAIL,
            evaluated_inputs=evaluated_inputs,
            reasons=(
                f"partition denominator sum mismatch: {partition_sum} != {parent_denominator}",
            ),
        )

    return ReconciliationCheckResult(
        check_id=check_id,
        check_type="denominator_partition",
        result=ReconciliationStatus.PASS,
        evaluated_inputs=evaluated_inputs,
        reasons=tuple(),
    )


def validate_parent_subslice_boundary(payload: Mapping[str, Any]) -> ReconciliationCheckResult:
    check_id = _base_reconciliation_inputs(payload)

    parent_numerator = _require_nonnegative_int(payload.get("parent_numerator"), "parent_numerator")
    parent_denominator = _require_nonnegative_int(payload.get("parent_denominator"), "parent_denominator")
    subslice_numerators = _as_int_tuple(payload.get("subslice_numerators"), "subslice_numerators")
    subslice_denominators = _as_int_tuple(payload.get("subslice_denominators"), "subslice_denominators")
    subslice_labels = _as_str_tuple(payload.get("subslice_labels"), "subslice_labels")
    blocked_reasons = _as_reason_tuple(payload.get("blocked_reasons"), "blocked_reasons")

    if not (len(subslice_numerators) == len(subslice_denominators) == len(subslice_labels)):
        raise ContractViolation("subslice numerators/denominators/labels must have equal length")

    evaluated_inputs = {
        "parent_numerator": parent_numerator,
        "parent_denominator": parent_denominator,
        "subslice_numerators": list(subslice_numerators),
        "subslice_denominators": list(subslice_denominators),
        "subslice_labels": list(subslice_labels),
    }

    if blocked_reasons:
        return ReconciliationCheckResult(
            check_id=check_id,
            check_type="parent_subslice_boundary",
            result=ReconciliationStatus.BLOCKED,
            evaluated_inputs=evaluated_inputs,
            reasons=blocked_reasons,
        )

    reasons: list[str] = []
    if sum(subslice_numerators) > parent_numerator:
        reasons.append(
            f"subslice numerator sum exceeds parent numerator: {sum(subslice_numerators)} > {parent_numerator}"
        )
    if sum(subslice_denominators) > parent_denominator:
        reasons.append(
            f"subslice denominator sum exceeds parent denominator: {sum(subslice_denominators)} > {parent_denominator}"
        )

    for label, numerator, denominator in zip(subslice_labels, subslice_numerators, subslice_denominators):
        if numerator > parent_numerator:
            reasons.append(f"subslice '{label}' numerator exceeds parent numerator")
        if denominator > parent_denominator:
            reasons.append(f"subslice '{label}' denominator exceeds parent denominator")

    if reasons:
        return ReconciliationCheckResult(
            check_id=check_id,
            check_type="parent_subslice_boundary",
            result=ReconciliationStatus.FAIL,
            evaluated_inputs=evaluated_inputs,
            reasons=tuple(reasons),
        )

    return ReconciliationCheckResult(
        check_id=check_id,
        check_type="parent_subslice_boundary",
        result=ReconciliationStatus.PASS,
        evaluated_inputs=evaluated_inputs,
        reasons=tuple(),
    )


def validate_split_to_aggregate(payload: Mapping[str, Any]) -> ReconciliationCheckResult:
    check_id = _base_reconciliation_inputs(payload)

    aggregate_numerator = _require_nonnegative_int(payload.get("aggregate_numerator"), "aggregate_numerator")
    aggregate_denominator = _require_nonnegative_int(payload.get("aggregate_denominator"), "aggregate_denominator")
    split_numerators = _as_int_tuple(payload.get("split_numerators"), "split_numerators")
    split_denominators = _as_int_tuple(payload.get("split_denominators"), "split_denominators")
    split_labels = _as_str_tuple(payload.get("split_labels"), "split_labels")
    blocked_reasons = _as_reason_tuple(payload.get("blocked_reasons"), "blocked_reasons")

    if not (len(split_numerators) == len(split_denominators) == len(split_labels)):
        raise ContractViolation("split numerators/denominators/labels must have equal length")

    evaluated_inputs = {
        "aggregate_numerator": aggregate_numerator,
        "aggregate_denominator": aggregate_denominator,
        "split_numerators": list(split_numerators),
        "split_denominators": list(split_denominators),
        "split_labels": list(split_labels),
    }

    if blocked_reasons:
        return ReconciliationCheckResult(
            check_id=check_id,
            check_type="split_to_aggregate",
            result=ReconciliationStatus.BLOCKED,
            evaluated_inputs=evaluated_inputs,
            reasons=blocked_reasons,
        )

    reasons: list[str] = []
    if sum(split_numerators) != aggregate_numerator:
        reasons.append(
            f"split numerator sum mismatch: {sum(split_numerators)} != {aggregate_numerator}"
        )
    if sum(split_denominators) != aggregate_denominator:
        reasons.append(
            f"split denominator sum mismatch: {sum(split_denominators)} != {aggregate_denominator}"
        )

    if reasons:
        return ReconciliationCheckResult(
            check_id=check_id,
            check_type="split_to_aggregate",
            result=ReconciliationStatus.FAIL,
            evaluated_inputs=evaluated_inputs,
            reasons=tuple(reasons),
        )

    return ReconciliationCheckResult(
        check_id=check_id,
        check_type="split_to_aggregate",
        result=ReconciliationStatus.PASS,
        evaluated_inputs=evaluated_inputs,
        reasons=tuple(),
    )


def validate_coverage_arithmetic(payload: Mapping[str, Any]) -> ReconciliationCheckResult:
    check_id = _base_reconciliation_inputs(payload)

    covered_count = _require_nonnegative_int(payload.get("covered_count"), "covered_count")
    uncovered_count = _require_nonnegative_int(payload.get("uncovered_count"), "uncovered_count")
    total_count = _require_nonnegative_int(payload.get("total_count"), "total_count")
    blocked_reasons = _as_reason_tuple(payload.get("blocked_reasons"), "blocked_reasons")

    evaluated_inputs = {
        "covered_count": covered_count,
        "uncovered_count": uncovered_count,
        "total_count": total_count,
    }

    if blocked_reasons:
        return ReconciliationCheckResult(
            check_id=check_id,
            check_type="coverage_arithmetic",
            result=ReconciliationStatus.BLOCKED,
            evaluated_inputs=evaluated_inputs,
            reasons=blocked_reasons,
        )

    if covered_count + uncovered_count != total_count:
        return ReconciliationCheckResult(
            check_id=check_id,
            check_type="coverage_arithmetic",
            result=ReconciliationStatus.FAIL,
            evaluated_inputs=evaluated_inputs,
            reasons=(
                f"coverage arithmetic mismatch: {covered_count} + {uncovered_count} != {total_count}",
            ),
        )

    return ReconciliationCheckResult(
        check_id=check_id,
        check_type="coverage_arithmetic",
        result=ReconciliationStatus.PASS,
        evaluated_inputs=evaluated_inputs,
        reasons=tuple(),
    )


def build_reconciliation_report(results: Iterable[ReconciliationCheckResult]) -> ReconciliationFoundationReport:
    result_list = list(results)
    counts = Counter(result.result for result in result_list)
    return ReconciliationFoundationReport(
        total_checks=len(result_list),
        pass_count=counts.get(ReconciliationStatus.PASS, 0),
        fail_count=counts.get(ReconciliationStatus.FAIL, 0),
        blocked_count=counts.get(ReconciliationStatus.BLOCKED, 0),
        results=result_list,
    )


def run_stage_c2_foundation_demo() -> StageC2FoundationReport:
    rows = [
        build_aggregation_row(
            {
                "family_id": "family_a",
                "concept_id": "family_a_non_exact",
                "row_id": "r1",
                "split_id": "train",
                "sub_slice_id": "direct-answer substitution",
                "eligible": True,
                "counted": True,
                "excluded": False,
                "provenance_ref": "dataset:2026-05-31",
                "evidence_ref": "evidence:r1",
            }
        ),
        build_aggregation_row(
            {
                "family_id": "family_a",
                "concept_id": "family_a_non_exact",
                "row_id": "r2",
                "split_id": "train",
                "sub_slice_id": "scalar substitution",
                "eligible": True,
                "counted": True,
                "excluded": False,
                "provenance_ref": "dataset:2026-05-31",
                "evidence_ref": "evidence:r2",
            }
        ),
        build_aggregation_row(
            {
                "family_id": "family_a",
                "concept_id": "family_a_non_exact",
                "row_id": "r3",
                "split_id": "val",
                "sub_slice_id": None,
                "eligible": True,
                "counted": False,
                "excluded": False,
                "provenance_ref": "dataset:2026-05-31",
                "evidence_ref": "evidence:r3",
            }
        ),
        build_aggregation_row(
            {
                "family_id": "family_a",
                "concept_id": "family_a_non_exact",
                "row_id": "r4",
                "split_id": "val",
                "sub_slice_id": None,
                "eligible": False,
                "counted": False,
                "excluded": True,
                "provenance_ref": "dataset:2026-05-31",
                "evidence_ref": "evidence:r4",
            }
        ),
    ]
    family_aggregation = aggregate_family_rows("family_a", rows)

    states = [
        evaluate_concept_state(
            StateEvaluationInput(
                concept_id="family_a_non_exact",
                required_evidence_fields=("non_exact_denominator", "subtype_counts"),
                present_evidence_fields=("non_exact_denominator", "subtype_counts"),
                explicit_noncomputability_reasons=tuple(),
                declared_comparability=ComparabilityState.BLOCKED,
                comparison_block_reasons=("no approved migration marker emitted",),
            )
        ),
        evaluate_concept_state(
            StateEvaluationInput(
                concept_id="family_a_direct_answer_subslice",
                required_evidence_fields=("subslice_numerator", "subslice_denominator"),
                present_evidence_fields=("subslice_numerator",),
                explicit_noncomputability_reasons=tuple(),
                declared_comparability=ComparabilityState.REFERENCE_ONLY,
                comparison_block_reasons=("historical value is reference-only",),
            )
        ),
    ]

    reconciliation_checks = [
        validate_denominator_partition(
            {
                "check_id": "family_a_partition",
                "parent_denominator": 3,
                "partition_denominators": [2, 1],
                "partition_labels": ["counted", "not_counted"],
            }
        ),
        validate_parent_subslice_boundary(
            {
                "check_id": "family_a_subslice_boundary",
                "parent_numerator": 2,
                "parent_denominator": 3,
                "subslice_numerators": [1, 1],
                "subslice_denominators": [1, 1],
                "subslice_labels": ["direct-answer substitution", "scalar substitution"],
            }
        ),
        validate_split_to_aggregate(
            {
                "check_id": "family_a_split_reconcile",
                "aggregate_numerator": 2,
                "aggregate_denominator": 3,
                "split_numerators": [2, 0],
                "split_denominators": [2, 1],
                "split_labels": ["train", "val"],
            }
        ),
        validate_coverage_arithmetic(
            {
                "check_id": "family_a_coverage",
                "covered_count": 3,
                "uncovered_count": 1,
                "total_count": 4,
            }
        ),
    ]

    return StageC2FoundationReport(
        family_aggregation=family_aggregation,
        state_records=states,
        reconciliation=build_reconciliation_report(reconciliation_checks),
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stage C2 family aggregation/state/reconciliation foundation"
    )
    parser.add_argument(
        "--report-output",
        default=None,
        help="Optional output path for Stage C2 foundation report JSON",
    )
    args = parser.parse_args()

    report = run_stage_c2_foundation_demo()
    payload = report.to_dict()

    if args.report_output:
        out_path = Path(args.report_output).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    # Demo must preserve the required invariants to return success.
    if report.reconciliation.fail_count > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
