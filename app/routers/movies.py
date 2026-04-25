from typing import List, Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query

from app.database import get_mongo_db
from app.models.movie import MovieCreate, MovieOut

router = APIRouter(prefix="/movies", tags=["movies"])


def _serialize(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc


@router.get("/", response_model=List[MovieOut])
async def list_movies(
    genre: Optional[str] = Query(None),
    db=Depends(get_mongo_db),
):
    query = {"genres": genre} if genre else {}
    cursor = db.movies.find(query).limit(50)
    return [_serialize(doc) async for doc in cursor]


@router.get("/{movie_id}", response_model=MovieOut)
async def get_movie(movie_id: str, db=Depends(get_mongo_db)):
    try:
        oid = ObjectId(movie_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid movie id")
    doc = await db.movies.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Movie not found")
    return _serialize(doc)


@router.post("/", response_model=MovieOut, status_code=201)
async def create_movie(payload: MovieCreate, db=Depends(get_mongo_db)):
    result = await db.movies.insert_one(payload.model_dump())
    doc = await db.movies.find_one({"_id": result.inserted_id})
    return _serialize(doc)
