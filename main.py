from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from routes.channel_retriever import router as channel_search_router
from routes.video_retriever import router as video_router
from routes.comments_retriever import router as comment_router
from contextlib import asynccontextmanager

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup code here
    print("Starting up")
    yield
    # shutdown code here
    print("Shutting down")

app.include_router(channel_search_router)
app.include_router(video_router)
app.include_router(comment_router)
