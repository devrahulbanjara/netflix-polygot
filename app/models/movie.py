from pydantic import BaseModel, Field
from typing import Literal
from bson import ObjectId

class CastMember(BaseModel):
    name: str
    role: str

class MovieCreate(BaseModel):
    title: str
    content_type: Literal["movie", "series", "documentary"]
    year: int = Field(..., ge=1888, le=2030)
    rating: str
    imdb_score: float | None = Field(None, ge=0.0, le=10.0)
    genres: list[str]
    cast: list[CastMember] = []
    languages: list[str] = ["en"]

class MovieResponse(BaseModel):
    id: str
    title: str
    content_type: str
    year: int
    genres: list[str]
    imdb_score: float | None

MovieOut = MovieResponse