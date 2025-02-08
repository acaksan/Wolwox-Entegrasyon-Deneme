import logging
from typing import List

from src.models.wolvox.product import WlxProduct
from src.services.firebird_service import FirebirdService

logger = logging.getLogger(__name__)

class WolvoxProductRepository:
    """Wolvox ürün repository sınıfı"""
    
    def __init__(self):
        self.fb_service = FirebirdService()
    
    async def get_products(self) -> List[WlxProduct]:
        """Wolvox'tan ürünleri çeker"""
        try:
            cursor = self.fb_service.connection.cursor()
            
            query = """
                SELECT FIRST 100
                    s.BLKODU,
                    s.STOKKODU,
                    s.STOK_ADI,
                    s.BARKODU,
                    s.BIRIMI,
                    s.KDV_ORANI,
                    s.MARKASI,
                    s.MODELI,
                    s.GRUBU,
                    s.WEBDE_GORUNSUN,
                    s.AKTIF,
                    s.ETICARET_ACIKLAMA,
                    s.RESIM_YOLU,
                    (
                        SELECT COALESCE(SUM(
                            CASE 
                                WHEN sh.TUTAR_TURU = 0 THEN sh.MIKTARI 
                                ELSE -sh.MIKTARI 
                            END), 0)
                        FROM STOKHR sh 
                        WHERE sh.BLSTKODU = s.BLKODU
                        AND sh.SILINDI = 0
                    ) as KALAN_MIKTAR,
                    (
                        SELECT FIRST 1 sf.FIYATI 
                        FROM STOK_FIYAT sf 
                        WHERE sf.BLSTKODU = s.BLKODU 
                        AND sf.FIYAT_NO = 1
                        AND sf.TANIMI = 'SATIŞ FİYATI -1'
                    ) as SATIS_FIYATI
                FROM STOK s
                WHERE s.AKTIF = 1 
                AND s.WEBDE_GORUNSUN = 1
                ORDER BY s.STOK_ADI
            """
            
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            products = []
            
            for row in cursor.fetchall():
                product_dict = dict(zip(columns, row))
                products.append(WlxProduct.parse_obj(product_dict))
            
            cursor.close()
            logger.info(f"{len(products)} adet ürün başarıyla çekildi")
            return products
            
        except Exception as e:
            logger.error(f"Ürün listesi çekilirken hata: {str(e)}")
            raise 