"""WooCommerce medya yükleme testleri"""

import logging
from pathlib import Path

import pytest
from PIL import Image
from src.services.woocommerce_media_service import woo_media_service

logger = logging.getLogger(__name__)

@pytest.fixture
def test_image():
    """Test görseli oluşturur"""
    # Test görseli yolu
    image_path = Path("tests/fixtures/test_image.jpg")
    image_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Eğer görsel yoksa oluştur
    if not image_path.exists():
        # 100x100 kırmızı test görseli
        img = Image.new('RGB', (100, 100), color='red')
        img.save(image_path)
    
    return str(image_path)

@pytest.mark.asyncio
async def test_media_upload(test_image):
    """Medya yükleme testi"""
    try:
        # Görseli yükle
        result = await woo_media_service.upload_image(
            image_path=test_image,
            title="Test Görsel",
            alt_text="Test Alt Text",
            caption="Test Açıklama"
        )
        
        # Sonuçları kontrol et
        assert result["id"] > 0
        assert result["title"]["rendered"] == "Test Görsel"
        assert result["alt_text"] == "Test Alt Text"
        assert result["caption"]["rendered"] == "<p>Test Açıklama</p>\n"  # HTML formatında
        
        logger.info(f"✅ Görsel başarıyla yüklendi: ID={result['id']}")
        logger.info(f"✅ URL: {result['source_url']}")
        
        # Yüklenen görseli sil
        deleted = await woo_media_service.delete_image(result["id"], force=True)
        assert deleted is True
        logger.info(f"✅ Görsel başarıyla silindi: ID={result['id']}")
        
    except Exception as e:
        logger.error(f"❌ Test hatası: {str(e)}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    pytest.main(["-v", __file__]) 