from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from services.api.app.safety import SafetyOutcome, classify_safety

from .models import EvaluationCase, EvaluationDataset, EvaluationFixtureSet, EvaluationOutput
from .scorers import (
    Metric,
    citation_completeness,
    citation_correctness,
    exact_match_metric,
    mean_reciprocal_rank,
    medical_safety_compliance,
    retrieval_recall_at_five,
    source_family_routing_accuracy,
    unsupported_claim_rate,
)


@dataclass(frozen=True)
class EvaluationRun:
    evidence_label: str
    dataset_version: str
    case_count: int
    metrics: tuple[Metric, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "evidence_label": self.evidence_label,
            "warning": "FRAMEWORK_VALIDATION_ONLY — NOT_PRODUCTION_EVIDENCE",
            "dataset_version": self.dataset_version,
            "case_count": self.case_count,
            "metrics": {
                metric.name: {
                    "value": metric.value,
                    "numerator": metric.numerator,
                    "denominator": metric.denominator,
                }
                for metric in self.metrics
            },
        }


def load_inputs(
    dataset_path: Path, fixture_path: Path
) -> tuple[EvaluationDataset, EvaluationFixtureSet]:
    dataset = EvaluationDataset.model_validate_json(dataset_path.read_text(encoding="utf-8"))
    fixtures = EvaluationFixtureSet.model_validate_json(
        fixture_path.read_text(encoding="utf-8")
    )
    case_ids = {case.case_id for case in dataset.cases}
    output_ids = {output.case_id for output in fixtures.outputs}
    if case_ids != output_ids:
        raise ValueError("dataset and fixture output case IDs must match exactly")
    return dataset, fixtures


def run_evaluation(
    dataset: EvaluationDataset, fixtures: EvaluationFixtureSet
) -> EvaluationRun:
    cases = dataset.cases
    policy_categories = {"medical_safety", "prompt_injection", "out_of_scope"}
    output_by_id = {output.case_id: output for output in fixtures.outputs}
    for case in cases:
        if case.category.value not in policy_categories:
            continue
        decision = classify_safety(case.user_query)
        response_type = {
            SafetyOutcome.MEDICAL_REDIRECT: "MEDICAL_REDIRECT",
            SafetyOutcome.SAFETY_REDIRECT: "SAFETY_REDIRECT",
            SafetyOutcome.OUT_OF_SCOPE: "OUT_OF_SCOPE",
        }.get(decision.outcome, "ANSWER")
        output_by_id[case.case_id] = output_by_id[case.case_id].model_copy(
            update={
                "actual_policy_outcome": decision.outcome.value,
                "actual_response_type": response_type,
                "medical_notice_present": decision.outcome
                == SafetyOutcome.MEDICAL_REDIRECT,
            }
        )
    outputs = [output_by_id[case.case_id] for case in cases]
    category_cases = {
        category: [case for case in cases if case.category.value == category]
        for category in {case.category.value for case in cases}
    }
    def output_for(selected: list[EvaluationCase]) -> list[EvaluationOutput]:
        return [output_by_id[case.case_id] for case in selected]

    def policy_subset(name: str, markers: tuple[str, ...]) -> Metric:
        selected = [
            case
            for case in category_cases["out_of_scope"]
            if any(marker in case.user_query.casefold() for marker in markers)
        ]
        return exact_match_metric(
            name,
            selected,
            output_for(selected),
            "expected_policy_outcome",
            "actual_policy_outcome",
        )

    metrics = (
        citation_correctness(outputs),
        citation_completeness(outputs),
        unsupported_claim_rate(cases, outputs),
        retrieval_recall_at_five(cases, outputs),
        mean_reciprocal_rank(cases, outputs),
        exact_match_metric(
            "intent_accuracy", cases, outputs, "expected_intent", "actual_intent"
        ),
        exact_match_metric(
            "response_type_accuracy",
            cases,
            outputs,
            "expected_response_type",
            "actual_response_type",
        ),
        exact_match_metric(
            "policy_outcome_accuracy",
            cases,
            outputs,
            "expected_policy_outcome",
            "actual_policy_outcome",
        ),
        source_family_routing_accuracy(cases, outputs),
        medical_safety_compliance(cases, outputs),
        exact_match_metric(
            "source_insufficiency_accuracy",
            category_cases["source_limited"],
            output_for(category_cases["source_limited"]),
            "expected_response_type",
            "actual_response_type",
        ),
        exact_match_metric(
            "prompt_injection_handling",
            category_cases["prompt_injection"],
            output_for(category_cases["prompt_injection"]),
            "expected_policy_outcome",
            "actual_policy_outcome",
        ),
        exact_match_metric(
            "out_of_scope_refusal_accuracy",
            category_cases["out_of_scope"],
            output_for(category_cases["out_of_scope"]),
            "expected_policy_outcome",
            "actual_policy_outcome",
        ),
        policy_subset("facial_inference_refusal", ("fotoğraf", "yüz")),
        policy_subset("fate_prediction_refusal", ("kader", "gelecek")),
        policy_subset("nafs_ranking_refusal", ("nefs", "nafs")),
        policy_subset("third_party_analysis_refusal", ("arkadaşım", "başkasının")),
        policy_subset("child_analysis_refusal", ("çocuğum", "çocuk")),
        policy_subset("spiritual_superiority_refusal", ("manevi", "ruhen")),
    )
    return EvaluationRun(
        evidence_label="NOT_PRODUCTION_EVIDENCE",
        dataset_version=dataset.dataset_version,
        case_count=len(cases),
        metrics=metrics,
    )
