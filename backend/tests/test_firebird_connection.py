import logging
import os

from dotenv import load_dotenv
from src.database.firebird import FirebirdDB

# Log ayarları
logging.basicConfig(level=logging.DEBUG)

# .env dosyasını yükle
load_dotenv()

def test_firebird_connection():
    """Firebird veritabanı bağlantısını test et"""
    try:
        with FirebirdDB() as db:
            # Test sorgusu
            db.execute("SELECT COUNT(*) FROM CARI")
            count = db.fetchone()[0]
            print(f"\nToplam müşteri sayısı: {count}")
            
            # Tablo yapısını kontrol et
            db.execute("""
                SELECT RDB$FIELD_NAME, RDB$FIELD_SOURCE
                FROM RDB$RELATION_FIELDS
                WHERE RDB$RELATION_NAME = 'CARI'
                ORDER BY RDB$FIELD_POSITION
            """)
            
            print("\nCARI tablosu yapısı:")
            for field in db.fetchall():
                field_name = field[0].strip()
                field_type = field[1].strip() if field[1] else 'NULL'
                print(f"- {field_name}: {field_type}")
                
            print("\nBağlantı başarılı!")
            return True
            
    except Exception as e:
        print(f"\nHata: {str(e)}")
        return False

if __name__ == "__main__":
    test_firebird_connection()
