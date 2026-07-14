from functools import lru_cache
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from services.api.app.contracts import AnalysisRequest, AnalysisResponse
from services.api.app.domain import AnalysisService

router = APIRouter(prefix="/api/v1", tags=["analysis"])


@lru_cache
def get_analysis_service() -> AnalysisService:
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="No production LLM provider is approved; configure AnalysisService explicitly.",
    )


@router.post(
    "/analyze/reflection",
    response_model=AnalysisResponse,
    operation_id="analyzeGroundedReflection",
)
def analyze_reflection(
    request: AnalysisRequest,
    service: Annotated[AnalysisService, Depends(get_analysis_service)],
) -> AnalysisResponse:
    return service.analyze(request)
