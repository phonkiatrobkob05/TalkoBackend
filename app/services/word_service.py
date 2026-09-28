from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.word_entry import WordEntry
from app.services import gemini_service


def get_or_create(db: Session, word: str) -> WordEntry:
    key = word.strip().lower()

    entry = db.scalar(select(WordEntry).where(WordEntry.word == key))
    if entry is not None:
        return entry

    info = gemini_service.generate_word_info(key)
    entry = WordEntry(
        word=key,
        pronunciation=info["pronunciation"],
        translation=info["translation"],
        example=info["example"],
        example_translation=info["example_translation"],
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
