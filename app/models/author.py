from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from ..db import db

if TYPE_CHECKING:
    from .book import Book

class Author(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    books: Mapped[list["Book"]] = relationship(back_populates="author")

    def to_dict(self):
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_dict(cls, author_data: dict):
        return cls(name=author_data["name"])