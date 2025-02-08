import pytest
from services.woocommerce_service import WooCommerceService


@pytest.mark.asyncio
class TestWooCommerceService:
    async def test_get_products(self, woo_service):
        products = await woo_service.get_products()
        assert isinstance(products, list)
        
    async def test_get_product(self, woo_service):
        # Test ürünü oluştur
        product_data = {
            "name": "Test Product",
            "regular_price": "10.00",
            "description": "Test Description"
        }
        
        # Ürünü kaydet
        response = await woo_service.create_product(product_data)
        product_id = response["id"]
        
        # Ürünü getir
        product = await woo_service.get_product(product_id)
        assert product["name"] == "Test Product"
        
        # Temizlik
        await woo_service.delete_product(product_id) 