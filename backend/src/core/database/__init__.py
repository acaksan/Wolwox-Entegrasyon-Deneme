"""Veritabanı bağlantısı modülü"""

import fdb
from src.core.settings import Settings, get_settings
from src.utils.logger import logger

settings = get_settings()

def get_db_connection():
    """Firebird veritabanı bağlantısı oluşturur"""
    try:
        connection = fdb.connect(
            host=settings.FIREBIRD_HOST,
            database=settings.FIREBIRD_DATABASE,
            user=settings.FIREBIRD_USER,
            password=settings.FIREBIRD_PASSWORD,
            charset=settings.FIREBIRD_CHARSET
        )
        return connection
    except Exception as e:
        logger.error(f"Veritabanı bağlantı hatası: {str(e)}")
        raise Exception(f"Veritabanı bağlantı hatası: {str(e)}")
