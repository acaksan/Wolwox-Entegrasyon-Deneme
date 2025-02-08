import pytest
from core.config import get_settings
from core.exceptions import ConnectionException
from woocommerce import API


@pytest.mark.connection
def test_woocommerce_connection():
    """WooCommerce API bağlantı testi"""
    settings = get_settings()
    
    wcapi = API(
        url=settings.WOOCOMMERCE_URL,
        consumer_key=settings.WOOCOMMERCE_KEY,
        consumer_secret=settings.WOOCOMMERCE_SECRET,
        version=settings.WOOCOMMERCE_API_VERSION,
        verify_ssl=settings.WOOCOMMERCE_VERIFY_SSL,
        timeout=30
    )
    
    try:
        response = wcapi.get("products")
        assert response.status_code in [200, 401, 404]  # Herhangi bir geçerli HTTP yanıtı
        print(f"✅ WooCommerce bağlantısı başarılı (Status: {response.status_code})")
        print(f"Response: {response.text[:200]}...")  # İlk 200 karakteri göster
        
    except Exception as e:
        raise ConnectionException(f"WooCommerce bağlantı hatası: {str(e)}") 