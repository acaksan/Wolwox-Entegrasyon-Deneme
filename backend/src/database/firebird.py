import logging
from typing import Optional

import fdb
from src.core.settings import get_settings

settings = get_settings()

class FirebirdDB:
    """Firebird veritabanı bağlantı sınıfı"""
    
    def __init__(self):
        """Veritabanı bağlantısını başlat"""
        self.connection: Optional[fdb.Connection] = None
        self.cursor: Optional[fdb.Cursor] = None
        
    def __enter__(self):
        """Context manager başlangıcı"""
        try:
            logging.debug(f"Veritabanı bağlantısı başlatılıyor: {settings.DB_PATH}")
            connection_string = (
                f"{settings.DB_HOST}:{settings.DB_PATH}"
                if settings.DB_HOST != "localhost"
                else settings.DB_PATH
            )
            self.connection = fdb.connect(
                dsn=connection_string,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                charset=settings.DB_CHARSET
            )
            self.cursor = self.connection.cursor()
            logging.info("Veritabanı bağlantısı başarılı")
            return self
            
        except Exception as e:
            logging.error(f"Veritabanı bağlantı hatası: {str(e)}")
            raise
            
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager bitişi"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            logging.debug("Veritabanı bağlantısı kapatıldı")
            
        except Exception as e:
            logging.error(f"Veritabanı bağlantısı kapatılırken hata: {str(e)}")
            raise
            
    def execute(self, sql: str, params: tuple = None) -> None:
        """SQL sorgusu çalıştır"""
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
                
        except Exception as e:
            logging.error(f"SQL sorgusu çalıştırılırken hata: {str(e)}")
            raise
            
    def fetchone(self):
        """Tek satır getir"""
        return self.cursor.fetchone()
        
    def fetchall(self):
        """Tüm satırları getir"""
        return self.cursor.fetchall()
        
    def commit(self):
        """Değişiklikleri kaydet"""
        self.connection.commit()
        
    def rollback(self):
        """Değişiklikleri geri al"""
        self.connection.rollback()
