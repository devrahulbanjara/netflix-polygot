import asyncpg
import motor.motor_asyncio
from app.config import settings

pg_pool: asyncpg.Pool | None = None

async def get_pg_pool() -> asyncpg.Pool:
    global pg_pool
    if pg_pool is None:
        pg_pool = await asyncpg.create_pool(
            dsn=settings.pg_dsn,
            min_size=2,
            max_size=10,  # max concurrent PG connections
        )
    return pg_pool

async def close_pg_pool():
    global pg_pool
    if pg_pool:
        await pg_pool.close()


mongo_client: motor.motor_asyncio.AsyncIOMotorClient | None = None

def get_mongo_db():
    global mongo_client
    if mongo_client is None:
        mongo_client = motor.motor_asyncio.AsyncIOMotorClient(
            settings.mongo_uri
        )
    return mongo_client[settings.MONGO_DB]

async def close_mongo():
    global mongo_client
    if mongo_client:
        mongo_client.close()