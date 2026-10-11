from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import resolve_user_id
from app.db.session import get_db
from app.schemas.feedback import FeedbackRequest, FeedbackResponse
from app.services import feedback_service

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("", response_model=FeedbackResponse)
def feedback(
    req: FeedbackRequest,
    auth_uid: str | None = Depends(resolve_user_id),
    db: Session = Depends(get_db),
) -> FeedbackResponse:
    req.user_id = auth_uid or req.user_id
    try:
        return feedback_service.evaluate(db, req)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"{type(exc).__name__}: {exc}")
