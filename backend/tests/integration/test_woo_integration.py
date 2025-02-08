import pytest
from services.woo_service import WooCommerceService


class TestWooIntegration:
    async def test_product_sync(self, woo_service):
        result = await woo_service.create_product({
            "name": "Test Ürün",
            "type": "simple",
            "regular_price": "99.99"
        })
        assert result is not None
        assert result["name"] == "Test Ürün"

    async def test_order_sync(self, woo_service):
        result = await woo_service.create_order({
            "payment_method": "bacs",
            "payment_method_title": "Direct Bank Transfer",
            "status": "pending"
        })
        assert result is not None
        assert result["status"] == "pending" 