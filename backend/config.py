from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

class Settings(BaseSettings):
    GITHUB_USERNAME : str
    BASE_URL : str

    model_config = SettingsConfigDict(
    env_file=".env", 
    case_sensitive=True
)


settings = Settings()