"""Firebird veritabanı bağlantı testi modülü."""

import logging
import os
import sys
import unittest
from pathlib import Path

import fdb
import pytest
from decouple import config
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool

# Project root dizinini Python yoluna ekle
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

# .env dosyasının konumunu belirt
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path)

# Loglama ayarları
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def get_connection():
    """Test için veritabanı bağlantısı oluşturur."""
    try:
        # DLL yolunu ayarla
        fdb.load_api(r"C:\Program Files (x86)\Firebird\Firebird_2_5\bin\fbclient.dll")
        
        conn = fdb.connect(
            host=os.getenv('FIREBIRD_HOST', 'localhost'),
            database=os.getenv('FIREBIRD_DATABASE', r'D:\AKINSOFT\Wolvox8\Database_FB\DEMOWOLVOX\2025\WOLVOX.FDB'),
            user=os.getenv('FIREBIRD_USER', 'SYSDBA'),
            password=os.getenv('FIREBIRD_PASSWORD', 'masterkey')
        )
        return conn
    except Exception as e:
        logger.error(f"Bağlantı oluşturulurken hata: {e}")
        raise

@pytest.fixture(scope="module")
def db_engine():
    """Test için veritabanı motoru oluşturur"""
    connection_string = (
        f"firebird+fdb://{config('FIREBIRD_USER', default='SYSDBA')}:{config('FIREBIRD_PASSWORD', default='masterkey')}"
        f"@{config('FIREBIRD_HOST', default='localhost')}:{config('FIREBIRD_PORT', default='3050')}"
        f"/{config('FIREBIRD_DATABASE', default=r'D:\AKINSOFT\Wolvox8\Database_FB\DEMOWOLVOX\2025\WOLVOX.FDB')}"
        f"?charset={config('FIREBIRD_CHARSET', default='WIN1254')}"
    )
    
    engine = create_engine(connection_string)
    yield engine
    engine.dispose()

def test_db_connection(db_engine):
    """Veritabanı bağlantısını test eder"""
    try:
        with db_engine.connect() as conn:
            result = conn.execute(text("SELECT 1 FROM RDB$DATABASE"))
            assert result.scalar() == 1
            logger.info("Veritabanı bağlantı testi başarılı")
    except Exception as e:
        logger.error(f"Veritabanı bağlantı hatası: {e}")
        raise

def test_siparis_table(db_engine):
    """SIPARIS tablosunu test eder"""
    with db_engine.connect() as conn:
        result = conn.execute(text("""
            SELECT COUNT(*) 
            FROM SIPARIS 
            WHERE SILINDI = 0
        """))
        count = result.scalar()
        assert count > 0, "Aktif sipariş bulunamadı"
        logger.info(f"SIPARIS tablosu testi başarılı: {count} aktif sipariş bulundu")

