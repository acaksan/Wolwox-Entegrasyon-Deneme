import pytest
# SSL uyarılarını devre dışı bırak (sadece test ortamı için)
import urllib3
from core.logging import logger
from services.woocommerce_analytics_service import WooCommerceAnalyticsService
from services.woocommerce_service import WooCommerceService

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@pytest.fixture(scope="function")
async def analytics_service():
    """Test için analytics servisi hazırlar"""
    woo_service = WooCommerceService()
    service = WooCommerceAnalyticsService(woo_service)
    logger.info("✅ Test için analytics servisi hazırlandı")
    return service

pytestmark = pytest.mark.asyncio  # Tüm testlere asyncio mark'ı ekle

class TestWooCommerceAnalytics:
    
    @pytest.mark.parametrize("period", ["week", "month", "last_month", "year"])
    async def test_get_revenue_stats(self, analytics_service, period):
        """Gelir istatistikleri testleri"""
        logger.info(f"🔍 {period} periyodu için gelir istatistikleri test ediliyor")
        stats = await analytics_service.get_revenue_stats(period=period)
        assert isinstance(stats, dict)  # Sözlük olarak kontrol et
        assert 'total_sales' in stats  # Örnek bir anahtar kontrolü
        logger.info(f"✅ {period} periyodu için gelir istatistikleri başarıyla alındı")

    async def test_get_product_performance(self, analytics_service):
        """Ürün performansı testi"""
        logger.info("🔍 Ürün performansı test ediliyor")
        products = await analytics_service.get_product_performance()
        assert isinstance(products, list)
        logger.info(f"✅ Ürün performansı başarıyla alındı: {len(products)} ürün")

    async def test_get_customer_stats(self, analytics_service):
        """Müşteri istatistikleri testi"""
        logger.info("🔍 Müşteri istatistikleri test ediliyor")
        stats = await analytics_service.get_customer_stats()
        assert isinstance(stats, list)
        assert len(stats) > 0
        logger.info(f"✅ Müşteri istatistikleri başarıyla alındı: {len(stats)} grup") 