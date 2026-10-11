from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import resolve_user_id
from app.db.session import get_db
from app.schemas.profile import ProfileOut, ProfileUpdate
from app.services import profile_service

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=ProfileOut)
def get_profile(
    auth_uid: str | None = Depends(resolve_user_id),
    db: Session = Depends(get_db),
):
    return profile_service.get_or_create(db, auth_uid or "demo")


@router.put("", response_model=ProfileOut)
def update_profile(
    req: ProfileUpdate,
    auth_uid: str | None = Depends(resolve_user_id),
    db: Session = Depends(get_db),
):
    return profile_service.update(db, auth_uid or "demo", req.level, req.username)
