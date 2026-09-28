from sqlalchemy.orm import Session

from app.models.scenario import Scenario
from app.schemas.chat import ChatRequest
from app.services import gemini_service

BASE_IDENTITY = (
    "You are Talko, an English conversation partner for Thai learners. "
    "Keep replies short, natural, and encourage the learner to keep talking."
)


def build_system_prompt(req: ChatRequest, scenario: Scenario | None) -> str:
    parts = [BASE_IDENTITY]

    if req.mode == "scenario" and scenario is not None:
        parts.append(scenario.system_prompt)

    if req.level:
        parts.append(
            f"Respond in English at CEFR level {req.level}, "
            "matching the learner's level."
        )

    return " ".join(parts)


def reply(db: Session, req: ChatRequest) -> str:
    scenario = None
    if req.mode == "scenario" and req.scenario_id is not None:
        scenario = db.get(Scenario, req.scenario_id)

    system_prompt = build_system_prompt(req, scenario)
    history = [turn.model_dump() for turn in req.history]
    return gemini_service.generate(system_prompt, req.message, history)
