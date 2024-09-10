from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    API_ACCESS_TOKEN: str
    API_KEY: str
    API_SECRET: str
    SHOPIFY_URL: str
    API_VERSION: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"