from fastapi import APIRouter, Query
from services.qdrant_service import fetch_relevant_memories

router = APIRouter(prefix="/memory")

@router.get("/")
def get_memories(user_id: str = Query(...), query: str = Query(...)):
  return fetch_relevant_memories(user_id, query)