from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.scenario import Scenario

SAMPLE_SCENARIOS = [
    {
        "title": "Ordering coffee",
        "description": "Practice ordering a drink at a cafe.",
        "level": "beginner",
    },
    {
        "title": "Checking in at a hotel",
        "description": "Practice checking in and asking about your room.",
        "level": "beginner",
    },
    {
        "title": "Job interview",
        "description": "Practice answering common interview questions.",
        "level": "intermediate",
    },
    {
        "title": "Asking for directions",
        "description": "Practice asking how to get to a place.",
        "level": "beginner",
    },
    {
        "title": "Making a doctor appointment",
        "description": "Practice booking an appointment and describing a problem.",
        "level": "intermediate",
    },
]


def seed_scenarios() -> None:
    db = SessionLocal()
    try:
        exists = db.scalar(select(Scenario).limit(1))
        if exists is None:
            db.add_all([Scenario(**s) for s in SAMPLE_SCENARIOS])
            db.commit()
    finally:
        db.close()
