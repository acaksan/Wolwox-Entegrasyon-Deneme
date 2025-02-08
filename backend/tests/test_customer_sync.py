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

from src.services.customer_sync_service import CustomerSyncService


def test_customer_sync():
    """Müşteri senkronizasyonunu test et"""
    try:
        # CustomerSyncService örneği oluştur
        sync_service = CustomerSyncService()
        
        # B2C müşterilerini senkronize et
        print("\nB2C müşterileri senkronize ediliyor...")
        b2c_results = sync_service.sync_b2c_customers()
        print(f"B2C sonuçları: {b2c_results}")
        
        # B2B müşterilerini senkronize et
        print("\nB2B müşterileri senkronize ediliyor...")
        b2b_results = sync_service.sync_b2b_customers()
        print(f"B2B sonuçları: {b2b_results}")
        
        # WooCommerce'den yeni müşterileri al
        print("\nYeni WooCommerce müşterileri senkronize ediliyor...")
        woo_results = sync_service.sync_new_woo_customers()
        print(f"WooCommerce sonuçları: {woo_results}")
        
        print("\nSenkronizasyon tamamlandı!")
        return True
        
    except Exception as e:
        print(f"Hata: {str(e)}")
        return False

if __name__ == "__main__":
    test_customer_sync()
