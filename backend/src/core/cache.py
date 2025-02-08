import json
import logging
from typing import Any, Optional

from redis import Redis
from redis import asyncio as aioredis

from .settings import settings

logger = logging.getLogger(__name__)

class AsyncCache:
    """Asenkron Redis cache yöneticisi"""
    
    def __init__(self):
        self._redis: Optional[aioredis.Redis] = None
        self._prefix = "wolvox:"
    
    async def connect(self) -> None:
        """Redis bağlantısı oluşturur"""
        try:
            if not self._redis:
                self._redis = aioredis.Redis(
                    host="localhost",
                    port=6379,
                    db=0,
                    decode_responses=True
                )
                await self._redis.ping()  # Bağlantıyı test et
                logger.info("✅ Redis bağlantısı başarılı")
        except Exception as e:
            logger.error(f"❌ Redis bağlantı hatası: {str(e)}")
            raise
    
    async def disconnect(self) -> None:
        """Redis bağlantısını kapatır"""
        if self._redis:
            await self._redis.aclose()  # aclose() kullan
            self._redis = None
            logger.info("Redis bağlantısı kapatıldı")
    
    def _make_key(self, key: str) -> str:
        """Cache anahtarı oluşturur"""
        return f"{self._prefix}{key}"
    
    async def get(self, key: str) -> Optional[Any]:
        """Cache'den veri okur"""
        try:
            if not self._redis:
                await self.connect()
            
            data = await self._redis.get(self._make_key(key))
            if data:
                return json.loads(data)
            return None
            
        except Exception as e:
            logger.error(f"❌ Cache okuma hatası: {str(e)}")
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None
    ) -> bool:
        """Cache'e veri yazar"""
        try:
            if not self._redis:
                await self.connect()
            
            await self._redis.set(
                self._make_key(key),
                json.dumps(value),
                ex=expire
            )
            return True
            
        except Exception as e:
            logger.error(f"❌ Cache yazma hatası: {str(e)}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Cache'den veri siler"""
        try:
            if not self._redis:
                await self.connect()
            
            await self._redis.delete(self._make_key(key))
            return True
            
        except Exception as e:
            logger.error(f"❌ Cache silme hatası: {str(e)}")
            return False
    
    async def clear(self) -> bool:
        """Tüm cache'i temizler"""
        try:
            if not self._redis:
                await self.connect()
            
            keys = await self._redis.keys(f"{self._prefix}*")
            if keys:
                await self._redis.delete(*keys)
            return True
            
        except Exception as e:
            logger.error(f"❌ Cache temizleme hatası: {str(e)}")
            return False

# Singleton instance
cache = AsyncCache() 