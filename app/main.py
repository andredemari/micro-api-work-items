from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from app.controllers.health_controller import router as health_router
from app.controllers.work_item_controller import router as work_items_router
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Initialize local persistence before the FastAPI app starts serving."""
    init_db()
    yield


app = FastAPI(
    title="micro-api-work-items",
    version="0.1.0",
    description="Small REST API for managing generic work items.",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(work_items_router)
