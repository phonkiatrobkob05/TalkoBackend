from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.vocab import VocabItem
from app.schemas.vocab import VocabCreate


def save(db: Session, req: VocabCreate) -> VocabItem:
    key = req.word.strip()
    existing = db.scalar(
        select(VocabItem).where(VocabItem.user_id == req.user_id, VocabItem.word == key)
    )
    if existing is not None:
        existing.translation = req.translation or existing.translation
        existing.category = req.category or existing.category
        db.commit()
        db.refresh(existing)
        return existing

    item = VocabItem(
        user_id=req.user_id, word=key, translation=req.translation, category=req.category
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_for_user(db: Session, user_id: str) -> list[VocabItem]:
    return list(db.scalars(select(VocabItem).where(VocabItem.user_id == user_id)))


def delete(db: Session, item_id: int) -> bool:
    item = db.get(VocabItem, item_id)
    if item is None:
        return False
    db.delete(item)
    db.commit()
    return True
