from tortoise import Tortoise

from app.config import ROOT_DIR

TORTOISE_ORM = {
    "connections": {"default": f"sqlite://{ROOT_DIR}/db.sqlite3"},
    "apps": {
        "models": {
            "models": ["app.expenses.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init():
    await Tortoise.init(config=TORTOISE_ORM)


async def disconnect():
    await Tortoise.close_connections()
