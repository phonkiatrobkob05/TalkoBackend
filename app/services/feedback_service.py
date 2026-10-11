from sqlalchemy.orm import Session

from app.models.scenario import Scenario
from app.schemas.feedback import FeedbackRequest
from app.services import gemini_service, progress_service


def evaluate(db: Session, req: FeedbackRequest) -> dict:
    scenario = db.get(Scenario, req.scenario_id) if req.scenario_id is not None else None
    objective = scenario.objective if scenario is not None else ""
    history = [turn.model_dump() for turn in req.history]

    result = gemini_service.generate_feedback(objective, req.level or "B1", history, req.metrics)

    if req.scenario_id is not None:
        progress_service.record(
            db, req.user_id, req.scenario_id, result["overall"], result["objectiveMet"]
        )

    return result
