import logging
import os

from dotenv import load_dotenv
from woocommerce import API

# Log ayarları
logging.basicConfig(level=logging.DEBUG)

# .env dosyasını yükle
load_dotenv()

def test_woocommerce_connection():
    """WooCommerce API bağlantısını test et"""
    try:
        # WooCommerce API bağlantısı
        wcapi = API(
            url=os.getenv('WOOCOMMERCE_URL'),
            consumer_key=os.getenv('WOOCOMMERCE_CONSUMER_KEY'),
            consumer_secret=os.getenv('WOOCOMMERCE_CONSUMER_SECRET'),
            version=os.getenv('WOOCOMMERCE_API_VERSION'),
            verify_ssl=os.getenv('WOOCOMMERCE_VERIFY_SSL', 'True').lower() == 'true',
            timeout=30
        )
        
        # Bağlantıyı test et
        response = wcapi.get("products")
        print(f"\nDurum Kodu: {response.status_code}")
        print(f"Headers: {response.headers}")
        
        if response.status_code == 200:
            print("\nBağlantı başarılı!")
            return True
        else:
            print(f"\nBağlantı hatası! Yanıt: {response.text}")
            return False
            
    except Exception as e:
        print(f"\nHata: {str(e)}")
        return False

if __name__ == "__main__":
    test_woocommerce_connection()
