from fastapi import APIRouter,HTTPException
import requests
from config import settings
from entities.youtube_entities.youtube_channel import YoutubeChannel
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
        raise HTTPException(status_code=500, detail={"error":str(e)})

