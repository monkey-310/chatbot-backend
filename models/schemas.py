from pydantic import BaseModel
from typing import List
from datetime import datetime

class ChatRequest(BaseModel):
  user_id: str
  message: str

class ChatResponse(BaseModel):
  answer: str

class HistoryRequest(BaseModel):
  user_id: str

class ChatHistory(BaseModel):
  user_id: str
  question: str
  answer: str
  created_at: datetime