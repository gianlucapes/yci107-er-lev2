from pydantic import BaseModel
from datetime import datetime

class YoutubeChannel(BaseModel):
    publishedAt: datetime
    channelId: str
    title: str
    description: str
    url:str