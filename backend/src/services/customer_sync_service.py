import logging
import os
from datetime import UTC, datetime, timedelta
from typing import Dict, List, Optional

from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from src.database.firebird import FirebirdDB
from woocommerce import API

# .env dosyasını yükle
load_dotenv()

class CustomerSyncService:
    """Müşteri senkronizasyon servisi"""
    
    def __init__(self):
        """WooCommerce API bağlantısını başlat"""
        try:
            # API URL'sini düzenle
            api_url = os.getenv('WOOCOMMERCE_URL', '').rstrip('/')
            
            # Basic auth için kullanıcı bilgileri
            self.auth = HTTPBasicAuth(
                os.getenv('WORDPRESS_USERNAME'),
                os.getenv('WORDPRESS_PASSWORD')
            )
            
            # WooCommerce API
            self.wcapi = API(
                url=api_url,
                consumer_key=os.getenv('WOOCOMMERCE_CONSUMER_KEY'),
                consumer_secret=os.getenv('WOOCOMMERCE_CONSUMER_SECRET'),
                version=os.getenv('WOOCOMMERCE_API_VERSION', 'wc/v3'),
                verify_ssl=os.getenv('WOOCOMMERCE_VERIFY_SSL', 'True').lower() == 'true',
                timeout=30
            )
            
            # API URL'lerini hazırla
            self.wp_api_url = f"{api_url}/wp-json"
            self.wc_api_url = f"{self.wp_api_url}/wc/v3"
            
            logging.info("WooCommerce API bağlantısı başlatıldı")
            
        except Exception as e:
            logging.error(f"WooCommerce API bağlantısı başlatılırken hata: {e}")
            raise
            
    def get_customer_by_email(self, email: str) -> Optional[Dict]:
        """Email adresine göre müşteriyi getir"""
        try:
            response = self.wcapi.get("customers", params={"email": email})
            if response.status_code == 200:
                customers = response.json()
                return customers[0] if customers else None
            return None
        except Exception as e:
            logging.error(f"Email ile müşteri aranırken hata: {e}")
            return None
            
    def create_customer(self, customer_data: Dict) -> Optional[Dict]:
        """Yeni müşteri oluştur"""
        try:
            response = self.wcapi.post("customers", customer_data)
            if response.status_code in [200, 201]:
                return response.json()
            logging.error(f"Müşteri oluşturma başarısız. Durum kodu: {response.status_code}")
            return None
        except Exception as e:
            logging.error(f"Müşteri oluştururken hata: {e}")
            return None
            
    def update_customer(self, customer_id: int, customer_data: Dict) -> Optional[Dict]:
        """Var olan müşteriyi güncelle"""
        try:
            response = self.wcapi.put(f"customers/{customer_id}", customer_data)
            if response.status_code == 200:
                return response.json()
            logging.error(f"Müşteri güncelleme başarısız. Durum kodu: {response.status_code}")
            return None
        except Exception as e:
            logging.error(f"Müşteri güncellenirken hata: {e}")
            return None
            
    def prepare_customer_data(self, cari_data: Dict) -> Dict:
        """Firebird müşteri verisini WooCommerce formatına dönüştür"""
        return {
            "email": cari_data.get("WEB_USER_NAME", ""),
            "first_name": cari_data.get("ADI", ""),
            "last_name": cari_data.get("SOYADI", ""),
            "username": cari_data.get("WEB_USER_NAME", "").split('@')[0],
            "billing": {
                "first_name": cari_data.get("ADI", ""),
                "last_name": cari_data.get("SOYADI", ""),
                "company": cari_data.get("TICARI_UNVANI", ""),
                "address_1": cari_data.get("ADRESI_1", ""),
                "city": cari_data.get("ILI_1", ""),
                "state": cari_data.get("ILCESI_1", ""),
                "postcode": cari_data.get("POSTA_KODU", ""),
                "country": "TR",
                "email": cari_data.get("WEB_USER_NAME", ""),
                "phone": cari_data.get("TELEFON", "")
            },
            "shipping": {
                "first_name": cari_data.get("ADI", ""),
                "last_name": cari_data.get("SOYADI", ""),
                "company": cari_data.get("TICARI_UNVANI", ""),
                "address_1": cari_data.get("ADRESI_1", ""),
                "city": cari_data.get("ILI_1", ""),
                "state": cari_data.get("ILCESI_1", ""),
                "postcode": cari_data.get("POSTA_KODU", ""),
                "country": "TR"
            },
            "meta_data": [
                {
                    "key": "musteri_tipi",
                    "value": "b2c" if cari_data.get("MUSTERI_TIPI") == 2 else "b2b"
                },
                {
                    "key": "vergi_dairesi",
                    "value": cari_data.get("VERGI_DAIRESI", "")
                },
                {
                    "key": "vergi_no",
                    "value": cari_data.get("VERGI_NO", "")
                },
                {
                    "key": "fb_blkodu",
                    "value": cari_data.get("BLKODU", "")
                }
            ]
        }
        
    def sync_customer(self, cari_data: Dict) -> bool:
        """Müşteriyi senkronize et"""
        try:
            # Müşteri verilerini hazırla
            customer_data = self.prepare_customer_data(cari_data)
            
            # Email kontrolü
            email = customer_data.get("email")
            if not email:
                logging.warning(f"Email adresi olmayan müşteri atlandı: {cari_data.get('TICARI_UNVANI')}")
                return False
                
            # Mevcut müşteriyi kontrol et
            existing_customer = self.get_customer_by_email(email)
            
            if existing_customer:
                # Müşteriyi güncelle
                customer_id = existing_customer["id"]
                result = self.update_customer(customer_id, customer_data)
                action = "güncellendi"
            else:
                # Yeni müşteri oluştur
                result = self.create_customer(customer_data)
                action = "oluşturuldu"
                
            if result:
                logging.info(f"Müşteri başarıyla {action}: {email}")
                return True
            else:
                logging.error(f"Müşteri {action}medi: {email}")
                return False
                
        except Exception as e:
            logging.error(f"Müşteri senkronizasyonu sırasında hata: {e}")
            return False
            
    def sync_b2c_customers(self) -> Dict[str, int]:
        """B2C müşterilerini senkronize et"""
        results = {
            'success': 0,
            'failed': 0,
            'total': 0
        }
        
        try:
            with FirebirdDB() as db:
                # B2C müşterilerini al
                db.execute("""
                    SELECT *
                    FROM CARI
                    WHERE MUSTERI_TIPI = 2
                    AND AKTIF = 1
                    AND WEB_USER_NAME IS NOT NULL
                    AND WEB_USER_NAME <> ''
                """)
                
                customers = []
                for row in db.fetchall():
                    customer = {}
                    for i, col in enumerate(db.cursor.description):
                        customer[col[0]] = row[i]
                    customers.append(customer)
                
                results['total'] = len(customers)
                
                # Her müşteriyi senkronize et
                for customer in customers:
                    if self.sync_customer(customer):
                        results['success'] += 1
                    else:
                        results['failed'] += 1
                        
                logging.info(f"B2C müşteri senkronizasyonu tamamlandı: {results}")
                return results
                
        except Exception as e:
            logging.error(f"B2C müşteri senkronizasyonu sırasında hata: {e}")
            return results
            
    def sync_b2b_customers(self) -> Dict[str, int]:
        """B2B müşterilerini senkronize et"""
        results = {
            'success': 0,
            'failed': 0,
            'total': 0
        }
        
        try:
            with FirebirdDB() as db:
                # B2B müşterilerini al
                db.execute("""
                    SELECT *
                    FROM CARI
                    WHERE MUSTERI_TIPI = 1
                    AND ARA_GRUBU = 'TOPTAN LASTİK'
                    AND AKTIF = 1
                """)
                
                customers = []
                for row in db.fetchall():
                    customer = {}
                    for i, col in enumerate(db.cursor.description):
                        customer[col[0]] = row[i]
                    customers.append(customer)
                
                results['total'] = len(customers)
                
                # Her müşteriyi senkronize et
                for customer in customers:
                    if self.sync_customer(customer):
                        results['success'] += 1
                    else:
                        results['failed'] += 1
                        
                logging.info(f"B2B müşteri senkronizasyonu tamamlandı: {results}")
                return results
                
        except Exception as e:
            logging.error(f"B2B müşteri senkronizasyonu sırasında hata: {e}")
            return results
            
    def sync_all_customers(self) -> Dict[str, Dict[str, int]]:
        """Tüm müşterileri senkronize et"""
        results = {
            'b2b': self.sync_b2b_customers(),
            'b2c': self.sync_b2c_customers()
        }
        
        logging.info(f"Tüm müşteri senkronizasyonu tamamlandı: {results}")
        return results

    def get_woo_customers(self, modified_after: datetime = None) -> List[Dict]:
        """WooCommerce'den müşterileri getir"""
        try:
            params = {
                "per_page": 100,
                "page": 1
            }
            
            if modified_after:
                params["modified_after"] = modified_after.isoformat()
                
            customers = []
            while True:
                response = self.wcapi.get("customers", params=params)
                if response.status_code != 200:
                    break
                    
                page_customers = response.json()
                if not page_customers:
                    break
                    
                customers.extend(page_customers)
                params["page"] += 1
                
            return customers
            
        except Exception as e:
            logging.error(f"WooCommerce müşterileri alınırken hata: {e}")
            return []

    def prepare_cari_data(self, woo_customer: Dict) -> Dict:
        """WooCommerce müşteri verisini Wolvox formatına dönüştür"""
        # Müşteri kodu oluştur (örn: WEB-00001)
        with FirebirdDB() as db:
            db.execute("SELECT COUNT(*) FROM CARI WHERE GRUBU = 'İNTERNET MÜŞTERİ'")
            count = db.fetchone()[0]
            cari_kodu = f"WEB-{(count + 1):05d}"
            
        return {
            "CARIKODU": cari_kodu,
            "TICARI_UNVANI": f"{woo_customer['billing']['first_name']} {woo_customer['billing']['last_name']}",
            "GRUBU": "İNTERNET MÜŞTERİ",
            "MUSTERI_TIPI": 2,  # B2C müşterisi
            "VERGI_DAIRESI": woo_customer['billing'].get('company', ''),
            "VERGI_NO": woo_customer['billing'].get('vat_number', ''),
            "ADRESI_1": woo_customer['billing']['address_1'],
            "ILI_1": woo_customer['billing']['city'],
            "ILCESI_1": woo_customer['billing']['state'],
            "TEL1": woo_customer['billing']['phone'],
            "E_MAIL": woo_customer['billing']['email'],
            "WEB_USER_NAME": woo_customer['billing']['email'],
            "AKTIF": 1
        }

    def sync_woo_customer_to_wolvox(self, woo_customer: Dict) -> bool:
        """WooCommerce müşterisini Wolvox'a senkronize et"""
        try:
            # Müşteri verilerini hazırla
            cari_data = self.prepare_cari_data(woo_customer)
            email = woo_customer.get("email")
            
            if not email:
                logging.warning("Email adresi olmayan müşteri atlandı")
                return False
                
            with FirebirdDB() as db:
                # Önce müşteriyi email ile kontrol et
                db.execute("""
                    SELECT BLKODU 
                    FROM CARI 
                    WHERE E_MAIL = ? 
                    AND AKTIF = 1
                """, (email,))
                
                existing = db.fetchone()
                
                if existing:
                    # Müşteriyi güncelle
                    blkodu = existing[0]
                    update_fields = []
                    update_values = []
                    
                    for key, value in cari_data.items():
                        if value is not None:
                            update_fields.append(f"{key} = ?")
                            update_values.append(value)
                            
                    update_values.append(blkodu)
                    
                    sql = f"""
                        UPDATE CARI 
                        SET {', '.join(update_fields)}
                        WHERE BLKODU = ?
                    """
                    
                    db.execute(sql, tuple(update_values))
                    
                else:
                    # Yeni müşteri oluştur
                    fields = list(cari_data.keys())
                    placeholders = ['?' for _ in fields]
                    values = [cari_data[field] for field in fields]
                    
                    sql = f"""
                        INSERT INTO CARI ({', '.join(fields)})
                        VALUES ({', '.join(placeholders)})
                    """
                    
                    db.execute(sql, tuple(values))
                    
                db.commit()
                return True
                
        except Exception as e:
            logging.error(f"WooCommerce müşterisi Wolvox'a aktarılırken hata: {e}")
            return False

    def sync_new_woo_customers(self) -> Dict[str, int]:
        """Son eklenen WooCommerce müşterilerini Wolvox'a senkronize et"""
        results = {
            'success': 0,
            'failed': 0,
            'total': 0
        }
        
        try:
            # Son 24 saat içinde eklenen/güncellenen müşterileri al
            cutoff_time = datetime.now(UTC) - timedelta(hours=24)
            customers = self.get_woo_customers(modified_after=cutoff_time)
            
            results['total'] = len(customers)
            
            for customer in customers:
                if self.sync_woo_customer_to_wolvox(customer):
                    results['success'] += 1
                else:
                    results['failed'] += 1
                    
            logging.info(f"WooCommerce müşteri senkronizasyonu tamamlandı: {results}")
            return results
            
        except Exception as e:
            logging.error(f"WooCommerce müşteri senkronizasyonu sırasında hata: {e}")
            return results

    def sync_order_customer(self, order_data: Dict) -> Optional[int]:
        """Sipariş müşterisini senkronize et"""
        try:
            # Müşteri verilerini hazırla
            customer_data = {
                'billing': order_data['billing'],
                'shipping': order_data['shipping']
            }
            
            with FirebirdDB() as db:
                # Önce email ile müşteriyi kontrol et
                db.execute("""
                    SELECT BLKODU 
                    FROM CARI 
                    WHERE E_MAIL = ? 
                    AND AKTIF = 1
                """, (customer_data['billing']['email'],))
                
                existing = db.fetchone()
                if existing:
                    return existing[0]
                    
                # Yeni müşteri oluştur
                cari_data = self.prepare_cari_data(customer_data)
                
                # Vergi no veya TC ise TC_KIMLIK_NO alanına da ekle
                vergi_no = customer_data['billing'].get('vat_number', '')
                if vergi_no and len(vergi_no) == 11:
                    cari_data["TC_KIMLIK_NO"] = vergi_no
                
                # Yeni BLKODU al
                db.execute("SELECT MAX(BLKODU) + 1 FROM CARI")
                new_blkodu = db.fetchone()[0] or 1
                
                # BLKODU ekle
                cari_data["BLKODU"] = new_blkodu
                
                fields = list(cari_data.keys())
                placeholders = ['?' for _ in fields]
                values = [cari_data[field] for field in fields]
                
                sql = f"""
                    INSERT INTO CARI ({', '.join(fields)})
                    VALUES ({', '.join(placeholders)})
                """
                
                db.execute(sql, tuple(values))
                db.commit()
                
                logging.info(f"Yeni müşteri oluşturuldu: {customer_data['billing']['email']} (BLKODU: {new_blkodu})")
                return new_blkodu
                
        except Exception as e:
            logging.error(f"Sipariş müşterisi senkronizasyonu hatası: {str(e)}")
            return None
