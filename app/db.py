from tortoise import Tortoise, run_async

from app.config import ROOT_DIR

(ROOT_DIR / "db").mkdir(exist_ok=True)
TORTOISE_ORM = {
    "connections": {"default": f"sqlite://{ROOT_DIR}/db/db.sqlite3"},
    "apps": {
        "models": {
            "models": ["app.expenses.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def aconnect():
    await Tortoise.init(config=TORTOISE_ORM)


def connect():
    run_async(aconnect())


async def adisconnect():
    await Tortoise.close_connections()


def disconnect():
    run_async(adisconnect())


async def acreate_db():
    await aconnect()
    await Tortoise.generate_schemas()
    await adisconnect()


def create_db():
    run_async(acreate_db())
