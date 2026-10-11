from typing import Literal

from pydantic import BaseModel

Level = Literal["A1", "A2", "B1", "B2", "C1", "C2"]


class ProfileOut(BaseModel):
    user_id: str
    username: str
    level: str

    model_config = {"from_attributes": True}


class ProfileUpdate(BaseModel):
    level: Level | None = None
    username: str | None = None
