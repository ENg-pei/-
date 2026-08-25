import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Optionally initialize database tables when the app starts."""
    if os.getenv("DB_INIT_ON_STARTUP", "false").lower() == "true":
        init_db()
    yield


app = FastAPI(
    title="CS Cloud Backend",
    description="CS云炼金后台API",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {
        "status": "running",
        "service": "CS Cloud Backend"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }
