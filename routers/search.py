from fastapi import APIRouter, Query
from vector_store import semantic_search

router = APIRouter()

@router.get("/")
def search(q: str = Query(...)):
    results = semantic_search(q)
    return {"results": results}
