from contextlib import contextmanager
from typing import Optional

import fdb
from src.core.exceptions import DatabaseException
from src.core.settings import get_settings
from src.utils.logger import log_event

settings = get_settings()

class DatabaseConnection:
    _instance: Optional['DatabaseConnection'] = None
    _connection: Optional[fdb.Connection] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.connection_params = {
            "host": settings.FIREBIRD_HOST,
            "database": settings.FIREBIRD_DATABASE,
            "user": settings.FIREBIRD_USER,
            "password": settings.FIREBIRD_PASSWORD,
            "charset": settings.FIREBIRD_CHARSET
        }

    @contextmanager
    def get_connection(self):
        try:
            if not self._connection or self._connection.closed:
                self._connection = fdb.connect(**self.connection_params)
                log_event("INFO", "database", "Veritabanı bağlantısı açıldı")
            yield self._connection
        except Exception as e:
            log_event("ERROR", "database", "Bağlantı hatası", str(e))
            raise DatabaseException(f"Veritabanı bağlantı hatası: {str(e)}")
        finally:
            if self._connection and not self._connection.closed:
                self._connection.close()
                log_event("INFO", "database", "Veritabanı bağlantısı kapatıldı")

db = DatabaseConnection()
get_db_connection = db.get_connection 