from typing import Any
from uuid import uuid4

from pydantic import ValidationError

from services.api.app.contracts import (
    AnalysisRequest,
    AnalysisResponse,
    AnalysisStatus,
    ProviderAnswer,
    SearchRequest,
    SearchStatus,
)
from services.api.app.domain.citations import CitationValidationError, CitationValidator
from services.api.app.domain.context import ContextBuilder
from services.api.app.domain.retrieval import SearchService
from services.api.app.prompts import GROUNDED_ANSWER_PROMPT, PromptMetadata
from services.api.app.providers import LLMProvider, ProviderTimeout
from services.api.app.safety import DOCTOR_NOTICE, SafetyOutcome, classify_safety


class AnalysisService:
    def __init__(
        self,
        retrieval: SearchService,
        provider: LLMProvider,
        *,
        prompt: PromptMetadata = GROUNDED_ANSWER_PROMPT,
        timeout_seconds: float = 10.0,
    ) -> None:
        self._retrieval = retrieval
        self._provider = provider
        self._prompt = prompt
        self._timeout_seconds = timeout_seconds
        self._context_builder = ContextBuilder()
        self._citations = CitationValidator()

    def analyze(self, request: AnalysisRequest) -> AnalysisResponse:
        correlation_id = str(uuid4())
        decision = classify_safety(request.query)
        if decision.outcome in {
            SafetyOutcome.OUT_OF_SCOPE,
            SafetyOutcome.SAFETY_REDIRECT,
            SafetyOutcome.MEDICAL_REDIRECT,
        }:
            return self._policy_response(decision.outcome, decision.message, correlation_id)

        retrieval = self._retrieval.search(
            SearchRequest(query=request.query, top_k=request.top_k)
        )
        retrieved = [item for group in retrieval.groups for item in group.results]
        medical_adjacent = decision.outcome == SafetyOutcome.HEALTH_ADJACENT
        if retrieval.status == SearchStatus.EMPTY or not retrieved:
            return AnalysisResponse(
                status=AnalysisStatus.SOURCE_LIMITED,
                source_limit_note=retrieval.source_limit_note
                or "Onaylı kaynaklarda yeterli dayanak bulunamadı.",
                medical_notice=DOCTOR_NOTICE if medical_adjacent else None,
                correlation_id=correlation_id,
            )

        context = self._context_builder.build(
            query=request.query,
            retrieval=retrieval,
            prompt=self._prompt,
            medical_adjacent=medical_adjacent,
        )
        try:
            raw: Any = self._provider.generate(context, timeout_seconds=self._timeout_seconds)
            answer = ProviderAnswer.model_validate(raw)
        except (ProviderTimeout, TimeoutError):
            return AnalysisResponse(
                status=AnalysisStatus.PROVIDER_UNAVAILABLE,
                message="Yanıt sağlayıcısı şu anda kullanılamıyor; daha sonra yeniden deneyin.",
                medical_notice=DOCTOR_NOTICE if medical_adjacent else None,
                correlation_id=correlation_id,
            )
        except (ValidationError, TypeError, ValueError):
            return AnalysisResponse(
                status=AnalysisStatus.PROVIDER_UNAVAILABLE,
                message="Sağlayıcı geçerli yapılandırılmış yanıt döndürmedi.",
                medical_notice=DOCTOR_NOTICE if medical_adjacent else None,
                correlation_id=correlation_id,
            )

        try:
            citations = self._citations.validate(answer.sourced_claims, retrieved)
        except CitationValidationError:
            return AnalysisResponse(
                status=AnalysisStatus.CITATION_VALIDATION_FAILED,
                message="Yanıt doğrulanabilir kaynak atıfları içermediği için engellendi.",
                medical_notice=DOCTOR_NOTICE if medical_adjacent else None,
                correlation_id=correlation_id,
            )

        return AnalysisResponse(
            status=AnalysisStatus.ANSWER,
            sourced_claims=answer.sourced_claims,
            general_symbolic_interpretation=answer.general_symbolic_interpretation,
            citations=citations,
            source_limit_note=retrieval.source_limit_note,
            medical_notice=DOCTOR_NOTICE if medical_adjacent else None,
            prompt_id=self._prompt.prompt_id,
            prompt_version=self._prompt.version,
            correlation_id=correlation_id,
        )

    @staticmethod
    def _policy_response(
        outcome: SafetyOutcome, message: str, correlation_id: str
    ) -> AnalysisResponse:
        statuses = {
            SafetyOutcome.OUT_OF_SCOPE: AnalysisStatus.OUT_OF_SCOPE,
            SafetyOutcome.SAFETY_REDIRECT: AnalysisStatus.SAFETY_REDIRECT,
            SafetyOutcome.MEDICAL_REDIRECT: AnalysisStatus.MEDICAL_REDIRECT,
        }
        return AnalysisResponse(
            status=statuses[outcome],
            message=message,
            medical_notice=DOCTOR_NOTICE
            if outcome == SafetyOutcome.MEDICAL_REDIRECT
            else None,
            correlation_id=correlation_id,
        )
