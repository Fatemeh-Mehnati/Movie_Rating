from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.exceptions.handlers import success
from app.services.movie_service import MovieService
from app.schemas.movie import MovieCreate, MovieUpdate
from app.schemas.rating import RatingCreate

router = APIRouter(prefix="/api/v1/movies", tags=["movies"])


@router.get("/")
def list_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    title: Optional[str] = None,
    release_year: Optional[int] = None,
    genre: Optional[str] = None,
    db: Session = Depends(get_db),
):
    svc = MovieService(db)
    data = svc.list_movies(page=page, page_size=page_size, title=title, release_year=release_year, genre=genre)
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
    # طبق مستند: 204 بدون بدنه
    return


@router.post("/{movie_id}/ratings", status_code=201)
def add_rating(movie_id: int, payload: RatingCreate, db: Session = Depends(get_db)):
    svc = MovieService(db)
    data = svc.add_rating(movie_id, payload.score)
    return success(data, status_code=201)
