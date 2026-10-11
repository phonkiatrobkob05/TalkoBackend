from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.progress import ProgressOut
from app.services import progress_service

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("", response_model=list[ProgressOut])
def get_progress(user_id: str = "demo", db: Session = Depends(get_db)):
    return progress_service.list_for_user(db, user_id)
