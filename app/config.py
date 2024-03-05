from pathlib import Path
from typing import Any

from fastapi import Depends
from fastapi.responses import HTMLResponse
from pydantic_settings import BaseSettings, SettingsConfigDict

from general_utils.utils import get_base_dir

APP_DIR = Path(__file__).resolve().parent
ROOT_DIR = get_base_dir()

STATIC_DIR: Path = APP_DIR / "static"
TEMPLATE_DIR: Path = APP_DIR / "templates"


class Settings(BaseSettings):
    EXPENSES_USERNAME: str
    EXPENSES_PASSWORD: str

    model_config = SettingsConfigDict(env_file=ROOT_DIR / ".env")

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        from app.security import authenticate

        FASTAPI_PROPERTIES: dict[str, Any] = {
            "title": "Accounter",
            "description": "Personal expenses management",
            "version": "0.0.1",
            "default_response_class": HTMLResponse,
            "openapi_url": None,
            "openapi_prefix": None,
            "docs_url": None,
            "redoc_url": None,
            "dependencies": [Depends(authenticate)],
        }
        return FASTAPI_PROPERTIES


settings = Settings()
