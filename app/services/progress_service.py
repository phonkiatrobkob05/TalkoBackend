from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.progress import Progress


def _get_or_create(db: Session, user_id: str, scenario_id: int) -> Progress:
    row = db.scalar(
        select(Progress).where(Progress.user_id == user_id, Progress.scenario_id == scenario_id)
    )
    if row is None:
        row = Progress(user_id=user_id, scenario_id=scenario_id, status="in_progress", best_score=0, attempts=0)
        db.add(row)
    return row


def start(db: Session, user_id: str, scenario_id: int) -> Progress:
    row = _get_or_create(db, user_id, scenario_id)
    row.attempts += 1
    if row.status != "completed":
        row.status = "in_progress"
    db.commit()
    db.refresh(row)
    return row


def record(db: Session, user_id: str, scenario_id: int, score: int, objective_met: bool) -> Progress:
    row = _get_or_create(db, user_id, scenario_id)
    row.best_score = max(row.best_score, score)
    if objective_met:
        row.status = "completed"
    db.commit()
    db.refresh(row)
    return row


def list_for_user(db: Session, user_id: str) -> list[Progress]:
    return list(db.scalars(select(Progress).where(Progress.user_id == user_id)))
