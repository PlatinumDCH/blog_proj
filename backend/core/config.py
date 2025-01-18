from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = 'Project-Blog'
    PROJECT_VERSION: str = '1.0.0'

    POSTGRES_USER:str = 'test'
    POSTGRES_PASSWORD:str = 'test'
    POSTGRES_SERVER:str = 'localhost'
    POSTGRES_PORT:int = 5432
    POSTGRES_DB:str = 'blog_db'
    DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'

    model_config = SettingsConfigDict(
        extra='ignore'
    )

    class Conf:
        env_file = '.env'
        env_file_encoding = 'unf-8'

settings = Settings()

