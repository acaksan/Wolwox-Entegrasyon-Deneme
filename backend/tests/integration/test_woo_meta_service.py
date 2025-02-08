import pytest
from services.woocommerce_meta_service import WooCommerceMetaService
from services.woocommerce_service import WooCommerceService


@pytest.fixture
async def meta_service():
    woo_service = WooCommerceService()
    return WooCommerceMetaService(woo_service)

@pytest.mark.integration
class TestWooCommerceMeta:
    
    test_product_id = 123  # Test ürün ID'si
    
    async def test_update_product_meta(self, meta_service, test_product):
        """Meta veri güncelleme testi"""
        result = await meta_service.update_product_meta(
            test_product,
            {"test_key": "test_value"}
        )
        assert result["meta_data"]
        print("✅ Meta veriler güncellendi")
        
    async def test_get_product_meta(self, meta_service, test_product):
        """Meta veri getirme testi"""
        meta_data = await meta_service.get_product_meta(test_product)
        assert isinstance(meta_data, list)
        print(f"✅ {len(meta_data)} meta veri alındı")
        
    async def test_get_specific_meta(self, meta_service, test_product):
        """Belirli meta veri getirme testi"""
        # Önce test verisi ekle
        await meta_service.update_product_meta(
            test_product,
            {"test_meta_key": "test_value"}
        )
        
        meta_data = await meta_service.get_product_meta(
            test_product,
            "test_meta_key"
        )
        assert isinstance(meta_data, list)
        assert all(m["key"] == "test_meta_key" for m in meta_data)
        print("✅ Belirli meta veri alındı") 