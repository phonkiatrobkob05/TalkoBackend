from pydantic import BaseModel


class ScenarioOut(BaseModel):
    id: int
    title: str
    description: str
    level: str

    model_config = {"from_attributes": True}
