from sqlalchemy.orm import Session
from app.models.director import Director
from app.exceptions.http_exceptions import ValidationError


class DirectorRepository:
    def __init__(self, db: Session):
        self.db = db

    def ensure_exists(self, director_id: int) -> None:
        exists = self.db.query(Director.id).filter(Director.id == director_id).first()
        if not exists:
            raise ValidationError("Invalid director_id or genres")
