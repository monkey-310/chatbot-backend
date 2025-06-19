from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct
from models.schemas import ChatHistory
import datetime
import openai
import os
import uuid

openai.api_key = os.getenv("OPENAI_API_KEY")

qdrant = QdrantClient(
  url="https://af390ee6-7f61-4853-bdcd-904562f60e62.us-west-2-0.aws.cloud.qdrant.io:6333", 
  api_key=os.getenv("QDRANT_API_KEY"),
  check_compatibility=False
)
COLLECTION = "chat-memory"

def embed(text):
  return openai.embeddings.create(input=[text], model="text-embedding-ada-002").data[0].embedding

def store_message(user_id, question, answer):
  vector = embed(question)
  qdrant.upsert(collection_name=COLLECTION, points=[PointStruct(id=str(uuid.uuid4()), vector=vector, payload={"user_id": user_id, "question": question,"answer": answer, "created_at": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')})])

def fetch_history(user_id):
  result = qdrant.scroll(
    collection_name=COLLECTION,
    scroll_filter=models.Filter(
      must=[
        models.FieldCondition(
          key="user_id",
          match=models.MatchValue(value=user_id)
        )
      ]
    ),
    order_by= models.OrderBy(
      key="created_at",
      direction="asc",
    )
  )
  return [
      ChatHistory(
          user_id=hit.payload["user_id"],
          question=hit.payload["question"],
          answer=hit.payload["answer"],
          created_at=hit.payload["created_at"],
      ) for hit in result[0]
  ]

def fetch_relevant_memories(user_id, query):
  vector = embed(query)
  hits = qdrant.query_points(collection_name=COLLECTION, query=vector, limit=3, query_filter=models.Filter(
    must=[
      models.FieldCondition(
        key="user_id",
        match=models.MatchValue(value=user_id)
      )
    ]
  ), score_threshold=0.75)
  if len(hits.points) == 0:
    return []
  return [
    hit.payload["question"]
   for hit in hits.points
  ]
