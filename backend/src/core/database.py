"""Veritabanı bağlantısı modülü"""

from typing import Optional

import fdb
from core.logging import log_error, log_info, logger
from core.settings import get_settings

settings = get_settings()

def get_db_connection() -> Optional[fdb.Connection]:
    """Firebird veritabanı bağlantısı oluşturur"""
    try:
        connection = fdb.connect(
            dsn=settings.DB_PATH,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            charset=settings.DB_CHARSET
        )
        log_info("database", "Veritabanı bağlantısı başarılı")
        return connection
    except Exception as e:
        log_error("database", "Veritabanı bağlantı hatası", {"error": str(e)})
        return None

def close_db_connection(connection: fdb.Connection) -> None:
    """Veritabanı bağlantısını kapatır"""
    try:
        if connection and not connection.closed:
            connection.close()
            log_info("database", "Veritabanı bağlantısı kapatıldı")
    except Exception as e:
        log_error("database", "Bağlantı kapatma hatası", {"error": str(e)})

def execute_query(connection: fdb.Connection, query: str, params: tuple = None) -> Optional[list]:
    """SQL sorgusu çalıştırır ve sonuçları döndürür"""
    try:
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        results = cursor.fetchall()
        cursor.close()
        return results
    except Exception as e:
        log_error("database", "Sorgu çalıştırma hatası", {
            "query": query,
            "params": params,
            "error": str(e)
        })
        return None
