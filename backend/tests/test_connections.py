import logging

import fdb
import pytest
from redis import Redis
from src.core.config import get_settings
from woocommerce import API

logger = logging.getLogger(__name__)

@pytest.mark.connection
def test_woocommerce_connection():
    """WooCommerce bağlantısını test eder"""
    settings = get_settings()
    
    try:
        wc = API(
            url=settings.WOOCOMMERCE_URL,
            consumer_key=settings.WOOCOMMERCE_KEY,
            consumer_secret=settings.WOOCOMMERCE_SECRET,
            version=settings.WOOCOMMERCE_API_VERSION,
            verify_ssl=settings.WOOCOMMERCE_VERIFY_SSL
        )
        response = wc.get("products")
        assert response.status_code in [200, 401]
        logger.info("✅ WooCommerce bağlantısı başarılı")
    except Exception as e:
        logger.error(f"❌ WooCommerce bağlantı hatası: {str(e)}")
        raise

@pytest.mark.connection
def test_redis_connection():
    """Redis bağlantı testi"""
    settings = get_settings()
    
    try:
        redis = Redis.from_url(settings.REDIS_URL)
        assert redis.ping()
        print("✅ Redis bağlantısı başarılı")
    except Exception as e:
        pytest.fail(f"Redis bağlantı hatası: {str(e)}")

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
        pytest.fail(f"Firebird bağlantı hatası: {str(e)}") 