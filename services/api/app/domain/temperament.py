from uuid import uuid4

from services.api.app.contracts import (
    SearchIntent,
    SearchRequest,
    TemperamentFinding,
    TemperamentRequest,
    TemperamentResponse,
    TemperamentStatus,
)
from services.api.app.domain.retrieval import SearchService
from services.api.app.safety import DOCTOR_NOTICE, SafetyOutcome, classify_safety

EDUCATIONAL_DISCLAIMER = (
    "Bu çalışma tarihsel kaynaklara dayalı tematik bir öz-düşünüm aracıdır; "
    "kişilik testi, kesin mizaç sınıflandırması veya tıbbi değerlendirme değildir."
)
SAFE_SUGGESTIONS = (
    "Günlük gözlemlerinizi yargılamadan not etmeyi düşünebilirsiniz.",
    "Rutinlerinizde dengeyi destekleyen küçük ve sürdürülebilir adımları gözlemleyebilirsiniz.",
)
REFLECTION_QUESTIONS = (
    "Hangi günlük koşullarda daha dengeli hissettiğinizi fark ediyorsunuz?",
    "Bu temalardan hangisi deneyiminizle kısmen örtüşüyor, hangisi örtüşmüyor?",
)


class TemperamentService:
    def __init__(self, retrieval: SearchService) -> None:
        self._retrieval = retrieval

    def analyze(self, request: TemperamentRequest) -> TemperamentResponse:
        correlation_id = str(uuid4())
        safety = classify_safety(request.observations)
        if safety.outcome in {SafetyOutcome.MEDICAL_REDIRECT, SafetyOutcome.SAFETY_REDIRECT}:
            return TemperamentResponse(
                status=TemperamentStatus.MEDICAL_REDIRECT
                if safety.outcome == SafetyOutcome.MEDICAL_REDIRECT
                else TemperamentStatus.SAFETY_REDIRECT,
                source_limit_note=safety.message,
                medical_safety_notice=DOCTOR_NOTICE
                if safety.outcome == SafetyOutcome.MEDICAL_REDIRECT
                else None,
                educational_disclaimer=EDUCATIONAL_DISCLAIMER,
                correlation_id=correlation_id,
            )

        retrieval = self._retrieval.search_for_intent(
            SearchRequest(query=f"mizaç {request.observations}", top_k=5),
            intent_override=SearchIntent.TEMPERAMENT,
            force_supplement=request.include_lifestyle_context,
        )
        primary = []
        supplementary = []
        citations = []
        for group in retrieval.groups:
            for result in group.results:
                citations.append(result)
                finding = TemperamentFinding(
                    text=(
                        f"Alıntılanan tarihsel pasajda {result.section} teması "
                        "öz-düşünüm için ilgili olabilir."
                    ),
                    citation_ids=[result.chunk_id],
                )
                if group.role == "primary":
                    primary.append(finding)
                else:
                    supplementary.append(finding)

        if not primary:
            return TemperamentResponse(
                status=TemperamentStatus.SOURCE_LIMITED,
                source_limit_note="Onaylı Marifetname içeriği bu profil için yeterli değildir.",
                medical_safety_notice=DOCTOR_NOTICE
                if safety.outcome == SafetyOutcome.HEALTH_ADJACENT
                else None,
                educational_disclaimer=EDUCATIONAL_DISCLAIMER,
                correlation_id=correlation_id,
            )

        return TemperamentResponse(
            status=TemperamentStatus.THEMES_FOUND,
            primary_source_findings=primary,
            supplementary_findings=supplementary,
            supplement_reason=(
                "Uyku, hareket, mevsim ve yaşam tarzı bağlamı için Ibn Sina "
                "ayrı bir ek kaynak olarak kullanıldı."
                if supplementary
                else None
            ),
            symbolic_themes=["dengeyi gözlemleme", "alışkanlıklar üzerine düşünme"],
            safe_wellbeing_suggestions=list(SAFE_SUGGESTIONS),
            reflection_questions=list(REFLECTION_QUESTIONS),
            citations=citations,
            source_limit_note=retrieval.source_limit_note,
            medical_safety_notice=DOCTOR_NOTICE
            if safety.outcome == SafetyOutcome.HEALTH_ADJACENT
            else None,
            educational_disclaimer=EDUCATIONAL_DISCLAIMER,
            correlation_id=correlation_id,
        )
