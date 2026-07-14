from fastapi import FastAPI

from services.api.app.api.analysis import router as analysis_router
from services.api.app.api.health import router as health_router
from services.api.app.api.search import router as search_router
from services.api.app.api.temperament import router as temperament_router
from services.api.app.config import get_settings
from services.api.app.security import SecurityMiddleware


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/docs" if settings.environment != "production" else None,
        redoc_url=None,
    )
    application.add_middleware(
        SecurityMiddleware,
        max_body_bytes=settings.max_request_body_bytes,
        rate_limit_requests=settings.rate_limit_requests,
        rate_limit_window_seconds=settings.rate_limit_window_seconds,
    )
    application.include_router(health_router)
    application.include_router(search_router)
    application.include_router(analysis_router)
    application.include_router(temperament_router)
    return application


app = create_app()
