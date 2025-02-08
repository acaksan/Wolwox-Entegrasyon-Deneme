import asyncio

import pytest
from core.metrics import registry, reset_metrics
from prometheus_client import REGISTRY
from services.woocommerce_service import WooCommerceService


@pytest.mark.metrics
class TestMetrics:
    
    @pytest.fixture(autouse=True)
    def setup_cleanup(self):
        """Her test öncesi/sonrası temizlik"""
        reset_metrics()
        yield
        reset_metrics()
        
    async def test_product_metrics(self, woo_service):
        """Ürün metriklerini test et"""
        try:
            # Test ürünü oluştur
            product_data = {
                "name": "Metrik Test Ürün",
                "type": "simple",
                "regular_price": "99.99",
                "description": "Test açıklama",
                "short_description": "Kısa açıklama",
                "stock_quantity": 10,
                "manage_stock": True,
                "status": "publish"
            }
            
            # Ürün oluştur ve metrik kontrolü
            created = await woo_service.create_product(product_data)
            product_counter = registry.get_sample_value('woo_products_total')
            assert product_counter == 1
            
            # Ürün güncelle ve metrik kontrolü
            await woo_service.update_product(created["id"], {"stock_quantity": 20})
            update_counter = registry.get_sample_value('woo_product_updates_total')
            assert update_counter == 1
            
            # Ürün sil ve metrik kontrolü
            await woo_service.delete_product(created["id"])
            delete_counter = registry.get_sample_value('woo_products_deleted_total')
            assert delete_counter == 1
            
        except Exception as e:
            pytest.fail(f"Test failed: {str(e)}")
            
    async def test_api_metrics(self, woo_service):
        """API metriklerini test et"""
        try:
            # API isteği yap
            await woo_service.get_products()
            
            # Metrik kontrolü
            request_counter = registry.get_sample_value(
                'woo_api_requests_total',
                {'endpoint': 'products', 'method': 'GET'}
            )
            assert request_counter == 1
            
            # Hata metriği kontrolü
            error_counter = registry.get_sample_value(
                'woo_api_errors_total',
                {'endpoint': 'products'}
            )
            assert error_counter == 0
            
        except Exception as e:
            pytest.fail(f"Test failed: {str(e)}")
            
    async def test_cache_metrics(self, woo_service):
        """Cache metriklerini test et"""
        try:
            # Test ürünü oluştur
            product = await woo_service.create_product({
                "name": "Cache Test",
                "type": "simple",
                "regular_price": "99.99",
                "status": "publish"
            })
            
            # Cache miss kontrolü
            await woo_service.get_product(product["id"])
            cache_miss = registry.get_sample_value('woo_cache_misses_total')
            assert cache_miss == 1
            
            # Cache hit kontrolü
            await woo_service.get_product(product["id"])
            cache_hit = registry.get_sample_value('woo_cache_hits_total')
            assert cache_hit == 1
            
            # Temizlik
            await woo_service.delete_product(product["id"])
            
        except Exception as e:
            pytest.fail(f"Test failed: {str(e)}") 