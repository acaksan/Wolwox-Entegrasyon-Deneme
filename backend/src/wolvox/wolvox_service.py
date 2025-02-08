"""Wolvox ERP API servisi"""

from typing import Any, Dict, List, Optional

import fdb
from core.logging import log_error, log_info, log_warning, logger
from core.settings import get_settings

settings = get_settings()

class WolvoxService:
    """Wolvox ERP API servisi"""
    
    def __init__(self):
        """Wolvox veritabanı bağlantısını başlat"""
        self.connection = None
        self.connect()
    
    def connect(self):
        """Veritabanına bağlan"""
        try:
            log_info("wolvox_service", f"Veritabanı bağlantısı başlatılıyor: {settings.DB_PATH}")
            
            # DLL yolunu ayarla
            fdb.load_api(r"C:\Program Files (x86)\Firebird\Firebird_2_5\bin\fbclient.dll")
            
            # Bağlantıyı oluştur
            self.connection = fdb.connect(
                dsn=settings.DB_PATH,
                user='SYSDBA',
                password='masterkey'
            )
            log_info("wolvox_service", "Wolvox veritabanına bağlanıldı")
        except Exception as e:
            log_error("wolvox_service", "Veritabanı bağlantı hatası", {"error": str(e)})
            raise RuntimeError(f"Veritabanı bağlantı hatası: {str(e)}")
    
    def ensure_connection(self):
        """Bağlantının açık olduğundan emin ol"""
        if not self.connection or self.connection.closed:
            self.connect()
    
    async def find_customer(self, search_params: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """Müşteri ara"""
        self.ensure_connection()
        
        try:
            cursor = self.connection.cursor()
            
            # Arama parametrelerini hazırla
            conditions = []
            params = []
            
            if search_params.get("vergi_no"):
                conditions.append("VERGI_NO = ?")
                params.append(search_params["vergi_no"])
            
            if search_params.get("email"):
                conditions.append("EMAIL = ?")
                params.append(search_params["email"])
            
            if search_params.get("telefon"):
                conditions.append("TELEFON = ?")
                params.append(search_params["telefon"])
            
            if not conditions:
                log_warning("wolvox_service", "Arama parametresi belirtilmedi")
                return None
            
            # SQL sorgusunu oluştur
            sql = f"""
                SELECT FIRST 1
                    MUSTERI_KODU,
                    UNVAN,
                    VERGI_NO,
                    VERGI_DAIRE,
                    ADRES,
                    ADRES2,
                    IL,
                    ILCE,
                    ULKE,
                    TELEFON,
                    EMAIL,
                    MUSTERI_TIPI,
                    PARA_BIRIMI
                FROM CARI_HESAPLAR
                WHERE {" OR ".join(conditions)}
            """
            
            cursor.execute(sql, params)
            row = cursor.fetchone()
            
            if row:
                # Sonucu sözlük olarak döndür
                columns = [desc[0].lower() for desc in cursor.description]
                customer = dict(zip(columns, row))
                log_info("wolvox_service", f"Müşteri bulundu: {customer['musteri_kodu']}")
                return customer
            
            log_info("wolvox_service", "Müşteri bulunamadı")
            return None
            
        except Exception as e:
            log_error("wolvox_service", "Müşteri arama hatası", {"error": str(e)})
            raise RuntimeError(f"Müşteri arama hatası: {str(e)}")
        finally:
            cursor.close()
    
    async def create_customer(self, customer_data: Dict[str, Any]) -> Optional[str]:
        """Yeni müşteri oluştur"""
        self.ensure_connection()
        
        try:
            cursor = self.connection.cursor()
            
            # Yeni müşteri kodu al
            cursor.execute("SELECT MAX(MUSTERI_KODU) FROM CARI_HESAPLAR")
            max_kod = cursor.fetchone()[0] or "C00000"
            yeni_kod = f"C{int(max_kod[1:]) + 1:05d}"
            
            # SQL sorgusunu hazırla
            sql = """
                INSERT INTO CARI_HESAPLAR (
                    MUSTERI_KODU, UNVAN, VERGI_NO, VERGI_DAIRE,
                    ADRES, ADRES2, IL, ILCE, ULKE,
                    TELEFON, EMAIL, MUSTERI_TIPI, PARA_BIRIMI,
                    AKTIF, ENTEGRASYON_ID
                ) VALUES (
                    ?, ?, ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?, ?, ?,
                    1, ?
                )
            """
            
            # Parametreleri hazırla
            params = [
                yeni_kod,
                customer_data.get("unvan", ""),
                customer_data.get("vergi_no", ""),
                customer_data.get("vergi_daire", ""),
                customer_data.get("adres", ""),
                customer_data.get("adres2", ""),
                customer_data.get("il", ""),
                customer_data.get("ilce", ""),
                customer_data.get("ulke", "TR"),
                customer_data.get("telefon", ""),
                customer_data.get("email", ""),
                customer_data.get("musteri_tipi", "B2C"),
                customer_data.get("para_birimi", "TRY"),
                customer_data.get("woo_customer_id", "")
            ]
            
            # Sorguyu çalıştır
            cursor.execute(sql, params)
            self.connection.commit()
            
            log_info("wolvox_service", f"Yeni müşteri oluşturuldu: {yeni_kod}")
            return yeni_kod
            
        except Exception as e:
            self.connection.rollback()
            log_error("wolvox_service", "Müşteri oluşturma hatası", {"error": str(e)})
            raise RuntimeError(f"Müşteri oluşturma hatası: {str(e)}")
        finally:
            cursor.close()
    
    async def update_customer(self, musteri_kodu: str, customer_data: Dict[str, Any]) -> bool:
        """Müşteri güncelle"""
        self.ensure_connection()
        
        try:
            cursor = self.connection.cursor()
            
            # SQL sorgusunu hazırla
            sql = """
                UPDATE CARI_HESAPLAR SET
                    UNVAN = ?,
                    VERGI_NO = ?,
                    VERGI_DAIRE = ?,
                    ADRES = ?,
                    ADRES2 = ?,
                    IL = ?,
                    ILCE = ?,
                    ULKE = ?,
                    TELEFON = ?,
                    EMAIL = ?,
                    MUSTERI_TIPI = ?,
                    PARA_BIRIMI = ?,
                    ENTEGRASYON_ID = ?
                WHERE MUSTERI_KODU = ?
            """
            
            # Parametreleri hazırla
            params = [
                customer_data.get("unvan", ""),
                customer_data.get("vergi_no", ""),
                customer_data.get("vergi_daire", ""),
                customer_data.get("adres", ""),
                customer_data.get("adres2", ""),
                customer_data.get("il", ""),
                customer_data.get("ilce", ""),
                customer_data.get("ulke", "TR"),
                customer_data.get("telefon", ""),
                customer_data.get("email", ""),
                customer_data.get("musteri_tipi", "B2C"),
                customer_data.get("para_birimi", "TRY"),
                customer_data.get("woo_customer_id", ""),
                musteri_kodu
            ]
            
            # Sorguyu çalıştır
            cursor.execute(sql, params)
            self.connection.commit()
            
            log_info("wolvox_service", f"Müşteri güncellendi: {musteri_kodu}")
            return True
            
        except Exception as e:
            self.connection.rollback()
            log_error("wolvox_service", "Müşteri güncelleme hatası", {"error": str(e)})
            raise RuntimeError(f"Müşteri güncelleme hatası: {str(e)}")
        finally:
            cursor.close()

# Servis örneği
wolvox_service = WolvoxService()
