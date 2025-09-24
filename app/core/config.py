from __future__ import annotations

import os
from collections.abc import Iterable
from enum import Enum
from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import (
    BaseSettings,
    DotEnvSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ENV_FILE = PROJECT_ROOT / ".env"
ENV_FILE_TEMPLATE = ".env.{env}"
ENVIRONMENT_VARIABLE_NAMES: tuple[str, ...] = (
    "IG_ENVIRONMENT",
    "IG_ENV",
    "APP_ENV",
    "ENVIRONMENT",
)


class Environment(str, Enum):
    DEFAULT = "default"
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"

    @classmethod
    def parse(cls, raw: str | None) -> Environment:
        if raw is None:
            return cls.DEFAULT
        normalized = raw.strip().lower()
        mapping: dict[str, Environment] = {
            "default": cls.DEFAULT,
            "local": cls.DEFAULT,
            "dev": cls.DEV,
            "development": cls.DEV,
            "staging": cls.STAGING,
            "stage": cls.STAGING,
            "prod": cls.PROD,
            "production": cls.PROD,
        }
        try:
            return mapping[normalized]
        except KeyError as exc:  # pragma: no cover - defensive branch
            msg = (
                "Unsupported environment '{value}'. Expected one of: "
                "default, dev, staging, prod."
            )
            raise ValueError(msg.format(value=raw)) from exc


def _read_env_value_from_file(path: Path, keys: Iterable[str]) -> str | None:
    if not path.is_file():
        return None

    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return None

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        name, _, value = line.partition("=")
        name = name.strip()
        if name not in keys:
            continue
        return value.strip().strip('"').strip("'")
    return None


def _discover_environment() -> Environment:
    for candidate in ENVIRONMENT_VARIABLE_NAMES:
        value = os.getenv(candidate)
        if value:
            return Environment.parse(value)

    file_value = _read_env_value_from_file(DEFAULT_ENV_FILE, ENVIRONMENT_VARIABLE_NAMES)
    if file_value:
        return Environment.parse(file_value)

    return Environment.DEFAULT


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=DEFAULT_ENV_FILE,
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    environment: Environment = Field(
        default=Environment.DEFAULT,
        validation_alias=AliasChoices(*ENVIRONMENT_VARIABLE_NAMES),
    )
    app_name: str = Field(
        default="instagram-bot",
        validation_alias=AliasChoices("IG_APP_NAME", "APP_NAME"),
    )
    api_prefix: str = Field(
        default="/",
        validation_alias=AliasChoices("IG_API_PREFIX", "API_PREFIX"),
    )
    debug: bool = Field(
        default=False,
        validation_alias=AliasChoices("IG_DEBUG", "DEBUG"),
    )
    log_level: str = Field(
        default="INFO",
        validation_alias=AliasChoices("IG_LOG_LEVEL", "LOG_LEVEL"),
    )
    database_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices("IG_DATABASE_URL", "DATABASE_URL"),
    )
    redis_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices("IG_REDIS_URL", "REDIS_URL"),
    )
    instagram_app_id: str | None = Field(
        default=None,
        validation_alias=AliasChoices("IG_INSTAGRAM_APP_ID", "INSTAGRAM_APP_ID"),
    )
    instagram_app_secret: str | None = Field(
        default=None,
        validation_alias=AliasChoices("IG_INSTAGRAM_APP_SECRET", "INSTAGRAM_APP_SECRET"),
    )
    webhook_verify_token: str | None = Field(
        default=None,
        validation_alias=AliasChoices("IG_WEBHOOK_VERIFY_TOKEN", "WEBHOOK_VERIFY_TOKEN"),
    )
    docs_url: str | None = Field(
        default="/docs",
        validation_alias=AliasChoices("IG_DOCS_URL", "DOCS_URL"),
    )
    redoc_url: str | None = Field(
        default="/redoc",
        validation_alias=AliasChoices("IG_REDOC_URL", "REDOC_URL"),
    )
    openapi_url: str | None = Field(
        default="/openapi.json",
        validation_alias=AliasChoices("IG_OPENAPI_URL", "OPENAPI_URL"),
    )

    @field_validator("environment", mode="before")
    def _coerce_environment(cls, value: str | None) -> Environment:
        return Environment.parse(value)

    @field_validator("log_level", mode="before")
    def _normalize_log_level(cls, value: str | None) -> str:
        if not value:
            return "INFO"
        return str(value).strip().upper()

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        environment = _discover_environment()
        env_specific_file = PROJECT_ROOT / ENV_FILE_TEMPLATE.format(env=environment.value)

        sources: list[PydanticBaseSettingsSource] = [
            init_settings,
            env_settings,
            dotenv_settings,
        ]

        if env_specific_file.is_file():
            sources.append(
                DotEnvSettingsSource(
                    settings_cls,
                    env_file=env_specific_file,
                    case_sensitive=False,
                    env_file_encoding="utf-8",
                )
            )

        sources.append(file_secret_settings)
        return tuple(sources)

    @property
    def is_default(self) -> bool:
        return self.environment is Environment.DEFAULT

    @property
    def is_dev(self) -> bool:
        return self.environment is Environment.DEV

    @property
    def is_staging(self) -> bool:
        return self.environment is Environment.STAGING

    @property
    def is_prod(self) -> bool:
        return self.environment is Environment.PROD


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()


__all__ = [
    "AppSettings",
    "Environment",
    "get_settings",
]
