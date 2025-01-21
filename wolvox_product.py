import os
import fdb
from config import *
import logging
from datetime import datetime

# Logs klasörünü oluştur
if not os.path.exists('logs'):
    os.makedirs('logs')

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/wolvox_product_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('WolvoxProduct')

class WolvoxProductReader:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.setup_connection()
    
    def setup_connection(self):
        """Veritabanı bağlantısını kur"""
        try:
            # Veritabanı bağlantısı
            self.connection = fdb.connect(
                host=FB_HOST,
                database=FB_DATABASE,
                user=FB_USER,
                password=FB_PASSWORD,
                charset=FB_CHARSET,
                port=FB_PORT
            )
            self.cursor = self.connection.cursor()
            logger.info("Veritabanı bağlantısı kuruldu")
            
        except Exception as e:
            logger.error(f"Veritabanı bağlantısı kurulamadı: {str(e)}")
            raise
    
    def get_all_products(self):
        """Tüm aktif ürünleri getir"""
        try:
            # Ürünleri sorgula
            self.cursor.execute("""
                SELECT 
                    s.STOKKODU,
                    s.STOK_ADI,
                    s.BARKODU,
                    s.BIRIMI,
                    s.KDV_ORANI,
                    s.GRUBU,
                    s.ARA_GRUBU,
                    s.ALT_GRUBU,
                    s.WEBDE_GORUNSUN,
                    s.AKTIF,
                    s.RESIM_YOLU,
                    s.ACIKLAMA1,
                    s.ACIKLAMA2,
                    s.ACIKLAMA3,
                    s.ETICARET_ACIKLAMA,
                    s.SATIS_FIYATI1,
                    s.SATIS_FIYATI2,
                    s.SATIS_FIYATI3,
                    s.SATIS_FIYATI4,
                    s.SATIS_FIYATI5,
                    s.MARKA,
                    s.MODEL,
                    s.MENSEI,
                    s.BIRIM2,
                    s.BIRIM3,
                    s.CARPAN2,
                    s.CARPAN3,
                    s.BLKODU
                FROM STOK s
                WHERE s.WEBDE_GORUNSUN = 1 
                AND s.AKTIF = 1
                ORDER BY s.STOKKODU
            """)
            
            products = []
            for row in self.cursor.fetchall():
                # Stok miktarını al
                stock_quantity = self.get_product_stock(row[0])
                
                # Resimleri al
                images = self.get_product_images(row[0])
                
                product = {
                    'stok_kodu': row[0].strip() if row[0] else '',
                    'stok_adi': row[1].strip() if row[1] else '',
                    'barkod': row[2].strip() if row[2] else '',
                    'birim': row[3].strip() if row[3] else '',
                    'kdv_orani': float(row[4]) if row[4] else 0,
                    'ana_grup': row[5].strip() if row[5] else '',
                    'ara_grup': row[6].strip() if row[6] else '',
                    'alt_grup': row[7].strip() if row[7] else '',
                    'webde_gorunsun': bool(row[8]),
                    'aktif': bool(row[9]),
                    'resim': row[10].strip() if row[10] else '',
                    'aciklama1': row[11].strip() if row[11] else '',
                    'aciklama2': row[12].strip() if row[12] else '',
                    'aciklama3': row[13].strip() if row[13] else '',
                    'eticaret_aciklama': row[14].strip() if row[14] else '',
                    'satis_fiyati': float(row[15]) if row[15] else 0,  # Ana satış fiyatı
                    'satis_fiyati2': float(row[16]) if row[16] else 0,
                    'satis_fiyati3': float(row[17]) if row[17] else 0,
                    'satis_fiyati4': float(row[18]) if row[18] else 0,
                    'satis_fiyati5': float(row[19]) if row[19] else 0,
                    'marka': row[20].strip() if row[20] else '',
                    'model': row[21].strip() if row[21] else '',
                    'mensei': row[22].strip() if row[22] else '',
                    'birim2': row[23].strip() if row[23] else '',
                    'birim3': row[24].strip() if row[24] else '',
                    'carpan2': float(row[25]) if row[25] else 0,
                    'carpan3': float(row[26]) if row[26] else 0,
                    'blkodu': row[27] if row[27] else None,
                    'stok_miktari': stock_quantity,
                    'resimler': images
                }
                
                # Açıklamaları birleştir
                product['aciklama'] = ''
                if product['aciklama1']:
                    product['aciklama'] += product['aciklama1'] + '\n'
                if product['aciklama2']:
                    product['aciklama'] += product['aciklama2'] + '\n'
                if product['aciklama3']:
                    product['aciklama'] += product['aciklama3'] + '\n'
                if product['eticaret_aciklama']:
                    product['aciklama'] += product['eticaret_aciklama']
                product['aciklama'] = product['aciklama'].strip()
                
                products.append(product)
            
            logger.info(f"{len(products)} adet ürün bulundu")
            return products
            
        except Exception as e:
            logger.error(f"Ürünler alınırken hata oluştu: {str(e)}")
            raise
        finally:
            if self.cursor:
                self.cursor.close()
    
    def get_product_stock(self, stok_kodu):
        """Ürün stok miktarını getir"""
        try:
            # Stok miktarını sorgula
            self.cursor.execute("""
                SELECT 
                    COALESCE(SUM(sh.MIKTARI), 0) as STOK_MIKTARI
                FROM STOKHR sh
                JOIN STOK s ON sh.BLSTKODU = s.BLKODU
                WHERE s.STOKKODU = ?
            """, (stok_kodu,))
            
            row = self.cursor.fetchone()
            stock_quantity = float(row[0]) if row else 0
            
            logger.info(f"Stok miktarı alındı: {stok_kodu} - {stock_quantity}")
            return stock_quantity
            
        except Exception as e:
            logger.error(f"Stok miktarı alınırken hata oluştu: {str(e)}")
            raise
    
    def get_product_images(self, stok_kodu):
        """Ürün resimlerini getir"""
        try:
            # Resimleri sorgula
            self.cursor.execute("""
                SELECT 
                    RESIM_YOLU
                FROM STOK
                WHERE STOKKODU = ?
            """, (stok_kodu,))
            
            row = self.cursor.fetchone()
            if not row or not row[0]:
                return []
            
            images = []
            image_path = row[0].strip()
            if image_path:
                images.append(image_path)
            
            logger.info(f"Resimler alındı: {stok_kodu} - {len(images)} adet")
            return images
            
        except Exception as e:
            logger.error(f"Resimler alınırken hata oluştu: {str(e)}")
            raise
    
    def get_categories(self):
        """Wolvox'tan kategorileri getir"""
        try:
            # Ana grupları getir
            main_groups = self.cursor.execute("""
                SELECT 
                    GRUPKODU,
                    GRUPADI,
                    WEBDE_GOSTERILECEK
                FROM STOK_ANA_GRUPLARI 
                WHERE WEBDE_GOSTERILECEK = 1
                ORDER BY GRUPADI
            """).fetchall()

            categories = []
            for main_group in main_groups:
                main_category = {
                    'id': main_group[0],
                    'name': main_group[1],
                    'type': 'main',
                    'subcategories': []
                }

                # Alt grupları getir
                sub_groups = self.cursor.execute("""
                    SELECT 
                        ALTGRUPKODU,
                        ALTGRUPADI,
                        WEBDE_GOSTERILECEK
                    FROM STOK_ALT_GRUPLARI 
                    WHERE ANA_GRUP = ? AND WEBDE_GOSTERILECEK = 1
                    ORDER BY ALTGRUPADI
                """, (main_group[0],)).fetchall()

                for sub_group in sub_groups:
                    sub_category = {
                        'id': sub_group[0],
                        'name': sub_group[1],
                        'type': 'sub',
                        'parent': main_group[1],
                        'subcategories': []
                    }

                    # Özel grupları getir
                    special_groups = self.cursor.execute("""
                        SELECT 
                            OZELGRUPKODU,
                            OZELGRUPADI,
                            WEBDE_GOSTERILECEK
                        FROM STOK_OZEL_GRUPLARI 
                        WHERE ANA_GRUP = ? AND ALT_GRUP = ? AND WEBDE_GOSTERILECEK = 1
                        ORDER BY OZELGRUPADI
                    """, (main_group[0], sub_group[0])).fetchall()

                    for special_group in special_groups:
                        special_category = {
                            'id': special_group[0],
                            'name': special_group[1],
                            'type': 'special',
                            'parent': sub_group[1]
                        }
                        sub_category['subcategories'].append(special_category)

                    main_category['subcategories'].append(sub_category)

                categories.append(main_category)

            return categories
        except Exception as e:
            logger.error(f"Kategoriler getirilirken hata: {str(e)}")
            raise e
    
    def close(self):
        """Veritabanı bağlantısını kapat"""
        if self.connection:
            self.connection.close()
            logger.info("Veritabanı bağlantısı kapatıldı")

