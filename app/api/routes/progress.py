from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import resolve_user_id
from app.db.session import get_db
from app.schemas.progress import ProgressOut
from app.services import progress_service

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("", response_model=list[ProgressOut])
def get_progress(
    user_id: str = "demo",
    auth_uid: str | None = Depends(resolve_user_id),
    db: Session = Depends(get_db),
):
    return progress_service.list_for_user(db, auth_uid or user_id)
