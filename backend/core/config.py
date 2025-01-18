from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = 'Project-Blog'
    PROJECT_VERSION: str = '1.0.0'

    POSTGRES_USER:str = 'test'
    POSTGRES_PASSWORD:str = 'test'
    POSTGRES_SERVER:str = 'localhost'
    POSTGRES_PORT:str = '5432'
    POSTGRES_DB:str = 'blog_db'
    DATABASE_URL:str = 'DatabaseUrl'

    model_config = SettingsConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )  # noqa


        

settings = Settings()

