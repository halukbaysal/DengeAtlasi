from enum import Enum

from pydantic import BaseModel, ConfigDict

from services.api.app.rag.normalization import normalize_text

DOCTOR_NOTICE = (
    "Bu içerik tarihsel ve genel bilgilendirme amaçlıdır; tıbbi değerlendirme, "
    "tanı veya tedavi yerine geçmez. Sağlıkla ilgili kararlar için hekime danışın."
)


class SafetyOutcome(str, Enum):
    ALLOW = "ALLOW"
    HEALTH_ADJACENT = "HEALTH_ADJACENT"
    MEDICAL_REDIRECT = "MEDICAL_REDIRECT"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
    SAFETY_REDIRECT = "SAFETY_REDIRECT"


class SafetyDecision(BaseModel):
    model_config = ConfigDict(frozen=True)

    outcome: SafetyOutcome
    message: str = ""


PROHIBITED_MEDICAL = frozenset(
    {
        "ilaç",
        "ilac",
        "doz",
        "dozaj",
        "tedavi",
        "teşhis",
        "teshis",
        "reçete",
        "recete",
        "bitkisel",
        "antibiyotik",
        "ilacı bırak",
        "ilaci birak",
        "tedavimi bırak",
        "tedavimi birak",
        "doktor yerine",
        "hekim yerine",
        "hangi hastalığı",
        "hangi hastaligi",
    }
)
HEALTH_TERMS = frozenset({"sağlık", "saglik", "hastalık", "hastalik", "belirti", "uyku"})
OUT_OF_SCOPE_TERMS = frozenset(
    {
        "yüz analizi", "yuz analizi", "fotoğraf", "fotograf", "kader",
        "geleceği söyle", "gelecegi soyle", "nefs mertebem", "nefis mertebem",
        "nefs mertebemi", "nefis mertebemi", "nafs ranking",
        "duygu analizi", "duygumu tanı", "duygumu tani",
        "çocuğumun kişiliğini", "cocugumun kisiligini",
        "başkasının kişiliğini", "baskasinin kisiligini",
        "arkadaşımın kişiliğini", "arkadasimin kisiligini",
        "manevi olarak", "ruhen üstün",
    }
)
INJECTION_MARKERS = (
    "ignore previous",
    "ignore all previous",
    "önceki talimatları",
    "onceki talimatlari",
    "system prompt",
    "sistem promptu",
    "gizli talimat",
    "developer message",
    "jailbreak",
    "environment variables",
    "güvenlik politikası yok",
    "guvenlik politikasi yok",
    "sırları söyle",
    "sirlari soyle",
)


def classify_safety(query: str) -> SafetyDecision:
    normalized = normalize_text(query).casefold()
    if any(marker in normalized for marker in INJECTION_MARKERS):
        return SafetyDecision(
            outcome=SafetyOutcome.SAFETY_REDIRECT,
            message="Bu istek güvenli analiz sınırları içinde işlenemiyor.",
        )
    if any(term in normalized for term in OUT_OF_SCOPE_TERMS):
        return SafetyDecision(
            outcome=SafetyOutcome.OUT_OF_SCOPE,
            message="Bu istek Denge Atlası'nın kaynak-temelli düşünme kapsamı dışındadır.",
        )
    if any(term in normalized for term in PROHIBITED_MEDICAL):
        return SafetyDecision(
            outcome=SafetyOutcome.MEDICAL_REDIRECT,
            message="Tanı, tedavi, ilaç veya doz önerisi sunamam. Bir hekime danışın.",
        )
    if any(term in normalized for term in HEALTH_TERMS):
        return SafetyDecision(outcome=SafetyOutcome.HEALTH_ADJACENT)
    return SafetyDecision(outcome=SafetyOutcome.ALLOW)
