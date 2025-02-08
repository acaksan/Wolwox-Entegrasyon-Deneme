"""Firebird veritabanı servisi"""

import logging
from typing import Dict, Optional

import fdb
from src.core.exceptions import DatabaseException
from src.core.settings import settings

from .base_service import BaseService

logger = logging.getLogger(__name__)

class FirebirdService(BaseService):
    """Firebird veritabanı servisi"""
    
    def __init__(self):
        """Servisi başlat"""
        super().__init__()
        self.connections: Dict[str, fdb.Connection] = {}
        logger.info("✅ Firebird servisi başlatıldı")
    
    async def get_connection(self, name: str = "default") -> fdb.Connection:
        """
        Firebird bağlantısı al veya oluştur
        
        Args:
            name (str): Bağlantı adı
            
        Returns:
            fdb.Connection: Firebird bağlantısı
        """
        try:
            if name not in self.connections or self.connections[name].closed:
                self.connections[name] = fdb.connect(
                    host=settings.FIREBIRD_HOST,
                    database=settings.FIREBIRD_DATABASE,
                    user=settings.FIREBIRD_USER,
                    password=settings.FIREBIRD_PASSWORD,
                    charset=settings.FIREBIRD_CHARSET
                )
                logger.info(f"✅ Yeni Firebird bağlantısı oluşturuldu: {name}")
            
            return self.connections[name]
            
        except Exception as e:
            logger.error(f"❌ Firebird bağlantı hatası: {str(e)}")
            raise DatabaseException(f"Firebird bağlantı hatası: {str(e)}")
    
    async def test_connection(self) -> bool:
        """Firebird bağlantısını test et"""
        try:
            conn = await self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM RDB$DATABASE")
            cursor.close()
            logger.info("✅ Firebird bağlantı testi başarılı")
            return True
        except Exception as e:
            logger.error(f"❌ Firebird bağlantı testi hatası: {str(e)}")
            return False
    
    async def close_all(self):
        """Tüm bağlantıları kapat"""
        for name, conn in self.connections.items():
            try:
                if not conn.closed:
                    conn.close()
                    logger.info(f"✅ Firebird bağlantısı kapatıldı: {name}")
            except Exception as e:
                logger.error(f"❌ Bağlantı kapatma hatası: {str(e)}")

# Singleton instance
fb_service = FirebirdService()

__all__ = ['FirebirdService', 'fb_service'] 