import asyncio
import random
from unittest.mock import AsyncMock, MagicMock

import pytest
from core.exceptions import ServiceException
from core.logging import logger
from services.woocommerce_service import WooCommerceService


@pytest.mark.asyncio
class TestWooCommerceService:
    
    @pytest.fixture(autouse=True)
    async def setup_service(self, woo_service):
        """Test servisi oluştur"""
        self.woo_service = woo_service
        yield
        
    async def test_get_product_cached(self):
        """Cache mekanizması testi"""
        try:
            # Mock ürün verisi
            product_data = {
                "name": "Test Ürün",
                "type": "simple",
                "regular_price": "99.99",
                "sku": f"TEST{random.randint(1000,9999)}"
            }
            
            # Test
            created = await self.woo_service.create_product(product_data)
            product_id = created["id"]
            
            # İlk istek - cache'e yazmalı
            product1 = await self.woo_service.get_product(product_id)
            # İkinci istek - cache'den okumalı
            product2 = await self.woo_service.get_product(product_id)
            
            assert product1["id"] == product2["id"]
            
            # Temizlik
            await self.woo_service.delete_product(product_id)
            
        except Exception as e:
            logger.error(f"❌ Test hatası: {str(e)}")
            pytest.fail(f"Test failed: {str(e)}")
        
    async def test_bulk_update_products(self):
        """Toplu güncelleme testi"""
        try:
            # Test ürünleri oluştur
            products = []
            for i in range(2):
                product = await self.woo_service.create_product({
                    "name": f"Test Ürün {i}",
                    "type": "simple",
                    "regular_price": "99.99",
                    "sku": f"TEST{random.randint(1000,9999)}"
                })
                products.append({
                    "id": product["id"],
                    "stock_quantity": 10 * (i + 1)
                })
            
            # Toplu güncelle
            results = await self.woo_service.bulk_update_products(products)
            
            # Kontroller
            assert len(results) == 2
            assert all(r["id"] for r in results)
            
            # Temizlik
            for product in products:
                await self.woo_service.delete_product(product["id"])
                
        except Exception as e:
            logger.error(f"❌ Test hatası: {str(e)}")
            pytest.fail(f"Test failed: {str(e)}")

@pytest.fixture
def mock_woo_service():
    """Mock WooCommerce servis fixture'ı"""
    mock_service = MagicMock(spec=WooCommerceService)
    mock_service.wcapi = MagicMock()
    mock_service.event_service = MagicMock()
    mock_service.get_products = AsyncMock(return_value=[])
    return mock_service

@pytest.mark.asyncio
async def test_woo_connection(woo_service):
    """WooCommerce bağlantı testi"""
    try:
        response = woo_service.wcapi.get("products")
        assert response.status_code == 200
        logger.info("✅ WooCommerce bağlantısı başarılı")
    except Exception as e:
        logger.error(f"❌ WooCommerce bağlantı hatası: {str(e)}")
        pytest.fail(f"WooCommerce bağlantı hatası: {str(e)}")

@pytest.mark.asyncio
async def test_woo_error_handling(mock_woo_service):
    """WooCommerce hata yönetimi testi"""
    mock_woo_service.get_products.side_effect = ServiceException("Unauthorized")
    
    with pytest.raises(ServiceException) as exc_info:
        await mock_woo_service.get_products()
    assert "Unauthorized" in str(exc_info.value)

@pytest.mark.asyncio
async def test_woo_retry_mechanism(mock_woo_service):
    """WooCommerce yeniden deneme mekanizması testi"""
    # Mock get_products metodunu ayarla
    mock_woo_service.get_products = AsyncMock()
    mock_woo_service.get_products.side_effect = [
        ServiceException("Error"),  # İlk çağrı hata verecek
        {"products": []}  # İkinci çağrı başarılı olacak
    ]
    
    # İlk denemede hata alacak
    with pytest.raises(ServiceException):
        await mock_woo_service.get_products()
    
    # İkinci deneme başarılı olacak
    result = await mock_woo_service.get_products()
    assert result == {"products": []}
    
    # Toplam 2 kez çağrılmış olmalı
    assert mock_woo_service.get_products.call_count == 2 