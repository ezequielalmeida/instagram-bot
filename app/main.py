from __future__ import annotations

import logging

from fastapi import APIRouter, FastAPI

from app.core.config import get_settings

settings = get_settings()

logging.basicConfig(level=settings.log_level, format="%(levelname)s [%(name)s] %(message)s")
logger = logging.getLogger("instagram_bot")


def _normalize_prefix(raw_prefix: str) -> str:
    if not raw_prefix:
        return ""
    prefix = raw_prefix.strip()
    if not prefix or prefix == "/":
        return ""
    if not prefix.startswith("/"):
        prefix = f"/{prefix}"
    return prefix.rstrip("/")


def _is_debug_enabled() -> bool:
    return settings.debug or settings.is_dev or settings.is_default


api_prefix = _normalize_prefix(settings.api_prefix)
router = APIRouter(prefix=api_prefix or "")


@router.get("/ping", tags=["health"])
async def ping() -> dict[str, str]:
    return {
        "status": "ok",
        "environment": settings.environment.value,
    }


debug_enabled = _is_debug_enabled()
docs_url = settings.docs_url if debug_enabled else None
redoc_url = settings.redoc_url if debug_enabled else None

api = FastAPI(
    title=settings.app_name,
    debug=debug_enabled,
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=settings.openapi_url,
)
api.include_router(router)


@api.on_event("startup")
async def _log_startup() -> None:
    logger.info(
        "Starting FastAPI app",
        extra={
            "environment": settings.environment.value,
            "debug": debug_enabled,
            "api_prefix": api_prefix or "/",
        },
    )


__all__ = ["api"]
