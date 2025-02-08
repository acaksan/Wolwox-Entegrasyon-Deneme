import pytest
from services.woocommerce_service import WooCommerceService
from services.woocommerce_tag_service import WooCommerceTagService


@pytest.fixture
async def tag_service():
    woo_service = WooCommerceService()
    return WooCommerceTagService(woo_service)

@pytest.mark.integration
class TestWooCommerceTag:
    
    async def test_create_tag(self, tag_service):
        """Etiket oluşturma testi"""
        tag_name = "Test Etiketi"
        result = await tag_service.create_tag(tag_name)
        assert isinstance(result, dict)
        assert result.get("name") == tag_name
        return result["id"]
        
    async def test_get_tags(self, tag_service):
        """Etiketleri listeleme testi"""
        tags = await tag_service.get_tags()
        assert isinstance(tags, list)
        print(f"✅ {len(tags)} etiket listelendi")
        
    async def test_assign_tags(self, tag_service, test_product):
        """Etiket atama testi"""
        tag_id = await self.test_create_tag(tag_service)
        result = await tag_service.assign_tags(test_product, [tag_id])
        assert tag_id in [t["id"] for t in result.get("tags", [])]
        print("✅ Etiket ürüne atandı") 