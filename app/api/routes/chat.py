from fastapi import APIRouter
from pydantic import BaseModel

from app.services.gemini_service import generate_reply

router = APIRouter(prefix="/chat", tags=["chat"])


class Turn(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[Turn] = []


class ChatResponse(BaseModel):
    reply: str


@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    reply = generate_reply(req.message, [t.model_dump() for t in req.history])
    return ChatResponse(reply=reply)
