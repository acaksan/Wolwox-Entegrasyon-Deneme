"""Test konfigürasyonu - Wolvox Entegrasyon"""

import logging
import os
import sys
from pathlib import Path
from typing import Generator, Optional

import pytest
import sentry_sdk
from dotenv import load_dotenv
from prometheus_client import (CollectorRegistry, Counter, Histogram,
                               generate_latest)

# Proje kök dizinini path'e ekle
project_root = str(Path(__file__).parent.parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi.testclient import TestClient
from src.core.cache import AsyncCache
from src.core.database import db
from src.core.exceptions import CacheException, DatabaseException
from src.core.logging import logger
# Çekirdek bileşenler
from src.core.settings import Settings
from src.main import app

# Global değişkenler
_settings: Optional[Settings] = None
_cache: Optional[AsyncCache] = None

# Mock sınıfı (Önbellek için)
class MockAsyncCache(AsyncCache):
    """Test için mock önbellek sınıfı"""
    async def connect(self):
        logger.info("🔄 Mock önbellek bağlantısı başlatıldı")
        return True

    async def disconnect(self):
        logger.info("🔄 Mock önbellek bağlantısı kapatıldı")
        return True

# Test metrikleri için Prometheus Collector
registry = CollectorRegistry()
TEST_METRICS = {
    'failures': Counter('test_failures_total', 'Total test failures', ['test_type'], registry=registry),
    'duration': Counter('test_duration_seconds', 'Test duration in seconds', ['test_type'], registry=registry),
    'request_latency': Histogram('test_request_latency_seconds', 'Request latency', ['endpoint'], registry=registry)
}

def pytest_configure(config):
    """Pytest Marker'larını Kaydet"""
    markers = [
        ("unit", "Birim testleri"),
        ("integration", "Entegrasyon testleri"),
        ("functional", "Fonksiyonel testler"),
        ("load", "Yük testleri"),
        ("uat", "Kullanıcı kabul testleri")
    ]
    for marker, desc in markers:
        config.addinivalue_line("markers", f"{marker}: {desc}")

class TestSettings(Settings):
    """Test ayarları sınıfı"""
    model_config = {
        "env_file": "tests/.env.test",
        "case_sensitive": True
    }

@pytest.fixture(scope="session")
def settings() -> Settings:
    """Test ayarları fixture'ı"""
    global _settings
    if _settings is None:
        _settings = TestSettings()
    return _settings

@pytest.fixture(scope="session")
async def test_db():
    """Test Veritabanı bağlantısı fixture'ı"""
    try:
        logger.info("🔌 Test veritabanı bağlantısı başlatılıyor...")
        await db.connect()
        yield db
    except DatabaseException as e:
        TEST_METRICS['failures'].labels(test_type="database").inc()
        logger.error(f"❌ Veritabanı hatası: {str(e)}")
        sentry_sdk.capture_exception(e)
        raise
    finally:
        logger.info("🔌 Test veritabanı bağlantısı kapatılıyor...")
        await db.close_all()

@pytest.fixture(scope="session")
async def test_cache():
    """Redis önbellek fixture'ı"""
    cache = MockAsyncCache()  # Mock sınıfı kullan
    try:
        logger.info("🔄 Test önbellek başlatılıyor...")
        await cache.connect()
        yield cache
    except CacheException as e:
        TEST_METRICS['failures'].labels(test_type="cache").inc()
        logger.error(f"❌ Önbellek hatası: {str(e)}")
        sentry_sdk.capture_exception(e)
        raise
    finally:
        logger.info("🔄 Test önbellek kapatılıyor...")
        await cache.disconnect()

@pytest.fixture(scope="function")
def test_client() -> TestClient:
    """FastAPI test client fixture'ı"""
    with TestClient(app) as client:
        logger.info("✅ Test client oluşturuldu")
        yield client

@pytest.fixture(autouse=True)
async def cleanup_after_test():
    """Her test sonrası temizlik yap"""
    yield
    logger.info("🧹 Test sonrası temizlik yapılıyor...")
    await reset_metrics()

def verify_environment():
    """Test ortamı doğrulama"""
    required_env_vars = [
        'FIREBIRD_HOST', 'FIREBIRD_DATABASE', 'FIREBIRD_USER', 'FIREBIRD_PASSWORD',
        'WOOCOMMERCE_URL', 'WOOCOMMERCE_KEY', 'WOOCOMMERCE_SECRET'
    ]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"❌ Eksik çevre değişkenleri: {missing_vars}")
        raise EnvironmentError(f"Eksik çevre değişkenleri: {missing_vars}")

    db_path = os.getenv('FIREBIRD_DATABASE')
    if not db_path or not os.path.exists(db_path):
        logger.error(f"❌ Veritabanı dosyası bulunamadı: {db_path}")
        raise FileNotFoundError(f"Veritabanı dosyası bulunamadı: {db_path}")

def pytest_sessionstart(session):
    """Test oturumu başlangıcı"""
    logger.info("📝 Test oturumu başladı")
    verify_environment()

def pytest_sessionfinish(session, exitstatus):
    """Test oturumu bitişi"""
    logger.info(f"✅ Test oturumu bitti. Çıkış kodu: {exitstatus}")
    metrics_output = generate_latest(registry).decode()
    logger.info(f"📊 Test metrikleri:\n{metrics_output}")

async def reset_metrics():
    """Test metriklerini sıfırla"""
    for metric in TEST_METRICS.values():
        if hasattr(metric, '_value'):
            metric._value.set(0)
