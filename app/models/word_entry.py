from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class WordEntry(Base):
    __tablename__ = "word_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    pronunciation: Mapped[str] = mapped_column(String(200), default="")
    translation: Mapped[str] = mapped_column(String(300), default="")
    example: Mapped[str] = mapped_column(String(500), default="")
    example_translation: Mapped[str] = mapped_column(String(500), default="")
