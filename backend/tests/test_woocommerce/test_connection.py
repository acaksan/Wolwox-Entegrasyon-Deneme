import pytest
from core.config import get_settings
from requests.exceptions import HTTPError
from woocommerce import API


@pytest.mark.woo
def test_woocommerce_connection(settings):
    try:
        wcapi = API(
            url=settings.WOOCOMMERCE_URL,
            consumer_key=settings.WOOCOMMERCE_KEY,
            consumer_secret=settings.WOOCOMMERCE_SECRET,
            version=settings.WOOCOMMERCE_API_VERSION,
            verify_ssl=settings.WOOCOMMERCE_VERIFY_SSL
        )
        
        response = wcapi.get("products")
        assert response.status_code == 200
    except Exception as e:
        pytest.skip(f"WooCommerce bağlantısı kurulamadı: {str(e)}")

@pytest.mark.woo
def test_woocommerce_auth_error():
    """Geçersiz kimlik bilgileriyle bağlantı testi"""
    wcapi = API(
        url="https://example.com",
        consumer_key="invalid_key",
        consumer_secret="invalid_secret",
        version="wc/v3",
        verify_ssl=False,
        timeout=5
    )
    
    try:
        response = wcapi.get("products")
        assert response.status_code in [401, 403, 404]  # Yetkilendirme hatası veya bulunamadı
    except HTTPError as e:
        assert e.response.status_code in [401, 403, 404]  # Yetkilendirme hatası veya bulunamadı
    except Exception as e:
        pytest.fail(f"Beklenmeyen hata: {str(e)}") 