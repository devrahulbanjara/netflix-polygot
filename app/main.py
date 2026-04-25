from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import get_pg_pool, close_pg_pool, close_mongo
from app.routers import users, movies
from loguru import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_pg_pool()
    logger.info("PostgreSQL pool ready")
    logger.info("MongoDB client ready (lazy connect)")
    yield
    await close_pg_pool()
    await close_mongo()
    logger.info("All connections closed")

app = FastAPI(
    title="Netflix Polyglot API",
    description="Phase 1 - PostgreSQL + MongoDB",
    lifespan=lifespan
)

app.include_router(users.router)
app.include_router(movies.router)

@app.get("/health")
async def health():
    return {"status": "ok", "phase": 1, "databases": ["postgresql", "mongodb"]}