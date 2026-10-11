from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.feedback import FeedbackRequest, FeedbackResponse
from app.services import feedback_service

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("", response_model=FeedbackResponse)
def feedback(req: FeedbackRequest, db: Session = Depends(get_db)) -> FeedbackResponse:
    try:
        return feedback_service.evaluate(db, req)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"{type(exc).__name__}: {exc}")
