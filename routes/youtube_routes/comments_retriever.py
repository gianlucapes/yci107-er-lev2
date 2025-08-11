from fastapi import APIRouter, HTTPException
import requests
from config import settings
from db import neo4jService
from entities.youtube_entities.comment import Comment
import json

router = APIRouter()

@router.get("/comments/search",tags=["comments"])
async def get_comments_by_video_id(videoId:str,max_results : int = 5):
    params = {
    "part": "snippet,replies",
    "videoId": videoId,
    "maxResults": max_results,
    "textFormat": "plainText",
    "key": settings.API_KEY_YOUTUBE_DEV
    }
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    try:
        response = requests.get(url, params=params)
        comments = []
        comment = {}
        for item in response.json()["items"]:
            comment["id"] = item["id"]
            comment["videoId"] = item["snippet"]["videoId"]
            comment["channelId"] = item["snippet"]["channelId"]
            comment["publishedAt"] = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
            comment["textDisplay"] = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comment["textOriginal"] = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
            comments.append(comment)
            comment = {}
        return [Comment(**item) for item in comments]
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error":str(e)})

