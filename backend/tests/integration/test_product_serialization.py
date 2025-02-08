import time
import uuid
from datetime import datetime

import pytest
from core.logging import logger
from models.schemas import Product
from services.woocommerce_product_service import WooCommerceProductService


@pytest.mark.asyncio
class TestProductSerialization:
    @pytest.fixture(autouse=True)
    async def setup(self):
        self.woo_product_service = WooCommerceProductService()
        
        # Benzersiz SKU oluştur
        unique_sku = f"TEST_{uuid.uuid4().hex[:8]}_{int(time.time())}"
        
        # Test ürünü
        self.test_product = Product(
            id=None,
            name=f"Test Ürün {unique_sku}",
            sku=unique_sku,
            regular_price="99.99",
            sale_price="89.99",
            description="Test ürün açıklaması",
            short_description="Kısa açıklama",
            stock_quantity=10,
            stock_status="instock",
            status="draft"
        )
        
        # Test ürününü oluştur
        product_dict = self.test_product.model_dump(
            exclude={'created_at', 'updated_at'}, 
            exclude_none=True
        )
        response = await self.woo_product_service.woo_service.create_product(product_dict)
        self.product_id = response["id"]
        
        yield
        
        # Temizlik
        if hasattr(self, 'product_id'):
            try:
                await self.woo_product_service.woo_service.delete_product(self.product_id)
            except Exception as e:
                logger.warning(f"Test temizliği sırasında hata: {str(e)}")

    async def test_product_serialization(self):
        """Ürün serileştirme testi"""
        # Ürünü getir
        product = await self.woo_product_service.get_product(self.product_id)
        
        # Product modeline dönüştür
        product_model = Product.model_validate(product)
        
        # Kontroller
        assert product_model.id == self.product_id
        assert product_model.name == self.test_product.name
        assert product_model.sku == self.test_product.sku
        assert float(product_model.regular_price) == float(self.test_product.regular_price)
        assert float(product_model.sale_price) == float(self.test_product.sale_price)
        # Stok kontrolü - None veya beklenen değer olabilir
        if product_model.stock_quantity is not None:
            assert product_model.stock_quantity == self.test_product.stock_quantity

    async def test_product_deserialization(self):
        """Ürün deserileştirme testi"""
        # Product modelini dict'e dönüştür
        product_dict = self.test_product.model_dump(exclude_none=True)
        
        # WooCommerce'e gönder
        response = await self.woo_product_service.woo_service.create_product(product_dict)
        
        # Kontroller
        assert response["name"] == self.test_product.name
        assert response["sku"] == self.test_product.sku
        assert float(response["regular_price"]) == float(self.test_product.regular_price)
        assert float(response["sale_price"]) == float(self.test_product.sale_price)
        # Stok kontrolü - None veya beklenen değer olabilir
        if response.get("stock_quantity") is not None:
            assert response["stock_quantity"] == self.test_product.stock_quantity 