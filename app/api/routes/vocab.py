from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import resolve_user_id
from app.db.session import get_db
from app.schemas.vocab import VocabCreate, VocabOut
from app.services import vocab_service

router = APIRouter(prefix="/vocab", tags=["vocab"])


@router.post("", response_model=VocabOut)
def create_vocab(
    req: VocabCreate,
    auth_uid: str | None = Depends(resolve_user_id),
    db: Session = Depends(get_db),
) -> VocabOut:
    req.user_id = auth_uid or req.user_id
    return vocab_service.save(db, req)


@router.get("", response_model=list[VocabOut])
def list_vocab(
    user_id: str = "demo",
    auth_uid: str | None = Depends(resolve_user_id),
    db: Session = Depends(get_db),
):
    return vocab_service.list_for_user(db, auth_uid or user_id)


@router.delete("/{item_id}")
def delete_vocab(item_id: int, db: Session = Depends(get_db)) -> dict:
    if not vocab_service.delete(db, item_id):
        raise HTTPException(status_code=404, detail="Vocab item not found")
    return {"deleted": True}
