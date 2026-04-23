from fastapi import FastAPI

from app.api.routes.health import router as health_router


app = FastAPI(
    title="micro-api-work-items",
    version="0.1.0",
    description="Small REST API for managing generic work items.",
)

app.include_router(health_router)
