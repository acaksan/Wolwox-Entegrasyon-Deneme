"""Firebird 2.5 veritabanı bağlantısı"""

from typing import Any, Dict, List, Optional

import fdb
from src.core.exceptions import DatabaseException
from src.core.logging import logger
from src.core.settings import get_settings

settings = get_settings()

class WolvoxDB:
    def __init__(self):
        """Wolvox veritabanı bağlantı sınıfı başlatıcısı"""
        self.connection_params = {
            "dsn": settings.FIREBIRD_DSN,
            "user": settings.FIREBIRD_USER,
            "password": settings.FIREBIRD_PASSWORD,
            "charset": "UTF8"
        }
        self.logger = logger
        self._connection = None

    async def _get_connection(self) -> fdb.Connection:
        """
        Veritabanı bağlantısını getir veya oluştur
        
        Returns:
            fdb.Connection: Veritabanı bağlantısı
            
        Raises:
            DatabaseException: Bağlantı hatası durumunda
        """
        try:
            if not self._connection or self._connection.closed:
                self._connection = fdb.connect(**self.connection_params)
            return self._connection
        except Exception as e:
            self.logger.error(f"Veritabanı bağlantı hatası: {str(e)}")
            raise DatabaseException(f"Veritabanı bağlantı hatası: {str(e)}")

    async def fetch_one(self, query: str, params: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """
        Tek kayıt getir
        
        Args:
            query: SQL sorgusu
            params: Sorgu parametreleri
            
        Returns:
            Dict: Kayıt veya None
            
        Raises:
            DatabaseException: Sorgu hatası durumunda
        """
        try:
            conn = await self._get_connection()
            cur = conn.cursor()
            
            try:
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)
                    
                columns = [column[0].lower() for column in cur.description]
                row = cur.fetchone()
                
                if not row:
                    return None
                    
                return dict(zip(columns, row))
                
            finally:
                cur.close()
                
        except Exception as e:
            self.logger.error(f"Sorgu hatası: {str(e)}")
            raise DatabaseException(f"Sorgu hatası: {str(e)}")

    async def fetch_all(self, query: str, params: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Tüm kayıtları getir
        
        Args:
            query: SQL sorgusu
            params: Sorgu parametreleri
            
        Returns:
            List[Dict]: Kayıt listesi
            
        Raises:
            DatabaseException: Sorgu hatası durumunda
        """
        try:
            conn = await self._get_connection()
            cur = conn.cursor()
            
            try:
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)
                    
                columns = [column[0].lower() for column in cur.description]
                rows = cur.fetchall()
                
                return [dict(zip(columns, row)) for row in rows]
                
            finally:
                cur.close()
                
        except Exception as e:
            self.logger.error(f"Sorgu hatası: {str(e)}")
            raise DatabaseException(f"Sorgu hatası: {str(e)}")

    async def execute(self, query: str, params: Optional[Dict] = None) -> None:
        """
        SQL sorgusu çalıştır
        
        Args:
            query: SQL sorgusu
            params: Sorgu parametreleri
            
        Raises:
            DatabaseException: Sorgu hatası durumunda
        """
        try:
            conn = await self._get_connection()
            cur = conn.cursor()
            
            try:
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)
                    
                conn.commit()
                
            finally:
                cur.close()
                
        except Exception as e:
            self.logger.error(f"Sorgu hatası: {str(e)}")
            raise DatabaseException(f"Sorgu hatası: {str(e)}")

    def __del__(self):
        """Yıkıcı metod - bağlantıyı kapat"""
        if self._connection and not self._connection.closed:
            self._connection.close()