if __name__ == "__main__":
    # Test
    reader = WolvoxProductReader()
    
    print("Ürünler listeleniyor...")
    print("-" * 50)
    
    products = reader.get_all_products()
    for product in products[:5]:  # İlk 5 ürünü göster
        print(f"Stok Kodu: {product['stok_kodu']}")
        print(f"Stok Adı: {product['stok_adi']}")
        print(f"Barkod: {product['barkod']}")
        print(f"Birim: {product['birim']}")
        print(f"KDV Oranı: {product['kdv_orani']}")
        print(f"Kategori: {product['ana_grup']} > {product['ara_grup']} > {product['alt_grup']}")
        
        stock = reader.get_product_stock(product['stok_kodu'])
        print(f"Stok Miktarı: {stock}")
        
        images = reader.get_product_images(product['stok_kodu'])
        print(f"Resim: {images[0] if images else 'Yok'}")
        print("-" * 50)
    
    categories = reader.get_categories()
    print("Kategoriler:")
    for category in categories:
        print(f"{category['name']} ({category['type']})")
        for sub_category in category['subcategories']:
            print(f"  {sub_category['name']} ({sub_category['type']})")
            for child_category in sub_category['subcategories']:
                print(f"    {child_category['name']} ({child_category['type']})")
    
    reader.close()
