"""Cache yönetimi."""

from functools import wraps
from typing import Any, Optional

import redis
from core.logging import log_error, log_info, logger
from core.settings import get_settings

settings = get_settings()

# Redis bağlantısı
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD,
    decode_responses=True
)

class MockCache:
    """Mock cache sınıfı"""
    def __init__(self):
        self._cache = {}
        
    def get(self, key: str) -> Optional[Any]:
        """Mock veri getir"""
        log_info("cache", f"Mock cache get: {key}")
        return self._cache.get(key)
        
    def set(self, key: str, value: Any, expire: int = 300) -> None:
        """Mock veri kaydet"""
        log_info("cache", f"Mock cache set: {key}")
        self._cache[key] = value
        
    def delete(self, key: str) -> None:
        """Mock veri sil"""
        log_info("cache", f"Mock cache delete: {key}")
        self._cache.pop(key, None)

_cache = MockCache()

def get_cache() -> MockCache:
    """Mock cache örneği döndür"""
    return _cache

def cache_decorator(prefix: str, ttl: int = 3600):
    """Redis cache decorator"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Cache anahtarını oluştur
            key = f"{prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"
            
            try:
                # Cache'den veriyi al
                cached_data = redis_client.get(key)
                if cached_data:
                    log_info("cache", f"Cache hit: {key}")
                    return cached_data
                
                # Veriyi fonksiyondan al
                result = await func(*args, **kwargs)
                
                # Cache'e kaydet
                redis_client.setex(key, ttl, str(result))
                log_info("cache", f"Cache miss, saved: {key}")
                
                return result
            except Exception as e:
                log_error("cache", "Cache error", {"key": key, "error": str(e)})
                # Cache hatası durumunda fonksiyonu normal çalıştır
                return await func(*args, **kwargs)
        
        return wrapper
    return decorator
