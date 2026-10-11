from sqlalchemy.orm import Session

from app.models.profile import Profile


def get_or_create(db: Session, user_id: str, username: str = "") -> Profile:
    row = db.get(Profile, user_id)
    if row is None:
        row = Profile(user_id=user_id, username=username, level="B1")
        db.add(row)
        db.commit()
        db.refresh(row)
    return row


def update(db: Session, user_id: str, level: str | None, username: str | None) -> Profile:
    row = get_or_create(db, user_id)
    if level is not None:
        row.level = level
    if username is not None:
        row.username = username
    db.commit()
    db.refresh(row)
    return row
