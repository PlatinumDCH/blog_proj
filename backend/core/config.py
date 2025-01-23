from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = 'Project-Blog'
    PROJECT_VERSION: str = '1.0.0'

    POSTGRES_USER:str = 'test'
    POSTGRES_PASSWORD:str = 'test'
    POSTGRES_SERVER:str = 'localhost'
    POSTGRES_PORT:str = '5432'
    POSTGRES_DB:str = 'blog_db'
    DATABASE_URL:str = 'DatabaseUrl'

    SECRET_KEY_JWT:str = '**************************************'   
    ALGORITHM: str = "******"                         
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 30  

    refresh_token: str = "refresh_token"
    access_token: str = "access_token"

    model_config = SettingsConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )  # noqa


        

settings = Settings()

