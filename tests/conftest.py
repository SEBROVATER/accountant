import pytest
from fastapi.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from app.main import get_app


@pytest.fixture(scope="session")
def client():
    config = {
        "connections": {"default": "sqlite://:memory:"},
        "apps": {
            "models": {
                "models": ["app.expenses.models"],
                "default_connection": "default",
            },
        },
    }
    app = get_app()
    register_tortoise(app, config)
    with TestClient(app) as client:
        yield client
