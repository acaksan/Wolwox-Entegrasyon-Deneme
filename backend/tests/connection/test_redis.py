import pytest
from core.config import get_settings
from redis import Redis


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
        pytest.fail(f"Redis bağlantı hatası: {str(e)}") 