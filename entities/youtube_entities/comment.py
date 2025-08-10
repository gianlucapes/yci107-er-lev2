from pydantic import BaseModel
from datetime import datetime

class Comment(BaseModel):
    id: str
    publishedAt : datetime
    channelId : str
    videoId : str
    textDisplay : str
    textOriginal : str