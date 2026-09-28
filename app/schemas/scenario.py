from pydantic import BaseModel


class ScenarioOut(BaseModel):
    id: int
    category: str
    title: str
    description: str
    level: str

    model_config = {"from_attributes": True}
