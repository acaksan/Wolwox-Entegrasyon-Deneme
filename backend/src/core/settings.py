"""Konfigürasyon ayarları"""

import logging
import os
from functools import lru_cache
from pathlib import Path
from typing import List, Optional, Union

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Uygulama ayarları"""
    
    # Uygulama
    APP_NAME: str = "Wolvox-WooCommerce Entegrasyonu"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    LOG_LEVEL: Union[str, int] = logging.DEBUG
    ENVIRONMENT: str = "development"
    
    # Loglama
    LOG_FILE: str = "logs/app.log"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_ROTATION: str = "1 day"  # Log rotasyon süresi
    LOG_MAX_BYTES: int = 10 * 1024 * 1024  # 10MB
    
    # Firebird
    DB_PATH: str = Field(env='FIREBIRD_DATABASE', default=r"D:\AKINSOFT\Wolvox8\Database_FB\DEMOWOLVOX\2025\WOLVOX.FDB")
    DB_USER: str = Field(env='FIREBIRD_USER', default="SYSDBA")
    DB_PASSWORD: str = Field(env='FIREBIRD_PASSWORD', default="masterkey")
    DB_CHARSET: str = Field(env='FIREBIRD_CHARSET', default="WIN1254")
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    # WooCommerce
    WC_URL: str = Field(env='WOO_URL', default="https://lastik-al.com")
    WC_CONSUMER_KEY: str = Field(env='WOO_CONSUMER_KEY', default="ck_14ca8aab6f546bb34e5fd7f27ab0f77c6728c066")
    WC_CONSUMER_SECRET: str = Field(env='WOO_CONSUMER_SECRET', default="cs_62e4007a181e06ed919fa469baaf6e3fac8ea45f")
    WC_VERSION: str = "wc/v3"
    WC_VERIFY_SSL: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields in .env file
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    """Ayarları getir (önbellekli)"""
    return Settings()

# Varsayılan ayarları yükle
settings = get_settings()
