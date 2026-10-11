from pydantic import BaseModel


class Turn(BaseModel):
    role: str
    content: str


class FeedbackRequest(BaseModel):
    user_id: str = "demo"
    scenario_id: int | None = None
    history: list[Turn] = []
    level: str | None = "B1"
    metrics: dict | None = None


class ScoreBreakdown(BaseModel):
    clarity: int
    context: int
    continuity: int


class FeedbackResponse(BaseModel):
    overall: int
    scores: ScoreBreakdown
    objectiveMet: bool
    strengths: list[str]
    improvements: list[str]
