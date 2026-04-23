from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


app = FastAPI(
    title="micro-api-work-items",
    version="0.1.0",
    description="Small REST API for managing generic work items.",
    lifespan=lifespan,
)

app.include_router(health_router)
