from typing import List
from sqlalchemy.orm import Session
from app.models.genre import Genre
from app.exceptions.http_exceptions import ValidationError


class GenreRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_ids(self, genre_ids: List[int]) -> List[Genre]:
        if not genre_ids:
            return []
        genres = self.db.query(Genre).filter(Genre.id.in_(genre_ids)).all()
        if len(genres) != len(set(genre_ids)):
            raise ValidationError("Invalid director_id or genres")
        return genres
