from datetime import datetime

import pytest

from backend.core.cache import AsyncCache
from backend.services import SyncService, WolvoxService, WooCommerceService
from backend.services.woocommerce_media_service import WooCommerceMediaService


@pytest.mark.integration
class TestProductSync:
    @pytest.fixture
    async def sync_service(self, woo_service, wolvox_service, redis_client):
        return SyncService(
            woo=woo_service,
            wolvox=wolvox_service,
            cache=AsyncCache()
        )
    
    @pytest.fixture
    async def test_product(self):
        return {
            "sku": f"TEST{datetime.now().timestamp()}",
            "name": "Test Product",
            "regular_price": "99.90",
            "stock_quantity": 100,
            "manage_stock": True
        }
    
    @pytest.fixture
    async def media_service(self, woo_service):
        return WooCommerceMediaService(woo_service)
    
    @pytest.mark.asyncio
    async def test_product_sync_flow(self, woo_service, media_service):
        # Test verisi
        product_data = {
            "name": "Test Sync Product",
            "regular_price": "20.00",
            "images": []
        }
        
        # Ürün oluştur
        product = await woo_service.create_product(product_data)
        product_id = product["id"]
        
        # Görsel ekle
        image_path = "tests/fixtures/test_image.jpg"
        image_result = await media_service.upload_image(
            image_path,
            title="Test Image"
        )
        
        # Görseli ürüne ekle
        await media_service.attach_image_to_product(
            product_id,
            image_result["id"]
        )
        
        # Kontrol et
        updated_product = await woo_service.get_product(product_id)
        assert len(updated_product["images"]) == 1
        
        # Temizlik
        await woo_service.delete_product(product_id)
    
    @pytest.mark.asyncio
    async def test_stock_sync(self, sync_service, test_product):
        """Test stock synchronization."""
        # 1. Initial sync
        result = await sync_service.sync_product(test_product)
        
        # 2. Update stock in Wolvox
        new_stock = 50
        await sync_service.wolvox.update_stock(
            test_product["sku"],
            new_stock
        )
        
        # 3. Sync stock
        await sync_service.sync_stock(test_product["sku"])
        
        # 4. Verify WooCommerce stock
        woo_product = await sync_service.woo.get_product(result.woo_id)
        assert woo_product["stock_quantity"] == new_stock
    
    @pytest.mark.asyncio
    async def test_price_sync(self, sync_service, test_product):
        """Test price synchronization."""
        # 1. Initial sync
        result = await sync_service.sync_product(test_product)
        
        # 2. Update price in Wolvox
        new_price = "149.90"
        await sync_service.wolvox.update_price(
            test_product["sku"],
            new_price
        )
        
        # 3. Sync price
        await sync_service.sync_price(test_product["sku"])
        
        # 4. Verify WooCommerce price
        woo_product = await sync_service.woo.get_product(result.woo_id)
        assert woo_product["regular_price"] == new_price
    
    @pytest.mark.asyncio
    async def test_sync_error_handling(self, sync_service):
        """Test sync error handling."""
        # 1. Try to sync non-existent product
        with pytest.raises(Exception) as exc_info:
            await sync_service.sync_product({
                "sku": "NONEXISTENT",
                "name": "Test Product"
            })
        assert "Product not found" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_bulk_sync(self, sync_service):
        """Test bulk synchronization."""
        # 1. Prepare test products
        products = [
            {
                "sku": f"BULK{i}",
                "name": f"Bulk Product {i}",
                "regular_price": "99.90",
                "stock_quantity": 100
            }
            for i in range(3)
        ]
        
        # 2. Bulk sync
        results = await sync_service.bulk_sync_products(products)
        
        # 3. Verify results
        assert len(results) == len(products)
        assert all(r.status == "success" for r in results)
        
        # 4. Verify all products synced
        for product in products:
            woo_product = await sync_service.woo.get_product_by_sku(product["sku"])
            assert woo_product is not None
            
            wolvox_product = await sync_service.wolvox.get_product_by_sku(product["sku"])
            assert wolvox_product is not None
    
    @pytest.mark.asyncio
    async def test_sync_with_variants(self, sync_service):
        """Test product sync with variants."""
        # 1. Prepare product with variants
        product = {
            "sku": "VAR001",
            "name": "Variable Product",
            "type": "variable",
            "variations": [
                {
                    "sku": "VAR001-S",
                    "attributes": [{"name": "Size", "option": "S"}],
                    "regular_price": "99.90",
                    "stock_quantity": 10
                },
                {
                    "sku": "VAR001-M",
                    "attributes": [{"name": "Size", "option": "M"}],
                    "regular_price": "99.90",
                    "stock_quantity": 20
                }
            ]
        }
        
        # 2. Sync product
        result = await sync_service.sync_product(product)
        
        # 3. Verify variants
        woo_product = await sync_service.woo.get_product(result.woo_id)
        assert len(woo_product["variations"]) == 2
        
        # 4. Verify variant stock
        for variation in product["variations"]:
            wolvox_variant = await sync_service.wolvox.get_product_by_sku(variation["sku"])
            assert wolvox_variant["stock"] == variation["stock_quantity"] 