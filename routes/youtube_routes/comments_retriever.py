from fastapi import APIRouter, HTTPException,status
import requests
from config import settings
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
        if response.status_code == status.HTTP_200_OK:
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
        elif response.status_code == status.HTTP_403_FORBIDDEN:
                raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail={"error":"The request cannot be completed because you have exceeded your quota"})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error":str(e)})

