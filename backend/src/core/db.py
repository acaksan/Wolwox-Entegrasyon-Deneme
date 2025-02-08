"""Veritabanı bağlantı havuzu"""

import logging
from typing import Optional

import fdb
from src.core.exceptions import DatabaseException
from src.core.settings import settings

logger = logging.getLogger(__name__)

class DatabasePool:
    """Firebird veritabanı bağlantı havuzu"""
    
    def __init__(self):
        """Veritabanı havuzunu başlat"""
        try:
            # Test bağlantısı yap
            self.test_connection = fdb.connect(
                host=settings.FIREBIRD_HOST,
                database=settings.FIREBIRD_DATABASE,
                user=settings.FIREBIRD_USER,
                password=settings.FIREBIRD_PASSWORD,
                port=settings.FIREBIRD_PORT,
                charset=settings.FIREBIRD_CHARSET
            )
            self.test_connection.close()
            logger.info("✅ Veritabanı havuzu başlatıldı")
            
        except Exception as e:
            logger.error(f"❌ Veritabanı havuzu başlatılamadı: {str(e)}")
            raise DatabaseException(f"Veritabanı havuzu hatası: {str(e)}")
    
    def get_connection(self) -> fdb.Connection:
        """Havuzdan bağlantı al"""
        try:
            return fdb.connect(
                host=settings.FIREBIRD_HOST,
                database=settings.FIREBIRD_DATABASE,
                user=settings.FIREBIRD_USER,
                password=settings.FIREBIRD_PASSWORD,
                port=settings.FIREBIRD_PORT,
                charset=settings.FIREBIRD_CHARSET
            )
        except Exception as e:
            logger.error(f"❌ Veritabanı bağlantısı alınamadı: {str(e)}")
            raise DatabaseException(f"Veritabanı bağlantı hatası: {str(e)}")

# Singleton instance
db_pool = DatabasePool()

__all__ = ['DatabasePool', 'db_pool'] 