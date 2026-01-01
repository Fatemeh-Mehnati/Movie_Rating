from typing import List, Optional, Tuple

from sqlalchemy import func, select, and_
from sqlalchemy.orm import Session, joinedload

from app.models.movie import Movie
from app.models.genre import Genre
from app.models.movie_rating import MovieRating
from app.exceptions.http_exceptions import NotFound


class MovieRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_movie_or_404(self, movie_id: int) -> Movie:
        movie = (
            self.db.query(Movie)
            .options(
                joinedload(Movie.director),
                joinedload(Movie.genres),
            )
            .filter(Movie.id == movie_id)
            .first()
        )
        if not movie:
            raise NotFound("Movie not found")
        return movie

    def list_movies(
        self,
        page: int = 1,
        page_size: int = 10,
        title: Optional[str] = None,
        release_year: Optional[int] = None,
        genre: Optional[str] = None,
    ) -> Tuple[int, List[Movie]]:
        """
        Returns: (total_items, movies)
        """
        query = self.db.query(Movie).options(
            joinedload(Movie.director),
            joinedload(Movie.genres),
        )

        filters = []
        if title:
            filters.append(Movie.title.ilike(f"%{title}%"))
        if release_year is not None:
            filters.append(Movie.release_year == release_year)
        if genre:
            query = query.join(Movie.genres)
            filters.append(Genre.name.ilike(f"%{genre}%"))

        if filters:
            query = query.filter(and_(*filters))

        # total count (distinct because of joins)
        total_items = query.distinct(Movie.id).count()

        movies = (
            query.order_by(Movie.id.asc())
            .distinct(Movie.id)
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return total_items, movies

    def create_movie(self, movie: Movie) -> Movie:
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def delete_movie(self, movie: Movie) -> None:
        self.db.delete(movie)
        self.db.commit()

    def add_rating(self, movie_id: int, score: int) -> MovieRating:
        # Ensure movie exists
        movie = self.db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            raise NotFound("Movie not found")

        rating = MovieRating(movie_id=movie_id, score=score)
        self.db.add(rating)
        self.db.commit()
        self.db.refresh(rating)
        return rating

    def get_rating_stats(self, movie_ids: List[int]) -> dict:
        """
        Returns dict: {movie_id: (avg, count)}
        """
        if not movie_ids:
            return {}

        rows = (
            self.db.query(
                MovieRating.movie_id.label("movie_id"),
                func.avg(MovieRating.score).label("avg"),
                func.count(MovieRating.id).label("cnt"),
            )
            .filter(MovieRating.movie_id.in_(movie_ids))
            .group_by(MovieRating.movie_id)
            .all()
        )
        return {r.movie_id: (float(r.avg), int(r.cnt)) for r in rows}
