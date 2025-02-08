import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # Database settings
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_NAME: str = os.getenv("DB_NAME", "")
    DB_USER: str = os.getenv("DB_USER", "SYSDBA")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "masterkey")

    # WooCommerce settings
    WC_URL: str = os.getenv("WC_URL", "")
    WC_CONSUMER_KEY: str = os.getenv("WC_CONSUMER_KEY", "")
    WC_CONSUMER_SECRET: str = os.getenv("WC_CONSUMER_SECRET", "")

    # Redis settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))

    class Config:
        env_file = ".env"

settings = Settings()
