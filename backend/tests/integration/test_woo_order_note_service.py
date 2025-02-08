import random

import pytest
from core.logging import logger
from services.woocommerce_order_note_service import WooCommerceOrderNoteService
from services.woocommerce_service import WooCommerceService


@pytest.fixture(scope="function")
async def note_service():
    """Test için order note servisi hazırlar"""
    woo_service = WooCommerceService()
    service = WooCommerceOrderNoteService(woo_service)
    logger.info("✅ Test için order note servisi hazırlandı")
    return service

@pytest.fixture
async def test_product(woo_service):
    """Test için ürün oluşturur"""
    product_data = {
        "name": "Test Ürün",
        "sku": f"TEST{random.randint(1000,9999)}",
        "regular_price": "100.00",
        "stock_quantity": 10
    }
    result = await woo_service.create_product(product_data)
    return result

pytestmark = pytest.mark.asyncio

class TestWooCommerceOrderNote:
    async def test_add_order_note(self, note_service, test_order):
        """Sipariş notu ekleme testi"""
        logger.info("🔍 Sipariş notu ekleme test ediliyor")
        
        result = await note_service.add_order_note(
            test_order,
            "Test notu",
            is_customer_note=True
        )
        
        assert result["note"] == "Test notu"
        logger.info(f"✅ Sipariş notu eklendi, ID: {result['id']}")
        
    async def test_get_order_notes(self, note_service, test_order):
        """Notları listeleme testi"""
        logger.info("🔍 Sipariş notlarını listeleme test ediliyor")
        
        notes = await note_service.get_order_notes(test_order)
        assert isinstance(notes, list)
        logger.info(f"✅ {len(notes)} sipariş notu listelendi") 