from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "expense" ADD "count" VARCHAR(40) NOT NULL  DEFAULT '1';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "expense" DROP COLUMN "count";"""
