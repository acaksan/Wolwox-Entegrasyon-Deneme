"""Wolvox ürün servisi.

Bu modül, Wolvox veritabanından ürün bilgilerini çekmek için gerekli fonksiyonları içerir.
"""

import fdb
from typing import List, Dict, Any, Optional
from core.config import get_settings
from core.logging import logger


class WolvoxProductService:
    """Wolvox ürün servisi sınıfı.
    
    Bu sınıf, Wolvox veritabanına bağlanmak ve ürün bilgilerini çekmek için gerekli metodları içerir.
    """

    def __init__(self) -> None:
        """Servis başlatıcı.
        
        Settings'ten veritabanı bağlantı bilgilerini alır.
        """
        self.settings = get_settings()
        self.connection: Optional[fdb.Connection] = None

    def get_db_connection(self) -> fdb.Connection:
        """Firebird veritabanına bağlanır ve bağlantıyı döndürür.
        
        Returns:
            fdb.Connection: Veritabanı bağlantı nesnesi
            
        Raises:
            Exception: Bağlantı hatası durumunda
        """
        try:
            conn = fdb.connect(
                host=self.settings.FIREBIRD_HOST,
                database=self.settings.FIREBIRD_DATABASE,
                user=self.settings.FIREBIRD_USER,
                password=self.settings.FIREBIRD_PASSWORD,
                port=self.settings.FIREBIRD_PORT,
                charset=self.settings.FIREBIRD_CHARSET
            )
            return conn
        except Exception as e:
            logger.error(f"❌ Veritabanına bağlanırken hata: {str(e)}")
            raise

    async def get_products(self) -> List[Dict[str, Any]]:
        """Firebird veritabanından ürün bilgilerini çeker.
        
        Returns:
            List[Dict[str, Any]]: Ürün bilgilerini içeren sözlük listesi
            
        Raises:
            Exception: Veritabanı sorgusu sırasında oluşan hatalar
        """
        try:
            with self.get_db_connection() as conn:
                with conn.cursor() as cur:
                    # Ürün bilgilerini alalım
                    query = """
                        SELECT 
                            s.BLKODU,
                            s.STOKKODU,
                            s.STOK_ADI,
                            s.BARKODU,
                            s.BIRIMI,
                            s.KDV_ORANI,
                            s.MARKASI,
                            s.MODELI,
                            s.GRUBU,
                            s.ALT_GRUBU,
                            s.WEBDE_GORUNSUN,
                            s.AKTIF,
                            s.BIRIM_AGIRLIK,
                            s.ETICARET_ACIKLAMA,
                            s.RESIM_YOLU,
                            s.ACIKLAMA1,
                            s.ACIKLAMA2,
                            s.ACIKLAMA3,
                            s.ACIKLAMA4,
                            COALESCE((
                                SELECT SUM(CASE WHEN sh.TUTAR_TURU = 0 THEN -sh.MIKTARI ELSE sh.MIKTARI END)
                                FROM STOKHR sh
                                WHERE sh.BLSTKODU = s.BLKODU
                                AND sh.SILINDI = 0
                            ), 0) as STOK_MIKTARI,
                            COALESCE((
                                SELECT sf.FIYATI
                                FROM STOK_FIYAT sf
                                WHERE sf.BLSTKODU = s.BLKODU
                                AND sf.ALIS_SATIS = 1 
                                AND sf.FIYAT_NO = 1
                            ), 0) as SATIS_FIYATI
                        FROM STOK s
                        WHERE s.WEBDE_GORUNSUN = 1
                        AND s.AKTIF = 1
                        ORDER BY s.STOK_ADI
                    """
                    cur.execute(query)
                    rows = cur.fetchall()

                    # Sonuçları listeye dönüştür
                    result = [{
                        'blkodu': row[0],
                        'stokkodu': row[1].strip() if row[1] else '',
                        'stok_adi': row[2].strip() if row[2] else '',
                        'barkodu': row[3].strip() if row[3] else '',
                        'birimi': row[4].strip() if row[4] else '',
                        'kdv_orani': float(row[5]) if row[5] else 0,
                        'markasi': row[6].strip() if row[6] else '',
                        'modeli': row[7].strip() if row[7] else '',
                        'grubu': row[8].strip() if row[8] else '',
                        'alt_grubu': row[9].strip() if row[9] else '',
                        'webde_gorunsun': bool(row[10]),
                        'aktif': bool(row[11]),
                        'birim_agirlik': float(row[12]) if row[12] else 0,
                        'eticaret_aciklama': row[13].strip() if row[13] else '',
                        'resim_yolu': row[14].strip() if row[14] else '',
                        'aciklama1': row[15].strip() if row[15] else '',
                        'aciklama2': row[16].strip() if row[16] else '',
                        'aciklama3': row[17].strip() if row[17] else '',
                        'aciklama4': row[18].strip() if row[18] else '',
                        'stok_miktari': float(row[19]) if row[19] else 0,
                        'satis_fiyati': float(row[20]) if row[20] else 0
                    } for row in rows]

                    logger.info(f"✅ {len(result)} adet ürün başarıyla getirildi!")
                    return result

        except Exception as e:
            logger.error(f"❌ Ürünler getirilirken hata: {str(e)}")
            raise 
