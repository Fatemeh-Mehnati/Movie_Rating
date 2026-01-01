from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    director_id = Column(Integer, ForeignKey("directors.id", ondelete="RESTRICT"), nullable=False)
    release_year = Column(Integer, nullable=True)
    cast = Column(Text, nullable=True)

    director = relationship("Director", back_populates="movies")

    genres = relationship(
        "Genre",
        secondary="genres_movie",
        back_populates="movies",
    )

    ratings = relationship(
        "MovieRating",
        back_populates="movie",
        cascade="all, delete-orphan",
    )
