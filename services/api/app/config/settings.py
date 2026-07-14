from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "services/api/.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Denge Atlası API"
    service_name: str = "denge-atlasi-api"
    app_version: str = "0.1.0"
    environment: Literal["local", "staging", "production", "test"] = "local"
    api_host: str = "127.0.0.1"
    api_port: int = Field(default=8000, ge=1, le=65535)
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    max_request_body_bytes: int = Field(default=16_384, ge=1024, le=1_048_576)
    rate_limit_requests: int = Field(default=60, ge=1, le=10_000)
    rate_limit_window_seconds: int = Field(default=60, ge=1, le=3600)


@lru_cache
def get_settings() -> Settings:
    return Settings()
