from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends

from services.api.app.config import Settings, get_settings
from services.api.app.contracts import HealthResponse

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse, operation_id="getHealth")
def health(settings: Annotated[Settings, Depends(get_settings)]) -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=settings.service_name,
        version=settings.app_version,
        timestamp=datetime.now(timezone.utc),
    )
