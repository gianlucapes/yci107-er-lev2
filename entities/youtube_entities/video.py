from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Video(BaseModel):
    publishedAt : Optional[datetime] = None
    title : str
    videoId : str
    description : Optional[str] = None
    thumb_url : str