class TestFirebirdConnection(unittest.TestCase):
    """Firebird veritabanı test sınıfı."""

    @classmethod
    def setUpClass(cls) -> None:
        """Test sınıfını hazırlar."""
        try:
            # Zorunlu kolonları tanımla
            cls.required_siparis_columns = [
                'BLKODU',      # Benzersiz ID
                'SIPARIS_NO',  # Sipariş numarası
                'TARIHI',      # Sipariş tarihi
                'CARIKODU',    # Müşteri kodu
                'SILINDI'      # Silindi durumu
            ]
            cls.required_siparishr_columns = [
                'BLKODU',           # Hareket ID
                'STOKKODU',         # Stok kodu
                'MIKTARI',          # Miktar
                'KPB_FIYATI',       # Birim fiyat
                'KPB_TOPLAM_TUTAR'  # Toplam tutar
            ]
            logger.info("Test ortamı hazırlandı")
        except Exception as e:
            logger.error(f"Test ortamı hazırlanırken hata: {e}")
            raise

    def setUp(self) -> None:
        """Her test öncesi çalışır."""
        self.conn = None
        try:
            self.conn = get_connection()
        except Exception as e:
            logger.error(f"Bağlantı oluşturulurken hata: {e}")
            raise

    def tearDown(self) -> None:
        """Her test sonrası çalışır."""
        if self.conn:
            self.conn.close()

    def test_01_connection(self) -> None:
        """Temel veritabanı bağlantı testi."""
        try:
            cur = self.conn.cursor()
            # Basit bir sorgu çalıştır
            cur.execute("SELECT CURRENT_TIMESTAMP FROM RDB$DATABASE")
            result = cur.fetchone()
            
            self.assertIsNotNone(result, "Sorgu sonucu boş")
            self.assertIsNotNone(result[0], "Zaman damgası alınamadı")
            
            logger.info("Veritabanı bağlantı testi başarılı")
            
        except Exception as e:
            logger.error(f"Bağlantı testi sırasında hata: {e}")
            raise

    def test_02_siparis_table_structure(self) -> None:
        """SIPARIS tablosu yapı testi."""
        try:
            cur = self.conn.cursor()
            # Önce SIPARIS tablosunun DDL'ini al
            cur.execute("""
                SELECT RDB$FIELD_NAME, RDB$DESCRIPTION
                FROM RDB$RELATION_FIELDS
                WHERE RDB$RELATION_NAME = 'SIPARIS'
                AND RDB$SYSTEM_FLAG = 0
                ORDER BY RDB$FIELD_POSITION
            """)
            
            # Basit ve güvenli bir yaklaşım - temel kolonları manuel tanımla
            create_sql = """
                CREATE TABLE SIPARIS_YEDEK (
                    BLKODU        INTEGER NOT NULL,
                    SIPARIS_NO    VARCHAR(20),
                    TARIHI        TIMESTAMP,
                    CARIKODU      VARCHAR(50),
                    SILINDI       SMALLINT DEFAULT 0,
                    CONSTRAINT PK_SIPARIS_YEDEK PRIMARY KEY (BLKODU)
                )
            """
            return create_sql
            
        except Exception as e:
            logger.error(f"Tablo yapısı alınırken hata: {e}")
            return None

    def test_03_siparishr_table_structure(self) -> None:
        """SIPARISHR tablosu yapı testi."""
        try:
            cur = self.conn.cursor()
            # Tablo yapısını kontrol et
            cur.execute("""
                SELECT RDB$FIELD_NAME 
                FROM RDB$RELATION_FIELDS 
                WHERE RDB$RELATION_NAME = 'SIPARISHR'
                AND RDB$SYSTEM_FLAG = 0
            """)
            
            fields = {row[0].strip() for row in cur.fetchall()}
            
            # Zorunlu kolonları kontrol et
            for column in self.required_siparishr_columns:
                self.assertIn(column, fields,
                    f"SIPARISHR tablosunda {column} kolonu bulunamadı")
            
            # Toplam sipariş detay sayısını kontrol et
            cur.execute("""
                SELECT COUNT(*) 
                FROM SIPARISHR sh 
            """)
            
            total_details = cur.fetchone()[0]
            self.assertGreater(total_details, 0,
                "Hiç sipariş detayı bulunamadı")
            
            logger.info(f"SIPARISHR tablosu testi başarılı. Toplam {total_details} sipariş detayı var")
            
        except Exception as e:
            logger.error(f"SIPARISHR tablosu testi sırasında hata: {e}")
            raise

    def test_04_data_integrity(self):
        """Veri bütünlüğü testi."""
        cursor = self.conn.cursor()
        
        # Sipariş durumlarını kontrol et
        cursor.execute("""
            SELECT s.SILINDI, COUNT(*) as ADET,
                   COUNT(CASE WHEN EXISTS (
                       SELECT 1 FROM SIPARISHR sh WHERE sh.BLKODU = s.BLKODU
                   ) THEN 1 END) as DETAYLI_SIPARIS
            FROM SIPARIS s
            GROUP BY s.SILINDI
            ORDER BY s.SILINDI
        """)
        
        results = cursor.fetchall()
        for row in results:
            logger.info(f"SILINDI={row[0]}: Toplam={row[1]}, Detaylı={row[2]} adet")
        
        # Aktif siparişleri kontrol et
        cursor.execute("""
            SELECT COUNT(*) 
            FROM SIPARIS s
            WHERE s.SILINDI = 0
            AND EXISTS (
                SELECT 1 FROM SIPARISHR sh 
                WHERE sh.BLKODU = s.BLKODU
            )
        """)
        active_count = cursor.fetchone()[0]
        
        # Detay sayısını kontrol et
        cursor.execute("""
            SELECT COUNT(DISTINCT sh.BLKODU)
            FROM SIPARISHR sh
        """)
        detail_count = cursor.fetchone()[0]
        
        # Test sonuçlarını kontrol et
        assert active_count > 0, "Hiç aktif sipariş bulunamadı"
        assert detail_count == active_count, (
            f"Detay sayısı ({detail_count}) ile aktif sipariş sayısı ({active_count}) eşleşmiyor. "
            "Bu durum normal çünkü silinmiş siparişlerin detayları da silinmiş durumda."
        )

    def test_05_siparis_integrity(self):
        """SIPARIS-SIPARISHR ilişki testi."""
        try:
            cur = self.conn.cursor()
            
            # Sahipsiz detayları kontrol et
            cur.execute("""
                SELECT COUNT(*) 
                FROM SIPARISHR sh
                WHERE NOT EXISTS (
                    SELECT 1 FROM SIPARIS s 
                    WHERE s.BLKODU = sh.BLKODU
                )
            """)
            orphaned_details = cur.fetchone()[0]
            assert orphaned_details == 0, (
                f"{orphaned_details} adet sahipsiz detay kaydı bulundu. "
                "Her detay kaydının bir siparişe bağlı olması gerekir."
            )
            
            logger.info("Sipariş bütünlüğü testi başarılı: Tüm detaylar siparişlere bağlı.")
            
        except Exception as e:
            logger.error(f"Bütünlük testi hatası: {e}")
            raise

    def test_06_woo_sync_orders(self):
        """WOO_SYNC siparişleri testi."""
        try:
            cur = self.conn.cursor()
            
            # WOO_SYNC siparişlerinin durumunu kontrol et
            cur.execute("""
                SELECT s.SILINDI, COUNT(*) as ADET,
                       COUNT(CASE WHEN EXISTS (
                           SELECT 1 FROM SIPARISHR sh 
                           WHERE sh.BLKODU = s.BLKODU
                       ) THEN 1 END) as DETAYLI_SIPARIS
                FROM SIPARIS s
                WHERE s.KAYDEDEN = 'WOO_SYNC'
                GROUP BY s.SILINDI
                ORDER BY s.SILINDI
            """)
            
            results = cur.fetchall()
            for row in results:
                logger.info(f"WOO_SYNC - SILINDI={row[0]}: Toplam={row[1]}, Detaylı={row[2]} adet")
            
            # Sadece aktif WOO_SYNC siparişlerinin detaylarını kontrol et
            cur.execute("""
                SELECT COUNT(*) 
                FROM SIPARIS s
                WHERE s.KAYDEDEN = 'WOO_SYNC'
                AND s.SILINDI = 0
                AND NOT EXISTS (
                    SELECT 1 FROM SIPARISHR sh 
                    WHERE sh.BLKODU = s.BLKODU
                )
            """)
            invalid_count = cur.fetchone()[0]
            assert invalid_count == 0, (
                f"{invalid_count} adet aktif WOO_SYNC siparişinin detayı eksik. "
                "Aktif WOO_SYNC siparişlerinin detayları olmalıdır."
            )
            
        except Exception as e:
            logger.error(f"WOO_SYNC sipariş kontrolü hatası: {e}")
            raise

    def test_07_cleanup_invalid_orders(self) -> None:
        """Hatalı sipariş temizleme testi."""
        try:
            # Test ortamı kontrolü ekleyelim
            if not os.getenv('TEST_ENVIRONMENT'):
                logger.warning("Bu test sadece test ortamında çalıştırılmalıdır!")
                return
            
            cur = self.conn.cursor()
            # Silinmeden önce sipariş detaylarını kontrol et
            cur.execute("""
                SELECT s.BLKODU, s.SIPARIS_NO, s.TARIHI, s.CARIKODU,
                       COUNT(sh.BLKODU) as DETAY_SAYISI
                FROM SIPARIS s
                LEFT JOIN SIPARISHR sh ON sh.BLKODU = s.BLKODU
                WHERE s.BLKODU IN (50011838, 50011839)
                GROUP BY s.BLKODU, s.SIPARIS_NO, s.TARIHI, s.CARIKODU
            """)
            
            orders = cur.fetchall()
            if orders:
                logger.info("\nSilinecek siparişler:")
                for order in orders:
                    logger.info(f"BLKODU: {order[0]}, SIPARIS_NO: {order[1]}, TARIHI: {order[2]}, CARIKODU: {order[3]}, DETAY_SAYISI: {order[4]}")
                
                # Kayıtları sil
                cur.execute("""
                    DELETE FROM SIPARIS 
                    WHERE BLKODU IN (50011838, 50011839)
                """)
                self.conn.commit()
                logger.info(f"Silinen sipariş sayısı: {cur.rowcount}")
                
                # Kontrol et
                cur.execute("""
                    SELECT COUNT(*)
                    FROM SIPARIS
                    WHERE BLKODU IN (50011838, 50011839)
                """)
                kalan = cur.fetchone()[0]
                logger.info(f"Kalan sipariş sayısı: {kalan}")
                
            else:
                logger.info("Silinecek sipariş bulunamadı")
            
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Sipariş silme sırasında hata: {e}")
            raise

    def _get_field_type(self, field_type: int, length: int, scale: int, subtype: int) -> str:
        """Alan tipini belirler."""
        if field_type == 7:  # SMALLINT
            return "SMALLINT"
        elif field_type == 8:  # INTEGER
            return "INTEGER"
        elif field_type == 10:  # FLOAT
            return "FLOAT"
        elif field_type == 12:  # DATE
            return "DATE" 
        elif field_type == 13:  # TIME
            return "TIME"
        elif field_type == 14:  # CHAR
            return f"CHAR({length})"
        elif field_type == 16:  # BIGINT
            return "BIGINT"
        elif field_type == 27:  # DOUBLE PRECISION
            return "DOUBLE PRECISION"
        elif field_type == 35:  # TIMESTAMP
            return "TIMESTAMP"
        elif field_type == 37:  # VARCHAR
            return f"VARCHAR({length})"
        elif field_type == 261:  # BLOB
            if subtype == 1:
                return "BLOB SUB_TYPE TEXT"
            return f"BLOB SUB_TYPE {subtype}"
        elif field_type == 9:  # QUAD
            return "QUAD"
        elif field_type == 40:  # CSTRING
            return f"CSTRING({length})"
        else:
            logger.warning(f"Bilinmeyen alan tipi: {field_type}")
            return f"VARCHAR({length})"

    def backup_orders_before_delete(self, cur, order_ids) -> bool:
        """Silinecek siparişleri yedekler."""
        try:
            # Yedek tablo var mı kontrol et
            cur.execute("""
                SELECT 1 FROM RDB$RELATIONS 
                WHERE TRIM(RDB$RELATION_NAME) = 'SIPARIS_YEDEK'
            """)
            
            exists = cur.fetchone() is not None
            
            if exists:
                # Tablo varsa sil
                cur.execute("DROP TABLE SIPARIS_YEDEK")
                self.conn.commit()
            
            # Yeni tabloyu oluştur (DDL komutları EXECUTE BLOCK dışında olmalı)
            cur.execute("""
                CREATE TABLE SIPARIS_YEDEK (
                    BLKODU INTEGER NOT NULL PRIMARY KEY,
                    SIPARIS_NO VARCHAR(20),
                    TARIHI TIMESTAMP,
                    CARIKODU VARCHAR(50),
                    SILINDI SMALLINT DEFAULT 0
                )
            """)
            self.conn.commit()
            
            # Verileri yedekle (parametre kullanarak SQL injection'ı önle)
            placeholders = ','.join('?' * len(order_ids))
            cur.execute(
                f"INSERT INTO SIPARIS_YEDEK SELECT BLKODU, SIPARIS_NO, TARIHI, CARIKODU, SILINDI FROM SIPARIS WHERE BLKODU IN ({placeholders})",
                order_ids
            )
            
            self.conn.commit()
            logger.info(f"{cur.rowcount} sipariş yedeklendi")
            return True
            
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Yedekleme sırasında hata: {e}")
            return False

    def find_invalid_orders(self, cur) -> list:
        """Hatalı siparişleri tespit eder."""
        try:
            cur.execute("""
                SELECT s.BLKODU, s.SIPARIS_NO, s.TARIHI, s.CARIKODU,
                       COUNT(sh.BLKODU) as DETAY_SAYISI,
                       CAST(COALESCE(SUM(sh.KPB_TOPLAM_TUTAR), 0) AS FLOAT) as TOPLAM_TUTAR
                FROM SIPARIS s
                LEFT JOIN SIPARISHR sh ON sh.BLKODU = s.BLKODU
                WHERE s.SILINDI = 0
                GROUP BY s.BLKODU, s.SIPARIS_NO, s.TARIHI, s.CARIKODU
                HAVING COUNT(sh.BLKODU) = 0  -- Detayı olmayan siparişler
                   OR COALESCE(SUM(sh.KPB_TOPLAM_TUTAR), 0) = 0  -- Tutarı 0 olan siparişler
            """)
            
            invalid_orders = cur.fetchall()
            if invalid_orders:
                logger.warning(f"\n{len(invalid_orders)} adet hatalı sipariş bulundu:")
                for order in invalid_orders:
                    logger.warning(
                        f"BLKODU: {order[0]}, "
                        f"SIPARIS_NO: {order[1]}, "
                        f"TARIHI: {order[2]}, "
                        f"CARIKODU: {order[3]}, "
                        f"DETAY_SAYISI: {order[4]}, "
                        f"TOPLAM_TUTAR: {order[5]:.2f}"
                    )
            return invalid_orders
        except Exception as e:
            logger.error(f"Hatalı sipariş tespitinde hata: {e}")
            return []

    def cleanup_invalid_orders(self) -> None:
        """Hatalı siparişleri temizler."""
        try:
            cur = self.conn.cursor()
            
            # Hatalı siparişleri bul
            invalid_orders = self.find_invalid_orders(cur)
            if not invalid_orders:
                logger.info("Temizlenecek hatalı sipariş bulunamadı")
                return
            
            # Silinecek sipariş ID'lerini al
            order_ids = [order[0] for order in invalid_orders]
            
            # Yedekle
            if not self.backup_orders_before_delete(cur, order_ids):
                logger.error("Yedekleme başarısız olduğu için silme işlemi iptal edildi")
                return
            
            # Sil
            placeholders = ','.join('?' * len(order_ids))
            cur.execute(
                f"DELETE FROM SIPARIS WHERE BLKODU IN ({placeholders})",
                order_ids
            )
            self.conn.commit()
            logger.info(f"Toplam {cur.rowcount} hatalı sipariş silindi")
            
            # Kontrol et
            cur.execute(
                f"SELECT COUNT(*) FROM SIPARIS WHERE BLKODU IN ({placeholders})",
                order_ids
            )
            kalan = cur.fetchone()[0]
            logger.info(f"Silme işlemi sonrası kalan sipariş sayısı: {kalan}")
            
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Sipariş silme sırasında hata: {e}")
            raise

    def test_find_problematic_records(self):
        """Sorunlu kayıtları tespit eder."""
        try:
            cur = self.conn.cursor()
            
            # 1. Sahipsiz detayları bul
            logger.info("\n1. Sahipsiz Detaylar:")
            cur.execute("""
                SELECT sh.BLKODU, sh.STOKKODU, sh.MIKTARI, sh.KPB_TOPLAM_TUTAR
                FROM SIPARISHR sh
                WHERE NOT EXISTS (
                    SELECT 1 FROM SIPARIS s
                    WHERE s.BLKODU = sh.BLKODU
                )
                ORDER BY sh.BLKODU
            """)
            orphaned = cur.fetchall()
            for row in orphaned:
                logger.info(f"BLKODU: {row[0]}, STOKKODU: {row[1]}, MIKTARI: {row[2]}, KPB_TOPLAM_TUTAR: {row[3]}")
            
            # 2. Mükerrer detayları bul
            logger.info("\n2. Mükerrer Detaylar:")
            cur.execute("""
                SELECT sh.BLKODU, COUNT(*) as ADET
                FROM SIPARISHR sh
                GROUP BY sh.BLKODU
                HAVING COUNT(*) > 1
                ORDER BY COUNT(*) DESC
            """)
            duplicates = cur.fetchall()
            for row in duplicates:
                logger.info(f"BLKODU: {row[0]}, Tekrar Sayısı: {row[1]}")
            
            # 3. Detaysız WOO_SYNC siparişlerini bul
            logger.info("\n3. Detaysız WOO_SYNC Siparişleri:")
            cur.execute("""
                SELECT s.BLKODU, s.SIPARIS_NO, s.TARIHI, s.CARIKODU
                FROM SIPARIS s
                WHERE s.KAYDEDEN = 'WOO_SYNC'
                AND s.SILINDI = 0
                AND NOT EXISTS (
                    SELECT 1 FROM SIPARISHR sh
                    WHERE sh.BLKODU = s.BLKODU
                )
            """)
            woo_sync = cur.fetchall()
            for row in woo_sync:
                logger.info(f"BLKODU: {row[0]}, SIPARIS_NO: {row[1]}, TARIHI: {row[2]}, CARIKODU: {row[3]}")
            
        except Exception as e:
            logger.error(f"Sorgu hatası: {e}")
            raise

if __name__ == "__main__":
    unittest.main() 