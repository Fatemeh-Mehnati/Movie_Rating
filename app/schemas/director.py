from pydantic import BaseModel
from typing import Optional


class DirectorBase(BaseModel):
    name: str
    birth_year: Optional[int] = None
    description: Optional[str] = None


class DirectorResponse(DirectorBase):
    id: int

    class Config:
        from_attributes = True
