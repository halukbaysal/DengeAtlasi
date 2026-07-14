from typing import Any

import pytest
from pydantic import ValidationError
from services.api.app.contracts import TemperamentRequest, TemperamentStatus
from services.api.app.domain import TemperamentService
from services.api.tests.test_analysis_service import build_retrieval


def request(**overrides: Any) -> TemperamentRequest:
    values = {
        "observations": "denge ve günlük alışkanlıklar",
        "consentAccepted": True,
        "confirmsAdult": True,
        "confirmsSelfReport": True,
        "includeLifestyleContext": False,
    }
    values.update(overrides)
    return TemperamentRequest.model_validate(values)


def test_consent_adult_and_self_report_are_required() -> None:
    for field in ("consentAccepted", "confirmsAdult", "confirmsSelfReport"):
        with pytest.raises(ValidationError):
            request(**{field: False})


def test_marifetname_is_primary_and_uses_uncertainty_language() -> None:
    response = TemperamentService(build_retrieval(minimum_score=0.0)).analyze(request())
    assert response.status == TemperamentStatus.THEMES_FOUND
    assert response.primary_source_findings
    assert response.citations[0].category == "PRIMARY"
    assert all("olabilir" in finding.text for finding in response.primary_source_findings)
    serialized = " ".join(
        finding.text for finding in response.primary_source_findings
    ).casefold()
    assert "kesin" not in serialized
    assert "puan" not in serialized


def test_ibn_sina_is_separate_and_has_supplement_reason() -> None:
    response = TemperamentService(build_retrieval(minimum_score=0.0)).analyze(
        request(includeLifestyleContext=True)
    )
    assert response.supplementary_findings
    assert response.supplement_reason and "Ibn Sina" in response.supplement_reason
    assert response.citations[0].category == "PRIMARY"
    assert any(item.category == "SUPPLEMENTARY" for item in response.citations)


def test_safe_suggestions_are_allowlisted_and_reflective() -> None:
    response = TemperamentService(build_retrieval(minimum_score=0.0)).analyze(request())
    assert response.safe_wellbeing_suggestions
    forbidden = ("ilaç", "doz", "tedavi", "hastalığın")
    assert not any(
        term in suggestion.casefold()
        for suggestion in response.safe_wellbeing_suggestions
        for term in forbidden
    )
    assert response.reflection_questions


def test_symptom_escalates_notice_and_medication_request_is_refused() -> None:
    service = TemperamentService(build_retrieval(minimum_score=0.0))
    symptom = service.analyze(request(observations="uyku belirtisi ve denge"))
    medicine = service.analyze(request(observations="ilaç dozu öner"))
    assert symptom.medical_safety_notice
    assert medicine.status == TemperamentStatus.MEDICAL_REDIRECT
    assert medicine.medical_safety_notice
    assert not medicine.safe_wellbeing_suggestions


def test_citations_are_derived_from_retrieval_and_source_limit_is_honest() -> None:
    response = TemperamentService(build_retrieval(minimum_score=0.0)).analyze(request())
    allowed = {citation.chunk_id for citation in response.citations}
    assert all(
        citation_id in allowed
        for finding in response.primary_source_findings
        for citation_id in finding.citation_ids
    )
    limited = TemperamentService(build_retrieval(minimum_score=2.0)).analyze(request())
    assert limited.status == TemperamentStatus.SOURCE_LIMITED
    assert limited.source_limit_note
