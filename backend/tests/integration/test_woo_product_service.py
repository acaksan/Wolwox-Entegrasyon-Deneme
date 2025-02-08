import logging
import time
import uuid

import pytest
from services.woocommerce_product_service import WooCommerceProductService

logger = logging.getLogger(__name__)

class TestWooCommerceProductService:
    @pytest.fixture(autouse=True)
    async def setup(self):
        self.woo_product_service = WooCommerceProductService()
        
        # Benzersiz SKU oluştur
        timestamp = int(time.time())
        random_str = uuid.uuid4().hex[:6]
        unique_sku = f"TEST_{timestamp}_{random_str}"
        
        logger.info(f"Test için benzersiz SKU oluşturuldu: {unique_sku}")
        
        # Test verisi
        self.test_product = {
            "name": f"Test Ürün {unique_sku}",
            "type": "simple",
            "regular_price": "99.99",
            "description": f"Test ürün açıklaması - {unique_sku}",
            "short_description": "Kısa açıklama",
            "sku": unique_sku,
            "manage_stock": True,
            "stock_quantity": 10,
            "status": "draft"  # Test ürünlerini taslak olarak oluştur
        }
        
        try:
            # Test ürünü oluştur
            self.product = await self.woo_product_service.woo_service.create_product(self.test_product)
            logger.info(f"Test ürünü oluşturuldu: {self.product['id']}")
        except Exception as e:
            logger.error(f"Test ürünü oluşturma hatası: {str(e)}")
            raise
        
        yield
        
        # Temizlik
        if hasattr(self, 'product'):
            try:
                await self.woo_product_service.woo_service.delete_product(self.product["id"])
                logger.info(f"Test ürünü silindi: {self.product['id']}")
            except Exception as e:
                logger.warning(f"Test temizliği sırasında hata: {str(e)}")

    @pytest.mark.asyncio
    async def test_stock_update_event(self):
        """Stok güncelleme testi"""
        response = await self.woo_product_service.update_stock(self.product["id"], 50)
        assert response["stock_quantity"] == 50
        
        # Event'in tetiklendiğini kontrol et
        events = await self.woo_product_service.event_service.get_events("stock_changed")
        assert len(events) > 0
        assert events[-1]["product_id"] == self.product["id"]
        assert events[-1]["new_quantity"] == 50

    @pytest.mark.asyncio
    async def test_price_update_event(self):
        """Fiyat güncelleme testi"""
        response = await self.woo_product_service.update_price(self.product["id"], 149.99)
        assert response["regular_price"] == "149.99"
        
        # Event'in tetiklendiğini kontrol et
        events = await self.woo_product_service.event_service.get_events("price_changed")
        assert len(events) > 0
        assert events[-1]["product_id"] == self.product["id"]
        assert float(events[-1]["new_price"]) == 149.99 