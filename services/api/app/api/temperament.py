from functools import lru_cache
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from services.api.app.contracts import TemperamentRequest, TemperamentResponse
from services.api.app.domain import TemperamentService

router = APIRouter(prefix="/api/v1", tags=["analysis"])


@lru_cache
def get_temperament_service() -> TemperamentService:
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Production retrieval is not configured for temperament analysis.",
    )


@router.post(
    "/analyze/temperament",
    response_model=TemperamentResponse,
    operation_id="analyzeTemperamentThemes",
)
def analyze_temperament(
    request: TemperamentRequest,
    service: Annotated[TemperamentService, Depends(get_temperament_service)],
) -> TemperamentResponse:
    return service.analyze(request)
