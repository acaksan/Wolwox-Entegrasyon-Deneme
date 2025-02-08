"""Firebird veritabanı bağlantı testi."""

import logging
import os
from pathlib import Path

import fdb

# Loglama ayarları
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def test_connection():
    """Temel veritabanı bağlantı testi."""
    try:
        # DLL yolunu ayarla
        fdb.load_api(r"C:\Program Files (x86)\Firebird\Firebird_2_5\bin\fbclient.dll")
        
        # Bağlantıyı dene
        conn = fdb.connect(
            dsn=r'D:\AKINSOFT\Wolvox8\Database_FB\DEMOWOLVOX\2025\WOLVOX.FDB',
            user='SYSDBA',
            password='masterkey'
        )
        logger.info("Bağlantı başarılı!")
        
        # Test sorgusu çalıştır
        cur = conn.cursor()
        cur.execute("SELECT CURRENT_TIMESTAMP FROM RDB$DATABASE")
        result = cur.fetchone()
        logger.info(f"Zaman damgası: {result[0]}")
        
        # Tablo listesini al
        cur.execute("""
            SELECT RDB$RELATION_NAME 
            FROM RDB$RELATIONS 
            WHERE RDB$SYSTEM_FLAG = 0
            ORDER BY RDB$RELATION_NAME
        """)
        tables = [row[0].strip() for row in cur.fetchall()]
        logger.info(f"Tablolar: {', '.join(tables)}")
        
        cur.close()
        conn.close()
        logger.info("Bağlantı kapatıldı")
        
    except Exception as e:
        logger.error(f"Hata: {str(e)}")
        raise

if __name__ == "__main__":
    test_connection() 