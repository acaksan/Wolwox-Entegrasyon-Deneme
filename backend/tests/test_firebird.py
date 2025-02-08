import logging
import os
import sys

from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Log ayarları
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Proje kök dizinini Python path'ine ekle
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.database.firebird import FirebirdDB


def test_firebird_connection():
    """Firebird veritabanı bağlantısını test et"""
    try:
        with FirebirdDB() as db:
            # Test sorgusu
            db.execute("SELECT COUNT(*) FROM CARI")
            count = db.fetchone()[0]
            print(f"Toplam müşteri sayısı: {count}")
            
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
                
        print("\nVeritabanı bağlantısı başarılı!")
        return True
        
    except Exception as e:
        print(f"Hata: {str(e)}")
        return False

if __name__ == "__main__":
    test_firebird_connection()
