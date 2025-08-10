from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    API_KEY_YOUTUBE_DEV : str = os.environ.get("API_KEY_YOUTUBE_DEV")
    NEO4J_PASSWORD : str = os.environ.get("NEO4J_PASSWORD")


settings=Settings()