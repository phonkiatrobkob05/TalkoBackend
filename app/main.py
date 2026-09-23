from fastapi import FastAPI

from app.api.routes import chat
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(chat.router)


@app.get("/health", tags=["system"])
def health() -> dict:
    return {"status": "ok", "app": settings.app_name}
