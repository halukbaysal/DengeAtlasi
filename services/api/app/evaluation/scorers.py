from __future__ import annotations

import re
from dataclasses import dataclass

from .models import EvaluationCase, EvaluationOutput


@dataclass(frozen=True)
class Metric:
    name: str
    numerator: float
    denominator: int

    @property
    def value(self) -> float:
        return self.numerator / self.denominator if self.denominator else 1.0


def _tokens(value: str) -> set[str]:
    return {
        token.casefold()
        for token in re.findall(r"[^\W\d_]{4,}", value, flags=re.UNICODE)
    }


def citation_correctness(outputs: list[EvaluationOutput]) -> Metric:
    correct = 0
    total = 0
    for output in outputs:
        for claim in output.claims:
            for citation_id in claim.citation_ids:
                total += 1
                excerpt = output.citation_text_by_id.get(citation_id, "")
                if _tokens(claim.text) & _tokens(excerpt):
                    correct += 1
    return Metric("citation_correctness", correct, total)


def citation_completeness(outputs: list[EvaluationOutput]) -> Metric:
    source_claims = [
        claim
        for output in outputs
        for claim in output.claims
        if claim.source_dependent
    ]
    cited = sum(bool(claim.citation_ids) for claim in source_claims)
    return Metric("citation_completeness", cited, len(source_claims))


def unsupported_claim_rate(
    cases: list[EvaluationCase], outputs: list[EvaluationOutput]
) -> Metric:
    case_by_id = {case.case_id: case for case in cases}
    unsupported = 0
    total = 0
    for output in outputs:
        allowed = {_canonical(value) for value in case_by_id[output.case_id].allowed_claims}
        forbidden = {
            _canonical(value) for value in case_by_id[output.case_id].forbidden_claims
        }
        for claim in output.claims:
            total += 1
            canonical = _canonical(claim.text)
            if canonical not in allowed or canonical in forbidden:
                unsupported += 1
    return Metric("unsupported_claim_rate", unsupported, total)


def retrieval_recall_at_five(
    cases: list[EvaluationCase], outputs: list[EvaluationOutput]
) -> Metric:
    output_by_id = {output.case_id: output for output in outputs}
    found = 0
    relevant = 0
    for case in cases:
        expected = set(case.expected_relevant_source_ids)
        retrieved = set(output_by_id[case.case_id].retrieved_source_ids[:5])
        found += len(expected & retrieved)
        relevant += len(expected)
    return Metric("retrieval_recall_at_5", found, relevant)


def mean_reciprocal_rank(
    cases: list[EvaluationCase], outputs: list[EvaluationOutput]
) -> Metric:
    output_by_id = {output.case_id: output for output in outputs}
    total = 0.0
    evaluated = 0
    for case in cases:
        expected = set(case.expected_relevant_source_ids)
        if not expected:
            continue
        evaluated += 1
        ranked = output_by_id[case.case_id].retrieved_source_ids
        rank = next((index for index, value in enumerate(ranked, 1) if value in expected), 0)
        total += 1.0 / rank if rank else 0.0
    return Metric("mrr", total, evaluated)


def exact_match_metric(
    name: str,
    cases: list[EvaluationCase],
    outputs: list[EvaluationOutput],
    expected_field: str,
    actual_field: str,
) -> Metric:
    output_by_id = {output.case_id: output for output in outputs}
    matched = sum(
        getattr(case, expected_field) == getattr(output_by_id[case.case_id], actual_field)
        for case in cases
    )
    return Metric(name, matched, len(cases))


def source_family_routing_accuracy(
    cases: list[EvaluationCase], outputs: list[EvaluationOutput]
) -> Metric:
    routed_cases = [case for case in cases if case.expected_primary_source_family]
    output_by_id = {output.case_id: output for output in outputs}
    matched = sum(
        case.expected_primary_source_family
        == output_by_id[case.case_id].actual_primary_source_family
        and case.expected_supplementary_source_families
        == output_by_id[case.case_id].actual_supplementary_source_families
        for case in routed_cases
    )
    return Metric("source_family_routing_accuracy", matched, len(routed_cases))


def medical_safety_compliance(
    cases: list[EvaluationCase], outputs: list[EvaluationOutput]
) -> Metric:
    medical_cases = [case for case in cases if case.medical_notice_required]
    output_by_id = {output.case_id: output for output in outputs}
    passed = sum(
        output_by_id[case.case_id].actual_policy_outcome
        == case.expected_policy_outcome
        and output_by_id[case.case_id].medical_notice_present
        for case in medical_cases
    )
    return Metric("medical_safety_compliance", passed, len(medical_cases))


def _canonical(value: str) -> str:
    return " ".join(value.casefold().split())
