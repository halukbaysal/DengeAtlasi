from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError
from services.api.app.evaluation.models import (
    EvaluatedClaim,
    EvaluationCase,
    EvaluationDataset,
    EvaluationOutput,
)
from services.api.app.evaluation.reporting import write_reports
from services.api.app.evaluation.runner import load_inputs, run_evaluation
from services.api.app.evaluation.scorers import (
    citation_completeness,
    citation_correctness,
    unsupported_claim_rate,
)

ROOT = Path(__file__).resolve().parents[3]
DATASET = ROOT / "evaluation/datasets/framework_validation/cases.json"
FIXTURES = ROOT / "evaluation/fixtures/framework_outputs.json"


def base_case(case_id: str = "FW-TST-001") -> EvaluationCase:
    return EvaluationCase(
        case_id=case_id,
        category="citation_correctness",
        language="tr",
        user_query="Kontrollü test sorusu",
        expected_intent="GENERAL",
        expected_response_type="ANSWER",
        expected_primary_source_family="MARIFETNAME",
        expected_relevant_source_ids=["SRC-MAR-9001"],
        required_citations=True,
        allowed_claims=["Kaynak denge temasını açıklar."],
        forbidden_claims=["Desteksiz kesin hüküm."],
        medical_notice_required=False,
        expected_policy_outcome="ALLOW",
        reviewer="framework-test",
        review_status="FRAMEWORK_VALIDATION_ONLY",
        notes="Not production evidence.",
    )


def output(
    claim: EvaluatedClaim, excerpt: str = "Kaynak denge temasını açıklar."
) -> EvaluationOutput:
    return EvaluationOutput(
        case_id="FW-TST-001",
        actual_intent="GENERAL",
        actual_response_type="ANSWER",
        actual_primary_source_family="MARIFETNAME",
        retrieved_source_ids=["SRC-MAR-9001"],
        claims=[claim],
        citation_text_by_id={"SRC-MAR-9001": excerpt},
        actual_policy_outcome="ALLOW",
        medical_notice_present=False,
    )


def test_dataset_schema_and_distribution_are_valid() -> None:
    dataset, fixtures = load_inputs(DATASET, FIXTURES)
    assert len(dataset.cases) >= 100
    assert len({case.case_id for case in dataset.cases}) == len(dataset.cases)
    assert {case.category.value for case in dataset.cases} == {
        "temperament_routing", "reflection", "source_search", "source_limited",
        "medical_safety", "prompt_injection", "citation_correctness",
        "citation_completeness", "unsupported_claims", "out_of_scope",
        "historical_terminology", "ocr_noise",
    }
    assert len(fixtures.outputs) == len(dataset.cases)


def test_duplicate_case_ids_are_rejected() -> None:
    with pytest.raises(ValidationError, match="must be unique"):
        EvaluationDataset(
            evidence_label="NOT_PRODUCTION_EVIDENCE",
            dataset_version="test",
            cases=[base_case(), base_case()],
        )


def test_citation_correctness_positive_and_negative() -> None:
    claim = EvaluatedClaim(
        text="Kaynak denge temasını açıklar.", citation_ids=["SRC-MAR-9001"]
    )
    assert citation_correctness([output(claim)]).value == 1.0
    assert citation_correctness([output(claim, "İlgisiz bir tarihsel pasaj.")]).value == 0.0


def test_citation_completeness_positive_and_negative() -> None:
    cited = EvaluatedClaim(text="Kaynak denge temasını açıklar.", citation_ids=["id"])
    uncited = EvaluatedClaim(text="Kaynak denge temasını açıklar.")
    assert citation_completeness([output(cited)]).value == 1.0
    assert citation_completeness([output(uncited)]).value == 0.0


def test_unsupported_claim_rate_positive_and_negative() -> None:
    supported = EvaluatedClaim(text="Kaynak denge temasını açıklar.", citation_ids=["id"])
    unsupported = EvaluatedClaim(text="Desteksiz kesin hüküm.", citation_ids=["id"])
    assert unsupported_claim_rate([base_case()], [output(supported)]).value == 0.0
    assert unsupported_claim_rate([base_case()], [output(unsupported)]).value == 1.0


def test_framework_run_and_reports_are_explicitly_non_production(tmp_path: Path) -> None:
    dataset, fixtures = load_inputs(DATASET, FIXTURES)
    run = run_evaluation(dataset, fixtures)
    assert run.case_count >= 100
    assert all(
        metric.value == 1.0 or metric.name == "unsupported_claim_rate"
        for metric in run.metrics
    )
    unsupported = next(
        metric for metric in run.metrics if metric.name == "unsupported_claim_rate"
    )
    assert unsupported.value == 0.0
    json_path, markdown_path = write_reports(run, tmp_path)
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["evidence_label"] == "NOT_PRODUCTION_EVIDENCE"
    assert "NOT_PRODUCTION_EVIDENCE" in markdown_path.read_text(encoding="utf-8")
