from typing import Literal

from pydantic import BaseModel


class Turn(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    mode: Literal["free", "scenario"] = "free"
    scenario_id: int | None = None
    message: str
    history: list[Turn] = []
    level: str | None = "B1"


class ChatResponse(BaseModel):
    reply: str
