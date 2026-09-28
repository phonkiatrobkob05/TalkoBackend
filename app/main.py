from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import chat, scenarios
from app.core.config import settings
from app.db.seed import seed_scenarios
from app.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_scenarios()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.include_router(chat.router)
app.include_router(scenarios.router)


@app.get("/health", tags=["system"])
def health() -> dict:
    return {"status": "ok", "app": settings.app_name}
