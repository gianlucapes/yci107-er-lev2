from fastapi import APIRouter, HTTPException,status
import requests
from config import settings
from entities.youtube_entities.video import Video
import json


router = APIRouter()

@router.get("/video/search",tags=["video"])
async def search_video_by_name(channelId: str,max_results : int = 5):
    params = {
    "part": "snippet,id",
    "channelId":channelId,
    "maxResults":max_results,
    "order":"date",
    "type": "video",
    "key": settings.API_KEY_YOUTUBE_DEV
    }
    url = "https://www.googleapis.com/youtube/v3/search"
    try:
        response = requests.get(url, params=params)
        if response.status_code == status.HTTP_200_OK:
            videos=[]
            video={}
            for item in response.json()["items"]:
                video["videoId"] = item["id"]["videoId"]
                video["publishedAt"] = item["snippet"]["publishedAt"]
                video["title"] = item["snippet"]["title"]
                video["description"]  = item["snippet"]["description"]
                video["thumb_url"]  = item["snippet"]["thumbnails"]["high"]["url"]
                videos.append(video)
                video={}
            return [Video(**item) for item in videos]
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail={"error":"The request cannot be completed because you have exceeded your quota"})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error":str(e)})

