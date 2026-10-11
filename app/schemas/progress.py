from pydantic import BaseModel


class ProgressOut(BaseModel):
    scenario_id: int
    status: str
    best_score: int
    attempts: int

    model_config = {"from_attributes": True}
