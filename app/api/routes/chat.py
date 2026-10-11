from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import resolve_user_id
from app.db.session import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services import chat_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(
    req: ChatRequest,
    auth_uid: str | None = Depends(resolve_user_id),
    db: Session = Depends(get_db),
) -> ChatResponse:
    req.user_id = auth_uid or req.user_id
    try:
        result = chat_service.reply(db, req)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"{type(exc).__name__}: {exc}")
    return ChatResponse(reply=result["reply"], finished=result["finished"])
