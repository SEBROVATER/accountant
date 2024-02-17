from fastapi import FastAPI

from app.config import Settings
from app.routes import router
from fastapi.staticfiles import StaticFiles
settings = Settings()

def get_app() -> FastAPI:
    """Create a FastAPI app with the specified settings."""

    app = FastAPI(**settings.fastapi_kwargs)
    app.mount("/static", StaticFiles(directory=settings.APP_DIR / "static"), name="static")
    app.include_router(router)

    return app


app = get_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)