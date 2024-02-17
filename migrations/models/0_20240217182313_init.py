from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "source" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "amount" VARCHAR(40) NOT NULL,
    "currency" VARCHAR(5) NOT NULL  /* USD: USD\nKGS: KGS\nRUB: RUB\nTRY: TRY\nEUR: EUR */,
    "name" VARCHAR(32) NOT NULL
);
CREATE TABLE IF NOT EXISTS "expense" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "amount" VARCHAR(40) NOT NULL,
    "currency" VARCHAR(5) NOT NULL  /* USD: USD\nKGS: KGS\nRUB: RUB\nTRY: TRY\nEUR: EUR */,
    "name" TEXT NOT NULL,
    "date" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "source_id" INT REFERENCES "source" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
