from pydantic import BaseModel, Field
from typing import List, Optional

from .director import DirectorResponse


class MovieCreate(BaseModel):
    title: str
    director_id: int
    release_year: Optional[int] = None
    cast: Optional[str] = None
    genres: List[int] = Field(default_factory=list)  # list of genre IDs


class MovieUpdate(BaseModel):
    title: Optional[str] = None
    release_year: Optional[int] = None
    cast: Optional[str] = None
    genres: Optional[List[int]] = None  # if provided -> sync genres_movie


class MovieListItem(BaseModel):
    id: int
    title: str
    release_year: Optional[int] = None
    director: DirectorResponse
    genres: List[str] = Field(default_factory=list)  # genre names
    average_rating: Optional[float] = None
    ratings_count: int = 0

    class Config:
        from_attributes = True


class MovieDetail(BaseModel):
    id: int
    title: str
    release_year: Optional[int] = None
    director: DirectorResponse
    genres: List[str] = Field(default_factory=list)
    cast: Optional[str] = None
    average_rating: Optional[float] = None
    ratings_count: int = 0

    class Config:
        from_attributes = True


class MoviesPage(BaseModel):
    page: int
    page_size: int
    total_items: int
    items: List[MovieListItem]
