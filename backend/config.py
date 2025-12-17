from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

class Settings(BaseSettings):
    GITHUB_USERNAME : str
    BASE_URL : str
    

settings = Settings()