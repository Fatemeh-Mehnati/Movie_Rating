from sqlalchemy import Column, Integer, ForeignKey
from app.db.database import Base


class GenreMovie(Base):
    __tablename__ = "genres_movie"

    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)
