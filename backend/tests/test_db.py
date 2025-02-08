import os

import fdb


def test_db_connection():
    try:
        # Veritabanı bağlantı parametreleri
        connection = fdb.connect(
            host="localhost",
            port=3050,
            database=r"D:\AKINSOFT\Wolvox8\Database_FB\DEMOWOLVOX\2025\WOLVOX.FDB",
            user="SYSDBA",
            password="masterkey",
            charset="WIN1254"
        )
        
        # Test sorgusu
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM CARI_HESAPLAR")
        count = cursor.fetchone()[0]
        print(f"Toplam müşteri sayısı: {count}")
        
        # Bağlantıyı kapat
        cursor.close()
        connection.close()
        print("Veritabanı bağlantısı başarılı!")
        return True
        
    except Exception as e:
        print(f"Hata: {str(e)}")
        return False

if __name__ == "__main__":
    test_db_connection()
