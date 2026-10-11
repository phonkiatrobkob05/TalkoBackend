from pydantic import BaseModel


class VocabCreate(BaseModel):
    user_id: str = "demo"
    word: str
    translation: str = ""
    category: str = ""


class VocabOut(BaseModel):
    id: int
    word: str
    translation: str
    category: str

    model_config = {"from_attributes": True}
