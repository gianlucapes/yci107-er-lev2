from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    API_KEY_YOUTUBE_DEV : str = os.environ.get("API_KEY_YOUTUBE_DEV")
    DEV : int = os.environ.get("DEV",default=0)


settings=Settings()