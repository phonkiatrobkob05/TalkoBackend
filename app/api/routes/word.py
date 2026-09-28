from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.word import WordOut
from app.services import word_service

router = APIRouter(prefix="/word", tags=["word"])


@router.get("/{word}", response_model=WordOut)
def get_word(word: str, db: Session = Depends(get_db)) -> WordOut:
    try:
        entry = word_service.get_or_create(db, word)
    except Exception:
        raise HTTPException(status_code=503, detail="Word service is busy, please try again.")

    return WordOut(
        word=entry.word,
        pronunciation=entry.pronunciation,
        translation=entry.translation,
        example=entry.example,
        exampleTranslation=entry.example_translation,
    )
