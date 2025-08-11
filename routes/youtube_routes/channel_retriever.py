from fastapi import APIRouter,HTTPException,status
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
        if response.status_code == status.HTTP_200_OK:
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
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail={"error":"The request cannot be completed because you have exceeded your quota"})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error":str(e)})

