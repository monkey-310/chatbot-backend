
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from os import getenv

load_dotenv()
from api import chat, memory

app = FastAPI()
app.include_router(chat.router)
app.include_router(memory.router)

if __name__ == "__main__":
    port = int(getenv("PORT", 3000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)