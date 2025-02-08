import asyncio
import random

import pytest
from src.core.exceptions import ServiceException
from src.core.logging import logger
from src.core.metrics import reset_metrics
from src.services.woocommerce_service import WooCommerceService


@pytest.mark.asyncio
class TestOrderFlow:
    
    @pytest.fixture(autouse=True)
    def setup_cleanup(self):
        """Her test öncesi/sonrası temizlik"""
        reset_metrics()
        yield
        reset_metrics()
        
    async def test_complete_order_flow(self, woo_service):
        """Tam sipariş akışı testi"""
        try:
            # Test ürünü oluştur
            product = await woo_service.create_product({
                "name": "Test Ürün",
                "type": "simple",
                "regular_price": "99.99",
                "sku": f"TEST{random.randint(1000,9999)}",
                "stock_quantity": 10,
                "manage_stock": True
            })
            
            # Sipariş oluştur
            order_data = {
                "payment_method": "bacs",
                "payment_method_title": "Banka Havalesi",
                "status": "pending",
                "line_items": [
                    {
                        "product_id": product["id"],
                        "quantity": 1
                    }
                ]
            }
            
            order = await woo_service.create_order(order_data)
            assert order["status"] == "pending"
            
            # Temizlik
            await woo_service.delete_product(product["id"])
            
        except Exception as e:
            pytest.fail(f"Test failed: {str(e)}") 