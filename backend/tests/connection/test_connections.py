import fdb
import pytest
from core.config import get_settings
from core.exceptions import ConnectionException
from redis import Redis
from woocommerce import API


@pytest.mark.connection
def test_redis_connection():
    """Redis bağlantı testi"""
    settings = get_settings()
    
    try:
        redis = Redis.from_url(settings.REDIS_URL)
        assert redis.ping()
        print("✅ Redis bağlantısı başarılı")
        
        # Test veri yazma/okuma
        redis.set("test_key", "test_value")
        value = redis.get("test_key")
        assert value == b"test_value"
        print("✅ Redis veri yazma/okuma başarılı")
        
        # Temizlik
        redis.delete("test_key")
        
    except Exception as e:
        raise ConnectionException(f"Redis bağlantı hatası: {str(e)}")

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
        assert response.status_code in [200, 401, 404]
        print(f"✅ WooCommerce bağlantısı başarılı (Status: {response.status_code})")
        print(f"Response: {response.text[:200]}...")
        
    except Exception as e:
        raise ConnectionException(f"WooCommerce bağlantı hatası: {str(e)}")

@pytest.mark.connection
def test_firebird_connection():
    """Firebird bağlantı testi"""
    settings = get_settings()
    
    try:
        conn = fdb.connect(
            host=settings.FIREBIRD_HOST,
            database=settings.FIREBIRD_DATABASE,
            user=settings.FIREBIRD_USER,
            password=settings.FIREBIRD_PASSWORD,
            charset=settings.FIREBIRD_CHARSET
        )
        assert conn.closed == False
        conn.close()
        print("✅ Firebird bağlantısı başarılı")
        
    except Exception as e:
        raise ConnectionException(f"Firebird bağlantı hatası: {str(e)}") 