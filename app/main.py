import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.inventory_items import router as inventory_items_router
from app.api.steam_accounts import router as steam_accounts_router
from app.api.users import router as users_router
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

app.include_router(users_router)
app.include_router(steam_accounts_router)
app.include_router(inventory_items_router)


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
