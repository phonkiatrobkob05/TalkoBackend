from pydantic import BaseModel


class WordOut(BaseModel):
    word: str
    pronunciation: str
    translation: str
    example: str
    exampleTranslation: str
