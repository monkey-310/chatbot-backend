from fastapi import APIRouter, Body
from models.schemas import ChatResponse, ChatRequest, ChatHistory, HistoryRequest
from typing import List
from services.qdrant_service import store_message, fetch_relevant_memories, fetch_history
from services.openai_service import get_ai_response

router = APIRouter(prefix="/chat")

@router.post("/", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest = Body(...)):
  memories = fetch_relevant_memories(request.user_id, request.message)
  ai_reply = get_ai_response(request.message, memories)
  store_message(request.user_id, request.message, ai_reply)
  return ChatResponse(answer=ai_reply)

@router.post("/history", response_model=List[ChatHistory])
def history_endpoint(request: HistoryRequest = Body(...)):
  return fetch_history(request.user_id)
