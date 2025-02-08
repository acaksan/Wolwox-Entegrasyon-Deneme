"""Cache servisi"""

import json
import logging
from typing import Any, Optional

from src.core.cache import cache
from src.core.exceptions import CacheException

logger = logging.getLogger(__name__)

class CacheService:
    """Cache işlemleri için servis sınıfı"""
    
    def __init__(self):
        self.cache = cache
        self.prefix = "wolvox:"
    
    def _make_key(self, key: str) -> str:
        """Cache anahtarı oluşturur"""
        return f"{self.prefix}{key}"
    
    async def get(self, key: str) -> Optional[Any]:
        """Cache'den veri okur"""
        try:
            data = await self.cache.get(self._make_key(key))
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.error(f"❌ Cache okuma hatası: {str(e)}")
            raise CacheException(f"Cache okuma hatası: {str(e)}")
    
    async def set(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None
    ) -> bool:
        """Cache'e veri yazar"""
        try:
            return await self.cache.set(
                self._make_key(key),
                json.dumps(value),
                expire
            )
        except Exception as e:
            logger.error(f"❌ Cache yazma hatası: {str(e)}")
            raise CacheException(f"Cache yazma hatası: {str(e)}")
    
    async def delete(self, key: str) -> bool:
        """Cache'den veri siler"""
        try:
            return await self.cache.delete(self._make_key(key))
        except Exception as e:
            logger.error(f"❌ Cache silme hatası: {str(e)}")
            raise CacheException(f"Cache silme hatası: {str(e)}")
    
    async def clear(self) -> bool:
        """Tüm cache'i temizler"""
        try:
            return await self.cache.clear()
        except Exception as e:
            logger.error(f"❌ Cache temizleme hatası: {str(e)}")
            raise CacheException(f"Cache temizleme hatası: {str(e)}")

# Singleton instance
cache_service = CacheService()

__all__ = ['CacheService', 'cache_service'] 