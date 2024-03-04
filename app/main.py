from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from app.config import Settings
from app.db import TORTOISE_ORM
from app.expenses.routes import router as expenses_router
from app.routes import router as main_router

settings = Settings()


def get_app() -> FastAPI:
    """Create a FastAPI app with the specified settings."""

    app = FastAPI(**settings.fastapi_kwargs)
    app.mount("/static", StaticFiles(directory=settings.APP_DIR / "static"), name="static")
    app.include_router(main_router)
    app.include_router(expenses_router)
    return app


app = get_app()
register_tortoise(app, config=TORTOISE_ORM)
