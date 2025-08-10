from fastapi import APIRouter
import requests
from config import settings
from db import neo4jService
from entities.youtube_channel import YoutubeChannel
import json


router = APIRouter()

@router.get("/youtubeChannel/search",tags=["youtube channel"])
async def search_channel_by_name(name: str):
    params = {
    "part": "snippet",
    "q": name,
    "type": "channel",
    "key": settings.API_KEY_YOUTUBE_DEV
    }
    url = "https://www.googleapis.com/youtube/v3/search"
    try:
        response = requests.get(url, params=params)
        channels=[]
        channel={}
        for item in response.json()["items"]:
            channel["channelId"] = item["id"]["channelId"]
            channel["publishedAt"] = item["snippet"]["publishedAt"]
            channel["title"] = item["snippet"]["title"]
            channel["description"]  = item["snippet"]["description"]
            channel["url"]  = item["snippet"]["thumbnails"]["high"]["url"]
            channels.append(channel)
            channel={}
        return [YoutubeChannel(**item) for item in channels]
    except Exception as e:
        raise e

@router.post("/youtubeChannel/insert",tags=["youtube channel"])
def insert_youtube_channel(youtubeChannel: YoutubeChannel):
    try:
        neo4jService.run_query("""
        MERGE (c:YoutubeChannel {
            publishedAt: $publishedAt,
            channelId: $channelId,
            title: $title,
            description: $description,
            url: $url
        })
        """,youtubeChannel.model_dump())
        return {"msg": "Youtube Channel created", "youtubeChannel": youtubeChannel}
    except Exception as e:
        raise e
