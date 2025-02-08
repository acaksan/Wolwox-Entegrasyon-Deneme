from unittest.mock import Mock, patch

import pytest
from services.woocommerce_media_service import WooCommerceMediaService


def test_validate_image():
    service = WooCommerceMediaService(Mock(), "user", "pass")
    
    # Geçerli görsel
    assert service._validate_image("valid.jpg") == True
    
    # Büyük dosya
    with pytest.raises(Exception):
        service._validate_image("large.jpg")

@pytest.mark.asyncio
class TestMediaService:
    async def test_upload_image(self, media_service):
        image_path = "tests/fixtures/test_image.jpg"
        result = await media_service.upload_image(
            image_path,
            title="Test Image"
        )
        assert result["title"] == "Test Image"
        assert "id" in result
        
    async def test_attach_image(self, media_service, woo_service):
        # Test ürünü oluştur
        product = await woo_service.create_product({
            "name": "Test Product",
            "regular_price": "10.00"
        })
        
        # Görsel yükle ve ekle
        image = await media_service.upload_image(
            "tests/fixtures/test_image.jpg"
        )
        await media_service.attach_image_to_product(
            product["id"],
            image["id"]
        )
        
        # Kontrol et
        updated = await woo_service.get_product(product["id"])
        assert len(updated["images"]) == 1
        
        # Temizlik
        await woo_service.delete_product(product["id"]) 