from typing import Optional
import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.exceptions.handlers import success
from app.services.movie_service import MovieService
from app.schemas.movie import MovieCreate, MovieUpdate
from app.schemas.rating import RatingCreate

router = APIRouter(prefix="/api/v1/movies", tags=["movies"])

# ✅ Logger for this module
logger = logging.getLogger("movie_rating")


@router.get("/")
def list_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    title: Optional[str] = None,
    release_year: Optional[int] = None,
    genre: Optional[str] = None,
    db: Session = Depends(get_db),
):
    # ✅ Log request info (Phase 2 requirement)
    logger.info(
        "Listing movies",
        extra={
            "route": "/api/v1/movies",
            "page": page,
            "page_size": page_size,
            "title": title,
            "release_year": release_year,
            "genre": genre,
        },
    )

    svc = MovieService(db)
    data = svc.list_movies(page=page, page_size=page_size, title=title, release_year=release_year, genre=genre)

    # ✅ Log result summary
    try:
        total_items = data.get("total_items")
        logger.info(
            "Movies listed successfully",
            extra={"route": "/api/v1/movies", "total_items": total_items, "returned_count": len(data.get("items", []))},
        )
    except Exception:
        # If the output structure is different, the log will not be corrupted.
        logger.info("Movies listed successfully", extra={"route": "/api/v1/movies"})

    return success(data)


@router.get("/{movie_id}")
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    svc = MovieService(db)
    data = svc.get_movie(movie_id)
    return success(data)


@router.post("/", status_code=201)
def create_movie(payload: MovieCreate, db: Session = Depends(get_db)):
    svc = MovieService(db)
    data = svc.create_movie(payload)
    return success(data, status_code=201)


@router.put("/{movie_id}")
def update_movie(movie_id: int, payload: MovieUpdate, db: Session = Depends(get_db)):
    svc = MovieService(db)
    data = svc.update_movie(movie_id, payload)
    return success(data)


@router.delete("/{movie_id}", status_code=204)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    svc = MovieService(db)
    svc.delete_movie(movie_id)
    return


@router.post("/{movie_id}/ratings", status_code=201)
def add_rating(movie_id: int, payload: RatingCreate, db: Session = Depends(get_db)):
    # ✅ Log rating attempt
    logger.info(
        "Adding rating to movie",
        extra={
            "route": f"/api/v1/movies/{movie_id}/ratings",
            "movie_id": movie_id,
            "score": payload.score,
        },
    )

    # ✅ Optional: defensive log (schema should already validate, but nice for visibility)
    if payload.score < 1 or payload.score > 10:
        logger.warning(
            "Invalid rating score received",
            extra={"movie_id": movie_id, "score": payload.score},
        )

    svc = MovieService(db)
    try:
        data = svc.add_rating(movie_id, payload.score)
        logger.info(
            "Rating added successfully",
            extra={"movie_id": movie_id, "score": payload.score},
        )
        return success(data, status_code=201)
    except Exception:
        # ✅ Log the full stacktrace for debugging
        logger.error(
            "Failed to add rating",
            extra={"movie_id": movie_id, "score": payload.score},
            exc_info=True,
        )
        raise
