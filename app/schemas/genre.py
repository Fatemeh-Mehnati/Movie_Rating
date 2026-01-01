from pydantic import BaseModel
from typing import Optional


class GenreBase(BaseModel):
    name: str
    description: Optional[str] = None


class GenreResponse(GenreBase):
    id: int

    class Config:
        from_attributes = True
