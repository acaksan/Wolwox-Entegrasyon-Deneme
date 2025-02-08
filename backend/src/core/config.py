"""Konfigürasyon yönetimi"""

from functools import lru_cache

from .settings import Settings


@lru_cache()
def get_settings() -> Settings:
    """Settings instance'ı döndürür (cached)"""
    return Settings()

settings = get_settings()

__all__ = ['Settings', 'settings', 'get_settings']    
