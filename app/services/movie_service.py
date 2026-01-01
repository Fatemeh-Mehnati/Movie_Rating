from typing import Optional, Dict, Any, List

from sqlalchemy.orm import Session

from app.models.movie import Movie
from app.repositories.movie_repository import MovieRepository
from app.repositories.director_repository import DirectorRepository
from app.repositories.genre_repository import GenreRepository
from app.schemas.movie import MovieCreate, MovieUpdate
from app.exceptions.http_exceptions import NotFound, ValidationError


class MovieService:
    def __init__(self, db: Session):
        self.db = db
        self.movies = MovieRepository(db)
        self.directors = DirectorRepository(db)
        self.genres = GenreRepository(db)

    def _to_list_item(self, movie: Movie, avg: Optional[float], cnt: int) -> Dict[str, Any]:
        return {
            "id": movie.id,
            "title": movie.title,
            "release_year": movie.release_year,
            "director": {
                "id": movie.director.id,
                "name": movie.director.name,
                "birth_year": movie.director.birth_year,
                "description": movie.director.description,
            },
            "genres": [g.name for g in movie.genres],
            "average_rating": avg,
            "ratings_count": cnt,
        }

    def list_movies(
        self,
        page: int = 1,
        page_size: int = 10,
        title: Optional[str] = None,
        release_year: Optional[int] = None,
        genre: Optional[str] = None,
    ) -> Dict[str, Any]:
        total, items = self.movies.list_movies(page, page_size, title, release_year, genre)
        ids = [m.id for m in items]
        stats = self.movies.get_rating_stats(ids)  # {id: (avg, cnt)}

        mapped = []
        for m in items:
            avg, cnt = stats.get(m.id, (None, 0))
            mapped.append({
                "id": m.id,
                "title": m.title,
                "release_year": m.release_year,
                "director": {"id": m.director.id, "name": m.director.name},
                "genres": [g.name for g in m.genres],
                "average_rating": avg,
                "ratings_count": cnt,
            })

        return {
            "page": page,
            "page_size": page_size,
            "total_items": total,
            "items": mapped,
        }

    def get_movie(self, movie_id: int) -> Dict[str, Any]:
        movie = self.movies.get_movie_or_404(movie_id)
        stats = self.movies.get_rating_stats([movie_id])
        avg, cnt = stats.get(movie_id, (None, 0))

        return {
            "id": movie.id,
            "title": movie.title,
            "release_year": movie.release_year,
            "director": {
                "id": movie.director.id,
                "name": movie.director.name,
                "birth_year": movie.director.birth_year,
                "description": movie.director.description,
            },
            "genres": [g.name for g in movie.genres],
            "cast": movie.cast,
            "average_rating": avg,
            "ratings_count": cnt,
        }

    def create_movie(self, payload: MovieCreate) -> Dict[str, Any]:
        if not payload.title:
            raise ValidationError("Invalid director_id or genres")

        self.directors.ensure_exists(payload.director_id)
        genre_objs = self.genres.get_by_ids(payload.genres)

        movie = Movie(
            title=payload.title,
            director_id=payload.director_id,
            release_year=payload.release_year,
            cast=payload.cast,
        )
        movie.genres = genre_objs

        movie = self.movies.create_movie(movie)

        # reload relations
        movie = self.movies.get_movie_or_404(movie.id)
        return {
            "id": movie.id,
            "title": movie.title,
            "release_year": movie.release_year,
            "director": {"id": movie.director.id, "name": movie.director.name},
            "genres": [g.name for g in movie.genres],
            "cast": movie.cast,
            "average_rating": None,
            "ratings_count": 0,
        }

    def update_movie(self, movie_id: int, payload: MovieUpdate) -> Dict[str, Any]:
        movie = self.movies.get_movie_or_404(movie_id)

        if payload.title is not None:
            movie.title = payload.title
        if payload.release_year is not None:
            movie.release_year = payload.release_year
        if payload.cast is not None:
            movie.cast = payload.cast

        # sync genres if provided
        if payload.genres is not None:
            genre_objs = self.genres.get_by_ids(payload.genres)
            movie.genres = genre_objs

        self.db.commit()
        self.db.refresh(movie)

        # reload relations
        movie = self.movies.get_movie_or_404(movie.id)
        stats = self.movies.get_rating_stats([movie.id])
        avg, cnt = stats.get(movie.id, (None, 0))

        return {
            "id": movie.id,
            "title": movie.title,
            "release_year": movie.release_year,
            "director": {"id": movie.director.id, "name": movie.director.name},
            "genres": [g.name for g in movie.genres],
            "cast": movie.cast,
            "average_rating": avg,
            "ratings_count": cnt,
        }

    def delete_movie(self, movie_id: int) -> None:
        movie = self.db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            raise NotFound("Movie not found")
        self.movies.delete_movie(movie)

    def add_rating(self, movie_id: int, score: int) -> Dict[str, Any]:
        if not isinstance(score, int) or score < 1 or score > 10:
            raise ValidationError("Score must be an integer between 1 and 10")

        rating = self.movies.add_rating(movie_id, score)
        return {
            "rating_id": rating.id,
            "movie_id": rating.movie_id,
            "score": rating.score,
            "created_at": rating.created_at.isoformat() if rating.created_at else None,
        }
